"""
internal > snap.py

This file manages the state of FL Studio's snapping.

Author: Miguel Guthridge
"""

import ui

from .messages import sendMidiMessage

import eventconsts

class SnapMgr:
    
    def __init__(self):
        self.refresh()

    def refresh(self):
        """Refreshes snap mode
        """
        self.snap_mode = ui.getSnapMode()

        if self.snap_mode == 3:
            self.snap_enabled = False
            sendMidiMessage(0xBF, 0x3B, 0x00)
        else:
            self.snap_enabled = True
            sendMidiMessage(0xBF, 0x3B, 0x7F)
            
    def getSnapEnabled(self):
        """Get whether snap mode is enabled

        Returns:
            bool: Whether snapping is enabled
        """
        return self.snap_enabled
    
    def getSnapMode(self):
        """Get current snap mode

        Returns:
            int: snap mode (index in snap mode drop down in FL)
        """
        return self.snap_mode
    
    def setSnapMode(self, new_mode):
        """Set snap mode

        Args:
            new_mode (int): snap mode (index in snap mode drop down in FL)
        """
        ui.snapMode(new_mode - self.snap_mode)
        
        
        
    def toggleSnapMode(self):
        """Toggles whether snap mode is enabled
        """
        ui.snapOnOff()
    
    def processSnapMode(self, command):
        """Process fader button events to set snap mode

        Args:
            command (ParsedEvent): Event to process, must be fader button
        """
        snap_mode = -1
        
        if command.is_lift:
            coord = command.coord_X + 1
            
            # Beat
            if coord == 1:
                # Beat
                snap_mode = 13
            
            # Quavers (1/8th)
            elif coord == 2:
                # 1/2 beat
                snap_mode = 12
            
            # Triplets (1/12th)
            elif coord == 3:
                # 1/3 beat
                snap_mode = 11
            
            # Semiquavers (1/16th)
            elif coord == 4:
                # 1/4 beat
                snap_mode = 10
            
            # Half-triplets (1/24th)
            elif coord == 5:
                # 1/6th beat
                snap_mode = 9
            
            # Demisemiquavers (1/32nd)
            elif coord == 6:
                # Step
                snap_mode = 8
                
            # Cell
            elif coord == 7:
                snap_mode = 1
            
            # Line
            elif coord == 8:
                snap_mode = 0
                
            # Toggle
            elif coord == 9:
                self.toggleSnapMode()
                command.handle("Toggle snap")
                return
            
            # Set snap mode
            if snap_mode != -1:
                self.setSnapMode(snap_mode)
                command.handle("Set snap mode")
        
        else:
            command.handle("Snap mode press catch")
        
snap = SnapMgr()


