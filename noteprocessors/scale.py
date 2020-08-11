"""
noteprocessors > template.py

This script is a template note processor.

Author: Miguel Guthridge
"""

import internalconstants
import eventconsts
import internal
import processorhelpers
import lightingconsts

# Define scale types
MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]
MINOR_SCALE = [0, 2, 3, 5, 7, 8, 10]

# The name of your mode
NAME = "Scale Snapping"

# The colour used to represent your mode
COLOUR = lightingconsts.colours["YELLOW"]

# Whether your mode should be unlisted in the note mode menu
SILENT = False

FORWARD_NOTES = True

INIT_COMPLETE = False
INIT_HAVE_ROOT = False
INIT_HAVE_SCALE = False

ROOT_NOTE = 0
SCALE_TO_USE = []

SNAP_NOTES = []

def setScale(root, scale_notes):
    global SNAP_NOTES
    for x in range(len(scale_notes)):
        scale_notes[x] = (scale_notes[x] + root) % 12
    scale_notes = sorted(scale_notes)
    
    SNAP_NOTES = [scale_notes[-1] - 12] + scale_notes + [scale_notes[0] + 12]


def process(command):
    """Called with an event to be processed by your note processor. Events aren't filtered so you'll want to make sure your processor checks that events are notes.

    Args:
        command (ProcessedEvent): An event for your function to modify/act on.
    """
    command.addProcessor("Scale Snapping")
    
    if not INIT_COMPLETE:
        processInit(command)
    
    # If command is a note
    elif command.type is eventconsts.TYPE_NOTE:
        
        note  = command.note % 12
        octave = command.note // 12
                
        if SNAP_NOTES == None:
            return
        
        closest_distance = 13
        closest_note = None
        closest_octave = 0
        for x in SNAP_NOTES:
            distance = abs(note - x)
            if distance < closest_distance:
                closest_note = x
                closest_distance = distance
                if distance == 0:
                    break
            
        new_note = closest_note + octave*12 + closest_octave*12
        command.edit(processorhelpers.RawEvent(command.status, new_note, command.value))
    
    pass

def redraw(lights):
    """Called when a redraw is taking place. Use this to draw menus to allow your users to choose options. Most of the time, you should leave this empty.

    Args:
        lights (LightMap): The lights to draw to
    """
    global INIT_COMPLETE
    if not INIT_COMPLETE:
        lights.setPadColour(0, 0, lightingconsts.colours["GREEN"])
        lights.setPadColour(1, 0, lightingconsts.colours["BLUE"])

def activeStart():
    """Called when your note mode is made active
    """
    pass

def activeEnd():
    """Called wen your note mode is no-longer active
    """
    global INIT_COMPLETE, INIT_HAVE_ROOT, INIT_HAVE_SCALE, SCALE_TO_USE, ROOT_NOTE, FORWARD_NOTES
    INIT_COMPLETE = False
    INIT_HAVE_ROOT = False
    INIT_HAVE_SCALE = False
    FORWARD_NOTES = True


def processInit(command):
    global INIT_COMPLETE, INIT_HAVE_ROOT, INIT_HAVE_SCALE, SCALE_TO_USE, ROOT_NOTE, FORWARD_NOTES
    if command.type == eventconsts.TYPE_PAD:
        if command.getPadCoord() == (0, 0):
            SCALE_TO_USE = MAJOR_SCALE
            INIT_HAVE_SCALE = True
            command.handle("Set scale to major")
        if command.getPadCoord() == (1, 0):
            SCALE_TO_USE = MINOR_SCALE
            INIT_HAVE_SCALE = True
            command.handle("Set scale to minor")
            
    if command.type == eventconsts.TYPE_NOTE:
        ROOT_NOTE = command.note % 12
        INIT_HAVE_ROOT = True
        command.handle("Set root note to" + str(ROOT_NOTE))
        
    if INIT_HAVE_ROOT and INIT_HAVE_SCALE:
        INIT_COMPLETE = True
        FORWARD_NOTES = False
        setScale(ROOT_NOTE, SCALE_TO_USE)
