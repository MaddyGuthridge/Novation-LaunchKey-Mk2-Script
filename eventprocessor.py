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
import internalconstants
import config
import processdefault
import processfirst
import processfirst_basic
import lighting

import WindowProcessors.processwindows as processwindows
import PluginProcessors.processplugins as processplugins
import NoteProcessors.processnotes as processnotes
import ControllerProcessors.keys as keys


# Recieve event and forward onto relative processors
def processExtended(command):

    try:

        # Process internal commands
        if command.recieved_internal:
            processReceived(command)
            return

        # Process error events
        if internal.errors.getError():
            internal.errors.eventProcessError(command)
            return

        # Reset idle timer
        if not ((command.type is eventconsts.TYPE_BASIC_PAD or command.type is eventconsts.TYPE_PAD or command.type is eventconsts.TYPE_TRANSPORT) and not command.is_lift):
            if lighting.idle_show_active():
                command.handle("End Idle Light Show")
            internal.window.reset_idle_tick()

        # Process key mappings
        keys.process(command)
        
        # Call primary processor
        processfirst.process(command)

        if command.handled: return

        # Shouldn't be called in extended mode
        """ # Attempt to process event using custom processors for plugins
        processplugins.process(command)

        if command.handled: return"""

        # Process content from windows
        processwindows.process(command)

        # If command hasn't been handled by any above uses, use the default controls
        if command.handled is False:
            processdefault.process(command)

    except Exception as e:
        internal.errors.triggerError(e)

def processBasic(command):

    # Send event to reset other controller
    internal.sendCompleteInternalMidiMessage(internalconstants.MESSAGE_RESET_INTERNAL_CONTROLLER)

    try:

        if command.recieved_internal:
            processReceived(command)
            return

        # For note events, use note processors
        if command.type == eventconsts.TYPE_NOTE:
            processnotes.process(command)
            return

        # Now process other events for errors.
        if internal.errors.getError():
            internal.errors.eventProcessError(command)
            return
        
        # Call primary processor
        processfirst_basic.process(command)

        if command.handled: return

        # Attempt to process event using custom processors for plugins
        processplugins.process(command)

        if command.handled: return

    except Exception as e:
        internal.errors.triggerError(e)

# Processes events received internally
def processReceived(command):
    command.actions.addProcessor("Internal event processor")

    if command.getDataMIDI() == internalconstants.MESSAGE_RESET_INTERNAL_CONTROLLER:
        internal.window.reset_idle_tick()
        command.handle("Reset idle tick", True)

    if command.getDataMIDI() == internalconstants.MESSAGE_ERROR_CRASH:
        internal.errors.triggerErrorFromOtherScript()
        command.handle("Trigger error state")

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
        
    lights = lighting.LightMap()

    if internal.errors.getError():
        internal.errors.redrawError(lights)
        lighting.state.setFromMap(lights)
        return

    # Error handling: set controller into an error state
    try:

        # Draws idle thing if idle
        lighting.idle_lightshow(lights)

        # Get UI from primary processor
        processfirst.redraw(lights)

        # Get UI drawn from plugins
        processplugins.redraw(lights)

        # Get UI drawn from windows
        processwindows.redraw(lights)

        # Get UI drawn from default processor
        processdefault.redraw(lights)

    except Exception as e:
        internal.errors.triggerError(e)


    # Call pads refresh function
    lighting.state.setFromMap(lights)

# Stores a single action as a string
class Action:
    def __init__(self, act, silent):
        self.act = act
        self.silent = silent

class ActionList:
    def __init__(self, name):
        self.name = name
        self.list = []
        self.didHandle = False

    # Append action to the list
    def appendAction(self, action, silent, handle):
        self.list.append(Action(action, silent))

        # Set flag indicating that this processor handled the event
        if handle:
            self.didHandle = True

    def getString(self):
        # Return that no action was taken if list is empty
        if len(self.list) == 0:
            return internal.getTab(self.name + ":", 2) + "[No actions]"

        # No indentation required if there was only one action
        elif len(self.list) == 1:
            ret = internal.getTab(self.name + ":", 2) + self.list[0].act

        # If there are multiple actions, indent them
        else:
            ret = self.name + ":"
            for i in range(len(self.list)):
                ret += '\n' + internal.getTab("") + self.list[i].act

        if self.didHandle:
            ret += '\n' + internal.getTab("") + "[Handled]"
        return ret

    # Returns the latest non-silent action to set as the hint message
    def getHintMsg(self):
        ret = ""
        for i in range(len(self.list)):
            if self.list[i].silent == False:
                ret = self.list[i].act
        return ret

