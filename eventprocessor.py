"""
eventprocessor.py
This file processes events and returns objects for events.

"""

import device

import eventconsts
import internal



class processedEvent:
    def __init__(self, event):

        # Bit-shift status and data bytes to get event ID
        self.id = (event.status + (event.data1 << 8))

        # Indicates whether to consider as a value or as an on/off
        self.isBinary = False

        # Determine type of event | unrecognised by default
        self.type = eventconsts.TYPE_UNRECOGNISED
        if self.id in eventconsts.InControlButtons: 
            self.type = eventconsts.TYPE_INCONTROL
            self.isBinary = True
        if self.id in eventconsts.SystemMessages: 
            self.type = eventconsts.TYPE_SYSTEM_MSG
            self.isBinary = True
        if self.id in eventconsts.TransportControls: 
            self.type = eventconsts.TYPE_TRANSPORT
            self.isBinary = True
        #if self.id in eventconsts.Knobs: 
        #    self.type = eventconsts.TYPE_KNOB
        if self.id in eventconsts.Faders: 
            self.type = eventconsts.TYPE_FADER
        
        # Check for pads is different as they use multiple signals
        temp = self.id // 0x100
        if temp in eventconsts.Pads:
            self.type = eventconsts.TYPE_PAD
        
        self.handled = False
        self.is_long_press = False
        self.is_double_press = device.isDoubleClick(internal.toMidiMessage(event.status, event.data1, event.data2))

        self.value = event.data2

        if self.value is 0: self.is_Lift = True
        else: self.is_Lift = False

        
    
    # Prints event data
    def printOut(self):

        TAB_INDENT = 16

        out = "Event: "

        # Event type
        temp = self.getType()
        out += temp + internal.getTab(TAB_INDENT - len(temp))
        
        # Event ID
        temp = self.getId()
        out += temp + internal.getTab(TAB_INDENT - len(temp))

        # Event value
        temp = str(self.value)
        out += temp + internal.getTab(TAB_INDENT - len(temp))

        # Event full data
        temp = self.getFullData()
        out += temp + internal.getTab(TAB_INDENT - len(temp))

        if self.is_double_press:
            out += " [Double click]"

        if self.handled is False:
            out += " [Unhandled]"
        
        print(out)

    def getType(self):
        if self.type is eventconsts.TYPE_UNRECOGNISED: return "Unrecognised"
        elif self.type is eventconsts.TYPE_SYSTEM_MSG: return "System"
        elif self.type is eventconsts.TYPE_INCONTROL: return "InControl"
        elif self.type is eventconsts.TYPE_TRANSPORT: return "Transport"
        elif self.type is eventconsts.TYPE_KNOB: return "Knob"
        elif self.type is eventconsts.TYPE_FADER: return "Fader"
        elif self.type is eventconsts.TYPE_MIXER_BUTTON: return "Mixer Button"
        elif self.type is eventconsts.TYPE_PAD: return "Pad"
        else: 
            internal.logError("Bad event type")
            return "ERROR!!!"

    def getId(self):
        # TODO: set up string returner thing for ID
        a = ""

        return a

    def getFullData(self):
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

        return a

    
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
