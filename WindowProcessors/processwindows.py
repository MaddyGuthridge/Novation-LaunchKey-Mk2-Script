"""
processwindowed.py
This script forwards events to event processors for FL Studio Windows

"""

import ui
import WindowProcessors.processmixer

PLAYLIST = 2
PIANO_ROLL = 3
CHANNEL_RACK = 1
MIXER = 0
BROWSER = 4

def process(command):

    if ui.getFocused(MIXER):
        WindowProcessors.processmixer.process(command)

    return