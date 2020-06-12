"""
eventprocessor.py
This file processes events and returns objects for events.

"""

import time

import device
import ui

import eventconsts
import internal
import config

shiftDown = False
shiftUsed = False

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
            self.eventProcessors.append(string)
            self.eventActions.append("")

    # Add to event action
    def appendAction(self, string):
        self.eventActions[len(self.eventProcessors) - 1] += string
        self.eventActions[len(self.eventProcessors) - 1] = internal.newGetTab(self.eventActions[len(self.eventProcessors) - 1])

    def flush(self):
        for x in range(len(self.eventProcessors)):
            out = self.eventProcessors[x]
            out = internal.newGetTab(out)
            out += self.eventActions[x]
            print(out)
            ui.setHintMsg(self.eventActions[x])

        self.eventActions.clear()
        self.eventProcessors.clear()

class processedEvent:
    def __init__(self, event):

        self.actions = actionPrinter()

        self.handled = False

        self.status = event.status
        self.note = event.data1
        self.value = event.data2
        
        # Bit-shift status and data bytes to get event ID
        self.id = (event.status + (event.data1 << 8))

        self.shifted = False

        global shiftDown
        global shiftUsed
        # Process shift button
        if self.id == config.SHIFT_BUTTON:
            if self.value == 127:
                shiftUsed = False
                shiftDown = True
            elif self.value == 0:
                shiftDown = False
                if shiftUsed:
                    self.handled = True
        elif shiftDown:
            self.shifted = True
            shiftUsed = True

        # Indicates whether to consider as a value or as an on/off
        self.isBinary = False

        # Determine type of event | unrecognised by default
        self.type = eventconsts.TYPE_UNRECOGNISED
        if self.id in eventconsts.InControlButtons: 
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
        # Pads have different signals for note on and note off
        elif (self.status == 0x9F or self.status == 0x8F) and self.note in eventconsts.Pads:
            self.type = eventconsts.TYPE_PAD
            self.isBinary = True
        elif (self.status == 0x99 or self.status == 0x89) and self.note in eventconsts.BasicPads:
            self.type = eventconsts.TYPE_BASIC_PAD
            self.isBinary = True
        # And also different signals for the buttons in basic mode
        elif self.status == 0xB0 and self.note in eventconsts.BasicPads:
            self.type = eventconsts.TYPE_BASIC_PAD
            self.isBinary = True
        
        
        # Check if buttons were lifted
        if self.value is 0: self.is_Lift = True
        else: self.is_Lift = False
        
        

        # Process long presses: TODO
        self.is_long_press = False

        # Process double presses (seperate for lifted and pressed buttons)
        self.is_double_click = False
        if self.isBinary is True: 
            if self.is_Lift is True:
                self.is_double_click = isDoubleClickLift(self.id)
            elif self.is_Lift is False and self.isBinary is True: 
                self.is_double_click = isDoubleClickPress(self.id)                                                                                                                                

        

        
    
    # Prints event data
    def printOut(self):

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

        # Handled
        if self.handled is False:
            temp = " [Unhandled]"
        else: temp = " [Handled]"
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


        
        
        print(out)
        self.actions.flush()

    # Returns string with type and ID of event
    def getType(self):
        a = ""
        b = ""
        if self.type is eventconsts.TYPE_UNRECOGNISED: 
            a = "Unrecognised"
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
        else: 
            internal.logError("Bad event type")
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
        if   self.note == eventconsts.PAD_TOP_1 or self.note == eventconsts.BASIC_PAD_TOP_1: return "Top 1"
        elif self.note == eventconsts.PAD_TOP_2 or self.note == eventconsts.BASIC_PAD_TOP_2: return "Top 2"
        elif self.note == eventconsts.PAD_TOP_3 or self.note == eventconsts.BASIC_PAD_TOP_3: return "Top 3"
        elif self.note == eventconsts.PAD_TOP_4 or self.note == eventconsts.BASIC_PAD_TOP_4: return "Top 4"
        elif self.note == eventconsts.PAD_TOP_5 or self.note == eventconsts.BASIC_PAD_TOP_5: return "Top 5"
        elif self.note == eventconsts.PAD_TOP_6 or self.note == eventconsts.BASIC_PAD_TOP_6: return "Top 6"
        elif self.note == eventconsts.PAD_TOP_7 or self.note == eventconsts.BASIC_PAD_TOP_7: return "Top 7"
        elif self.note == eventconsts.PAD_TOP_8 or self.note == eventconsts.BASIC_PAD_TOP_8: return "Top 8"

        elif self.note == eventconsts.PAD_BOTTOM_1 or self.note == eventconsts.BASIC_PAD_BOTTOM_1: return "Bottom 1"
        elif self.note == eventconsts.PAD_BOTTOM_2 or self.note == eventconsts.BASIC_PAD_BOTTOM_2: return "Bottom 2"
        elif self.note == eventconsts.PAD_BOTTOM_3 or self.note == eventconsts.BASIC_PAD_BOTTOM_3: return "Bottom 3"
        elif self.note == eventconsts.PAD_BOTTOM_4 or self.note == eventconsts.BASIC_PAD_BOTTOM_4: return "Bottom 4"
        elif self.note == eventconsts.PAD_BOTTOM_5 or self.note == eventconsts.BASIC_PAD_BOTTOM_5: return "Bottom 5"
        elif self.note == eventconsts.PAD_BOTTOM_6 or self.note == eventconsts.BASIC_PAD_BOTTOM_6: return "Bottom 6"
        elif self.note == eventconsts.PAD_BOTTOM_7 or self.note == eventconsts.BASIC_PAD_BOTTOM_7: return "Bottom 7"
        elif self.note == eventconsts.PAD_BOTTOM_8 or self.note == eventconsts.BASIC_PAD_BOTTOM_8: return "Bottom 8"

        elif self.note == eventconsts.PAD_TOP_BUTTON or self.note == eventconsts.BASIC_PAD_TOP_BUTTON: return "Top Button"
        elif self.note == eventconsts.PAD_BOTTOM_BUTTON or self.note == eventconsts.BASIC_PAD_BOTTOM_BUTTON: return "Bottom Button"

        else: return "ERROR"
    
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
    
    # Returns (formatted) value
    def getValue(self):
        a = str(self.value)
        b = ""
        if self.isBinary:
            if self.value == 0:
                b = "(Off)"
            else: b = "(On)"
        a = internal.newGetTab(a, 5)
        return a + b

    # Returns string with (formatted) hex of event
    def getDataString(self):
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
    if padNumber is eventconsts.PAD_TOP_1: return eventconsts.BASIC_PAD_TOP_1
    elif padNumber is eventconsts.PAD_TOP_2: return eventconsts.BASIC_PAD_TOP_2
    elif padNumber is eventconsts.PAD_TOP_3: return eventconsts.BASIC_PAD_TOP_3
    elif padNumber is eventconsts.PAD_TOP_4: return eventconsts.BASIC_PAD_TOP_4
    elif padNumber is eventconsts.PAD_TOP_5: return eventconsts.BASIC_PAD_TOP_5
    elif padNumber is eventconsts.PAD_TOP_6: return eventconsts.BASIC_PAD_TOP_6
    elif padNumber is eventconsts.PAD_TOP_7: return eventconsts.BASIC_PAD_TOP_7
    elif padNumber is eventconsts.PAD_TOP_8: return eventconsts.BASIC_PAD_TOP_8
    elif padNumber is eventconsts.PAD_BOTTOM_1: return eventconsts.BASIC_PAD_BOTTOM_1
    elif padNumber is eventconsts.PAD_BOTTOM_2: return eventconsts.BASIC_PAD_BOTTOM_2
    elif padNumber is eventconsts.PAD_BOTTOM_3: return eventconsts.BASIC_PAD_BOTTOM_3
    elif padNumber is eventconsts.PAD_BOTTOM_4: return eventconsts.BASIC_PAD_BOTTOM_4
    elif padNumber is eventconsts.PAD_BOTTOM_5: return eventconsts.BASIC_PAD_BOTTOM_5
    elif padNumber is eventconsts.PAD_BOTTOM_6: return eventconsts.BASIC_PAD_BOTTOM_6
    elif padNumber is eventconsts.PAD_BOTTOM_7: return eventconsts.BASIC_PAD_BOTTOM_7
    elif padNumber is eventconsts.PAD_BOTTOM_8: return eventconsts.BASIC_PAD_BOTTOM_8
    elif padNumber is eventconsts.PAD_TOP_BUTTON: return eventconsts.BASIC_PAD_TOP_BUTTON
    elif padNumber is eventconsts.PAD_BOTTOM_BUTTON: return eventconsts.BASIC_PAD_BOTTOM_BUTTON
    internal.logError("Pad number not defined")

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
