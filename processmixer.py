"""
processmixer.py
This script processes events when the mixer window is active

"""

import mixer

import eventconsts
import internal
import config

def process(command):

    internal.actionStr.addProcessor("Mixer Processor")

    #---------------------------------
    # Faders
    #---------------------------------

    # Fader 1
    if command.id == eventconsts.FADER_1: 
        setVolume(1, command.value)
        internal.actionStr.appendAction("Set Track 1 volume to " + getVolumeValue(command.value))
        command.handled = True
    
    # Fader 2
    if command.id == eventconsts.FADER_2: 
        setVolume(2, command.value)
        internal.actionStr.appendAction("Set Track 2 volume to " + getVolumeValue(command.value))
        command.handled = True

    # Fader 3
    if command.id == eventconsts.FADER_3: 
        setVolume(3, command.value)
        internal.actionStr.appendAction("Set Track 3 volume to " + getVolumeValue(command.value))
        command.handled = True
    
    # Fader 4
    if command.id == eventconsts.FADER_4: 
        setVolume(4, command.value)
        internal.actionStr.appendAction("Set Track 4 volume to " + getVolumeValue(command.value))
        command.handled = True

    # Fader 5
    if command.id == eventconsts.FADER_5: 
        setVolume(5, command.value)
        internal.actionStr.appendAction("Set Track 5 volume to " + getVolumeValue(command.value))
        command.handled = True
    
    # Fader 6
    if command.id == eventconsts.FADER_6: 
        setVolume(6, command.value)
        internal.actionStr.appendAction("Set Track 6 volume to " + getVolumeValue(command.value))
        command.handled = True
    
    # Fader 7
    if command.id == eventconsts.FADER_7: 
        setVolume(7, command.value)
        internal.actionStr.appendAction("Set Track 7 volume to " + getVolumeValue(command.value))
        command.handled = True

    # Fader 8
    if command.id == eventconsts.FADER_8: 
        setVolume(8, command.value)
        internal.actionStr.appendAction("Set Track 8 volume to " + getVolumeValue(command.value))
        command.handled = True

    # Fader 9
    if command.id == eventconsts.FADER_9: 
        # Get current track number
        track = mixer.trackNumber()
        setVolume(track, command.value)
        internal.actionStr.appendAction("Set Track " + str(track) + " volume to " + getVolumeValue(command.value))
        command.handled = True

    
    

    # Add did not handle flag if not handled
    if command.handled is False: 
        internal.actionStr.appendAction("[Did not handle]")

def setVolume(track, value):
    mixer.setTrackVolume(track, getVolumeSend(value))

# Returns volume value set to send to FL Studio
def getVolumeSend(inVal):
    return internal.snap(internal.toFloat(inVal), config.MIXER_VOLUME_SNAP_TO)

def getVolumeValue(inVal):
    return str(round(getVolumeSend(inVal) / config.MIXER_VOLUME_SNAP_TO * 100)) + "%"