"""
internal > __init__.py

This module contains functions that maintain the internal state of the controller.
 - Active window manager
 - Extended mode manager
 - etc

Author: Miguel Guthridge
"""


from .state import sharedInit, extendedMode, errors, getPortExtended
from .messages import sendInternalMidiMessage, sendCompleteInternalMidiMessage, sendMidiMessage, sendCompleteMidiMessage, toMidiMessage
from .logging import debugLog, getLineBreak, printCommand, printCommandOutput, getTab
from .windowstate import window
from .shiftstate import shift
from .misc import idleProcessor, beat, refreshProcessor, processSysEx
from .notemanager import noteMode, notesDown
from .snap import snap
