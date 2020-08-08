"""PluginProcessors > bbcso.py

This script processes events when the BBC Symphony Orchesra plugin is active.
It allows the use of keyswitches, and maps faders to expression, dynamics and reverb.

Author: Miguel Guthridge
"""

plugins = ["BBC Symphony Orchestra"]


import config
import internal
import lightingconsts
import eventconsts
import eventprocessor

# Constants for event remapping
EXPRESSION = 11
DYNAMICS = 1
REVERB = 19


# Called when plugin is top plugin
def topPluginStart():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS)
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS)
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS)
    return

# Called when plugin is no longer top plugin
def topPluginEnd():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
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
        for x in range(0, 8):
            lights.setPadColour(x, 1, lightingconsts.COLOUR_LIGHT_BLUE)

    return

def process(command):
    command.actions.addProcessor("BBCSO Processor")

    if command.type is eventconsts.TYPE_BASIC_PAD:
        # Dispatch event to extended mode
        internal.sendMidiMessage(command.status, command.note, command.value)

        if command.coord_Y == 1:
            # Use coord_X number for keyswitch number
            keyswitchNum = command.coord_X

            command.edit(eventprocessor.rawEvent(0x90, keyswitchNum, command.value))

    """ Link to parameters - Fix this once API updates
    if command.id == eventconsts.BASIC_FADER_1:
        command.edit(eventprocessor.rawEvent(0xB0, EXPRESSION, command.value))
    
    if command.id == eventconsts.BASIC_FADER_2:
        command.edit(eventprocessor.rawEvent(0xB0, DYNAMICS, command.value))
    
    if command.id == eventconsts.BASIC_FADER_3:
        command.edit(eventprocessor.rawEvent(0xB0, REVERB, command.value))
    """


    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
    return


