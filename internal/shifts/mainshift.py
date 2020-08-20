"""
internal > shifts > mainshift.py

Contains class to manage shift mode for normal shift

Author: Miguel Guthridge
"""

import general
import ui
import transport

from ..shiftstate import ShiftState
import eventconsts
from .. import consts
import lightingconsts
from ..snap import snap
from ..windowstate import window
from ..state import extendedMode
from ..messages import sendCompleteInternalMidiMessage


class MainShift(ShiftState):
    def __init__(self):
        """Creates instance of ShiftState object

        Args:
            name (str): Name of shift button
            id_listen (int): Event ID for a shift button. This is checked when determining whether to enable shift.
        """
        self.name = "Shift"
        self.id_listen = eventconsts.TRANSPORT_LOOP
        
        self.enable_sustain = True
        self.is_down = False
        self.is_sustained = False
        self.is_used = False
        
    def process(self, command):
        """Process events in shift menu

        Args:
            command (ParsedEvent): Event to process
        """
        command.addProcessor("Main shift menu")
        if command.type == eventconsts.TYPE_FADER_BUTTON:
            snap.processSnapMode(command)
            self.use()
        elif command.type == eventconsts.TYPE_PAD:
            if command.is_lift:
                if command.note == eventconsts.Pads[0][1]: 
                    ui.showWindow(consts.WINDOW_PLAYLIST)
                    self.use()
                    command.handle("Switched window to Playlist")
                    
                elif command.note == eventconsts.Pads[1][1]: 
                    ui.showWindow(consts.WINDOW_CHANNEL_RACK)
                    self.use()
                    command.handle("Switched window to Channel rack")
                    
                elif command.note == eventconsts.Pads[2][1]: 
                    ui.showWindow(consts.WINDOW_PIANO_ROLL)
                    self.use()
                    command.handle("Switched window to Piano roll")
                    
                elif command.note == eventconsts.Pads[3][1]: 
                    ui.showWindow(consts.WINDOW_MIXER)
                    self.use()
                    command.handle("Switched window to Mixer")
                    
                elif command.note == eventconsts.Pads[4][1]: 
                    ui.showWindow(consts.WINDOW_BROWSER)
                    self.use()
                    command.handle("Switched window to Browser")
                    
                elif command.note == eventconsts.Pads[6][0]: 
                    ui.selectWindow(True)
                    self.use()
                    command.handle("Previous window")
                
                elif command.note == eventconsts.Pads[7][0]: 
                    ui.selectWindow(False)
                    self.use()
                    command.handle("Next window")
                    
                elif command.note == eventconsts.Pads[0][0]: 
                    general.undoUp()
                    self.use()
                    command.handle("Undo")
                    
                elif command.note == eventconsts.Pads[1][0]: 
                    general.undoDown()
                    self.use()
                    command.handle("Redo")

                elif command.note == eventconsts.Pads[7][1]:
                    transport.globalTransport(eventconsts.midi.FPT_F8, 1)
                    self.use()
                    command.handle("Launch Plugin Picker")

                elif command.note == eventconsts.Pads[3][0]:
                    transport.globalTransport(eventconsts.midi.FPT_Save, 1)
                    self.use()
                    command.handle("Save project")
                else:
                    command.handle("Shift menu catch others")

            else:
                command.handle("Shift menu catch press")

        
    def redraw(self, lights):
        """Redraw lights

        Args:
            lights (LightMap): Lights to draw on
        """

        UNDO_LAST = 1
        UNDO_MIDDLE = 0
        UNDO_FIRST = -1

        undo_position = general.getUndoHistoryLast()
        undo_length = general.getUndoHistoryCount()
        
        if undo_position == 0:
            undo_type = UNDO_LAST
        elif undo_position + 1 == undo_length:
            undo_type = UNDO_FIRST
        else:
            undo_type = UNDO_MIDDLE

        if window.getAnimationTick() > 0:
            # Playlist
            if window.getString() == consts.FL_WINDOW_LIST[consts.WINDOW_PLAYLIST]:
                lights.setPadColour(0, 1, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(0, 1, lightingconsts.WINDOW_PLAYLIST)

        if window.getAnimationTick() > 1:
            # Channel Rack
            if window.getString() == consts.FL_WINDOW_LIST[consts.WINDOW_CHANNEL_RACK]:
                lights.setPadColour(1, 1, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(1, 1, lightingconsts.WINDOW_CHANNEL_RACK)

            # Undo
            if undo_type  == UNDO_FIRST:
                lights.setPadColour(0, 0, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(0, 0, lightingconsts.UI_UNDO)

        if window.getAnimationTick() > 2:
            # Piano roll
            if window.getString() == consts.FL_WINDOW_LIST[consts.WINDOW_PIANO_ROLL]:
                lights.setPadColour(2, 1, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(2, 1, lightingconsts.WINDOW_PIANO_ROLL)

            # Redo
            if undo_type == UNDO_LAST:
                lights.setPadColour(1, 0, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(1, 0, lightingconsts.UI_REDO)

        if window.getAnimationTick() > 3:
            # Mixer
            if window.getString() == consts.FL_WINDOW_LIST[consts.WINDOW_MIXER]:
                lights.setPadColour(3, 1, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(3, 1, lightingconsts.WINDOW_MIXER)

            # Next plugin
            lights.setPadColour(7, 0, lightingconsts.UI_NAV_HORIZONTAL)

            # Save
            lights.setPadColour(3, 0, lightingconsts.UI_SAVE)
            
        if window.getAnimationTick() > 4:
            # Browser
            if window.getString() == consts.FL_WINDOW_LIST[consts.WINDOW_BROWSER]:
                lights.setPadColour(4, 1, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(4, 1, lightingconsts.WINDOW_BROWSER)

            # Prev plugin
            lights.setPadColour(6, 0, lightingconsts.UI_NAV_HORIZONTAL)

            # Plugin picker
            lights.setPadColour(7, 1, lightingconsts.WINDOW_PLUGIN_PICKER)
                

        lights.solidifyAll()

    def onPress(self):
        """When shift button pressed
        """
        extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
        extendedMode.setVal(True, eventconsts.INCONTROL_FADERS)
        sendCompleteInternalMidiMessage(consts.MESSAGE_SHIFT_DOWN)
        
    def onLift(self):
        """When shift button lifted
        """
        extendedMode.revert(eventconsts.INCONTROL_PADS)
        extendedMode.revert(eventconsts.INCONTROL_FADERS)
        sendCompleteInternalMidiMessage(consts.MESSAGE_SHIFT_UP)
        
            