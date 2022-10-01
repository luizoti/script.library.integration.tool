# -*- coding: utf-8 -*-

"""Defines the ManagedMoviesMenu class."""

import logging
from os.path import basename

import xbmc
import xbmcgui

from resources.lib import ADDON_NAME
from resources.lib.content.movie.managed import ManagedMovie
from resources.lib.database.database import DBCommon
from resources.lib.gui.colors import Colors
from resources.lib.gui.gui_utils import bold, colorize, get_string, notification
from resources.lib.gui.progressbar import ProgressBar
from resources.lib.gui.select import Select

LOG = logging.getLogger(basename(__file__))


class ManagedMoviesMenu:
    """
    Contain window for displaying managed movies.

    Provive tools for manipulating the objects and managed file.
    """

    def __init__(self, parent_menu):
        """__init__ ManagedMoviesMenu."""
        self.database = DBCommon()
        self.progress_dialog = ProgressBar()
        self.parent_menu = parent_menu
        self.last_choice = 99999

        self.finished_string = get_string(32043)
        self.managed_movies = self.database.get_content_items(
            status="managed", content_type="movie"
        )

    # TODO: Remove the two strings and make them one
    # maybe -> Processing items
    # 32013
    # 32015
    # 32136
    # 32046
    def delete_all(self):
        """Delete all managed movies from library."""
        self.progress_dialog.create_progress_dialog(head=get_string(32013))
        title: str
        info: dict
        for index, movie_dict_info in enumerate(self.managed_movies.items()):
            title, info = movie_dict_info
            movie = ManagedMovie(**info, database=self.database)
            movie.remove_completely()
            self.progress_dialog.update_progress_dialog(
                index / len(self.managed_movies), title
            )
        self.progress_dialog.close_progress_dialog()
        notification(self.finished_string)

    def move_all_to_staged(self):
        """Move all managed movies to staged."""
        self.progress_dialog.create_progress_dialog(head=get_string(32015))
        title: str
        info: dict
        for index, movie_dict_info in enumerate(self.managed_movies.items()):
            title, info = movie_dict_info
            movie = ManagedMovie(**info, database=self.database)
            movie.move_to_staged()
            self.progress_dialog.update_progress_dialog(
                index / len(self.managed_movies), title
            )
        self.progress_dialog.close_progress_dialog()
        notification(self.finished_string)

    def delete_all_nfo_files(self):
        """Delete all metadata (.nfo only) for all movies."""
        self.progress_dialog.create_progress_dialog(head=get_string(32136))
        title: str
        info: dict
        for index, movie_dict_info in enumerate(self.managed_movies.items()):
            title, info = movie_dict_info
            movie = ManagedMovie(**info, database=self.database)
            movie.delete_nfo()
            self.progress_dialog.update_progress_dialog(
                index / len(self.managed_movies), title
            )
        self.progress_dialog.close_progress_dialog()
        notification(self.finished_string)

    def create_all_nfo_files(self):
        """Create all metadata (.nfo only) for all movies."""
        self.progress_dialog.create_progress_dialog(head=get_string(32046))
        title: str
        info: dict
        for index, movie_dict_info in enumerate(self.managed_movies.items()):
            title, info = movie_dict_info
            movie = ManagedMovie(**info, database=self.database)
            movie.build_movie_nfo_string()
            movie.create_nfo()
            self.progress_dialog.update_progress_dialog(
                index / len(self.managed_movies), title
            )
        self.progress_dialog.close_progress_dialog()
        notification(self.finished_string)

    def movie_options(self, movie_dict_info):
        """Provide options for a single managed movie in a dialog window."""
        movie = ManagedMovie(**movie_dict_info, database=self.database)
        select_menu = Select(
                heading=bold(
                        f"{get_string(32053)} - {colorize(movie.title)} {colorize(movie.formed_year, colorname=Colors.LIGHTSALMON)}"
                ),
                turn_bold=True,
        )
        select_menu.options(
                {
                    32017: movie.remove_completely,
                    32018: movie.move_to_staged,
                    32052: movie.create_nfo,
                    32051: movie.delete_nfo,
                },
                turn_bold=True,
        )
        selected_option = select_menu.show(use_details=True, pre_select=999999)
        if not selected_option or "back" in selected_option:
            self.show()
            return
        selected_index, selected_key, selected_value = selected_option
        self.last_choice = selected_index

        if selected_key in [32017, 32018]:
            selected_value()
            self.managed_movies.pop(movie_dict_info["title"])
            xbmc.sleep(400)
            if self.managed_movies:
                self.show()
            else:
                self.parent_menu.show()
        selected_value()

    def show(self):
        """
        Display all managed movies, which are selectable and lead to options.
        """
        if not self.managed_movies:
            xbmcgui.Dialog().ok(ADDON_NAME, get_string(32037))
            return
        select_menu = Select(
                heading=bold(
                        f"{colorize(get_string(32002), colorname=Colors.DEEPSKYBLUE)}"
                ),
                turn_bold=True,
        )
        select_menu.options(
                options=self.managed_movies,
                turn_bold=True,
        )
        select_menu.extra_options(
            {
                32009: self.delete_all,
                32010: self.move_all_to_staged,
                32040: self.create_all_nfo_files,
                32174: self.delete_all_nfo_files,
            }
        )
        selected_option = select_menu.show(use_details=True, pre_select=self.last_choice)
        if not selected_option or "back" in selected_option:
            self.parent_menu.show()
            return
        selected_index, selected_key, selected_value = selected_option
        self.last_choice = selected_index
        if selected_key in [32009, 32010]:
            selected_value()
            self.parent_menu.show()
        else:
            self.movie_options(movie_dict_info=selected_value)
