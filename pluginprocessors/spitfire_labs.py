"""
pluginprocessors > spitfire_labs.py

This processor links parameters for the Spitfire Labs plugin

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

# Add names of plugins your script can process to this list
PLUGINS = ["LABS"]


# Import any modules you might need\
import plugins
import config
import internal
import eventconsts
import eventprocessor
import lightingconsts
import processorhelpers

# Constants for event remapping
EXPRESSION = 0
DYNAMICS = 1


def topPluginStart():
    """Called when plugin is top plugin (not neccesarily focused)
    """
    
    # Only in extended mode: uncomment lines to set inControl mode
    if internal.getPortExtended():
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS) # Faders
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS) # Knobs
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS) # Pads
        pass
    return

def topPluginEnd():
    """Called when plugin is no longer top plugin (not neccesarily focused)
    """
    
    # Only in extended mode: uncomment lines to revert to previous inControl modes
    if internal.getPortExtended():
        # internal.extendedMode.revert(eventconsts.INCONTROL_FADERS) # Faders
        # internal.extendedMode.revert(eventconsts.INCONTROL_KNOBS) # Knobs
        # internal.extendedMode.revert(eventconsts.INCONTROL_PADS) # Pads
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
    command.actions.addProcessor("Labs Processor")

    # When you handle your events, use command.handle("Some action") to handle events.

    return


