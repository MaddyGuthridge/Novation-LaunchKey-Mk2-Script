"""
flags.py

This function allows for the parsing of FL flags.

Author: Praashie

This code is from the open-source project FLatmate, licenced under GNU GPL v3.
Website: https://github.com/praashie/flatmate
Current file version: FLatmate v0.3.2, released July 20th 2020
"""


import midi

FLAG_PREFIXES = ['PME', 'TLC', 'HW_Dirty', 'UF', 'GT']

class FlagParser:
    def __init__(self, prefix):
        self.__name__ = prefix
        self.flagtable = []
        for var in dir(midi):
            value = getattr(midi, var)
            if var.startswith(prefix + '_') and type(value) == int:
                self.flagtable.append(var)
                setattr(self, var[len(prefix)+1:], value)

    def __call__(self, x):
        return ' | '.join([flag for flag in self.flagtable if (x & getattr(midi, flag))])

def setup_tables(prefixes, namespace):
    for prefix in prefixes:
        namespace[prefix] = FlagParser(prefix)

setup_tables(FLAG_PREFIXES, globals())

GT.flagtable.remove("GT_All")
GT.flagtable.remove("GT_Cannot")