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
# Macros
#

MACRO = "Macro"
NUM_MACROS = 4

def processMacros(command):
    global prev_param_index
    if command.type == eventconsts.TYPE_BASIC_FADER and command.coord_X < NUM_MACROS:
        param_str = MACRO + " " + str(command.coord_X + 1)
        prev_param_index = pluginswrapper.setParamByName(
                                param_str, 
                                command.value, -1, prev_param_index)
        command.handle("Set macro", 1)

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

FILTER_BLEND = "Blend"
FILTER_CUT = "Cutoff"
FILTER_RESONANCE = "Resonance"

FILTER_DRIVE = "Drive"
FILTER_MIX = "Mix"
FILTER_KEY = "Key Track"

def processFilter(command):
    global prev_param_index, selected_filter
    
    param_str =  FILTER + " " + str(selected_filter) + " "
    
    if not pluginswrapper.getParamByName(param_str + FILTER_ENABLED):
        selected_filter = 0
        
    if command.type is eventconsts.TYPE_BASIC_PAD and command.coord_Y == 1:
        # Change filters
        if command.coord_X < NUM_FILTERS:
            filter_num = command.coord_X + 1
            param_str = FILTER + " " + str(filter_num) + " "
            
            # Acting on selected filter
            if filter_num == selected_filter:
                # If disabled
                if not pluginswrapper.getParamByName(param_str + FILTER_ENABLED):
                    pluginswrapper.setParamByName(param_str + FILTER_ENABLED, 1.0)
                    command.handle("Vital: Enable filter " + str(filter_num))
                else:
                    pluginswrapper.setParamByName(param_str + FILTER_ENABLED, 0.0)
                    selected_osc = 0
                    command.handle("Vital: Disable filter " + str(filter_num))
            
            else:
                # If disabled
                if not pluginswrapper.getParamByName(param_str + FILTER_ENABLED):
                    pluginswrapper.setParamByName(param_str + FILTER_ENABLED, 1.0)
                    selected_filter = filter_num
                    command.handle("Vital: Enable filter " + str(filter_num))
                else:
                    selected_filter = filter_num
                    command.handle("Vital: Select filter " + str(filter_num))
        
        else:
            command.handle("Pads catch-all", 1)
        
    # No filter selected
    if selected_filter == 0:
        return

    if command.type == eventconsts.TYPE_BASIC_FADER:
        if command.coord_X == 0:
            prev_param_index = pluginswrapper.setParamByName(param_str + FILTER_BLEND, command.value, -1, prev_param_index)
            command.handle("Set filter blend", 1)
        elif command.coord_X == 1:
            prev_param_index = pluginswrapper.setParamByName(param_str + FILTER_CUT, command.value, -1, prev_param_index)
            command.handle("Set filter cut", 1)
        elif command.coord_X == 2:
            prev_param_index = pluginswrapper.setParamByName(param_str + FILTER_RESONANCE, command.value, -1, prev_param_index)
            command.handle("Set filter resonance", 1)
    
    elif command.type ==  eventconsts.TYPE_BASIC_KNOB:
        if command.coord_X == 0:
            prev_param_index = pluginswrapper.setParamByName(param_str + FILTER_DRIVE, command.value, -1, prev_param_index)
            command.handle("Set filter drive", 1)
        elif command.coord_X == 1:
            prev_param_index = pluginswrapper.setParamByName(param_str + FILTER_MIX, command.value, -1, prev_param_index)
            command.handle("Set filter mix", 1)
        elif command.coord_X == 2:
            prev_param_index = pluginswrapper.setParamByName(param_str + FILTER_KEY, command.value, -1, prev_param_index)
            command.handle("Set filter key tracking", 1)
    

