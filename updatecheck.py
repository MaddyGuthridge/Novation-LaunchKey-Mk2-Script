"""
update_check.py

This module basically checks for script updates and returns true if they are available.

Author: Miguel Guthridge
"""

import json
import urllib.request

import internalconstants
import internal



def check():
    """Checks for an update to the script using the GitHub API

    Returns:
        bool: need_update_flag
            Indicates whether an update to the script is available
    """

    need_update_flag = False
    try:
        with urllib.request.urlopen(internalconstants.UPDATE_JSON_URL) as url:
            data = json.loads(url.read().decode())
    except:
        return False
        
    latest_ver = data[0]["name"].split(".")

    latest_maj = int(latest_ver[0][1:])
    latest_min = int(latest_ver[1])
    latest_rev = int(latest_ver[2].split("-")[0])

    if latest_maj > internalconstants.SCRIPT_VERSION_MAJOR:
        need_update_flag = True
    elif latest_min > internalconstants.SCRIPT_VERSION_MINOR:
        need_update_flag = True
    elif latest_rev > internalconstants.SCRIPT_VERSION_REVISION:
        need_update_flag = True
    
    internal.SCRIPT_UPDATE_AVAILABLE = need_update_flag
    return need_update_flag


