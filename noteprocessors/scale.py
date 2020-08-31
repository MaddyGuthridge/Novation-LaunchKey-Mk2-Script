"""
noteprocessors > scale.py

This script snaps notes to the closest note in a scale.

Author: Miguel Guthridge
"""

import internal.consts
import eventconsts
import internal
import processorhelpers
import lightingconsts



# The name of your mode
NAME = "Scale Snapping"

# The colour used to represent your mode
DEFAULT_COLOUR = lightingconsts.colours["YELLOW"]

# The colour while active
COLOUR = lightingconsts.colours["YELLOW"]
CURRENT_SCALE_COLOUR = lightingconsts.colours["YELLOW"]

# Whether your mode should be unlisted in the note mode menu
SILENT = False

FORWARD_NOTES = True

INIT_COMPLETE = False

#------------------------
# Define scale types
#------------------------

class Scale:
    """Container for scales
    """
    def __init__(self, name, colour, scale):
        self.name = name
        self.colour = colour
        self.scale = scale

class ScaleClass:
    """Container for classes of scale (contains scales)
    """
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour
        self.scale_list = []
        
    def addScale(self, name, colour, scale):
        self.scale_list.append(Scale(name, colour, scale))
        
class ScaleMgr:
    """Container for scale classes (contains ScaleClass objects)
    """
    def __init__(self):
        self.scale_class_list = []
        
    def addScaleClass(self, name, colour):
        self.scale_class_list.append(ScaleClass(name, colour))
    
    def addScale(self, name, colour, scale):
        self.scale_class_list[-1].addScale(name, colour, scale)

scales = ScaleMgr()

scales.addScaleClass("Major", lightingconsts.colours["YELLOW"])
scales.addScale("Major", lightingconsts.colours["YELLOW"], [0, 2, 4, 5, 7, 9, 11])
scales.addScale("Wholetone", lightingconsts.colours["TEAL"], [0, 2, 4, 6, 8, 10])

scales.addScaleClass("Minor", lightingconsts.colours["ORANGE"])
scales.addScale("Natural Minor", lightingconsts.colours["ORANGE"], [0, 2, 3, 5, 7, 8, 10])
scales.addScale("Harmonic Minor", lightingconsts.colours["RED"], [0, 2, 3, 5, 7, 8, 11])
scales.addScale("Melodic Minor", lightingconsts.colours["PINK"], [0, 2, 3, 5, 7, 9, 11])

scales.addScaleClass("Blues", lightingconsts.colours["LIGHT BLUE"])
scales.addScale("Major Blues", lightingconsts.colours["LIGHT BLUE"], [0, 2, 3, 4, 7, 9])
scales.addScale("Minor Blues", lightingconsts.colours["BLUE"], [0, 3, 5, 6, 7, 10])

scales.addScaleClass("Pentatonic", lightingconsts.colours["RED"])
scales.addScale("Major Pentatonic", lightingconsts.colours["YELLOW"], [0, 2, 4, 7, 9])
scales.addScale("Minor Pentatonic", lightingconsts.colours["RED"], [0, 3, 5, 7, 10])
scales.addScale("Ryukyu", lightingconsts.colours["PURPLE"], [0, 4, 5, 7, 11])

scales.addScaleClass("Non-western", lightingconsts.colours["BLUE"])
scales.addScale("Egyptian", lightingconsts.colours["ORANGE"], [0, 2, 5, 7, 10])
scales.addScale("Arabic", lightingconsts.colours["RED"], [0, 2, 4, 6, 8, 10])
scales.addScale("Gypsy", lightingconsts.colours["TEAL"], [0, 2, 3, 6, 7, 8, 11])

scales.addScaleClass("Modal", lightingconsts.colours["PURPLE"])
scales.addScale("Ionian", lightingconsts.colours["YELLOW"], [0, 2, 4, 5, 7, 9, 11])
scales.addScale("Dorian", lightingconsts.colours["PINK"], [0, 2, 3, 5, 7, 9, 10])
scales.addScale("Phrygian", lightingconsts.colours["LILAC"], [0, 1, 3, 5, 7, 8, 10])
scales.addScale("Lydian", lightingconsts.colours["GREEN"], [0, 2, 4, 6, 7, 9, 11])
scales.addScale("Mixolydian", lightingconsts.colours["TEAL"], [0, 2, 4, 5, 7, 9, 10])
scales.addScale("Aeolian", lightingconsts.colours["RED"], [0, 2, 3, 5, 7, 8, 10])
scales.addScale("Locrian", lightingconsts.colours["ORANGE"], [0, 1, 3, 5, 6, 8, 10])


