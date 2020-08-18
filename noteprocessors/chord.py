"""
noteprocessors > chord.py

This script plays individual notes as chords.

Author: Miguel Guthridge
"""

import internal.consts
import eventconsts
from internal.notemanager import notesDown
import processorhelpers
import lightingconsts

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

MAJOR_CHORD = [0, 4, 7]
MINOR_CHORD = [0, 3, 7]
DIM_CHORD = [0, 3, 6]

class Chord:
    
    def __init__(self, notes):
        self.notes = notes
        
    def getNotes(self, offset=0):
        ret = self.notes.copy()
        for i in range(len(ret)):
            ret[i] += offset
        return ret
    
class ChordSet:
    
    def __init__(self, name):
        self.name = name
        self.chords = dict()
    
    def addChord(self, root, notes):
        self.chords[root] = Chord(notes)
        
    def getChord(self, root):
        try:
            return self.chords[root % 12].getNotes(root)
        except:
            return [root]

majorChords = ChordSet("Major")
majorChords.addChord(0, MAJOR_CHORD)
majorChords.addChord(2, MINOR_CHORD)
majorChords.addChord(4, MINOR_CHORD)
majorChords.addChord(5, MAJOR_CHORD)
majorChords.addChord(7, MAJOR_CHORD)
majorChords.addChord(9, MINOR_CHORD)
majorChords.addChord(11, DIM_CHORD)

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
            print(notes_list)
            notes_events = []
            for i in range(1, len(notes_list)):
                notes_events.append(processorhelpers.RawEvent(command.status, notes_list[i] + ROOT_NOTE, command.value))
            
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

