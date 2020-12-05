"""
windowprocessors > processbrowser.py

This script processes events when the browser window is active.
It provides functionality to navigate the browser and load files and plugins.

Author: Miguel Guthridge [hdsq@outlook.com.au]
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
    if internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        if internal.window.getAnimationTick() >= 0:
            lights.setPadColour(3, 1, lightingconsts.colours["PURPLE"])   # Next
        if internal.window.getAnimationTick() >= 1:
            lights.setPadColour(3, 0, lightingconsts.colours["PURPLE"])   # Prev
            lights.setPadColour(4, 1, lightingconsts.colours["RED"])      # Stop
        if internal.window.getAnimationTick() >= 2:
            lights.setPadColour(5, 1, lightingconsts.colours["GREEN"])    # Play
        if internal.window.getAnimationTick() >= 4:
            lights.setPadColour(7, 1, lightingconsts.colours["BLUE"], lightingconsts.MODE_PULSE)     # Select
    return

def process(command):

    command.actions.addProcessor("Browser Processor")

    if command.type == eventconsts.TYPE_PAD:
        if command.coord_X < 8:
            if command.is_lift:
                coord = [command.coord_X, command.coord_Y]
                
                # Previous
                if coord == [3, 0]:
                    ui.up()
                    command.handle("Previous")

                # Next
                elif coord == [3, 1]:
                    ui.down()
                    command.handle("Next")

                # Stop
                elif coord == [4, 1]:
                    ui.left()
                    command.handle("Collapse")

                # Play
                elif coord == [5, 1]:
                    ui.right()
                    command.handle("Expand/Play")

                # Play
                elif coord == [7, 1]:
                    ui.enter()
                    command.handle("Add to selected track on channel rack")
            
            else:
                # Always handle all pad commands
                command.handle("Pads catch-all", silent=True)

def beatChange(beat):
    pass
