# This strings will be used to ignore itens in show diretectories

import json
import re
from enum import Enum
from os.path import expanduser, join

import xbmc
import xbmcgui
from resources.lib.gui.colors import Colors

SKIP_STRINGS = [
    "resumo",
    "suggested",
    "extras",
    # 'trailer',
    r"\#(?:\d{1,5}\.\d{1,5}|SP)",
]


def re_search(string, tosearch=None):
    """Function check if string exist with re."""
    tosearch = tosearch if isinstance(tosearch, list) else [tosearch]
    return bool(any(re.search(rgx, string, re.I) for rgx in tosearch))


def skip_filter(contents_json, _key, toskip):
    """Function to iterate jsons in a list and filter by key with re."""
    try:
        for item in contents_json:
            if not bool(any(re.search(rgx, item[_key], re.I) for rgx in toskip)):
                yield item
    except TypeError:
        yield None


def is_season(string):
    """Function to check if item is a season."""
    return bool(re_search(string, ["season", "temporada", r"S\d{1,4}"]))

# in future path arg will select the clean method
def videolibrary(method, database="video"):
    """A dedicated method to performe jsonrpc VideoLibrary.Scan or VideoLibrary."""
    command = {
        "scan": f"CleanLibrary({database})",
        "clean": f"UpdateLibrary({database})",
    }
    xbmc.executebuiltin(command[method])
