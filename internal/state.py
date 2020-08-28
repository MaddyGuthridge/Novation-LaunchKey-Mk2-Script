"""
internal > state.py

Contains variables and objects to manage the state of the script.

Author: Miguel Guthridge
"""

import math

import device
import ui
import general

from .logging import getLineBreak, debugLog
from .notemanager import noteMode

import config
from . import consts
from .snap import snap
# import .updatecheck # Currently modules are unavailable
import lighting
import lightingconsts
import eventconsts

DEVICE_TYPE = consts.DEVICE_NOT_SET

PORT = -1 # Set in initialisation function then left constant

SHARED_INIT_STATE = consts.INIT_INCOMPLETE


class PitchBendMgr:
    """Maintains state of pitch bend wheel in basic mode script.
    Note that pitch bend events aren't forwarded to the extended mode script so this will be useless there.
    """
    value = 64
    direction = 0
    def setVal(self, new_value):
        """Update current pitch bend value

        Args:
            new_value (int): Midi data value
        """
        if self.value < new_value:
            self.direction = 1
        elif self.value > new_value:
            self.direction = -1
        else:
            self.direction = 0
        self.value = new_value
    
    def getVal(self):
        """Return current pitch bend value

        Returns:
            int: Midi data value
        """
        return self.value
    
    def getParsedVal(self):
        """Return current pitch bend value adjusted so that centre is zero

        Returns:
            int: Data value adjusted
        """
        return self.value - 64

    def getDirection(self):
        """Returns direction that pitch bend wheel is moving

        Returns:
            int: 0 for stationary, 1 for increasing, -1 for decreasing
        """
        return self.direction

pitchBend = PitchBendMgr()

def idleShift():
    """Controls pitchbend wheel navigation
    """
    
    pitch_val = -pitchBend.getParsedVal()
    
    if pitch_val == 0:
        multiplier = 0
    elif pitch_val > 0:
        multiplier = 1
    elif pitch_val < 0:
        multiplier = -1
    
    send_float = abs(pitch_val) * config.PITCH_BEND_JOG_SPEED
    
    if not window.getAbsoluteTick() % abs(65 - pitch_val):
        send_val = math.ceil(send_float)
    else:
        send_val = math.floor(send_float)
    
    ui.jog(multiplier * send_val)


def getPortExtended():
    """Get whether the current script is running on the extended port

    Returns:
        bool: Whether the script is the extended port script
    """
    return PORT == config.DEVICE_PORT_EXTENDED

def getVersionStr():
    """Returns Script version as a string

    Returns:
        str: Version number
    """
    return str(consts.SCRIPT_VERSION_MAJOR) + '.' + str(consts.SCRIPT_VERSION_MINOR) + '.' + str(consts.SCRIPT_VERSION_REVISION)

def sharedInit():
    """Performs initialisation actions common to both scripts
    """
    global PORT
    global SHARED_INIT_STATE

    SHARED_INIT_STATE = consts.INIT_OK

    # Refresh snap mode
    snap.refresh()

    PORT = device.getPortNumber()

    sendUniversalDeviceEnquiry()
    
    sendCompleteInternalMidiMessage(consts.MESSAGE_RESTART_DEVICE)

    print(getLineBreak())

    print(consts.SCRIPT_NAME + " - Version: " + getVersionStr() + " " + consts.SCRIPT_VERSION_SUFFIX)
    print(" - " + consts.SCRIPT_AUTHOR)
    print("")
    print("Running in FL Studio Version: " + ui.getVersion())


    # Check for script updates - UNCOMMENT THIS WHEN MODULES ADDED
    """
    if updatecheck.check():
        SHARED_INIT_STATE = consts.INIT_UPDATE_AVAILABLE
        printLineBreak()
        print("An update to this script is available!")
        print("Follow this link to download it: " + consts.SCRIPT_URL)
        printLineBreak()
    """
    
    if PORT != config.DEVICE_PORT_BASIC and PORT != config.DEVICE_PORT_EXTENDED:
        print("It appears that the device ports are not configured correctly. Please edit config.py to rectify this.")
        SHARED_INIT_STATE = consts.INIT_PORT_MISMATCH

    # Check FL Scripting version
    midi_script_version = general.getVersion()
    print("FL Studio Scripting version: " + str(midi_script_version) + ". Minimum recommended version: " + str(consts.MIN_FL_SCRIPT_VERSION))
    # Outdated FL version
    if midi_script_version < consts.MIN_FL_SCRIPT_VERSION:
        print("You may encounter issues using this script. Consider updating to the latest version FL Studio.")
        SHARED_INIT_STATE = consts.INIT_API_OUTDATED

    # Check debug mode
    if config.CONSOLE_DEBUG_MODE != []:
        print("Advanced debugging is enabled:", config.CONSOLE_DEBUG_MODE)
    print("")

    beat.refresh() # Update beat indicator


