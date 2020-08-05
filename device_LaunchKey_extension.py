# name=LaunchKey Mk2 Extension
# url=https://github.com/MiguelGuthridge/Novation-LaunchKey49-Mk2-Script
# receiveFrom=LaunchKey Mk2

"""
device_LaunchKey49 port 2.py
This file is the controller file for port 2 of the LaunchKey49 Mk2.
It handles communication with the device, including colours.

"""


#-------------------------------
# Edit this file at your own risk. All user-modifyable variables are found in 'config.py'.
#-------------------------------

import patterns
import channels
import mixer
import device
import transport
import arrangement
import general
import launchMapPages 
import playlist
import ui
import screen

import midi
import utils

import time

# Other project files
import config
import internal
import lighting
import eventconsts
import eventprocessor



initialisation_flag = False
initialisation_flag_response = False



class TGeneric():
    def __init__(self):
        return

    def OnInit(self):

        # Run shared init functions
        internal.sharedInit()

        # Set the device into Extended Mode
        internal.extendedMode.setVal(True, force=True)

        # Run light show
        lighting.lightShow()

        # Process inControl preferences | Say it's external since we want the settings to be applied regardless
        if config.START_IN_INCONTROL_KNOBS == False: internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS, from_internal=False) 
        if config.START_IN_INCONTROL_FADERS == False: internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS, from_internal=False) 
        if config.START_IN_INCONTROL_PADS == False: internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS, from_internal=False) 
        

        print('Initialisation complete')
        print(internal.getLineBreak())
        print(internal.getLineBreak())
        print("")
        print("")

    def OnDeInit(self):
        lighting.lightShow()
        # Return the device into Basic Mode
        internal.extendedMode.setVal(False)
        print('Deinitialisation complete')
        print(internal.getLineBreak())
        print(internal.getLineBreak())
        print("")
        print("")
        

    def OnMidiIn(self, event):
        event.handled = False
        internal.eventClock.start()
        # Update active window (ui.onRefresh() isnt working properly)
        internal.ActiveWindow = ui.getFocusedFormCaption()

        # Process the event into processedEvent format
        command = eventprocessor.processedEvent(event)

        # Print event before processing
        internal.printCommand(command)

        # Check for shift button releases (return early)
        if event.handled:
            internal.printCommandOutput(command)
            return

        # Process command
        eventprocessor.processExtended(command)

        # If command was edited, update event object
        if command.edited:
            event.status = command.status
            event.data1 = command.note
            event.data2 = command.value

        # Print output of command
        internal.printCommandOutput(command)
        event.handled = True
    
    def OnIdle(self):
        internal.idleProcessor()
        eventprocessor.redraw()
        return

    def OnRefresh(self, flags):
        internal.refreshProcessor()
        
        # Prevent idle lightshow when other parts of FL are being used
        internal.window.reset_idle_tick()
        return
    
    def OnUpdateBeatIndicator(self, beat):
        internal.beat.set_beat(beat)
        
        # Prevent idle lightshow from being triggered during playback
        internal.window.reset_idle_tick()
        
    def OnSendTempMsg(self, msg, duration):
        internal.window.reset_idle_tick()

Generic = TGeneric()

def OnInit():
    Generic.OnInit()

def OnDeInit():
    Generic.OnDeInit()

def OnMidiIn(event):
    Generic.OnMidiIn(event)

def OnIdle():
    Generic.OnIdle()

def OnRefresh(flags):
    Generic.OnRefresh(flags)

def OnUpdateBeatIndicator(beat):
    Generic.OnUpdateBeatIndicator(beat)

def OnSendTempMsg(msg, duration):
    Generic.OnSendTempMsg(msg, duration)
