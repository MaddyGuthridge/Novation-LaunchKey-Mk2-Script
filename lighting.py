"""
lighting.py
This file contains functions and constants related to controlling lights on the controller.

"""


import time

import internal
import eventconsts
import eventprocessor
import internalconstants

# LightMap is sent around to collect colours on UI redraws
class LightMap:
    def __init__(self):
        # 0 = off, 1-127 = colour
        self.reset()
    
    # Set all pads to off      
    def reset(self):

        # 0 = unfrozen, 1 = frozen
        self.FrozenMap = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

        # 0 = off, 1-127 = colour
        self.PadColours = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

        # 0 = off, 1 = on, 2 = pulse, negative = flash
        self.PadStates = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

    # Set the colour of a pad
    def setPadColour(self, x, y, colour, state = 3, override = False):
        if self.FrozenMap[x][y] == 0 or override: # If pad available to map
            self.PadColours[x][y] = colour
            self.PadStates[x][y] = state
            self.solidifyPad(x, y)
            return True
        else: return False
    
    # Sets colours based on state of LightMap object
    def setFromMatrix(self, map, state=3, override = False):
        for x in range(len(self.FrozenMap)):
            for y in range(len(self.FrozenMap[x])):
                if self.FrozenMap[x][y] == 0 or override:
                    self.setPadColour(x, y, map[x][y], state, override)
        return


    # Prevents pad from being overwritten
    def solidifyPad(self, x, y):
        if self.FrozenMap[x][y] == 0: # If pad available to map
            self.FrozenMap[x][y] = 1
    
    # Prevents row from being overwritten
    def solidifyRow(self, y):
        for x in range(len(self.FrozenMap)):
            if self.FrozenMap[x][y] == 0: self.FrozenMap[x][y] = 1
    
    # Prevents column from being overwritten
    def solidifyColumn(self, x):
        for y in range(len(self.FrozenMap)):
            if self.FrozenMap[x][y] == 0: self.FrozenMap[x][y] = 1

    # Prevents all pads from being overwritten
    def solidifyAll(self):
        for x in range(len(self.FrozenMap)):
            for y in range(len(self.FrozenMap[x])):
                self.solidifyPad(x, y)

