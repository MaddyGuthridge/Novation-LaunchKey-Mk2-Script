"""
Provides wrapper functions around the plugins module, to allow it to be more tightly-integrated
with the script without repeating code

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import plugins

import internal
import processorhelpers

def _getPluginIndexTuple(plugin_index):
    """Converts an index to a tuple-form index if it isn't already
    
    If plugin_index is -1, it will be replaced with the selected plugin's index
    """
    
    if plugin_index == -1:
        plugin_index = internal.window.getPluginIndex()
    
    if type(plugin_index) is tuple:
        track_index = plugin_index[0]
        plugin_index = plugin_index[1]
    else:
        track_index = -1
    
    return (track_index, plugin_index)

def getParamByName(name, plugin_index=-1, expected_param_index=-1):
    """Returns the index of a parameter in a plugin given the name of the parameter.

    Args:
        name (str): Name of the parameter to find.
        
        plugin_index (optional)
         *  (int): Plugin index to search. Use -1 for currently-selected
                plugin's index.
         *  (tuple: 2 ints): Respectively, mixer track and plugin index to search.
        
        expected_param_index (optional, int): index where the parameter is expected to be.
            it is searched first to increase efficiency
        

    Returns:
        int: Index of parameter. -1 if not found.
    """

    plugin_index = _getPluginIndexTuple(plugin_index)
    
    if plugins.getParamName(expected_param_index, plugin_index[1], plugin_index[0]) == name:
        return expected_param_index

    for i in range(plugins.getParamCount(plugin_index[1], plugin_index[0])):
        if plugins.getParamName(i, plugin_index[1], plugin_index[0]) == name:
            return i
    
    return -1

def setParamByName(name, value,  plugin_index=-1, expected_param_index=-1):
    """Sets a parameter in a plugin given the name of the parameter.

    Args:
        name (str): Name of the parameter to find.
        
        value:
         *  (float):    Value to set the parameter to.
         *  (int):      MIDI value to set the parameter to (will be converted to a float between
                0 and 1).
        
        plugin_index (optional)
         *  (int):              Plugin index to search. Use -1 for currently-selected
                                    plugin's index.
         *  (tuple: 2 ints):    Respectively, mixer track and plugin index to search.
        
        expected_param_index (optional, int): index where the parameter is expected to be.
            it is searched first to increase efficiency
    
    Returns:
        int: parameter index changed
    """
    
    plugin_index = _getPluginIndexTuple(plugin_index)
    
    param_index = getParamByName(name, plugin_index, expected_param_index)
    
    if type(value) is int:
        value = processorhelpers.toFloat(value)
    
    plugins.setParamValue(value, param_index, plugin_index[1], plugin_index[0])
    
    return param_index

def setParamByIndex(param_index, value,  plugin_index=-1):
    """Sets a parameter in a plugin given the name of the parameter.

    Args:
        param_index (int): index where the parameter is.
            
        name (str): Name of the parameter to find.
        
        value:
         *  (float):    Value to set the parameter to.
         *  (int):      MIDI value to set the parameter to (will be converted to a float between
                0 and 1).
        
        plugin_index (optional)
         *  (int):              Plugin index to search. Use -1 for currently-selected
                                    plugin's index.
         *  (tuple: 2 ints):    Respectively, mixer track and plugin index to search.        
    """
    
    if type(value) is int:
        value = processorhelpers.toFloat(value)
    
    plugin_index = _getPluginIndexTuple(plugin_index)
    
    plugins.setParamValue(value, param_index, plugin_index[1], plugin_index[0])
    