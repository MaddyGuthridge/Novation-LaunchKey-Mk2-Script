"""
processbrowser.py
This script processes events when the browser window is active

"""



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
    #lights.
    return

def process(command):

    command.actions.addProcessor("Browser Processor")

    

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
