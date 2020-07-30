"""
processchannelrack.py
This script handles events when the channel rack is active

"""

import math # For logarithm

import channels
import ui

import lighting
import config
import internalconstants
import internal
import eventconsts
import processorhelpers

ui_mode = processorhelpers.UI_mode_handler(2)


MENU_MODE_COLOUR = lighting.UI_CHOOSE
BIT_MODE_COLOUR = lighting.COLOUR_RED

def process(command):

    command.actions.addProcessor("Channel rack Processor")

    current_channel = channels.channelNumber()

    #---------------------------------
    # Pads
    #---------------------------------
    if command.type == eventconsts.TYPE_PAD and command.is_lift:
        # UI Mode
        if command.coord_Y == 1 and command.coord_X == 0:
            ui_mode.nextMode()
            internal.window.reset_animation_tick()
            command.handle("Channel Rack: Next UI mode")

        elif ui_mode.getMode() == 1:
            process_bit_mode(command)

        elif ui_mode.getMode() == 0:
            process_menu_mode(command)

    #---------------------------------
    # Faders
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER:
        fader_num = command.coord_X

        if fader_num == 8 and not command.shifted:
            channel_num = current_channel
        else:
            channel_num = fader_num

        setVolume(command, channel_num, command.value)

    #---------------------------------
    # Knobs
    #---------------------------------
    if command.type == eventconsts.TYPE_KNOB:
        knob_num = command.coord_X

        if knob_num == 7 and not command.shifted:
            channel_num = current_channel
        else:
            channel_num = knob_num

        setPan(command, channel_num, command.value)


    #---------------------------------
    # Mixer Buttons - mute/solo tracks
    #---------------------------------
    if command.type == eventconsts.TYPE_FADER_BUTTON:
        fader_num = command.coord_X
        print(fader_num)
        if fader_num == 8 and not command.shifted:
            channel_num = current_channel
        else:
            channel_num = fader_num

        processMuteSolo(channel_num, command)

    return

# Process when in grid bits
def process_bit_mode(command):
    current_track = channels.channelNumber()
    #---------------------------------
    # Pads
    #---------------------------------
    if command.type == eventconsts.TYPE_PAD and command.is_lift:
        # Grid bits
        if command.coord_Y == 0 and command.coord_X != 8:
            
            if channels.channelCount() <= current_track:
                command.handle("Channel out of range")
                return
            
            gridBits.toggleBit(current_track, command.coord_X)
            command.handle("Grid Bits: Toggle bit")
        
        coord = [command.coord_X, command.coord_Y]


        # Scroll grid bits
        if coord == [4, 1]:
            if command.is_double_click:
                gridBits.resetScroll()
                command.actions.appendAction("Grid Bits: Reset scroll")
                command.handled = True
            else:
                gridBits.scrollLeft()
                command.actions.appendAction("Grid Bits: Scroll left")
                command.handled = True
        if coord == [5, 1]:
            gridBits.scrollRight()
            command.actions.appendAction("Grid Bits: Scroll right")
            command.handled = True
        # Zoom grid bits
        if coord == [6, 1]:
            gridBits.zoomOut()
            command.actions.appendAction("Grid Bits: Zoom out")
            command.handled = True
        if coord == [7, 1]:
            if command.is_double_click:
                gridBits.resetZoom()
                command.actions.appendAction("Grid Bits: Reset zoom")
            else:
                gridBits.zoomIn()
                command.actions.appendAction("Grid Bits: Zoom in")
            command.handled = True

# Process when in menu
def process_menu_mode(command):
    coord = [command.coord_X, command.coord_Y]

    # Next/prev track
    if coord == [1, 0]:
        ui.previous()
        command.actions.appendAction("Channel Rack: Previous channel")
        command.handled = True
    elif coord == [1, 1]:
        ui.next()
        command.actions.appendAction("Channel Rack: Next channel")
        command.handled = True

    # Cut, Copy, Paste
    elif coord == [3, 0]:
        ui.cut()
        command.actions.appendAction("UI: Cut")
        command.handled = True
    elif coord == [4, 0]:
        ui.copy()
        command.actions.appendAction("UI: Copy")
        command.handled = True
    elif coord == [5, 0]:
        ui.paste()
        command.actions.appendAction("UI: Paste")
        command.handled = True

    # To piano roll
    elif coord == [7, 1]:
        ui.showWindow(internalconstants.WINDOW_PIANO_ROLL)
        command.actions.appendAction("Sent to pianoroll")
        command.handled = True

    # Plugin window
    elif coord == [6, 1]:
        channels.showEditor(channels.channelNumber())
        command.handle("Opened plugin window")

