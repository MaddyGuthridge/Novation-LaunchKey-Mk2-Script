"""
pluginprocessors > bbcso.py

This script processes events when the BBC Symphony Orchesra plugin is active.
It allows the use of keyswitches, and maps faders to expression, dynamics and reverb.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

PLUGINS = ["BBC Symphony Orchestra"]

import plugins

import config
import internal
import lightingconsts
import eventconsts
import processorhelpers

# Constants for event remapping
EXPRESSION = 0
DYNAMICS = 1

NEAR_FAR = 6

REVERB = 2
RELEASE = 3
TIGHTNESS = 4
VARIATION = 14
VIBRATO = 5



# Called when plugin is top plugin
def topPluginStart():
    # Only in extended mode:
    if internal.getPortExtended():
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS)
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS)
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS)
    return

# Called when plugin is no longer top plugin
def topPluginEnd():
    # Only in extended mode:
    if internal.getPortExtended():
       internal.extendedMode.revert(eventconsts.INCONTROL_FADERS)
       internal.extendedMode.revert(eventconsts.INCONTROL_KNOBS)
       internal.extendedMode.revert(eventconsts.INCONTROL_PADS)
    return

# Called when plugin brought to foreground
def activeStart():
    
    return

# Called when plugin no longer in foreground
def activeEnd():
    
    return

def redraw(lights):
    if not internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        processorhelpers.keyswitches.redraw(lights, lightingconsts.BLUE_SHADES, 4, 2)

    return

def process(command):
    command.actions.addProcessor("BBCSO Processor")

    if command.type is eventconsts.TYPE_BASIC_PAD:
        
        if config.USE_FULL_KEYSWITCHES or command.coord_Y == 1:
            
            keyswitch_num = processorhelpers.keyswitches.getNum(command.coord_X, command.coord_Y, 4, 2)

            command.edit(processorhelpers.RawEvent(0x90, keyswitch_num, command.value), "Remap keyswitches")

    #
    # Map parameters
    #
    
    value = processorhelpers.toFloat(command.value)

    if command.type is eventconsts.TYPE_BASIC_FADER:
        if command.coord_X == 0:
            plugins.setParamValue(
                value,
                EXPRESSION,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Expression to " + str(round(value, 2)) + "%")
        elif command.coord_X == 1:
            plugins.setParamValue(
                value,
                DYNAMICS,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Dynamics to " + str(round(value, 2)) + "%")
        
        elif command.coord_X == 7:
            plugins.setParamValue(
                value,
                NEAR_FAR,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Near-far to " + str(round(value, 2)) + "%")
    
    if command.type is eventconsts.TYPE_BASIC_KNOB:
        if command.coord_X == 0:
            plugins.setParamValue(
                processorhelpers.toFloat(command.value),
                REVERB,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Reverb to " + str(round(value, 2)) + "%")
            
        if command.coord_X == 1:
            plugins.setParamValue(
                processorhelpers.toFloat(command.value),
                RELEASE,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Release to " + str(round(value, 2)) + "%")
        
        if command.coord_X == 2:
            plugins.setParamValue(
                processorhelpers.toFloat(command.value),
                TIGHTNESS,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Tightness to " + str(round(value, 2)) + "%")
        
        if command.coord_X == 3:
            plugins.setParamValue(
                processorhelpers.toFloat(command.value),
                VARIATION,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Variation to " + str(round(value, 2)) + "%")
        
        if command.coord_X == 4:
            plugins.setParamValue(
                processorhelpers.toFloat(command.value),
                VIBRATO,
                internal.window.getPluginIndex()
            )
            command.handle("Set BBCSO Vibrato to " + str(round(value, 2)) + "%")



    return

def beatChange(beat):
    pass
