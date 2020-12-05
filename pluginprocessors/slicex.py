"""
pluginprocessors > slicex.py

The file processes events and redraws lights when the Slicex or Fruity Slicer plugin is active.
It remaps the drum pads to play slices in each of them.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

# Add names of plugins your script can process to this list
PLUGINS = ["Slicex", "Fruity Slicer"]


# Import any modules you might need
import config
import internal
import eventconsts
import eventprocessor
import lightingconsts
import processorhelpers


def topPluginStart():
    """Called when plugin is top plugin (not neccesarily focused)
    """
    
    # Only in extended mode: uncomment lines to set inControl mode
    if internal.getPortExtended():
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS) # Faders
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS) # Knobs
        internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS) # Pads
        pass
    return

def topPluginEnd():
    """Called when plugin is no longer top plugin (not neccesarily focused)
    """
    
    # Only in extended mode: uncomment lines to revert to previous inControl modes
    if internal.getPortExtended():
        # internal.extendedMode.revert(eventconsts.INCONTROL_FADERS) # Faders
        # internal.extendedMode.revert(eventconsts.INCONTROL_KNOBS) # Knobs
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
    if internal.window.active_plugin == "Slicex":
        colour = lightingconsts.colours["ORANGE"]
    else:
        colour = lightingconsts.colours["DULL BLUE"]
    
    processorhelpers.keyswitches.redraw(lights, colour, -1, -1, 0)

def process(command):
    """Called when processing commands. 

    Args:
        command (ParsedEvent): contains useful information about the event. 
            Use this to determing what actions your processor will take.
    """
    
    # Add event processor to actions list (useful for debugging)
    command.actions.addProcessor("Slicex Processor")

    if command.type == eventconsts.TYPE_BASIC_PAD and command.coord_Y == 1:
        keyswitch_num = processorhelpers.keyswitches.getNum(command.coord_X, command.coord_Y, -1, -1, 0)

        if internal.window.active_plugin == "Slicex":
            keyswitch_num += 60
        
        command.edit(processorhelpers.RawEvent(0x90, keyswitch_num, command.value), "Remap keyswitches")

    return

def beatChange(beat):
    pass
