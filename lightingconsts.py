"""
lightingconsts.py

This file contains constants regarding lights. It is reorganised into objects so as to allow for colour mapping to match FL Colours.

Author: Miguel Guthridge
"""

MODE_OFF = 0
MODE_ON = 1
MODE_PULSE = 2

class ColourContainer:
    """Object that basic colours are stored in. Will have functionality to search by name or RGB value.
    """
    
    int_colours = dict()
    
    rgb_colours = dict()
    
    def addColour(self, name, int_val, rgb):
        """Adds a colour to the list

        Args:
            name (str): Name of colour, used as key in dictionaries
            int_val (int): colour on keyboard
            rgb (int): RGB value
        """
        self.int_colours[name] = int_val
        self.rgb_colours[name] = rgb
        
    def getColourByName(self, name):
        """Returns details of colour

        Args:
            name (str): Name of colour

        Returns:
            tuple:
                int: int_colour
                int: rgb_clour
        """
        return (self.int_colours[name], self.rgb_colours[name])
    
    def __getitem__(self, key):
        """Get internal colour

        Args:
            key (str): Key (name of colour)

        Returns:
            int: internal colour
        """
        return self.int_colours[key]
    
colours = ColourContainer()

colours.addColour("OFF", 0, 0x000000)
colours.addColour("TRANSPARENT", -1, 0x000000)
colours.addColour("WHITE", 3, 0xFFFFFF)

colours.addColour("RED", 5, 0xFF2900)
colours.addColour("GREEN", 25, 0xFF2900)
colours.addColour("PINK", 53, 0xFF40FF)
colours.addColour("BLUE", 45, 0x0433FF)
colours.addColour("YELLOW", 13, 0x0433FF)
colours.addColour("PURPLE", 49, 0x6435FF)
colours.addColour("LILAC", 116, 0x9E7DFF)
colours.addColour("ORANGE", 84, 0x9E7DFF)

colours.addColour("LIGHT YELLOW", 109, 0xFFE400)
colours.addColour("LIGHT BLUE", 37, 0x00B7FF)
colours.addColour("LIGHT_LILAC", 115, 0xA7ABFF)
colours.addColour("LIGHT LIGHT BLUE", 40, 0x509CFF)

colours.addColour("DARK GREY", 1, 0x509CFF)
colours.addColour("DARK PURPLE", 51, 0x0C0641)
colours.addColour("DARK BLUE", 47, 0x0C0641)
colours.addColour("DARK RED", 59, 0x0C0641)

# Define colour pallettes used by light show
PALLETE_NORMAL = [
    colours["RED"], colours["PINK"], colours["PURPLE"], colours["BLUE"], 
    colours["LIGHT BLUE"], colours["GREEN"], colours["YELLOW"], colours["ORANGE"], colours["OFF"]
    ]
PALLETE_INIT_FAIL = [
    colours["YELLOW"], colours["ORANGE"], colours["ORANGE"], colours["RED"], 
    colours["RED"], colours["ORANGE"], colours["ORANGE"], colours["YELLOW"], colours["OFF"]
    ] 
PALLETE_UPDATE = [
    colours["BLUE"], colours["LIGHT BLUE"], colours["LIGHT BLUE"], colours["GREEN"], 
    colours["GREEN"], colours["LIGHT BLUE"], colours["LIGHT BLUE"], colours["BLUE"], colours["OFF"]
    ] 

# Define UI colours
UI_NAV_VERTICAL = colours["LIGHT BLUE"]
UI_NAV_HORIZONTAL = colours["PURPLE"]
UI_ZOOM = colours["BLUE"]
UI_ACCEPT = colours["GREEN"]
UI_REJECT = colours["RED"]
UI_CHOOSE = colours["PURPLE"]

UI_UNDO = colours["LIGHT LIGHT BLUE"]
UI_REDO = colours["LIGHT BLUE"]

UI_COPY = colours["BLUE"]
UI_CUT = colours["LIGHT BLUE"]
UI_PASTE = colours["GREEN"]

UI_SAVE = colours["GREEN"]

# Define tool colours
TOOL_PENCIL = colours["ORANGE"]
TOOL_BRUSH = colours["LIGHT BLUE"]
TOOL_DELETE = colours["RED"]
TOOL_MUTE = colours["PINK"]
TOOL_SLIP = colours["ORANGE"]
TOOL_SLICE = colours["LIGHT BLUE"]
TOOL_SELECT = colours["YELLOW"]
TOOL_ZOOM = colours["BLUE"]
TOOL_PLAYBACK = colours["GREEN"]

# Define Window Colours
WINDOW_PLAYLIST = colours["GREEN"]
WINDOW_CHANNEL_RACK = colours["RED"]
WINDOW_PIANO_ROLL = colours["PINK"]
WINDOW_MIXER = colours["LIGHT BLUE"]
WINDOW_BROWSER = colours["ORANGE"]
WINDOW_PLUGIN_PICKER = colours["BLUE"]

# Define Beat Indicator Colours
BEAT_PAT_BAR = colours["RED"]
BEAT_PAT_BEAT = colours["ORANGE"]
BEAT_SONG_BAR = colours["LIGHT BLUE"]
BEAT_SONG_BEAT = colours["GREEN"]

TEMPO_TAP = colours["PINK"]
METRONOME = colours["DARK GREY"]

# Colour Matrix for errors
ERROR_COLOURS = [
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]],
    [colours["RED"], colours["RED"]]
]
