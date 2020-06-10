"""
internal.py
This file contains functions common to  scripts loaded by both files.

"""

#-------------------------------
# Edit this file at your own risk. All user-modifyable variables are found in 'config.py'.
#-------------------------------

import device

extendedMode = False

# The previous mesage sent to the MIDI out device
previous_event_out = 0

# TODO: process extended mode messages.

# Queries whether extended mode is active. Only accessible from port 2
def queryExtendedMode():
    global extendedMode
    return extendedMode

# Sets extended mode on the device
def setExtendedMode(newMode):
    global extendedMode
    if newMode is True:
        sendMidiMessage(0x9F, 0x0C, 0x7F)
        extendedMode = True
    elif newMode is False:
        sendMidiMessage(0x9F, 0x0C, 0x00)
        extendedMode = False
    else: logError("Extended mode not boolean")

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
