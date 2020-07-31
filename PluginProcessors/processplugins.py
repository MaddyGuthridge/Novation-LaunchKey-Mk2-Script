"""PluginProcessors > processplugins.py

This script forwards events to any plugin processors that can handle the currently active plugin.
More plugin processors can be added by adding them to the import list.

Author: Miguel Guthridge
"""

#
# Add custom event processors to this list
#
imports = ["fpc", "bbcso"]
#
#
#

import config
import internal
import PluginProcessors

# Import custom processors specified in list above
print("Importing Plguin Processors")
customProcessors = []
for x in range(len(imports)):
    try:
        customProcessors.append( __import__("PluginProcessors." + imports[x]) )
        print (" - Successfully imported: " + imports[x])
    except ImportError:
        print (" - Error importing: " + imports[x])
print("Plugin Processor import complete")

# Called when plugin is top plugin
def topPluginStart():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
        for x in imports:
            object_to_call = getattr(PluginProcessors, x)
            if can_handle(object_to_call):
                object_to_call.topPluginStart()
    return

# Called when plugin is no longer top plugin
def topPluginEnd():
    # Only in extended mode:
    if internal.PORT == config.DEVICE_PORT_EXTENDED:
        for x in imports:
            object_to_call = getattr(PluginProcessors, x)
            if can_handle(object_to_call):
                object_to_call.topPluginEnd()
    return

# Called when plugin brought to foreground
def activeStart():
    for x in imports:
        object_to_call = getattr(PluginProcessors, x)
        if can_handle(object_to_call):
            object_to_call.activeStart()
    return

# Called when plugin no longer in foreground
def activeEnd():
    for x in imports:
        object_to_call = getattr(PluginProcessors, x)
        if can_handle(object_to_call):
            object_to_call.activeEnd()
    return

def redraw(lights):
    for x in imports:
        object_to_call = getattr(PluginProcessors, x)
        if can_handle(object_to_call):
            object_to_call.redraw(lights)

def process(command):
    for x in imports:
        object_to_call = getattr(PluginProcessors, x)
        if can_handle(object_to_call):
            object_to_call.process(command)
        
        if command.handled: return

def can_handle(object_to_call):
    for x in range(len(object_to_call.plugins)):
        if object_to_call.plugins[x] == internal.window.active_plugin:
            return True

    return False

