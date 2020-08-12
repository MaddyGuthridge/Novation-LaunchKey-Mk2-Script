"""
internalconstants.py

This file contains constants used by the script to allow it to function properly.
It is not recommended that the user modify these constants, as they may break the script.

Author: Miguel Guthridge
"""

import midi
import eventconsts

#---------------------------------
# Script Info - Change this if you're forking the project
#---------------------------------

SCRIPT_NAME = "Novation LaunchKey Mk2 Controller Script"
SCRIPT_AUTHOR = "Miguel Guthridge"
SCRIPT_VERSION_MAJOR = 1
SCRIPT_VERSION_MINOR = 3
SCRIPT_VERSION_REVISION = 1
MIN_FL_SCRIPT_VERSION = 7
SCRIPT_URL = "https://github.com/MiguelGuthridge/Novation-LaunchKey-Mk2-Script"
UPDATE_JSON_URL = "https://api.github.com/repos/MiguelGuthridge/Novation-LaunchKey-Mk2-Script/tags"

#---------------------------------
# Device constants
#---------------------------------

DEVICE_UNRECOGNISED = -1
DEVICE_NOT_SET = 0
DEVICE_KEYS_25 = 25
DEVICE_KEYS_49 = 49
DEVICE_KEYS_61 = 61

#---------------------------------

DEVICE_ENQUIRY_MESSAGE = bytes([0xF0, 0x7E, 0x7F, 0x06, 0x01, 0xF7])

DEVICE_RESPONSE_FIRST = bytes([0xF0, 0x7E, 0x00, 0x06, 0x02, 0x00, 0x20, 0x29])
DEVICE_RESPONSE_25 = 123
DEVICE_RESPONSE_49 = 124
DEVICE_RESPONSE_61 = 125

#---------------------------------
# Initialisation states
#---------------------------------
INIT_INCOMPLETE = -1
INIT_OK = 0
INIT_UPDATE_AVAILABLE = 1
INIT_API_OUTDATED = 2
INIT_PORT_MISMATCH = 3

#---------------------------------
# Window constants
#---------------------------------

WINDOW_PLAYLIST = midi.widPlaylist
WINDOW_PIANO_ROLL = midi.widPianoRoll
WINDOW_CHANNEL_RACK = midi.widChannelRack
WINDOW_MIXER = midi.widMixer
WINDOW_BROWSER = midi.widBrowser

WINDOW_STR_SCRIPT_OUTPUT = "Script output"
WINDOW_STR_COLOUR_PICKER = "Color selector"
FL_WINDOW_LIST = ["Mixer", "Channel rack", "Playlist", "Piano roll", "Browser"]
#---------------------------------
# Snapping constants
#---------------------------------

# Mixer snap values
MIXER_VOLUME_SNAP_TO = 0.8 # Snap mixer track volumes to 100%
MIXER_PAN_SNAP_TO = 0.0 # Snap mixer track pannings to Centred
MIXER_STEREO_SEP_SNAP_TO = 0.0 # Snap mixer track stereo separation to Original

# Channel rack snap values
CHANNEL_VOLUME_SNAP_TO = 0.78125 # Snap channel volumes to ~= 78% (FL Default)
CHANNEL_PAN_SNAP_TO = 0.0 # Snap channel pans to Centred

#---------------------------------
# Debug level constants
#---------------------------------

DEBUG_ERROR = "Errors"
DEBUG_PROCESSOR_PERFORMANCE = "Processor performance"
DEBUG_LIGHTING_RESET = "Lighting reset"
DEBUG_LIGHTING_MESSAGE = "Lighting message"
DEBUG_DISPATCH_EVENT = "Dispatch event"
DEBUG_IDLE_PERFORMANCE = "Idle Performance"
DEBUG_ANIMATION_IDLE_TIMERS = "Timers"
DEBUG_EVENT_DATA = "Event data"
DEBUG_EVENT_ACTIONS = "Event actions"
DEBUG_WINDOW_CHANGES = "Window changed"
DEBUG_WARNING_DEPRECIATED_FEATURE = "Depreciated feature"
DEBUG_DEVICE_TYPE = "Device type"
DEBUG_NOTE_MODE = "Note mode"


#---------------------------------
# Data for internal communication
#---------------------------------

MESSAGE_RESET_INTERNAL_CONTROLLER = 0x7F00BE

MESSAGE_ERROR_CRASH = 0x7F7FBE
MESSAGE_ERROR_RECOVER = 0x007FBE

MESSAGE_SHIFT_DOWN = 0x7F01BE
MESSAGE_SHIFT_UP = 0x0001BE
MESSAGE_SHIFT_USE = 0x0101BE

MESSAGE_INPUT_MODE_SELECT = 0x02BE # Mode number as velocity

#---------------------------------
# Note States
#---------------------------------

NOTE_STATE_NORMAL = "Default"
NOTE_STATE_ERROR = "Error"

# What events should be ignored when shifting
SHIFT_IGNORE_TYPES = [eventconsts.TYPE_INCONTROL, eventconsts.TYPE_INTERNAL_EVENT, 
                      eventconsts.TYPE_SYSEX_EVENT, eventconsts.TYPE_SYSTEM_MSG, eventconsts.TYPE_UNRECOGNISED]


OMNI_CHANNEL_STATUS = 0xD
INTERNAL_CHANNEL_STATUS = 0xE

