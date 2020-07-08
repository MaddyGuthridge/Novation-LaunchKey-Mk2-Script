"""
processfirst.py
This file processes events before anything else.

"""

import transport
import ui
import general

import config
import internalconstants
import eventprocessor
import eventconsts
import internal
import lighting

in_popup = False

def redraw(lights):
    global in_popup
    # In Popup Menu
    if ui.isInPopupMenu() and (internal.window.active_plugin != internalconstants.WINDOW_SCRIPT_OUTPUT):
        if not in_popup:
            internal.window.reset_animation_tick()
            in_popup = True
        
        if internal.window.get_animation_tick() > 0:
            lights.setPadColour(1, 1, lighting.UI_NAV_VERTICAL)         # Down

        if internal.window.get_animation_tick() > 1:
            lights.setPadColour(1, 0, lighting.UI_NAV_VERTICAL)         # Up
            lights.setPadColour(0, 1, lighting.UI_NAV_HORIZONTAL)       # Left
            lights.setPadColour(2, 1, lighting.UI_NAV_HORIZONTAL)       # Right

        if internal.window.get_animation_tick() > 2:
            lights.setPadColour(3, 1, lighting.UI_REJECT)               # No

        if internal.window.get_animation_tick() > 3:
            lights.setPadColour(4, 1, lighting.UI_ACCEPT)               # Yes
        
        lights.solidifyAll()

    else:
        if in_popup:
            internal.window.reset_animation_tick()
            in_popup = False

    # Shift key triggers window switcher
    if internal.shift.getDown():
        
        if internal.window.get_animation_tick() > 0:
            lights.setPadColour(0, 1, lighting.WINDOW_PLAYLIST)         # Playlist
        if internal.window.get_animation_tick() > 1:
            lights.setPadColour(1, 1, lighting.WINDOW_CHANNEL_RACK)     # Channel rack
            lights.setPadColour(0, 0, lighting.UI_UNDO)                 # Undo
        if internal.window.get_animation_tick() > 2:
            lights.setPadColour(2, 1, lighting.WINDOW_PIANO_ROLL)       # Piano roll
            lights.setPadColour(1, 0, lighting.UI_REDO)                 # Redo
        if internal.window.get_animation_tick() > 3:
            lights.setPadColour(3, 1, lighting.WINDOW_MIXER)            # Mixer
            lights.setPadColour(7, 0, lighting.UI_NAV_HORIZONTAL)       # Next plugin
        if internal.window.get_animation_tick() > 4:
            lights.setPadColour(4, 1, lighting.WINDOW_BROWSER)          # Browser
            lights.setPadColour(6, 0, lighting.UI_NAV_HORIZONTAL)       # Prev plugin
            

        lights.solidifyAll()


    return

def process(command):

    command.actions.addProcessor("Primary Processor")

    # If in extended mode
    if internal.PORT == config.DEVICE_PORT_EXTENDED:

        # Pads down (white light)
        if command.type == eventconsts.TYPE_BASIC_PAD or command.type == eventconsts.TYPE_PAD:
            if command.value: # Press down
                internal.pads.press(command.padX, command.padY)
            else:
                internal.pads.lift(command.padX, command.padY)

        # Shift button (in control for pads (window switcher))
        if command.id == config.SHIFT_BUTTON:
            if command.is_lift:
                internal.extendedMode.revert(eventconsts.INCONTROL_PADS)
            else:
                internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)

        # Shift down - Window switcher
        if command.shifted and command.type == eventconsts.TYPE_PAD and command.is_lift:
            
            if command.note == eventconsts.Pads[0][1]: 
                ui.showWindow(internalconstants.WINDOW_PLAYLIST)
                command.actions.appendAction("Switched window to Playlist")
                command.handled = True

            if command.note == eventconsts.Pads[1][1]: 
                ui.showWindow(internalconstants.WINDOW_CHANNEL_RACK)
                command.actions.appendAction("Switched window to Channel rack")
                command.handled = True

            if command.note == eventconsts.Pads[2][1]: 
                ui.showWindow(internalconstants.WINDOW_PIANO_ROLL)
                command.actions.appendAction("Switched window to Piano roll")
                command.handled = True
            
            if command.note == eventconsts.Pads[3][1]: 
                ui.showWindow(internalconstants.WINDOW_MIXER)
                command.actions.appendAction("Switched window to Mixer")
                command.handled = True
            
            if command.note == eventconsts.Pads[4][1]: 
                ui.showWindow(internalconstants.WINDOW_BROWSER)
                command.actions.appendAction("Switched window to Browser")
                command.handled = True
            
            if command.note == eventconsts.Pads[6][0]: 
                ui.selectWindow(True)
                command.actions.appendAction("Previous window")
                command.handled = True
            
            if command.note == eventconsts.Pads[7][0]: 
                ui.selectWindow(False)
                command.actions.appendAction("Next window")
                command.handled = True

            if command.note == eventconsts.Pads[0][0]: 
                general.undoUp()
                command.actions.appendAction("Undo")
                command.handled = True
            
            if command.note == eventconsts.Pads[1][0]: 
                general.undoDown()
                command.actions.appendAction("Redo")
                command.handled = True

            

        # Right click menu
        if ui.isInPopupMenu() and command.type == eventconsts.TYPE_PAD and command.is_lift and (internal.window.active_plugin != internalconstants.WINDOW_SCRIPT_OUTPUT):
            
            # Always handle all presses
            command.handled = True

            if command.note == eventconsts.Pads[1][0]:
                ui.up()
                command.actions.appendAction("UI Up")

            if command.note == eventconsts.Pads[1][1]:
                ui.down()
                command.actions.appendAction("UI Down")

            if command.note == eventconsts.Pads[0][1]:
                ui.left()
                command.actions.appendAction("UI Left")
            
            if command.note == eventconsts.Pads[2][1]:
                ui.right()
                command.actions.appendAction("UI Right")

            if command.note == eventconsts.Pads[3][1]:
                ui.escape()
                command.actions.appendAction("UI Escape")

            if command.note == eventconsts.Pads[4][1]:
                ui.enter()
                command.actions.appendAction("UI Enter")

        #
        # Extended Mode signals
        #

        # All
        if command.id == eventconsts.SYSTEM_EXTENDED:
            internal.extendedMode.recieve(not command.is_lift)
            command.actions.appendAction("Set Extended Mode to " + str(not command.is_lift))
            command.handled = True

        # Knobs
        if command.id == eventconsts.INCONTROL_KNOBS:
            internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_KNOBS)
            command.actions.appendAction("Set Extended Mode (Knobs) to " + str(not command.is_lift))
            command.handled = True
        
        # Faders
        if command.id == eventconsts.INCONTROL_FADERS:
            internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_FADERS)
            command.actions.appendAction("Set Extended Mode (Faders) to " + str(not command.is_lift))
            command.handled = True
        
        # Pads
        if command.id == eventconsts.INCONTROL_PADS:
            internal.extendedMode.recieve(not command.is_lift, eventconsts.INCONTROL_PADS)
            command.actions.appendAction("Set Extended Mode (Pads) to " + str(not command.is_lift))
            command.handled = True
        
        # That random event on the knobs button
        if command.id == eventconsts.SYSTEM_MISC:
            command.handled = True
    
    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")

