"""
windowprocessors > processbrowser.py

This script processes events when the browser window is active.
It provides functionality to navigate the browser and load files and plugins.

Author: Miguel Guthridge
"""



import ui

import eventconsts
import internal
import config
import lightingconsts

def activeStart():
    
    return

def activeEnd():
    
    return

def topWindowStart():
    internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
    return

def topWindowEnd():
    internal.extendedMode.revert(eventconsts.INCONTROL_PADS)
    return

def redraw(lights):
    if internal.window.getAnimationTick() >= 0:
        lights.setPadColour(3, 1, lightingconsts.colours["PURPLE"])   # Next
    if internal.window.getAnimationTick() >= 1:
        lights.setPadColour(3, 0, lightingconsts.colours["PURPLE"])   # Prev
        lights.setPadColour(4, 1, lightingconsts.colours["RED"])      # Stop
    if internal.window.getAnimationTick() >= 2:
        lights.setPadColour(5, 1, lightingconsts.colours["GREEN"])    # Play
    if internal.window.getAnimationTick() >= 4:
        lights.setPadColour(7, 1, lightingconsts.colours["BLUE"], 2)     # Select
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
