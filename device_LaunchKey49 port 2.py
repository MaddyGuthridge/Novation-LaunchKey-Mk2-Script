#   name=LaunchKey49 Mk2 (Port 2)
# url=
# version = 0.0.1

"""
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

import config
import internal

initialisation_flag = False
initialisation_flag_response = False

class TGeneric():
    def __init__(self):
        return

    def OnInit(self):
        initialisation_flag = True
        # Set the device into Extended Mode
        device.midiOutMsg(internal.toMidiMessage(0x9F, 0x0C, 0x7F))
        
        
        print('Initialisation complete')

    def OnDeInit(self):
        # Return the device into Basic Mode
        device.midiOutMsg(internal.toMidiMessage(0x9F, 0x0C, 0x00))
        print('Deinitialisation complete')

    def OnMidiIn(self, event):
        event.handled = False
        
        
        
        # If the event is unhandled, print out what it is:
        if event.handled is False:
            print("Unhandled event: {:X} {:X} {:2X} {}".format(event.status, event.data1, event.data2,  internal.EventNameT[(event.status - 0x80) // 16] + ': '+  utils.GetNoteName(event.data1)))


Generic = TGeneric()

def OnInit():
    Generic.OnInit()

def OnDeInit():
    Generic.OnDeInit()

def OnMidiIn(event):
    Generic.OnMidiIn(event)