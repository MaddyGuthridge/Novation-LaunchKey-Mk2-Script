"""
pluginprocessors > bbcso.py

This script processes events when the BBC Symphony Orchesra plugin is active.
It allows the use of keyswitches, and maps faders to expression, dynamics and reverb.

Author: Miguel Guthridge
"""

plugins = ["BBC Symphony Orchestra"]

FULL_KEYSWITCHES = True

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
        if FULL_KEYSWITCHES:
            for y in range(2):
                for x in range(8):
                    lights.setPadColour(x, y, lightingconsts.colours["LIGHT BLUE"])
        else:
            for x in range(0, 8):
                lights.setPadColour(x, 1, lightingconsts.colours["LIGHT BLUE"])

    return

def process(command):
    command.actions.addProcessor("BBCSO Processor")

    if command.type is eventconsts.TYPE_BASIC_PAD:
        # Dispatch event to extended mode
        internal.sendMidiMessage(command.status, command.note, command.value)
        if FULL_KEYSWITCHES:
            x, y = command.getPadCoord()
            # Fancy branchless stuff
            keyswitch_num = (x)*(x < 4) + (x + 4)*(4 <= x < 8) + 4*y
        else:
            if command.coord_Y == 1:
                # Use coord_X number for keyswitch number
                keyswitch_num = command.coord_X

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


