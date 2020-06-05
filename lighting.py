"""
lighting.py
This file contains functions and constants related to controlling lights on the controller.

"""

import internal

# Front-facing functions

# Set the colour of a pad
def setPadColour(padNumber, colour):
    if internal.queryExtendedMode(): 
        internal.sendMidiMessage(0x9F, padNumber, colour)
    else: 
        internal.sendMidiMessage(0x9F, convertPadMapping(padNumber), colour)



# Define colour codes

COLOUR_OFF = 0
COLOUR_WHITE = 3
COLOUR_RED = 5
COLOUR_GREEN = 25
COLOUR_PINK = 53
COLOUR_BLUE = 41
COLOUR_YELLOW = 13
COLOUR_PURPLE = 49
COLOUR_LILAC = 116
COLOUR_ORANGE = 84

COLOUR_LIGHT_YELLOW = 109


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
