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
import transport
import general

import eventconsts
import config
import eventprocessor
import lighting
# import updatecheck # Currently modules are unavailable

import WindowProcessors.processwindows as processwindows
import PluginProcessors.processplugins as processplugins

MIN_FL_SCRIPT_VERSION = 4

PORT = -1 # Set in initialisation function then left constant

SHARED_INIT_OK = False
SCRIPT_UPDATE_AVAILABLE = False


""" # Inactive code... delete soon

ActiveWindow = "Nil"

# The previous mesage sent to the MIDI out device
previous_event_out = 0
"""

def getVersionStr():
    return str(config.SCRIPT_VERSION_MAJOR) + '.' + str(config.SCRIPT_VERSION_MINOR) + '.' + str(config.SCRIPT_VERSION_REVISION)

def sharedInit():
    global SHARED_INIT_OK
    global SCRIPT_UPDATE_AVAILABLE
    printLineBreak()

    print(config.SCRIPT_NAME + " - Version: " + getVersionStr())
    print(" - " + config.SCRIPT_AUTHOR)
    print("")
    print("Running in FL Studio Version: " + ui.getVersion())

    # Check for script updates
    # updatecheck.check()
    if SCRIPT_UPDATE_AVAILABLE:
        printLineBreak()
        print("An update to this script is available!")
        print("Follow this link to download it: " + config.SCRIPT_URL)
        printLineBreak()


    midi_script_version = general.getVersion()
    print("FL Studio Scripting version: " + str(midi_script_version) + ". Minimum recommended version: " + str(MIN_FL_SCRIPT_VERSION))

    if midi_script_version < MIN_FL_SCRIPT_VERSION:
        print("You may encounter issues using this script. Consider updating to the latest version FL Studio.")
    else: SHARED_INIT_OK = True
    print("")

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
            
            special_flag = False

            # Check for special windows
            if new_plugin == "Color selector" or new_plugin == "Script output":
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

# Handles extended mode state
class extended:
    def __init__(self):
        self.extendedMode = False
        self.inControl_Knobs = False
        self.inControl_Faders = False
        self.inControl_Pads = False

        self.prev_extendedMode = False
        self.prev_inControl_Knobs = False
        self.prev_inControl_Faders = False
        self.prev_inControl_Pads = False

    # Queries whether extended mode is active. Only accessible from extended port
    def query(self, option = eventconsts.SYSTEM_EXTENDED):
        
        if option == eventconsts.SYSTEM_EXTENDED: return self.extendedMode
        elif option == eventconsts.INCONTROL_KNOBS: return self.inControl_Knobs
        elif option == eventconsts.INCONTROL_FADERS: return self.inControl_Faders
        elif option == eventconsts.INCONTROL_PADS: return self.inControl_Pads

    def revert(self, option = eventconsts.SYSTEM_EXTENDED):
        # Set all
        if option == eventconsts.SYSTEM_EXTENDED:
            
            if self.prev_extendedMode is True:
                self.setVal(True)
            elif self.prev_extendedMode is False:
                self.setVal(False)
            else: logError("New mode mode not boolean")

            

        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            
            if self.prev_inControl_Knobs is True:
                self.setVal(True, eventconsts.INCONTROL_KNOBS)
            elif self.prev_inControl_Knobs is False:
                self.setVal(False, eventconsts.INCONTROL_KNOBS)
            else: logError("New mode mode not boolean")
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            if self.prev_inControl_Faders is True:
                self.setVal(True, eventconsts.INCONTROL_FADERS)
            elif self.prev_inControl_Faders is False:
                self.setVal(False, eventconsts.INCONTROL_FADERS)
            else: logError("New mode mode not boolean")
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
           
            if self.prev_inControl_Pads is True:
                self.setVal(True, eventconsts.INCONTROL_PADS)
            elif self.prev_inControl_Pads is False:
                self.setVal(False, eventconsts.INCONTROL_PADS)
            else: logError("New mode mode not boolean")


    # Sets extended mode on the device, use inControl constants to choose which
    def setVal(self, newMode, option = eventconsts.SYSTEM_EXTENDED):
        # Set all
        if option == eventconsts.SYSTEM_EXTENDED:
            if newMode is True and self.extendedMode is False:
                sendMidiMessage(0x9F, 0x0C, 0x7F)
            elif newMode is True and self.extendedMode is True: # Doesn't send event but still add it to history
                self.prev_extendedMode = True
            elif newMode is False and self.extendedMode is True:
                sendMidiMessage(0x9F, 0x0C, 0x00)
            elif newMode is False and self.extendedMode is False: # Doesn't send event but still add it to history
                self.prev_extendedMode = False
            
        
        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            if newMode is True and self.inControl_Knobs is False:
                sendMidiMessage(0x9F, 0x0D, 0x7F)
            elif newMode is True and self.inControl_Knobs is True: # Doesn't send event but still add it to history
                self.prev_inControl_Knobs = True
            elif newMode is False and self.inControl_Knobs is True:
                sendMidiMessage(0x9F, 0x0D, 0x00)
            elif newMode is False and self.inControl_Knobs is False: # Doesn't send event but still add it to history
                self.prev_inControl_Knobs = False
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            if newMode is True and self.inControl_Faders is False:
                sendMidiMessage(0x9F, 0x0E, 0x7F)
            elif newMode is True and self.inControl_Faders is True: # Doesn't send event but still add it to history
                self.prev_inControl_Faders = True
            elif newMode is False and self.inControl_Faders is True:
                sendMidiMessage(0x9F, 0x0E, 0x00)
            elif newMode is False and self.inControl_Faders is False: # Doesn't send event but still add it to history
                self.prev_inControl_Faders = False
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            if newMode is True and self.inControl_Pads is False:
                sendMidiMessage(0x9F, 0x0F, 0x7F)
            elif newMode is True and self.inControl_Pads is True: # Doesn't send event but still add it to history
                self.prev_inControl_Pads = True
            elif newMode is False and self.inControl_Pads is True:
                sendMidiMessage(0x9F, 0x0F, 0x00)
            elif newMode is False and self.inControl_Pads is False: # Doesn't send event but still add it to history
                self.prev_inControl_Pads = False

    # Processes extended mode messages from device
    def recieve(self, newMode, option = eventconsts.SYSTEM_EXTENDED):
        print("recieved value")
        # Set all
        if option == eventconsts.SYSTEM_EXTENDED:
            # Process variables for previous states
            self.prev_extendedMode = self.extendedMode
            self.prev_inControl_Knobs = config.START_IN_INCONTROL_KNOBS    # Set to default because otherwise 
            self.prev_inControl_Faders = config.START_IN_INCONTROL_FADERS  # they'll revert badly sometimes
            self.prev_inControl_Pads = config.START_IN_INCONTROL_PADS      #
            if newMode is True:
                self.extendedMode = True
                self.inControl_Knobs = True
                self.inControl_Faders = True
                self.inControl_Pads = True
            elif newMode is False:
                self.extendedMode = False
                self.inControl_Knobs = False
                self.inControl_Faders = False
                self.inControl_Pads = False
            else: logError("New mode mode not boolean")
        
        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            self.prev_inControl_Knobs = self.inControl_Knobs
            if newMode is True:
                self.inControl_Knobs = True
            elif newMode is False:
                self.inControl_Knobs = False
            else: logError("New mode mode not boolean")
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            self.prev_inControl_Faders = self.inControl_Faders
            if newMode is True:
                self.inControl_Faders = True
            elif newMode is False:
                self.inControl_Faders = False
            else: logError("New mode mode not boolean")
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            self.prev_inControl_Pads = self.inControl_Pads
            if newMode is True:
                self.inControl_Pads = True
            elif newMode is False:
                self.inControl_Pads = False
            else: logError("New mode mode not boolean")


