"""
lighting.py
This file contains functions and constants related to controlling lights on the controller.

"""

import internal
import time

import eventconsts
import eventprocessor

# Front-facing functions

# Set the colour of a pad
def setPadColour(padNumber, colour):
    if internal.queryExtendedMode(): 
        internal.sendMidiMessage(0x9F, padNumber, colour)
    else: 
        internal.sendMidiMessage(0x9F, eventprocessor.convertPadMapping(padNumber), colour)
        
def resetPads():
    for x in eventconsts.Pads:
        setPadColour(x, COLOUR_OFF)


def lightShow():
    print("Lights: Begin show")
    sleepTime = 0.05
    x = 0
    while True:
        # Group 1
        if (x >= 0) and (x < len(rainbowColours)):
            setPadColour(eventconsts.PAD_BOTTOM_1, rainbowColours[x])
        
         # Group 2
        if (x >= 1) and (x < len(rainbowColours) + 1):
            setPadColour(eventconsts.PAD_BOTTOM_2, rainbowColours[x - 1])
            setPadColour(eventconsts.PAD_TOP_1, rainbowColours[x - 1])
        
        # Group 3
        if (x >= 2) and (x < len(rainbowColours) + 2):
            setPadColour(eventconsts.PAD_BOTTOM_3, rainbowColours[x - 2])
            setPadColour(eventconsts.PAD_TOP_2, rainbowColours[x - 2])
        
        # Group 4
        if (x >= 3) and (x < len(rainbowColours) + 3):
            setPadColour(eventconsts.PAD_BOTTOM_4, rainbowColours[x - 3])
            setPadColour(eventconsts.PAD_TOP_3, rainbowColours[x - 3])
        
        # Group 5
        if (x >= 4) and (x < len(rainbowColours) + 4):
            setPadColour(eventconsts.PAD_BOTTOM_5, rainbowColours[x - 4])
            setPadColour(eventconsts.PAD_TOP_4, rainbowColours[x - 4])
        
        # Group 6
        if (x >= 5) and (x < len(rainbowColours) + 5):
            setPadColour(eventconsts.PAD_BOTTOM_6, rainbowColours[x - 5])
            setPadColour(eventconsts.PAD_TOP_5, rainbowColours[x - 5])
        
        # Group 7
        if (x >= 6) and (x < len(rainbowColours) + 6):
            setPadColour(eventconsts.PAD_BOTTOM_7, rainbowColours[x - 6])
            setPadColour(eventconsts.PAD_TOP_6, rainbowColours[x - 6])
        
        # Group 8
        if (x >= 7) and (x < len(rainbowColours) + 7):
            setPadColour(eventconsts.PAD_BOTTOM_8, rainbowColours[x - 7])
            setPadColour(eventconsts.PAD_TOP_7, rainbowColours[x - 7])
        
        # Group 9
        if (x >= 8) and (x < len(rainbowColours) + 8):
            setPadColour(eventconsts.PAD_TOP_8, rainbowColours[x - 8])
        
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




