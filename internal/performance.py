"""
internal > performance.py

This module contains functions and objects important for checking script performance

Author: Miguel Guthridge
"""

import time

import internalconstants
import config

from .logging import getLineBreak

class PerformanceMontor:
    """
    PerformanceMonitor
    
    This object tracks performance times for certain actions to complete.
    """
    def __init__(self, monitor_name, debug_level):

        self.name = monitor_name
        self.debug_level = debug_level

        self.total_time = 0
        self.startTime = -1
        self.endTime = -1
        self.num_events = 0
    
    def start(self):
        self.startTime = time.perf_counter()
    
    def stop(self):
        self.endTime = time.perf_counter()
        process_time = self.endTime - self.startTime
        self.total_time += process_time
        self.num_events += 1
        if self.debug_level in config.CONSOLE_DEBUG_MODE:
            getLineBreak()
            print(self.name)
            print("Processed in:", round(process_time, 4), "seconds")
            print("Average processing time:", round(self.total() / self.num_events, 4), "seconds")
            getLineBreak()
        return process_time
    
    def total(self):
        return self.total_time

# Create instances of performance counters
eventClock = PerformanceMontor("Event Processor", internalconstants.DEBUG_PROCESSOR_PERFORMANCE)
idleClock = PerformanceMontor("Idle Processor", internalconstants.DEBUG_IDLE_PERFORMANCE)
