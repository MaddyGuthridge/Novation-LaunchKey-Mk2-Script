"""
fpc.py
This script is a custom processor module that can process events when the FPC plugin is active

"""

plugins = ["FPC"]



def process(command):
    command.actions.addProcessor("FPC Processor")


    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
    return