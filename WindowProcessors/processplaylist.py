"""
processplaylist.py
This script processes events when the playlist is active

"""

import eventconsts
import eventprocessor

import transport
import internal


def activeStart():
    return

def activeEnd():
    return

def topWindowStart():
    return

def topWindowEnd():
    return

def redraw(lights):
    return

def process(command):
    command.actions.addProcessor("Playlist Processor")

    if command.type == eventconsts.TYPE_TRANSPORT:
        if not internal.shift.getDown() and (command.id == eventconsts.TRANSPORT_BACK or command.id == eventconsts.TRANSPORT_FORWARD):
            
            if command.is_lift:
                if command.id == eventconsts.TRANSPORT_BACK:
                    transport.markerJumpJog(-1)
                    command.handle("Transport: Jump to previous marker")
                if command.id == eventconsts.TRANSPORT_FORWARD:
                    transport.markerJumpJog(1)
                    command.handle("Transport: Jump to next marker")
            else:
                command.handle("Catch transport skips")

        else:
            internal.shift.use()


    
    return