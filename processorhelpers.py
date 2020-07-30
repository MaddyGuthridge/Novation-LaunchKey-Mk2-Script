"""
processorhelpers.py
This script includes objects useful for event processors
"""

import config

# Use for creating multiple UIs, which can be switched through. 
# Create instances in handler scripts
class UI_mode_handler: 
    
    def __init__(self, num_modes):
        self.mode = 0
        self.num_modes = num_modes

    # Switch to next mode
    def nextMode(self):
        self.mode += 1
        if self.mode == self.num_modes:
            self.mode = 0
        
        return self.mode

    def resetMode(self):
        self.mode = 0

    # Get current mode number
    def getMode(self):
        return self.mode

# Returns snap value
def snap(value, snapTo):
    if abs(value - snapTo) <= config.SNAP_RANGE:
        return snapTo
    else: return value

# Returns snap value
def didSnap(value, snapTo):
    if abs(value - snapTo) <= config.SNAP_RANGE:
        return True
    else: return False

# Converts MIDI event range to float for use in volume, pan, etc functions
def toFloat(value, min = 0, max = 1):
    return (value / 127) * (max - min) + min

# Allows fancy note stuff like chord mode and the like
class ExtensibleNote():
    
    def __init__(self, root_note, extended_notes):
        self.root = root_note
        self.extended_notes = extended_notes
