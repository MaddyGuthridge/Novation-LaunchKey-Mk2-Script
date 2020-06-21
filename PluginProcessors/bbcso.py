"""
bbcso.py
this script processes events when the BBC Symphony Orchesra plugin is active

"""

plugins = ["BBC Symphony Orchestra"]


import config
import internal
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
    return

# Called when plugin is no longer top plugin
def topPluginEnd():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
       internal.extendedMode.setVal(True, eventconsts.INCONTROL_FADERS)
       internal.extendedMode.setVal(True, eventconsts.INCONTROL_KNOBS)
    return

# Called when plugin brought to foreground
def activeStart():
    
    return

# Called when plugin no longer in foreground
def activeEnd():
    
    return

def redraw(lights):
    return

def process(command):
    command.actions.addProcessor("BBCSO Processor")

    if command.id == eventconsts.BASIC_FADER_1:
        command.edit(eventprocessor.rawEvent(0xB0, EXPRESSION, command.value))
    
    if command.id == eventconsts.BASIC_FADER_2:
        command.edit(eventprocessor.rawEvent(0xB0, DYNAMICS, command.value))
    
    if command.id == eventconsts.BASIC_FADER_3:
        command.edit(eventprocessor.rawEvent(0xB0, REVERB, command.value))

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
    return


