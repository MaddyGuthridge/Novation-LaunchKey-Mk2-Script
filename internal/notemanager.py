"""
internal > notemanager.py

Contains objects and classes to manage notes and note modes, as well as pad presses.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

from . import consts
import channels

from internal.logging import debugLog

class NoteModeState:
    """Manages state of current note mode
    """
    current_state = consts.NOTE_STATE_NORMAL

    def getState(self):
        """Returns current note state

        Returns:
            str: Note state name
        """
        return self.current_state

    def setState(self, newState):
        """Set note mode state

        Args:
            newState (str): New note mode
        """
        debugLog("Set note mode state to " + newState, consts.DEBUG.NOTE_MODE)
        # Add some checks to ensure not setting into a bad state
        self.current_state = newState

noteMode = NoteModeState()

class NotesDownMgr:
    """Manages notes down; used for note processors, allowing multiple notes to be pressed at the same time.
    """
    def __init__(self):
        """Create object, including notes list to contain notes in.
        """
        # Append note objects to inner list when they are pressed
        self.notes_list = [ [] for _ in range(128)]
        self.active_notes = [0 for _ in range(128)]
        
    def __del__(self):
        """When the object is deleted, remove all existing notes being played.
        """
        self.allNotesOff()
        
    def noteOn(self, ext_note):
        """Add a note to the list

        Args:
            ext_note (ExtensibleNote): The note (and its extensions) to add
        """
        ch_index = channels.channelNumber()
        # Push note onto list
        self.notes_list[ext_note.root.data1].append(ext_note)
        
        # Set root note to on - don't need to - FL does this for us
        # channels.midiNoteOn(ch_index, ext_note.root.data1, ext_note.root.data2)
        
        for note in ext_note.extended_notes:
            if self.active_notes[note.data1]:
                channels.midiNoteOn(ch_index, note.data1, 0)
            channels.midiNoteOn(ch_index, note.data1, note.data2)
            self.active_notes[note.data1] += 1
        
        
    def noteOff(self, note):
        """Remove a note from the notes list

        Args:
            note (RawEvent): The note to lift
        """
        ch_index = channels.channelNumber()
        
        note_num = note.data1
        
        # Don't need to turn root note off - FL does this for us
        # channels.midiNoteOn(ch_index, note_num, 0)
        
        # Get ext_note from list - return early if list is empty
        if len(self.notes_list[note_num]) == 0: return
        ext_note = self.notes_list[note_num].pop()
        
        # Loop through and turn off any notes that were associated with that note
        for enote in ext_note.extended_notes:
            self.active_notes[enote.data1] -= 1
            if not self.active_notes[enote.data1]:
                channels.midiNoteOn(ch_index, enote.data1, 0)
            
        
    def allNotesOff(self):
        """Remove all notes from the list
        """
        ch_index = channels.channelNumber()
        
        self.notes_list = [ [] for _ in range(128)]
        self.active_notes = [0 for _ in range(128)]
        
        # Send note off to all notes
        for x in range(128):
            channels.midiNoteOn(ch_index, x, 0)
    
notesDown = NotesDownMgr()


class PadMgr:
    """Contains whether or not a pad is down (for use in extended mode)
    """
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
        """Press a pad down at given coordinates

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        self.padsDown[x][y] = True
    
    def lift(self, x, y):
        """Lift a pad at given coordinates

        Args:
            x (int): X coordinates
            y (int): Y coordinates
        """
        self.padsDown[x][y] = False

    def getVal(self, x, y):
        """Get the state of a pad at the coordinates

        Args:
            x (int): X coordinate
            y (int): Y coordinate

        Returns:
            bool: Whether the pad is down
        """
        return self.padsDown[x][y]

pads = PadMgr()

