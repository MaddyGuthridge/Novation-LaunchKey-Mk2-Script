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
SCRIPT_VERSION_MAJOR = 2
SCRIPT_VERSION_MINOR = 0
SCRIPT_VERSION_REVISION = 0
SCRIPT_VERSION_SUFFIX = ""
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
# Event handling constants
#---------------------------------

EVENT_NO_HANDLE = 0
EVENT_HANDLE = 1
EVENT_IGNORE = 2

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
class DEBUG:
    ERROR = "Errors"
    PROCESSOR_PERFORMANCE = "Processor performance"
    LIGHTING_RESET = "Lighting reset"
    LIGHTING_MESSAGE = "Lighting message"
    DISPATCH_EVENT = "Dispatch event"
    IDLE_PERFORMANCE = "Idle Performance"
    ANIMATION_IDLE_TIMERS = "Timers"
    EVENT_DATA = "Event data"
    EVENT_ACTIONS = "Event actions"
    WINDOW_CHANGES = "Window changed"
    WARNING_DEPRECIATED_FEATURE = "Depreciated feature"
    DEVICE_TYPE = "Device type"
    NOTE_MODE = "Note mode"
    SHIFT_EVENTS = "Shift events"

FORCE_DEBUG_MODES_LIST = [DEBUG.ERROR, DEBUG.EVENT_DATA, DEBUG.EVENT_ACTIONS, DEBUG.WINDOW_CHANGES, DEBUG.WARNING_DEPRECIATED_FEATURE, DEBUG.NOTE_MODE]

#---------------------------------
# Data for internal communication
#---------------------------------

# Sent when resetting the idle tick
MESSAGE_RESET_INTERNAL_CONTROLLER = 0x7F00BE
# Sent when a script restarts to tell the other script to reset its self
MESSAGE_RESTART_DEVICE = 0x0000BE

# Sent regarding device crashes
MESSAGE_ERROR_CRASH = 0x7F7FBE
MESSAGE_ERROR_RECOVER = 0x007FBE
MESSAGE_ERROR_RECOVER_DEBUG = 0x017FBE

# Enter debug mode
MESSAGE_ENTER_DEBUG_MODE = 0x027FBE

# Sent for main shift menu
MESSAGE_SHIFT_DOWN = 0x7F01BE
MESSAGE_SHIFT_UP = 0x0001BE
MESSAGE_SHIFT_USE = 0x0101BE

# Sent for note processor modes
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


LOG_TAB_LENGTH = 16
