"""
internal > misc.py

Contains other functions, objects and classes regarding the internal state of the device.

Author: Miguel Guthridge
"""

import general
import transport

import lighting
import lightingconsts
import internalconstants
import eventconsts

from .performance import idleClock
from .logging import getLineBreak, debugLog, getTab
from . import state
from .snap import snap

import controllerprocessors

def refreshProcessor():
    """Called on refresh
    """
    beat.refresh()
    snap.refresh()
    


def idleProcessor():
    """Called on idle
    """
    # Start performance timer
    idleClock.start()

    # Increment animation tick
    window.incrementTicks()

    debugLog(getTab("Animation Tick:", 2) + str(window.getAnimationTick()), internalconstants.DEBUG_ANIMATION_IDLE_TIMERS)
    debugLog(getTab("Idle Tick:", 2) + str(window.getIdleTick()), internalconstants.DEBUG_ANIMATION_IDLE_TIMERS)
    debugLog("", internalconstants.DEBUG_ANIMATION_IDLE_TIMERS)

    # Update active window
    window.update()
    
    # If in a right-click menu, reset idle timer
    

    # Stop performance timer
    idleClock.stop()


class BeatMgr:
    """Manages beat numbers and lighting redraws for this
    """
    beat = 0

    is_tapping_tempo = False
    
    metronome_enabled = False


    def refresh(self):
        """Update beat number
        """
        self.metronome_enabled = (general.getUseMetronome() == 1)

    
    def toggle_metronome(self):
        """Toggle state of metronome

        Returns:
            bool: Whether the metronome is now enabled
        """
        transport.globalTransport(eventconsts.midi.FPT_Metronome, True)
        self.metronome_enabled = (general.getUseMetronome() == 1)
        return self.metronome_enabled


    def toggle_tempo_tap(self):
        """Toggles tempo tapping

        Returns:
            bool: Whether tempo tapping is now enabled
        """
        self.is_tapping_tempo = not self.is_tapping_tempo
        return self.is_tapping_tempo


    def tap_tempo(self):
        """Taps tempo
        """
        transport.globalTransport(eventconsts.midi.FPT_TapTempo, True)

    
    def set_beat(self, beat):
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

        if self.is_tapping_tempo:
            lights.setPadColour(8, 0, lightingconsts.TEMPO_TAP)
        
        if transport.getLoopMode():
            bar_col = lightingconsts.BEAT_SONG_BAR
            beat_col = lightingconsts.BEAT_SONG_BEAT
        else:
            bar_col = lightingconsts.BEAT_PAT_BAR
            beat_col = lightingconsts.BEAT_PAT_BEAT

        if self.beat is 1: lights.setPadColour(8, 0, bar_col)     # Bar
        elif self.beat is 2: lights.setPadColour(8, 0, beat_col)  # Beat

        if self.metronome_enabled:
            lights.setPadColour(8, 0, lightingconsts.METRONOME)

beat = BeatMgr()

def processSysEx(event):
    """Process SysEx events (which are always responses to universal device enquiries since the script doesn't really do any others)

    Args:
        event (ProcessedEvent): processed MIDI Sysex Event
    """
    
    # Check if it matches device specifications
    if event.sysex[:8] == internalconstants.DEVICE_RESPONSE_FIRST:
        if event.sysex[8] == internalconstants.DEVICE_RESPONSE_25:
            state.DEVICE_TYPE = internalconstants.DEVICE_KEYS_25

        elif event.sysex[8] == internalconstants.DEVICE_RESPONSE_49:
            state.DEVICE_TYPE = internalconstants.DEVICE_KEYS_49

        elif event.sysex[8] == internalconstants.DEVICE_RESPONSE_61:
            state.DEVICE_TYPE = internalconstants.DEVICE_KEYS_61
        else:
            state.DEVICE_TYPE = internalconstants.DEVICE_UNRECOGNISED
            print("If you're seeing this, create an issue on GitHub. ")
            print("Make sure to tell me your device info, and include a copy of the Syxex Event below.")
            print("Link to GitHub Page: " + internalconstants.SCRIPT_URL)

        controllerprocessors.onInit()
        
    else:
        state.DEVICE_TYPE = internalconstants.DEVICE_UNRECOGNISED
        print("ERROR - DEVICE NOT RECOGNISED")
        

    getLineBreak()
    getLineBreak()
    print("")

from .windowstate import window
