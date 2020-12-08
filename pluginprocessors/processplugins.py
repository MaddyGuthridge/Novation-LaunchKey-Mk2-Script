"""
pluginprocessors > processplugins.py

This script forwards events to any plugin processors that can handle the currently active plugin.
More plugin processors can be added by adding them to the import list.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

#
# Add custom event processors to this list
#
imports = ["fpc", "spitfire_bbcso", "slicex", "flex", "spitfire_labs", "piano_generic"]
#
#
#

import channels
import general

import config
import internal
import pluginprocessors
import eventconsts
import processorhelpers

# Import custom processors specified in list above
print("Importing Plguin Processors")
customProcessors = []
for x in range(len(imports)):
    try:
        customProcessors.append( __import__("pluginprocessors." + imports[x]) )
        print (" - Successfully imported:", getattr(pluginprocessors, imports[x]).PLUGINS)
    except ImportError:
        print (" - Error importing: " + imports[x])
print("Plugin Processor import complete")

# Called when plugin is top plugin
def topPluginStart():
    # Only in extended mode:
    if internal.state.PORT == config.DEVICE_PORT_EXTENDED:
        for x in imports:
            object_to_call = getattr(pluginprocessors, x)
            if canHandle(object_to_call):
                object_to_call.topPluginStart()
    return

# Called when plugin is no longer top plugin
def topPluginEnd():
    # Only in extended mode:
    if internal.state.PORT == config.DEVICE_PORT_EXTENDED:
        for x in imports:
            object_to_call = getattr(pluginprocessors, x)
            if canHandle(object_to_call):
                object_to_call.topPluginEnd()
    return

# Called when plugin brought to foreground
def activeStart():
    for x in imports:
        object_to_call = getattr(pluginprocessors, x)
        if canHandle(object_to_call):
            object_to_call.activeStart()
    return

# Called when plugin no longer in foreground
def activeEnd():
    for x in imports:
        object_to_call = getattr(pluginprocessors, x)
        if canHandle(object_to_call):
            object_to_call.activeEnd()
    return

def redraw(lights):
    for x in imports:
        object_to_call = getattr(pluginprocessors, x)
        if canHandle(object_to_call):
            object_to_call.redraw(lights)

mute_toggle_channel = None
previous_channel_volume = None

def process(command):
    
    # REQUIRES SCRIPTING VERSION 8
    #if general.getVersion() >= 8:
    # Process pitch bend wheel
    if command.id == eventconsts.PITCH_BEND:
        current_channel = channels.selectedChannel()
        channels.setChannelPitch(current_channel, processorhelpers.toFloat(command.value, -1, 1))
    
    # Process master fader changing selected channel volume.
    if command.id == eventconsts.BASIC_FADER_9:
        current_channel = channels.selectedChannel()
        volume = processorhelpers.snap(processorhelpers.toFloat(command.value), internal.consts.CHANNEL_VOLUME_SNAP_TO)
        channels.setChannelVolume(current_channel, volume)
        action = "Set " + channels.getChannelName(current_channel) + " volume to " + str(round(volume * 100)) + "%"
        if processorhelpers.didSnap(processorhelpers.toFloat(command.value), internal.consts.CHANNEL_VOLUME_SNAP_TO):
            action += " [Snapped]"
        command.handle(action)
    
    # Process master fader button to mute/unmute.
    if command.id == eventconsts.BASIC_FADER_BUTTON_9:
        global mute_toggle_channel, previous_channel_volume
        if command.is_lift:
            if type(mute_toggle_channel) is int and type(previous_channel_volume) is float:
                if 0 == channels.getChannelVolume(mute_toggle_channel):
                    channels.setChannelVolume(mute_toggle_channel, previous_channel_volume)
                    command.handle("Unmuted " + channels.getChannelName(mute_toggle_channel))
                mute_toggle_channel = None
                previous_channel_volume = None
        else:
            mute_toggle_channel = channels.selectedChannel()
            previous_channel_volume = channels.getChannelVolume(mute_toggle_channel)
            channels.setChannelVolume(mute_toggle_channel, 0)
            command.handle("Muted " + channels.getChannelName(mute_toggle_channel))
    
    for x in imports:
        object_to_call = getattr(pluginprocessors, x)
        if canHandle(object_to_call):
            object_to_call.process(command)
        
        if command.ignored: return

def beatChange(beat):
    for x in imports:
        object_to_call = getattr(pluginprocessors, x)
        object_to_call.beatChange(beat)

def canHandle(object_to_call):
    for x in range(len(object_to_call.PLUGINS)):
        if object_to_call.PLUGINS[x] == internal.window.getPluginName():
            return True

    return False

