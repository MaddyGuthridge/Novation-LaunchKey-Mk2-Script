"""
error.py
This script processes notes when the error state is active
"""

import internalconstants
import eventconsts
import internal
import processorhelpers

NOTE_MODE = internalconstants.NOTE_STATE_NORMAL

def process(command):
    command.actions.addProcessor("Default Note Handler")
    
    if not command.is_lift:
        
        note = processorhelpers.ExtensibleNote(command, [])
        
        internal.notesDown.noteOn(note)
        
        command.handle("Note on")
        
    else:
        internal.notesDown.noteOff(command)
        command.handle("Note off")

