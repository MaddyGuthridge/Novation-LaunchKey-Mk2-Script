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
import processorhelpers
import eventconsts
import lightingconsts

# Import custom processors specified in list above
print("Importing Note Processors")
customProcessors = []
for x in range(len(imports)):
    try:
        __import__("noteprocessors." + imports[x])
        customProcessors.append(imports[x])
        print (" - Successfully imported: ", imports[x])
    except ImportError:
        print (" - Error importing: ", imports[x])
print("Note Processor import complete")


# Object to hold place in note mode menu
noteModeMenu = processorhelpers.UiModeHandler(len(customProcessors) // 16 + 1)

noteMenuActive = False

def process(command):
    for x in customProcessors:
        object_to_call = getattr(noteprocessors, x)
        if object_to_call.NOTE_MODE == internal.noteMode.getState():
            object_to_call.process(command)
        
            if command.handled: return

def redrawNoteModeMenu(lights):
    if noteMenuActive:
        redrawTo = min(len(customProcessors) - 16*noteModeMenu.getMode(), 16)
        
        for ctr in range(16*noteModeMenu.getMode(), 16*noteModeMenu.getMode() + redrawTo):
            
            x = ctr % 8
            y = ctr // 8
            
            lights.setPadColour(x, y, getattr(noteprocessors, customProcessors[ctr]).COLOUR)

def processNoteModeMenu(command):
    
    global noteMenuActive
    
    if command.type is eventconsts.TYPE_PAD and command.is_lift:
        if command.getPadCoord() == (8, 1):
            
            if noteMenuActive:
                if command.is_double_click:
                    noteMenuActive = False
                    noteModeMenu.resetMode()
                else:
                    noteModeMenu.nextMode()
            
            elif not noteMenuActive:
                noteMenuActive = True

