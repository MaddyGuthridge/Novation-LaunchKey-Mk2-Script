"""
internal.py
This file contains functions common to  scripts loaded by both files.

"""

#-------------------------------
# Edit this file at your own risk. All user-modifyable variables are found in 'config.py'.
#-------------------------------

import time

import device
import ui
import transport
import general
import channels

import eventconsts
import config
import internalconstants
import eventprocessor
import lighting
# import updatecheck # Currently modules are unavailable

import WindowProcessors.processwindows as processwindows
import PluginProcessors.processplugins as processplugins
import ControllerProcessors.keys as keys