class ExtendedMgr:
    """Handles extended mode states
    """
    def __init__(self):
        self.ignore_all = False

        self.extendedMode = False
        self.inControl_Knobs = False
        self.inControl_Faders = False
        self.inControl_Pads = False

        self.prev_extendedMode = [False]
        self.prev_inControl_Knobs = [False]
        self.prev_inControl_Faders = [False]
        self.prev_inControl_Pads = [False]

    def query(self, option = eventconsts.SYSTEM_EXTENDED):
        """Queries whether extended mode is active for a control set (system, pads, knobs, faders)

        Args:
            option (eventID, optional): Control Set ID - can be:
                 - SYSTEM_EXTENDED
                 - INCONTROL_FADERS
                 - INCONTROL_KNOBS
                 - INCONTROL_PADS
                Defaults to eventconsts.SYSTEM_EXTENDED.

        Returns:
            bool: Current extended mode
        """
        if option == eventconsts.SYSTEM_EXTENDED: return self.extendedMode
        elif option == eventconsts.INCONTROL_KNOBS: return self.inControl_Knobs
        elif option == eventconsts.INCONTROL_FADERS: return self.inControl_Faders
        elif option == eventconsts.INCONTROL_PADS: return self.inControl_Pads

    def revert(self, option = eventconsts.SYSTEM_EXTENDED):
        """Reverts to previous extended mode

        Args:
            option (eventID, optional): Control set ID. Defaults to eventconsts.SYSTEM_EXTENDED.
        """
        if self.ignore_all:
            return
        
        if not config.AUTO_SET_INCONTROL_MODE:
            return
        
        # Set all
        if option == eventconsts.SYSTEM_EXTENDED:
            self.setVal(self.prev_extendedMode.pop())
            if len(self.prev_extendedMode) == 0:
                self.prev_extendedMode.append(False)

            

        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            self.setVal(self.prev_inControl_Knobs.pop(), eventconsts.INCONTROL_KNOBS)
            if len(self.prev_inControl_Knobs) == 0:
                self.prev_inControl_Knobs.append(config.START_IN_INCONTROL_KNOBS)
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            self.setVal(self.prev_inControl_Faders.pop(), eventconsts.INCONTROL_FADERS)
            if len(self.prev_inControl_Faders) == 0:
                self.prev_inControl_Faders.append(config.START_IN_INCONTROL_FADERS)
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            self.setVal(self.prev_inControl_Pads.pop(), eventconsts.INCONTROL_PADS)
            if len(self.prev_inControl_Pads) == 0:
                self.prev_inControl_Pads.append(config.START_IN_INCONTROL_PADS)

    def setVal(self, new_mode, option = eventconsts.SYSTEM_EXTENDED, force=False, from_internal = True):
        """Set inControl modes on the controller

        Args:
            newMode (bool): new mode
            option (eventID, optional): control set ID. Defaults to eventconsts.SYSTEM_EXTENDED.
            force (bool, optional): whether the value should be assumed to have been received successfully by the controller. Defaults to False.
            from_internal (bool, optional): 
                Whether the inControl change was triggered by the script or whether it was caused by initialisation/hardware changes. 
                Defaults to True.
        """
        if self.ignore_all and not force:
            return
        
        if (not config.AUTO_SET_INCONTROL_MODE) and from_internal and not force:
            return
        
        # Set all
        if option == eventconsts.SYSTEM_EXTENDED:
            if new_mode is True:
                sendMidiMessage(0x9F, 0x0C, 0x7F)
            elif new_mode is False:
                sendMidiMessage(0x9F, 0x0C, 0x00)
        
        # On 25-key model, link the fader to the knobs
        elif DEVICE_TYPE == consts.DEVICE_KEYS_25 and (option == eventconsts.INCONTROL_FADERS or option == eventconsts.INCONTROL_KNOBS):
            if new_mode is True:
                sendMidiMessage(0x9F, 0x0D, 0x7F)
            elif new_mode is False:
                sendMidiMessage(0x9F, 0x0D, 0x00)
        
        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            if new_mode is True:
                sendMidiMessage(0x9F, 0x0D, 0x7F)
            elif new_mode is False:
                sendMidiMessage(0x9F, 0x0D, 0x00)
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            if new_mode is True:
                sendMidiMessage(0x9F, 0x0E, 0x7F)
            elif new_mode is False:
                sendMidiMessage(0x9F, 0x0E, 0x00)
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            if new_mode is True:
                sendMidiMessage(0x9F, 0x0F, 0x7F)
            elif new_mode is False:
                sendMidiMessage(0x9F, 0x0F, 0x00)

        if force:
            self.recieve(new_mode, option)

    def recieve(self, new_mode, option = eventconsts.SYSTEM_EXTENDED):
        """Processes extended mode switches received from the device

        Args:
            newMode (bool): new extended mode
            option (eventID, optional): Control set ID. Defaults to eventconsts.SYSTEM_EXTENDED.
        """
        #if self.ignore_all:
        #    return
        
        # Set all
        if option == eventconsts.SYSTEM_EXTENDED:
            # Process variables for previous states
            self.prev_extendedMode.append(self.extendedMode)
            self.prev_inControl_Knobs = [config.START_IN_INCONTROL_KNOBS]    # Set to default because otherwise 
            self.prev_inControl_Faders = [config.START_IN_INCONTROL_FADERS]  # they'll revert badly sometimes
            self.prev_inControl_Pads = [config.START_IN_INCONTROL_PADS]      #
            if new_mode is True:
                self.extendedMode = True
                self.inControl_Knobs = True
                self.inControl_Faders = True
                self.inControl_Pads = True
            elif new_mode is False:
                self.extendedMode = False
                self.inControl_Knobs = False
                self.inControl_Faders = False
                self.inControl_Pads = False
            else: debugLog("New mode mode not boolean")
            lighting.state.reset()

        # On 25-key model, link the fader to the knobs
        elif DEVICE_TYPE == consts.DEVICE_KEYS_25 and (option == eventconsts.INCONTROL_FADERS or option == eventconsts.INCONTROL_KNOBS):
            self.prev_inControl_Knobs.append(self.inControl_Knobs)
            if new_mode is True:
                self.inControl_Knobs = True
            elif new_mode is False:
                self.inControl_Knobs = False
                
            self.prev_inControl_Faders.append(self.inControl_Faders)
            if new_mode is True:
                self.inControl_Faders = True
            elif new_mode is False:
                self.inControl_Faders = False

        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            self.prev_inControl_Knobs.append(self.inControl_Knobs)
            if new_mode is True:
                self.inControl_Knobs = True
            elif new_mode is False:
                self.inControl_Knobs = False
            else: debugLog("New mode mode not boolean")
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            self.prev_inControl_Faders.append(self.inControl_Faders)
            if new_mode is True:
                self.inControl_Faders = True
            elif new_mode is False:
                self.inControl_Faders = False
            else: debugLog("New mode mode not boolean")
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            self.prev_inControl_Pads.append(self.inControl_Pads)
            window.resetAnimationTick()
            if new_mode is True:
                self.inControl_Pads = True
            elif new_mode is False:
                self.inControl_Pads = False
            else: debugLog("New mode mode not boolean")
            lighting.state.reset()

    def forceEnd(self):
        """Force the controller out of extended mode and prevent all further changes. Use only in emergencies.
        """
        self.setVal(False)
        self.recieve(False)
        self.ignore_all = True
        
