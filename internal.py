"""
internal.py
This file contains functions common to  scripts loaded by both files.

"""

#-------------------------------
# Edit this file at your own risk. All user-modifyable variables are found in 'config.py'.
#-------------------------------

import device

import eventconsts

PORT = -1 # Set in initialisation function then left constant

extendedMode = False
inControl_Knobs = False
inControl_Faders = False
inControl_Pads = False

ActiveWindow = "Nil"

# The previous mesage sent to the MIDI out device
previous_event_out = 0

# TODO: process extended mode messages.

# Queries whether extended mode is active. Only accessible from extended port
def queryExtendedMode(option = eventconsts.SYSTEM_EXTENDED):
    global extendedMode
    global inControl_Knobs
    global inControl_Faders
    global inControl_Pads
    
    if option == eventconsts.SYSTEM_EXTENDED: return extendedMode
    elif option == eventconsts.INCONTROL_KNOBS: return inControl_Knobs
    elif option == eventconsts.INCONTROL_FADERS: return inControl_Faders
    elif option == eventconsts.INCONTROL_PADS: return inControl_Pads

# Sets extended mode on the device, use inControl constants to choose which
def setExtendedMode(newMode, option = eventconsts.SYSTEM_EXTENDED):
    global extendedMode
    global inControl_Knobs
    global inControl_Faders
    global inControl_Pads

    # Set all
    if option == eventconsts.SYSTEM_EXTENDED:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0C, 0x7F)
            extendedMode = True
            inControl_Knobs = True
            inControl_Faders = True
            inControl_Pads = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0C, 0x00)
            extendedMode = False
            inControl_Knobs = False
            inControl_Faders = False
            inControl_Pads = False
        else: logError("New mode mode not boolean")
    
    # Set knobs
    elif option == eventconsts.INCONTROL_KNOBS:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0D, 0x7F)
            inControl_Knobs = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0D, 0x00)
            inControl_Knobs = False
        else: logError("New mode mode not boolean")
    
    # Set faders
    elif option == eventconsts.INCONTROL_FADERS:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0E, 0x7F)
            inControl_Faders = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0E, 0x00)
            inControl_Faders = False
        else: logError("New mode mode not boolean")
    
    # Set pads
    elif option == eventconsts.INCONTROL_PADS:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0F, 0x7F)
            inControl_Pads = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0F, 0x00)
            inControl_Pads = False
        else: logError("New mode mode not boolean")

# Processes extended mode messages from device
def recieveExtendedMode(newMode, option = eventconsts.SYSTEM_EXTENDED):
    global extendedMode
    global inControl_Knobs
    global inControl_Faders
    global inControl_Pads

    # Set all
    if option == eventconsts.SYSTEM_EXTENDED:
        if newMode is True:
            extendedMode = True
            inControl_Knobs = True
            inControl_Faders = True
            inControl_Pads = True
        elif newMode is False:
            extendedMode = False
            inControl_Knobs = False
            inControl_Faders = False
            inControl_Pads = False
        else: logError("New mode mode not boolean")
    
    # Set knobs
    elif option == eventconsts.INCONTROL_KNOBS:
        if newMode is True:
            inControl_Knobs = True
        elif newMode is False:
            inControl_Knobs = False
        else: logError("New mode mode not boolean")
    
    # Set faders
    elif option == eventconsts.INCONTROL_FADERS:
        if newMode is True:
            inControl_Faders = True
        elif newMode is False:
            inControl_Faders = False
        else: logError("New mode mode not boolean")
    
    # Set pads
    elif option == eventconsts.INCONTROL_PADS:
        if newMode is True:
            inControl_Pads = True
        elif newMode is False:
            inControl_Pads = False
        else: logError("New mode mode not boolean")

# Compares revieved event to previous
def compareEvent(event):
    if toMidiMessage(event.status, event.data1, event.data2) is previous_event_out: return True
    else: return False

EventNameT = ['Note Off', 'Note On ', 'Key Aftertouch', 'Control Change','Program Change',  'Channel Aftertouch', 'Pitch Bend', 'System Message' ]

# Sends message to the default MIDI out device
def sendMidiMessage(status, data1, data2):
    global previous_event_out
    previous_event_out  = toMidiMessage(status, data1, data2)
    device.midiOutMsg(previous_event_out)

# Generates a MIDI message given arguments
def toMidiMessage(status, data1, data2):
    return status + (data1 << 8) + (data2 << 16)

# Print out error message
def logError(message):
    print("Error: ", message)

# Return a simulation of the tab character
def getTab(length):
    if length < 0: print("ERROR: not enough spacing, need to use greater tab indents")
    a = ""
    for x in range(length):
        a += ' '
    return a
