"""
internal.py
This file contains functions common to  scripts loaded by both files.

"""

#-------------------------------
# Edit this file at your own risk. All user-modifyable variables are found in 'config.py'.
#-------------------------------

import time

import device
import ui

import eventconsts
import config
import eventprocessor

import WindowProcessors.processwindows as processwindows
import PluginProcessors.processplugins as processplugins

PORT = -1 # Set in initialisation function then left constant

extendedMode = False
inControl_Knobs = False
inControl_Faders = False
inControl_Pads = False

ActiveWindow = "Nil"

# The previous mesage sent to the MIDI out device
previous_event_out = 0

# Prints a line break
def printLineBreak():
    print("————————————————————————————————————————————————————")

# Returns string with tab characters at the end
def newGetTab(string, length = config.TAB_LENGTH):
    string += " "
    toAdd = length - len(string) % length

    for x in range(toAdd):
        string += " "
    return string

# Counts processing time
class performanceMonitor:
    def __init__(self):
        self.total_time = 0
        self.startTime = -1
        self.endTime = -1
    
    def start(self):
        self.startTime = time.perf_counter()
    
    def stop(self):
        self.endTime = time.perf_counter()
        a = self.endTime - self.startTime
        self.total_time += a
        if config.CONSOLE_PRINT_PERFORMANCE_TIMES:
            print("")
            print("Processed in: ", round(self.endTime, 4), " seconds")
            print("Total processing time: ", round(self.total(), 4))
        return a
    
    def total(self):
        return self.total_time
eventClock = performanceMonitor()
idleClock = performanceMonitor()


# Manages active window - CURRENTLY BROKEN!!!!
class windowMgr:
    def __init__(self):
        self.plugin_focused = False
        self.active_plugin = ""
        self.active_fl_window = -1
    
    """
    def update(self):
        self.active_fl_window
        # Update FL Window
        if   ui.getFocused(config.WINDOW_MIXER):        
            new_fl_window = config.WINDOW_MIXER

        elif ui.getFocused(config.WINDOW_PIANO_ROLL):   
            new_fl_window = config.WINDOW_PIANO_ROLL

        elif ui.getFocused(config.WINDOW_CHANNEL_RACK): 
            new_fl_window = config.WINDOW_CHANNEL_RACK

        elif ui.getFocused(config.WINDOW_PLAYLIST):     
            new_fl_window = config.WINDOW_PLAYLIST

        elif ui.getFocused(config.WINDOW_BROWSER):      
            new_fl_window = config.WINDOW_BROWSER
        
        else: new_fl_window = -1

        # If active window for FL plugin changes
        if new_fl_window != self.active_fl_window:
            eventprocessor.activeEnd()
            self.active_fl_window = new_fl_window
            eventprocessor.activeStart()

        new = ui.getFocusedFormCaption()
        # If window is FL Window
        if ui.getFocused(config.WINDOW_MIXER) or ui.getFocused(config.WINDOW_PIANO_ROLL) or ui.getFocused(config.WINDOW_PLAYLIST) or \
            ui.getFocused(config.WINDOW_CHANNEL_RACK) or ui.getFocused(config.WINDOW_BROWSER):

            # If active window not focused
            if self.plugin_focused == False: return
            self.plugin_focused = False
            print("Background: ", self.active_plugin)
            printLineBreak()
        else:
            # If window didn't change
            if new == self.active_plugin:
                return False
            else:
                self.plugin_focused = True
                self.active_plugin = new
            print("Window: ", self.active_plugin, "[Active]")
            printLineBreak()
            return True
    """

    def update(self):
        old_window = self.active_fl_window
        # Update FL Window
        if   ui.getFocused(config.WINDOW_MIXER):        
            new_fl_window = config.WINDOW_MIXER

        elif ui.getFocused(config.WINDOW_PIANO_ROLL):   
            new_fl_window = config.WINDOW_PIANO_ROLL

        elif ui.getFocused(config.WINDOW_CHANNEL_RACK): 
            new_fl_window = config.WINDOW_CHANNEL_RACK

        elif ui.getFocused(config.WINDOW_PLAYLIST):     
            new_fl_window = config.WINDOW_PLAYLIST

        elif ui.getFocused(config.WINDOW_BROWSER):      
            new_fl_window = config.WINDOW_BROWSER
        
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

            print("Active Window: ", get_fl_window_string(self.active_fl_window))
            print("[Background: ", self.active_plugin, "]")
            printLineBreak()

            # Start new window
            if new_fl_window != old_window:
                processwindows.topWindowStart()

            # Start new window active
            eventprocessor.activeStart()
            return True
        else: # Check for changes to Plugin
            new_plugin = ui.getFocusedFormCaption()
            old_plugin = self.active_plugin
            
            last = -1
            length = len(new_plugin)
            for y in range(length):
                if new_plugin[y] is '(':
                    last = y + 1
            if last == -1 or last > length: # If no brackets found
                return False
            
            # Trim string
            new_plugin = new_plugin[last: -2]

            # If window didn't change
            
            if new_plugin != self.active_plugin or self.plugin_focused == False:

                # End active plugin
                eventprocessor.activeEnd()

                # End replaced plugin
                if new_plugin != self.active_plugin:
                    processplugins.topPluginEnd()

                # Set new plugin
                self.plugin_focused = True
                self.active_plugin = new_plugin

                print("Active Window: ", self.active_plugin)
                print("[Background: ", get_fl_window_string(self.active_fl_window), "]")
                printLineBreak()

                # Start new plugin
                if new_plugin != old_plugin:
                    processplugins.topPluginStart()

                # Start new plugin active
                eventprocessor.activeStart()
                return True
            else: return False


