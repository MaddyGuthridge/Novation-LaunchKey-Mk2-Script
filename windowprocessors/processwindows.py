"""
windowprocessors > processwindows.py

This script forwards events to event processors for FL Studio Windows.

Author: Miguel Guthridge
"""


import config
import internal
import internal.consts

import windowprocessors.processmixer
import windowprocessors.processbrowser
import windowprocessors.processchannelrack
import windowprocessors.processplaylist

import windowprocessors.processdefault

def getWindowObject():
    """Returns reference to module associated with a window

    Returns:
        module: active FL Window
    """
    if internal.window.active_fl_window == internal.consts.WINDOW_MIXER:
        return windowprocessors.processmixer
    
    elif internal.window.active_fl_window == internal.consts.WINDOW_BROWSER:
        return windowprocessors.processbrowser
    
    elif internal.window.active_fl_window == internal.consts.WINDOW_CHANNEL_RACK:
        return windowprocessors.processchannelrack

    elif internal.window.active_fl_window == internal.consts.WINDOW_PLAYLIST:
        return windowprocessors.processplaylist

    else: return windowprocessors.processdefault

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
    if internal.state.PORT == config.DEVICE_PORT_EXTENDED:
        current_window = getWindowObject()
        current_window.topWindowStart()

    return

def topWindowEnd():
    # Only in extended mode:
    if internal.state.PORT == config.DEVICE_PORT_EXTENDED:
        current_window = getWindowObject()
        current_window.topWindowEnd()

    return

def beatChange(beat):
    current_window = getWindowObject()
    current_window.beatChange(beat)