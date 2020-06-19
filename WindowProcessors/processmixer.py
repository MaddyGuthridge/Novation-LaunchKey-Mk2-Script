"""
processmixer.py
This script processes events when the mixer window is active

"""

import mixer
import transport

import eventconsts
import internal
import config
import lighting


# Process is called to handle events
def process(command):

    command.actions.addProcessor("Mixer Processor")

    current_track = mixer.trackNumber()

    #---------------------------------
    # Faders
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER:
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
                setVolume(command, current_track, command.value)
                command.handled = True

    #---------------------------------
    # Knobs
    #---------------------------------
    if command.type == eventconsts.TYPE_KNOB:
        # Knob 1
        if command.id == eventconsts.KNOB_1: 
            setPan(command, 1, command.value)
            command.handled = True
        
        # Knob 2
        if command.id == eventconsts.KNOB_2: 
            setPan(command, 2, command.value)
            command.handled = True

        # Knob 3
        if command.id == eventconsts.KNOB_3: 
            setPan(command, 3, command.value)
            command.handled = True
        
        # Knob 4
        if command.id == eventconsts.KNOB_4: 
            setPan(command, 4, command.value)
            command.handled = True

        # Knob 5
        if command.id == eventconsts.KNOB_5: 
            setPan(command, 5, command.value)
            command.handled = True
        
        # Knob 6
        if command.id == eventconsts.KNOB_6: 
            setPan(command, 6, command.value)
            command.handled = True
        
        # Knob 7
        if command.id == eventconsts.KNOB_7: 
            setPan(command, 7, command.value)
            command.handled = True

        # Knob 8 # Like fader 9: applies to current track or master
        if command.id == eventconsts.KNOB_8: 
            # If shift key held, change master track
            if command.shifted:
                setPan(command, 0, command.value)
                command.handled = True
            # Otherwise change current track
            else:
                setPan(command, current_track, command.value)
                command.handled = True


    #---------------------------------
    # Mixer Buttons - mute/solo tracks
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER_BUTTON:
        if command.id == eventconsts.FADER_BUTTON_1:
            processMuteSolo(1, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_2:
            processMuteSolo(2, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_3:
            processMuteSolo(3, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_4:
            processMuteSolo(4, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_5:
            processMuteSolo(5, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_6:
            processMuteSolo(6, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_7:
            processMuteSolo(7, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_8:
            processMuteSolo(8, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_9:
            # If shift key held, change master track
            if command.shifted:
                processMuteSolo(0, command)
                command.handled = True
            else:
                processMuteSolo(current_track, command)
                command.handled = True

    #---------------------------------
    # Other
    #---------------------------------

    if command.id == eventconsts.TRANSPORT_RECORD and command.is_lift:
        mixer.armTrack(current_track)
        command.handled = True

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
    if internal.didSnap(internal.toFloat(value), config.MIXER_VOLUME_SNAP_TO):
        command.actions.appendAction("[Snapped]")

# Returns volume value set to send to FL Studio
def getVolumeSend(inVal):
    if config.ENABLE_SNAPPING:
        return internal.snap(internal.toFloat(inVal), config.MIXER_VOLUME_SNAP_TO)
    else: return internal.toFloat(inVal)


def getVolumeValue(inVal):
    
    return str(round(getVolumeSend(inVal) / config.MIXER_VOLUME_SNAP_TO * 100)) + "%"

def setPan(command, track, value):
    volume = getPanSend(value)
    mixer.setTrackPan(track, volume)
    command.actions.appendAction("Set " + mixer.getTrackName(track) + " pan to " + getPanValue(value))
    if internal.didSnap(internal.toFloat(value, -1), config.MIXER_PAN_SNAP_TO):
        command.actions.appendAction("[Snapped]")

# Returns volume value set to send to FL Studio
def getPanSend(inVal):
    if config.ENABLE_SNAPPING:
        return internal.snap(internal.toFloat(inVal, -1), config.MIXER_PAN_SNAP_TO)
    else: return internal.toFloat(inVal, -1)


def getPanValue(inVal):
    
    a = round(getPanSend(inVal) * 100)
    if a < 0: b = str(a) + "% Left"
    elif a > 0: b = str(a) + "% Right"
    else: b = "Centred"
    return b
