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


class TGeneric():
    def __init__(self):
        return

    def OnInit(self):
        print('Initialisation complete')

    def OnDeInit(self):
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