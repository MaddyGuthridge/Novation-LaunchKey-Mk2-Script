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
NUM_OSCS = 3

selected_osc = 1

OSC_ENABLED = "Switch"

OSC_WAVE_FRAME = "Wave Frame"
OSC_UNISON = "Unison Voices"
OSC_DETUNE = "Unison Detune"
OSC_PHASE = "Phase"
OSC_PHASE_RAND = "Phase Randomization"

OSC_LEVEL = "Level"
OSC_PAN = "Pan"
OSC_FREQUENCY_MORPH = "Frequency Morph Amount"
OSC_DISTORTION = "Distortion Amount"




def processOsc(command):
    global prev_param_index, selected_osc
    
    param_str =  OSCILLATOR + " " + str(selected_osc) + " "
    
    if not pluginswrapper.getParamByName(param_str + OSC_ENABLED):
        selected_osc = 0
    
    if command.type is eventconsts.TYPE_BASIC_PAD and command.coord_Y == 1:
        if command.is_lift:
            # Change oscillators
            if command.coord_X < NUM_OSCS:
                osc_num = command.coord_X + 1
                param_str = OSCILLATOR + " " + str(osc_num) + " "
                
                # Acting on selected oscillator
                if osc_num == selected_osc:
                    # If disabled
                    if not pluginswrapper.getParamByName(param_str + OSC_ENABLED):
                        pluginswrapper.setParamByName(param_str + OSC_ENABLED, 1.0)
                        command.handle("Vital: Enable oscillator " + str(osc_num))
                    else:
                        pluginswrapper.setParamByName(param_str + OSC_ENABLED, 0.0)
                        selected_osc = 0
                        command.handle("Vital: Disable oscillator " + str(osc_num))
                
                else:
                    # If disabled
                    if not pluginswrapper.getParamByName(param_str + OSC_ENABLED):
                        pluginswrapper.setParamByName(param_str + OSC_ENABLED, 1.0)
                        selected_osc = osc_num
                        command.handle("Vital: Enable oscillator " + str(osc_num))
                    else:
                        selected_osc = osc_num
                        command.handle("Vital: Select oscillator " + str(osc_num))
            
            else:
                command.handle("Pads catch-all", 1)
        else:
            command.handle("Handle presses", 1)
    # No oscilator selected
    if selected_osc == 0:
        return

    if command.type is eventconsts.TYPE_BASIC_FADER:
        if command.coord_X == 0:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + OSC_WAVE_FRAME, 
                                    command.value, -1, prev_param_index)
            command.handle("Wave frame", 1)
            
        elif command.coord_X == 1:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + OSC_UNISON, 
                                    command.value, -1, prev_param_index)
            command.handle("Unison voices", 1)
            
        elif command.coord_X == 2:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + OSC_DETUNE, 
                                    command.value, -1, prev_param_index)
            command.handle("Detune", 1)
            
    elif command.type is eventconsts.TYPE_BASIC_KNOB:
        if command.coord_X == 0:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + OSC_LEVEL, 
                                    command.value, -1, prev_param_index)
            command.handle("Level", 1)
        elif command.coord_X == 1:
            pluginswrapper.setParamByName(
                                    param_str + OSC_PAN, 
                                    command.value, -1, prev_param_index)
            command.handle("Pan", 1)
        elif command.coord_X == 2:
            prev_param_index = pluginswrapper.setParamByName(
                                    param_str + OSC_FREQUENCY_MORPH, 
                                    command.value, -1, prev_param_index)
            command.handle("Frequency Morph", 1)
        elif command.coord_X == 3:
            pluginswrapper.setParamByName(
                                    param_str + OSC_DISTORTION, 
                                    command.value, -1, prev_param_index)
            command.handle("Distortion", 1)
    
def redrawOsc(lights):
    global selected_osc
    
    for osc in range(0, NUM_OSCS):
        param_str =  OSCILLATOR + " " + str(osc + 1) + " " + OSC_ENABLED
        if pluginswrapper.getParamByName(param_str):
            if osc + 1 == selected_osc:
                lights.setPadColour(osc, 1, lightingconsts.colours["RED"])
            else:
                lights.setPadColour(osc, 1, lightingconsts.colours["PURPLE"])
        else:
            if osc == selected_osc:
                selected_osc = 0
            
            lights.setPadColour(osc, 1, lightingconsts.colours["DARK GREY"])


#
# Filter
#

FILTER = "Filter"
NUM_FILTERS = 2

selected_filter = 1

FILTER_ENABLED = "Switch"

#
# Overall functions
#

current_selection = ""

SELECTIONS = [OSCILLATOR, FILTER]

def topPluginStart():
    """Called when plugin is top plugin (not neccesarily focused)
    """
    global current_selection
    
    # Only in extended mode: uncomment lines to set inControl mode
    if internal.getPortExtended():
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS) # Faders
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS) # Knobs
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS) # Pads
        pass
    
    if current_selection ==  "":
        current_selection = OSCILLATOR
    
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
    
    redrawOsc(lights)
    
    return

def process(command):
    """Called when processing commands. 

    Args:
        command (ParsedEvent): contains useful information about the event. 
            Use this to determing what actions your processor will take.
    """
    global current_selection
    
    
    # Add event processor to actions list (useful for debugging)
    command.actions.addProcessor("Vital Processor")

    if command.type == eventconsts.TYPE_BASIC_PAD:
        if command.coord_Y == 0:
            if command.coord_X < len(SELECTIONS):
                current_selection = SELECTIONS[command.coord_X]
                command.handle("Select: " + SELECTIONS[command.coord_X])

            else:
                command.handle("Lower pads catch-all")

    if command.handled: return

    if current_selection == OSCILLATOR:
        processOsc(command)
    elif current_selection == FILTER:
        pass

    return

def beatChange(beat):
    pass
