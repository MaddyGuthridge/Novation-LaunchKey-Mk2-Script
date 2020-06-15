#   name=LaunchKey49 Mk2
# url=
# version = 0.0.1

"""
device_LaunchKey49.py
This file is the controller file for port 1 of the LaunchKey49 Mk2.
It handles most note and controller events.

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

import config
import internal
import eventprocessor

import processdefault


class TGeneric():
    def __init__(self):
        return

    def OnInit(self):
        # Set port to basic
        internal.PORT = config.DEVICE_PORT_BASIC

        print('Initialisation complete')
        internal.printLineBreak()
        internal.printLineBreak()
        print("")
        print("")



    def OnDeInit(self):
        print('Deinitialisation complete')

    def OnMidiIn(self, event):
        event.handled = False
        
        # Process the event into processedEvent format
        command = eventprocessor.processedEvent(event)

        eventprocessor.process(command)

        # If command hasn't been handled by any above uses, use the default controls
        if command.handled is False:
            processdefault.process(command)
        
        internal.printCommand(command)
    
    def OnIdle(self):
        internal.idleProcessor()
        
        


Generic = TGeneric()

def OnInit():
    Generic.OnInit()

def OnDeInit():
    Generic.OnDeInit()

def OnMidiIn(event):
    Generic.OnMidiIn(event)

def OnIdle():
    Generic.OnIdle()