INIT_HAVE_ROOT = False
INIT_HAVE_SCALE = False

CUSTOM_SCALE = False

SCALE_CLASS = -1

PREVENT_NONSCALE = False

ROOT_NOTE = 0
SCALE_TO_USE = []
SCALE_TO_USE_INDEX = -1

SNAP_NOTES = []

def setScale(root, scale_notes):
    global SNAP_NOTES
    for x in range(len(scale_notes)):
        scale_notes[x] = (scale_notes[x] + root) % 12
    scale_notes = sorted(scale_notes)
    
    SNAP_NOTES = [scale_notes[-1] - 12] + scale_notes + [scale_notes[0] + 12]


def process(command):
    """Called with an event to be processed by your note processor. Events aren't filtered so you'll want to make sure your processor checks that events are notes.

    Args:
        command (ParsedEvent): An event for your function to modify/act on.
    """
    command.addProcessor("Scale Processor")
    
    if not INIT_COMPLETE:
        processInit(command)
    
    # If command is a note
    elif command.type is eventconsts.TYPE_NOTE:
        if not command.is_lift:
            note  = command.note % 12
            octave = command.note // 12
                    
            if SNAP_NOTES == None:
                return
            
            closest_distance = 13
            closest_note = None
            closest_octave = 0
            for x in SNAP_NOTES:
                distance = abs(note - x)
                if distance < closest_distance:
                    closest_note = x
                    closest_distance = distance
                    if distance == 0:
                        break
                
            new_note = closest_note + octave*12 + closest_octave*12
            if PREVENT_NONSCALE and new_note != command.note:
                command.handle("Prevent non-scale note", True)
                return
            internal.notesDown.noteOn(processorhelpers.ExtensibleNote(command, [processorhelpers.RawEvent(command.status, new_note, command.value)]))
            command.handle("Snapped note on")
        else:
            internal.notesDown.noteOff(command)
            command.handle("Snapped note off")
    pass

def redraw(lights):
    """Called when a redraw is taking place. Use this to draw menus to allow your users to choose options. Most of the time, you should leave this empty.

    Args:
        lights (LightMap): The lights to draw to
    """
    global INIT_COMPLETE, SCALE_CLASS
    if not INIT_COMPLETE and internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        if not CUSTOM_SCALE:
            for ctr in range(min(len(scales.scale_class_list), 7)):
                if (ctr < internal.window.getAnimationTick() and SCALE_CLASS == -1) or SCALE_CLASS != -1:
                    colour = scales.scale_class_list[ctr].colour
                    if SCALE_CLASS == ctr:
                        pulse = lightingconsts.MODE_PULSE
                    else:
                        pulse = lightingconsts.MODE_ON
                    lights.setPadColour(ctr, 0, colour, pulse)
            
            if SCALE_CLASS != -1:
                if len(scales.scale_class_list[SCALE_CLASS].scale_list) > 1:
                    for ctr in range(min(len(scales.scale_class_list[SCALE_CLASS].scale_list), 8)):
                        if ctr >= internal.window.getAnimationTick():
                            break
                        colour = scales.scale_class_list[SCALE_CLASS].scale_list[ctr].colour
                        if SCALE_TO_USE_INDEX == ctr:
                            pulse = lightingconsts.MODE_PULSE
                        else:
                            pulse = lightingconsts.MODE_ON
                        lights.setPadColour(ctr, 1, colour, pulse)
            else:
                colour = PREVENT_NONSCALE * lightingconsts.colours["RED"] \
                    + (not PREVENT_NONSCALE) * lightingconsts.colours["PINK"]
                lights.setPadColour(0, 1, colour)
        
        lights.setPadColour(7, 0, lightingconsts.colours["GREEN"])
        
        lights.solidifyAll()

def activeStart():
    """Called when your note mode is made active
    """
    internal.extendedMode.setVal(True, eventconsts.INCONTROL_PADS)

