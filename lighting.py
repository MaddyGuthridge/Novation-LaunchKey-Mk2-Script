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

# Set all pads to off      
def resetPads():
    internal.sendMidiMessage(0xBF, 0x00, 0x00)

# OoooOooOOOooO PREETTTTTYYYY!!!!!!
def lightShow():
    sleepTime = 0.05
    x = 0
    while True:
        # Group 1
        if (x >= 0) and (x < len(rainbowColours)):
            setPadColour(eventconsts.Pads[1][0], rainbowColours[x])
        
         # Group 2
        if (x >= 1) and (x < len(rainbowColours) + 1):
            setPadColour(eventconsts.Pads[1][1], rainbowColours[x - 1])
            setPadColour(eventconsts.Pads[0][0], rainbowColours[x - 1])
        
        # Group 3
        if (x >= 2) and (x < len(rainbowColours) + 2):
            setPadColour(eventconsts.Pads[1][2], rainbowColours[x - 2])
            setPadColour(eventconsts.Pads[0][1], rainbowColours[x - 2])
        
        # Group 4
        if (x >= 3) and (x < len(rainbowColours) + 3):
            setPadColour(eventconsts.Pads[1][3], rainbowColours[x - 3])
            setPadColour(eventconsts.Pads[0][2], rainbowColours[x - 3])
        
        # Group 5
        if (x >= 4) and (x < len(rainbowColours) + 4):
            setPadColour(eventconsts.Pads[1][4], rainbowColours[x - 4])
            setPadColour(eventconsts.Pads[0][3], rainbowColours[x - 4])
        
    
        # Group 6
        if (x >= 5) and (x < len(rainbowColours) + 5):
            setPadColour(eventconsts.Pads[1][5], rainbowColours[x - 5])
            setPadColour(eventconsts.Pads[0][4], rainbowColours[x - 5])
        
        # Group 7
        if (x >= 6) and (x < len(rainbowColours) + 6):
            setPadColour(eventconsts.Pads[1][6], rainbowColours[x - 6])
            setPadColour(eventconsts.Pads[0][5], rainbowColours[x - 6])
        
        # Group 8
        if (x >= 7) and (x < len(rainbowColours) + 7):
            setPadColour(eventconsts.Pads[1][7], rainbowColours[x - 7])
            setPadColour(eventconsts.Pads[0][6], rainbowColours[x - 7])
        
        # Group 9
        if (x >= 8) and (x < len(rainbowColours) + 8):
            setPadColour(eventconsts.Pads[0][7], rainbowColours[x - 8])
        
        x += 1
        time.sleep(sleepTime)
        
        if x > len(rainbowColours) + 8: break

    resetPads()

# Quick update of pads (redrawing bouncers or something)
def updatePads(event = None):
    # If event exists: If not button, draw event value

    # If in mixer: redraw bouncer
    return

# Full refresh of pads
def refreshPads():
    return

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




