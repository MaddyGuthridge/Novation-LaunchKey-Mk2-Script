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

ROOT_NOTE = -1
ENABLE_RANDOMNESS = False

INIT_COMPLETE = False

#########################################################

JAZZY_COLOURS = [
    lightingconsts.colours["LIGHT YELLOW"],
    lightingconsts.colours["YELLOW"],
    lightingconsts.colours["LIME"],
    lightingconsts.colours["GREEN"],
    lightingconsts.colours["TEAL"],
    lightingconsts.colours["LIGHT BLUE"],
    lightingconsts.colours["BLUE"],
    lightingconsts.colours["PURPLE"]
]

#########################################################

MAJOR_CHORD = [0, 4, 7]
MINOR_CHORD = [0, 3, 7]
DIM_CHORD = [0, 3, 6]

SUS2_CHORD = [0, 2, 7]
SUS4_CHORD = [0, 5, 7]

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
    
    def __init__(self, notes, can_change):
        self.notes = notes
        self.can_change = can_change
        
    def getNotes(self, offset=0):
        ret = self.notes.copy()
        for i in range(len(ret)):
            ret[i] += offset
        return ret
    
class ChordStack:
    def __init__(self):
        self.stack = []
        self.recent_index = -1
    
    def addChord(self, notes, can_change):
        self.stack.append(Chord(notes, can_change))
    
    def getNotes(self, offset, random, was_previous):
        if len(self.stack) == 0:
            return [offset]
        
        if was_previous and not self.stack[self.recent_index].can_change:
            return self.stack[self.recent_index].getNotes(offset)
        else:
            access_index = round(rng.random() * (len(self.stack) - 1))
            if access_index > chords.jazziness:
                print(access_index)
                access_index = 0
            self.recent_index = access_index
            return self.stack[access_index].getNotes(offset)

class ChordSet:
    
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.recent_root = -1
        self.chords = [ChordStack() for i in range(12)]
    
    def addChord(self, root, notes, can_change):
        self.chords[root].addChord(notes, can_change)
        
    def getChord(self, root):
        is_recent = (root == self.recent_root)
        self.recent_root = root
        return self.chords[root % 12].getNotes(root, ENABLE_RANDOMNESS, is_recent)

class ChordMgr:
    def __init__(self):
        self.active = ""
        self.active_index = -1
        self.jazziness = 0
        self.classes = []
    
    def addChordClass(self, name, colour):
        self.classes.append(ChordSet(name, colour))
        self.recent = name
    
    def addChord(self, root, notes, can_change=True):
        self.classes[-1].addChord(root, notes, can_change)
        
    def getChord(self, root):
        return self.classes[self.active_index].getChord(root)
        
    def setMode(self, index):
        if index >= 0:
            self.active = self.classes[index].name
        else:
            self.active = ""
        self.active_index = index

    def getMode(self):
        return self.active_index
    
    def setJazziness(self, val):
        self.jazziness = val
    
    def getJazziness(self):
        return self.jazziness

chords = ChordMgr()

#-----------
# Major chord set
#-----------
chords.addChordClass("Major", lightingconsts.colours["YELLOW"])

# Primary notes
#--------------
chords.addChord(0, MAJOR_CHORD, False)
chords.addChord(0, MAJOR_MAJOR_SEVENTH_CHORD)
chords.addChord(0, SUS2_CHORD)

chords.addChord(2, MINOR_CHORD, False)
chords.addChord(2, MAJOR_CHORD, False)
chords.addChord(2, MAJOR_MINOR_SEVENTH_CHORD)

chords.addChord(4, MINOR_CHORD)
chords.addChord(4, MINOR_MINOR_SEVENTH_CHORD, False)

chords.addChord(5, MAJOR_CHORD)
chords.addChord(5, MAJOR_MAJOR_SEVENTH_CHORD, False)
chords.addChord(5, MAJOR_MINOR_SEVENTH_CHORD, False)
chords.addChord(5, MAJOR_MAJOR_SIXTH_CHORD, False)
chords.addChord(5, MINOR_MAJOR_SIXTH_CHORD, False)
chords.addChord(5, SUS4_CHORD)

chords.addChord(7, MAJOR_CHORD, False)
chords.addChord(7, SUS4_CHORD)
chords.addChord(7, MAJOR_MINOR_SEVENTH_CHORD, False)

chords.addChord(9, MINOR_CHORD, False)
chords.addChord(9, MINOR_MINOR_SEVENTH_CHORD, False)
chords.addChord(9, SUS4_CHORD)

chords.addChord(11, DIM_CHORD)

# Non-scale notes
#----------------
chords.addChord(1, MAJOR_CHORD)

chords.addChord(3, MAJOR_CHORD)
chords.addChord(3, MAJOR_MAJOR_SIXTH_CHORD, False)

chords.addChord(6, DIM_MAJOR_SEVENTH_CHORD)

