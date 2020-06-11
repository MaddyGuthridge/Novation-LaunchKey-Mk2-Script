"""
config.py
This file contains variables intended for the user to edit to suit their needs.
It also contains constants which are used to enable featurs such as snapping.
You can modify those values too, and the script will still work, but it may not operate in ways you would expect.

"""

#-------------------------------
# USER VARIABLES
#-------------------------------

LONG_PRESS_TIME = 0.5 # Change how long a long press needs to be held for

ENABLE_SNAPPING = True # Change to False to prevent faders and knobs from snapping to default values
SNAP_RANGE = 0.03 # Will snap if within this disatnce of snap value

START_IN_INCONTROL_KNOBS = True
START_IN_INCONTROL_FADERS = True
START_IN_INCONTROL_PADS = True

# Port values. Change these to match the ports for each device set in FL Studio
DEVICE_PORT_BASIC = 220
DEVICE_PORT_EXTENDED = 225

#-------------------------------
# CONSTANTS
#-------------------------------

# Mixer snap values
MIXER_VOLUME_SNAP_TO = 0.8 # Snap mixer track volumes to 100%
MIXER_PAN_SNAP_TO = 0.0 # Snap mixer track pannings to Centred
MIXER_STEREO_SEP_SNAP_TO = 0.0 # Snap mixer track stereo separation to Original

# Channel rack snap values
CHANNEL_VOLUME_SNAP_TO = 0.78125 # Snap channel volumes to ~= 78% (FL Default)
CHANNEL_PAN_SNAP_TO = 0.0 # Snap channel pans to Centred


