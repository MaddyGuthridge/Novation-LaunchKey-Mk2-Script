"""
processwindowed.py
This script forwards events to event processors for FL Studio Windows

"""


import config
import internal

import WindowProcessors.processmixer


def process(command):

    if internal.window.active_fl_window == config.WINDOW_MIXER:
        WindowProcessors.processmixer.process(command)

    return

def redraw(lights):

    if internal.window.active_fl_window == config.WINDOW_MIXER:
        WindowProcessors.processmixer.redraw(lights)

    return

def activeStart():

    if internal.window.active_fl_window == config.WINDOW_MIXER:
        WindowProcessors.processmixer.activeStart()

    return

def activeEnd():

    if internal.window.active_fl_window == config.WINDOW_MIXER:
        WindowProcessors.processmixer.activeEnd()

    return

def topWindowStart():

    if internal.window.active_fl_window == config.WINDOW_MIXER:
        WindowProcessors.processmixer.topWindowStart()

    return

def topWindowEnd():

    if internal.window.active_fl_window == config.WINDOW_MIXER:
        WindowProcessors.processmixer.topWindowEnd()

    return