"""
internal > performance.py

This module contains functions and objects important for checking script performance

Author: Miguel Guthridge
"""

import time

from . import consts
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
        """Start monitoring performance
        """
        self.startTime = time.perf_counter()
    
    def stop(self):
        """Stop monitoring performance

        Returns:
            float: Processing time
        """
        self.endTime = time.perf_counter()
        process_time = self.endTime - self.startTime
        self.total_time += process_time
        self.num_events += 1
        if self.debug_level in config.CONSOLE_DEBUG_MODE:
            print(getLineBreak())
            print(self.name)
            print("Processed in:", round(process_time, 4), "seconds")
            print("Average processing time:", round(self.total() / self.num_events, 4), "seconds")
            print(getLineBreak())
        return process_time
    
    def total(self):
        """Get total processing time

        Returns:
            float: total processing time
        """
        return self.total_time

# Create instances of performance counters
eventClock = PerformanceMontor("Event Processor", consts.DEBUG.PROCESSOR_PERFORMANCE)
idleClock = PerformanceMontor("Idle Processor", consts.DEBUG.IDLE_PERFORMANCE)
