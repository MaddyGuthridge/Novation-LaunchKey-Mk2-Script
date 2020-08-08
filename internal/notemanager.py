"""
internal > notemanager.py

Contains objects and classes to manage notes and note modes, as well as pad presses.

Author: Miguel Guthridge
"""

import internalconstants
import channels

class NoteModeState:
    current_state = internalconstants.NOTE_STATE_NORMAL

    def getState(self):
        return self.current_state

    def setState(self, newState):
        # Add some checks to ensure not setting into a bad state
        self.current_state = newState

noteMode = NoteModeState()

class NotesDownMgr:
    
    def __init__(self):
        # Append note objects to inner list when they are pressed
        self.notes_list = [ [] for _ in range(128)]
        
    def __del__(self):
        self.allNotesOff()
        
    def noteOn(self, ext_note):
        ch_index = channels.channelNumber()
        # Push note onto list
        self.notes_list[ext_note.root.data1].append(ext_note)
        
        # Set root note to on - don't need to - FL does this for us
        # channels.midiNoteOn(ch_index, ext_note.root.data1, ext_note.root.data2)
        
        for note in ext_note.extended_notes:
            channels.midiNoteOn(ch_index, note.data1, note.data2)
        
    def noteOff(self, note):
        ch_index = channels.channelNumber()
        
        note_num = note.data1
        
        # Don't need to turn root note off - FL does this for us
        # channels.midiNoteOn(ch_index, note_num, 0)
        
        # Get ext_note from list - return early if list is empty
        if len(self.notes_list[note_num]) == 0: return
        ext_note = self.notes_list[note_num].pop()
        
        # Loop through and turn off any notes that were associated with that note
        for enote in ext_note.extended_notes:
            channels.midiNoteOn(ch_index, enote.data1, 0)
        
    def allNotesOff(self):
        ch_index = channels.channelNumber()
        
        self.notes_list = [ [] for _ in range(128)]
        
        # Send note off to all notes
        for x in range(128):
            channels.midiNoteOn(ch_index, x, 0)
    
notesDown = NotesDownMgr()


class PadMgr:
    # Contains whether or not a pad is down (for use in extended mode)
    padsDown = [
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False]
    ]

    def press(self, x, y):
        self.padsDown[x][y] = True
    
    def lift(self, x, y):
        self.padsDown[x][y] = False

    def getVal(self, x, y):
        return self.padsDown[x][y]

pads = PadMgr()

