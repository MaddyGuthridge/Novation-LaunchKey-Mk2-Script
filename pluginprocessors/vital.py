"""
pluginprocessors > vital.py

This processor adds integration with the wavetable synthesizer Vital by Matt Tytel

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

# Add names of plugins your script can process to this list
PLUGINS = ["Vital"]


# Import any modules you might need\
import pluginswrapper
import config
import internal
import eventconsts
import eventprocessor
import lightingconsts
import processorhelpers

# Previous param index: should speed things up
prev_param_index = -1

#
# Oscillator
#

# Params

OSCILLATOR = "Oscillator"

WAVE_FRAME = "Wave Frame"
UNISON = "Unison Voices"
DETUNE = "Unison Detune"
FREQUENCY_MORPH = "Frequency Morph Amount"
DISTORTION = "Distortion Amount"


NUM_OSCS = 3

selected_osc = 1

def processOsc(command):
    global prev_param_index
    
    param_str =  OSCILLATOR + " " + str(selected_osc) + " "
    
    # When you handle your events, use command.handle("Some action") to handle events.
    if command.type is eventconsts.TYPE_BASIC_FADER:
        if command.coord_X == 0:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + WAVE_FRAME, 
                                    command.value, -1, prev_param_index)
            command.handle("Wave frame", 1)
            
        elif command.coord_X == 1:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + UNISON, 
                                    command.value, -1, prev_param_index)
            command.handle("Unison voices", 1)
            
        elif command.coord_X == 2:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + DETUNE, 
                                    command.value, -1, prev_param_index)
            command.handle("Detune", 1)
            
    elif command.type is eventconsts.TYPE_BASIC_KNOB:
        if command.coord_X == 0:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + FREQUENCY_MORPH, 
                                    command.value, -1, prev_param_index)
            command.handle("Frequency Morph", 1)
        elif command.coord_X == 1:
            pluginswrapper.setParamByName(
                                    param_str + DISTORTION, 
                                    command.value, -1, prev_param_index)
            command.handle("Distortion", 1)
            


#
# Redirect functions
#

def topPluginStart():
    """Called when plugin is top plugin (not neccesarily focused)
    """
    
    # Only in extended mode: uncomment lines to set inControl mode
    if internal.getPortExtended():
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS) # Faders
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS) # Knobs
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS) # Pads
        pass
    return

def topPluginEnd():
    """Called when plugin is no longer top plugin (not neccesarily focused)
    """
    
    # Only in extended mode: uncomment lines to revert to previous inControl modes
    if internal.getPortExtended():
        internal.extendedMode.revert(eventconsts.INCONTROL_FADERS) # Faders
        internal.extendedMode.revert(eventconsts.INCONTROL_KNOBS) # Knobs
        internal.extendedMode.revert(eventconsts.INCONTROL_PADS) # Pads
        pass
    return

def activeStart():
    """Called when plugin brought to foreground (focused)
    """
    
    return

def activeEnd():
    """Called when plugin no longer in foreground (end of focused)
    """
    
    return

def redraw(lights):
    """Called when redrawing UI on pads. Set colours of lights here.

    Args:
        lights (LightMap): object containing state of lights for next redraw. 
            Modify the object using it's methods to set light colours.
    """
    return

def process(command):
    """Called when processing commands. 

    Args:
        command (ParsedEvent): contains useful information about the event. 
            Use this to determing what actions your processor will take.
    """
    
    
    # Add event processor to actions list (useful for debugging)
    command.actions.addProcessor("Vital Processor")

    processOsc(command)


    return

def beatChange(beat):
    pass
