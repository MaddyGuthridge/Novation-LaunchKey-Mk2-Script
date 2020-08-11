"""
internal > state.py

Contains variables and objects to manage the state of the script.

Author: Miguel Guthridge
"""

import device
import ui
import general

from .logging import getLineBreak, debugLog
from .notemanager import noteMode

import config
import internalconstants
# import updatecheck # Currently modules are unavailable
import lighting
import lightingconsts
import eventconsts

DEVICE_TYPE = internalconstants.DEVICE_NOT_SET

PORT = -1 # Set in initialisation function then left constant

SHARED_INIT_STATE = internalconstants.INIT_INCOMPLETE

def getPortExtended():
    return PORT == config.DEVICE_PORT_EXTENDED

def getVersionStr():
    """Returns Script version as a string

    Returns:
        str: Version number
    """
    return str(internalconstants.SCRIPT_VERSION_MAJOR) + '.' + str(internalconstants.SCRIPT_VERSION_MINOR) + '.' + str(internalconstants.SCRIPT_VERSION_REVISION)

def sharedInit():
    """Performs initialisation actions common to both scripts
    """
    global PORT
    global SHARED_INIT_STATE

    SHARED_INIT_STATE = internalconstants.INIT_OK

    PORT = device.getPortNumber()

    sendUniversalDeviceEnquiry()

    print(getLineBreak())

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

    def setVal(self, newMode, option = eventconsts.SYSTEM_EXTENDED, force=False, from_internal = True):
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
            if newMode is True:
                sendMidiMessage(0x9F, 0x0C, 0x7F)
            elif newMode is False:
                sendMidiMessage(0x9F, 0x0C, 0x00)
        
        # On 25-key model, link the fader to the knobs
        elif DEVICE_TYPE == internalconstants.DEVICE_KEYS_25 and (option == eventconsts.INCONTROL_FADERS or option == eventconsts.INCONTROL_KNOBS):
            if newMode is True:
                sendMidiMessage(0x9F, 0x0D, 0x7F)
            elif newMode is False:
                sendMidiMessage(0x9F, 0x0D, 0x00)
        
        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            if newMode is True:
                sendMidiMessage(0x9F, 0x0D, 0x7F)
            elif newMode is False:
                sendMidiMessage(0x9F, 0x0D, 0x00)
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            if newMode is True:
                sendMidiMessage(0x9F, 0x0E, 0x7F)
            elif newMode is False:
                sendMidiMessage(0x9F, 0x0E, 0x00)
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            if newMode is True:
                sendMidiMessage(0x9F, 0x0F, 0x7F)
            elif newMode is False:
                sendMidiMessage(0x9F, 0x0F, 0x00)

        if force:
            self.recieve(newMode, option)

    def recieve(self, newMode, option = eventconsts.SYSTEM_EXTENDED):
        """Processes extended mode switches received from the device

        Args:
            newMode (bool): new extended mode
            option (eventID, optional): Control set ID. Defaults to eventconsts.SYSTEM_EXTENDED.
        """
        if self.ignore_all:
            return
        
        # Set all
        if option == eventconsts.SYSTEM_EXTENDED:
            # Process variables for previous states
            self.prev_extendedMode.append(self.extendedMode)
            self.prev_inControl_Knobs = [config.START_IN_INCONTROL_KNOBS]    # Set to default because otherwise 
            self.prev_inControl_Faders = [config.START_IN_INCONTROL_FADERS]  # they'll revert badly sometimes
            self.prev_inControl_Pads = [config.START_IN_INCONTROL_PADS]      #
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

        # On 25-key model, link the fader to the knobs
        elif DEVICE_TYPE == internalconstants.DEVICE_KEYS_25 and (option == eventconsts.INCONTROL_FADERS or option == eventconsts.INCONTROL_KNOBS):
            self.prev_inControl_Knobs.append(self.inControl_Knobs)
            if newMode is True:
                self.inControl_Knobs = True
            elif newMode is False:
                self.inControl_Knobs = False
                
            self.prev_inControl_Faders.append(self.inControl_Faders)
            if newMode is True:
                self.inControl_Faders = True
            elif newMode is False:
                self.inControl_Faders = False

        # Set knobs
        elif option == eventconsts.INCONTROL_KNOBS:
            self.prev_inControl_Knobs.append(self.inControl_Knobs)
            if newMode is True:
                self.inControl_Knobs = True
            elif newMode is False:
                self.inControl_Knobs = False
            else: debugLog("New mode mode not boolean")
        
        # Set faders
        elif option == eventconsts.INCONTROL_FADERS:
            self.prev_inControl_Faders.append(self.inControl_Faders)
            if newMode is True:
                self.inControl_Faders = True
            elif newMode is False:
                self.inControl_Faders = False
            else: debugLog("New mode mode not boolean")
        
        # Set pads
        elif option == eventconsts.INCONTROL_PADS:
            self.prev_inControl_Pads.append(self.inControl_Pads)
            window.resetAnimationTick()
            if newMode is True:
                self.inControl_Pads = True
            elif newMode is False:
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


