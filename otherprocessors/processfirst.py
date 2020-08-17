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
import internal.consts
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

    noteprocessors.redrawNoteModeMenu(lights)

    return

def redrawPopup(lights):
    if not (internal.window.active_plugin == internal.consts.WINDOW_STR_SCRIPT_OUTPUT and internal.window.plugin_focused):
        
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



def process(command):

    command.actions.addProcessor("Primary Processor")

    # Forward onto basic processor for things
    if command.type == eventconsts.TYPE_PAD:
        internal.sendInternalMidiMessage(command.status, command.note, command.value)
        command.actions.appendAction("Forward to basic script processor", silent=True)

    # Pads down (white light)
    if command.type == eventconsts.TYPE_BASIC_PAD or command.type == eventconsts.TYPE_PAD:
        if command.value: # Press down
            internal.notemanager.pads.press(command.coord_X, command.coord_Y)
        else:
            internal.notemanager.pads.lift(command.coord_X, command.coord_Y)

    


    # Right click menu
    if ui.isInPopupMenu() and command.type == eventconsts.TYPE_PAD and command.is_lift and (internal.window.getString() != internal.consts.WINDOW_STR_SCRIPT_OUTPUT):
        
        processPopup(command)

    # Note Processor Menu
    noteprocessors.processNoteModeMenu(command)

    if command.handled:
        return

    noteprocessors.process(command)

    #
    # Extended Mode signals
    #

    # All
    if command.id == eventconsts.SYSTEM_EXTENDED:
        internal.extendedMode.recieve(not command.is_lift)
        command.handle("Set Extended Mode to " + str(not command.is_lift), silent=True)

    # Knobs
    if command.id == eventconsts.INCONTROL_KNOBS:
        internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_KNOBS)
        command.handle("Set Extended Mode (Knobs) to " + str(not command.is_lift))
    
    # Faders
    if command.id == eventconsts.INCONTROL_FADERS:
        internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_FADERS)
        command.handle("Set Extended Mode (Faders) to " + str(not command.is_lift), silent=True)
    
    # Pads
    if command.id == eventconsts.INCONTROL_PADS:
        internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_PADS)
        if command.is_lift:
            # Close select note mode menu
            noteprocessors.processnotes.switchNoteModeMenu(False, True)
        command.handle("Set Extended Mode (Pads) to " + str(not command.is_lift), silent=True)
    
    # That random event on the knobs button
    if command.id == eventconsts.SYSTEM_MISC:
        command.handle("Handle misc event", silent=True)
       
        

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
        command.handle("Right click menu catch-all", silent=True)
