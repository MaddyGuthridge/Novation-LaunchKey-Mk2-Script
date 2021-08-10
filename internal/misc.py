"""
internal > misc.py

Contains other functions, objects and classes regarding the internal state of the device.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import general
import transport

import lighting
import lightingconsts
from . import consts
import eventconsts

from .performance import idleClock
from .logging import getLineBreak, debugLog, getTab
from . import state
from .snap import snap

import controllerprocessors

def refreshProcessor():
    """Called on refresh
    """
    snap.refresh()

def idleProcessor():
    """Called on idle
    """
    # Start performance timer
    idleClock.start()

    # Increment animation tick
    window.incrementTicks()

    debugLog(getTab("Animation Tick:", 2) + str(window.getAnimationTick()), consts.DEBUG.ANIMATION_IDLE_TIMERS)
    debugLog(getTab("Idle Tick:", 2) + str(window.getIdleTick()), consts.DEBUG.ANIMATION_IDLE_TIMERS)
    debugLog("", consts.DEBUG.ANIMATION_IDLE_TIMERS)

    try:
        # Update active window
        window.update()
    except Exception as e:
        state.errors.triggerError(e)

    # Stop performance timer
    idleClock.stop()


class BeatMgr:
    """Manages beat numbers and lighting redraws for this
    """
    beat = 0

    def setBeat(self, beat):
        """Sets beat number

        Args:
            beat (int): Beat number (see FL scripting manual)
        """
        self.beat = beat
        self.redraw(lighting.state)

    def redraw(self, lights):
        """Draws beat light onto top right pad

        Args:
            lights (LightMap): Lighting object during redraw
        """
        
        if transport.getLoopMode():
            bar_col = lightingconsts.BEAT_SONG_BAR
            beat_col = lightingconsts.BEAT_SONG_BEAT
        else:
            bar_col = lightingconsts.BEAT_PAT_BAR
            beat_col = lightingconsts.BEAT_PAT_BEAT

        if self.beat is 1: lights.setPadColour(8, 0, bar_col)     # Bar
        elif self.beat is 2: lights.setPadColour(8, 0, beat_col)  # Beat

beat = BeatMgr()

def processSysEx(event):
    """Process SysEx events (which are always responses to universal device enquiries since the script doesn't really do any others)

    Args:
        event (ParsedEvent): processed MIDI Sysex Event
    """
    
    # Check if it matches device specifications
    if event.sysex[:8] == consts.DEVICE_RESPONSE_FIRST:
        if event.sysex[8] == consts.DEVICE_RESPONSE_25:
            state.DEVICE_TYPE = consts.DEVICE_KEYS_25

        elif event.sysex[8] == consts.DEVICE_RESPONSE_49:
            state.DEVICE_TYPE = consts.DEVICE_KEYS_49

        elif event.sysex[8] == consts.DEVICE_RESPONSE_61:
            state.DEVICE_TYPE = consts.DEVICE_KEYS_61
        else:
            state.DEVICE_TYPE = consts.DEVICE_UNRECOGNISED
            print("If you're seeing this, create an issue on GitHub. ")
            print("Make sure to tell me your device info, and include a copy of the Syxex Event below.")
            print("Link to GitHub Page: " + consts.SCRIPT_URL)

        controllerprocessors.onInit()
        
    else:
        state.DEVICE_TYPE = consts.DEVICE_UNRECOGNISED
        print("ERROR - DEVICE NOT RECOGNISED")
        

    getLineBreak()
    getLineBreak()
    print("")

from .windowstate import window