window = windowMgr()

# Gets string for FL Window
def get_fl_window_string(index):
    if index == -1: return "NONE"
    if index == config.WINDOW_MIXER: return "Mixer"
    if index == config.WINDOW_PLAYLIST: return "Playlist"
    if index == config.WINDOW_CHANNEL_RACK: return "Channel Rack"
    if index == config.WINDOW_PIANO_ROLL: return "Piano Roll"
    if index == config.WINDOW_BROWSER: return "Browser"

# Print command data
def printCommand(command):
    command.printInfo()
    return

# Print command results
def printCommandOutput(command):
    command.printOutput()
    processTime = eventClock.stop()
    printLineBreak()
    print("")

# Queries whether extended mode is active. Only accessible from extended port
def queryExtendedMode(option = eventconsts.SYSTEM_EXTENDED):
    global extendedMode
    global inControl_Knobs
    global inControl_Faders
    global inControl_Pads
    
    if option == eventconsts.SYSTEM_EXTENDED: return extendedMode
    elif option == eventconsts.INCONTROL_KNOBS: return inControl_Knobs
    elif option == eventconsts.INCONTROL_FADERS: return inControl_Faders
    elif option == eventconsts.INCONTROL_PADS: return inControl_Pads

# Sets extended mode on the device, use inControl constants to choose which
def setExtendedMode(newMode, option = eventconsts.SYSTEM_EXTENDED):
    global extendedMode
    global inControl_Knobs
    global inControl_Faders
    global inControl_Pads

    # Set all
    if option == eventconsts.SYSTEM_EXTENDED:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0C, 0x7F)
            extendedMode = True
            inControl_Knobs = True
            inControl_Faders = True
            inControl_Pads = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0C, 0x00)
            extendedMode = False
            inControl_Knobs = False
            inControl_Faders = False
            inControl_Pads = False
        else: logError("New mode mode not boolean")
    
    # Set knobs
    elif option == eventconsts.INCONTROL_KNOBS:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0D, 0x7F)
            inControl_Knobs = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0D, 0x00)
            inControl_Knobs = False
        else: logError("New mode mode not boolean")
    
    # Set faders
    elif option == eventconsts.INCONTROL_FADERS:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0E, 0x7F)
            inControl_Faders = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0E, 0x00)
            inControl_Faders = False
        else: logError("New mode mode not boolean")
    
    # Set pads
    elif option == eventconsts.INCONTROL_PADS:
        if newMode is True:
            sendMidiMessage(0x9F, 0x0F, 0x7F)
            inControl_Pads = True
        elif newMode is False:
            sendMidiMessage(0x9F, 0x0F, 0x00)
            inControl_Pads = False
        else: logError("New mode mode not boolean")

# Processes extended mode messages from device
def recieveExtendedMode(newMode, option = eventconsts.SYSTEM_EXTENDED):
    global extendedMode
    global inControl_Knobs
    global inControl_Faders
    global inControl_Pads

    # Set all
    if option == eventconsts.SYSTEM_EXTENDED:
        if newMode is True:
            extendedMode = True
            inControl_Knobs = True
            inControl_Faders = True
            inControl_Pads = True
        elif newMode is False:
            extendedMode = False
            inControl_Knobs = False
            inControl_Faders = False
            inControl_Pads = False
        else: logError("New mode mode not boolean")
    
    # Set knobs
    elif option == eventconsts.INCONTROL_KNOBS:
        if newMode is True:
            inControl_Knobs = True
        elif newMode is False:
            inControl_Knobs = False
        else: logError("New mode mode not boolean")
    
    # Set faders
    elif option == eventconsts.INCONTROL_FADERS:
        if newMode is True:
            inControl_Faders = True
        elif newMode is False:
            inControl_Faders = False
        else: logError("New mode mode not boolean")
    
    # Set pads
    elif option == eventconsts.INCONTROL_PADS:
        if newMode is True:
            inControl_Pads = True
        elif newMode is False:
            inControl_Pads = False
        else: logError("New mode mode not boolean")

# Compares revieved event to previous
def compareEvent(event):
    if toMidiMessage(event.status, event.data1, event.data2) is previous_event_out: return True
    else: return False

EventNameT = ['Note Off', 'Note On ', 'Key Aftertouch', 'Control Change','Program Change',  'Channel Aftertouch', 'Pitch Bend', 'System Message' ]

# Sends message to the default MIDI out device
def sendMidiMessage(status, data1, data2):
    global previous_event_out
    previous_event_out  = toMidiMessage(status, data1, data2)
    device.midiOutMsg(previous_event_out)

# Generates a MIDI message given arguments
def toMidiMessage(status, data1, data2):
    return status + (data1 << 8) + (data2 << 16)

# Returns snap value
def snap(value, snapTo):
    if abs(value - snapTo) <= config.SNAP_RANGE:
        return snapTo
    else: return value
# Returns snap value
def didSnap(value, snapTo):
    if abs(value - snapTo) <= config.SNAP_RANGE:
        return True
    else: return False

# Converts MIDI event range to float for use in volume, pan, etc functions
def toFloat(value, min = 0, max = 1):
    return (value / 127) * (max - min) + min

# Called on idle
def idleProcessor():
    # Start performance timer
    idleClock.start()
    window.update()

    # Stop performance timer
    idleClock.stop()

# Print out error message
def logError(message):
    print("Error: ", message)

