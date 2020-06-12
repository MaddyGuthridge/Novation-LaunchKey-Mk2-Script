"""
processmixer.py
This script processes events when the mixer window is active

"""

import mixer

import eventconsts
import internal
import config

def process(command):

    command.actions.addProcessor("Mixer Processor")

    #---------------------------------
    # Faders
    #---------------------------------

    # Fader 1
    if command.id == eventconsts.FADER_1: 
        setVolume(command, 1, command.value)
        command.handled = True
    
    # Fader 2
    if command.id == eventconsts.FADER_2: 
        setVolume(command, 2, command.value)
        command.handled = True

    # Fader 3
    if command.id == eventconsts.FADER_3: 
        setVolume(command, 3, command.value)
        command.handled = True
    
    # Fader 4
    if command.id == eventconsts.FADER_4: 
        setVolume(command, 4, command.value)
        command.handled = True

    # Fader 5
    if command.id == eventconsts.FADER_5: 
        setVolume(command, 5, command.value)
        command.handled = True
    
    # Fader 6
    if command.id == eventconsts.FADER_6: 
        setVolume(command, 6, command.value)
        command.handled = True
    
    # Fader 7
    if command.id == eventconsts.FADER_7: 
        setVolume(command, 7, command.value)
        command.handled = True

    # Fader 8
    if command.id == eventconsts.FADER_8: 
        setVolume(command, 8, command.value)
        command.handled = True

    # Fader 9
    if command.id == eventconsts.FADER_9: 
        # If shift key held, change master track
        if command.shifted:
            setVolume(command, 0, command.value)
            command.handled = True
        # Otherwise change current track
        else:
            # Get current track number
            track = mixer.trackNumber()
            setVolume(command, track, command.value)
            command.handled = True

    
    

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")

def setVolume(command, track, value):
    volume = getVolumeSend(value)
    mixer.setTrackVolume(track, volume)
    command.actions.appendAction("Set " + mixer.getTrackName(track) + " volume to " + getVolumeValue(value))
    if internal.didSnap(internal.toFloat(value), config.MIXER_VOLUME_SNAP_TO):
        command.actions.appendAction("[Snapped]")

# Returns volume value set to send to FL Studio
def getVolumeSend(inVal):
    return internal.snap(internal.toFloat(inVal), config.MIXER_VOLUME_SNAP_TO)

def getVolumeValue(inVal):
    
    return str(round(getVolumeSend(inVal) / config.MIXER_VOLUME_SNAP_TO * 100)) + "%"