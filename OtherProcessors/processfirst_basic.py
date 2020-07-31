"""
processfirst.py
This file processes events before anything else.

"""

import transport
import ui
import general

import config
import internalconstants
import eventprocessor
import eventconsts
import internal
import lighting


def process(command):

    command.actions.addProcessor("Primary Processor")

    # Forward onto main processor for lighting
    if command.type == eventconsts.TYPE_BASIC_PAD:
        internal.sendInternalMidiMessage(command.status, command.note, command.value)
        command.actions.appendAction("Forward to extended script processor")
    
    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")

