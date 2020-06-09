"""
eventprocessor.py
This file processes events and returns objects for events.

"""

import eventconsts
import internal

# Define contant for determining button presses and knob/fader motions
BUTTON_PRESS = 1
KNOB_FADER = 2

class processedEvent:
    def __init__(self, event):
        print("Creating processed event class")

        self.type = BUTTON_PRESS

        self.is_long_press = False
        self.is_Lift = True

        self.value = event.data2
    
    
# Internal functions

# Convert between Extended Mode pad mappings and Basic Mode pad mappings
def convertPadMapping(padNumber):
    if padNumber is eventconsts.PAD_TOP_1: return eventconsts.BASIC_PAD_TOP_1
    elif padNumber is eventconsts.PAD_TOP_2: return eventconsts.BASIC_PAD_TOP_2
    elif padNumber is eventconsts.PAD_TOP_3: return eventconsts.BASIC_PAD_TOP_3
    elif padNumber is eventconsts.PAD_TOP_4: return eventconsts.BASIC_PAD_TOP_4
    elif padNumber is eventconsts.PAD_TOP_5: return eventconsts.BASIC_PAD_TOP_5
    elif padNumber is eventconsts.PAD_TOP_6: return eventconsts.BASIC_PAD_TOP_6
    elif padNumber is eventconsts.PAD_TOP_7: return eventconsts.BASIC_PAD_TOP_7
    elif padNumber is eventconsts.PAD_TOP_8: return eventconsts.BASIC_PAD_TOP_8
    elif padNumber is eventconsts.PAD_BOTTOM_1: return eventconsts.BASIC_PAD_BOTTOM_1
    elif padNumber is eventconsts.PAD_BOTTOM_2: return eventconsts.BASIC_PAD_BOTTOM_2
    elif padNumber is eventconsts.PAD_BOTTOM_3: return eventconsts.BASIC_PAD_BOTTOM_3
    elif padNumber is eventconsts.PAD_BOTTOM_4: return eventconsts.BASIC_PAD_BOTTOM_4
    elif padNumber is eventconsts.PAD_BOTTOM_5: return eventconsts.BASIC_PAD_BOTTOM_5
    elif padNumber is eventconsts.PAD_BOTTOM_7: return eventconsts.BASIC_PAD_BOTTOM_7
    elif padNumber is eventconsts.PAD_BOTTOM_8: return eventconsts.BASIC_PAD_BOTTOM_8
    elif padNumber is eventconsts.PAD_TOP_BUTTON: return eventconsts.BASIC_PAD_TOP_BUTTON
    elif padNumber is eventconsts.PAD_BOTTOM_BUTTON: return eventconsts.BASIC_PAD_BOTTOM_BUTTON
    internal.logError("Pad number not defined")
