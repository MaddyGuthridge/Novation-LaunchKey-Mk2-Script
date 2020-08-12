"""
windowprocessors > processdefault.py

This script can be used as a template for window scripts.

Author: Miguel Guthridge
"""





def activeStart():
    """Called when this window becomes the top-most window or plugin
    """
    return

def activeEnd():
    """Called when this window is no-longer the top-most window or plugin
    """
    return

def topWindowStart():
    """Called when this window becomes the top-most FL Studio window
    """
    return

def topWindowEnd():
    """Called when this window is no-longer the top-most FL Studio window (ie another FL window is now active)
    """
    return

def redraw(lights):
    """Called during onIdle() to refresh lighting.

    Args:
        lights (LightMap): set pad colours and states to control the colours of them.
    """
    return

def process(command):
    """Called to process an event.

    Args:
        command (ParsedEvent): object containing data about the event and the actions taken to handle it.
    """
    #command.actions.addProcessor("[None] Processor")

    return