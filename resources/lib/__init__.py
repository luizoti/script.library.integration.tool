# -*- coding: utf-8 -*-

from resources.lib.gui.progressbar import BGProgressBar, ProgressBar

from resources.lib.items.contentmanager import ContentManagerMovie, ContentManagerShow
from resources.lib.items.episode import EpisodeItem
from resources.lib.items.movie import MovieItem


def build_json_item(item):
    """Shortcut to convert a database item into a json."""
    formated_json = {}
    keys = ["file", "title", "type", "state", "year"]
    if len(item) == 8:
        # extra keys to convert show from db
        keys += ["showtitle", "season", "episode"]
    for key, value in zip(keys, item):
        formated_json[key] = value
    return formated_json


def build_contentitem(jsonitem):
    """Shortcut to return a MovieItem or EpisodeItem json."""
    command = {"tvshow": EpisodeItem, "movie": MovieItem}
    return command[jsonitem["type"]](jsonitem).returasjson()


def build_contentmanager(database, jsonitem):
    """Shortcut to create a ContentManager object."""
    command = {"tvshow": ContentManagerShow, "movie": ContentManagerMovie}
    return command[jsonitem["type"]](database, jsonitem)
