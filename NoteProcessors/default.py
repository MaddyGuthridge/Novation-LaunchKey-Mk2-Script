"""
noteprocessors > default.py
This script processes notes nomally.

Author: Miguel Guthridge
"""

import internalconstants
import eventconsts
import internal
import processorhelpers
import lightingconsts

NOTE_MODE = internalconstants.NOTE_STATE_NORMAL

COLOUR = lightingconsts.colours["DARK GREY"]

def process(command):
    """
    command.actions.addProcessor("Default Note Handler")
    
    if not command.is_lift:
        
        note = processorhelpers.ExtensibleNote(command, [])
        
        internal.notesDown.noteOn(note)
        
        command.handle("Note on")
        
    else:
        internal.notesDown.noteOff(command)
        command.handle("Note off")
    """
    pass

