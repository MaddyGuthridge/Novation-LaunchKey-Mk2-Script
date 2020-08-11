"""
processorhelpers.py

This script includes objects useful for event processors. 
It is worth investigating potential applications of these functions when writing your processors, 
or adding other frequently-required functions here.

Author: Miguel Guthridge
"""

import time

import utils
import ui

import config
import eventconsts
import internal
import internalconstants


class UiModeHandler: 
    """This object is used to manage menu layers, which can be toggled and switched through.
        It is best used in handler scripts to allow for a plugin or window to have multiple menus.
    """
    
    def __init__(self, num_modes):
        """Create instance of UIModeHandler.

        Args:
            num_modes (int): The number of different menus to be contained in the object
        """
        self.mode = 0
        self.num_modes = num_modes

    # Switch to next mode
    def nextMode(self):
        """Jump to the next menu layer

        Returns:
            int: mode number
        """
        self.mode += 1
        if self.mode == self.num_modes:
            self.mode = 0
        
        return self.mode

    def resetMode(self):
        """Resets menu layer to zero
        """
        self.mode = 0

    # Get current mode number
    def getMode(self):
        """Returns mode number

        Returns:
            int: mode number
        """
        return self.mode

def snap(value, snapTo):
    """Returns a snapped value

    Args:
        value (float): value being snapped
        snapTo (float): value to snap to

    Returns:
        float: value after snapping
    """
    if abs(value - snapTo) <= config.SNAP_RANGE and config.ENABLE_SNAPPING:
        return snapTo
    else: return value

def didSnap(value, snapTo):
    """Returns a boolean indicating whether a value was snapped

    Args:
        value (float): value being snapped
        snapTo (float): value to snap to

    Returns:
        bool: whether the value would snap
    """
    if abs(value - snapTo) <= config.SNAP_RANGE and config.ENABLE_SNAPPING:
        return True
    else: return False

def toFloat(value, min = 0, max = 1):
    """Converts a MIDI event value (data2) to a float to set parameter values.

    Args:
        value (int): MIDI event value (0-127)
        min (float, optional): lower value to set between. Defaults to 0.
        max (float, optional): upper value to set between. Defaults to 1.

    Returns:
        float: range value
    """
    return (value / 127) * (max - min) + min

class ExtensibleNote():
    """A note with other notes tacked on. Used for playing chords in note processors.
    """
    def __init__(self, root_note, extended_notes):
        """Create instance of ExtensibleNote object

        Args:
            root_note (note event): the note that the user pressed (or a modified version of it). 
                Can be of type RawEvent, ProcessedEvent or FLMidiMessage.
                
            extended_notes (list of note events): List of notes that should also be pressed. Can be of 
                same types as root_note, but RawEvent is recommended for performance reasons.
        """
        self.root = root_note
        self.extended_notes = extended_notes


def convertPadMapping(padNumber):
    """Converts between basic mode pad mapping and extended mode mapping

    Args:
        padNumber (int): note number for extended pad

    Returns:
        int: note number for basic pad
    """
    for y in range(len(eventconsts.Pads)):
        for x in range(len(eventconsts.Pads[y])):
            if padNumber == eventconsts.Pads[y][x]:
                return eventconsts.BasicPads[y][x]


lastPressID = -1
lastPressTime = -1
def isDoubleClickPress(id):
    """Returns whether a press event was a double click

    Args:
        id (int): Event ID

    Returns:
        bool: whether the event was a double click
    """
    global lastPressID
    global lastPressTime
    ret = False
    currentTime = time.perf_counter()
    if id == lastPressID and (currentTime - lastPressTime < config.DOUBLE_PRESS_TIME):
        ret = True
    lastPressID = id
    lastPressTime = currentTime
    return ret


lastLiftID = -1
lastLiftTime = -1
def isDoubleClickLift(id):
    """Returns whether a lift event was a double click

    Args:
        id (int): Event ID

    Returns:
        bool: whether the event was a double click
    """
    global lastLiftID
    global lastLiftTime
    ret = False
    currentTime = time.perf_counter()
    if id == lastLiftID and (currentTime - lastLiftTime < config.DOUBLE_PRESS_TIME):
        ret = True
    lastLiftID = id
    lastLiftTime = currentTime
    return ret



class Action:
    """Stores an action as a string
    """
    def __init__(self, act, silent):
        """Create an event action

        Args:
            act (str): The action taken
            silent (bool): Whether the action should be set as a hint message
        """
        self.act = act
        self.silent = silent

class ActionList:
    """Stores a list of actions taken by a single processor
    """
    def __init__(self, name):
        """Create an action list

        Args:
            name (str): Name of the processor
        """
        self.name = name
        self.list = []
        self.didHandle = False

    
    def appendAction(self, action, silent, handle):
        """Append action to list of actions

        Args:
            action (str): The action taken
            silent (bool): Whether the action should be set as a hint message
            handle (bool): Whether this action handled the event
        """
        self.list.append(Action(action, silent))

        # Set flag indicating that this processor handled the event
        if handle:
            self.didHandle = True

    def getString(self):
        """Returns a string of the actions taken

        Returns:
            str: actions taken
        """
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
        """Returns string of hint message to set, empty string if none

        Returns:
            str: Hint message
        """
        ret = ""
        for i in range(len(self.list)):
            if self.list[i].silent == False:
                ret = self.list[i].act
        return ret