# Lights manages state of pad lights
class Lights:
    def __init__(self):
        # 0 = off, 1-127 = colour
        self.PadColours = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

        # 0 = off, 1 = on, 2 = pulse, negative = flash
        self.PadStates = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

    # Set all pads to off      
    def reset(self):
        
        internal.sendMidiMessage(0xBF, 0x00, 0x00)
        internal.debugLog("Sent lighting reset signal", internalconstants.DEBUG_LIGHTING_RESET)
        internal.window.reset_animation_tick()
        self.__init__()

    # Set the colour of a pad
    def setPadColour(self, x, y, colour, state = 3, override = False):

        # Handle light offs
        if colour == 0 and state == 3:
            state = 0

        # Set legacy state
        elif state == 3:
            state = 1

        if state == 0:
            colour = 0

        # Check if pad is already in that state - don't bother with event if so
        if self.PadColours[x][y] == colour and self.PadStates[x][y] == state and not override:
            return

        # Set state variables
        self.PadColours[x][y] = colour
        self.PadStates[x][y] = state

        status_a = 0x9
        status_b = 0xF

        if state == 0:
            status_a = 0x8

        elif state == 2:
            status_b = 0x2

        elif state < 0:
            status_b = 0xF

        # Round pads in basic mode
        if x == 8 and not internal.extendedMode.query(eventconsts.INCONTROL_PADS):
            status_a = 0xB

        # Calculate Status
        status = (status_a << 4) + status_b

        if internal.extendedMode.query(eventconsts.INCONTROL_PADS): 
            internal.sendMidiMessage(status, eventconsts.Pads[x][y], colour)
            internal.debugLog("Sent lighting command [" + str(x) + ", " + str(y) + "] (InControl Enabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
            
        else: 
            internal.sendMidiMessage(status, eventprocessor.convertPadMapping(eventconsts.Pads[x][y]), colour)
            internal.debugLog("Sent lighting command [" + str(x) + ", " + str(y) + "] (InControl Disabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
        
        if state < 0: # Send extra event to trigger flashing
            status_b = 0x1
            status = (status_a << 4) + status_b

            if internal.extendedMode.query(eventconsts.INCONTROL_PADS): 
                
                internal.sendMidiMessage(status, eventconsts.Pads[x][y], -state)
                internal.debugLog("Sent light flash command [" + str(x) + ", " + str(y) + "] (InControl Enabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
                
            else: 
                internal.sendMidiMessage(status, eventprocessor.convertPadMapping(eventconsts.Pads[x][y]), -state)
                internal.debugLog("Sent light flash command [" + str(x) + ", " + str(y) + "] (InControl Disabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
    
    # Sets colours based on state of LightMap object
    def setFromMap(self, map):
        map.solidifyAll()
        for x in range(len(self.PadColours)):
            for y in range(len(self.PadColours[x])):
                self.setPadColour(x, y, map.PadColours[x][y], map.PadStates[x][y])
        return
    
    def redraw(self):
        for x in range(len(self.PadColours)):
            for y in range(len(self.PadColours[x])):
                self.setPadColour(x, y, self.PadColours[x][y], override=True)

state = Lights()

# OoooOooOOOooO PREETTTTTYYYY!!!!!!
def lightShow():

    state.reset()

    sleepTime = 0.05
    x = 0
    if internal.SHARED_INIT_OK:
        if internal.SCRIPT_UPDATE_AVAILABLE:
            rainbowColours = [COLOUR_BLUE, COLOUR_LIGHT_BLUE, COLOUR_LIGHT_BLUE, COLOUR_GREEN, COLOUR_GREEN, COLOUR_LIGHT_BLUE, COLOUR_LIGHT_BLUE, COLOUR_BLUE, COLOUR_OFF] 
        else:
            rainbowColours = [COLOUR_RED, COLOUR_PINK, COLOUR_PURPLE, COLOUR_BLUE, COLOUR_LIGHT_BLUE, COLOUR_GREEN, COLOUR_YELLOW, COLOUR_ORANGE, COLOUR_OFF]
    else:
        rainbowColours = [COLOUR_YELLOW, COLOUR_ORANGE, COLOUR_ORANGE, COLOUR_RED, COLOUR_RED, COLOUR_ORANGE, COLOUR_ORANGE, COLOUR_YELLOW, COLOUR_OFF] 


    while True:

        time.sleep(sleepTime)

        # Group 1
        if (x >= 0) and (x < len(rainbowColours)):
            state.setPadColour(0, 1, rainbowColours[x])
        
         # Group 2
        if (x >= 1) and (x < len(rainbowColours) + 1):
            state.setPadColour(1, 1, rainbowColours[x - 1])
            state.setPadColour(0, 0, rainbowColours[x - 1])
        
        # Group 3
        if (x >= 2) and (x < len(rainbowColours) + 2):
            state.setPadColour(2, 1, rainbowColours[x - 2])
            state.setPadColour(1, 0, rainbowColours[x - 2])
        
        # Group 4
        if (x >= 3) and (x < len(rainbowColours) + 3):
            state.setPadColour(3, 1, rainbowColours[x - 3])
            state.setPadColour(2, 0, rainbowColours[x - 3])
        
        # Group 5
        if (x >= 4) and (x < len(rainbowColours) + 4):
            state.setPadColour(4, 1, rainbowColours[x - 4])
            state.setPadColour(3, 0, rainbowColours[x - 4])
        
    
        # Group 6
        if (x >= 5) and (x < len(rainbowColours) + 5):
            state.setPadColour(5, 1, rainbowColours[x - 5])
            state.setPadColour(4, 0, rainbowColours[x - 5])
        
        # Group 7
        if (x >= 6) and (x < len(rainbowColours) + 6):
            state.setPadColour(6, 1, rainbowColours[x - 6])
            state.setPadColour(5, 0, rainbowColours[x - 6])
        
        # Group 8
        if (x >= 7) and (x < len(rainbowColours) + 7):
            state.setPadColour(7, 1, rainbowColours[x - 7])
            state.setPadColour(6, 0, rainbowColours[x - 7])
        
        # Group 9
        if (x >= 8) and (x < len(rainbowColours) + 8):
            state.setPadColour(7, 0, rainbowColours[x - 8])
        
        x += 1
       
        
        if x > len(rainbowColours) + 8: break

    state.reset()



# Define colour codes
COLOUR_TRANSPARENT = -1
COLOUR_OFF = 0
COLOUR_WHITE = 3
COLOUR_RED = 5
COLOUR_GREEN = 25
COLOUR_PINK = 53
COLOUR_BLUE = 46
COLOUR_YELLOW = 13
COLOUR_PURPLE = 49
COLOUR_LILAC = 116
COLOUR_ORANGE = 84

COLOUR_LIGHT_YELLOW = 109
COLOUR_LIGHT_BLUE = 37
COLOUR_LIGHT_LILAC = 116
COLOUR_LIGHT_LIGHT_BLUE = 40

COLOUR_DARK_GREY = 1
COLOUR_DARK_PURPLE = 51
COLOUR_DARK_BLUE = 47
COLOUR_DARK_RED = 59



# Define UI colours
UI_NAV_VERTICAL = COLOUR_LIGHT_BLUE
UI_NAV_HORIZONTAL = COLOUR_PURPLE
UI_ZOOM = COLOUR_BLUE
UI_ACCEPT = COLOUR_GREEN
UI_REJECT = COLOUR_RED
UI_CHOOSE = COLOUR_PURPLE

UI_UNDO = COLOUR_LIGHT_LIGHT_BLUE
UI_REDO = COLOUR_LIGHT_BLUE

UI_COPY = COLOUR_BLUE
UI_CUT = COLOUR_LIGHT_BLUE
UI_PASTE = COLOUR_GREEN

# Define tool colours
TOOL_PENCIL = COLOUR_ORANGE
TOOL_BRUSH = COLOUR_LIGHT_BLUE
TOOL_DELETE = COLOUR_RED
TOOL_MUTE = COLOUR_PINK
TOOL_SLIP = COLOUR_ORANGE
TOOL_SLICE = COLOUR_LIGHT_BLUE
TOOL_SELECT = COLOUR_YELLOW
TOOL_ZOOM = COLOUR_BLUE
TOOL_PLAYBACK = COLOUR_GREEN

# Define Window Colours
WINDOW_PLAYLIST = COLOUR_GREEN
WINDOW_CHANNEL_RACK = COLOUR_RED
WINDOW_PIANO_ROLL = COLOUR_PINK
WINDOW_MIXER = COLOUR_LIGHT_BLUE
WINDOW_BROWSER = COLOUR_ORANGE

# Define Beat Indicator Colours
BEAT_PAT_BAR = COLOUR_RED
BEAT_PAT_BEAT = COLOUR_ORANGE
BEAT_SONG_BAR = COLOUR_LIGHT_BLUE
BEAT_SONG_BEAT = COLOUR_GREEN

TEMPO_TAP = COLOUR_PINK
METRONOME = COLOUR_DARK_GREY

# Colour Matrix for errors
ERROR_COLOURS = [
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED],
    [COLOUR_RED, COLOUR_RED]
]
