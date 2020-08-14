"""
noteprocessors > error.py
This script processes notes when the error state is active.
It includes the "Chaotic Evil Error Note Handler" which changes single note on events to all 128 note-on events.

Author: Miguel Guthridge
"""

import internalconstants
import config
import internal
import processorhelpers
import lightingconsts
import eventconsts

NAME = internalconstants.NOTE_STATE_ERROR

COLOUR = lightingconsts.colours["ORANGE"]

DEFAULT_COLOUR = lightingconsts.colours["RED"]

SILENT = True

FORWARD_NOTES = False

def process(command):
    command.actions.addProcessor("Error note handler")
    
    if (command.type is eventconsts.TYPE_BASIC_PAD or command.type == eventconsts.TYPE_PAD) and command.is_lift and command.getPadCoord() == (8, 1):
        internal.errors.recoverError(False, True)
        command.handle("Recover error")
        
    elif (command.type is eventconsts.TYPE_BASIC_PAD or command.type == eventconsts.TYPE_PAD) and command.is_lift and command.getPadCoord() == (8, 0):
        internal.errors.recoverError(True, True)
        command.handle("Recover error, entered debug mode")
            
    elif config.CHAOTIC_EVIL_ERROR_NOTE_HANDLER and command.type is eventconsts.TYPE_NOTE:
        
        # Do chaotic evil things
        if not command.is_lift:
            
            notes_list = [processorhelpers.RawEvent(0, x, 127) for x in range(127, -1, -1)]
            
            note = processorhelpers.ExtensibleNote(command, notes_list)
            
            internal.notesDown.noteOn(note)
            
            command.handle("All notes on")
            
        else:
            internal.notesDown.allNotesOff()
            command.handle("All notes off")
    else:
        if not (command.type in internalconstants.SHIFT_IGNORE_TYPES):
            command.handle("Device in error state")

def redraw(lights):
    internal.errors.redrawError(lights)

def activeStart():
    pass

def activeEnd():
    pass

