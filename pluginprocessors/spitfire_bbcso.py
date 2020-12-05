"""
pluginprocessors > bbcso.py

This script processes events when the BBC Symphony Orchesra plugin is active.
It allows the use of keyswitches, and maps faders to expression, dynamics and reverb.

Author: Miguel Guthridge
"""

PLUGINS = ["BBC Symphony Orchestra"]

import config
import internal
import lightingconsts
import eventconsts
import processorhelpers

# Constants for event remapping
EXPRESSION = 11
DYNAMICS = 1
REVERB = 19


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

    """ Link to parameters - Fix this once API updates
    if command.id == eventconsts.BASIC_FADER_1:
        command.edit(eventprocessor.rawEvent(0xB0, EXPRESSION, command.value))
    
    if command.id == eventconsts.BASIC_FADER_2:
        command.edit(eventprocessor.rawEvent(0xB0, DYNAMICS, command.value))
    
    if command.id == eventconsts.BASIC_FADER_3:
        command.edit(eventprocessor.rawEvent(0xB0, REVERB, command.value))
    """

    return

def beatChange(beat):
    pass