class ErrorState:
    """Manages state of device (whether it has encountered an error or not)

    Raises:
        e: Any exception triggered by anything
    """
    error = False

    def triggerError(self, e):
        """Triggers an error state

        Args:
            e (Exception): An exception object

        Raises:
            e: That same exception
        """
        self.error = True

        # Set other script into error state too
        sendCompleteInternalMidiMessage(internalconstants.MESSAGE_ERROR_CRASH)

        noteMode.setState(internalconstants.NOTE_STATE_ERROR)

        if PORT == config.DEVICE_PORT_EXTENDED:
            # Force remove from in-control mode
            extendedMode.forceEnd()

            # Set pad lights
            lightMap = lighting.LightMap()
            lightMap.setFromMatrix(lightingconsts.ERROR_COLOURS, 2)
            lighting.state.setFromMap(lightMap)

        # Print error message
        print("")
        print("")
        print(getLineBreak())
        print(getLineBreak())
        print("Unfortunately, an error occurred, and the script has crashed.")
        print("Please save a copy of this output to a text file, and create an issue on the project's GitHub page:")
        print("          " + internalconstants.SCRIPT_URL)
        print("Then, please restart both scripts by clicking `Reload script` in the Script output window.")
        print(getLineBreak())
        print(getLineBreak())
        print("")
        print("")

        if config.DEBUG_HARD_CRASHING:
            raise e

    def triggerErrorFromOtherScript(self):
        """Sets the device into an error state when an error was encoutered on the other script.
        """
        self.error = True

        noteMode.setState(internalconstants.NOTE_STATE_ERROR)

        if PORT == config.DEVICE_PORT_EXTENDED:
            # Force remove from in-control mode
            extendedMode.forceEnd()

            # Set pad lights
            lightMap = lighting.LightMap()
            lightMap.setFromMatrix(lightingconsts.ERROR_COLOURS, 2)
            lighting.state.setFromMap(lightMap)

        # Print error message
        print("")
        print("")
        print(getLineBreak())
        print(getLineBreak())
        print("Unfortunately, an error occurred, and the script has crashed.")
        print("Please refer to the other script output for the error info and instructions to report the error, ", end="")
        print("then restart both scripts by clicking `Reload script` in the Script output window.")
        print(getLineBreak())
        print(getLineBreak())
        print("")
        print("")

    def getError(self):
        """Gets whether the script is in an error state

        Returns:
            bool: error state
        """
        return self.error

    def redrawError(self, lights):
        """Redraws lights to make them all error colours

        Args:
            lights (LightMap): Object containining lighting state during redraw
        """
        lights.setFromMatrix(lightingconsts.ERROR_COLOURS)
        lights.setPadColour(8, 1, lightingconsts.colours["ORANGE"])
        lights.solidifyAll()

    def recoverError(self, received=False):
        self.error = False
        if not received:
            sendCompleteInternalMidiMessage(internalconstants.MESSAGE_ERROR_RECOVER)
        
        if getPortExtended():
            extendedMode.ignore_all = False
            extendedMode.setVal(True)
            
        noteMode.setState(internalconstants.NOTE_STATE_NORMAL)
        
        #config.DEBUG_HARD_CRASHING = True
            
        print(getLineBreak())
        print("Error ignored")
        print(getLineBreak())
    
    def eventProcessError(self, command):
        """Handles extended mode events when in an error state

        Args:
            command (ProcessedEvent): An event
        """
        command.handle("Device in error state")
    
errors = ErrorState()


from .messages import sendUniversalDeviceEnquiry, sendCompleteInternalMidiMessage, sendMidiMessage

from .windowstate import window

from .misc import beat