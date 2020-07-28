"""
error.py
This script processes notes when the error state is active
"""

import internalconstants

NOTE_MODE = internalconstants.NOTE_STATE_NORMAL

def process(command):
    command.actions.addProcessor("Default Note Handler")

