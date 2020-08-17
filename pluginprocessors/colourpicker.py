"""
pluginprocessors > colourpicker.py

The file handles events when the colour picker window is active.
Currently, this doesn't work in the playlist as there is no way to get selected track

Author: Miguel Guthridge
"""

plugins = ["Color selector"]


import config
import internal
import eventconsts
import eventprocessor
import lightingconsts
import internal.consts

import ui
import playlist
import patterns
import mixer
import channels

COLOUR_MAP = [
    [lightingconsts.colours["RED"], lightingconsts.colours["LIGHT BLUE"]],
    [lightingconsts.colours["ORANGE"], lightingconsts.colours["BLUE"]],
    [lightingconsts.colours["YELLOW"], lightingconsts.colours["PURPLE"]],
    [lightingconsts.colours["GREEN"], lightingconsts.colours["PINK"]],
    [-1, -1],
    [-1, -1],
    [-1, -1],
    [-1, -1],
    [-1, -1]
]

FL_DEFAULT_COLOUR = -12037802

COLOUR_HEX_MAP = [
    [-4242624, -13462892],
    [-5675720, -13283936],
    [-3947699, -4358957],
    [-12533888, -3647046],
    [FL_DEFAULT_COLOUR, FL_DEFAULT_COLOUR],
    [FL_DEFAULT_COLOUR, FL_DEFAULT_COLOUR],
    [FL_DEFAULT_COLOUR, FL_DEFAULT_COLOUR],
    [FL_DEFAULT_COLOUR, FL_DEFAULT_COLOUR],
]


# Called when plugin is top plugin (not neccesarily focused)
def topPluginStart():
    
    return

# Called when plugin is no longer top plugin (not neccesarily focused)
def topPluginEnd():
    
    return

# Called when plugin brought to foreground (focused)
def activeStart():
    # Only in extended mode: uncomment lines to set inControl mode
    if internal.extendedMode.query():
        internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS) # Pads
    return

# Called when plugin no longer in foreground (end of focused)
def activeEnd():
    # Only in extended mode: uncomment lines to revert to previous inControl modes
    if internal.extendedMode.query():
        internal.extendedMode.revert(eventconsts.INCONTROL_PADS) # Pads\
    
    # Revert active plugin to previous state
    internal.window.revertPlugin()
    return

# Called when redrawing UI on pads. Set colours of lights here.
def redraw(lights):
    lights.setFromMatrix(COLOUR_MAP)
    lights.solidifyAll()
    return

# Called when processing commands. 
def process(command):
    # Add event processor to actions list (useful for debugging)
    command.actions.addProcessor("Colour Picker Processor")

    if command.type == eventconsts.TYPE_PAD and command.coord_X != 8:
        command.handled == True
        if command.is_lift:

            colour = COLOUR_HEX_MAP[command.coord_X][command.coord_Y]

            if internal.window.active_fl_window == internal.consts.WINDOW_PLAYLIST:
                patterns.setPatternColor(patterns.patternNumber(), colour)
            
            if internal.window.active_fl_window == internal.consts.WINDOW_MIXER:
                mixer.setTrackColor(mixer.trackNumber(), colour)

            if internal.window.active_fl_window == internal.consts.WINDOW_CHANNEL_RACK:
                channels.setChannelColor(channels.channelNumber(), colour)
                
            command.actions.appendAction("Set colour to " + str(colour))
            # quit the colour picker
            ui.escape()

    return


