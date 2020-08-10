"""
lighting.py

This file contains functions and constants related to controlling lights on the controller.

Author: Miguel Guthridge
"""

IDLE_ANIMATION_SPEED = 1
IDLE_ANIMATION_STRETCH = 2
IDLE_ANIMATION_DO_TRAILS = True
IDLE_ANIMATION_TRAIL_SPEED_MODIFIER = 1
IDLE_ANIMATION_TRAIL_SPEED = 2
IDLE_ANIMATION_TRAIL_LENGTH = 6
IDLE_ANIMATION_TRAIL_INFREQUENCY = 37
IDLE_ANIMATION_TRAIL_Y_OFFSET = 13

import time

import internal
import eventconsts
import eventprocessor
import processorhelpers
import internalconstants
import config
import lightingconsts


class LightMap:
    """This object is sent through event processors to gather colours for UI redraws.
    """
    def __init__(self):
        """Create instance
        """
        self.reset()
    
      
    def reset(self):
        """Resets all lights to transparent
        """
        # 0 = unfrozen, 1 = frozen
        self.FrozenMap = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

        # 0 = off, 1-127 = colour
        self.PadColours = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

        # 0 = off, 1 = on, 2 = pulse, negative = flash
        self.PadStates = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]


    def setPadColour(self, x, y, colour, state = 3, override = False):
        """Sets the colour of a pad

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            colour (int): Colour (specified in lightingconsts)
            state (int, optional): Lighting mode. Defaults to 3.
                - 0 = off
                - 1 = on
                - 2 = pulse
                - negative = flashing with abs(state)
                - 3 = automatic
            override (bool, optional): Whether to override the current pad option. Defaults to False.

        Returns:
            bool: Whether the assignment was successful.
        """
        if self.FrozenMap[x][y] == 0 or override: # If pad available to map
            self.PadColours[x][y] = colour
            self.PadStates[x][y] = state
            if colour != -1:
                self.solidifyPad(x, y)
            return True
        else: return False
    
    
    def setFromMatrix(self, map, state=3, override = False):
        """Set pad lights from a 2x8 matrix

        Args:
            map (matrix): 2D list structure containing light settings
            state (int, optional): Lighting mode. Defaults to 3.
                - 0 = off
                - 1 = on
                - 2 = pulse
                - negative = flashing with abs(state)
                - 3 = automatic
            override (bool, optional): Whether to override the current pad option. Defaults to False.
        """
        for x in range(len(self.FrozenMap) - 1): # Don't modify round pads
            for y in range(len(self.FrozenMap[x])):
                if self.FrozenMap[x][y] == 0 or override:
                    self.setPadColour(x, y, map[x][y], state, override)
        return


    def solidifyPad(self, x, y):
        """Prevent a pad from being overwritten

        Args:
            x (int): X coordinate
            y (int): Y coordinate
        """
        if self.FrozenMap[x][y] == 0: # If pad available to map
            self.FrozenMap[x][y] = 1
    
    
    def solidifyRow(self, y):
        """Prevent a row of lights from being overwritten (not including round pads)

        Args:
            y (int): Y coordinate
        """
        for x in range(len(self.FrozenMap) - 1): # Don't solidify round pads
            if self.FrozenMap[x][y] == 0: self.FrozenMap[x][y] = 1
    
    
    def solidifyColumn(self, x):
        """Prevents a column from being overwritten

        Args:
            x (int): X coordinate
        """
        for y in range(len(self.FrozenMap)):
            if self.FrozenMap[x][y] == 0: self.FrozenMap[x][y] = 1

    # Prevents all pads from being overwritten
    def solidifyAll(self):
        """Prevents all pads from being overwritten (not including round pads). Call this at the end of your redraw functions 
        if you don't want other processors to possibly draw behind your UI.
        """
        for x in range(len(self.FrozenMap) - 1): # Don't solidify round pads
            for y in range(len(self.FrozenMap[x])):
                self.solidifyPad(x, y)


