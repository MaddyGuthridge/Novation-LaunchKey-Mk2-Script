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

NAME = internalconstants.NOTE_STATE_NORMAL

COLOUR = lightingconsts.colours["DARK GREY"]

SILENT = False

FORWARD_NOTES = False

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

def redraw(lights):
    pass

def activeStart():
    pass

def activeEnd():
    pass

