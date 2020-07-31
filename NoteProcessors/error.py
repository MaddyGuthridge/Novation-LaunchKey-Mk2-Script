"""
error.py
This script processes notes when the error state is active
"""

import internalconstants
import config
import internal
import processorhelpers
import eventprocessor

NOTE_MODE = internalconstants.NOTE_STATE_ERROR

def process(command):
    command.actions.addProcessor("Error note handler")
    if config.CHAOTIC_EVIL_ERROR_NOTE_HANDLER:
        # Do chaotic evil things
        if not command.is_lift:
            
            notes_list = [eventprocessor.rawEvent(0, x, 127) for x in range(127, -1, -1)]
            
            note = processorhelpers.ExtensibleNote(command, notes_list)
            
            internal.notesDown.noteOn(note)
            
            command.handle("All notes on")
            
        else:
            internal.notesDown.allNotesOff()
            command.handle("All notes off")
    else:
        command.handle("Device in error state")

