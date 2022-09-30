# -*- coding: utf-8 -*-

"""Group of Shortcut functions to manipulate and create all type of content."""

# # from dataclasses import dataclass, field
# from resources.lib.items.contentmanager import ContentManagerMovie, ContentManagerShow
# from resources.lib.items.episode import EpisodeItem
# from resources.lib.items.movie import MovieItem


# def build_json_item(item):
#     """Shortcut to convert a database item into a json."""
#     formated_json = {}
#     keys = ["file", "title", "type", "state", "year"]
#     if len(item) == 8:
#         # extra keys to convert show from db
#         keys += ["showtitle", "season", "episode"]
#     for key, value in zip(keys, item):
#         formated_json[key] = value
#     return formated_json

# def build_contentitem(jsonitem):
#     """Shortcut to return a MovieItem or EpisodeItem json."""
#     command = {"tvshow": EpisodeItem, "movie": MovieItem}
#     return command[jsonitem["type"]](jsonitem).returasjson()


# def build_contentmanager(database, jsonitem):
#     """Shortcut to create a ContentManager object."""
#     command = {"tvshow": ContentManagerShow, "movie": ContentManagerMovie}
#     return command[jsonitem["type"]](database, jsonitem)


import logging
from os.path import basename, join

import xbmc
import xbmcaddon
import xbmcvfs

# from resources.lib.filesystem import isdir, mk_dir
# from resources.lib.gui.gui_utils import get_string, notification
from resources.lib.misc import re_search

# Get settings
ADDON_ID = "script.library.integration.tool"
ADDON = xbmcaddon.Addon(ADDON_ID)
ADDON_NAME = ADDON.getAddonInfo("name")
ADDON_PATH = ADDON.getAddonInfo("path")
ADDON_VERSION = ADDON.getAddonInfo("version")

AUTO_ADD_MOVIES = ADDON.getSetting("auto_add_movies") == "true"
AUTO_ADD_TVSHOWS = ADDON.getSetting("auto_add_tvshows") == "true"
AUTO_CREATE_NFO_MOVIES = ADDON.getSetting("auto_create_nfo_movies") == "true"
AUTO_CREATE_NFO_SHOWS = ADDON.getSetting("auto_create_nfo_shows") == "true"
# USE_SHOW_ARTWORK_SHOW = ADDON.getSetting("use_show_artwork_show") == "true"

RECURSION_LIMIT = int(ADDON.getSetting("recursion_limit"))

USING_CUSTOM_MANAGED_FOLDER = ADDON.getSetting("custom_managed_folder") == "true"
CUSTOM_MANAGED_FOLDER = ADDON.getSetting("managed_folder")
ADDON_SPECIAL_DIR = f"special://userdata/addon_data/{ADDON_ID}/"


LOG = logging.getLogger(basename(__file__))

LOG.debug("This is The main.py")

NETWORK_PATHS = [
    r"smb://",
    r"nfs://",
    r"ftp://",
]

MANAGED_FOLDER = xbmcvfs.translatePath(ADDON_SPECIAL_DIR)
DATABASE_PATH = xbmcvfs.translatePath(join(MANAGED_FOLDER, "managed.db"))

if USING_CUSTOM_MANAGED_FOLDER:
    MANAGED_FOLDER = xbmcvfs.validatePath(CUSTOM_MANAGED_FOLDER)

    if re_search(MANAGED_FOLDER, NETWORK_PATHS):
        DATABASE_PATH = xbmcvfs.translatePath(join(ADDON_SPECIAL_DIR, "managed.db"))
    else:
        DATABASE_PATH = xbmcvfs.translatePath(join(MANAGED_FOLDER, "managed.db"))
