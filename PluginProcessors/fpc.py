"""
fpc.py
This script is a custom processor module that can process events when the FPC plugin is active

"""

import eventconsts
import eventprocessor
import internal

plugins = ["FPC"]

def activeStart():
    internal.setExtendedMode(False, eventconsts.INCONTROL_PADS)
    return

def activeEnd():
    internal.setExtendedMode(True, eventconsts.INCONTROL_PADS)
    return

def process(command):
    command.actions.addProcessor("FPC Processor")

    # Change pedals to kick:
    if command.id == eventconsts.PEDAL:
        if command.value == 0: # Pedal up
            command.edit(eventprocessor.rawEvent(0x89, eventconsts.BASIC_PAD_BOTTOM_2, command.value))
        else: # Pedal up
            command.edit(eventprocessor.rawEvent(0x99, eventconsts.BASIC_PAD_BOTTOM_2, command.value))

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
    return