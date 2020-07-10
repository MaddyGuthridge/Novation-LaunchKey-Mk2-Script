"""
eventprocessor.py
This file processes events and returns objects for events.

"""

import time

import device
import ui
import utils

import eventconsts
import internal
import config
import processdefault
import processfirst
import lighting
import WindowProcessors.processwindows as processwindows
import PluginProcessors.processplugins as processplugins



# Recieve event and forward onto relative processors
def process(command):
    
    # If basic processor, don't bother for note events
    if internal.PORT == config.DEVICE_PORT_BASIC and command.type == eventconsts.TYPE_NOTE:
        return
    
    # Call primary processor
    processfirst.process(command)

    if command.handled: return

    # Attempt to process event using custom processors for plugins
    processplugins.process(command)

    if command.handled: return

    # Process content from windows
    processwindows.process(command)

    # If command hasn't been handled by any above uses, use the default controls
    if command.handled is False:
        processdefault.process(command)

# Called after a window is activated
def activeStart():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
        if internal.window.plugin_focused:
            processplugins.activeStart()
        else:
            processwindows.activeStart()

# Called just before active window is deactivated
def activeEnd():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
        if internal.window.plugin_focused:
            processplugins.activeEnd()
        else:
            processwindows.activeEnd()

def redraw():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:

        lights = lighting.LightMap()

        # Get UI from primary processor
        processfirst.redraw(lights)

        # Get UI drawn from plugins
        processplugins.redraw(lights)

        # Get UI drawn from windows
        processwindows.redraw(lights)

        # Get UI drawn from default processor
        processdefault.redraw(lights)

        # Call pads refresh function
        lighting.state.setFromMap(lights)

# Stores actions taken by various processor modules
class actionPrinter:
    

    def __init__(self):
        # String that is output after each event is processed
        self.eventActions = [""]
        self.eventProcessors = [""]

    # Set event processor
    def addProcessor(self, string):
        if self.eventProcessors[0] == "":
            self.eventProcessors[0] = string
        else:
            if self.eventActions[len(self.eventActions) - 1] == "":
                self.eventActions[len(self.eventActions) - 1] = "[Did not handle]"
            self.eventProcessors.append(string)
            self.eventActions.append("")

    # Add to event action
    def appendAction(self, string):
        self.eventActions[len(self.eventProcessors) - 1] += string
        self.eventActions[len(self.eventProcessors) - 1] = internal.newGetTab(self.eventActions[len(self.eventProcessors) - 1])

    def flush(self):
        for x in range(len(self.eventProcessors)):
            out = self.eventProcessors[x]
            out = internal.newGetTab(out, 2)
            out += self.eventActions[x]
            print(out)
            if self.eventActions[x] != "" and not "[Did not handle]" in self.eventActions[x]:
                ui.setHintMsg(self.eventActions[x])

        self.eventActions.clear()
        self.eventProcessors.clear()

# Stores event in raw form. Used to edit events
class rawEvent:
    def __init__(self, status, data1, data2, shift = False):
        self.status = status
        self.data1 = data1
        self.data2 = data2
        self.shift = shift

