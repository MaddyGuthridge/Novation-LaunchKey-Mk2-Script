"""
error.py
This script processes notes when the error state is active
"""

import internalconstants
import config

NOTE_MODE = internalconstants.NOTE_STATE_ERROR

def process(command):
    command.actions.addProcessor("Error note handler")
    if config.CHAOTIC_EVIL_ERROR_NOTE_HANDLER:
        # Do chaotic evil things
        pass
    else:
        command.handle("Device in error state")