class ActionPrinter:
    """Object containing actions taken by all processor modules
    """

    def __init__(self):
        # String that is output after each event is processed
        self.eventProcessors = []

    
    def addProcessor(self, name):
        """Add an event processor

        Args:
            name (str): Name of the processor
        """
        self.eventProcessors.append(ActionList(name))

    
    def appendAction(self, act, silent=False, handled=False):
        """Appends an action to the current event processor

        Args:
            act (str): The action taken
            silent (bool, optional): Whether the action should be set as a hint message. Defaults to False.
            handled (bool, optional): Whether the action handled the event. Defaults to False.
        """

        # Add some random processor if a processor doesn't exist for some reason
        if len(self.eventProcessors) == 0:
            self.addProcessor("NoProcessor")
            internal.debugLog("Added NoProcessor Processor", internalconstants.DEBUG_WARNING_DEPRECIATED_FEATURE)
        # Append the action
        self.eventProcessors[len(self.eventProcessors) - 1].appendAction(act, silent, handled)

    def flush(self):
        """Log all actions taken, and set a hint message if applicable
        """
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


class RawEvent:
    """Stores event in raw form. A quick way to generate events for editing.
    """
    def __init__(self, status, data1, data2, shift = False):
        """Create a RawEvent object

        Args:
            status (int): Status byte
            data1 (int): First data byte
            data2 (int): 2nd data byte
            shift (bool, optional): Whether the event is shifted. Defaults to False.
        """
        self.status = status
        self.data1 = data1
        self.data2 = data2
        self.shift = shift