def activeEnd():
    """Called wen your note mode is no-longer active
    """
    global INIT_COMPLETE, INIT_HAVE_ROOT, INIT_HAVE_SCALE, SCALE_TO_USE, \
        ROOT_NOTE, FORWARD_NOTES, SCALE_CLASS, COLOUR, SCALE_TO_USE_INDEX, \
            CUSTOM_SCALE, PREVENT_NONSCALE
    
    INIT_COMPLETE = False
    INIT_HAVE_ROOT = False
    INIT_HAVE_SCALE = False
    FORWARD_NOTES = True
    SCALE_CLASS = -1
    COLOUR = DEFAULT_COLOUR
    SCALE_TO_USE_INDEX = -1
    CUSTOM_SCALE = False
    PREVENT_NONSCALE = False
    SCALE_TO_USE = []


def processInit(command):
    global INIT_COMPLETE, INIT_HAVE_ROOT, INIT_HAVE_SCALE, SCALE_TO_USE, ROOT_NOTE, \
        FORWARD_NOTES, SCALE_CLASS, COLOUR, CURRENT_SCALE_COLOUR, SCALE_TO_USE_INDEX, \
            CUSTOM_SCALE, PREVENT_NONSCALE
    if command.type == eventconsts.TYPE_PAD and command.is_lift:
        x, y = command.getPadCoord()
        
        if y == 0:
            if x == 7:
                internal.window.resetAnimationTick()
                if not CUSTOM_SCALE:
                    SCALE_CLASS = -1
                    CUSTOM_SCALE = True
                    command.handle("Entered custom scale mode")
                else:
                    if len(SCALE_TO_USE):
                        command.handle("Use custom scale")
                        # Enter scale mode
                        ROOT_NOTE = 0
                        INIT_HAVE_SCALE = True
                        INIT_HAVE_ROOT = True
                        CURRENT_SCALE_COLOUR = lightingconsts.colours["GREEN"]
                    else:
                        CUSTOM_SCALE = False
                        command.handle("Exited custom scale mode")
            
            elif x < len(scales.scale_class_list):
                if x == SCALE_CLASS:
                    SCALE_CLASS = -1
                    command.handle("Remove scale class")
                    return
                internal.window.resetAnimationTick()
                
                SCALE_CLASS = x
                SCALE_TO_USE_INDEX = -1
                command.handle("Set scale class to " + scales.scale_class_list[x].name)
                
                if len(scales.scale_class_list[SCALE_CLASS].scale_list) == 1:
                    INIT_HAVE_SCALE = True
                    SCALE_TO_USE = scales.scale_class_list[SCALE_CLASS].scale_list[0].scale
                    SCALE_TO_USE_INDEX = 0
                    command.handle("Set scale to " + scales.scale_class_list[SCALE_CLASS].scale_list[0].name)
                    CURRENT_SCALE_COLOUR = scales.scale_class_list[SCALE_CLASS].scale_list[0].colour
                
            else: command.handle("Catch-all", silent=True)
        
        if y == 1:
            if SCALE_CLASS != -1:
                if x < len(scales.scale_class_list[SCALE_CLASS].scale_list):
                    INIT_HAVE_SCALE = True
                    SCALE_TO_USE = scales.scale_class_list[SCALE_CLASS].scale_list[x].scale
                    SCALE_TO_USE_INDEX = x
                    command.handle("Set scale to " + scales.scale_class_list[SCALE_CLASS].scale_list[x].name)
                    CURRENT_SCALE_COLOUR = scales.scale_class_list[SCALE_CLASS].scale_list[x].colour
                else: command.handle("Catch-all", silent=True)
            else:
                if x == 0:
                    PREVENT_NONSCALE = not PREVENT_NONSCALE
                    command.handle("Toggle prevention of non-scale notes")
                else: command.handle("Catch-all", silent=True)
            
    if command.type == eventconsts.TYPE_NOTE and command.is_lift:
        if CUSTOM_SCALE:
            note = command.note % 12
            if not note in SCALE_TO_USE:
                SCALE_TO_USE.append(note)
            command.act("Add note to custom scale")
        
        else:
            ROOT_NOTE = command.note % 12
            INIT_HAVE_ROOT = True
            command.act("Set root note to" + str(ROOT_NOTE))
        
        
    if INIT_HAVE_ROOT and INIT_HAVE_SCALE:
        INIT_COMPLETE = True
        FORWARD_NOTES = False
        setScale(ROOT_NOTE, SCALE_TO_USE)
        COLOUR = CURRENT_SCALE_COLOUR
        internal.extendedMode.revert(eventconsts.INCONTROL_PADS)
