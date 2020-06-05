#	name=Generic device
# url=

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

EventNameT = ['Note Off', 'Note On ', 'Key Aftertouch', 'Control Change','Program Change',  'Channel Aftertouch', 'Pitch Bend', 'System Message' ]

class TGeneric():
	def __init__(self):
		return

	def OnInit(self):
		print('init ready')

	def OnDeInit(self):
		print('deinit ready')

	def OnMidiMsg(self, event):
		event.handled = False
		print ("{:X} {:X} {:2X} {}".format(event.status, event.data1, event.data2,  EventNameT[(event.status - 0x80) // 16] + ': '+  utils.GetNoteName(event.data1)))


Generic = TGeneric()

def OnInit():
	Generic.OnInit()

def OnDeInit():
	Generic.OnDeInit()

def OnMidiMsg(event):
	Generic.OnMidiMsg(event)