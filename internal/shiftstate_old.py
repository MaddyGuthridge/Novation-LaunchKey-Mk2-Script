"""
internal > shiftstate.py

This module contains classes and objects regarding using buttons as shift controls.

Author: Miguel Guthridge
"""

import config
import internalconstants

from .windowstate import window
from .messages import sendCompleteInternalMidiMessage
from .state import getPortExtended


class ShiftMgr:
    is_down = False
    used = False
    sustained = False
    
    def setDown(self, value):
        self.is_down = value
        self.used = False

    def press(self, double_click):
        if getPortExtended():
            sendCompleteInternalMidiMessage(internalconstants.MESSAGE_SHIFT_DOWN)
        self.is_down = True
        self.used = False
        window.resetAnimationTick()
    
    def lift(self, double_click):
        
        if self.sustained:
            self.sustained = False
            self.used = True

        if double_click and config.ENABLE_SUSTAINED_SHIFT:
            self.sustained = True
        else:
            if getPortExtended():
                sendCompleteInternalMidiMessage(internalconstants.MESSAGE_SHIFT_UP)
        self.is_down = False
        window.resetAnimationTick()
        return self.used

    def use(self, lift = False):
        if self.is_down or self.sustained:
            if not getPortExtended():
                sendCompleteInternalMidiMessage(internalconstants.MESSAGE_SHIFT_USE)
            self.used = True
            if lift and config.AUTOCANCEL_SUSTAINED_SHIFT:
                self.sustained = False
            return True
        else: return False

    def getDown(self):
        if self.sustained:
            return self.sustained
        return self.is_down
    
    def getUsed(self):
        if self.is_down:
            return self.used
        else: return "ERROR Shift not down"

shift = ShiftMgr()

