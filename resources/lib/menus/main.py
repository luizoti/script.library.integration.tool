# -*- coding: utf-8 -*-

"""Defines the MainMenu class, which gets called from the main executable."""

import logging
import sys
from os.path import basename

import xbmc
from resources.lib import ADDON_ID, ADDON_NAME
from resources.lib.gui.colors import Colors
from resources.lib.gui.gui_utils import bold, colorize

# from resources.lib.gui.progressbar import ProgressBar
from resources.lib.gui.select import Select
from resources.lib.menus.movie.managed import ManagedMoviesMenu
from resources.lib.menus.movie.staged import StagedMoviesMenu
from resources.lib.menus.show.managed import ManagedTVMenu
from resources.lib.menus.show.staged import StagedTVMenu
from resources.lib.misc import videolibrary

# from resources.lib.menus.synced import SyncedMenu
# from resources.lib.menus.blocked import BlockedMenu

# TODO: automatically clean & update when adding/removing based in type and path
# TODO: rebuild library option
#   1. FLAG all itens in managed
#   2. move all all to staged
#   3. delete all managed itens
#   4. re-add all FLAGGED itens

LOG = logging.getLogger(basename(__file__))


class MainMenu:
    """Perform basic initialization of folder structure."""

    def __init__(self):
        """__init__ MainMenu."""
        # An impossible value seems to force
        # the parent to choose none, in list
        self.lastchoice = 99999
        LOG.debug("MainMenu Started")

    def library_options(self):
        """Display dedicated menu to Library functions."""
        select_menu = Select(
                heading=bold(f"{colorize('Library options')}"),
                turn_bold=True,
        )
        select_menu.options(
                {
                    653:   "scan",
                    14247: "clean",
                },
                turn_bold=False,
        )
        selected_option = select_menu.show(use_details=True, pre_select=self.last_choice)

        if not selected_option or "back" in selected_option:
            self.show()
            return
        selected_index, _, selected_value = selected_option
        self.lastchoice = selected_index
        videolibrary(selected_value)
        xbmc.sleep(1500)
        self.library_options()

    def show(self):
        """Display main menu which leads to other menus."""
        select_menu = Select(
            # TODO: .replace("[\B]", "") because it seems not possible to close a tag [B] when using a tag color
            # fix this in future
            heading=colorize(bold(ADDON_NAME), Colors.SKYBLUE).replace(r"[/B]", ""),
            back_option=False,
        )
        select_menu.options(
            {
                32002: ManagedMoviesMenu,
                32004: StagedMoviesMenu,
                32003: ManagedTVMenu,
                32005: StagedTVMenu,
                # 32006: SyncedMenu,
                # 32007: BlockedMenu,
            }
        )
        select_menu.extra_options(
            {
                32180: self.library_options,
                32179: xbmc.executebuiltin,
            }
        )
        selected_option: tuple = select_menu.show(use_details=True)

        if not selected_option or "back" in selected_option:
            return
        _, selected_key, selected_value = selected_option
        if selected_key == 32180:
            selected_value()
        elif selected_key == 32179:
            # # Open addon settings, the second argument turn a blocking task
            selected_value(f"Addon.OpenSettings({ADDON_ID})", True)
            self.show()
        else:
            selected_value(self).show()
        sys.exit()
