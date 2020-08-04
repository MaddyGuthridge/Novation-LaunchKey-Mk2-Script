"""
key_25.py

This script handles initialisation and some event handling specific to the 25-key model
"""

import eventconsts
import internal
import internalconstants
import eventprocessor

def process(command):
    
    if command.type == eventconsts.TYPE_BASIC_FADER and command.coord_X == 8:
        command.edit(eventprocessor.rawEvent(0xBF, 0x07, command.value))
    pass

def onInit():
    internal.debugLog("Running on 25-key model", internalconstants.DEBUG_DEVICE_TYPE)
    # Force into extended mode for faders
    internal.extendedMode.recieve(True, eventconsts.INCONTROL_FADERS)


