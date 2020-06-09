"""
eventconsts.py
This file contains constants for buttons/faders/knobs sent from the controller.

You shouldn't need to adjust these values, 
but if you are modifying the script for use with a different controller with the same features,
this is the place to start.
"""

# Define faders
FADER_1
FADER_2
FADER_3
FADER_4
FADER_5
FADER_6
FADER_7
FADER_8
FADER_9

Faders = [FADER_1, FADER_2, FADER_3, FADER_4, FADER_5, FADER_6, FADER_7, FADER_8, FADER_9]


# Define pad references

PAD_TOP_1 = 0x60
PAD_TOP_2 = 0x61
PAD_TOP_3 = 0x62
PAD_TOP_4 = 0x63
PAD_TOP_5 = 0x64
PAD_TOP_6 = 0x65
PAD_TOP_7 = 0x66
PAD_TOP_8 = 0x67

PAD_BOTTOM_1 = 0x70
PAD_BOTTOM_2 = 0x71
PAD_BOTTOM_3 = 0x72
PAD_BOTTOM_4 = 0x73
PAD_BOTTOM_5 = 0x74
PAD_BOTTOM_6 = 0x75
PAD_BOTTOM_7 = 0x76
PAD_BOTTOM_8 = 0x77

PAD_TOP_BUTTON = 0x68
PAD_BOTTOM_BUTTON = 0x78

Pads = [PAD_TOP_1, PAD_TOP_2, PAD_TOP_3, PAD_TOP_4, PAD_TOP_5, PAD_TOP_6, PAD_TOP_7, PAD_TOP_8, PAD_BOTTOM_1, PAD_BOTTOM_2, PAD_BOTTOM_3, PAD_BOTTOM_4, PAD_BOTTOM_5, PAD_BOTTOM_6, PAD_BOTTOM_7, PAD_BOTTOM_8, PAD_TOP_BUTTON, PAD_BOTTOM_BUTTON]

# Define Basic Mode pad references
BASIC_PAD_TOP_1 = 0x28
BASIC_PAD_TOP_2 = 0x29
BASIC_PAD_TOP_3 = 0x2A
BASIC_PAD_TOP_4 = 0x2B
BASIC_PAD_TOP_5 = 0x30
BASIC_PAD_TOP_6 = 0x31
BASIC_PAD_TOP_7 = 0x32
BASIC_PAD_TOP_8 = 0x33

BASIC_PAD_BOTTOM_1 = 0x24
BASIC_PAD_BOTTOM_2 = 0x25
BASIC_PAD_BOTTOM_3 = 0x26
BASIC_PAD_BOTTOM_4 = 0x27
BASIC_PAD_BOTTOM_5 = 0x2C
BASIC_PAD_BOTTOM_6 = 0x2D
BASIC_PAD_BOTTOM_7 = 0x2E
BASIC_PAD_BOTTOM_8 = 0x2F

BASIC_PAD_TOP_BUTTON = 0x68
BASIC_PAD_BOTTOM_BUTTON = 0x69
