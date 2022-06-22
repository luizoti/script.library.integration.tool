# -*- coding: utf-8 -*-

"""Defines the ManagedMoviesMenu class."""

import logging
from os.path import basename, join
from resources.lib.database.database import DBCommon

import xbmcgui
import xbmcvfs
from resources.lib import ADDON_NAME, MANAGED_FOLDER
from resources.lib.filesystem import listdir
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

    # TODO: context menu for managed items in library
    # TODO: synced watched status with plugin item
    def __init__(self, parent_menu):
        """__init__ ManagedMoviesMenu."""
        self.database = DBCommon()
        self.progressdialog = ProgressBar()
        self.parent_menu = parent_menu
        self.lastchoice = 99999
        self.movies = self.database.get_content_items(status="managed", _type="movie")

    def move_all_to_staged(self, items):
        """Remove all managed movies from library, and add them to staged."""
        STR_MOVING_ALL_MOVIES_BACK_TO_STAGED = get_string(32015)
        self.progressdialog.create_progressdialog(
            msg=STR_MOVING_ALL_MOVIES_BACK_TO_STAGED
        )
        for index, item in enumerate(items):
            self.progressdialog.update_progressdialog(index / len(items), item.title())
            item.remove_from_library()
            item.set_as_staged()
        self.progressdialog.close_progressdialog()
        notification(STR_MOVING_ALL_MOVIES_BACK_TO_STAGED)

    def remove_all(self, items):
        """Remove all managed movies from library."""
        STR_REMOVING_ALL_MOVIES = get_string(32013)
        STR_ALL_MOVIES_REMOVED = get_string(32014)
        self.progressdialog.create_progressdialog(msg=STR_REMOVING_ALL_MOVIES)
        for index, item in enumerate(items):
            self.progressdialog.update_progressdialog(index / len(items), item.title())
            item.remove_from_library()
            item.delete()
        self.progressdialog.close_progressdialog()
        notification(STR_ALL_MOVIES_REMOVED)

    @staticmethod
    def clean_up_all_managed_metadata(_=None):
        """Delete all metada (.nfo only) for all movies."""
        STR_MOVIE_METADATA_CLEANED = get_string(32136)
        managed_movies_dir = join(MANAGED_FOLDER, "movies")
        for full_path_movie_dir in listdir(managed_movies_dir, True):
            try:
                for filepath in listdir(full_path_movie_dir, True):
                    if ".nfo" in filepath:
                        xbmcvfs.delete(filepath)
            except Exception as error:
                raise error
        notification(STR_MOVIE_METADATA_CLEANED)

    def generate_all_managed_metadata(self, items):
        """Generate metadata items for all managed movies."""
        STR_GENERATING_ALL_MOVIE_METADATA = get_string(32046)
        STR_ALL_MOVIE_METADTA_CREATED = get_string(32047)
        self.progressdialog.create_progressdialog(msg=STR_GENERATING_ALL_MOVIE_METADATA)
        for index, item in enumerate(items):
            self.progressdialog.update_progressdialog(index / len(items), item.title())
            item.create_metadata_item()
        self.progressdialog.close_progressdialog()
        notification(STR_ALL_MOVIE_METADTA_CREATED)

    def options(self, item):
        """Provide options for a single managed movie in a dialog window."""
        # TODO: add rename option
        # TODO: add reload metadata option
        STR_REMOVE = get_string(32017)
        STR_MOVE_BACK_TO_STAGED = get_string(32018)
        STR_GENERATE_METADATA_ITEM = get_string(32052)
        STR_BACK = get_string(32011)
        STR_MANAGED_MOVIE_OPTIONS = get_string(32053)
        lines = [
            STR_REMOVE,
            STR_MOVE_BACK_TO_STAGED,
            STR_GENERATE_METADATA_ITEM,
            STR_BACK,
        ]
        ret = xbmcgui.Dialog().select(
            f"{ADDON_NAME} - {STR_MANAGED_MOVIE_OPTIONS} - {bold(colorize(item.title(), colorname=Colors.SKYBLUE))}",
            lines,
        )
        if ret >= 0:
            if lines[ret] == STR_REMOVE:
                item.remove_from_library()
                item.delete()
            elif lines[ret] == STR_MOVE_BACK_TO_STAGED:
                item.remove_from_library()
                item.set_as_staged()
            elif lines[ret] == STR_GENERATE_METADATA_ITEM:
                item.create_metadata_item()
                self.options(item)
            elif lines[ret] == STR_BACK:
                return self.show_all()
        return self.show_all()

    def show_all(self):
        """
        Display all managed movies, which are selectable and lead to options.

        Also provides additional options at bottom of menu.
        """
        return
        managed_movies = list(
            self.database.get_content_items(status="managed", _type="movie")
        )
        sel = Select(
            heading=f"{ADDON_NAME} - {get_string(32002)}",
        )
        sel.options([str(x) for x in managed_movies])
        sel.extra_options(
            {
                32009: self.remove_all,
                32010: self.move_all_to_staged,
                32040: self.generate_all_managed_metadata,
                32174: self.clean_up_all_managed_metadata,
            }
        )
        if not managed_movies:
            xbmcgui.Dialog().ok(ADDON_NAME, get_string(32008))
            return
        selected = sel.show(useDetails=False, preselect=False)
        if selected:
            if selected["type"] == "item":
                self.options(managed_movies[selected["index1"]])
            elif selected["type"] == "opt":
                command = OPTIONS[list(OPTIONS.keys())[selected["index1"]]]
                command(managed_movies)
        return

        # if selected_option:
        #     selected_index, _, selected_value = selected_option

        #     if selected_value == "back":
        #         self.show()
        #     else:
        #         videolibrary(selected_value)
        #         xbmc.sleep(1500)
        #         self.library_options()
        #     return
