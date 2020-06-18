"""
processfirst.py
This file processes events before anything else.

"""

import transport
import ui

import config
import eventprocessor
import eventconsts
import internal

def redraw():

    return

def process(command):

    command.actions.addProcessor("Primary Processor")

    # If in extended mode
    if internal.PORT == config.DEVICE_PORT_EXTENDED:

        if command.type == eventconsts.TYPE_BASIC_PAD or command.type == eventconsts.TYPE_PAD:
            if command.value: # Press down
                internal.pads.press(command.padX, command.padY)
            else:
                internal.pads.lift(command.padX, command.padY)


        # Extended Mode
        if command.id == eventconsts.SYSTEM_EXTENDED:
            internal.extendedMode.recieve(not command.is_Lift)
            command.actions.appendAction("Set Extended Mode to " + str(not command.is_Lift))
            command.handled = True

        # Knobs
        if command.id == eventconsts.INCONTROL_KNOBS:
            internal.extendedMode.recieve(not command.is_Lift, eventconsts.INCONTROL_KNOBS)
            command.actions.appendAction("Set Extended Mode (Knobs) to " + str(not command.is_Lift))
            command.handled = True
        
        # Faders
        if command.id == eventconsts.INCONTROL_FADERS:
            internal.extendedMode.recieve(not command.is_Lift, eventconsts.INCONTROL_FADERS)
            command.actions.appendAction("Set Extended Mode (Faders) to " + str(not command.is_Lift))
            command.handled = True
        
        # Pads
        if command.id == eventconsts.INCONTROL_PADS:
            internal.extendedMode.recieve(not command.is_Lift, eventconsts.INCONTROL_PADS)
            command.actions.appendAction("Set Extended Mode (Pads) to " + str(not command.is_Lift))
            command.handled = True
        
        # That random event on the knobs button
        if command.id == eventconsts.SYSTEM_MISC:
            command.handled = True
    
    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")

