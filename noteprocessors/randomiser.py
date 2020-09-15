"""
noteprocessors > _template.py

This script is a template note processor.

Author: Miguel Guthridge
"""

import internal.consts
import eventconsts
import internal
import processorhelpers
import lightingconsts
import transport

import math

import _random
# Create random number generator
rng = _random.Random()

# The name of your mode
NAME = "Randomiser"

# The colour used to represent your mode
DEFAULT_COLOUR = lightingconsts.colours["PINK"]

# The colour used to represent your mode while active... 
# you can change this while your script is running
COLOUR = lightingconsts.colours["PINK"]

# Signifies whether the processor has completed its initialisation.
# Change this to true somewhere in processInit() if your script requires events to configure it
# otherwise change it here
INIT_COMPLETE = False

# Whether your mode should be unlisted in the note mode menu
SILENT = False

# Whether to forward all notes to the extended mode script to be processed as well. 
# You can modify this during execution to make it only forward notes sometimes.
FORWARD_NOTES = True

# Chord sets
chord_sets = [[] for _ in range(8)]
current_set = 0

# Autochange set
bar_progresses_set = False
last_transport = False

def process(command):
    """Called with an event to be processed by your note processor. Events aren't filtered so you'll want to make sure your processor checks that events are notes.

    Args:
        command (ParsedEvent): An event for your function to modify/act on.
    """
    global current_set
    command.addProcessor("Note Randomiser Processor")
    
    # If the note processor isn't initialised, call the initialise function instead
    if not INIT_COMPLETE:
        processInit(command)
        return
    
    # If command is a note
    if command.type is eventconsts.TYPE_NOTE:
        if command.value:
            new_note = chord_sets[current_set][math.floor(abs(rng.random() * len(chord_sets[current_set]) - 0.01))]
            internal.notesDown.noteOn(processorhelpers.ExtensibleNote(command, [processorhelpers.RawEvent(command.status, new_note, command.value)]))
            command.handle("Randomise note")
        else:
            internal.notesDown.noteOff(command)
            command.handle("Randomise note off", True)
    
    elif command.id == eventconsts.PEDAL:
        if command.is_lift:
            command.handle("Pedal lift", True)
        else:
            toNextSet()
            if not internal.getPortExtended():
                # Forward note
                internal.sendCompleteInternalMidiMessage(command.getDataMIDI())
            command.handle("Next chord set")
    
    elif command.type is eventconsts.TYPE_PAD:
        if command.coord_Y == 1 and command.coord_X < 8:
            if len(chord_sets[command.coord_X]):
                current_set = command.coord_X
                command.handle("Set chord set number")
            else:
                command.handle("Chord set doesn't exist")
        elif command.coord_Y == 0 and command.coord_X < 8:
            command.handle("Drum pads catch-all", True)
    

def processInit(command):
    """Called if the INIT_COMPLETE flag is set to false

    Args:
        command (ParsedEvent): event to process
    """
    global current_set, chord_sets, INIT_COMPLETE, FORWARD_NOTES, bar_progresses_set
    # If command is a note
    if command.type is eventconsts.TYPE_NOTE and not command.value:
        chord_sets[current_set].append(command.note)
        command.ignore("Add note to list " + str(current_set))
    
    elif command.id == eventconsts.PEDAL:
        if command.is_lift:
            command.handle("Pedal lift", True)
        else:
            current_set += 1
            if current_set >= 8:
                current_set = 0
            if not internal.getPortExtended():
                # Forward note to other processor
                internal.sendCompleteInternalMidiMessage(command.getDataMIDI())
            command.handle("Next chord set")
    
    elif command.type is eventconsts.TYPE_PAD:
        if command.is_lift:
            if command.coord_Y == 1 and command.coord_X < 8:
                current_set = command.coord_X
                command.handle("Set chord set number")
            elif command.coord_X == 7 and command.coord_Y == 0:
                non_empty  = -1
                for i in range(8):
                    if len(chord_sets[i]):
                        non_empty = i
                        break
                if non_empty != -1:
                    current_set = non_empty
                    INIT_COMPLETE = True
                    FORWARD_NOTES = False
                    command.handle("Finish setup")
                else:
                    command.handle("Couldn't finish setup - no notes added")
            elif command.coord_X == 6 and command.coord_Y == 0:
                bar_progresses_set = not bar_progresses_set
                command.handle("Toggle automatic set progression")

def redraw(lights):
    """Called when a redraw is taking place. Use this to draw menus to allow your users to choose options. Most of the time, you should leave this empty.

    Args:
        lights (LightMap): The lights to draw to
    """
    if internal.extendedMode.query(eventconsts.INCONTROL_PADS):
        # If the note processor isn't initialised, call the initialise function instead
        if not INIT_COMPLETE:
            redrawInit(lights)
            return
        
        # Set controls
        for x in range(8):
            if internal.window.getAnimationTick() > x:
                if x == current_set:
                    if len(chord_sets[x]):
                        colour = lightingconsts.colours["PINK"]
                    else:
                        colour = lightingconsts.colours["OFF"]
                else:
                    if len(chord_sets[x]):
                        colour = lightingconsts.colours["DARK GREY"]
                    else:
                        colour = lightingconsts.colours["OFF"]
                lights.setPadColour(x, 1, colour)
        lights.solidifyAll()

def redrawInit(lights):
    # Set controls
    for x in range(8):
        if internal.window.getAnimationTick() > x:
            if x == current_set:
                if len(chord_sets[x]):
                    colour = lightingconsts.colours["PURPLE"]
                else:
                    colour = lightingconsts.colours["RED"]
            else:
                if len(chord_sets[x]):
                    colour = lightingconsts.colours["PINK"]
                else:
                    colour = lightingconsts.colours["DARK GREY"]
            lights.setPadColour(x, 1, colour)
    
    # Finish button
    lights.setPadColour(7, 0, lightingconsts.colours["GREEN"])
    
    colour = bar_progresses_set * lightingconsts.colours["LIGHT BLUE"] + (not bar_progresses_set) * lightingconsts.colours["ORANGE"]
    # Bar progression button
    lights.setPadColour(6, 0, colour)
    
    lights.solidifyAll()


def activeStart():
    """Called when your note mode is made active
    """
    pass

def activeEnd():
    """Called wen your note mode is no-longer active
    """
    global COLOUR, INIT_COMPLETE, FORWARD_NOTES, chord_sets, current_set
    # Reset current colour to default
    COLOUR = DEFAULT_COLOUR
    INIT_COMPLETE = False
    FORWARD_NOTES = True
    chord_sets = [[] for _ in range(8)]
    current_set = 0

def beatChange(beat):
    global last_transport
    if bar_progresses_set:
        transport_on = transport.isPlaying()
        if beat == 1 and last_transport == transport_on:
            toNextSet()
        last_transport = transport_on

def toNextSet():
    global current_set
    # Increment bar number
    next_set = current_set
    check_set = current_set + 1
    loop_count = 0
    while(True):
        if check_set >= 8:
            check_set = 0
        if len(chord_sets[check_set]):
            next_set = check_set
            break
        check_set += 1
        
        if loop_count >= 1000:
            raise("Loop threshold exceeded")
        loop_count += 1
    current_set = next_set