def redraw(lights):
    if internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        current_ui_mode = ui_mode.getMode()

        if current_ui_mode == 0:
            ui_button_colour = MENU_MODE_COLOUR
        else:
            ui_button_colour = BIT_MODE_COLOUR

        lights.setPadColour(0, 1, ui_button_colour)    

        if current_ui_mode == 0:
            redraw_menu_mode(lights)

        elif current_ui_mode == 1:
            redraw_bit_mode(lights)

    return

# Redraw when in menu
def redraw_menu_mode(lights):
    
    # Set colours for controls
    if internal.window.get_animation_tick() >= 1:
        lights.setPadColour(1, 1, lighting.UI_NAV_VERTICAL)     # Next track

    if internal.window.get_animation_tick() >= 2:
        lights.setPadColour(1, 0, lighting.UI_NAV_VERTICAL)     # Prev track
        lights.setPadColour(3, 0, lighting.UI_COPY)             # Copy
    if internal.window.get_animation_tick() >= 3:
        lights.setPadColour(4, 0, lighting.UI_CUT)              # Cut
    if internal.window.get_animation_tick() >= 4:
        lights.setPadColour(5, 0, lighting.UI_PASTE)            # Paste

    if internal.window.get_animation_tick() >= 2:
        lights.setPadColour(6, 1, lighting.UI_CHOOSE)
    if internal.window.get_animation_tick() >= 3:
        lights.setPadColour(7, 1, lighting.UI_ACCEPT, 2)           # To piano roll

# Redraw when in grid bits
def redraw_bit_mode(lights):
    setGridBits(lights)

    # Set colours for controls
    if internal.window.get_animation_tick() >= 6:
        lights.setPadColour(4, 1, lighting.UI_NAV_HORIZONTAL)   # Move left
    if internal.window.get_animation_tick() >= 5:
        lights.setPadColour(5, 1, lighting.UI_NAV_HORIZONTAL)   # Move right
    if internal.window.get_animation_tick() >= 4:
        lights.setPadColour(6, 1, lighting.UI_ZOOM)             # Zoom out
    if internal.window.get_animation_tick() >= 3:
        lights.setPadColour(7, 1, lighting.UI_ZOOM)             # Zoom in


def activeStart():

    internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)

    return

def activeEnd():

    # Reset Grid Bit controller
    gridBits.resetZoom()
    gridBits.resetScroll()
    ui_mode.resetMode()

    internal.extendedMode.revert(eventconsts.INCONTROL_PADS)

    return

def topWindowStart():
    

    return

def topWindowEnd():
    

    return


    # Internal functions

class gridBitMgr:
    scroll = 0
    zoom = 1

    def getBit(self, track, position):
        return channels.getGridBit(track, position*self.zoom + 8*self.scroll)
    
    def toggleBit(self, track, position):
        val = not channels.getGridBit(track, position*self.zoom + 8*self.scroll)
        return channels.setGridBit(track, position*self.zoom + 8*self.scroll, val)
    
    def resetScroll(self):
        self.scroll = 0

    def scrollLeft(self):
        if self.scroll > 0:
            self.scroll -= 1
        
    def scrollRight(self):
        self.scroll += 1

    def zoomOut(self):
        self.zoom *= 2
    
    def zoomIn(self):
        if self.zoom > 1: self.zoom = int(self.zoom / 2)

    def resetZoom(self):
        self.zoom = 1

gridBits = gridBitMgr()

