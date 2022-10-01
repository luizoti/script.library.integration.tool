# -*- coding: utf-8 -*-

"""Defines the StagedEpisodeMenu class."""

import logging
from os.path import basename

import xbmc
import xbmcgui

from resources.lib import ADDON_NAME
from resources.lib.content.show.staged.staged_episode import StagedEpisode
from resources.lib.content.show.staged.staged_show import StagedShow
from resources.lib.database.show.db_show import DBShows
from resources.lib.gui.colors import Colors
from resources.lib.gui.gui_utils import bold, colorize, get_string, notification
from resources.lib.gui.progressbar import ProgressBar
from resources.lib.gui.select import Select

LOG = logging.getLogger(basename(__file__))


class StagedShowsMenu:
    """Provide windows for displaying staged tvshows and episodes."""

    def __init__(self, parent_menu):
        """__init__ StagedShowsMenu."""
        self.database = DBShows()
        self.progress_dialog = ProgressBar()
        self.parent_menu = parent_menu
        self.last_choice = 99999

        self.finished_string = get_string(32043)
        self.staged_shows = self.database.get_content_items(
                status="staged", content_type="tvshow"
        )
        LOG.debug(self.staged_shows)
        self.rollback = []
        self.all_shows_episodes = []

        for show in self.staged_shows.values():
            self.all_shows_episodes += show

    def show_actions(self, content_type):
        """
        This method performs only two actions
        Staged Episode().move_to_managed() and Staged Episode().delete_from_staged().
        Separate this method has two names add_all_to_managed and remove_all_from_staged.

        Args:
            content_type (str): The name of action add or remove.
        """
        actions = {"add": 32042, "delete": 32013}
        break_loop: bool
        episode_dict_info: dict
        self.progress_dialog.create_progress_dialog(head=bold(get_string(actions[content_type])))
        for index, episode_dict_info in enumerate(self.all_shows_episodes):
            episode = StagedEpisode(**episode_dict_info, database=self.database)
            if content_type == "add":
                episode.move_to_managed()
            elif content_type == "delete":
                episode.delete_from_staged()
            self.rollback.append(episode_dict_info)
            self.progress_dialog.update_progress_dialog(
                    percentage=(index / len(self.all_shows_episodes)), message=str(episode)
            )
            break_loop = self.progress_dialog.close_progress_dialog()
            if break_loop:
                # TODO: In this setup self.rollback will store all itens processed,
                # to revert all performed actions in this case ManagedEpisode
                LOG.debug(f"rollback {self.rollback}")
                break
            else:
                self.staged_shows[episode.showtitle].remove(episode_dict_info)
                if not self.staged_shows[episode.showtitle]:
                    self.staged_shows.pop(episode.showtitle)
        self.progress_dialog.close()
        notification(self.finished_string)

    def show_options(self, show_dict_info):
        """Provide options for a single staged show in a dialog window."""
        # Here we will access the first item of episode list, and use to create the StagedShow object
        show = StagedShow(**show_dict_info[0], database=self.database)
        select_menu = Select(
                heading=bold(
                        f"""{get_string(32053)} - {colorize(show.title)} {colorize(show.formed_year, colorname=Colors.LIGHTSALMON)}"""
                ),
                turn_bold=True,
        )
        select_menu.options(
                options={x["season"]: "" for x in show_dict_info},
                turn_bold=True,
        )
        select_menu.extra_options(
                {
                    32048: show.move_to_managed,
                    32017: show.delete_from_staged,
                    32049: show.delete_from_staged_and_block,
                },

        )
        selected_option = select_menu.show(use_details=True, pre_select=999999)
        if not selected_option or "back" in selected_option:
            self.show_all()
            return
        selected_index, _, selected_value = selected_option
        self.last_choice = selected_index

        selected_value()
        self.staged_shows.pop(show_dict_info["title"])
        xbmc.sleep(400)
        if self.staged_shows:
            self.show_all()
        else:
            self.parent_menu.show()

    def show_all(self):
        """
        Display all staged shows, which are selectable and lead to options.
        """
        if not self.staged_shows:
            xbmcgui.Dialog().ok(ADDON_NAME, get_string(32037))
            return
        select_menu = Select(
                heading=bold(
                        f"{colorize(get_string(32005), colorname=Colors.DEEPSKYBLUE)}"
                ),
                turn_bold=True,
        )
        select_menu.options(
                options=self.staged_shows,
                turn_bold=True,
        )
        select_menu.extra_options(
                options={
                    32038: self.show_actions,
                    32009: self.show_actions,
                }
        )
        selected_option = select_menu.show(use_details=True, pre_select=self.last_choice)
        if not selected_option or "back" in selected_option:
            self.parent_menu.show()
            return
        selected_index, selected_key, selected_value = selected_option
        self.last_choice = selected_index
        if selected_key == 32038:
            selected_value(content_type="add")
        elif selected_key == 32009:
            selected_value(content_type="delete")
        LOG.info(f"Staged selected show: {selected_key} on menu {selected_index}")
        self.show_options(show_dict_info=selected_value)
