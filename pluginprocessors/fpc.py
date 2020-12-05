"""
pluginprocessors > fpc.py

This script is a custom processor module that can process events when the FPC plugin is active.
It maps the pedal to the kick, and rearranges drums to match the FPC default layout, 
as well as drawing pad colours to match the colours of the default note layout.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

REMAP_DRUMS = True

PLUGINS = ["FPC"]

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
        light_map = COLOUR_MAP.copy()
        for x in range(8):
            light_map[x] = light_map[x].copy()
        tick = internal.window.getAnimationTick()
        for x in range(8):
            for y in range(2):
                if x >=4 and y == 0:
                    if tick + 4 < x:
                        light_map[x][y] = lightingconsts.colours["OFF"]
                elif x < 4 and y == 0:
                    if tick - 1 < x:
                        light_map[x][y] = lightingconsts.colours["OFF"]
                elif x >= 4 and y == 1:
                    if tick + 3 < x:
                        light_map[x][y] = lightingconsts.colours["OFF"]
                elif x < 4 and y == 1:
                    if tick - 2 < x:
                        light_map[x][y] = lightingconsts.colours["OFF"]
        lights.setFromMatrix(light_map)


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
        if command.is_lift:
            status = 0x89
        else:
            status = 0x99
        command.edit(processorhelpers.RawEvent(status, eventconsts.BasicPads[1][1], command.value), "Remap pedal")

    if command.type is eventconsts.TYPE_BASIC_PAD and command.coord_X < 8:
        # Dispatch event to extended mode
        internal.sendInternalMidiMessage(command.status, command.note, command.value)

        # Map drums to match FPC default layout
        changePads(command)

        if config.DRUM_PADS_FULL_VELOCITY and command.value != 0:
            command.edit(processorhelpers.RawEvent(command.status, command.note, 127), "Full velocity")
        
        command.ignore("Remap for FPC", True)
    
    return

def beatChange(beat):
    pass

# Change pads to default note layout for FPC
def changePads(command):
    if REMAP_DRUMS:
        if command.note is eventconsts.BasicPads[0][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][0], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[1][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][1], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[2][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][2], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[3][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[3][3], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[4][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][0], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[5][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][1], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[6][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][2], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[7][1]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[1][3], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[0][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][0], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[1][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][1], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[2][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][2], command.value), "Remap drum")
            return
            
        if command.note is eventconsts.BasicPads[3][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[2][3], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[4][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][0], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[5][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][1], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[6][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][2], command.value), "Remap drum")
            return

        if command.note is eventconsts.BasicPads[7][0]:
            command.edit(processorhelpers.RawEvent(command.status, FPC_DRUM_CONSTS[0][3], command.value), "Remap drum")
            return

