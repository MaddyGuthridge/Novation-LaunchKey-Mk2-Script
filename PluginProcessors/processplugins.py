"""
processwindowed.py
This script forwards events to event processors for FL Studio Windows

"""

#
# Add custom event processors to this list
#
imports = ["fpc"]
#
#
#


import internal
import PluginProcessors

# Import custom processors specified in list above
customProcessors = []
for x in range(len(imports)):
    try:
        customProcessors.append( __import__("PluginProcessors." + imports[x]) )
        print ("Successfully imported: ", imports[x])
        print(customProcessors)
    except ImportError:
        print ("Error importing: ", imports[x])

"""
# Returns true if custom processor at index can handle events in window
def customProcessor_canHandle(processorNum):
    for x in range(len(customProcessors[processorNum].plugins)):
        # Currently searching for plugin name in header (could cause issues if poorly named plugins are used)
        # Eventually switch to ends with
        # Or just use a get plugin name function when they add that
        last = -1
        length = len(internal.window.active)
        for y in range(length):
            if internal.window.active[y] is '(':
                last = y + 1
        if last == -1 or last > length: # If no brackets found
            return False
        plugin = internal.window.active[last: -2]
        if customProcessors[processorNum].plugins[x] == plugin:
            return True

    return False

# Runs through custom processors
def process(command):
    for x in range(len(customProcessors)):
        if customProcessor_canHandle(x):
            customProcessors[x].process(command)
        if command.handled == True: break
"""

def process(command):
    for x in imports:
        object_to_call = getattr(PluginProcessors, x)
        if can_handle(object_to_call):
            object_to_call.process(command)

def can_handle(object_to_call):
    last = -1
    length = len(internal.window.active)
    for y in range(length):
        if internal.window.active[y] is '(':
            last = y + 1
    if last == -1 or last > length: # If no brackets found
        return False
    for x in range(len(object_to_call.plugins)):
        # Currently using Plugin Name (in backets at the end of string)
        # This causes issues when people use templates for their plugins
        # Or just use a get plugin name function when they add that
        
        plugin = internal.window.active[last: -2]
        if object_to_call.plugins[x] == plugin:
            return True

    return False
