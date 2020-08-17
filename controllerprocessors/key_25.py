"""
controllerprocessors > key_25.py

This script handles initialisation and some event handling specific to the 25-key model

Author: Miguel Guthridge
"""

import eventconsts
import internal
import internal.consts
import processorhelpers

def process(command):
    command.actions.addProcessor("25-key Processor")
    # Change fader automatically
    if command.type == eventconsts.TYPE_BASIC_FADER and command.coord_X == 8:
        if internal.extendedMode.query(eventconsts.INCONTROL_FADERS):
            command.edit(processorhelpers.RawEvent(0xBF, 0x07, command.value), "Remap fader")
        else:
            internal.sendCompleteInternalMidiMessage(command.getDataMIDI())
            command.handle("Send basic fader to basic processor")



def onInit():
    internal.debugLog("Running on 25-key model", internal.consts.DEBUG.DEVICE_TYPE)
    # Force into extended mode for faders
    internal.extendedMode.recieve(True, eventconsts.INCONTROL_FADERS)


