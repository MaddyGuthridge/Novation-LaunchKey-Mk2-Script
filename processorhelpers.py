"""processorhelpers.py

This script includes objects useful for event processors. 
It is worth investigating potential applications of these functions when writing your processors, 
or adding other frequently-required functions here.

Author: Miguel Guthridge
"""

import config

class UI_mode_handler: 
    """This object is used to manage menu layers, which can be toggled and switched through.
        It is best used in handler scripts to allow for a plugin or window to have multiple menus.
    """
    
    def __init__(self, num_modes):
        """Create instance of UIModeHandler.

        Args:
            num_modes (int): The number of different menus to be contained in the object
        """
        self.mode = 0
        self.num_modes = num_modes

    # Switch to next mode
    def nextMode(self):
        """Jump to the next menu layer

        Returns:
            int: mode number
        """
        self.mode += 1
        if self.mode == self.num_modes:
            self.mode = 0
        
        return self.mode

    def resetMode(self):
        """Resets menu layer to zero
        """
        self.mode = 0

    # Get current mode number
    def getMode(self):
        """Returns mode number

        Returns:
            int: mode number
        """
        return self.mode

def snap(value, snapTo):
    """Returns a snapped value

    Args:
        value (float): value being snapped
        snapTo (float): value to snap to

    Returns:
        float: value after snapping
    """
    if abs(value - snapTo) <= config.SNAP_RANGE and config.ENABLE_SNAPPING:
        return snapTo
    else: return value

def didSnap(value, snapTo):
    """Returns a boolean indicating whether a value was snapped

    Args:
        value (float): value being snapped
        snapTo (float): value to snap to

    Returns:
        bool: whether the value would snap
    """
    if abs(value - snapTo) <= config.SNAP_RANGE and config.ENABLE_SNAPPING:
        return True
    else: return False

def toFloat(value, min = 0, max = 1):
    """Converts a MIDI event value (data2) to a float to set parameter values.

    Args:
        value (int): MIDI event value (0-127)
        min (float, optional): lower value to set between. Defaults to 0.
        max (float, optional): upper value to set between. Defaults to 1.

    Returns:
        float: range value
    """
    return (value / 127) * (max - min) + min

class ExtensibleNote():
    """A note with other notes tacked on. Used for playing chords in note processors.
    """
    def __init__(self, root_note, extended_notes):
        """Create instance of ExtensibleNote object

        Args:
            root_note (note event): the note that the user pressed (or a modified version of it). 
                Can be of type RawEvent, ProcessedEvent or FLMidiMessage.
                
            extended_notes (list of note events): List of notes that should also be pressed. Can be of 
                same types as root_note, but RawEvent is recommended for performance reasons.
        """
        self.root = root_note
        self.extended_notes = extended_notes
