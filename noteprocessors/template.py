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
NAME = "Template"

# The colour used to represent your mode
DEFAULT_COLOUR = lightingconsts.colours["PURPLE"]

# The colour used to represent your mode while active... 
# you can change this while your script is running
COLOUR = lightingconsts.colours["PURPLE"]

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
    command.addProcessor("Template Processor")
    # If command is a note
    if command.type is eventconsts.TYPE_NOTE:
        pass
    
    pass

def redraw(lights):
    """Called when a redraw is taking place. Use this to draw menus to allow your users to choose options. Most of the time, you should leave this empty.

    Args:
        lights (LightMap): The lights to draw to
    """
    pass

def activeStart():
    """Called when your note mode is made active
    """
    pass

def activeEnd():
    """Called wen your note mode is no-longer active
    """
    global COLOUR
    # Reset current colour to default
    COLOUR = DEFAULT_COLOUR

