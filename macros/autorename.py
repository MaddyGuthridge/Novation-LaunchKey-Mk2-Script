"""macros > autorename.py

This script renames all content using some specified parameters.
It can be run by calling the run() function.

Author: Miguel Guthridge
"""

# How many leading characters to remove
TRIM_FIRST = 0

# Leading characters to remove if present
TRIM_FIRST_CHARS = "Lullaby Stems_"

# How many ending characters to remove
TRIM_END = 0

# Ending characters to remove if present
TRIM_END_CHARS = ""

# List of characters to replace. Each element should be a tuple containing the character to find and the character to replace it with
CHARACTER_REPLACEMENTS = [("_", " ")]

# Whether to capitalise first letters of words
CAPITALISE_FIRST_LETTERS = False

CHANGE_PATTERNS = True
CHANGE_PLAYLIST_TRACKS = True
CHANGE_CHANNELS = True
CHANGE_MIXER_TRACKS = True

import channels
import mixer
import playlist
import patterns
import general

def getNewName(name):
    # Trim starts and ends
    if len(name) > (TRIM_FIRST + TRIM_END):
        if TRIM_END:
            name = name[ TRIM_FIRST : -TRIM_END ]
        else:
            name = name[ TRIM_FIRST : ]
    else:
        name = ""
    
    # Trim first and ending chars
    if name[ : len(TRIM_FIRST_CHARS) ] == TRIM_FIRST_CHARS and len(TRIM_FIRST_CHARS):
        name = name[ len(TRIM_FIRST_CHARS) : ]
    
    if name[ -len(TRIM_END_CHARS) : ] == TRIM_END_CHARS and len(TRIM_END_CHARS):
        name = name[ : -len(TRIM_END_CHARS) ]
    
    # Make character replacements
    for replacement in CHARACTER_REPLACEMENTS:
        for i in range(len(name)):
            if name[i] == replacement[0]:
                if i != len(name):
                    name = name[ : i] + replacement[1] + name[i + 1 : ]
                else:
                    name = name[ : i] + replacement[1]
    
    # Set to Title Case
    if CAPITALISE_FIRST_LETTERS:
        name = name.title()
    
    return name

def run():
    if CHANGE_PATTERNS:
        for i in range(1, patterns.patternCount() + 1):
            patterns.setPatternName(i, getNewName(patterns.getPatternName(i)))
    
    if CHANGE_PLAYLIST_TRACKS:
        for i in range(playlist.trackCount()):
            playlist.setTrackName(i, getNewName(playlist.getTrackName(i)))
    
    if CHANGE_CHANNELS:
        for i in range(channels.channelCount(1)):
            try:
                channels.setChannelName(i, getNewName(channels.getChannelName(i)))
            except:
                print("An index out of range error occurred. Change the Channel Rack's display filter to 'All'.")
    
    if CHANGE_MIXER_TRACKS:
        for i in range(mixer.trackCount()):
            mixer.setTrackName(i, getNewName(mixer.getTrackName(i)))
    
    # This doesn't do anything for some reason
    general.saveUndo("Run autorename Script", 0)
    
    
