# -*- coding: utf-8 -*-

"""Defines the StagedMoviesMenu class."""

import logging
from os.path import basename

import xbmc
import xbmcgui

from resources.lib import ADDON_NAME
from resources.lib.content.movie.staged import StagedMovie
from resources.lib.database.database import DBCommon
from resources.lib.gui.colors import Colors
from resources.lib.gui.gui_utils import bold, colorize, get_string, notification
from resources.lib.gui.progressbar import ProgressBar
from resources.lib.gui.select import Select

# from resources.lib.items.contentmanager import ContentManagerMovie

LOG = logging.getLogger(basename(__file__))


class StagedMoviesMenu:
    """Provide windows for displaying staged movies, and tools for managing the items."""

    # TODO: don't commit sql changes for "... all" until end
    # TODO: decorator for "...all" commands

    def __init__(self, parent_menu):
        """__init__ StagedMoviesMenu."""
        # Only realy connect to database when open the content menu.
        self.database = DBCommon()
        self.progress_dialog = ProgressBar()
        self.parent_menu = parent_menu
        self.last_choice = 99999

        self.finished_string = get_string(32043)
        self.staged_movies = self.database.get_content_items(
                status="staged", content_type="movie"
        )

    def add_all_to_managed(self):
        """Add all items to managed (library)."""
        self.progress_dialog.create_progress_dialog(head=get_string(32042))
        title: str
        info: dict
        for index, movie_dict_info in enumerate(self.staged_movies.items()):
            title, info = movie_dict_info
            movie = StagedMovie(**info, database=self.database)
            movie.move_to_managed()
            self.progress_dialog.update_progress_dialog(
                index / len(self.staged_movies), title
            )
        self.progress_dialog.close_progress_dialog()
        notification(self.finished_string)

    def remove_all_from_staged(self):
        """Remove all items from staged."""
        self.progress_dialog.create_progress_dialog(head=get_string(32013))
        title: str
        info: dict
        for index, movie_dict_info in enumerate(self.staged_movies.items()):
            title, info = movie_dict_info
            movie = StagedMovie(**info, database=self.database)
            movie.delete_from_staged()
            self.progress_dialog.update_progress_dialog(
                index / len(self.staged_movies), title
            )
        self.progress_dialog.close_progress_dialog()
        notification(self.finished_string)

    # @staticmethod
    # def rename_dialog(item):
    #     """Prompt input for new name, and rename if non-empty string."""
    #     # TODO: move to utils or parent class so it's not duplicated
    #     input_ret = xbmcgui.Dialog().input("Title", defaultt=item.title())
    #     if input_ret:
    #         item.rename(input_ret)

    def movie_options(self, movie_dict_info):
        """Provide options for a single staged movie in a dialog window."""
        movie = StagedMovie(**movie_dict_info, database=self.database)
        select_menu = Select(
                heading=bold(
                        f"{get_string(32053)} - {colorize(movie.title)} {colorize(movie.formed_year, colorname=Colors.LIGHTSALMON)}"
                ),
                turn_bold=True,
        )
        # # TODO: RENAME STRING --> 32050
        select_menu.options(
                {
                    32048: movie.move_to_managed,
                    32017: movie.delete_from_staged,
                    32049: movie.delete_from_staged_and_block,
                },
                turn_bold=True,
        )
        selected_option = select_menu.show(use_details=True, pre_select=999999)
        if not selected_option or "back" in selected_option:
            self.show_all()
            return
        selected_index, _, selected_value = selected_option
        self.last_choice = selected_index

        selected_value()
        self.staged_movies.pop(movie_dict_info["title"])
        xbmc.sleep(400)
        if self.staged_movies:
            self.show_all()
        else:
            self.parent_menu.show()

    def show_all(self):
        """Display all staged movies, which are selectable and lead to options."""
        if not self.staged_movies:
            xbmcgui.Dialog().ok(ADDON_NAME, get_string(32037))
            return
        select_menu = Select(
                heading=bold(
                        f"{colorize(get_string(32004), colorname=Colors.DEEPSKYBLUE)}"
                ),
                turn_bold=True,
        )
        select_menu.options(
                options=self.staged_movies,
                turn_bold=True,
        )
        select_menu.extra_options(
                options={
                    32038: self.add_all_to_managed,
                    32009: self.remove_all_from_staged,
                }
        )
        selected_option = select_menu.show(use_details=True, pre_select=self.last_choice)
        if not selected_option or "back" in selected_option:
            self.parent_menu.show()
            return
        selected_index, selected_key, selected_value = selected_option
        self.last_choice = selected_index
        if selected_key in [32038, 32009]:
            selected_value()
            self.parent_menu.show()
        else:
            self.movie_options(movie_dict_info=selected_value)
