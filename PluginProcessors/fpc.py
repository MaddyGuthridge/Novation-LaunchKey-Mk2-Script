"""
fpc.py
This script is a custom processor module that can process events when the FPC plugin is active

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
import eventprocessor
import internal
import eventconsts
import config
import lighting

COLOUR_MAP = [
    [lighting.COLOUR_BLUE, lighting.COLOUR_BLUE],
    [lighting.COLOUR_BLUE, lighting.COLOUR_RED],
    [lighting.COLOUR_GREEN, lighting.COLOUR_GREEN],
    [lighting.COLOUR_GREEN, lighting.COLOUR_ORANGE],
    [lighting.COLOUR_YELLOW, lighting.COLOUR_ORANGE],
    [lighting.COLOUR_YELLOW, lighting.COLOUR_ORANGE],
    [lighting.COLOUR_LIGHT_BLUE, lighting.COLOUR_ORANGE],
    [lighting.COLOUR_LIGHT_BLUE, lighting.COLOUR_ORANGE]
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

    # Basic Mode Processing:
    if internal.PORT == config.DEVICE_PORT_BASIC:
        # Change pedals to kick:
        if command.id == eventconsts.PEDAL:
            if command.value == 0: # Pedal up
                command.edit(eventprocessor.rawEvent(0x89, eventconsts.BasicPads[1][1], command.value))
            else: # Pedal up
                command.edit(eventprocessor.rawEvent(0x99, eventconsts.BasicPads[1][1], command.value))

        # Dispatch event to extended mode
        internal.sendMidiMessage(command.status, command.note, command.value)

        # Map drums to match FPC default layout
        change_pads(command)


    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
    return



# Change pads to default note layout for FPC
def change_pads(command):
    if REMAP_DRUMS:
        if command.note is eventconsts.BasicPads[0][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][0], command.value))
            return

        if command.note is eventconsts.BasicPads[1][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][1], command.value))
            return

        if command.note is eventconsts.BasicPads[2][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][2], command.value))
            return

        if command.note is eventconsts.BasicPads[3][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[3][3], command.value))
            return

        if command.note is eventconsts.BasicPads[4][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][0], command.value))
            return

        if command.note is eventconsts.BasicPads[5][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][1], command.value))
            return

        if command.note is eventconsts.BasicPads[6][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][2], command.value))
            return

        if command.note is eventconsts.BasicPads[7][1]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[1][3], command.value))
            return

        if command.note is eventconsts.BasicPads[0][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][0], command.value))
            return

        if command.note is eventconsts.BasicPads[1][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][1], command.value))
            return

        if command.note is eventconsts.BasicPads[2][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][2], command.value))
            return
            
        if command.note is eventconsts.BasicPads[3][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[2][3], command.value))
            return

        if command.note is eventconsts.BasicPads[4][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][0], command.value))
            return

        if command.note is eventconsts.BasicPads[5][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][1], command.value))
            return

        if command.note is eventconsts.BasicPads[6][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][2], command.value))
            return

        if command.note is eventconsts.BasicPads[7][0]:
            command.edit(eventprocessor.rawEvent(command.status, FPC_DRUM_CONSTS[0][3], command.value))
            return

