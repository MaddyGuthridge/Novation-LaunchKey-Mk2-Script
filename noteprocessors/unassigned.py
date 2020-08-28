"""
noteprocessors > template.py

This script is a template note processor.

Author: Miguel Guthridge
"""

import internal.consts
import eventconsts
import internal
import processorhelpers
import lightingconsts

# The name of your mode
NAME = "Unassigned Mode"

# The colour used to represent your mode
DEFAULT_COLOUR = lightingconsts.colours["LIGHT BLUE"]

# The colour used to represent your mode while active... 
# you can change this while your script is running
COLOUR = lightingconsts.colours["LIGHT BLUE"]

# Signifies whether the processor has completed its initialisation.
# Change this to true somewhere in processInit() if your script requires events to configure it
# otherwise change it here
INIT_COMPLETE = True

# Whether your mode should be unlisted in the note mode menu
SILENT = False

# Whether to forward all notes to the extended mode script to be processed as well. 
# You can modify this during execution to make it only forward notes sometimes.
FORWARD_NOTES = False

def process(command):
    """Called with an event to be processed by your note processor. Events aren't filtered so you'll want to make sure your processor checks that events are notes.

    Args:
        command (ParsedEvent): An event for your function to modify/act on.
    """
    command.addProcessor("Unassigned processor")
    
    if command.type is not eventconsts.TYPE_INCONTROL and command.type is not eventconsts.TYPE_TRANSPORT:
        command.ignore("Ignore all events")
    
    return

def processInit(command):
    """Called if the INIT_COMPLETE flag is set to false

    Args:
        command (ParsedEvent): event to process
    """
    pass

def redraw(lights):
    """Called when a redraw is taking place. Use this to draw menus to allow your users to choose options. Most of the time, you should leave this empty.

    Args:
        lights (LightMap): The lights to draw to
    """
    # Solidify all lights to prevent redrawing over the top
    lights.solidifyAll()

def activeStart():
    """Called when your note mode is made active
    """
    internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS)
    internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS)
    internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS)

def activeEnd():
    """Called wen your note mode is no-longer active
    """
    internal.extendedMode.revert(eventconsts.INCONTROL_KNOBS)
    internal.extendedMode.revert(eventconsts.INCONTROL_FADERS)
    internal.extendedMode.revert(eventconsts.INCONTROL_PADS)

