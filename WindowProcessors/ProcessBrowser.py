"""
processbrowser.py
This script processes events when the browser window is active

"""



import ui

import eventconsts
import internal
import config
import lighting

def activeStart():
    internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
    return

def activeEnd():
    internal.extendedMode.revert(eventconsts.INCONTROL_PADS)
    return

def topWindowStart():
    return

def topWindowEnd():
    return

def redraw(lights):
    lights.setPadColour(3, 0, lighting.COLOUR_PURPLE)   # Prev
    lights.setPadColour(3, 1, lighting.COLOUR_PURPLE)   # Next
    lights.setPadColour(4, 1, lighting.COLOUR_RED)      # Stop
    lights.setPadColour(5, 1, lighting.COLOUR_GREEN)    # Play
    lights.setPadColour(7, 1, lighting.COLOUR_BLUE)     # Select
    return

def process(command):

    command.actions.addProcessor("Browser Processor")

    if command.type == eventconsts.TYPE_PAD and command.is_lift:
        coord = [command.padX, command.padY]
        
        # Previous
        if coord == [3, 0]:
            ui.up()
            command.actions.appendAction("Previous")

        # Next
        elif coord == [3, 1]:
            ui.down()
            command.actions.appendAction("Next")

        # Stop
        elif coord == [4, 1]:
            ui.left()
            command.actions.appendAction("Collapse")

        # Play
        elif coord == [5, 1]:
            ui.right()
            command.actions.appendAction("Expand/Play")

        # Play
        elif coord == [7, 1]:
            ui.enter()
            command.actions.appendAction("Add to selected track on channel rack")
        
        # Always handle all pad commands
        command.handled = True

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
