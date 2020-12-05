"""
otherprocessors > processfirst_basic.py
This file processes events before anything else when basic mode is active.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import transport
import ui
import general

import config
import internal.consts
import eventprocessor
import eventconsts
import internal
import lighting



def process(command):

    command.actions.addProcessor("Primary Processor")

    # Forward onto main processor for lighting
    if command.type == eventconsts.TYPE_BASIC_PAD:
        internal.sendInternalMidiMessage(command.status, command.note, command.value)
        command.actions.appendAction("Forward to extended script processor", silent=True)
    
    if command.id == eventconsts.PITCH_BEND:
        internal.state.pitchBend.setVal(command.value)
            

