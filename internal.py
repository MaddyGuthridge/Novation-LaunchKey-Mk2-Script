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
import internalconstants
import eventprocessor
import lighting
# import updatecheck # Currently modules are unavailable

import WindowProcessors.processwindows as processwindows
import PluginProcessors.processplugins as processplugins

DEVICE_TYPE = internalconstants.DEVICE_NOT_SET

PORT = -1 # Set in initialisation function then left constant

SHARED_INIT_STATE = internalconstants.INIT_INCOMPLETE

def processSysEx(event):
    print(event.sysex)

def sendUniversalDeviceEnquiry():
    device.midiOutSysex(internalconstants.DEVICE_ENQUIRY_MESSAGE)

def getVersionStr():
    return str(internalconstants.SCRIPT_VERSION_MAJOR) + '.' + str(internalconstants.SCRIPT_VERSION_MINOR) + '.' + str(internalconstants.SCRIPT_VERSION_REVISION)

def sharedInit():
    global PORT
    global SHARED_INIT_STATE

    SHARED_INIT_STATE = internalconstants.INIT_OK

    PORT = device.getPortNumber()

    sendUniversalDeviceEnquiry()

    printLineBreak()

    print(internalconstants.SCRIPT_NAME + " - Version: " + getVersionStr())
    print(" - " + internalconstants.SCRIPT_AUTHOR)
    print("")
    print("Running in FL Studio Version: " + ui.getVersion())


    # Check for script updates - UNCOMMENT THIS WHEN MODULES ADDED
    """
    if updatecheck.check():
        SHARED_INIT_STATE = internalconstants.INIT_UPDATE_AVAILABLE
        printLineBreak()
        print("An update to this script is available!")
        print("Follow this link to download it: " + internalconstants.SCRIPT_URL)
        printLineBreak()
    """
    
    if PORT != config.DEVICE_PORT_BASIC and PORT != config.DEVICE_PORT_EXTENDED:
        print("It appears that the device ports are not configured correctly. Please edit config.py to rectify this.")
        SHARED_INIT_STATE = internalconstants.INIT_PORT_MISMATCH

    # Check FL Scripting version
    midi_script_version = general.getVersion()
    print("FL Studio Scripting version: " + str(midi_script_version) + ". Minimum recommended version: " + str(internalconstants.MIN_FL_SCRIPT_VERSION))
    # Outdated FL version
    if midi_script_version < internalconstants.MIN_FL_SCRIPT_VERSION:
        print("You may encounter issues using this script. Consider updating to the latest version FL Studio.")
        SHARED_INIT_STATE = internalconstants.INIT_API_OUTDATED

    # Check debug mode
    if config.CONSOLE_DEBUG_MODE != []:
        print("Advanced debugging is enabled:", config.CONSOLE_DEBUG_MODE)
    print("")

    beat.refresh() # Update beat indicator

def refreshProcessor():
    beat.refresh()

# Called on idle
def idleProcessor():
    # Start performance timer
    idleClock.start()

    # Increment animation tick
    window.incr_animation_tick()

    # Update active window
    window.update()

    # Stop performance timer
    idleClock.stop()

# Prints a line break
def printLineBreak():
    print("————————————————————————————————————————————————————")

# Returns string with tab characters at the end
def newGetTab(string, multiplier = 1, length = config.TAB_LENGTH):
    string += " "
    toAdd = (length * multiplier) - len(string) % (length * multiplier)

    for x in range(toAdd):
        string += " "
    return string

# Counts processing time
class performanceMonitor:
    def __init__(self, monitor_name, debug_level):

        self.name = monitor_name
        self.debug_level = debug_level

        self.total_time = 0
        self.startTime = -1
        self.endTime = -1
        self.num_events = 0
    
    def start(self):
        self.startTime = time.perf_counter()
    
    def stop(self):
        self.endTime = time.perf_counter()
        process_time = self.endTime - self.startTime
        self.total_time += process_time
        self.num_events += 1
        if self.debug_level in config.CONSOLE_DEBUG_MODE:
            printLineBreak()
            print(self.name)
            print("Processed in:", round(process_time, 4), "seconds")
            print("Average processing time:", round(self.total() / self.num_events, 4), "seconds")
            printLineBreak()
        return process_time
    
    def total(self):
        return self.total_time
eventClock = performanceMonitor("Event Processor", internalconstants.DEBUG_PROCESSOR_PERFORMANCE)
idleClock = performanceMonitor("Idle Processor", internalconstants.DEBUG_IDLE_PERFORMANCE)


# Manages active window - CURRENTLY BROKEN!!!!
class windowMgr:
    def __init__(self):
        self.plugin_focused = False
        self.previous_plugin = ""
        self.active_plugin = ""
        self.active_fl_window = -1
        self.animation_tick_number = 0
    
    # Reset tick number to zero
    def reset_animation_tick(self):
        self.animation_tick_number = 0

    # Called on idle to increase tick number
    def incr_animation_tick(self):
        self.animation_tick_number += 1

    # Get number of ticks since window update
    def get_animation_tick(self):
        return self.animation_tick_number

    # Update active window
    def update(self):
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
            if new_plugin == internalconstants.WINDOW_COLOUR_PICKER or new_plugin == internalconstants.WINDOW_SCRIPT_OUTPUT:
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

    # Revert to previous plugin
    def revertPlugin(self):
        self.active_plugin = self.previous_plugin
        self.previous_plugin = ""

window = windowMgr()

