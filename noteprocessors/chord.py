"""
noteprocessors > chord.py

This script plays individual notes as chords.

Author: Miguel Guthridge
"""

import _random

import internal.consts
import eventconsts
from internal.notemanager import notesDown
import processorhelpers
import lightingconsts

# Create random number generator
rng = _random.Random()

MAX_VEL_OFFSET = 10

# The name of your mode
NAME = "Chord"

# The colour used to represent your mode
DEFAULT_COLOUR = lightingconsts.colours["TEAL"]

# The colour used to represent your mode while active... 
# you can change this while your script is running
COLOUR = lightingconsts.colours["TEAL"]

# Whether your mode should be unlisted in the note mode menu
SILENT = False

# Whether to forward all notes to the extended mode script to be processed as well. 
# You can modify this during execution to make it only forward notes sometimes.
FORWARD_NOTES = False

ROOT_NOTE = 0
SCALE_TYPE = "Major"
ENABLE_RANDOMNESS = False

MAJOR_CHORD = [0, 4, 7]
MINOR_CHORD = [0, 3, 7]
DIM_CHORD = [0, 3, 6]

MAJOR_MAJOR_SEVENTH_CHORD = [0, 4, 7, 11]
MAJOR_MINOR_SEVENTH_CHORD = [0, 4, 7, 10]

MINOR_MAJOR_SEVENTH_CHORD = [0, 3, 7, 11]
MINOR_MINOR_SEVENTH_CHORD = [0, 3, 7, 10]

DIM_MAJOR_SEVENTH_CHORD = [0, 3, 6, 10]
DIM_MINOR_SEVENTH_CHORD = [0, 3, 6, 9]

MAJOR_MAJOR_SIXTH_CHORD = [0, 4, 7, 9]
MAJOR_MINOR_SIXTH_CHORD = [0, 4, 7, 8]

MINOR_MAJOR_SIXTH_CHORD = [0, 3, 7, 9]
MINOR_MINOR_SIXTH_CHORD = [0, 3, 7, 8]

DIM_MAJOR_SIXTH_CHORD = [0, 3, 6, 8]

class Chord:
    
    def __init__(self, notes):
        self.notes = notes
        
    def getNotes(self, offset=0):
        ret = self.notes.copy()
        for i in range(len(ret)):
            ret[i] += offset
        return ret
    
class ChordStack:
    def __init__(self):
        self.stack = []
    
    def addChord(self, notes):
        self.stack.append(Chord(notes))
    
    def getNotes(self, offset=0, random=False):
        if len(self.stack) == 0:
            return [offset]
        if not random:
            return self.stack[0].getNotes(offset)
        else:
            access_index = int(rng.random() * (len(self.stack) - 1))
            return self.stack[access_index].getNotes(offset)
        

class ChordSet:
    
    def __init__(self, name):
        self.name = name
        self.chords = [ChordStack() for i in range(12)]
    
    def addChord(self, root, notes):
        self.chords[root].addChord(notes)
        
    def getChord(self, root):
        return self.chords[root % 12].getNotes(root, ENABLE_RANDOMNESS)


majorChords = ChordSet("Major")
# Primary notes
majorChords.addChord(0, MAJOR_CHORD)
majorChords.addChord(2, MINOR_CHORD)
majorChords.addChord(4, MINOR_CHORD)
majorChords.addChord(5, MAJOR_CHORD)
majorChords.addChord(7, MAJOR_CHORD)
majorChords.addChord(9, MINOR_CHORD)
majorChords.addChord(11, DIM_CHORD)

# Non-scale notes
majorChords.addChord(3, MAJOR_CHORD)
majorChords.addChord(6, DIM_MAJOR_SEVENTH_CHORD)
majorChords.addChord(8, MAJOR_MAJOR_SIXTH_CHORD)
majorChords.addChord(10, MAJOR_MAJOR_SIXTH_CHORD)

minorChords = ChordSet("Minor")

def process(command):
    """Called with an event to be processed by your note processor. Events aren't filtered so you'll want to make sure your processor checks that events are notes.

    Args:
        command (ParsedEvent): An event for your function to modify/act on.
    """
    command.addProcessor("Chord Processor")
    # If command is a note
    if command.type is eventconsts.TYPE_NOTE:
        if not command.is_lift:
            # How far note is up scale
            scale_pos = command.note - ROOT_NOTE
            
            notes_list = majorChords.getChord(scale_pos)
            notes_events = []
            for i in range(1, len(notes_list)):
                new_velocity = int(2*(rng.random() - 0.5) * MAX_VEL_OFFSET * (command.value/127)) + command.value
                if new_velocity > 127:
                    new_velocity = 127
                elif new_velocity < 0:
                    new_velocity = 0
                    
                notes_events.append(processorhelpers.RawEvent(command.status, notes_list[i] + ROOT_NOTE, new_velocity))
            
            send_notes = processorhelpers.ExtensibleNote(command, notes_events)
            command.act("Played chord")
            
            notesDown.noteOn(send_notes)
        else:
            command.act("Stopped chord")
            notesDown.noteOff(command)
    
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