def redrawFilter(lights):
    global selected_filter
    
    for i in range(0, NUM_FILTERS):
        param_str =  FILTER + " " + str(i + 1) + " " + FILTER_ENABLED
        if pluginswrapper.getParamByName(param_str):
            if i + 1 == selected_filter:
                lights.setPadColour(i, 1, lightingconsts.colours["RED"])
            else:
                lights.setPadColour(i, 1, lightingconsts.colours["ORANGE"])
        else:
            if i == selected_filter:
                selected_filter = 0
            
            lights.setPadColour(i, 1, lightingconsts.colours["DARK GREY"])

#
# Envelopes
#

ENVELOPE = "Envelope"
NUM_ENVELOPES = 6

selected_envelope = 1

ENVELOPE_ENABLED = "Switch"

ENV_DELAY = "Delay"
ENV_ATTACK = "Attack"
ENV_HOLD = "Hold"
ENV_DECAY = "Decay"
ENV_SUSTAIN = "Sustain"
ENV_RELEASE = "Release"

ENV_KNOBS = [ENV_DELAY, ENV_ATTACK, ENV_HOLD, ENV_DECAY, ENV_SUSTAIN, ENV_RELEASE]

def processEnv(command):
    global prev_param_index, selected_envelope
    
    param_str =  ENVELOPE + " " + str(selected_envelope) + " "
        
    if command.type is eventconsts.TYPE_BASIC_PAD and command.coord_Y == 1:
        # Change envelopes
        if command.coord_X < NUM_ENVELOPES:
            selected_envelope = command.coord_X + 1
            command.handle("Select envelope")
        
        else:
            command.handle("Pads catch-all", 1)

    if command.type == eventconsts.TYPE_BASIC_KNOB:
        if command.coord_X < len(ENV_KNOBS):
            prev_param_index = pluginswrapper.setParamByName(param_str + ENV_KNOBS[command.coord_X], command.value, -1, prev_param_index)
            command.handle("Set envelope " + ENV_KNOBS[command.coord_X], 1)
        

def redrawEnv(lights):
    global selected_envelope
    
    for i in range(0, NUM_ENVELOPES):
        if i + 1 == selected_envelope:
            lights.setPadColour(i, 1, lightingconsts.colours["TEAL"])
        else:
            lights.setPadColour(i, 1, lightingconsts.colours["DARK GREY"])

#
# Overall functions
#

# Default selection is macros
current_selection = MACRO

SELECTIONS = [MACRO, OSCILLATOR, FILTER, ENVELOPE]
SELECTION_COLOURS = [lightingconsts.colours["LIGHT BLUE"], lightingconsts.colours["PURPLE"], lightingconsts.colours["ORANGE"], lightingconsts.colours["TEAL"]]

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
    
    if internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        return
    
    for i in range(len(SELECTIONS)):
        if SELECTIONS[i] == current_selection:
            lights.setPadColour(i, 0, lightingconsts.colours["DARK GREY"])
        else:
            lights.setPadColour(i, 0, SELECTION_COLOURS[i])
    
    
    if current_selection == OSCILLATOR:
        redrawOsc(lights)
    elif current_selection == FILTER:
        redrawFilter(lights)
    elif current_selection == ENVELOPE:
        redrawEnv(lights)
    
    lights.solidifyAll()
    
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
        if command.is_lift:
            command.handle("Handle presses")
        
        if command.coord_Y == 0:
            if command.coord_X < len(SELECTIONS):
                current_selection = SELECTIONS[command.coord_X]
                command.handle("Select: " + SELECTIONS[command.coord_X])

            else:
                command.handle("Upper pads catch-all")

    if command.handled: return

    if current_selection == MACRO:
        processMacros(command)
    elif current_selection == OSCILLATOR:
        processOsc(command)
    elif current_selection == FILTER:
        processFilter(command)
    elif current_selection == ENVELOPE:
        processEnv(command)

    if command.type == eventconsts.TYPE_BASIC_PAD:
        command.handle("Pads catch-all", 1)

    return

def beatChange(beat):
    pass
