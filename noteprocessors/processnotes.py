"""
noteprocessors > processnotes.py
This script forwards events to note processors depending on the current mode.

Author: Miguel Guthridge [hdsq@outlook.com.au]

"""

#
# Add custom event processors to this list
#
imports = ["default", "error", "scale", "chord", "omni", "randomiser", "unassigned"]
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
success = 0
for x in range(len(imports)):
    try:
        __import__("noteprocessors." + imports[x])
        customProcessorsAll.append(imports[x])
        if not getattr(noteprocessors, imports[x]).SILENT:
            customProcessors.append(imports[x])
        success += 1
    except ImportError as e:
        print ("\tError importing: ", imports[x])
        print("\t" + e)
        if config.DEBUG_HARD_CRASHING:
            raise e
print("Successfully imported " + str(success) + "/" + str(len(imports)) + " modules")

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
    """Processes events to forward them onto note processors

    Args:
        command (ParsedEvent): command to process
    """
    # If in note mode menu, use that processor
    if note_menu_active:
        processNoteModeMenu(command)
    
    # Otherwise use note processors
    else:
        for x in customProcessorsAll:
            object_to_call = getattr(noteprocessors, x)
            if object_to_call.NAME == internal.noteMode.getState():
                
                if object_to_call.FORWARD_NOTES and command.type == eventconsts.TYPE_NOTE and not internal.getPortExtended():
                    internal.sendCompleteInternalMidiMessage(command.getDataMIDI())
                
                object_to_call.process(command)
            
                if command.ignored: return
    
    if command.ignored: return
    
    # Then check the note mode menu button
    processNoteModeMenuOpener(command)

def processNoteModeMenu(command):
    command.addProcessor("Note Menu Processor")
    if command.type is eventconsts.TYPE_PAD and command.is_lift:
        note_mode_index = noteModeMenu.getMode()*16 + command.coord_X + 8*command.coord_Y
                
        if note_mode_index < len(customProcessors):
            internal.sendCompleteInternalMidiMessage(internal.consts.MESSAGE_INPUT_MODE_SELECT + (note_mode_index << 16))
            switchNoteModeMenu(False)
            setModeByIndex(note_mode_index)
            command.handle("Set note mode to " + getattr(noteprocessors, customProcessors[note_mode_index]).NAME)
        
        elif command.coord_X < 8:
            command.handle("Note mode catch-all", silent=True)

def processNoteModeMenuOpener(command):
    command.addProcessor("Note Menu Opener Processor")
    if (
        command.type is eventconsts.TYPE_PAD
        and command.is_lift 
        and (command.coord_X, command.coord_Y) == (8, 1)
    ):
        
        if not note_menu_active:
            switchNoteModeMenu(True)
            command.handle("Open note mode menu", True)
        else:
            # If on last page
            if noteModeMenu.num_modes - 1 == noteModeMenu.mode:
                # Exit menu
                switchNoteModeMenu(False)
                command.handle("Exit note mode menu", True)
            
            else:
                noteModeMenu.nextMode()
                command.handle("Next page of note mode menu", True)
    elif ( # Basic drum pad: forward event
        command.type is eventconsts.TYPE_BASIC_PAD
        and command.is_lift 
        and (command.coord_X, command.coord_Y) == (8, 1)
        and not note_menu_active
    ):
        switchNoteModeMenu(True)
        if not internal.getPortExtended():
            internal.sendCompleteInternalMidiMessage(command.getDataMIDI(), "Forward drum for opening note mode menu")
        else:
            internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
        command.handle("Open note mode menu", True)

def beatChange(beat):
    for x in customProcessorsAll:
        object_to_call = getattr(noteprocessors, x)
        if object_to_call.NAME == internal.noteMode.getState():
            object_to_call.beatChange(beat)
   
def redraw(lights):
    # Find current note processor
    current_name = internal.noteMode.getState()
    for ctr in range(len(customProcessorsAll)):
        if getattr(noteprocessors, customProcessorsAll[ctr]).NAME == current_name:
            note_mode_index = ctr
            break
    
    if note_menu_active:
        colour = lightingconsts.colours["DARK GREY"]
        light_mode = lightingconsts.MODE_PULSE
    else:
        colour = getattr(noteprocessors, customProcessorsAll[note_mode_index]).COLOUR
    
        if not getattr(noteprocessors, customProcessorsAll[ctr]).INIT_COMPLETE:
            light_mode = lightingconsts.MODE_PULSE
        else:
            light_mode = lightingconsts.MODE_ON
    
    lights.setPadColour(8, 1, colour, state=light_mode)
    
    # Redraw menus for current note input
    if not note_menu_active:
        getattr(noteprocessors, customProcessorsAll[note_mode_index]).redraw(lights)
    
    else:
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

# Old code
"""


def process(command):
    
    # If in note mode menu, use that processor
    if note_menu_active:
        processNoteModeMenu(command)
        return
    
    # Otherwise use note processors
    for x in customProcessorsAll:
        object_to_call = getattr(noteprocessors, x)
        if object_to_call.NAME == internal.noteMode.getState():
            
            if object_to_call.FORWARD_NOTES and command.type == eventconsts.TYPE_NOTE and not internal.getPortExtended():
                internal.sendCompleteInternalMidiMessage(command.getDataMIDI())
            
            object_to_call.process(command)
        
            if command.ignored: return
    
    # Then check the note mode menu button
    processNoteModeMenuOpener(command)
    

def processNoteModeMenuOpener(command):
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

def processNoteModeMenu(command):
    
    global note_menu_active
    
    if command.type is eventconsts.TYPE_PAD and command.is_lift:
        
        
        
        # Note menu open
        if note_menu_active:
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


"""

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
    
    