"""
otherprocessors > processfirst.py

This file processes events before anything else. 
Add things here when they need to override all other functionality (eg shift menu).

Author: Miguel Guthridge
"""

import ui
import general
import transport

import config
import internalconstants
import processorhelpers
import eventconsts
import internal
import lighting
import lightingconsts
import noteprocessors

def redraw(lights):
    # In Popup Menu
    if internal.window.getInPopup():
        redrawPopup(lights)
        
    # Shift key triggers window switcher
    if internal.shift.getDown():
        redrawShift(lights)

    noteprocessors.redrawNoteModeMenu(lights)

    return

def redrawPopup(lights):
    if not (internal.window.active_plugin == internalconstants.WINDOW_STR_SCRIPT_OUTPUT and internal.window.plugin_focused):
        
        if internal.window.getAnimationTick() > 0:
            lights.setPadColour(1, 1, lightingconsts.UI_NAV_VERTICAL)         # Down

        if internal.window.getAnimationTick() > 1:
            lights.setPadColour(1, 0, lightingconsts.UI_NAV_VERTICAL)         # Up
            lights.setPadColour(0, 1, lightingconsts.UI_NAV_HORIZONTAL)       # Left
            lights.setPadColour(2, 1, lightingconsts.UI_NAV_HORIZONTAL)       # Right

        if internal.window.getAnimationTick() > 2:
            lights.setPadColour(3, 1, lightingconsts.UI_REJECT)               # No

        if internal.window.getAnimationTick() > 3:
            lights.setPadColour(4, 1, lightingconsts.UI_ACCEPT)               # Yes
        
        lights.solidifyAll()

