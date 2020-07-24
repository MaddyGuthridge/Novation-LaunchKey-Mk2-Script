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
    if internal.window.get_animation_tick() >= 0:
        lights.setPadColour(3, 1, lighting.COLOUR_PURPLE)   # Next
    if internal.window.get_animation_tick() >= 1:
        lights.setPadColour(3, 0, lighting.COLOUR_PURPLE)   # Prev
        lights.setPadColour(4, 1, lighting.COLOUR_RED)      # Stop
    if internal.window.get_animation_tick() >= 2:
        lights.setPadColour(5, 1, lighting.COLOUR_GREEN)    # Play
    if internal.window.get_animation_tick() >= 4:
        lights.setPadColour(7, 1, lighting.COLOUR_BLUE, 2)     # Select
    return

def process(command):

    command.actions.addProcessor("Browser Processor")

    if command.type == eventconsts.TYPE_PAD and command.is_lift:
        coord = [command.coord_X, command.coord_Y]
        
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
