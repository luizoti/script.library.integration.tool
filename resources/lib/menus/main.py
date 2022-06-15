# -*- coding: utf-8 -*-

"""Defines the MainMenu class, which gets called from the main executable."""

import sys

import xbmc
from resources import ADDON_ID, ADDON_NAME
from resources.lib.database import Database
from resources.lib.dialog_select import Select
from resources.lib.menus.managed_movies import ManagedMoviesMenu
from resources.lib.menus.managed_tv import ManagedTVMenu
from resources.lib.menus.staged_movies import StagedMoviesMenu
from resources.lib.menus.staged_tv import StagedTVMenu
from resources.lib.misc import bold, color, videolibrary
from resources.lib.progressbar import ProgressBar

# from resources.lib.menus.synced import SyncedMenu
# from resources.lib.menus.blocked import BlockedMenu

# TODO: automatically clean & update when adding/removing based in type and path
# TODO: rebuild library option
#   1. FLAG all itens in managed
#   2. move all all to staged
#   3. delete all managed itens
#   4. re-add all FLAGGED itens


class MainMenu:
    """Perform basic initialization of folder structure."""

    def __init__(self):
        """__init__ MainMenu."""
        self.database = Database
        self.progressbar = ProgressBar
        # An impossible value seems to force
        # the parent to choose none, in list
        self.lastchoice = 99999

    def library_options(self):
        """Display dedicated menu to Library functions."""
        select_menu = Select(
            heading=bold(f"{ADDON_NAME} - {color('Library options')}"),
            turnbold=True,
        )
        select_menu.options(
            {
                653: "scan",
                14247: "clean",
            },
            turnbold=False,
        )
        selected_option = select_menu.show(useDetails=True, preselect=self.lastchoice)

        if selected_option:
            selected_index, _, selected_value = selected_option
            self.lastchoice = selected_index

            if selected_value == "back":
                self.show()
            else:
                videolibrary(selected_value)
                xbmc.sleep(1500)
                self.library_options()
            return

    def show(self):
        """Display main menu which leads to other menus."""
        select_menu = Select(heading=ADDON_NAME, turnbold=True, back_option=False)
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
        selected_option: tuple = select_menu.show(useDetails=True)
        if selected_option:
            _, selected_key, selected_value = selected_option
            if selected_key == 32179:
                # # Open addon settings, the second argument turn a blocking task
                selected_value(f"Addon.OpenSettings({ADDON_ID})", True)
                self.show()
            if selected_option == "back":
                self.show()
            else:
                selected_value(self.database, self.progressbar).show_all()
        sys.exit()
