"""
internal > shiftstate_new.py

This module contains classes and objects for managing shift menus.
it is a remake of shiftstate.py

Author: Miguel Guthridge
"""

import config

class ShiftState:
    """Object for managing the state of a single shift menu.
    """
    
    def __init__(self):
        """Creates instance of ShiftState object

        Args:
            name (str): Name of shift button
            id_listen (int): Event ID for a shift button. This is checked when determining whether to enable shift.
        """
        self.name = "None"
        self.id_listen = 0
        
        self.is_down = False
        self.is_sustained = False
        self.is_used = False
        
    def processShift(self, command):
        """Processes command to check whether to press the shift button.

        Args:
            command (ParsedEvent): command chercked against object's internal shift ID.
            
        Returns:
            int: new state of shift. 
               -1 for wrong event id
                0 for now up
                1 for now down.
        """
        # Return if this isn't the right button.
        if command.id != self.id_listen:
            return -1
        
        if command.is_lift:
            if self.is_down:
                self.onLift()
                self.is_down = False
                if self.is_used:
                    command.act("Exit shift menu")
                    self.is_used = False
                
            return 0
            
        else:
            self.is_down = True
            if self.is_sustained:
                self.is_sustained = False
            else:
                self.onPress()
                command.act("Enter shift menu")
                if command.is_double_click:
                    self.is_sustained = True
                    command.handle("Enter sustained shift")
                
            return 1
        
    def use(self):
        """Check if shift button is down (or sustained) and use it if it is.

        Returns:
            bool: Whether the button was pressed
        """
        if self.is_down:
            self.is_used = True
            
            return True
        elif self.is_sustained:
            if config.AUTOCANCEL_SUSTAINED_SHIFT:
                self.is_sustained = False
                self.onLift()
        else:
            return False
        
    def query(self):
        """Check if shift button is down (or sustained)

        Returns:
            bool: Whether the shift is active
        """
        return (self.is_down or self.is_sustained)
    
    def setDown(self, new_val):
        self.is_sustained = False
        self.is_down = new_val
    
    def process(self, command):
        """Process command: implemented by child classes

        Args:
            command (ParsedEvent): Event to be processed
        """
        pass
        
    def redraw(self, lights):
        """Redraw lights: implemented by child classes

        Args:
            lights (LightMap): Lights object to draw on
        """
        pass
        
    def onPress(self):
        pass
    
    def onLift(self):
        pass
        
class ShiftsMgr:
    """Manages multiple shift menus
    """
    def __init__(self):
        self.menus = dict()
        self.current_down = ""
        
    def processShift(self, command):
        """Process events to set active shift menu

        Args:
            command (ParsedEvent): Command that may or may not trigger shift menus
        """
        # If a shift menu is active
        if self.current_down != "":
            # Process shift in active shift menu
            result = self.menus[self.current_down].processShift(command)
            # If event didn't change active shift menu
            if result == -1:
                # Ignore it
                return
            
            # If event caused shift menu to lift
            elif result == 0:
                self.current_down = ""
                return
            
            # If shift menu caused shift menu to press
            else:
                # Ignore it
                return
        
        # No shift menu active
        else:
            for menu_key in self.menus.keys():
                # Process shift in active shift menu
                result = self.menus[menu_key].processShift(command)
                # If event didn't change active shift menu
                if result == -1:
                    continue # Ignore it
                
                # If event caused shift menu to press
                elif result == 1:
                    # Set that shift menu as down
                    self.current_down = menu_key
                    return
                
                # If shift menu caused shift menu to press
                else:
                    # Ignore it
                    continue
    
    def process(self, command):
        """Call shift menu processor for current shift menu

        Args:
            command (ParsedEvent): A parsed event
        """
        if self.current_down != "":
            self.menus[self.current_down].process(command)
            
    def redraw(self, lights):
        """Call shift menu redraw function for current shift menu

        Args:
            lights (LightMap): Lights to draw onto
        """
        if self.current_down != "":
            self.menus[self.current_down].redraw(lights)
            
    def query(self):
        """Returns true if any shift button is down
        """
        return self.current_down != ""
            
    def __getitem__(self, key):
        return self.menus[key]
    
    def addShift(self, Shift, name):
        """Add a shift menu to the list

        Args:
            Shift (class): Class from which to construct shift menu
            name (str): Name of the menu (for access from key)
        """
        self.menus[name] = Shift()
    

shifts = ShiftsMgr()

from .shifts.mainshift import MainShift
from .shifts.debugshift import DebugShift

shifts.addShift(MainShift, "MAIN")
shifts.addShift(DebugShift, "DEBUG")
