"""
internalconstants.py
This file contains constants used by the script to allow it to function properly.
It is not recommended that the user modify these constants, as they may break the script.

"""

import midi

#---------------------------------
# Script Info - Change this if you're forking the project
#---------------------------------

SCRIPT_NAME = "Novation LaunchKey Mk2 Controller Script"
SCRIPT_AUTHOR = "Miguel Guthridge"
SCRIPT_VERSION_MAJOR = 1
SCRIPT_VERSION_MINOR = 0
SCRIPT_VERSION_REVISION = 2
SCRIPT_URL = "https://github.com/MiguelGuthridge/Novation-LaunchKey-Mk2-Script"
UPDATE_JSON_URL = "https://api.github.com/repos/MiguelGuthridge/Novation-LaunchKey-Mk2-Script/tags"

#---------------------------------
# Window constants
#---------------------------------

WINDOW_PLAYLIST = midi.widPlaylist
WINDOW_PIANO_ROLL = midi.widPianoRoll
WINDOW_CHANNEL_RACK = midi.widChannelRack
WINDOW_MIXER = midi.widMixer
WINDOW_BROWSER = midi.widBrowser

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

DEBUG_ERRORS_ONLY = 0
DEBUG_PROCESSOR_PERFORMANCE = 1
DEBUG_DISPATCH_EVENTS = 2
DEBUG_IDLE_PERFORMANCE = 3