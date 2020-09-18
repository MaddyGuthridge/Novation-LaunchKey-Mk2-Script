"""
noteprocessors > processnotes.py
This script forwards events to note processors depending on the current mode.

Author: Miguel Guthridge

"""

#
# Add custom event processors to this list
#
imports = ["default", "error", "scale", "chord", "omni", "unassigned"]
#
#
#

import config
import internal
import internal.consts
import noteprocessors
import processorhelpers
import eventconsts
import lightingconsts

# Import custom processors specified in list above
print("Importing Note Processors")
customProcessors = []       # Not including hidden ones
customProcessorsAll = []    # Includes hidden ones
for x in range(len(imports)):
    try:
        __import__("noteprocessors." + imports[x])
        customProcessorsAll.append(imports[x])
        if not getattr(noteprocessors, imports[x]).SILENT:
            customProcessors.append(imports[x])
        print (" - Successfully imported:", str(getattr(noteprocessors, imports[x]).NAME))
    except ImportError as e:
        print (" - Error importing: ", imports[x])
        if config.DEBUG_HARD_CRASHING:
            raise e
print("Note Processor import complete")


# Object to hold place in note mode menu
noteModeMenu = processorhelpers.UiModeSelector(len(customProcessors) // 16 + 1)

note_menu_active = False

def switchNoteModeMenu(newMode, quiet=False):
    global note_menu_active
    note_menu_active = newMode
    noteModeMenu.resetMode()
    if not quiet:
        if newMode:
            internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
        else:
            internal.extendedMode.revert(eventconsts.INCONTROL_PADS)

def process(command):
    for x in customProcessorsAll:
        object_to_call = getattr(noteprocessors, x)
        if object_to_call.NAME == internal.noteMode.getState():
            
            if object_to_call.FORWARD_NOTES and command.type == eventconsts.TYPE_NOTE and not internal.getPortExtended():
                internal.sendCompleteInternalMidiMessage(command.getDataMIDI())
            
            object_to_call.process(command)
        
            if command.ignored: return

def redrawNoteModeMenu(lights):
    
    current_name = internal.noteMode.getState()
    for ctr in range(len(customProcessorsAll)):
        if getattr(noteprocessors, customProcessorsAll[ctr]).NAME == current_name:
            note_mode_index = ctr
            break
    
    if note_menu_active:
        colour = lightingconsts.colours["DARK GREY"]
        light_mode = lightingconsts.MODE_ON
    else:
        colour = getattr(noteprocessors, customProcessorsAll[note_mode_index]).COLOUR
    
        if note_menu_active or not getattr(noteprocessors, customProcessorsAll[ctr]).INIT_COMPLETE:
            light_mode = lightingconsts.MODE_PULSE
        else:
            light_mode = lightingconsts.MODE_ON
    
    lights.setPadColour(8, 1, colour, state=light_mode)
    
    # Redraw menus for current note input
    if not note_menu_active:
        getattr(noteprocessors, customProcessorsAll[note_mode_index]).redraw(lights)
    
    if note_menu_active:
        redrawTo = min(len(customProcessors) - 16*noteModeMenu.getMode(), 16)
        
        for ctr in range(16*noteModeMenu.getMode(), 16*noteModeMenu.getMode() + redrawTo):
            if ctr >= internal.window.getAnimationTick():
                break
            x = ctr % 8
            y = ctr // 8
            
            if getattr(noteprocessors, customProcessors[ctr]).NAME == internal.noteMode.getState():
                light_mode = lightingconsts.MODE_PULSE
            else:
                light_mode = lightingconsts.MODE_ON
            
            lights.setPadColour(x, y, getattr(noteprocessors, customProcessors[ctr]).DEFAULT_COLOUR, state=light_mode)
            
            
        lights.solidifyAll()

def processNoteModeMenu(command):
    
    global note_menu_active
    
    if command.type is eventconsts.TYPE_PAD and command.is_lift:
        
        # Note menu button
        if command.getPadCoord() == (8, 1):
            
            if note_menu_active:
                if command.is_double_click:
                    switchNoteModeMenu(False)
                    command.handle("Close note mode menu")
                else:
                    if noteModeMenu.num_modes == 1:
                        switchNoteModeMenu(False)
                        command.handle("Close note mode menu")
                    else:
                        noteModeMenu.nextMode()
                        command.handle("Next note mode menu")
            
            elif not note_menu_active and not internal.errors.getError():
                
                switchNoteModeMenu(True)
                command.handle("Open note mode menu")
        
        # Note menu open
        elif note_menu_active:
            note_mode_index = noteModeMenu.getMode()*16 + command.coord_X + 8*command.coord_Y
            
            if note_mode_index < len(customProcessors):
                internal.sendCompleteInternalMidiMessage(internal.consts.MESSAGE_INPUT_MODE_SELECT + (note_mode_index << 16))
                switchNoteModeMenu(False)
                setModeByIndex(note_mode_index)
                command.handle("Set note mode to " + getattr(noteprocessors, customProcessors[note_mode_index]).NAME)
            
            else:
                command.handle("Note mode catch-all", silent=True)

    if command.type is eventconsts.TYPE_BASIC_PAD and command.is_lift:
        if command.getPadCoord() == (8, 1):
            
            if note_menu_active:
                if command.is_double_click:
                    internal.extendedMode.revert(eventconsts.INCONTROL_PADS)
                    switchNoteModeMenu(False)
                    command.handle("Close note mode menu")
                else:
                    noteModeMenu.nextMode()
                    command.handle("Next note mode menu")
            
            elif not note_menu_active:
                internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
                switchNoteModeMenu(True)
                command.handle("Open note mode menu")

def setModeByIndex(index):
    current_name = internal.noteMode.getState()
    for ctr in range(len(customProcessorsAll)):
        if getattr(noteprocessors, customProcessorsAll[ctr]).NAME == current_name:
            note_mode_index = ctr
            break
    # Deactivate old note mode
    getattr(noteprocessors, customProcessorsAll[note_mode_index]).activeEnd()
    
    internal.noteMode.setState(getattr(noteprocessors, customProcessors[index]).NAME)

    # Activate new note mode
    getattr(noteprocessors, customProcessors[index]).activeStart()
