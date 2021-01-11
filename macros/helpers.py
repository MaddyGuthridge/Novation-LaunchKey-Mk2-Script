"""
macros > helpers.py

Provides helper functions for running macros

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import time

import ui

import lighting
import lightingconsts

# Time to sleep for after macro finished
POST_SLEEP_TIME = 0.5

def setProgress(major, minor=0.0, major_colour=lightingconsts.colours["WHITE"], minor_colour=lightingconsts.colours["DARK GREY"]):
    """Displays lights on the controller indicating the progress of the macro.

    Args:
        major (float): Progress of the overall operation. Between 0 and 1.
        minor (float, optional): Progress of a sub-operation. Between 0 and 1. Defaults to 0.0.
        major_colour (int, optional): Colour of major progress meter. Defaults to white.
        minor_colour (int, optional): Colour of minor progress meter. Defaults to dark grey.
    """
    
    major_i = major * 8
    for i in range(8):
        if major_i >= i:
            lighting.state.setPadColour(i, 0, major_colour)
        else:
            lighting.state.setPadColour(i, 0, lightingconsts.colours["OFF"])
    
    minor_i = minor * 8
    for i in range(8):
        if minor_i >= i:
            lighting.state.setPadColour(i, 1, minor_colour)
        else:
            lighting.state.setPadColour(i, 1, lightingconsts.colours["OFF"])
    
    ui.setHintMsg("Macro progress: " + str(round(major * 100)) + "%")

def runMacro(name):
    """Runs a macro given its name

    Args:
        name (str): name of module to lead and run the macro from
    """
    
    start = time.time()
    try:
        m = __import__("macros." + name)
    except Exception as e:
        print("Error importing macro")
        print(e)
        
        for x in range(8):
            for y in range(2):
                lighting.state.setPadColour(x, y, lightingconsts.colours["RED"], override=True)
        time.sleep(POST_SLEEP_TIME)
        return
    
    try:
        getattr(m, name).run()
    except Exception as e:
        print("Error running macro")
        print(e)
        
        for x in range(8):
            for y in range(2):
                lighting.state.setPadColour(x, y, lightingconsts.colours["ORANGE"], override=True)
        time.sleep(POST_SLEEP_TIME)
        return
    
    end = time.time()
    
    print("Macro executed in " + str(round(end - start, 3)) + " seconds")
    for x in range(8):
        for y in range(2):
            lighting.state.setPadColour(x, y, lightingconsts.colours["GREEN"], override=True)
    time.sleep(POST_SLEEP_TIME)
    