# Stores useful data about processed event
class processedEvent:
    def __init__(self, event):
        self.edited = False
        self.actions = actionPrinter()

        self.handled = False

        self.status = event.status
        self.note = event.data1
        self.value = event.data2
        self.status_nibble = event.status >> 4              # Get first half of status byte
        self.channel = event.status & int('00001111', 2)    # Get 2nd half of status byte
        
        # Add sysex information
        self.sysex = event.sysex

        # Bit-shift status and data bytes to get event ID
        self.id = (self.status + (self.note << 8))

        self.shifted = False

        self.parse()  
        
        # Process shift button
        if self.id == config.SHIFT_BUTTON:
            if self.is_lift:
                if self.is_double_click and config.ENABLE_STICKY_SHIFT:
                    internal.shift.set_sticky()
                else:
                    self.handled = internal.shift.lift()
            else:
                internal.shift.press()

            if internal.shift.get_sticky():
                self.handle("Deactivate Held Shift")

        elif internal.shift.get_sticky():
            if self.isBinary:
                if self.is_lift:
                    internal.shift.use_sticky()
                    self.shifted = True

        # Process sysex events
        if self.type is eventconsts.TYPE_SYSEX_EVENT:
            internal.processSysEx(self)

        elif internal.shift.getDown():
            self.shifted = internal.shift.use()

                                                                                                                                     

    def parse(self):
        # Indicates whether to consider as a value or as an on/off
        self.isBinary = False

        # Determine type of event | unrecognised by default
        self.type = eventconsts.TYPE_UNRECOGNISED

        # If using basic port, check for notes

        if self.status == eventconsts.SYSEX:
            self.type = eventconsts.TYPE_SYSEX_EVENT

        elif self.id in eventconsts.InControlButtons: 
            self.type = eventconsts.TYPE_INCONTROL
            self.isBinary = True

        elif self.id in eventconsts.SystemMessages: 
            self.type = eventconsts.TYPE_SYSTEM_MSG
            self.isBinary = True

        elif self.id in eventconsts.TransportControls: 
            self.type = eventconsts.TYPE_TRANSPORT
            self.isBinary = True

        elif self.id in eventconsts.Knobs: 
            self.type = eventconsts.TYPE_KNOB

        elif self.id in eventconsts.BasicKnobs: 
            self.type = eventconsts.TYPE_BASIC_KNOB

        elif self.id in eventconsts.Faders: 
            self.type = eventconsts.TYPE_FADER

        elif self.id in eventconsts.BasicFaders: 
            self.type = eventconsts.TYPE_BASIC_FADER

        elif self.id in eventconsts.FaderButtons: 
            self.type = eventconsts.TYPE_FADER_BUTTON
            self.isBinary = True
        
        elif self.id in eventconsts.BasicEvents:
            self.type = eventconsts.TYPE_BASIC_EVENT
            if self.id == eventconsts.PEDAL:
                self.isBinary = True

        elif self.status_nibble == eventconsts.NOTE_ON or self.status_nibble == eventconsts.NOTE_OFF:
        # Pads are actually note events
            if (self.status == 0x9F or self.status == 0x8F) or ((self.status == 0x99 or self.status == 0x89)):
                x, y = self.getPadCoord()
                if x != -1 and y != -1:
                    # Is a pad
                    self.padX = x
                    self.padY = y
                    self.isBinary = True
                    if self.isPadExtendedMode():
                        self.type = eventconsts.TYPE_PAD
                    else:
                        self.type = eventconsts.TYPE_BASIC_PAD
            else:
                self.type = eventconsts.TYPE_NOTE


        # And also different signals for the mixer buttons in basic mode
        # TODO: FIX THIS
        elif self.status == 0xB0 and self.note in eventconsts.BasicPads:
            self.type = eventconsts.TYPE_BASIC_PAD
            self.isBinary = True
        
        
        # Check if buttons were lifted
        if self.value is 0: 
            self.is_lift = True
        else: 
            self.is_lift = False
        
        

        # Process long presses: TODO
        self.is_long_press = False

        # Process double presses (seperate for lifted and pressed buttons)
        self.is_double_click = False
        if self.isBinary is True: 
            if self.is_lift is True:
                self.is_double_click = isDoubleClickLift(self.id)
            elif self.is_lift is False and self.isBinary is True: 
                self.is_double_click = isDoubleClickPress(self.id)
        
    def edit(self, event):
        self.edited = True
        self.status = event.status
        self.note = event.data1
        self.value = event.data2
        self.shifted = event.shift

        # Bit-shift status and data bytes to get event ID
        self.id = (self.status + (self.note << 8))

        self.parse()

        newEventStr = "Changed event: \n" + self.getInfo()

        self.actions.appendAction(newEventStr)
    
    def handle(self, action):
        self.handled = True
        self.actions.appendAction(action)

    # Returns event info as string
    def getInfo(self):
        out = "Event:"
        out = internal.newGetTab(out)

        # Event type and ID
        temp = self.getType()
        out += temp
        out = internal.newGetTab(out)

        # Event value
        temp = self.getValue()
        out += temp
        out = internal.newGetTab(out)

        # Event full data
        temp = self.getDataString()
        out += temp
        out = internal.newGetTab(out)

        if self.is_double_click:
            out += "[Double Click]"
            out = internal.newGetTab(out)
        
        if self.is_long_press:
            out += "[Long Press]"
            out = internal.newGetTab(out)
        
        if self.shifted:
            out += "[Shifted]"
            out = internal.newGetTab(out)
        
        if self.id == config.SHIFT_BUTTON:
            out += "[Shift Key]"
            out = internal.newGetTab(out)

        return out

    # Prints event info
    def printInfo(self):
        print(self.getInfo())
    
    # Prints event output
    def printOutput(self):

        print("")
        self.actions.flush()
        if self.handled:
            print("[Event was handled]")
        else: 
            print("[Event wasn't handled]")

    # Returns string with type and ID of event
    def getType(self):
        a = ""
        b = ""
        if self.type is eventconsts.TYPE_UNRECOGNISED: 
            a = "Unrecognised"
        elif self.type is eventconsts.TYPE_SYSEX_EVENT:
            a = "Sysex"
        elif self.type is eventconsts.TYPE_NOTE:
            a = "Note"
            b = utils.GetNoteName(self.note) + " (Ch. " + str(self.channel) + ')'
        elif self.type is eventconsts.TYPE_SYSTEM_MSG: 
            a = "System"
            b = self.getID_System()
        elif self.type is eventconsts.TYPE_INCONTROL: 
            a = "InControl"
            b = self.getID_InControl()
        elif self.type is eventconsts.TYPE_TRANSPORT: 
            a = "Transport"
            b = self.getID_Transport()
        elif self.type is eventconsts.TYPE_KNOB or self.type is eventconsts.TYPE_BASIC_KNOB: 
            a = "Knob"
            b = self.getID_Knobs()
        elif self.type is eventconsts.TYPE_FADER or self.type is eventconsts.TYPE_BASIC_FADER: 
            a = "Fader"
            b = self.getID_Fader()
        elif self.type is eventconsts.TYPE_FADER_BUTTON or self.type is eventconsts.TYPE_BASIC_FADER_BUTTON: 
            a = "Fader Button"
            b = self.getID_FaderButton()
        elif self.type is eventconsts.TYPE_PAD or self.type is eventconsts.TYPE_BASIC_PAD: 
            a = "Pad"
            b = self.getID_Pads()
        elif self.type is eventconsts.TYPE_BASIC_EVENT:
            a = "Basic Event"
            b = self.getID_Basic()
        else: 
            internal.debugLog("Bad event type")
            a = "ERROR!!!"
        a = internal.newGetTab(a)
        return a + b

    # Returns string event ID for system events
    def getID_System(self):
        if   self.id == eventconsts.SYSTEM_EXTENDED: return "InControl"
        elif self.id == eventconsts.SYSTEM_MISC: return "Misc"
        else: return "ERROR"

    # Returns string event ID for InControl events
    def getID_InControl(self):
        if   self.id == eventconsts.INCONTROL_KNOBS: return "Knobs"
        elif self.id == eventconsts.INCONTROL_FADERS: return "Faders"
        elif self.id == eventconsts.INCONTROL_PADS: return "Pads"
        else: return "ERROR"
    
    # Returns string event ID for basic events
    def getID_Basic(self):
        if self.id == eventconsts.PEDAL: return "Pedal"
        elif self.id == eventconsts.MOD_WHEEL: return "Modulation"
        elif self.id == eventconsts.PITCH_BEND: return "Pitch Bend"
        else: return "ERROR"

    # Returns string event ID for transport events
    def getID_Transport(self):
        if   self.id == eventconsts.TRANSPORT_BACK: return "Back"
        elif self.id == eventconsts.TRANSPORT_FORWARD: return "Forward"
        elif self.id == eventconsts.TRANSPORT_STOP: return "Stop"
        elif self.id == eventconsts.TRANSPORT_PLAY: return "Play"
        elif self.id == eventconsts.TRANSPORT_LOOP: return "Loop"
        elif self.id == eventconsts.TRANSPORT_RECORD: return "Record"
        elif self.id == eventconsts.TRANSPORT_TRACK_NEXT: return "Next Track"
        elif self.id == eventconsts.TRANSPORT_TRACK_PREVIOUS: return "Previous Track"
        else: return "ERROR"
    
    # Returns string eventID for knob events
    def getID_Pads(self):
        x_map, y_map = self.getPadCoord()
        
        ret_str = ""

        if y_map == 0:   ret_str += "Top "
        elif y_map == 1: ret_str += "Bottom "
        else: return "ERROR"
        if x_map == 8:
            ret_str += "Button"
            return ret_str
        ret_str += str(x_map + 1)

        return ret_str
    
    # Returns string eventID for fader events
    def getID_Fader(self):
        if   self.id == eventconsts.FADER_1 or self.id == eventconsts.BASIC_FADER_1: return "1"
        elif self.id == eventconsts.FADER_2 or self.id == eventconsts.BASIC_FADER_2: return "2"
        elif self.id == eventconsts.FADER_3 or self.id == eventconsts.BASIC_FADER_3: return "3"
        elif self.id == eventconsts.FADER_4 or self.id == eventconsts.BASIC_FADER_4: return "4"
        elif self.id == eventconsts.FADER_5 or self.id == eventconsts.BASIC_FADER_5: return "5"
        elif self.id == eventconsts.FADER_6 or self.id == eventconsts.BASIC_FADER_6: return "6"
        elif self.id == eventconsts.FADER_7 or self.id == eventconsts.BASIC_FADER_7: return "7"
        elif self.id == eventconsts.FADER_8 or self.id == eventconsts.BASIC_FADER_8: return "8"
        elif self.id == eventconsts.FADER_9 or self.id == eventconsts.BASIC_FADER_9: return "9 / Master"
        else: return "ERROR"

    # Returns string eventID for fader events
    def getID_FaderButton(self):
        if   self.id == eventconsts.FADER_BUTTON_1 or self.id == eventconsts.BASIC_FADER_BUTTON_1: return "1"
        elif self.id == eventconsts.FADER_BUTTON_2 or self.id == eventconsts.BASIC_FADER_BUTTON_2: return "2"
        elif self.id == eventconsts.FADER_BUTTON_3 or self.id == eventconsts.BASIC_FADER_BUTTON_3: return "3"
        elif self.id == eventconsts.FADER_BUTTON_4 or self.id == eventconsts.BASIC_FADER_BUTTON_4: return "4"
        elif self.id == eventconsts.FADER_BUTTON_5 or self.id == eventconsts.BASIC_FADER_BUTTON_5: return "5"
        elif self.id == eventconsts.FADER_BUTTON_6 or self.id == eventconsts.BASIC_FADER_BUTTON_6: return "6"
        elif self.id == eventconsts.FADER_BUTTON_7 or self.id == eventconsts.BASIC_FADER_BUTTON_7: return "7"
        elif self.id == eventconsts.FADER_BUTTON_8 or self.id == eventconsts.BASIC_FADER_BUTTON_8: return "8"
        elif self.id == eventconsts.FADER_BUTTON_9 or self.id == eventconsts.BASIC_FADER_BUTTON_9: return "9 / Master"
        else: return "ERROR"
    
    def getID_Knobs(self):
        if   self.id == eventconsts.KNOB_1 or self.id == eventconsts.BASIC_KNOB_1: return "1"
        elif self.id == eventconsts.KNOB_2 or self.id == eventconsts.BASIC_KNOB_2: return "2"
        elif self.id == eventconsts.KNOB_3 or self.id == eventconsts.BASIC_KNOB_3: return "3"
        elif self.id == eventconsts.KNOB_4 or self.id == eventconsts.BASIC_KNOB_4: return "4"
        elif self.id == eventconsts.KNOB_5 or self.id == eventconsts.BASIC_KNOB_5: return "5"
        elif self.id == eventconsts.KNOB_6 or self.id == eventconsts.BASIC_KNOB_6: return "6"
        elif self.id == eventconsts.KNOB_7 or self.id == eventconsts.BASIC_KNOB_7: return "7"
        elif self.id == eventconsts.KNOB_8 or self.id == eventconsts.BASIC_KNOB_8: return "8"
    
    # Returns X and Y tuple for pads
    def getPadCoord(self):
        y_map = -1
        x_map = -1
        done_flag = False
        for x in range(len(eventconsts.Pads)):
            for y in range(len(eventconsts.Pads[x])):
                if self.note == eventconsts.Pads[x][y] or self.note == eventconsts.BasicPads[x][y]:
                    y_map = y
                    x_map = x
                    done_flag = True
                    break
            if done_flag: break
        return x_map, y_map

    # Returns True if Pad is Extended
    def isPadExtendedMode(self):
        if self.note == eventconsts.Pads[self.padX][self.padY]: return True
        elif self.note == eventconsts.BasicPads[self.padX][self.padY]: return False
        else: print("ERROR!!?")

    # Returns (formatted) value
    def getValue(self):
        a = str(self.value)
        b = ""
        if self.isBinary:
            if self.value == 0:
                b = "(Off)"
            else: b = "(On)"
        a = internal.newGetTab(a, length=5)
        return a + b

    # Returns string with (formatted) hex of event
    def getDataString(self):

        if self.type is eventconsts.TYPE_SYSEX_EVENT:
            return str(self.sysex)

        # Append hex value of ID
        a = str(hex(self.id + (self.value << 16)))
        # If string requires leading zeros
        if len(a) is 7: a = "0x0" + a[2:].upper()
        elif len(a) is 6: a = "0x00" + a[2:].upper()
        elif len(a) is 5: a = "0x000" + a[2:].upper()
        elif len(a) is 4: a = "0x0000" + a[2:].upper()
        elif len(a) is 3: a = "0x00000" + a[2:].upper()
        elif len(a) is 2: a = "0x000000" + a[2:].upper()
        else: a = "0x" + a[2:].upper()

        a = a[:2] + " " + a[2:4] + " " + a[4:6] + " " + a[6:8]
        
        return a

    # Returns int with hex of event
    def getDataMIDI(self):
        return hex(self.id + (self.value << 16))


    
# Internal functions

# Convert between Extended Mode pad mappings and Basic Mode pad mappings
def convertPadMapping(padNumber):
    for y in range(len(eventconsts.Pads)):
        for x in range(len(eventconsts.Pads[y])):
            if padNumber == eventconsts.Pads[y][x]:
                return eventconsts.BasicPads[y][x]
    internal.debugLog("Pad number note defined")

# Returns true if is a double click for a press
lastPressID = -1
lastPressTime = -1
def isDoubleClickPress(id):
    global lastPressID
    global lastPressTime
    ret = False
    currentTime = time.perf_counter()
    if id == lastPressID and (currentTime - lastPressTime < config.DOUBLE_PRESS_TIME):
        ret = True
    lastPressID = id
    lastPressTime = currentTime
    return ret

# Returns true if is a double click for a lift
lastLiftID = -1
lastLiftTime = -1
def isDoubleClickLift(id):
    global lastLiftID
    global lastLiftTime
    ret = False
    currentTime = time.perf_counter()
    if id == lastLiftID and (currentTime - lastLiftTime < config.DOUBLE_PRESS_TIME):
        ret = True
    lastLiftID = id
    lastLiftTime = currentTime
    return ret
