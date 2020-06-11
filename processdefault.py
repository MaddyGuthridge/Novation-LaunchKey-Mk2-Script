"""
processdefault.py
This file contains functions to process and act on events. It provides default functionality

"""

import transport
import ui

import eventprocessor
import eventconsts

def process(command):

    #---------------------------------
    # Transport functions
    #---------------------------------

    # Play-pause: only on lift
    if command.id == eventconsts.TRANSPORT_PLAY and command.is_Lift: 
        transport.start()
        command.handled = True

    # Stop: only on lift
    if command.id == eventconsts.TRANSPORT_STOP and command.is_Lift: 
        transport.stop()
        command.handled = True

    # Loop: only on lift
    if command.id == eventconsts.TRANSPORT_LOOP and command.is_Lift: 
        transport.setLoopMode()
        command.handled = True
    
    # Record: only on lift
    if command.id == eventconsts.TRANSPORT_RECORD and command.is_Lift: 
        transport.record()
        command.handled = True

    # Skip forward: start on press, stop on lift, faster on double press?
    if command.id == eventconsts.TRANSPORT_FORWARD:
        speed = 1
        if command.is_double_click: speed = 2

        if command.is_Lift is False: 
            transport.continuousMove(speed, 2)
        if command.is_Lift is True: 
            transport.continuousMove(speed, 0)
        command.handled = True
    
    # Skip back: start on press, stop on lift, faster on double press?
    if command.id == eventconsts.TRANSPORT_BACK:
        speed = -1
        if command.is_double_click: speed = -2

        if command.is_Lift is False: 
            transport.continuousMove(speed, 2)
        if command.is_Lift is True: 
            transport.continuousMove(speed, 0)
        command.handled = True
    
    # Next Track: next UI element
    if command.id == eventconsts.TRANSPORT_TRACK_NEXT and command.is_Lift:
        ui.next()
        command.handled = True

    # Prev Track: prev UI element
    if command.id == eventconsts.TRANSPORT_TRACK_PREVIOUS and command.is_Lift:
        ui.previous()
        command.handled = True

