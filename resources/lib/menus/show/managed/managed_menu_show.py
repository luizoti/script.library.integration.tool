# pylint: disable=line-too-long
# -*- coding: utf-8 -*-

"""Defines the ManagedShowMenu class."""
import xbmcgui

from resources.lib import ADDON_NAME
from resources.lib.database.show.db_show import DBShows
from resources.lib.gui.gui_utils import bold, colorize, get_string, notification
from resources.lib.gui.progressbar import ProgressBar
from resources.lib.gui.select import Select


class ManagedShowsMenu:
    """
    Provide windows for displaying managed shows and episodes.

    Also tools for manipulating the objects and managed file.
    """

    def __init__(self, parent_menu):
        """__init__ ManagedShowMenu."""
        self.database = DBShows()
        self.progress_dialog: ProgressBar = ProgressBar()

    def move_all_episodes_to_staged(self, items):
        """Move all episodes to staged."""
        showtitle = bold(items[0].showtitle)
        STR_MOVING_ALL_x_EPISODES_TO_STAGED = get_string(32034)
        STR_ALL_x_EPISODES_MOVED_TO_STAGED = get_string(32035) % colorize(
                showtitle, "skyblue"
        )
        self.progress_dialog.create_progress_dialog(
                head=STR_MOVING_ALL_x_EPISODES_TO_STAGED % colorize(showtitle)
        )
        for index, item in enumerate(items):
            self.progress_dialog.update_progress_dialog(
                    index / len(items),
                    message=f"{colorize(bold(item.showtitle()))}\n{item.episode_title_with_id()}",
            )
            item.remove_from_library()
            item.set_as_staged()
        self.progress_dialog.close_progress_dialog()
        notification(STR_ALL_x_EPISODES_MOVED_TO_STAGED)

    def move_all_seasons_to_staged(self, showtitle):
        """Move all Seasons to staged."""
        _showtitle = bold(showtitle)
        STR_MOVING_ALL_x_SEASONS_TO_STAGED = get_string(32026)
        STR_ALL_x_SEASONS_MOVED_TO_STAGED = get_string(32173) % colorize(
                _showtitle, "skyblue"
        )
        self.progress_dialog.create_progress_dialog(
                head=STR_MOVING_ALL_x_SEASONS_TO_STAGED % colorize(_showtitle)
        )
        items = list(self.database.get_content_items(status="managed", content_type="tvshow"))
        for index, item in enumerate(items):
            self.progress_dialog.update_progress_dialog(
                    index / len(items),
                    message=f"{colorize(bold(item.showtitle()))}\n{item.episode_title_with_id()}",
            )
            item.remove_from_library()
            item.set_as_staged()
        self.progress_dialog.close_progress_dialog()
        notification(STR_ALL_x_SEASONS_MOVED_TO_STAGED)

    def move_all_tvshows_to_staged(self):
        """Move all shows to staged."""
        STR_MOVING_ALL_TV_SHOWS_TO_STAGED = get_string(32026)
        STR_ALL_TV_SHOWS_MOVED_TO_STAGED = get_string(32027)
        self.progress_dialog.create_progress_dialog(
                head=STR_MOVING_ALL_TV_SHOWS_TO_STAGED
        )
        managed_tv_items = list(
                self.database.get_content_items(status="managed", content_type="tvshow")
        )
        for index, item in enumerate(managed_tv_items):
            self.progress_dialog.update_progress_dialog(
                    index / len(managed_tv_items),
                    message=f"{colorize(bold(item.showtitle()))}\n{item.episode_title_with_id()}",
            )
            item.remove_from_library()
            item.set_as_staged()
        self.progress_dialog.close_progress_dialog()
        notification(STR_ALL_TV_SHOWS_MOVED_TO_STAGED)

    def generate_all_managed_episodes_metadata(self, episodes):
        """Create metadata for all managed episodes."""
        STR_GENERATING_ALL_TV_EPISODES_METADATA = get_string(32181)
        STR_ALL_TV_EPISODES_METADATA_CREATED = get_string(32182)
        self.progress_dialog.create_progress_dialog(
                head=STR_GENERATING_ALL_TV_EPISODES_METADATA
        )
        for index, item in enumerate(episodes):
            self.progress_dialog.update_progress_dialog(
                    index / len(episodes),
                    "\n".join(
                            [
                                f"Criando metadados para: {colorize(bold(item.showtitle()))}",
                                f"Episode: {item.episode_title_with_id()}",
                            ]
                    ),
            )
            item.create_metadata_item()
        self.progress_dialog.close_progress_dialog()
        notification(STR_ALL_TV_EPISODES_METADATA_CREATED)

    def generate_all_managed_seasons_metadata(self, showtitle):
        """Create metadata for all managed seasons."""
        STR_GENERATING_ALL_TV_SEASONS_METADATA = get_string(32181)
        STR_ALL_TV_SEASONS_METADATA_CREATED = get_string(32182)
        self.progress_dialog.create_progress_dialog(
                head=STR_GENERATING_ALL_TV_SEASONS_METADATA
        )
        managed_seasons = list(
                self.database.get_season_items(status="managed", showtitle=showtitle)
        )
        for index, item in enumerate(managed_seasons):
            self.progress_dialog.update_progress_dialog(
                    index / len(managed_seasons),
                    "\n".join(
                            [
                                f"Criando metadados para: {colorize(bold(item.showtitle()))}",
                                f"Seasons {item.season()}",
                            ]
                    ),
            )
            item.create_metadata_item()
        self.progress_dialog.close_progress_dialog()
        notification(STR_ALL_TV_SEASONS_METADATA_CREATED)

    def generate_all_managed_tvshows_metadata(self):
        """Create metadata for all managed tvshows."""
        STR_GENERATING_ALL_TV_SHOWS_METADATA = get_string(32063)
        STR_ALL_TV_SHOWS_METADATA_CREATED = get_string(32064)
        self.progress_dialog.create_progress_dialog(
                head=STR_GENERATING_ALL_TV_SHOWS_METADATA
        )
        managed_tvshows = list(
                self.database.get_content_items(status="managed", content_type="tvshow")
        )
        for index, item in enumerate(managed_tvshows):
            self.progress_dialog.update_progress_dialog(
                    index / len(managed_tvshows),
                    "\n".join(
                            [
                                # TODO: add string to strings.po
                                f"Criando metadados para: {colorize(bold(item.showtitle()))}",
                                item.episode_title_with_id(),
                            ]
                    ),
            )
            item.create_metadata_item()
        self.progress_dialog.close_progress_dialog()
        notification(STR_ALL_TV_SHOWS_METADATA_CREATED)

    def episode_options(self, item, season):
        """Provide options for a single managed episode in a dialog window."""
        STR_GENERATE_EPISODE_METADATA = get_string(32017)
        STR_MOVE_BACK_TO_STAGED = get_string(32018)
        STR_BACK = get_string(32011)
        STR_MANAGED_EPISODE_OPTIONS = get_string(32036)
        lines = [STR_GENERATE_EPISODE_METADATA, STR_MOVE_BACK_TO_STAGED, STR_BACK]
        ret = xbmcgui.Dialog().select(
                " - ".join(
                        [
                            STR_MANAGED_EPISODE_OPTIONS,
                            colorize(bold(item.showtitle()), "skyblue"),
                            colorize(bold(item.episode_id()), "green"),
                        ]
                ),
                lines,
        )
        if ret >= 0:
            if lines[ret] == STR_GENERATE_EPISODE_METADATA:
                item.create_metadata_item()
            elif lines[ret] == STR_MOVE_BACK_TO_STAGED:
                item.remove_from_library()
                item.set_as_staged()
                self.view_episodes(item.showtitle(), season)
            elif lines[ret] == STR_BACK:
                self.view_episodes(item.showtitle(), season)
        self.view_episodes(item.showtitle(), season)

    def view_episodes(self, showtitle, season):
        """Display all managed episodes in the specified show, which are selectable and lead to options."""
        STR_NO_MANAGED_x_EPISODES = get_string(32028)
        STR_MANAGED_x_EPISODES = get_string(32031)
        managed_episodes = list(
                self.database.get_episode_items(
                        status="managed", showtitle=showtitle, season=season
                )
        )
        OPTIONS = {
            32183: [self.generate_all_managed_episodes_metadata, managed_episodes],
            32172: [self.move_all_episodes_to_staged, managed_episodes],
        }
        if not managed_episodes:
            xbmcgui.Dialog().ok(
                    ADDON_NAME,
                    STR_NO_MANAGED_x_EPISODES % colorize(bold(showtitle), "skyblue"),
            )
            self.show_all()
            return
        sel = Select(
                f"{ADDON_NAME} - {STR_MANAGED_x_EPISODES % colorize(bold(showtitle), 'skyblue')}"
        )
        sel.options([str(x) for x in managed_episodes])
        sel.extra_options([get_string(x) for x in OPTIONS])
        selection = sel.show(use_details=False, pre_select=False, back_option=True)
        if selection:
            if selection["type"] == "Item":
                self.episode_options(managed_episodes[selection["index1"]], season)
            elif selection["type"] == "opt":
                command = OPTIONS[list(OPTIONS.keys())[selection["index1"]]]
                command[0](command[1])
            self.view_seasons(showtitle)

    def view_seasons(self, showtitle):
        """Display all managed seasons in the specified show, which are selectable and lead to options."""
        STR_NO_MANAGED_X_SEASONS = get_string(32170)
        STR_MANAGED_X_SEASONS = get_string(32175)
        OPTIONS = {
            32181: self.generate_all_managed_seasons_metadata,
            32172: self.move_all_seasons_to_staged,
        }
        managed_seasons = list(
                self.database.get_season_items(status="managed", showtitle=showtitle)
        )
        sel = Select(
                heading=f"{ADDON_NAME} - {STR_MANAGED_X_SEASONS % colorize(bold(showtitle), 'skyblue')}",
                back_option=True,
        )
        sel.options([f"Season {x}" for x in {x.season() for x in managed_seasons}])
        sel.extra_options(OPTIONS)
        if not managed_seasons:
            xbmcgui.Dialog().ok(
                    ADDON_NAME,
                    STR_NO_MANAGED_X_SEASONS % colorize(bold(showtitle), "skyblue"),
            )
            self.show_all()
            return
        selection = sel.show(use_details=False, pre_select=False)
        if selection:
            if selection["type"] == "Item":
                self.view_episodes(
                        showtitle, season="".join(filter(str.isdigit, selection["str"]))
                )
            elif selection["type"] == "opt":
                command = OPTIONS[list(OPTIONS.keys())[selection["index1"]]]
                command(showtitle)
        self.show_all()

    def show_all(self):
        """Display all managed tvshows, which are selectable and lead to options."""
        STR_NO_MANAGED_TV_SHOWS = get_string(32020)
        STR_MANAGED_TV_SHOWS = get_string(32003)
        OPTIONS = {
            32022: self.move_all_tvshows_to_staged,
            32040: self.generate_all_managed_tvshows_metadata,
        }
        managed_tvshows = list(self.database.get_all_shows("managed"))
        sel = Select(
                heading=f"{ADDON_NAME} - {colorize(bold(STR_MANAGED_TV_SHOWS), 'lightblue')}",
                back_option=True,
        )
        sel.options([str(x) for x in managed_tvshows])
        sel.extra_options([get_string(x) for x in OPTIONS])
        if not managed_tvshows:
            xbmcgui.Dialog().ok(ADDON_NAME, STR_NO_MANAGED_TV_SHOWS)
            return
        selection = sel.show(use_details=False, pre_select=False)
        if selection:
            if selection["type"] == "Item":
                self.view_seasons(selection["str"])
            elif selection["type"] == "opt":
                command = OPTIONS[list(OPTIONS.keys())[selection["index1"]]]
                command()
