"""
pluginprocessors > bbcso.py

This script processes events when the BBC Symphony Orchesra plugin is active.
It allows the use of keyswitches, and maps faders to expression, dynamics and reverb.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

PLUGINS = ["BBC Symphony Orchestra"]

import pluginswrapper
from . import spitfire_generic

import config
import internal
import lightingconsts
import eventconsts
import processorhelpers

# Constants for event remapping
NEAR_FAR = 6
VARIATION = 14



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
            spitfire_generic.setExpression(command)
        elif command.coord_X == 1:
            spitfire_generic.setExpression(command)
        
        elif command.coord_X == 7:
            pluginswrapper.setParamByName("Variation", command.value, -1, VARIATION)
            command.handle("Set BBCSO Near-far", 1)
    
    if command.type is eventconsts.TYPE_BASIC_KNOB:
        if command.coord_X == 0:
            spitfire_generic.setReverb(command)
        elif command.coord_X == 1:
            spitfire_generic.setRelease(command)
        elif command.coord_X == 2:
            spitfire_generic.setTightness(command)
            
        elif command.coord_X == 3:
            pluginswrapper.setParamByName("Variation", command.value, -1, VARIATION)
            command.handle("Set BBCSO Variation", 1)
        
        elif command.coord_X == 4:
            spitfire_generic.setVibrato(command)



    return

def beatChange(beat):
    pass
