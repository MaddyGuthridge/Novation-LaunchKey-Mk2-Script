"""
noteprocessors > processnotes.py
This script forwards events to note processors depending on the current mode.

Author: Miguel Guthridge

"""

#
# Add custom event processors to this list
#
imports = ["default", "error"]
#
#
#

import config
import internal
import noteprocessors

# Import custom processors specified in list above
print("Importing Note Processors")
customProcessors = []
for x in range(len(imports)):
    try:
        customProcessors.append( __import__("noteprocessors." + imports[x]) )
        print (" - Successfully imported: ", imports[x])
    except ImportError:
        print (" - Error importing: ", imports[x])
print("Note Processor import complete")

def process(command):
    for x in imports:
        object_to_call = getattr(noteprocessors, x)
        if object_to_call.NOTE_MODE == internal.noteMode.getState():
            object_to_call.process(command)
        
            if command.handled: return