chords.addChord(8, MAJOR_MAJOR_SIXTH_CHORD, False)
chords.addChord(8, MAJOR_CHORD, False)
chords.addChord(8, SUS2_CHORD)

chords.addChord(10, MAJOR_MAJOR_SIXTH_CHORD, False)
chords.addChord(10, MAJOR_CHORD)
chords.addChord(10, MAJOR_MAJOR_SEVENTH_CHORD, False)

#-----------
# Minor chord set
#-----------
chords.addChordClass("Minor", lightingconsts.colours["ORANGE"])

# Primary notes
#--------------
chords.addChord(0, MINOR_CHORD)

chords.addChord(2, DIM_CHORD)

chords.addChord(3, MAJOR_CHORD)

chords.addChord(5, MINOR_CHORD)

chords.addChord(7, MAJOR_CHORD)

chords.addChord(8, MAJOR_CHORD)

chords.addChord(10, MAJOR_CHORD)


def process(command):
    """Called with an event to be processed by your note processor. Events aren't filtered so you'll want to make sure your processor checks that events are notes.

    Args:
        command (ParsedEvent): An event for your function to modify/act on.
    """
    command.addProcessor("Chord Processor")
    
    if not INIT_COMPLETE:
        processInit(command)
        return
    
    # If command is a note
    elif command.type is eventconsts.TYPE_NOTE:
        if not command.is_lift:
            # How far note is up scale
            scale_pos = command.note - ROOT_NOTE
            
            notes_list = chords.getChord(scale_pos)
            notes_events = []
            for i in range(1, len(notes_list)):
                if ENABLE_RANDOMNESS:
                    new_velocity = int(2*(rng.random() - 0.5) * MAX_VEL_OFFSET * (command.value/127)) + command.value
                    if new_velocity > 127:
                        new_velocity = 127
                    elif new_velocity < 0:
                        new_velocity = 0
                else:
                    new_velocity = command.value
                notes_events.append(processorhelpers.RawEvent(command.status, notes_list[i] + ROOT_NOTE, new_velocity))
            
            send_notes = processorhelpers.ExtensibleNote(command, notes_events)
            command.act("Played chord")
            
            notesDown.noteOn(send_notes)
        else:
            command.act("Stopped chord")
            notesDown.noteOff(command)
    
    pass

def processInit(command):
    global ROOT_NOTE, ENABLE_RANDOMNESS, INIT_COMPLETE, FORWARD_NOTES
    if command.type is eventconsts.TYPE_NOTE:
        ROOT_NOTE = command.note % 12
        command.act("Set root note to " + str(ROOT_NOTE))
    elif command.type is eventconsts.TYPE_PAD:
        if not command.is_lift:
            coords = command.getPadCoord()
            
            if coords[1] == 0:
                if coords[0] < len(chords.classes):
                    chords.setMode(coords[0])
                    command.handle("Set chord mode to " + chords.active)
                else:
                    command.handle("Init function catch-all", silent=True)
                
            elif coords == (6, 1):
                jazz = round((float(command.value) / 127)**2 * 7)
                chords.setJazziness(jazz)
                command.handle("Set jazziness to " + str(jazz))
            elif coords == (7, 1):
                ENABLE_RANDOMNESS = not ENABLE_RANDOMNESS
                command.handle("Set randomness to " + str(ENABLE_RANDOMNESS))
            else:
                command.handle("Init function catch-all", silent=True)
            
        else:
            command.handle("Init function lift catch-all", silent=True)

    if ROOT_NOTE != -1 and chords.getMode() != -1:
        INIT_COMPLETE = True
        FORWARD_NOTES = False
        internal.extendedMode.revert(eventconsts.INCONTROL_PADS)

def redraw(lights):
    """Called when a redraw is taking place. Use this to draw menus to allow your users to choose options. Most of the time, you should leave this empty.

    Args:
        lights (LightMap): The lights to draw to
    """
    if (not INIT_COMPLETE) and internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        for i in range(min(len(chords.classes), 8)):
            mode = (i == chords.active_index) + 1
            lights.setPadColour(i, 0, chords.classes[i].colour, mode)


        lights.setPadColour(6, 1, JAZZY_COLOURS[chords.jazziness])
        
        if ENABLE_RANDOMNESS:
            lights.setPadColour(7, 1, lightingconsts.colours["TEAL"])
        else:
            lights.setPadColour(7, 1, lightingconsts.colours["DARK GREY"])
        
        lights.solidifyAll()

def activeStart():
    """Called when your note mode is made active
    """
    global FORWARD_NOTES, INIT_COMPLETE
    FORWARD_NOTES = True
    INIT_COMPLETE = False


def activeEnd():
    """Called wen your note mode is no-longer active
    """
    global COLOUR, ENABLE_RANDOMNESS, ROOT_NOTE
    # Reset current colour to default
    COLOUR = DEFAULT_COLOUR
    ROOT_NOTE = -1
    ENABLE_RANDOMNESS = False
    chords.setMode(-1)
    

