# -*- coding: utf-8 -*-
# pylint: disable=E1101

"""
Add selected item to library.

This module gets called from the context menu item "" (32000).
The purpose is to stage the currently selected movie/tvshow, and update synced directories.
"""

import sys

import xbmc
import xbmcgui

from resources.lib.database import Database
from resources.lib.menus.synced import SyncedMenu
from resources.lib.misc import get_string, notification, re_search, title_with_color
from resources.lib.progressbar import ProgressBar
from resources.lib.utils import entrypoint

STR_IS_A_MOVIE = get_string(32155)
STR_IS_A_SHOW = get_string(32156)
STR_CANCEL_RED = get_string(32157)
STR_NOT_SELECTED = get_string(32163)
STR_CHOOSE_CONTENT_TYPE = get_string(32159)

# possible values ​​that content can have
LIST_TYPE_SERIES = [
    "series",
    "directory",
    "show",
    "browse",
    "root",
    "mode=102",
    "mode=ondemand",
    "mode=series",
]
LIST_TYPE_MOVIES = ["movie", "PlayVideo", "play&_play", "mode=103", "type=movies"]


@entrypoint
def main():
    """Main entrypoint for context menu item."""
    title = sys.listitem.getLabel()
    year = xbmc.getInfoLabel("ListItem.Year")
    year = int(year) if year else False
    file = sys.listitem.getPath()
    str_formed_type_of_content = (
        f"{title_with_color(label=title, year=year)} - {STR_CHOOSE_CONTENT_TYPE}"
    )
    lines = [STR_IS_A_MOVIE, STR_IS_A_SHOW, STR_CANCEL_RED]
    selection = xbmcgui.Dialog().select(str_formed_type_of_content, lines)
    selection = lines[selection]
    if selection:
        syncedmenu = SyncedMenu(database=Database(), progressdialog=ProgressBar())
        # Call corresponding method
        if selection == STR_IS_A_MOVIE:
            if re_search(file, LIST_TYPE_MOVIES):
                syncedmenu.add_single_movie(title=title, year=year, file=file)
        elif selection == STR_IS_A_SHOW:
            if re_search(file, LIST_TYPE_SERIES):
                syncedmenu.add_single_tvshow(title=title, year=year, file=file)
        elif selection == STR_CANCEL_RED:
            xbmc.sleep(300)
            notification(get_string(32158))
        else:
            xbmc.sleep(300)
            notification(
                f"{title_with_color(label=title, year=year)} {STR_NOT_SELECTED}"
            )


if __name__ == "__main__":
    main()
