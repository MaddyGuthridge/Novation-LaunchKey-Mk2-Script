"""
processbrowser.py
This script processes events when the browser window is active

"""

# Commands:
# 2, 1 : PREVIOUS
# 3, 1 : STOP/COLLAPSE
# 4, 1 : PLAY/EXPAND
# 5, 1 : NEXT
# 7, 1 : ADD TO NEW TRACK

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
    lights.setPadColour(2, 1, lighting.COLOUR_PURPLE)
    lights.setPadColour(3, 1, lighting.COLOUR_RED)
    lights.setPadColour(4, 1, lighting.COLOUR_GREEN)
    lights.setPadColour(5, 1, lighting.COLOUR_PURPLE)
    lights.setPadColour(7, 1, lighting.COLOUR_BLUE)
    return

def process(command):

    command.actions.addProcessor("Browser Processor")

    if command.type == eventconsts.TYPE_PAD and command.value != 0:
        coord = [command.padX, command.padY]
        
        # Previous
        if coord == [2, 1]:
            ui.up()
            command.actions.appendAction("Previous")

        # Next
        elif coord == [5, 1]:
            ui.down()
            command.actions.appendAction("Next")

        # Stop
        elif coord == [3, 1]:
            ui.left()
            command.actions.appendAction("Collapse")

        # Play
        elif coord == [4, 1]:
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
