# -*- coding: utf-8 -*-

"""Defines the MainMenu class, which gets called from the main executable."""

import sys

import xbmc

from resources import ADDON_ID
from resources import ADDON_NAME


from resources.lib.misc import color, getstring, videolibrary
from resources.lib.dialog_select import Select

from resources.lib.database import Database
from resources.lib.progressbar import ProgressBar

from resources.lib.menus.managed_movies import ManagedMoviesMenu
from resources.lib.menus.staged_movies import StagedMoviesMenu
from resources.lib.menus.managed_tv import ManagedTVMenu
from resources.lib.menus.staged_tv import StagedTVMenu
# from resources.lib.menus.synced import SyncedMenu
from resources.lib.menus.blocked import BlockedMenu

# TODO: automatically clean & update when adding/removing based in type and path
# TODO: rebuild library option
#   1. FLAG all itens in managed
#   2. move all all to staged
#   3. delete all managed itens
#   4. re-add all FLAGGED itens


class MainMenu():
    """Perform basic initialization of folder structure."""

    def __init__(self):
        """__init__ MainMenu."""
        self.database = Database()
        self.progressbar = ProgressBar()
        self.lastchoice = False

    def library_options(self):
        """Display dedicated menu to Library functions."""
        OPTIONS = {
            653: 'scan',
            14247: 'clean',
        }
        sel = Select(
            heading=f"{ADDON_NAME} - {color('Library options')}",
            turnbold=True
        )
        sel.items([
            color(xbmc.getLocalizedString(x).title(), "darkgrey")
                for x in OPTIONS
            ],
            turnbold=False
        )
        selection = sel.show(
            useDetails=True,
            preselect=self.lastchoice,
            back=True
        )
        try:
            self.lastchoice = selection["index1"]
        except TypeError:
            pass
        if selection:
            if selection['type'] == 'item':
                options_arg = OPTIONS[list(OPTIONS)[selection["index1"]]]
                videolibrary(options_arg)
                xbmc.sleep(1500)
            self.library_options()

    def show(self):
        """Display main menu which leads to other menus."""
        self.lastchoice = False
        OPTIONS = {
            32002: ManagedMoviesMenu(self.database, self.progressbar).show_all,
            32004: StagedMoviesMenu(self.database, self.progressbar).show_all,
            32003: ManagedTVMenu(self.database, self.progressbar).show_all,
            32005: StagedTVMenu(self.database, self.progressbar).show_all,
            # 32006: SyncedMenu(self.database, self.progressbar).view,
            32007: BlockedMenu(self.database, self.progressbar).show_all,
        }
        EXTRA_OPTIONS = {
            32180: self.library_options,
            32179: xbmc.executebuiltin,
        }
        sel = Select(
            heading=ADDON_NAME,
            turnbold=True
        )
        sel.items([getstring(x) for x in OPTIONS])
        sel.extraopts([getstring(x) for x in EXTRA_OPTIONS])
        selection = sel.show(
            useDetails=True,
            preselect=self.lastchoice,
            back=False
        )
        if selection:
            if selection['type'] == 'item':
                command = OPTIONS[list(OPTIONS)[selection['index1']]]
                command()
            elif selection['type'] == 'opt':
                selected = list(EXTRA_OPTIONS)[selection['index1']]
                command = EXTRA_OPTIONS[list(EXTRA_OPTIONS)[selection['index1']]]
                if int(selected) == 32179:
                    # Open addon settings, the second argument turn a blocking task
                    command(f"Addon.OpenSettings({ADDON_ID})", True)
                else:
                    # Open library options
                    command()
                # When closed, open the MainMenu again
            self.show()
        sys.exit()