class Lights:
    """Manages the current state of lights.
    """
    def __init__(self):
        """Create instance.
        """
        # 0 = off, 1-127 = colour
        self.PadColours = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]

        # 0 = off, 1 = on, 2 = pulse, negative = flash
        self.PadStates = [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
            ]


    def reset(self):
        """Reset all lights to off
        """
        internal.sendMidiMessage(0xBF, 0x00, 0x00)
        internal.debugLog("Sent lighting reset signal", internalconstants.DEBUG_LIGHTING_RESET)
        internal.window.resetAnimationTick()
        self.__init__()


    def setPadColour(self, x, y, colour, state = 3, override = False):
        """Set the colour of a pad

        Args:
            x (int): X coordinate
            y (int): Y coordinate
            colour (int): Colour option
            state (int, optional): Light mode. Defaults to 3.
            override (bool, optional): Whether the event should be sent regardless of the 
                current state of that pad. Defaults to False.
        """
        if internal.window.getAbsoluteTick() % config.LIGHTS_FULL_REDRAW_FREQUENCY == 0:
            full_redraw = True
        else:
            full_redraw = False
            
        
        # Handle light offs
        if colour == 0 and state == 3:
            state = 0

        # Set legacy state
        elif state == 3:
            state = 1

        if state == 0:
            colour = 0

        # Check if pad is already in that state - don't bother with event if so
        if self.PadColours[x][y] == colour and self.PadStates[x][y] == state and not override and not full_redraw:
            return

        # Set state variables
        self.PadColours[x][y] = colour
        self.PadStates[x][y] = state

        status_a = 0x9
        status_b = 0xF

        if state == 0:
            status_a = 0x8

        elif state == 2:
            status_b = 0x2

        elif state < 0:
            status_b = 0xF

        # Round pads in basic mode
        if x == 8 and not internal.extendedMode.query(eventconsts.INCONTROL_PADS):
            status_a = 0xB

        # Calculate Status
        status = (status_a << 4) + status_b

        if internal.extendedMode.query(eventconsts.INCONTROL_PADS): 
            internal.sendMidiMessage(status, eventconsts.Pads[x][y], colour)
            internal.debugLog("Sent lighting command [" + str(x) + ", " + str(y) + "] (InControl Enabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
            
        else: 
            internal.sendMidiMessage(status, processorhelpers.convertPadMapping(eventconsts.Pads[x][y]), colour)
            internal.debugLog("Sent lighting command [" + str(x) + ", " + str(y) + "] (InControl Disabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
        
        if state < 0: # Send extra event to trigger flashing
            status_b = 0x1
            status = (status_a << 4) + status_b

            if internal.extendedMode.query(eventconsts.INCONTROL_PADS): 
                
                internal.sendMidiMessage(status, eventconsts.Pads[x][y], -state)
                internal.debugLog("Sent light flash command [" + str(x) + ", " + str(y) + "] (InControl Enabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
                
            else: 
                internal.sendMidiMessage(status, processorhelpers.convertPadMapping(eventconsts.Pads[x][y]), -state)
                internal.debugLog("Sent light flash command [" + str(x) + ", " + str(y) + "] (InControl Disabled)", internalconstants.DEBUG_LIGHTING_MESSAGE)
    
    
    def setFromMap(self, map):
        """Set light colours from LightMap object

        Args:
            map (LightMap): What to set the lights to
        """
        map.solidifyAll()
        for x in range(len(self.PadColours)):
            for y in range(len(self.PadColours[x])):
                self.setPadColour(x, y, map.PadColours[x][y], map.PadStates[x][y])
        return
    
    def redraw(self):
        """Resends all lighting options from current state.
        """
        for x in range(len(self.PadColours)):
            for y in range(len(self.PadColours[x])):
                self.setPadColour(x, y, self.PadColours[x][y], override=True)

state = Lights()


def lightShow():
    """OooOOoOOoOOoOOoOoO PREEEETTTTTTTTTTTTTYYYYYYYYYYYYYYYYYY!!!!!!!!!!!
    
    This draws the initialisation sequence.
    """
    state.reset()

    sleepTime = 0.05
    x = 0
    if internal.state.SHARED_INIT_STATE == internalconstants.INIT_OK:
        rainbowColours = lightingconsts.PALLETE_NORMAL
    elif  internal.state.SHARED_INIT_STATE == internalconstants.INIT_API_OUTDATED or internal.state.SHARED_INIT_STATE == internalconstants.INIT_PORT_MISMATCH:
        rainbowColours = lightingconsts.PALLETE_INIT_FAIL
    elif internal.state.SHARED_INIT_STATE == internalconstants.INIT_UPDATE_AVAILABLE:
        rainbowColours = lightingconsts.PALLETE_UPDATE
    else:
        rainbowColours = lightingconsts.PALLETE_INIT_FAIL


    while True:

        time.sleep(sleepTime)

        # Group 1
        if (x >= 0) and (x < len(rainbowColours)):
            state.setPadColour(0, 1, rainbowColours[x])
        
         # Group 2
        if (x >= 1) and (x < len(rainbowColours) + 1):
            state.setPadColour(1, 1, rainbowColours[x - 1])
            state.setPadColour(0, 0, rainbowColours[x - 1])
        
        # Group 3
        if (x >= 2) and (x < len(rainbowColours) + 2):
            state.setPadColour(2, 1, rainbowColours[x - 2])
            state.setPadColour(1, 0, rainbowColours[x - 2])
        
        # Group 4
        if (x >= 3) and (x < len(rainbowColours) + 3):
            state.setPadColour(3, 1, rainbowColours[x - 3])
            state.setPadColour(2, 0, rainbowColours[x - 3])
        
        # Group 5
        if (x >= 4) and (x < len(rainbowColours) + 4):
            state.setPadColour(4, 1, rainbowColours[x - 4])
            state.setPadColour(3, 0, rainbowColours[x - 4])
        
    
        # Group 6
        if (x >= 5) and (x < len(rainbowColours) + 5):
            state.setPadColour(5, 1, rainbowColours[x - 5])
            state.setPadColour(4, 0, rainbowColours[x - 5])
        
        # Group 7
        if (x >= 6) and (x < len(rainbowColours) + 6):
            state.setPadColour(6, 1, rainbowColours[x - 6])
            state.setPadColour(5, 0, rainbowColours[x - 6])
        
        # Group 8
        if (x >= 7) and (x < len(rainbowColours) + 7):
            state.setPadColour(7, 1, rainbowColours[x - 7])
            state.setPadColour(6, 0, rainbowColours[x - 7])
        
        # Group 9
        if (x >= 8) and (x < len(rainbowColours) + 8):
            state.setPadColour(7, 0, rainbowColours[x - 8])
        
        x += 1
       
        
        if x > len(rainbowColours) + 8: break

    state.reset()

def idleLightshow(lights):
    """EVEN PRETTIER!!!!!!!!!!

    Args:
        lights (LightMap): LightMap object to draw to
    """
    if internal.window.getIdleTick() > config.IDLE_WAIT_TIME and config.IDLE_LIGHTS_ENABLED:
        tick_num = internal.window.getIdleTick() - int(config.IDLE_WAIT_TIME) + IDLE_ANIMATION_TRAIL_LENGTH * IDLE_ANIMATION_TRAIL_SPEED

        for x in range(9):
            for y in range(2):
                # Generate colours
                if IDLE_ANIMATION_DO_TRAILS:
                    animation_speed = IDLE_ANIMATION_SPEED * IDLE_ANIMATION_TRAIL_SPEED_MODIFIER
                else:
                    animation_speed = IDLE_ANIMATION_SPEED
                colour = ((tick_num // animation_speed) + x - y) // IDLE_ANIMATION_STRETCH % 128

                light_mode = 1

                # Set off to on
                if colour == 0:
                    colour = 1

                if IDLE_ANIMATION_DO_TRAILS:
                    if not (((tick_num // IDLE_ANIMATION_TRAIL_SPEED) + x + IDLE_ANIMATION_TRAIL_Y_OFFSET*y) % IDLE_ANIMATION_TRAIL_INFREQUENCY < IDLE_ANIMATION_TRAIL_LENGTH):
                        colour = lightingconsts.COLOUR_OFF

                lights.setPadColour(x, y, colour, light_mode)

def idleLightshowActive():
    """Whether the idle lightshow is currently active

    Returns:
        bool: Whether it's active
    """
    if internal.window.getIdleTick() > config.IDLE_WAIT_TIME and config.IDLE_LIGHTS_ENABLED:
        return True

    else:
        return False

def triggerIdleLightshow():
    """Set idle tick number to tick required for lightshow to begin.
    Call this to get that sweet sweet RGB going.
    """
    internal.window.idle_tick_number = config.IDLE_WAIT_TIME

