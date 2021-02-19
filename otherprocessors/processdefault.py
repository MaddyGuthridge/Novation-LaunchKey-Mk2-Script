"""
otherprocessors > processdefault.py

This script is the last to process events. It provides default functionality.
Add things here when they are common throughout the entire script but can be overridden easily.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import time

import transport
import ui

import lightingconsts
import eventprocessor
import eventconsts
import internal

def redraw(lights):

    # redraw beat indicator
    internal.beat.redraw(lights)

    # Pads white if pressed
    for x in range(len(internal.notemanager.pads.padsDown)):
            for y in range(len(internal.notemanager.pads.padsDown[x])):
                if internal.notemanager.pads.getVal(x, y):
                    lights.setPadColour(x, y, lightingconsts.colours["WHITE"], lightingconsts.MODE_PULSE, True)
    return

def process(command):

    command.actions.addProcessor("Default Processor")
    
    #---------------------------------
    # Transport functions
    #---------------------------------
    if command.type == eventconsts.TYPE_TRANSPORT:
        # Play-pause: only on lift
        if command.id == eventconsts.TRANSPORT_PLAY and command.is_lift: 
            transport.start()
            command.handle("Play/Pause Transport")

        # Stop: only on lift
        if command.id == eventconsts.TRANSPORT_STOP and command.is_lift: 
            transport.stop()
            command.handle("Stop Transport")

        # Loop: only on lift
        if command.id == eventconsts.TRANSPORT_LOOP and command.is_lift: 
            transport.setLoopMode()
            command.handle("Toggle Loop Mode")
        
        # Record: only on lift
        if command.id == eventconsts.TRANSPORT_RECORD and command.is_lift: 
            transport.record()
            command.handle("Toggle Recording")

        # Skip forward: start on press, stop on lift, faster on double press?
        if command.id == eventconsts.TRANSPORT_FORWARD:
            speed = 1
            command.actions.appendAction("Fast Forward")
            if command.is_double_click: 
                speed = 2
                command.actions.appendAction("[2x Speed]")

            if command.is_lift is False: 
                transport.continuousMove(speed, 2)
            if command.is_lift is True: 
                transport.continuousMove(speed, 0)
                command.actions.appendAction("Stopped")
            command.handle("Continuous move", True)
        
        # Skip back: start on press, stop on lift, faster on double press?
        if command.id == eventconsts.TRANSPORT_BACK:
            speed = -1
            command.actions.appendAction("Rewind")
            if command.is_double_click: 
                speed = -2
                command.actions.appendAction("[2x Speed]")

            if command.is_lift is False: 
                transport.continuousMove(speed, 2)
            if command.is_lift is True: 
                transport.continuousMove(speed, 0)
                command.actions.appendAction("Stopped")
            command.handle("Continuous move", True)
        
        # Next Track: next UI element
        if command.id == eventconsts.TRANSPORT_TRACK_NEXT and command.is_lift:
            ui.next()
            command.handle("Next UI Element")

        # Prev Track: prev UI element
        if command.id == eventconsts.TRANSPORT_TRACK_PREVIOUS and command.is_lift:
            ui.previous()
            command.handle("Previous UI Element")


