"""
internal > shifts > debugshift.py

Contains class to manage shift mode for debugging

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import general
import ui
import transport

from ..shiftstate import ShiftState
from ..windowstate import window
import config
import eventconsts
from .. import consts
import lightingconsts
from lighting import triggerIdleLightshow
from ..state import extendedMode, enterDebugMode

# Ticks until menu is drawn/handled
ENABLE_AFTER = 10

changed_incontrol = False

class DebugShift(ShiftState):
    def __init__(self):
        """Creates instance of ShiftState object

        Args:
            name (str): Name of shift button
            id_listen (int): Event ID for a shift button. This is checked when determining whether to enable shift.
        """
        self.name = "Debug"
        self.id_listen = eventconsts.TRANSPORT_STOP
        
        self.enable_sustain = False
        self.is_down = False
        self.is_sustained = False
        self.is_used = False
        
    def process(self, command):
        """Process events when menu active

        Args:
            command (ParsedEvent): Event to process

        Raises:
            Exception: Manually initiated crash
        """
        if window.getAnimationTick() > ENABLE_AFTER:
            command.addProcessor("Debug shift menu")
            if command.type == eventconsts.TYPE_PAD:
                if command.is_lift:
                    if command.note == eventconsts.Pads[0][0]: 
                        command.handle("Initiate crash")
                        self.use()
                        raise Exception("Manually initiated crash")
                        
                        
                    elif command.note == eventconsts.Pads[1][0]: 
                        enterDebugMode()
                        self.use()
                        command.handle("Enable debug mode")
                        
                    elif command.note == eventconsts.Pads[2][0]:
                        triggerIdleLightshow()
                        self.use()
                        command.handle("Trigger lightshow")

                    else:
                        command.handle("Shift menu catch others")

                else:
                    command.handle("Shift menu catch press")

        
    def redraw(self, lights):
        """Redraw lights

        Args:
            lights (LightMap): Lights to draw on
        """
        global changed_incontrol
        if window.getAnimationTick() == ENABLE_AFTER and not changed_incontrol and not extendedMode.query(eventconsts.INCONTROL_PADS):
            extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
            changed_incontrol = True

        if (window.getAnimationTick() > ENABLE_AFTER and extendedMode.query(eventconsts.INCONTROL_PADS)) or changed_incontrol:
            # Crash
            lights.setPadColour(0, 0, lightingconsts.colours["RED"])

            # DEBUG MODE
            if len(config.CONSOLE_DEBUG_MODE) and config.DEBUG_HARD_CRASHING:
                lights.setPadColour(1, 0, lightingconsts.colours["DARK GREY"])
            else:
                lights.setPadColour(1, 0, lightingconsts.colours["ORANGE"])
            
            # Light show
            lights.setPadColour(2, 0, lightingconsts.colours["GREEN"])

            lights.solidifyAll()

    def onPress(self):
        """When the shift button is pressed
        """
        global changed_incontrol
        changed_incontrol = False
        
    def onLift(self):
        """When the shift button is lifted
        """
        if changed_incontrol:
            extendedMode.revert(eventconsts.INCONTROL_PADS)
        
            