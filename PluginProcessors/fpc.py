"""
pluginprocessors > fpc.py

This script is a custom processor module that can process events when the FPC plugin is active.
It maps the pedal to the kick, and rearranges drums to match the FPC default layout, 
as well as drawing pad colours to match the colours of the default note layout.

Author: Miguel Guthridge
"""

REMAP_DRUMS = True

plugins = ["FPC"]

# Matrix of FPC Drums [y][x] (I should probs fix this some time for the sake of consistency But I can't be bothered)
FPC_DRUM_CONSTS = [
    [49, 55, 51, 53],
    [48, 47, 45, 43],
    [40, 38, 46, 44],
    [37, 36, 42, 54]
]



import eventconsts
import internal
import eventconsts
import config
import lightingconsts
import processorhelpers

COLOUR_MAP = [
    [lightingconsts.colours["BLUE"], lightingconsts.colours["BLUE"]],
    [lightingconsts.colours["BLUE"], lightingconsts.colours["RED"]],
    [lightingconsts.colours["GREEN"], lightingconsts.colours["GREEN"]],
    [lightingconsts.colours["GREEN"], lightingconsts.colours["ORANGE"]],
    [lightingconsts.colours["YELLOW"], lightingconsts.colours["ORANGE"]],
    [lightingconsts.colours["YELLOW"], lightingconsts.colours["ORANGE"]],
    [lightingconsts.colours["LIGHT BLUE"], lightingconsts.colours["ORANGE"]],
    [lightingconsts.colours["LIGHT BLUE"], lightingconsts.colours["ORANGE"]]
]





def redraw(lights):
    if not internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        lights.setFromMatrix(COLOUR_MAP)


def topPluginStart():
    internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS)
    return

def topPluginEnd():
    internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
    return

def activeStart():
    return

def activeEnd():
    return

def process(command):
    command.actions.addProcessor("FPC Processor")

   
    # Change pedals to kick:
    if command.id == eventconsts.PEDAL:
        if command.value == 0: # Pedal up
            command.edit(processorhelpers.RawEvent(0x89, eventconsts.BasicPads[1][1], command.value))
        else: # Pedal up
            command.edit(processorhelpers.RawEvent(0x99, eventconsts.BasicPads[1][1], command.value))

    if command.type is eventconsts.TYPE_BASIC_PAD:
        # Dispatch event to extended mode
        internal.sendInternalMidiMessage(command.status, command.note, command.value)

        # Map drums to match FPC default layout
        change_pads(command)


    
    return



# Change pads to default note layout for FPC
def change_pads(command):
    if REMAP_DRUMS:
        if command.note is eventconsts.BasicPads[0][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][0], command.value))
            return

        if command.note is eventconsts.BasicPads[1][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][1], command.value))
            return

        if command.note is eventconsts.BasicPads[2][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][2], command.value))
            return

        if command.note is eventconsts.BasicPads[3][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][3], command.value))
            return

        if command.note is eventconsts.BasicPads[4][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][0], command.value))
            return

        if command.note is eventconsts.BasicPads[5][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][1], command.value))
            return

        if command.note is eventconsts.BasicPads[6][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][2], command.value))
            return

        if command.note is eventconsts.BasicPads[7][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][3], command.value))
            return

        if command.note is eventconsts.BasicPads[0][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][0], command.value))
            return

        if command.note is eventconsts.BasicPads[1][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][1], command.value))
            return

        if command.note is eventconsts.BasicPads[2][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][2], command.value))
            return
            
        if command.note is eventconsts.BasicPads[3][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][3], command.value))
            return

        if command.note is eventconsts.BasicPads[4][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][0], command.value))
            return

        if command.note is eventconsts.BasicPads[5][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][1], command.value))
            return

        if command.note is eventconsts.BasicPads[6][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][2], command.value))
            return

        if command.note is eventconsts.BasicPads[7][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][3], command.value))
            return

