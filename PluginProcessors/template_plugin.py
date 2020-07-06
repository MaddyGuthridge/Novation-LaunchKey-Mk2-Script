"""
template_plugin.py
The file acts as a template for plugin handlers. Copy it and edit to add your own plugin handlers.
To get it to be imported by the event processor, add its filename (without the .py) to processplugins.py

"""

# Add names of plugins your script can process to this list
plugins = []


# Import any modules you might need
import config
import internal
import eventconsts
import eventprocessor
import lighting


# Called when plugin is top plugin (not neccesarily focused)
def topPluginStart():
    # Only in extended mode: uncomment lines to set inControl mode
    if internal.extendedMode.query():
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_FADERS) # Faders
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_KNOBS) # Knobs
        # internal.extendedMode.setVal(False, eventconsts.INCONTROL_PADS) # Pads
        pointless_variable = "BOTTOM TEXT"  # Need this here when everything is commented or Python throws a hissy fit. 
                                            # Feel free to delete.
    return

# Called when plugin is no longer top plugin (not neccesarily focused)
def topPluginEnd():
    # Only in extended mode: uncomment lines to revert to previous inControl modes
    if internal.extendedMode.query():
        # internal.extendedMode.revert(eventconsts.INCONTROL_FADERS) # Faders
        # internal.extendedMode.revert(eventconsts.INCONTROL_KNOBS) # Knobs
        # internal.extendedMode.revert(eventconsts.INCONTROL_PADS) # Pads
        pointless_variable = "BOTTOM TEXT"  # Need this here when everything is commented or Python throws a hissy fit. 
                                            # Feel free to delete.
    return

# Called when plugin brought to foreground (focused)
def activeStart():
    
    return

# Called when plugin no longer in foreground (end of focused)
def activeEnd():
    
    return

# Called when redrawing UI on pads. Set colours of lights here.
def redraw(lights):
    return

# Called when processing commands. 
def process(command):
    # Add event processor to actions list (useful for debugging)
    command.actions.addProcessor("Your Processor Name")

    # When you handle your events, use command.actions.appendAction to log what you did,
    # and if you want processing to be finished, set command.handled to true

    # Add did not handle flag if not handled
    if command.handled is False: 
        command.actions.appendAction("[Did not handle]")
    return


