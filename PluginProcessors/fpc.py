"""
fpc.py
This script is a custom processor module that can process events when the FPC plugin is active

"""

REMAP_DRUMS = True

# Matrix of FPC Drums [Row][Column]
FPC_DRUM_CONSTS = [
    [49, 55, 51, 53],
    [48, 47, 45, 43],
    [40, 38, 46, 44],
    [37, 36, 42, 82]
]

import eventconsts
import eventprocessor
import internal
import config

plugins = ["FPC"]

def topPluginStart():
    internal.setExtendedMode(False, eventconsts.INCONTROL_PADS)
    return

def topPluginEnd():
    internal.setExtendedMode(True, eventconsts.INCONTROL_PADS)
    return

def activeStart():
    return

def activeEnd():
    return

def drawUI(ui):
    return

def process(command):
    command.actions.addProcessor("FPC Processor")

    # Change pedals to kick:
    if command.id == eventconsts.PEDAL:
        if command.value == 0: # Pedal up
            command.edit(eventprocessor.rawEvent(0x89, eventconsts.BasicPads[1][1], command.value))
        else: # Pedal up
            command.edit(eventprocessor.rawEvent(0x99, eventconsts.BasicPads[1][1], command.value))

    # Map drums to match FPC defaults
    change_pads(command)

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
    return



# Change pads to default note layout for FPC
def change_pads(command):
    if REMAP_DRUMS:
        if command.note is eventconsts.BasicPads[1][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][0], command.value))
            return

        if command.note is eventconsts.BasicPads[1][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][1], command.value))
            return

        if command.note is eventconsts.BasicPads[1][2]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][2], command.value))
            return

        if command.note is eventconsts.BasicPads[1][3]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][3], command.value))
            return

        if command.note is eventconsts.BasicPads[1][4]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][0], command.value))
            return

        if command.note is eventconsts.BasicPads[1][5]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][1], command.value))
            return

        if command.note is eventconsts.BasicPads[1][6]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][2], command.value))
            return

        if command.note is eventconsts.BasicPads[1][7]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][3], command.value))
            return

        if command.note is eventconsts.BasicPads[0][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][0], command.value))
            return

        if command.note is eventconsts.BasicPads[0][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][1], command.value))
            return

        if command.note is eventconsts.BasicPads[0][2]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][2], command.value))
            return
            
        if command.note is eventconsts.BasicPads[0][3]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][3], command.value))
            return

        if command.note is eventconsts.BasicPads[0][4]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][0], command.value))
            return

        if command.note is eventconsts.BasicPads[0][5]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][1], command.value))
            return

        if command.note is eventconsts.BasicPads[0][6]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][2], command.value))
            return

        if command.note is eventconsts.BasicPads[0][7]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][3], command.value))
            return

