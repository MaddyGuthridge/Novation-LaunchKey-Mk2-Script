"""
eventprocessor.py

This file processes events and lighting redraws.

Author: Miguel Guthridge
"""

import time

import device
import ui
import utils

import eventconsts
import internal
import internalconstants
import config
import lighting

import otherprocessors.processdefault as processdefault
import otherprocessors.processfirst as processfirst
import otherprocessors.processfirst_basic as processfirst_basic

import windowprocessors
import pluginprocessors
import noteprocessors
import controllerprocessors

"""
num_sys_safe = 0
num_sys = 0
num_ct = 0
"""


# Recieve event and forward onto relative processors
def processExtended(command):

    """
    global num_sys_safe
    global num_sys
    global num_ct
    
    num_sys_safe += command.pme_system_safe
    num_sys += command.pme_system
    num_ct += 1
    
    print("Sys rate:      ", num_sys/num_ct)
    print("Sys safe rate: ", num_sys_safe/num_ct)
    """

    try:

        # Process internal commands
        if command.recieved_internal:
            processReceived(command)
            return

        # Process error events
        if internal.errors.getError():
            internal.errors.eventProcessError(command)
            return

        # Reset idle timer
        if not ((command.type is eventconsts.TYPE_BASIC_PAD or command.type is eventconsts.TYPE_PAD or command.type is eventconsts.TYPE_TRANSPORT) and not command.is_lift):
            if lighting.idle_show_active():
                command.handle("End Idle Light Show")
            internal.window.resetIdleTick()

        # Process key mappings
        controllerprocessors.process(command)
        
        # Call primary processor
        processfirst.process(command)

        if command.handled: return

        # Only call plugin and window processors if it is safe to do so | Disabled because of errors
        if command.pme_system_safe or True:

            # Shouldn't be called in extended mode
            """ # Attempt to process event using custom processors for plugins
            processplugins.process(command)

            if command.handled: return"""

            # Process content from windows
            windowprocessors.process(command)

        # If command hasn't been handled by any above uses, use the default controls
        if command.handled is False:
            processdefault.process(command)

    except Exception as e:
        internal.errors.triggerError(e)

def processBasic(command):

    # Send event to reset other controller
    internal.sendCompleteInternalMidiMessage(internalconstants.MESSAGE_RESET_INTERNAL_CONTROLLER)

    try:

        if command.recieved_internal:
            processReceived(command)
            return

        # For note events, use note processors
        if command.type == eventconsts.TYPE_NOTE:
            noteprocessors.process(command)
            return

        # Now process other events for errors.
        if internal.errors.getError():
            internal.errors.eventProcessError(command)
            return
        
        # Call primary processor
        processfirst_basic.process(command)

        if command.handled: return

        # Only call plugin and window processors if it is safe to do so | Currently disabled due to errors
        if command.pme_system_safe or True:

            # Attempt to process event using custom processors for plugins
            pluginprocessors.process(command)

        if command.handled: return

    except Exception as e:
        internal.errors.triggerError(e)

# Processes events received internally
def processReceived(command):
    command.actions.addProcessor("Internal event processor")

    data = command.getDataMIDI()

    if data == internalconstants.MESSAGE_RESET_INTERNAL_CONTROLLER:
        internal.window.resetIdleTick()
        command.handle("Reset idle tick", True)

    elif data == internalconstants.MESSAGE_ERROR_CRASH:
        internal.errors.triggerErrorFromOtherScript()
        command.handle("Trigger error state")
        
    elif data == internalconstants.MESSAGE_SHIFT_DOWN:
        internal.shift.setDown(True)
        command.handle("Press shift")
        
    elif data == internalconstants.MESSAGE_SHIFT_UP:
        internal.shift.setDown(False)
        command.handle("Release shift")
        
    elif data == internalconstants.MESSAGE_SHIFT_USE:
        internal.shift.use()
        command.handle("Use shift")

# Called after a window is activated
def activeStart():
    # Only in extended mode:
    if internal.state.PORT == config.DEVICE_PORT_EXTENDED:
        if internal.window.plugin_focused:
            pluginprocessors.activeStart()
        else:
            windowprocessors.activeStart()

# Called just before active window is deactivated
def activeEnd():
    # Only in extended mode:
    if internal.state.PORT == config.DEVICE_PORT_EXTENDED:
        if internal.window.plugin_focused:
            pluginprocessors.activeEnd()
        else:
            windowprocessors.activeEnd()

def redraw():
        
    lights = lighting.LightMap()

    if internal.errors.getError():
        internal.errors.redrawError(lights)
        lighting.state.setFromMap(lights)
        return

    # Error handling: set controller into an error state
    try:

        # Draws idle thing if idle
        lighting.idle_lightshow(lights)

        # Get UI from primary processor
        processfirst.redraw(lights)

        # Get UI drawn from plugins
        pluginprocessors.redraw(lights)

        # Get UI drawn from windows
        windowprocessors.redraw(lights)

        # Get UI drawn from default processor
        processdefault.redraw(lights)

    except Exception as e:
        internal.errors.triggerError(e)


    # Call pads refresh function
    lighting.state.setFromMap(lights)
