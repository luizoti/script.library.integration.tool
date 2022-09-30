# -*- coding: utf-8 -*-

"""This module gets called from the context menu item "Sync directory to library" (32001).

The purpose is to stage all movies/tvshows in the current directory, and update database.
"""

import xbmc

from resources.lib.database import Database
from resources.lib.gui.progressbar import ProgressBar
from resources.lib.gui.select import Select
from resources.lib.menus.synced import SyncedMenu
from resources.lib.misc import get_string, notification
from resources.lib.progressbar import ProgressBar
from resources.lib.utils import entrypoint

LOG = logging.getLogger(basename(__file__))
logger.logging_setup()

@entrypoint
def main():
    """Main entrypoint for context menu item."""
    select_menu = Select(heading=get_string(32164), turnbold=True, back_option=32157)
    select_menu.options(
        {
            32160: "all_items",
            32161: "movie",
            32162: "tvshow",
            32167: "filter",
        },
        turnbold=False,
    )
    selected_option = select_menu.show(useDetails=False)
    if selected_option:
        _, _, selected_value = selected_option
        if selected_value == "back":
            notification(get_string(32158), 4000)
            return
        SyncedMenu(
            database=Database(), progressdialog=ProgressBar()
        ).add_all_items_in_directory(
            selected_value,
            xbmc.getInfoLabel("Container.FolderName"),
            xbmc.getInfoLabel("Container.FolderPath"),
        )


if __name__ == "__main__":
    main()
