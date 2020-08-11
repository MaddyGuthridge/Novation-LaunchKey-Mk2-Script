"""
lightingconsts.py

This file contains constants regarding lights. It is reorganised into objects so as to allow for colour mapping to match FL Colours.

Author: Miguel Guthridge
"""

import math

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
    
    def getClosestName(self, rgb):
        """Returns name of closest colour in colour set

        Args:
            rgb (int): RGB colour

        Returns:
            str: colour name (key)
        """
                
        # Trim unnessesary data (bitwise and with 3-bytes of 1)
        rgb = rgb&((1 << 24) - 1)
                
        # Extract r, g, b values
        r = rgb >> 16
        g = (rgb >> 8) - (r << 8)
        b = rgb - (g << 8) - (r << 16)
        
        # Loop over each colour to get the closest one
        min_distance = math.inf
        min_distance_name= None
        for name_check, rgb_check in self.rgb_colours.items():
            
            # Extract r, g, b values
            r_check = rgb_check >> 16
            g_check = (rgb_check >> 8) - (r_check << 8)
            b_check = rgb_check - (g_check << 8) - (r_check << 16)
            
            # Use distance formula to get closest colour in RGB space
            distance = math.sqrt( (r - r_check)**2 + (g - g_check)**2 + (b - b_check)**2 )
            
            if distance < min_distance:
                min_distance = distance
                min_distance_name = name_check
        
        return min_distance_name
    
    def getClosestInt(self, rgb):
        """Returns internal value of closest colour in colour set

        Args:
            rgb (int): RGB colour

        Returns:
            int: colour internal number
        """
        return self.int_colours[self.getClosestName(rgb)]
    
    def getClosestRgb(self, rgb):
        """Returns rgb of closest colour in colour set

        Args:
            rgb (int): RGB colour

        Returns:
            int: colour rgb
        """
        return self.rgb_colours[self.getClosestName(rgb)]



colours = ColourContainer()

colours.addColour("OFF", 0, 0x000000)
colours.addColour("TRANSPARENT", -1, 0x000000)
colours.addColour("WHITE", 3, 0xFFFFFF)

colours.addColour("RED", 5, 0x94323E)
colours.addColour("GREEN", 25, 0x289536)
colours.addColour("TEAL", 77, 0x4A958C)
colours.addColour("PINK", 53, 0xA05096)
colours.addColour("BLUE", 45, 0x3C69B4)
colours.addColour("YELLOW", 13, 0xACAC39)
colours.addColour("PURPLE", 49, 0x6439AC)
colours.addColour("LILAC", 116, 0x8861CA)
colours.addColour("ORANGE", 84, 0xBF8F40)

colours.addColour("LIGHT YELLOW", 109, 0xD1D176)
colours.addColour("LIGHT BLUE", 37, 0x3F9EBE)
colours.addColour("LIGHT LILAC", 115, 0xB3A1D0)
colours.addColour("LIGHT LIGHT BLUE", 40, 0x98CCDD)

colours.addColour("DARK GREY", 1, 0x485156)
colours.addColour("DARK PURPLE", 51, 0x48297B)
colours.addColour("DARK BLUE", 47, 0x323294)
colours.addColour("DARK RED", 59, 0x602028)


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