def setGridBits(lights):
    current_track = channels.channelNumber()

    if channels.channelCount() <= current_track:
        return

    # Set scroll indicator
    light_num_scroll = gridBits.scroll
    if light_num_scroll < 8:

        if not gridBits.getBit(channels.channelNumber(), light_num_scroll):
            lights.setPadColour(light_num_scroll, 0, lighting.COLOUR_LIGHT_LILAC)
        else:
            lights.setPadColour(light_num_scroll, 0, lighting.COLOUR_PINK, 2)
         
    # Set zoom indicator
    light_num_zoom = 7 - int(math.log(gridBits.zoom, 2))
    if light_num_zoom >= 0 and internal.window.get_animation_tick() > 7:
        if not gridBits.getBit(channels.channelNumber(), light_num_zoom):
            lights.setPadColour(light_num_zoom, 0, lighting.COLOUR_LIGHT_LIGHT_BLUE)
        else:
            lights.setPadColour(light_num_zoom, 0, lighting.COLOUR_BLUE, 2)

    # If zoom and scroll lie on same pad
    if light_num_scroll == light_num_zoom:
        if not gridBits.getBit(channels.channelNumber(), light_num_zoom):
            lights.setPadColour(light_num_zoom, 0, lighting.COLOUR_LIGHT_YELLOW)
        else:
            lights.setPadColour(light_num_zoom, 0, lighting.COLOUR_PINK, 2)

    # Set remaining grid bits
    for i in range(8):
        if i <= internal.window.get_animation_tick():
            if gridBits.getBit(current_track, i):
                lights.setPadColour(i, 0, lighting.COLOUR_RED, 2)
            else:
                lights.setPadColour(i, 0, lighting.COLOUR_DARK_GREY)

    return

def processMuteSolo(channel, command):

    if channels.channelCount() <= channel:
        command.handle("Channel out of range. Couldn't process mute")
        return

    if command.value == 0: return
    if channels.isChannelSolo(channel) and channels.channelCount() != 1:
        channels.soloChannel(channel)
        action = "Unsolo channel"
        
    elif command.is_double_click:
        channels.soloChannel(channel)
        action = "Solo channel"
    else: 
        channels.muteChannel(channel)
        if channels.isChannelMuted(channel):
            action = "Mute channel"
        else: 
            action = "Unmute channel"

    command.handle(action)

def setVolume(command, channel, value):

    if channels.channelCount() <= channel:
        command.handle("Channel out of range. Couldn't set volume")
        return

    volume = getVolumeSend(value)
    channels.setChannelVolume(channel, volume)
    action = "Set " + channels.getChannelName(channel) + " volume to " + getVolumeValue(value)
    if processorhelpers.didSnap(processorhelpers.toFloat(value), internalconstants.CHANNEL_VOLUME_SNAP_TO):
        action += " [Snapped]"
    command.handle(action)

def setPan(command, channel, value):
    if channels.channelCount() <= channel:
        command.handle("Channel out of range. Couldn't setpan")
        return

    volume = getPanSend(value)
    channels.setChannelPan(channel, volume)
    action = "Set " + channels.getChannelName(channel) + " pan to " + getPanValue(value)
    if processorhelpers.didSnap(processorhelpers.toFloat(value, -1), internalconstants.CHANNEL_PAN_SNAP_TO):
        action = "[Snapped]"
    command.handle(action)

# Returns volume value set to send to FL Studio
def getVolumeSend(inVal):
    if config.ENABLE_SNAPPING:
        return processorhelpers.snap(processorhelpers.toFloat(inVal), internalconstants.CHANNEL_VOLUME_SNAP_TO)
    else: return processorhelpers.toFloat(inVal)


def getVolumeValue(inVal):
    
    return str(round(getVolumeSend(inVal) * 100)) + "%"



# Returns volume value set to send to FL Studio
def getPanSend(inVal):
    if config.ENABLE_SNAPPING:
        return processorhelpers.snap(processorhelpers.toFloat(inVal, -1), internalconstants.CHANNEL_PAN_SNAP_TO)
    else: return processorhelpers.toFloat(inVal, -1)


def getPanValue(inVal):
    
    a = round(getPanSend(inVal) * 100)
    if a < 0: b = str(a) + "% Left"
    elif a > 0: b = str(a) + "% Right"
    else: b = "Centred"
    return b
