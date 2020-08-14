import general
import ui
import transport

from ..shiftstate import ShiftState
import config
import eventconsts
import internalconstants
import lightingconsts
from ..state import extendedMode, enterDebugMode


class DebugShift(ShiftState):
    def __init__(self):
        """Creates instance of ShiftState object

        Args:
            name (str): Name of shift button
            id_listen (int): Event ID for a shift button. This is checked when determining whether to enable shift.
        """
        self.name = "Debug"
        self.id_listen = eventconsts.TRANSPORT_STOP
        
        self.is_down = False
        self.is_sustained = False
        self.is_used = False
        
    def process(self, command):
        command.addProcessor("Debug shift menu")
        if command.type == eventconsts.TYPE_PAD:
            if command.is_lift:
                if command.note == eventconsts.Pads[0][0]: 
                    raise Exception("Manually initiated crash")
                    command.handle("Initiate crash")
                    
                elif command.note == eventconsts.Pads[1][0]: 
                    enterDebugMode()
                    command.handle("Enable debug mode")

                else:
                    command.handle("Shift menu catch others")

            else:
                command.handle("Shift menu catch press")

        
    def redraw(self, lights):


        # Crash
        lights.setPadColour(0, 0, lightingconsts.colours["RED"])

        # DEBUG MODE
        if len(config.CONSOLE_DEBUG_MODE) and config.DEBUG_HARD_CRASHING:
            lights.setPadColour(1, 0, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(1, 0, lightingconsts.colours["ORANGE"])
                

        lights.solidifyAll()

    def onPress(self):
        extendedMode.setVal(True, eventconsts.INCONTROL_PADS)
        
    def onLift(self):
        extendedMode.revert(eventconsts.INCONTROL_PADS)
        
            