def redrawShift(lights):

    UNDO_LAST = 1
    UNDO_MIDDLE = 0
    UNDO_FIRST = -1

    undo_position = general.getUndoHistoryLast()
    undo_length = general.getUndoHistoryCount()
    
    if undo_position == 0:
        undo_type = UNDO_LAST
    elif undo_position + 1 == undo_length:
        undo_type = UNDO_FIRST
    else:
        undo_type = UNDO_MIDDLE

    if internal.window.getAnimationTick() > 0:
        # Playlist
        if internal.window.getString() == internalconstants.WINDOW_STR_PLAYLIST:
            lights.setPadColour(0, 1, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(0, 1, lightingconsts.WINDOW_PLAYLIST)

    if internal.window.getAnimationTick() > 1:
        # Channel Rack
        if internal.window.getString() == internalconstants.WINDOW_STR_CHANNEL_RACK:
            lights.setPadColour(1, 1, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(1, 1, lightingconsts.WINDOW_CHANNEL_RACK)

        # Undo
        if undo_type  == UNDO_FIRST:
            lights.setPadColour(0, 0, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(0, 0, lightingconsts.UI_UNDO)

    if internal.window.getAnimationTick() > 2:
        # Piano roll
        if internal.window.getString() == internalconstants.WINDOW_STR_PIANO_ROLL:
            lights.setPadColour(2, 1, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(2, 1, lightingconsts.WINDOW_PIANO_ROLL)

        # Redo
        if undo_type == UNDO_LAST:
            lights.setPadColour(1, 0, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(1, 0, lightingconsts.UI_REDO)

    if internal.window.getAnimationTick() > 3:
        # Mixer
        if internal.window.getString() == internalconstants.WINDOW_STR_MIXER:
            lights.setPadColour(3, 1, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(3, 1, lightingconsts.WINDOW_MIXER)

        # Next plugin
        lights.setPadColour(7, 0, lightingconsts.UI_NAV_HORIZONTAL)

        # Save
        lights.setPadColour(3, 0, lightingconsts.UI_SAVE)
        
    if internal.window.getAnimationTick() > 4:
        # Browser
        if internal.window.getString() == internalconstants.WINDOW_STR_BROWSER:
            lights.setPadColour(4, 1, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(4, 1, lightingconsts.WINDOW_BROWSER)

        # Prev plugin
        lights.setPadColour(6, 0, lightingconsts.UI_NAV_HORIZONTAL)

        # Plugin picker
        lights.setPadColour(7, 1, lightingconsts.WINDOW_PLUGIN_PICKER)
            

    lights.solidifyAll()


def process(command):

    command.actions.addProcessor("Primary Processor")

    # Forward onto main processor for lighting
    if command.type == eventconsts.TYPE_PAD:
        internal.sendInternalMidiMessage(command.status, command.note, command.value)
        command.actions.appendAction("Forward to basic script processor")

    # Pads down (white light)
    if command.type == eventconsts.TYPE_BASIC_PAD or command.type == eventconsts.TYPE_PAD:
        if command.value: # Press down
            internal.notemanager.pads.press(command.coord_X, command.coord_Y)
        else:
            internal.notemanager.pads.lift(command.coord_X, command.coord_Y)

    # Shift button (in control for pads (window switcher))
    if command.id == config.SHIFT_BUTTON:
        if command.is_lift:
            internal.extendedMode.revert(eventconsts.INCONTROL_PADS)
        else:
            internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)

    # Shift down - Window switcher
    if command.shifted and command.type == eventconsts.TYPE_PAD and command.is_lift:
        
        processShift(command)

    # Right click menu
    if ui.isInPopupMenu() and command.type == eventconsts.TYPE_PAD and command.is_lift and (internal.window.getString() != internalconstants.WINDOW_STR_SCRIPT_OUTPUT):
        
        processPopup(command)

    # Note Processor Menu
    noteprocessors.processNoteModeMenu(command)

    noteprocessors.process(command)

    #
    # Extended Mode signals
    #

    # All
    if command.id == eventconsts.SYSTEM_EXTENDED:
        internal.extendedMode.recieve(not command.is_lift)
        command.handle("Set Extended Mode to " + str(not command.is_lift))

    # Knobs
    if command.id == eventconsts.INCONTROL_KNOBS:
        internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_KNOBS)
        command.handle("Set Extended Mode (Knobs) to " + str(not command.is_lift))
    
    # Faders
    if command.id == eventconsts.INCONTROL_FADERS:
        internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_FADERS)
        command.handle("Set Extended Mode (Faders) to " + str(not command.is_lift))
    
    # Pads
    if command.id == eventconsts.INCONTROL_PADS:
        internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_PADS)
        if command.is_lift:
            noteprocessors.processnotes.switchNoteModeMenu(False)
        command.handle("Set Extended Mode (Pads) to " + str(not command.is_lift))
    
    # That random event on the knobs button
    if command.id == eventconsts.SYSTEM_MISC:
        command.handle("Handle misc event")

def processShift(command):
    if command.note == eventconsts.Pads[0][1]: 
        ui.showWindow(internalconstants.WINDOW_PLAYLIST)
        command.handle("Switched window to Playlist")
        
    elif command.note == eventconsts.Pads[1][1]: 
        ui.showWindow(internalconstants.WINDOW_CHANNEL_RACK)
        command.handle("Switched window to Channel rack")
        
    elif command.note == eventconsts.Pads[2][1]: 
        ui.showWindow(internalconstants.WINDOW_PIANO_ROLL)
        command.handle("Switched window to Piano roll")
        
    elif command.note == eventconsts.Pads[3][1]: 
        ui.showWindow(internalconstants.WINDOW_MIXER)
        command.handle("Switched window to Mixer")
        
    elif command.note == eventconsts.Pads[4][1]: 
        ui.showWindow(internalconstants.WINDOW_BROWSER)
        command.handle("Switched window to Browser")
        
    elif command.note == eventconsts.Pads[6][0]: 
        ui.selectWindow(True)
        command.handle("Previous window")
    
    elif command.note == eventconsts.Pads[7][0]: 
        ui.selectWindow(False)
        command.handle("Next window")
        
    elif command.note == eventconsts.Pads[0][0]: 
        general.undoUp()
        command.handle("Undo")
        
    elif command.note == eventconsts.Pads[1][0]: 
        general.undoDown()
        command.handle("Redo")

    elif command.note == eventconsts.Pads[7][1]:
        transport.globalTransport(eventconsts.midi.FPT_F8, 1)
        command.handle("Launch Plugin Picker")

    elif command.note == eventconsts.Pads[3][0]:
        transport.globalTransport(eventconsts.midi.FPT_Save, 1)
        command.handle("Save project")

    else:
        command.handle("Shift menu catch-all")

def processPopup(command):
    # Always handle all presses
    if command.note == eventconsts.Pads[1][0]:
        ui.up()
        command.handle("UI Up")

    elif command.note == eventconsts.Pads[1][1]:
        ui.down()
        command.handle("UI Down")

    elif command.note == eventconsts.Pads[0][1]:
        ui.left()
        command.handle("UI Left")
    
    elif command.note == eventconsts.Pads[2][1]:
        ui.right()
        command.handle("UI Right")

    elif command.note == eventconsts.Pads[3][1]:
        ui.escape()
        command.handle("UI Escape")

    elif command.note == eventconsts.Pads[4][1]:
        ui.enter()
        command.handle("UI Enter")

    else:
        command.handle("Right click menu catch-all")
