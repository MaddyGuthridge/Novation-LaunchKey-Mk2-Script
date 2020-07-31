"""
key.py

This script handles initialisation and some event handling specific to certain devices
"""

import eventconsts
import internal
import internalconstants

import ControllerProcessors.key_25 as k25
import ControllerProcessors.key_49 as k49
import ControllerProcessors.key_61 as k61

def process(command):
    
    if internal.DEVICE_TYPE == internalconstants.DEVICE_KEYS_25:
        k25.process(command)
    
    if internal.DEVICE_TYPE == internalconstants.DEVICE_KEYS_49:
        k49.process(command)
        
    if internal.DEVICE_TYPE == internalconstants.DEVICE_KEYS_61:
        k61.process(command)

def onInit():
    
    if internal.DEVICE_TYPE == internalconstants.DEVICE_KEYS_25:
        k25.onInit()
    
    if internal.DEVICE_TYPE == internalconstants.DEVICE_KEYS_49:
        k49.onInit()
        
    if internal.DEVICE_TYPE == internalconstants.DEVICE_KEYS_61:
        k61.onInit()
