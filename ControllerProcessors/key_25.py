"""
key_25.py

This script handles initialisation and some event handling specific to the 25-key model
"""

import eventconsts
import internal
import internalconstants

def process(command):
    
    pass

def onInit():
    internal.debugLog("Running on 25-key model", internalconstants.DEBUG_DEVICE_TYPE)
    # Force into extended mode for faders
    internal.extended.recieve(True, eventconsts.INCONTROL_FADERS)
