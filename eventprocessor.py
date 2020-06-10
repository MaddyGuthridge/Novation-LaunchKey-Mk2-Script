"""
eventprocessor.py
This file processes events and returns objects for events.

"""

import device

import eventconsts
import internal



class processedEvent:
    def __init__(self, event):
        
        # Number of spaces per column in output
        self.TAB_INDENT = 16
        
        # Bit-shift status and data bytes to get event ID
        self.id = (event.status + (event.data1 << 8))

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
        #elif self.id in eventconsts.Knobs: 
        #    self.type = eventconsts.TYPE_KNOB
        elif self.id in eventconsts.Faders: 
            self.type = eventconsts.TYPE_FADER
        elif self.id in eventconsts.FaderButtons: 
            self.type = eventconsts.TYPE_FADER_BUTTON
            self.isBinary = True
        else: 
            # Check for pads is different as they use multiple signals
            temp = self.id // 0x100
            if temp in eventconsts.Pads:
                self.type = eventconsts.TYPE_PAD
                self.isBinary = True
        
        self.value = event.data2

        if self.value is 0: self.is_Lift = True
        else: self.is_Lift = False
        
        self.handled = False
        self.is_long_press = False

        # Process double presses only for lifted buttons
        self.is_double_click = False
        if self.is_Lift is True and self.isBinary is True: 
            self.is_double_click = device.isDoubleClick(internal.toMidiMessage(event.status, event.data1, event.data2))

        

        
    
    # Prints event data
    def printOut(self):

        out = "Event: "

        # Event type and ID
        temp = self.getType()
        out += temp

        # Event value
        temp = self.getValue()
        out += temp + internal.getTab(self.TAB_INDENT - len(temp))

        # Event full data
        temp = self.getDataString()
        out += temp + internal.getTab(self.TAB_INDENT - len(temp))

        # Handled
        if self.handled is False:
            temp = " [Unhandled]"
        else: temp = " [Handled]"
        out += temp + internal.getTab(self.TAB_INDENT - len(temp))

        if self.is_double_click:
            out += " [Double Click]"
        
        if self.is_long_press:
            out += " [Long Press]"


        
        
        print(out)

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
        elif self.type is eventconsts.TYPE_KNOB: 
            a = "Knob"
        elif self.type is eventconsts.TYPE_FADER: 
            a = "Fader"
        elif self.type is eventconsts.TYPE_FADER_BUTTON: 
            a = "Fader Button"
        elif self.type is eventconsts.TYPE_PAD: 
            a = "Pad"
        else: 
            internal.logError("Bad event type")
            a = "ERROR!!!"

        return a + internal.getTab(self.TAB_INDENT - len(a)) + b + internal.getTab(self.TAB_INDENT - len(b))

    # Returns string event ID for system events
    def getID_System(self):
        if self.id == eventconsts.SYSTEM_IN_CONTROL: return "InControl"
        elif self.id == eventconsts.SYSTEM_MISC: return "Misc"
        else: return "ERROR"

    # Returns string event ID for InControl events
    def getID_InControl(self):
        if self.id == eventconsts.INCONTROL_KNOBS: return "Knobs"
        elif self.id == eventconsts.INCONTROL_FADERS: return "Faders"
        elif self.id == eventconsts.INCONTROL_PADS: return "Pads"
        else: return "ERROR"

    # Returns string event ID for transport events
    def getID_Transport(self):
        if self.id == eventconsts.TRANSPORT_BACK: return "Back"
        elif self.id == eventconsts.TRANSPORT_FORWARD: return "Forward"
        elif self.id == eventconsts.TRANSPORT_STOP: return "Stop"
        elif self.id == eventconsts.TRANSPORT_PLAY: return "Play"
        elif self.id == eventconsts.TRANSPORT_LOOP: return "Loop"
        elif self.id == eventconsts.TRANSPORT_RECORD: return "Record"
        elif self.id == eventconsts.TRANSPORT_TRACK_NEXT: return "Next Track"
        elif self.id == eventconsts.TRANSPORT_TRACK_PREVIOUS: return "Previous Track"
        else: return "ERROR"
    
    # Returns (formatted) value
    def getValue(self):
        a = str(self.value)
        b = ""
        if self.isBinary:
            if self.value == 0:
                b = "(Off)"
            else: b = "(On)"
        return a + internal.getTab(5 - len(a)) + b

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
