"""
processchannelrack.py
This script handles events when the channel rack is active

"""

import channels

import config
import internal
import eventconsts



def process(command):

    command.actions.addProcessor("Channel rack Processor")

    #---------------------------------
    # Faders
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER:
        # Fader 1
        if command.id == eventconsts.FADER_1: 
            setVolume(command, 0, command.value)
            command.handled = True
        
        # Fader 2
        if command.id == eventconsts.FADER_2: 
            setVolume(command, 1, command.value)
            command.handled = True

        # Fader 3
        if command.id == eventconsts.FADER_3: 
            setVolume(command, 2, command.value)
            command.handled = True
        
        # Fader 4
        if command.id == eventconsts.FADER_4: 
            setVolume(command, 3, command.value)
            command.handled = True

        # Fader 5
        if command.id == eventconsts.FADER_5: 
            setVolume(command, 4, command.value)
            command.handled = True
        
        # Fader 6
        if command.id == eventconsts.FADER_6: 
            setVolume(command, 5, command.value)
            command.handled = True
        
        # Fader 7
        if command.id == eventconsts.FADER_7: 
            setVolume(command, 6, command.value)
            command.handled = True

        # Fader 8
        if command.id == eventconsts.FADER_8: 
            setVolume(command, 7, command.value)
            command.handled = True

        # Fader 9
        if command.id == eventconsts.FADER_9: 
            # If shift key held, change master track
            if command.shifted:
                setVolume(command, 8, command.value)
                command.handled = True
            # Otherwise change current track
            else:
                # Get current track number
                track = channels.channelNumber()
                setVolume(command, track, command.value)
                command.handled = True

    #---------------------------------
    # Knobs
    #---------------------------------
    if command.type == eventconsts.TYPE_KNOB:
        # Knob 1
        if command.id == eventconsts.KNOB_1: 
            setPan(command, 0, command.value)
            command.handled = True
        
        # Knob 2
        if command.id == eventconsts.KNOB_2: 
            setPan(command, 1, command.value)
            command.handled = True

        # Knob 3
        if command.id == eventconsts.KNOB_3: 
            setPan(command, 2, command.value)
            command.handled = True
        
        # Knob 4
        if command.id == eventconsts.KNOB_4: 
            setPan(command, 3, command.value)
            command.handled = True

        # Knob 5
        if command.id == eventconsts.KNOB_5: 
            setPan(command, 4, command.value)
            command.handled = True
        
        # Knob 6
        if command.id == eventconsts.KNOB_6: 
            setPan(command, 5, command.value)
            command.handled = True
        
        # Knob 7
        if command.id == eventconsts.KNOB_7: 
            setPan(command, 6, command.value)
            command.handled = True

        # Knob 8
        if command.id == eventconsts.KNOB_8: 
            # If shift key held, change track 7
            if command.shifted:
                setPan(command, 7, command.value)
                command.handled = True
            # Otherwise change current track
            else:
                # Get current track number
                track = channels.channelNumber()
                setPan(command, track, command.value)
                command.handled = True


    #---------------------------------
    # Mixer Buttons - mute/solo tracks
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER_BUTTON:
        if command.id == eventconsts.FADER_BUTTON_1:
            processMuteSolo(0, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_2:
            processMuteSolo(1, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_3:
            processMuteSolo(2, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_4:
            processMuteSolo(3, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_5:
            processMuteSolo(4, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_6:
            processMuteSolo(5, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_7:
            processMuteSolo(6, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_8:
            processMuteSolo(7, command)
            command.handled = True

        if command.id == eventconsts.FADER_BUTTON_9:
            # If shift key held, change 9th track
            if command.shifted:
                processMuteSolo(8, command)
                command.handled = True
            else:
                processMuteSolo(channels.channelNumber(), command)
                command.handled = True

    return

def redraw(lights):



    return

def activeStart():

    internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)

    return

def activeEnd():

    internal.extendedMode.revert(eventconsts.INCONTROL_PADS)

    return

def topWindowStart():
    

    return

def topWindowEnd():
    

    return


    # Internal functions

def processMuteSolo(channel, command):
    if command.value == 0: return
    if channels.isChannelSolo(channel):
        channels.soloChannel(channel)
        command.actions.appendAction("Unsolo channel " + str(channel))
        return
    channels.muteChannel(channel)
    if command.is_double_click:
        channels.soloChannel(channel)
        command.actions.appendAction("Solo channel " + str(channel))
    else: 
        if channels.isChannelMuted(channel):
            command.actions.appendAction("Mute channel " + str(channel))
        else: 
            command.actions.appendAction("Unmute channel " + str(channel))

def setVolume(command, track, value):
    volume = getVolumeSend(value)
    channels.setChannelVolume(track, volume)
    command.actions.appendAction("Set " + channels.getChannelName(track) + " volume to " + getVolumeValue(value))
    if internal.didSnap(internal.toFloat(value), config.CHANNEL_VOLUME_SNAP_TO):
        command.actions.appendAction("[Snapped]")

# Returns volume value set to send to FL Studio
def getVolumeSend(inVal):
    if config.ENABLE_SNAPPING:
        return internal.snap(internal.toFloat(inVal), config.CHANNEL_VOLUME_SNAP_TO)
    else: return internal.toFloat(inVal)


def getVolumeValue(inVal):
    
    return str(round(getVolumeSend(inVal) * 100)) + "%"

def setPan(command, track, value):
    volume = getPanSend(value)
    channels.setChannelPan(track, volume)
    command.actions.appendAction("Set " + channels.getChannelName(track) + " pan to " + getPanValue(value))
    if internal.didSnap(internal.toFloat(value, -1), config.CHANNEL_PAN_SNAP_TO):
        command.actions.appendAction("[Snapped]")

# Returns volume value set to send to FL Studio
def getPanSend(inVal):
    if config.ENABLE_SNAPPING:
        return internal.snap(internal.toFloat(inVal, -1), config.CHANNEL_PAN_SNAP_TO)
    else: return internal.toFloat(inVal, -1)


def getPanValue(inVal):
    
    a = round(getPanSend(inVal) * 100)
    if a < 0: b = str(a) + "% Left"
    elif a > 0: b = str(a) + "% Right"
    else: b = "Centred"
    return b
