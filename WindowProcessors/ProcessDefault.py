"""
ProcessDefault.py
This script can be used as a template for window scripts.

"""





def activeStart():
    return

def activeEnd():
    return

def topWindowStart():
    return

def topWindowEnd():
    return

def redraw(lights):
    return

def process(command):

    command.actions.addProcessor("[None] Processor")

    

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