# Stores actions taken by various processor modules
class actionPrinter:
    

    def __init__(self):
        # String that is output after each event is processed
        self.eventProcessors = []

    # Add an event processor object
    def addProcessor(self, name):
        self.eventProcessors.append(ActionList(name))

    # Add to event action
    def appendAction(self, act, silent=False, handled=False):

        # Add some random processor if a processor doesn't exist for some reason
        if len(self.eventProcessors) == 0:
            self.addProcessor("NoProcessor")
            internal.debugLog("Added NoProcessor Processor", internalconstants.DEBUG_WARNING_DEPRECIATED_FEATURE)
        # Append the action
        self.eventProcessors[len(self.eventProcessors) - 1].appendAction(act, silent, handled)

    def flush(self):
        # Log all actions taken
        for x in range(len(self.eventProcessors)):
            internal.debugLog(self.eventProcessors[x].getString(), internalconstants.DEBUG_EVENT_ACTIONS)

        # Get hint message to set (ignores silent messages)
        hint_msg = ""
        for x in range(len(self.eventProcessors)):
            cur_msg = self.eventProcessors[x].getHintMsg()

            # Might want to fix this some time, some handler modules append this manually
            if cur_msg != "" and cur_msg != "[Did not handle]":
                hint_msg = cur_msg

        if hint_msg != "":
            ui.setHintMsg(hint_msg)
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
        self.recieved_internal = False
        self.edited = False
        self.actions = actionPrinter()

        self.handled = False

        self.status = event.status
        
        self.note = event.data1
        self.data1 = event.data1
        
        self.value = event.data2
        self.data2 = event.data2
        
        self.status_nibble = event.status >> 4              # Get first half of status byte
        self.channel = event.status & int('00001111', 2)    # Get 2nd half of status byte
        
        if self.channel == 14:
            self.recieved_internal = True

        # PME Flags to make sure errors don't happen or something
        self.flags = event.pmeFlags

        # Add sysex information
        self.sysex = event.sysex

        # Bit-shift status and data bytes to get event ID
        self.id = (self.status + (self.note << 8))

        self.shifted = False

        self.parse()  
        
        # Process shift button
        if self.id == config.SHIFT_BUTTON:
            if self.is_lift:
                self.handled = internal.shift.lift(self.is_double_click)
            else:
                internal.shift.press(self.is_double_click)
        elif internal.shift.getDown():
            self.shifted = internal.shift.use(self.is_lift)

        # Process sysex events
        if self.type is eventconsts.TYPE_SYSEX_EVENT:
            internal.processSysEx(self)

                                                                                                                               

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
            self.coord_X = self.note - 0x15

        elif self.id in eventconsts.BasicKnobs: 
            self.type = eventconsts.TYPE_BASIC_KNOB
            self.coord_X = self.note - 0x15

        elif self.id in eventconsts.Faders: 
            self.type = eventconsts.TYPE_FADER
            self.coord_X = self.note - 0x29
            if self.note == 0x07: self.coord_X = 8

        elif self.id in eventconsts.BasicFaders: 
            self.type = eventconsts.TYPE_BASIC_FADER
            self.coord_X = self.note - 0x29
            if self.note == 0x07: self.coord_X = 8

        elif self.id in eventconsts.FaderButtons: 
            self.type = eventconsts.TYPE_FADER_BUTTON
            self.coord_X = self.note - 0x33
            self.isBinary = True

        elif self.id in eventconsts.BasicFaderButtons: 
            self.type = eventconsts.TYPE_BASIC_FADER_BUTTON
            self.coord_X = self.note - 0x33
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
                    self.coord_X = x
                    self.coord_Y = y
                    self.isBinary = True
                    if self.isPadExtendedMode():
                        self.type = eventconsts.TYPE_PAD
                    else:
                        self.type = eventconsts.TYPE_BASIC_PAD
            else:
                self.type = eventconsts.TYPE_NOTE
                self.isBinary = True

        # Detect basic circular pads
        elif self.status == 0xB0 and self.note in eventconsts.BasicPads[8]:
            self.type = eventconsts.TYPE_BASIC_PAD
            self.coord_X = 8
            self.coord_Y = eventconsts.BasicPads[8].index(self.note)
            self.isBinary = True
        
        # Also check for basic mode buttons
        
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
    
    def handle(self, action, silent=False):
        self.handled = True
        self.actions.appendAction(action, silent, True)

    # Returns event info as string
    def getInfo(self):
        out = "Event:"
        out = internal.getTab(out)

        # Event type and ID
        temp = self.getType()
        out += temp
        out = internal.getTab(out)

        # Event value
        temp = self.getValue()
        out += temp
        out = internal.getTab(out)

        # Event full data
        temp = self.getDataString()
        out += temp
        out = internal.getTab(out)

        if self.is_double_click:
            out += "[Double Click]"
            out = internal.getTab(out)
        
        if self.is_long_press:
            out += "[Long Press]"
            out = internal.getTab(out)
        
        if self.shifted:
            out += "[Shifted]"
            out = internal.getTab(out)
        
        if self.id == config.SHIFT_BUTTON:
            out += "[Shift Key]"
            out = internal.getTab(out)

        return out

    # Prints event info
    def printInfo(self):
        internal.debugLog(self.getInfo(), internalconstants.DEBUG_EVENT_DATA)
    
    # Prints event output
    def printOutput(self):

        internal.debugLog("", internalconstants.DEBUG_EVENT_ACTIONS)
        self.actions.flush()
        if self.handled:
            internal.debugLog("[Event was handled]", internalconstants.DEBUG_EVENT_ACTIONS)
        else: 
            internal.debugLog("[Event wasn't handled]", internalconstants.DEBUG_EVENT_ACTIONS)

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
        a = internal.getTab(a)
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
        return str(self.coord_X + 1)

    # Returns string eventID for fader events
    def getID_FaderButton(self):
        return str(self.coord_X + 1)
    
    def getID_Knobs(self):
        return str(self.coord_X + 1)
    
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
        if self.note == eventconsts.Pads[self.coord_X][self.coord_Y]: return True
        elif self.note == eventconsts.BasicPads[self.coord_X][self.coord_Y]: return False
        else: print("ERROR!!?")

    # Returns (formatted) value
    def getValue(self):
        a = str(self.value)
        b = ""
        if self.isBinary:
            if self.value == 0:
                b = "(Off)"
            else: b = "(On)"
        a = internal.getTab(a, length=5)
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
        return internal.toMidiMessage(self.status, self.note, self.value)


    
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
