"""
noteprocessors > template.py

This script is a template note processor.

Author: Miguel Guthridge
"""

import channels

import internal.consts
import eventconsts
import internal
import processorhelpers
import lightingconsts

# The name of your mode
NAME = "Omni Mode"

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

INIT_COMPLETE = False

PAD_MAPPINGS = [
    [48, 62],
    [50, 64],
    [52, 65],
    [53, 67],
    [55, 69],
    [57, 71],
    [59, 72],
    [60, 74]
]


def process(command):
    """Called with an event to be processed by your note processor. Events aren't filtered so you'll want to make sure your processor checks that events are notes.

    Args:
        command (ParsedEvent): An event for your function to modify/act on.
    """
    command.addProcessor("Omni Mode Processor")
    # If command is a note
    if command.type is eventconsts.TYPE_NOTE:
        # Set status byte to channel 0xD (Omni preview channel)
        new_status = (command.status_nibble << 4) + internal.consts.OMNI_CHANNEL_STATUS
        command.edit(processorhelpers.RawEvent(new_status, command.note, command.value), "Remap for omni mode")
        command.ignore("Switch to omni channel")
    
    elif command.type is eventconsts.TYPE_BASIC_PAD or command.type is eventconsts.TYPE_PAD:
        if command.coord_X < 8:
            new_status = (9 << 4) + internal.consts.OMNI_CHANNEL_STATUS
            command.edit(processorhelpers.RawEvent(new_status, PAD_MAPPINGS[command.coord_X][command.coord_Y], command.value), "Remap for omni mode")
            command.ignore("Remap to omni mode")
        

def redraw(lights):
    """Called when a redraw is taking place. Use this to draw menus to allow your users to choose options. Most of the time, you should leave this empty.

    Args:
        lights (LightMap): The lights to draw to
    """
    for ctr in range(min(channels.channelCount(1), 16)):
        x = ctr % 8
        y = ctr // 8
        lights.setPadColour(x, y, lightingconsts.colours.getClosestInt(channels.getChannelColor(ctr)))

    lights.solidifyAll()

def activeStart():
    """Called when your note mode is made active
    """
    global INIT_COMPLETE
    INIT_COMPLETE = True

def activeEnd():
    """Called wen your note mode is no-longer active
    """
    global COLOUR, INIT_COMPLETE
    # Reset current colour to default
    COLOUR = DEFAULT_COLOUR
    INIT_COMPLETE = False
    
def beatChange(beat):
    pass
