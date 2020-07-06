"""
processwindowed.py
This script forwards events to event processors for FL Studio Windows

"""


import config
import internal
import internalconstants

import WindowProcessors.processmixer
import WindowProcessors.ProcessBrowser
import WindowProcessors.processchannelrack
import WindowProcessors.processplaylist

import WindowProcessors.ProcessDefault

def getWindowObject():
    if internal.window.active_fl_window == internalconstants.WINDOW_MIXER:
        return WindowProcessors.processmixer
    
    elif internal.window.active_fl_window == internalconstants.WINDOW_BROWSER:
        return WindowProcessors.ProcessBrowser
    
    elif internal.window.active_fl_window == internalconstants.WINDOW_CHANNEL_RACK:
        return WindowProcessors.processchannelrack

    elif internal.window.active_fl_window == internalconstants.WINDOW_PLAYLIST:
        return WindowProcessors.processplaylist

    else: return WindowProcessors.ProcessDefault

def process(command):

    current_window = getWindowObject()
    current_window.process(command)

    return

def redraw(lights):

    current_window = getWindowObject()
    current_window.redraw(lights)

    return

def activeStart():

    current_window = getWindowObject()
    current_window.activeStart()

    return

def activeEnd():

    current_window = getWindowObject()
    current_window.activeEnd()

    return

def topWindowStart():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
        current_window = getWindowObject()
        current_window.topWindowStart()

    return

def topWindowEnd():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
        current_window = getWindowObject()
        current_window.topWindowEnd()

    return