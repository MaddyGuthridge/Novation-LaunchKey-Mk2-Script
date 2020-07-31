"""WindowProcessors > processmixer.py

This script processes events when the mixer window is active. It provides functionality
such as setting track volumes and visualising peak metres when transport is active.

Author: Miguel Guthridge
"""

import mixer
import transport

import eventconsts
import internal
import internalconstants
import config
import lighting
import processorhelpers


# Process is called to handle events
def process(command):

    command.actions.addProcessor("Mixer Processor")

    current_track = mixer.trackNumber()

    #---------------------------------
    # Faders
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER:
        processFaders(command)

    #---------------------------------
    # Knobs
    #---------------------------------
    if command.type == eventconsts.TYPE_KNOB:
        processKnobs(command)


    #---------------------------------
    # Mixer Buttons - mute/solo tracks
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER_BUTTON:
        processFaderButtons(command)

    #---------------------------------
    # Other
    #---------------------------------

    # Arms current mixer track when shifted
    if command.id == eventconsts.TRANSPORT_RECORD and command.is_lift and command.shifted:
        mixer.armTrack(current_track)
        command.handle("Arm current mixer track")

# Process fader events
def processFaders(command):
    current_track = mixer.trackNumber()

    fader_num = command.coord_X + 1

    if fader_num == 9:
        if command.shifted:
            track_num = 0
        else:
            track_num = current_track
    else:
        track_num = fader_num

    setVolume(command, track_num, command.value)

# Process knob events
def processKnobs(command):
    current_track = mixer.trackNumber()

    knob_num = command.coord_X + 1

    if knob_num == 8:
        if command.shifted:
            track_num = 0
        else:
            track_num = current_track
    else:
        track_num = knob_num

    setPan(command, track_num, command.value)

# Process fader button events
def processFaderButtons(command):
    current_track = mixer.trackNumber()
    
    fader_num = command.coord_X + 1

    if fader_num == 9:
        if command.shifted:
            track_num = 0
        else:
            track_num = current_track
    else:
        track_num = fader_num

    processMuteSolo(track_num, command)


def redraw(lights):

    # When playing, display peak metre
    if transport.isPlaying():
        setPeaks(lights)
    

    return

def activeStart():
    return

def activeEnd():
    return

def topWindowStart():
    return

def topWindowEnd():
    return

# Internal functions

def processPeak(lights, y, level):
    level = level ** 3
    colour = lighting.COLOUR_RED
    for i in range(8):
        
        if level > 1 - (i + 1)/8:
            if i >= 4:
                colour = lighting.COLOUR_GREEN
            elif i >= 2:
                colour = lighting.COLOUR_YELLOW
            elif i >= 1:
                colour = lighting.COLOUR_ORANGE
            lights.setPadColour(7 - i, y, colour)
    

def setPeaks(lights):
    # Get selected mixer track
    selected_track = mixer.trackNumber()
    peakLeft = mixer.getTrackPeaks(selected_track, 0)
    peakRight = mixer.getTrackPeaks(selected_track, 1)

    processPeak(lights, 0, peakLeft)
    processPeak(lights, 1, peakRight)

    return

def processMuteSolo(track, command):
    if command.value == 0: return
    if mixer.isTrackSolo(track):
        mixer.soloTrack(track)
        command.actions.appendAction("Unsolo track " + str(track))
        return
    mixer.muteTrack(track)
    if command.is_double_click:
        mixer.soloTrack(track)
        command.actions.appendAction("Solo track " + str(track))
    else: 
        if mixer.isTrackMuted(track):
            command.actions.appendAction("Mute track " + str(track))
        else: 
            command.actions.appendAction("Unmute track " + str(track))

def setVolume(command, track, value):
    volume = getVolumeSend(value)
    mixer.setTrackVolume(track, volume)
    command.actions.appendAction("Set " + mixer.getTrackName(track) + " volume to " + getVolumeValue(value))
    if processorhelpers.didSnap(processorhelpers.toFloat(value), internalconstants.MIXER_VOLUME_SNAP_TO):
        command.actions.appendAction("[Snapped]")

# Returns volume value set to send to FL Studio
def getVolumeSend(inVal):
    if config.ENABLE_SNAPPING:
        return processorhelpers.snap(processorhelpers.toFloat(inVal), internalconstants.MIXER_VOLUME_SNAP_TO)
    else: return processorhelpers.toFloat(inVal)


def getVolumeValue(inVal):
    
    return str(round(getVolumeSend(inVal) / internalconstants.MIXER_VOLUME_SNAP_TO * 100)) + "%"

def setPan(command, track, value):
    volume = getPanSend(value)
    mixer.setTrackPan(track, volume)
    command.actions.appendAction("Set " + mixer.getTrackName(track) + " pan to " + getPanValue(value))
    if processorhelpers.didSnap(processorhelpers.toFloat(value, -1), internalconstants.MIXER_PAN_SNAP_TO):
        command.actions.appendAction("[Snapped]")

# Returns volume value set to send to FL Studio
def getPanSend(inVal):
    if config.ENABLE_SNAPPING:
        return processorhelpers.snap(processorhelpers.toFloat(inVal, -1), internalconstants.MIXER_PAN_SNAP_TO)
    else: return processorhelpers.toFloat(inVal, -1)


def getPanValue(inVal):
    
    a = round(getPanSend(inVal) * 100)
    if a < 0: b = str(a) + "% Left"
    elif a > 0: b = str(a) + "% Right"
    else: b = "Centred"
    return b