extendedMode = ExtendedMgr()

def setDefaultExtended():
    extendedMode.setVal(config.START_IN_INCONTROL_KNOBS, eventconsts.INCONTROL_KNOBS, from_internal=False) 
    extendedMode.setVal(config.START_IN_INCONTROL_FADERS, eventconsts.INCONTROL_FADERS, from_internal=False) 
    extendedMode.setVal(config.START_IN_INCONTROL_PADS, eventconsts.INCONTROL_PADS, from_internal=False) 

class ErrorState:
    """Manages state of device (whether it has encountered an error or not)

    Raises:
        e: Any exception triggered by anything
    """
    error = False
    from_other = False
    error_count = 0

    def triggerError(self, e):
        """Triggers an error state

        Args:
            e (Exception): An exception object

        Raises:
            e: That same exception
        """
        self.error = True
        self.error_count += 1

        # Set other script into error state too
        sendCompleteInternalMidiMessage(consts.MESSAGE_ERROR_CRASH)

        noteMode.setState(consts.NOTE_STATE_ERROR)

        if PORT == config.DEVICE_PORT_EXTENDED:
            try:
                if config.DEBUG_HARD_CRASHING:
                    # Force remove from in-control mode
                    extendedMode.forceEnd()

                # Set pad lights
                lightMap = lighting.LightMap()
                lightMap.setFromMatrix(lightingconsts.ERROR_COLOURS, 2)
                lighting.state.setFromMap(lightMap)
            except:
                pass

        # Print error message
        self.printError(False, e.args)

        if config.DEBUG_HARD_CRASHING:
            raise e

    def triggerErrorFromOtherScript(self):
        """Sets the device into an error state when an error was encoutered on the other script.
        """
        self.error = True
        self.from_other = True

        noteMode.setState(consts.NOTE_STATE_ERROR)

        if PORT == config.DEVICE_PORT_EXTENDED:
            try:
                # Force remove from in-control mode
                extendedMode.forceEnd()

                # Set pad lights
                lightMap = lighting.LightMap()
                lightMap.setFromMatrix(lightingconsts.ERROR_COLOURS, 2)
                lighting.state.setFromMap(lightMap)
            except:
                pass
            
        self.printError(True)

    def getError(self):
        """Gets whether the script is in an error state

        Returns:
            bool: error state
        """
        return self.error

    def getFromOther(self):
        return self.from_other

    def redrawError(self, lights):
        """Redraws lights to make them all error colours

        Args:
            lights (LightMap): Object containining lighting state during redraw
        """
        lights.setFromMatrix(lightingconsts.ERROR_COLOURS)
        if not config.DEBUG_HARD_CRASHING:
            lights.setPadColour(8, 0, lightingconsts.colours["ORANGE"])
            lights.setPadColour(8, 1, lightingconsts.colours["GREEN"])
        lights.solidifyAll()

    def printError(self, fromOther, error=""):
        """Print an error message

        Args:
            fromOther (bool): whether the error occurred on the other script
            error (str, optional): The error message. Defaults to "".
        """
        print("")
        print("")
        print(getLineBreak())
        print(getLineBreak())
        print("Unfortunately, an error occurred, and the script has crashed.")
        if config.DEBUG_HARD_CRASHING:
            if fromOther:
                print("Please refer to the other script output for the error info and instructions to report the error, ", end="")
            else:
                print("Please save a copy of this output to a text file, and create an issue on the project's GitHub page:")
                print("          " + consts.SCRIPT_URL)
            print("then restart both scripts by clicking `Reload script` in the Script output window.")
        else:
            print("Please restart the script by pressing the green pad, or restart the script with debugging enabled ", end="")
            print("by pressing the orange pad. If possible, try to recreate the issue with debugging enabled.")
        if error != "":
            print(getLineBreak())
            print("Error code:", error)
        print(getLineBreak())
        print(getLineBreak())
        print("")
        print("")

    def recoverError(self, enter_debug, received=False):
        """Recover from an error

        Args:
            enter_debug (bool): Whether to enable debugging
            received (bool, optional): Whether the command was recieved from other port. Defaults to False.
        """
        self.error = False
        self.from_other = False
        
        if enter_debug:
            enterDebugMode()
        
        if not received:
            if enter_debug:
                sendCompleteInternalMidiMessage(consts.MESSAGE_ERROR_RECOVER_DEBUG)
            else:
                sendCompleteInternalMidiMessage(consts.MESSAGE_ERROR_RECOVER)
        
        if getPortExtended():
            extendedMode.ignore_all = False
            extendedMode.setVal(True)
            
        noteMode.setState(consts.NOTE_STATE_NORMAL)
        
        #config.DEBUG_HARD_CRASHING = True
            
        print(getLineBreak())
        print("Error ignored")
        print(getLineBreak())
    
    def eventProcessError(self, command):
        """Handles extended mode events when in an error state

        Args:
            command (ParsedEvent): An event
        """
        if config.DEBUG_HARD_CRASHING or getPortExtended():
            command.handle("Device in error state")
        
errors = ErrorState()

def enterDebugMode():
    """Put the script into debug mode
    """
    if not config.DEBUG_HARD_CRASHING:
        sendCompleteInternalMidiMessage(consts.MESSAGE_ENTER_DEBUG_MODE)
    config.DEBUG_HARD_CRASHING = True
    config.CONSOLE_DEBUG_MODE = consts.FORCE_DEBUG_MODES_LIST

def restartDevice():
    """Reset a bunch of components from the script
    """
    noteMode.setState(consts.NOTE_STATE_NORMAL)
    
    setDefaultExtended()
    
    if errors.getError():
        if not errors.getFromOther():
            sendCompleteInternalMidiMessage(consts.MESSAGE_ERROR_CRASH)
        else:
            errors.recoverError(False, True)

from .messages import sendUniversalDeviceEnquiry, sendCompleteInternalMidiMessage, sendMidiMessage

from .windowstate import window

from .misc import beat

from .notemanager import noteMode