# Gets string for FL Window
def get_fl_window_string(index):
    if index == -1: return "NONE"
    if index == internalconstants.WINDOW_MIXER: return "Mixer"
    if index == internalconstants.WINDOW_PLAYLIST: return "Playlist"
    if index == internalconstants.WINDOW_CHANNEL_RACK: return "Channel Rack"
    if index == internalconstants.WINDOW_PIANO_ROLL: return "Piano Roll"
    if index == internalconstants.WINDOW_BROWSER: return "Browser"

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
            else: debugLog("New mode mode not boolean")

            

        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            
            if self.prev_inControl_Knobs is True:
                self.setVal(True, eventconsts.INCONTROL_KNOBS)
            elif self.prev_inControl_Knobs is False:
                self.setVal(False, eventconsts.INCONTROL_KNOBS)
            else: debugLog("New mode mode not boolean")
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            if self.prev_inControl_Faders is True:
                self.setVal(True, eventconsts.INCONTROL_FADERS)
            elif self.prev_inControl_Faders is False:
                self.setVal(False, eventconsts.INCONTROL_FADERS)
            else: debugLog("New mode mode not boolean")
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
           
            if self.prev_inControl_Pads is True:
                self.setVal(True, eventconsts.INCONTROL_PADS)
            elif self.prev_inControl_Pads is False:
                self.setVal(False, eventconsts.INCONTROL_PADS)
            else: debugLog("New mode mode not boolean")


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
            else: debugLog("New mode mode not boolean")
            lighting.state.reset()

        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            self.prev_inControl_Knobs = self.inControl_Knobs
            if newMode is True:
                self.inControl_Knobs = True
            elif newMode is False:
                self.inControl_Knobs = False
            else: debugLog("New mode mode not boolean")
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            self.prev_inControl_Faders = self.inControl_Faders
            if newMode is True:
                self.inControl_Faders = True
            elif newMode is False:
                self.inControl_Faders = False
            else: debugLog("New mode mode not boolean")
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            self.prev_inControl_Pads = self.inControl_Pads
            window.reset_animation_tick()
            if newMode is True:
                self.inControl_Pads = True
            elif newMode is False:
                self.inControl_Pads = False
            else: debugLog("New mode mode not boolean")
            lighting.state.reset()

extendedMode = extended()

""" Unneeded code - delete soon
# Compares revieved event to previous
def compareEvent(event):
    if toMidiMessage(event.status, event.data1, event.data2) is previous_event_out: return True
    else: return False

EventNameT = ['Note Off', 'Note On ', 'Key Aftertouch', 'Control Change','Program Change',  'Channel Aftertouch', 'Pitch Bend', 'System Message' ]
"""

# Sends message to the default MIDI out device
def sendMidiMessage(status, data1, data2):
    event_out  = toMidiMessage(status, data1, data2)
    str_event_out = str(status) + " " + str(data1) + " " + str(data2)
    if PORT == config.DEVICE_PORT_EXTENDED:
        debugLog("Dispatched external MIDI message " + str_event_out, internalconstants.DEBUG_DISPATCH_EVENT)
        device.midiOutMsg(event_out)
    else:
        debugLog("Dispatched internal MIDI message" + str_event_out, internalconstants.DEBUG_DISPATCH_EVENT)
        device.dispatch(0, event_out)

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

# Print out error message
def debugLog(message, level = 0):
    if level in config.CONSOLE_DEBUG_MODE or level == internalconstants.DEBUG_ERROR:
        print(message)

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
    sticky = False

    def press(self):
        self.is_down = True
        self.used = False
        window.reset_animation_tick()
    
    def lift(self):
        self.is_down = False
        window.reset_animation_tick()
        return self.used

    def use(self):
        if self.is_down:
            self.used = True
            return True
        else: return False

    # Sets shift key to be down until pressed again
    def set_sticky(self):
        self.press()
        self.sticky = True

    def use_sticky(self):
        self.lift()
        self.sticky = False

    def get_sticky(self):
        return self.sticky

    def getDown(self):
        return self.is_down
    
    def getUsed(self):
        if self.is_down:
            return self.used
        else: return "ERROR Shift not down"

shift = shiftMgr()

class beatMgr:
    beat = 0

    is_tapping_tempo = False
    
    metronome_enabled = False

    def refresh(self):
        self.metronome_enabled = (general.getUseMetronome() == 1)

    # Toggle state of metronome
    def toggle_metronome(self):
        transport.globalTransport(eventconsts.midi.FPT_Metronome, True)
        self.metronome_enabled = (general.getUseMetronome() == 1)
        return self.metronome_enabled

    def toggle_tempo_tap(self):
        self.is_tapping_tempo = not self.is_tapping_tempo
        return self.is_tapping_tempo

    def tap_tempo(self):
        transport.globalTransport(eventconsts.midi.FPT_TapTempo, True)

    # Set current beat
    def set_beat(self, beat):
        self.beat = beat
        self.redraw(lighting.state)

    # Redraw lights
    def redraw(self, lights):

        if self.is_tapping_tempo:
            lights.setPadColour(8, 0, lighting.TEMPO_TAP)
        
        if transport.getLoopMode():
            bar_col = lighting.BEAT_SONG_BAR
            beat_col = lighting.BEAT_SONG_BEAT
        else:
            bar_col = lighting.BEAT_PAT_BAR
            beat_col = lighting.BEAT_PAT_BEAT

        if self.beat is 1: lights.setPadColour(8, 0, bar_col)     # Bar
        elif self.beat is 2: lights.setPadColour(8, 0, beat_col)  # Beat

        if self.metronome_enabled:
            lights.setPadColour(8, 0, lighting.METRONOME)

beat = beatMgr()



