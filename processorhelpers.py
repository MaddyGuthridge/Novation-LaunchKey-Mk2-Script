"""
processorhelpers.py
This script includes objects useful for event processors
"""

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


class ExtensibleNote():
    
    def __init__(self, root_note, extended_notes):
        self.root = root_note
        self.extended_notes = extended_notes
