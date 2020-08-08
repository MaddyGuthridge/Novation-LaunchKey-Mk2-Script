"""
internal > window.py

Contains objects and functions to do with managing active FL windows.

Author: Miguel Guthridge
"""

import ui

import internalconstants
import config
import eventprocessor

import WindowProcessors.processwindows as processwindows
import PluginProcessors.processplugins as processplugins

from .logging import debugLog, getLineBreak


class WindowMgr:
    """Contains and manages the state of FL Windows as well as tickers for animations.
    """
    def __init__(self):
        self.plugin_focused = False
        self.previous_plugin = ""
        self.active_plugin = ""
        self.active_fl_window = -1
        self.animation_tick_number = 0
        self.idle_tick_number = 0
        self.absolute_tick_number = 0
        self.in_popup = False
    
    
    def resetAnimationTick(self):
        """Reset animation tick to zero (play animations again)
        """
        debugLog("Reset animation timer", internalconstants.DEBUG_LIGHTING_RESET)
        self.animation_tick_number = 0

    
    def resetIdleTick(self):
        """Reset idle tick to zero (cancel light show)
        """
        debugLog("Reset idle timer", internalconstants.DEBUG_LIGHTING_RESET)
        self.idle_tick_number = 0

    
    def incrementTicks(self):
        """Increments all tick counters
         - Animation tick
         - Idle tick
         - Absolute tick
        """
        self.animation_tick_number += 1
        self.idle_tick_number += 1
        self.absolute_tick_number += 1

    
    def getAnimationTick(self):
        """Get number of ticks since last window change or animation reset
        Used when calculating the drawing of animations.

        Returns:
            int: animation tick
        """
        if config.LIGHTS_REDUCE_MOTION:
            return config.IDLE_WAIT_TIME - 1
        else:
            return self.animation_tick_number

    
    def getIdleTick(self):
        """Get number of ticks since last event. Used to help draw idle light show.

        Returns:
            int: idle tick
        """
        return self.idle_tick_number


    def getAbsoluteTick(self):
        """Returns number of ticks since script started

        Returns:
            int: absolute tick
        """
        return self.absolute_tick_number

    
    def getInPopup(self):
        """Returns whether a popup menu is active

        Returns:
            bool: whether a popup is active
        """
        return self.in_popup

    
    def update(self):
        """Update active window

        Returns:
            bool: Changed
        """
        
        popup_active = ui.isInPopupMenu()
        if popup_active:
            # If state has changed, reset idle tick
            if not self.in_popup:
                self.resetIdleTick()
                self.resetAnimationTick()
                
            self.in_popup = True
            
        else:
            # If state has changed, reset idle tick
            if self.in_popup:
                self.resetIdleTick()
                self.resetAnimationTick()
                
            self.in_popup = False
            
        
        old_window = self.active_fl_window
        # Update FL Window
        if   ui.getFocused(internalconstants.WINDOW_MIXER):        
            new_fl_window = internalconstants.WINDOW_MIXER

        elif ui.getFocused(internalconstants.WINDOW_PIANO_ROLL):   
            new_fl_window = internalconstants.WINDOW_PIANO_ROLL

        elif ui.getFocused(internalconstants.WINDOW_CHANNEL_RACK): 
            new_fl_window = internalconstants.WINDOW_CHANNEL_RACK

        elif ui.getFocused(internalconstants.WINDOW_PLAYLIST):     
            new_fl_window = internalconstants.WINDOW_PLAYLIST

        elif ui.getFocused(internalconstants.WINDOW_BROWSER):      
            new_fl_window = internalconstants.WINDOW_BROWSER
        
        else: new_fl_window = -1

        # Detect change in

        # If active FL window changes
        if (new_fl_window != self.active_fl_window or self.plugin_focused == True) and new_fl_window != -1:

            # End active window
            eventprocessor.activeEnd()

            # End old window
            if new_fl_window != self.active_fl_window:
                processwindows.topWindowEnd()

            # Set active window
            self.active_fl_window = new_fl_window
            self.plugin_focused =  False

            debugLog("Active Window: " + getFlWindowString(self.active_fl_window), internalconstants.DEBUG_WINDOW_CHANGES)
            debugLog("[Background: " + self.active_plugin + "]", internalconstants.DEBUG_WINDOW_CHANGES)
            debugLog(getLineBreak())

            # Start new window
            if new_fl_window != old_window:
                processwindows.topWindowStart()

            # Start new window active
            eventprocessor.activeStart()

            if not shift.getDown():   
                self.resetAnimationTick()
            self.resetIdleTick()
            return True
        
        else: # Check for changes to Plugin
            new_plugin = ui.getFocusedFormCaption()
            old_plugin = self.active_plugin
            
            special_flag = False

            # Check for special windows
            if new_plugin == internalconstants.WINDOW_STR_COLOUR_PICKER or new_plugin == internalconstants.WINDOW_STR_SCRIPT_OUTPUT:
                special_flag = True

            if not special_flag:
                last = -1
                length = len(new_plugin)
                for y in range(length):
                    if new_plugin[y] is '(':
                        last = y + 1
                if last == -1 or last > length: # If no brackets found
                    return False
                
                # Trim string
                new_plugin = new_plugin[last: -2]

            # If window changed
            
            if new_plugin != self.active_plugin or self.plugin_focused == False:

                # End active plugin
                eventprocessor.activeEnd()

                # End replaced plugin
                if new_plugin != self.active_plugin:
                    self.previous_plugin = self.active_plugin
                    processplugins.topPluginEnd()

                # Set new plugin
                self.plugin_focused = True
                self.active_plugin = new_plugin

                debugLog("Active Window: " + self.active_plugin, internalconstants.DEBUG_WINDOW_CHANGES)
                debugLog("[Background: " + getFlWindowString(self.active_fl_window) + "]", internalconstants.DEBUG_WINDOW_CHANGES)
                debugLog(getLineBreak(), internalconstants.DEBUG_WINDOW_CHANGES)

                # Start new plugin
                if new_plugin != old_plugin:
                    processplugins.topPluginStart()

                # Start new plugin active
                eventprocessor.activeStart()

                if not shift.getDown():   
                    self.resetAnimationTick()
                self.resetIdleTick()
                return True
            else: return False

    def getString(self):
        """Returns current window as a string

        Returns:
            str: Current window name
        """
        if self.plugin_focused:
            return self.active_plugin

        else:
            return getFlWindowString(self.active_fl_window)

    
    def revertPlugin(self):
        """Reverts to previous plugin
        
        Note to self: I don't know when this is used - probably delete at some point.
        """
        self.active_plugin = self.previous_plugin
        self.previous_plugin = ""

# Create instance of window object
window = WindowMgr()


def getFlWindowString(index):
    """Returns FL Window as string given window index

    Args:
        index (int): FL Window index

    Returns:
        str: FL Window name
    """
    if index == -1: return "NONE"
    if index == internalconstants.WINDOW_MIXER: return internalconstants.WINDOW_STR_MIXER
    if index == internalconstants.WINDOW_PLAYLIST: return internalconstants.WINDOW_STR_PLAYLIST
    if index == internalconstants.WINDOW_CHANNEL_RACK: return internalconstants.WINDOW_STR_CHANNEL_RACK
    if index == internalconstants.WINDOW_PIANO_ROLL: return internalconstants.WINDOW_STR_PIANO_ROLL
    if index == internalconstants.WINDOW_BROWSER: return internalconstants.WINDOW_STR_BROWSER
    
from .shiftstate import shift
    