class ProcessedEvent:
    """Stores data about an event, including useful parsed data
    """
    def __init__(self, event):
        """Create ProcessedEvent from event object

        Args:
            event (MIDI Event): FL Studio MIDI Event
        """
        self.recieved_internal = False
        self.edited = False
        self.actions = ActionPrinter()

        self.handled = False

        self.status = event.status
        
        self.note = event.data1
        self.data1 = event.data1
        
        self.value = event.data2
        self.data2 = event.data2
        
        self.status_nibble = event.status >> 4              # Get first half of status byte
        self.channel = event.status & int('00001111', 2)    # Get 2nd half of status byte
        
        if self.channel == internalconstants.INTERNAL_CHANNEL_STATUS:
            self.recieved_internal = True

        # PME Flags to make sure errors don't happen or something
        self.processPmeFlags(event.pmeFlags)

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
        elif internal.shift.getDown() and self.type not in internalconstants.SHIFT_IGNORE_TYPES:
            self.shifted = internal.shift.use(self.is_lift)

        # Process sysex events
        if self.type is eventconsts.TYPE_SYSEX_EVENT:
            internal.processSysEx(self)
                                                                                                          
    def parse(self):
        """Parses information about the event
        """
        
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
        
        if self.recieved_internal:
            self.type = eventconsts.TYPE_INTERNAL_EVENT
        
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
        """Edit the event to change data

        Args:
            event (RawEvent): A MIDI Event to change this event to
        """
        self.edited = True
        
        self.status = event.status
        
        self.note = event.data1
        self.data1 = event.data1
        
        self.value = event.data2
        self.data2 = event.data2
        
        self.status_nibble = event.status >> 4              # Get first half of status byte
        self.channel = event.status & int('00001111', 2)    # Get 2nd half of status byte
        
        self.shifted = event.shift

        # Bit-shift status and data bytes to get event ID
        self.id = (self.status + (self.note << 8))

        self.parse()

        newEventStr = "Changed event: \n" + self.getInfo()

        self.actions.appendAction(newEventStr)
    
    def handle(self, action, silent=False):
        """Handles the event

        Args:
            action (str): The action that handled the event
            silent (bool, optional): Whether the action should be set as a hint message. Defaults to False.
        """
        self.handled = True
        self.actions.appendAction(action, silent, True)

    def act(self, action):
        """Adds an action to the event without handling it

        Args:
            action (str): The action taken
        """
        self.actions.appendAction(action, False, False)

    def addProcessor(self, name):
        """Adds an event processor to the processor list

        Args:
            name (str): Name of processor
        """
        self.actions.addProcessor(name)
    
    def getInfo(self):
        """Returns info about event

        Returns:
            str: Details about the event
        """
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

    
    def printInfo(self):
        """Prints string info about event
        """
        internal.debugLog(self.getInfo(), internalconstants.DEBUG_EVENT_DATA)
    
    
    def printOutput(self):
        """Prints actions taken whilst handling event
        """
        internal.debugLog("", internalconstants.DEBUG_EVENT_ACTIONS)
        self.actions.flush()
        if self.handled:
            internal.debugLog("[Event was handled]", internalconstants.DEBUG_EVENT_ACTIONS)
        else: 
            internal.debugLog("[Event wasn't handled]", internalconstants.DEBUG_EVENT_ACTIONS)

    
    def getType(self):
        """Returns string detailing type and ID of event

        Returns:
            str: Type and ID of event info
        """
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
        elif self.type is eventconsts.TYPE_PAD: 
            a = "Pad"
            b = self.getID_Pads()
        elif self.type is eventconsts.TYPE_BASIC_PAD:
            a = "Pad (Basic)"
            b = self.getID_Pads()
        elif self.type is eventconsts.TYPE_BASIC_EVENT:
            a = "Basic Event"
            b = self.getID_Basic()
        elif self.type is eventconsts.TYPE_INTERNAL_EVENT:
            a = "Internal event"
        else: 
            internal.debugLog("Bad event type")
            a = "ERROR!!!"
        a = internal.getTab(a)
        return a + b

    def processPmeFlags(self, flags):
        """Processes PME flags on event (Currently very broken)

        Args:
            flags (int): PME flags
        """
        #print(flags)
        bin_string = format(flags, '8b')[:5]
        #print(bin_string)
        flags_list = [x == '1' for x in bin_string]
        self.pme_system = flags_list[0]
        
        self.pme_system_safe = flags_list[1]
        
        self.pme_preview_note = flags_list[2]
        
        self.pme_from_host = flags_list[3]
        
        self.pme_from_midi = flags_list[4]
        

    def getID_System(self):
        """Returns string event ID for system events

        Returns:
            str: Event ID details
        """
        if   self.id == eventconsts.SYSTEM_EXTENDED: return "InControl"
        elif self.id == eventconsts.SYSTEM_MISC: return "Misc"
        else: return "ERROR"

    
    def getID_InControl(self):
        """Returns string event ID for InControl events

        Returns:
            str: Event ID details
        """
        if   self.id == eventconsts.INCONTROL_KNOBS: return "Knobs"
        elif self.id == eventconsts.INCONTROL_FADERS: return "Faders"
        elif self.id == eventconsts.INCONTROL_PADS: return "Pads"
        else: return "ERROR"
    
    
    def getID_Basic(self):
        """Returns string event ID for basic events

        Returns:
            str: Event ID Details
        """
        if self.id == eventconsts.PEDAL: return "Pedal"
        elif self.id == eventconsts.MOD_WHEEL: return "Modulation"
        elif self.id == eventconsts.PITCH_BEND: return "Pitch Bend"
        else: return "ERROR"

    
    def getID_Transport(self):
        """Returns string event ID for transport events

        Returns:
            str: Event ID details
        """
        if   self.id == eventconsts.TRANSPORT_BACK: return "Back"
        elif self.id == eventconsts.TRANSPORT_FORWARD: return "Forward"
        elif self.id == eventconsts.TRANSPORT_STOP: return "Stop"
        elif self.id == eventconsts.TRANSPORT_PLAY: return "Play"
        elif self.id == eventconsts.TRANSPORT_LOOP: return "Loop"
        elif self.id == eventconsts.TRANSPORT_RECORD: return "Record"
        elif self.id == eventconsts.TRANSPORT_TRACK_NEXT: return "Next Track"
        elif self.id == eventconsts.TRANSPORT_TRACK_PREVIOUS: return "Previous Track"
        else: return "ERROR"
    
    
    def getID_Pads(self):
        """Returns string eventID for pad events

        Returns:
            str: Event ID details
        """
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
    
    
    def getID_Fader(self):
        """Returns string eventID for fader events

        Returns:
            str: Event ID details
        """
        return str(self.coord_X + 1)


    def getID_FaderButton(self):
        """Returns string eventID for fader button events

        Returns:
            str: Event ID details
        """
        return str(self.coord_X + 1)
    
    def getID_Knobs(self):
        """Returns string eventID for knob events

        Returns:
            str: Event ID details
        """
        return str(self.coord_X + 1)
    
    
    def getPadCoord(self):
        """Returns X, Y coordinates for pad events

        Returns:
            int: X
            int: Y
        """
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

    
    def isPadExtendedMode(self):
        """Returns True if Pad is Extended

        Returns:
            bool: whether pad is extended
        """
        if self.note == eventconsts.Pads[self.coord_X][self.coord_Y]: return True
        elif self.note == eventconsts.BasicPads[self.coord_X][self.coord_Y]: return False
        else: print("ERROR!!?")

    
    def getValue(self):
        """Returns (formatted) value of event  

        Returns:
            str: Formatted value (data2) of event
        """
        a = str(self.value)
        b = ""
        if self.isBinary:
            if self.value == 0:
                b = "(Off)"
            else: b = "(On)"
        a = internal.getTab(a, length=5)
        return a + b

    
    def getDataString(self):
        """Returns string with (formatted) hex of event

        Returns:
            str: hex of event
        """
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

    
    def getDataMIDI(self):
        """Returns int with hex of event

        Returns:
            int: MIDI event
        """
        return internal.toMidiMessage(self.status, self.note, self.value)


