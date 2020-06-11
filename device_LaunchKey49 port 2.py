#   name=LaunchKey49 Mk2 (Port 2)
# url=
# version = 0.0.1

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
        initialisation_flag = True

        # Set port to 2 since this is the script for extended events
        internal.PORT = 2

        # Set the device into Extended Mode
        
        lighting.lightShow()
        internal.setExtendedMode(True)
        
        print('Initialisation complete')

    def OnDeInit(self):
        # Return the device into Basic Mode
        internal.setExtendedMode(False)
        print('Deinitialisation complete')
        

    def OnMidiIn(self, event):
        event.handled = False
        
        # Process the event into processedEvent format
        command = eventprocessor.processedEvent(event)
        
        
        # Print out event
        command.printOut()
        print("")
        
        event.handled = True
        
    def OnIdle(self):
        return
    
    def OnUpdateBeatIndicator(self, beat):
        print("Update beat: ", beat)
        if beat is 1: lighting.setPadColour(eventconsts.PAD_TOP_BUTTON, lighting.COLOUR_RED) # Bar
        elif beat is 2: lighting.setPadColour(eventconsts.PAD_TOP_BUTTON, lighting.COLOUR_YELLOW) # Beat
        elif beat is 0: lighting.setPadColour(eventconsts.PAD_TOP_BUTTON, lighting.COLOUR_OFF) # Off

Generic = TGeneric()

def OnInit():
    Generic.OnInit()

def OnDeInit():
    Generic.OnDeInit()

def OnMidiIn(event):
    Generic.OnMidiIn(event)

def OnIdle():
    Generic.OnIdle()

def OnUpdateBeatIndicator(beat):
    Generic.OnUpdateBeatIndicator(beat)


