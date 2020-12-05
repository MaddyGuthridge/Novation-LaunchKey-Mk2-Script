"""
update_check.py

This module basically checks for script updates and returns true if they are available.

Author: Miguel Guthridge [hdsq@outlook.com.au]
"""

import json
import urllib.request

from . import consts
import internal



def check():
    """Checks for an update to the script using the GitHub API

    Returns:
        bool: need_update_flag
            Indicates whether an update to the script is available
    """

    need_update_flag = False
    try:
        with urllib.request.urlopen(consts.UPDATE_JSON_URL) as url:
            data = json.loads(url.read().decode())
    except:
        return False
        
    latest_ver = data[0]["name"].split(".")

    latest_maj = int(latest_ver[0][1:])
    latest_min = int(latest_ver[1])
    latest_rev = int(latest_ver[2].split("-")[0])

    if latest_maj > consts.SCRIPT_VERSION_MAJOR:
        need_update_flag = True
    elif latest_min > consts.SCRIPT_VERSION_MINOR:
        need_update_flag = True
    elif latest_rev > consts.SCRIPT_VERSION_REVISION:
        need_update_flag = True
        
    return need_update_flag


