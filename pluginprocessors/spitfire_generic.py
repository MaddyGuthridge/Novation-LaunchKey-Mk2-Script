"""
pluginprocessors > spitfire_generic.py

This module contains functions for managing and setting parameters for
Spitfire Audio plugins, as they contain many common parameters. It has error
checking to find parameters by name if they ever don't align.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import pluginswrapper
import processorhelpers

EXPECTED_EXPRESSION = 0
EXPECTED_DYNAMICS = 1
EXPECTED_REVERB = 2
EXPECTED_RELEASE = 3
EXPECTED_TIGHTNESS = 4
EXPECTED_VIBRATO = 5

def setExpression(command):
    global EXPECTED_EXPRESSION
    EXPECTED_EXPRESSION = pluginswrapper.setParamByName("Expression", command.value, -1, EXPECTED_EXPRESSION, command)

def setDynamics(command):
    global EXPECTED_DYNAMICS
    EXPECTED_DYNAMICS = pluginswrapper.setParamByName("Dynamics", command.value, -1, EXPECTED_DYNAMICS, command)

def setReverb(command):
    global EXPECTED_REVERB
    EXPECTED_REVERB = pluginswrapper.setParamByName("Reverb", command.value, -1, EXPECTED_REVERB, command)

def setRelease(command):
    global EXPECTED_RELEASE
    EXPECTED_RELEASE = pluginswrapper.setParamByName("Release", command.value, -1, EXPECTED_RELEASE, command)

def setTightness(command):
    global EXPECTED_TIGHTNESS
    EXPECTED_TIGHTNESS = pluginswrapper.setParamByName("Tightness", command.value, -1, EXPECTED_TIGHTNESS, command)

def setVibrato(command):
    global EXPECTED_VIBRATO
    EXPECTED_VIBRATO = pluginswrapper.setParamByName("Vibrato", command.value, -1, EXPECTED_VIBRATO, command)