extendedMode = extended()

# Compares revieved event to previous
def compareEvent(event):
    if toMidiMessage(event.status, event.data1, event.data2) is previous_event_out: return True
    else: return False

EventNameT = ['Note Off', 'Note On ', 'Key Aftertouch', 'Control Change','Program Change',  'Channel Aftertouch', 'Pitch Bend', 'System Message' ]

# Sends message to the default MIDI out device
def sendMidiMessage(status, data1, data2):
    global previous_event_out
    previous_event_out  = toMidiMessage(status, data1, data2)
    if PORT == config.DEVICE_PORT_EXTENDED:
        device.midiOutMsg(previous_event_out)
    else:
        device.dispatch(0, previous_event_out)

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

class padMgr:
    # Contains whether or not a pad is down (for use in extended mode)
    padsDown = [
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False],
        [False, False]
    ]

    def press(self, x, y):
        self.padsDown[x][y] = True
    
    def lift(self, x, y):
        self.padsDown[x][y] = False

    def getVal(self, x, y):
        return self.padsDown[x][y]

pads = padMgr()

class shiftMgr:
    is_down = False
    used = False

    def press(self):
        self.is_down = True
        self.used = False
    
    def lift(self):
        self.is_down = False
        return self.used

    def use(self):
        if self.is_down:
            self.used = True
            return True
        else: return False

    def getDown(self):
        return self.is_down
    
    def getUsed(self):
        if self.is_down:
            return self.used
        else: return "ERROR Shift not down"

shift = shiftMgr()

class beatMgr:
    beat = 0
    
    def set(self, beat):
        self.beat = beat
        self.redraw(lighting.state)

    def redraw(self, lights):
        if transport.getLoopMode():
            bar_col = lighting.BEAT_SONG_BAR
            beat_col = lighting.BEAT_SONG_BEAT
        else:
            bar_col = lighting.BEAT_PAT_BAR
            beat_col = lighting.BEAT_PAT_BEAT


        if self.beat is 1: lights.setPadColour(8, 0, bar_col)                # Bar
        elif self.beat is 2: lights.setPadColour(8, 0, beat_col)             # Beat
        elif self.beat is 0: lights.setPadColour(8, 0, lighting.COLOUR_OFF)  # Off

beat = beatMgr()



