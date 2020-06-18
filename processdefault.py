"""
processdefault.py
This file contains functions to process and act on events. It provides default functionality

"""

import time

import transport
import ui

import lighting
import eventprocessor
import eventconsts
import internal

def redraw(lights):
    for x in range(len(internal.pads.padsDown)):
            for y in range(len(internal.pads.padsDown[x])):
                if internal.pads.getVal(x, y):
                    lights.setPadColour(x, y, lighting.COLOUR_WHITE, True)
    return

def process(command):

    command.actions.addProcessor("Default Processor")

    #---------------------------------
    # Transport functions
    #---------------------------------

    # Play-pause: only on lift
    if command.id == eventconsts.TRANSPORT_PLAY and command.is_Lift: 
        transport.start()
        command.actions.appendAction("Play/Pause Transport")
        command.handled = True

    # Stop: only on lift
    if command.id == eventconsts.TRANSPORT_STOP and command.is_Lift: 
        transport.stop()
        command.actions.appendAction("Stop Transport")
        command.handled = True

    # Loop: only on lift
    if command.id == eventconsts.TRANSPORT_LOOP and command.is_Lift: 
        transport.setLoopMode()
        command.actions.appendAction("Toggle Loop Mode")
        command.handled = True
    
    # Record: only on lift
    if command.id == eventconsts.TRANSPORT_RECORD and command.is_Lift: 
        transport.record()
        command.actions.appendAction("Toggle Recording")
        command.handled = True

    # Skip forward: start on press, stop on lift, faster on double press?
    if command.id == eventconsts.TRANSPORT_FORWARD:
        speed = 1
        command.actions.appendAction("Fast Forward")
        if command.is_double_click: 
            speed = 2
            command.actions.appendAction("[2x Speed]")

        if command.is_Lift is False: 
            transport.continuousMove(speed, 2)
        if command.is_Lift is True: 
            transport.continuousMove(speed, 0)
            command.actions.appendAction("Stopped")
        command.handled = True
    
    # Skip back: start on press, stop on lift, faster on double press?
    if command.id == eventconsts.TRANSPORT_BACK:
        speed = -1
        command.actions.appendAction("Rewind")
        if command.is_double_click: 
            speed = -2
            command.actions.appendAction("[2x Speed]")

        if command.is_Lift is False: 
            transport.continuousMove(speed, 2)
        if command.is_Lift is True: 
            transport.continuousMove(speed, 0)
            command.actions.appendAction("Stopped")
        command.handled = True
    
    # Next Track: next UI element
    if command.id == eventconsts.TRANSPORT_TRACK_NEXT and command.is_Lift:
        ui.next()
        command.actions.appendAction("Next UI Element")
        command.handled = True

    # Prev Track: prev UI element
    if command.id == eventconsts.TRANSPORT_TRACK_PREVIOUS and command.is_Lift:
        ui.previous()
        command.actions.appendAction("Previous UI Element")
        command.handled = True

    #--------------------------------------------------

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")

