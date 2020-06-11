# Novation-LaunchKey49-Mk2-Script

A WIP Python script for linking the Novation LaunchKey49 Mk2 controller to FL Studio.

Author: [Miguel Guthridge](https://www.youtube.com/channel/UCPB_zkvsJKuIkCgEzoXtN3g)

Project Page: [GitHub](https://github.com/MiguelGuthridge/Novation-LaunchKey49-Mk2-Script)

## Setup

In order to set up the controller script, please follow these instructions:

1. Copy the script's folder to your `/Image-Line/FL Studio/Settings/Hardware/` directory.

2. Launch FL Studio and navigate to MIDI Settings. Set the following options:

     - Device: `Launchkey MK2 49`; Controller: `LaunchKey49 Mk2 (user)`

     - Device: `MIDIIN2 (Launchkey MK2 49)`; Controller: `LaunchKey49 Mk2 (Extended) (user)`

3. Open the script `config.py` and edit the port constants to match those shown in FL Studio. Save and close the file.

4. Restart FL Studio. A light pattern should appear, indicating a successful connection.

## Basic Controls

The controller currently only supports basic transport controls.

 - Play                 Starts or Pauses playback.

 - Stop                 Stops playback. (Double press to stop all sounds).

 - Loop                 Toggle loop mode (Pattern/Song).

 - Record               Toggle recording mode.

 - Fast-forward/Rewind  Skip forward or backwards. (Double press for faster navigation speed).

 - Previous/Next Track  Select the previous/next UI element. (Can be used to navigate through Flex presets, the browser, etc).

## Passive Controls

The controller also performs various actions without the need for user interaction.

 - The Channel 9 LED Indicator flashes to the beat during playback.

## Feature Roadmap

I have big plans for this script, and now that I have a solid codebase, bringing them to life shouldn't take long. For the full list of plans, see [the script's Projects page](https://github.com/MiguelGuthridge/Novation-LaunchKey49-Mk2-Script/projects). Here are the coolest ones:

 - Use the pads to edit the bit grid in the channel rack.

 - Use the pad lights to show an updating parameter's value as it is being adjusted.

 - Use the pad lights to show the peak metre for the selected track while in the mixer.

 - Use the pads as tool selectors when in the playlist or the piano roll.

 - Use the pads for navigation in the browser.

## Bug Reports

If you encounter any issues with this script, please don't hesitate to create an issue on [the project's GitHub page](https://github.com/MiguelGuthridge/Novation-LaunchKey49-Mk2-Script). Be sure to include:

 - A copy of the script's console output.

 - A list of instructions for how to reproduce the issue, along with a clear description of what should have happened and what actually happened.
