"""
internalconstants.py
This file contains constants used by the script to allow it to function properly.
It is not recommended that the user modify these constants, as they may break the script.

"""
#---------------------------------
# Script Info
#---------------------------------

SCRIPT_NAME = "Novation LaunchKey Mk2 Controller Script"
SCRIPT_AUTHOR = "Miguel Guthridge"
SCRIPT_VERSION = "1.1.1"

#---------------------------------
# Window constants
#---------------------------------

WINDOW_PLAYLIST = 2
WINDOW_PIANO_ROLL = 3
WINDOW_CHANNEL_RACK = 1
WINDOW_MIXER = 0
WINDOW_BROWSER = 4

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
