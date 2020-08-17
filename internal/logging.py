"""
internal > logging.py

This module contains functions for logging information, ans well as some helpers

Author: Miguel Guthridge
"""


from . import consts


def getLineBreak():
    """
    Returns a series of - characters to simulate a ruled line break. Useful when printing stuff
    """
    return "————————————————————————————————————————————————————"


def getTab(string, multiplier = 1, length = consts.LOG_TAB_LENGTH):
    """Returns your string plus spaces to make the string length equal to a multiple of the tab length defined in config.py

    Args:
        string (str): the string to append to
        multiplier (int, optional): the number of tabs to do (useful for alligning statements when things get long). Defaults to 1.
        length (int, optional): how far to tab across. Defaults to config.TAB_LENGTH.

    Returns:
        str: the original string with spaces appended to it to equal a tab
    """
    string += " "
    toAdd = (length * multiplier) - len(string) % (length * multiplier)

    for x in range(toAdd):
        string += " "
    return string


def debugLog(message, level = 0):
    """Print a message for debugging, but only if the debug mode includes the debug type specified

    Args:
        message (str): what to log
        level (int, optional): the message type. Should be in the form of consts.DEBUG_SOME_MODE. Defaults to 0.
    """
    if level in config.CONSOLE_DEBUG_MODE or level == consts.DEBUG.ERROR:
        print(message)


def printCommand(command):
    """Prints ParsedEvent information

    Args:
        command (ParsedEvent): Event to print data of
    """
    command.printInfo()
    return


def printCommandOutput(command):
    """Print actions taken on a ParsedEvent

    Args:
        command (ParsedEvent): Event to print actions of
    """
    command.printOutput()
    debugLog(getLineBreak(), consts.DEBUG.EVENT_DATA)
    debugLog("", consts.DEBUG.EVENT_DATA)

import config
