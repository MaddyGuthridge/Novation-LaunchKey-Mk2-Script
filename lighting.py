"""
lighting.py
This file contains functions and constants related to controlling lights on the controller.

"""

import internal
import time



# Front-facing functions

# Set the colour of a pad
def setPadColour(padNumber, colour):
    if internal.queryExtendedMode(): 
        internal.sendMidiMessage(0x9F, padNumber, colour)
    else: 
        internal.sendMidiMessage(0x9F, convertPadMapping(padNumber), colour)
        
def resetPads():
    for x in Pads:
        setPadColour(x, COLOUR_OFF)


def lightShow():
    print("Lights: Begin show")
    sleepTime = 0.05
    x = 0
    while True:
        # Group 1
        if (x >= 0) and (x < len(rainbowColours)):
            setPadColour(PAD_BOTTOM_1, rainbowColours[x])
        
         # Group 2
        if (x >= 1) and (x < len(rainbowColours) + 1):
            setPadColour(PAD_BOTTOM_2, rainbowColours[x - 1])
            setPadColour(PAD_TOP_1, rainbowColours[x - 1])
        
        # Group 3
        if (x >= 2) and (x < len(rainbowColours) + 2):
            setPadColour(PAD_BOTTOM_3, rainbowColours[x - 2])
            setPadColour(PAD_TOP_2, rainbowColours[x - 2])
        
        # Group 4
        if (x >= 3) and (x < len(rainbowColours) + 3):
            setPadColour(PAD_BOTTOM_4, rainbowColours[x - 3])
            setPadColour(PAD_TOP_3, rainbowColours[x - 3])
        
        # Group 5
        if (x >= 4) and (x < len(rainbowColours) + 4):
            setPadColour(PAD_BOTTOM_5, rainbowColours[x - 4])
            setPadColour(PAD_TOP_4, rainbowColours[x - 4])
        
        # Group 6
        if (x >= 5) and (x < len(rainbowColours) + 5):
            setPadColour(PAD_BOTTOM_6, rainbowColours[x - 5])
            setPadColour(PAD_TOP_5, rainbowColours[x - 5])
        
        # Group 7
        if (x >= 6) and (x < len(rainbowColours) + 6):
            setPadColour(PAD_BOTTOM_7, rainbowColours[x - 6])
            setPadColour(PAD_TOP_6, rainbowColours[x - 6])
        
        # Group 8
        if (x >= 7) and (x < len(rainbowColours) + 7):
            setPadColour(PAD_BOTTOM_8, rainbowColours[x - 7])
            setPadColour(PAD_TOP_7, rainbowColours[x - 7])
        
        # Group 9
        if (x >= 8) and (x < len(rainbowColours) + 8):
            setPadColour(PAD_TOP_8, rainbowColours[x - 8])
        
        x += 1
        time.sleep(sleepTime)
        
        if x > len(rainbowColours) + 8: break

    resetPads()
    print("Lights: End show")

# Define colour codes

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

rainbowColours = [COLOUR_RED, COLOUR_PINK, COLOUR_PURPLE, COLOUR_BLUE, COLOUR_LIGHT_BLUE, COLOUR_GREEN, COLOUR_YELLOW, COLOUR_ORANGE, COLOUR_OFF]


# Define pad references

PAD_TOP_1 = 0x60
PAD_TOP_2 = 0x61
PAD_TOP_3 = 0x62
PAD_TOP_4 = 0x63
PAD_TOP_5 = 0x64
PAD_TOP_6 = 0x65
PAD_TOP_7 = 0x66
PAD_TOP_8 = 0x67

PAD_BOTTOM_1 = 0x70
PAD_BOTTOM_2 = 0x71
PAD_BOTTOM_3 = 0x72
PAD_BOTTOM_4 = 0x73
PAD_BOTTOM_5 = 0x74
PAD_BOTTOM_6 = 0x75
PAD_BOTTOM_7 = 0x76
PAD_BOTTOM_8 = 0x77

PAD_TOP_BUTTON = 0x68
PAD_BOTTOM_BUTTON = 0x78

Pads = [PAD_TOP_1, PAD_TOP_2, PAD_TOP_3, PAD_TOP_4, PAD_TOP_5, PAD_TOP_6, PAD_TOP_7, PAD_TOP_8, PAD_BOTTOM_1, PAD_BOTTOM_2, PAD_BOTTOM_3, PAD_BOTTOM_4, PAD_BOTTOM_5, PAD_BOTTOM_6, PAD_BOTTOM_7, PAD_BOTTOM_8, PAD_TOP_BUTTON, PAD_BOTTOM_BUTTON]

# Define Basic Mode pad references
BASIC_PAD_TOP_1 = 0x28
BASIC_PAD_TOP_2 = 0x29
BASIC_PAD_TOP_3 = 0x2A
BASIC_PAD_TOP_4 = 0x2B
BASIC_PAD_TOP_5 = 0x30
BASIC_PAD_TOP_6 = 0x31
BASIC_PAD_TOP_7 = 0x32
BASIC_PAD_TOP_8 = 0x33

BASIC_PAD_BOTTOM_1 = 0x24
BASIC_PAD_BOTTOM_2 = 0x25
BASIC_PAD_BOTTOM_3 = 0x26
BASIC_PAD_BOTTOM_4 = 0x27
BASIC_PAD_BOTTOM_5 = 0x2C
BASIC_PAD_BOTTOM_6 = 0x2D
BASIC_PAD_BOTTOM_7 = 0x2E
BASIC_PAD_BOTTOM_8 = 0x2F

BASIC_PAD_TOP_BUTTON = 0x68
BASIC_PAD_BOTTOM_BUTTON = 0x69

# Internal functions

# Convert between Extended Mode pad mappings and Basic Mode pad mappings
def convertPadMapping(padNumber):
    if padNumber is PAD_TOP_1: return BASIC_PAD_TOP_1
    elif padNumber is PAD_TOP_2: return BASIC_PAD_TOP_2
    elif padNumber is PAD_TOP_3: return BASIC_PAD_TOP_3
    elif padNumber is PAD_TOP_4: return BASIC_PAD_TOP_4
    elif padNumber is PAD_TOP_5: return BASIC_PAD_TOP_5
    elif padNumber is PAD_TOP_6: return BASIC_PAD_TOP_6
    elif padNumber is PAD_TOP_7: return BASIC_PAD_TOP_7
    elif padNumber is PAD_TOP_8: return BASIC_PAD_TOP_8
    elif padNumber is PAD_BOTTOM_1: return BASIC_PAD_BOTTOM_1
    elif padNumber is PAD_BOTTOM_2: return BASIC_PAD_BOTTOM_2
    elif padNumber is PAD_BOTTOM_3: return BASIC_PAD_BOTTOM_3
    elif padNumber is PAD_BOTTOM_4: return BASIC_PAD_BOTTOM_4
    elif padNumber is PAD_BOTTOM_5: return BASIC_PAD_BOTTOM_5
    elif padNumber is PAD_BOTTOM_6: return BASIC_PAD_BOTTOM_6
    elif padNumber is PAD_BOTTOM_7: return BASIC_PAD_BOTTOM_7
    elif padNumber is PAD_BOTTOM_8: return BASIC_PAD_BOTTOM_8
    elif padNumber is PAD_TOP_BUTTON: return BASIC_PAD_TOP_BUTTON
    elif padNumber is PAD_BOTTOM_BUTTON: return BASIC_PAD_BOTTOM_BUTTON
    internal.logError("Pad number not defined")
