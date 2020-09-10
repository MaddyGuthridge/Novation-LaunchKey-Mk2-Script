"""
windowprocessors > processplaylist.py

This script processes events when the playlist is active.
It allows you to jump between markers if the exist using the skip button.
There is planned support for performance mode in the not-too-distant future.

Author: Miguel Guthridge
"""

import eventconsts
import processorhelpers

import transport
import internal
import arrangement


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
    
    # Process marker jumps
    if command.type == eventconsts.TYPE_TRANSPORT:
        if (command.id == eventconsts.TRANSPORT_BACK or command.id == eventconsts.TRANSPORT_FORWARD):
            if not internal.shifts["MAIN"].use():
                if command.is_lift:
                    # Check that markers exist
                    if arrangement.getMarkerName(0) is not "":
                        if command.id == eventconsts.TRANSPORT_BACK:
                            transport.markerJumpJog(-1)
                            command.handle("Transport: Jump to previous marker")
                        if command.id == eventconsts.TRANSPORT_FORWARD:
                            transport.markerJumpJog(1)
                            command.handle("Transport: Jump to next marker")
                else:
                    command.handle("Catch transport skips", silent=True)
            


    
    return