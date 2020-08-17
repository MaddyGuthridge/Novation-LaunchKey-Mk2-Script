"""
otherprocessors > processdefault.py

This script is the last to process events. It provides default functionality.
Add things here when they are common throughout the entire script but can be overridden easily.

Author: Miguel Guthridge
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
                    lights.setPadColour(x, y, lightingconsts.colours["WHITE"], 2, True)
    return

def process(command):

    command.actions.addProcessor("Default Processor")

    #---------------------------------
    # Tempo button
    #---------------------------------
    if (command.type == eventconsts.TYPE_PAD or command.type == eventconsts.TYPE_BASIC_PAD) and command.is_lift:
        if command.coord_X == 8 and command.coord_Y == 0:

            # Double press: tap tempo
            if command.is_double_click:
                internal.beat.toggleMetronome()
                internal.beat.toggleTempoTap()
                command.actions.appendAction("Toggled Tempo Tapping")

            if internal.beat.is_tapping_tempo:
                internal.beat.tapTempo()
                command.actions.appendAction("Tapped Tempo")
            else:
                # Toggle metronome back to original
                internal.beat.toggleMetronome()
                command.actions.appendAction("Toggled Metronome")
            command.handled = True
    
    
    #---------------------------------
    # Transport functions
    #---------------------------------
    if command.type == eventconsts.TYPE_TRANSPORT:
        # Play-pause: only on lift
        if command.id == eventconsts.TRANSPORT_PLAY and command.is_lift: 
            transport.start()
            command.actions.appendAction("Play/Pause Transport")
            command.handled = True

        # Stop: only on lift
        if command.id == eventconsts.TRANSPORT_STOP and command.is_lift: 
            transport.stop()
            command.actions.appendAction("Stop Transport")
            command.handled = True

        # Loop: only on lift
        if command.id == eventconsts.TRANSPORT_LOOP and command.is_lift: 
            transport.setLoopMode()
            command.actions.appendAction("Toggle Loop Mode")
            command.handled = True
        
        # Record: only on lift
        if command.id == eventconsts.TRANSPORT_RECORD and command.is_lift: 
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

            if command.is_lift is False: 
                transport.continuousMove(speed, 2)
            if command.is_lift is True: 
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

            if command.is_lift is False: 
                transport.continuousMove(speed, 2)
            if command.is_lift is True: 
                transport.continuousMove(speed, 0)
                command.actions.appendAction("Stopped")
            command.handled = True
        
        # Next Track: next UI element
        if command.id == eventconsts.TRANSPORT_TRACK_NEXT and command.is_lift:
            ui.next()
            command.actions.appendAction("Next UI Element")
            command.handled = True

        # Prev Track: prev UI element
        if command.id == eventconsts.TRANSPORT_TRACK_PREVIOUS and command.is_lift:
            ui.previous()
            command.actions.appendAction("Previous UI Element")
            command.handled = True

    #--------------------------------------------------

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")

