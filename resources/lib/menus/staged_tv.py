# -*- coding: utf-8 -*-

"""Defines the StagedTVMenu class."""

import xbmcgui

from resources import ADDON_NAME

from resources.lib.log import logged_function

from resources.lib.dialog_select import Select

from resources.lib.misc import bold, color, notification, get_string


class StagedTVMenu():
    """
    Provide windows for displaying staged tvshows and episodes.

    Provide tools for managing the items.
    """

    def __init__(self, database, progressdialog):
        """__init__ StagedTVMenu."""
        self.database = database
        self.progressdialog = progressdialog

    # @staticmethod
    # def rename_dialog(item):
    #     """Prompt input for new name, and rename if non-empty string."""
    #     input_ret = xbmcgui.Dialog().input(
    #         "Title",
    #         defaultt=item.showtitle()
    #     )
    #     if input_ret:
    #         item.rename(input_ret)

    # def rename_episodes_using_metadata(self, items):
    #     """Rename all episodes in show using nfo files."""
    #     STR_RENAMING_x_EPISODES_USING_METADATA = getstring(32075)
    #     STR_x_EPISODES_RENAMED_USING_METADATA = getstring(32076)
    #     showtitle = items[0].showtitle
    #     self.progressdialog.create_progressdialog(
    #         msg=STR_RENAMING_x_EPISODES_USING_METADATA % showtitle
    #     )
    #     for index, item in enumerate(items):
    #         self.progressdialog.update_progressdialog(
    #             index / len(items),
    #             f"{item.showtitle()}\n{item.episode_title_with_id()}"
    #         )
    #     self.progressdialog.close_progressdialog()
    #     notification(STR_x_EPISODES_RENAMED_USING_METADATA % showtitle)

    def add_all_staged_episodes_to_library(self, episodes):
        """Add all episodes from specified show to library."""
        STR_ADDING_ALL_x_EPISODES = get_string(32071)
        STR_ALL_x_EPISODES_ADDED = get_string(32072)
        showtitle = episodes[0].showtitle
        self.progressdialog.create_progressdialog(
            msg=STR_ADDING_ALL_x_EPISODES % showtitle
        )
        for index, item in enumerate(episodes):
            self.progressdialog.update_progressdialog(
                index / len(episodes),
                f"{color(bold(item.showtitle()))}\n{item.episode_title_with_id()}"
            )
            item.add_to_library()
        self.progressdialog.close_progressdialog()
        notification(
            STR_ALL_x_EPISODES_ADDED % color(
                bold(showtitle),
                'skyblue'
            )
        )

    def add_all_staged_seasons_to_library(self, showtitle):
        """Add all episodes from specified show to library."""
        # TODO: add to strings.po >
        STR_ADDING_ALL_x_SEASONS = 'Adding all %s seasons...'
        STR_ALL_x_SEASONS_ADDED = 'All %s seasons added'
        # <
        staged_seasons = list(
            self.database.get_season_items(
                status='staged',
                showtitle=showtitle
            )
        )
        self.progressdialog.create_progressdialog(
            msg=STR_ADDING_ALL_x_SEASONS % showtitle
        )
        for index, item in enumerate(staged_seasons):
            self.progressdialog.update_progressdialog(
                index / len(staged_seasons),
                f"{color(bold(item.showtitle()))}\n{item.episode_title_with_id()}"
            )
            item.add_to_library()
        self.progressdialog.close_progressdialog()
        notification(
            STR_ALL_x_SEASONS_ADDED % color(
                bold(showtitle),
                'skyblue'
            )
        )

    def add_all_staged_shows_to_library(self):
        """Add all tvshow items to library."""
        STR_ADDING_ALL_TV_SHOWS = get_string(32059)
        STR_ALL_TV_SHOWS_ADDED = get_string(32060)
        self.progressdialog.create_progressdialog(
            msg=STR_ADDING_ALL_TV_SHOWS
        )
        staged_tv_items = list(
            self.database.get_content_items(
                status='staged',
                _type='tvshow'
            )
        )
        for index, item in enumerate(staged_tv_items):
            self.progressdialog.update_progressdialog(
                index / len(staged_tv_items),
                f"{color(bold(item.showtitle()))}\n{item.episode_title_with_id()}"
            )
            item.add_to_library()
        self.progressdialog.close_progressdialog()
        notification(STR_ALL_TV_SHOWS_ADDED)

    def remove_all_shows(self):
        """Remove all staged tvshow items."""
        STR_REMOVING_ALL_TV_SHOWS = get_string(32024)
        STR_ALL_TV_SHOW_REMOVED = get_string(32025)
        self.progressdialog.create_progressdialog(
            msg=STR_REMOVING_ALL_TV_SHOWS
        )
        self.database.delete_item_from_table_with_status_or_showtitle(
            _type='tvshow',
            status='staged'
        )
        self.progressdialog.close_progressdialog()
        notification(STR_ALL_TV_SHOW_REMOVED)

    def remove_all_seasons(self, showtitle):
        """Remove all seasons from the specified show."""
        STR_REMOVING_ALL_x_SEASONS = get_string(32032) % showtitle
        STR_ALL_x_SEASONS_REMOVED = get_string(32033) % showtitle
        self.progressdialog.create_progressdialog(
            msg=STR_REMOVING_ALL_x_SEASONS
        )
        self.database.delete_item_from_table_with_status_or_showtitle(
            _type='tvshow',
            status='staged',
            showtitle=showtitle
        )
        self.progressdialog.close_progressdialog()
        notification(STR_ALL_x_SEASONS_REMOVED)

    def remove_all_episodes(self, showtitle):
        """Remove all episodes from the specified show."""
        formed_title = color(bold(showtitle), 'skyblue')
        STR_REMOVING_ALL_x_EPISODES = get_string(32032) % formed_title
        STR_ALL_x_EPISODES_REMOVED = get_string(32033) % formed_title
        self.progressdialog.create_progressdialog(
            msg=STR_REMOVING_ALL_x_EPISODES
        )
        self.database.delete_item_from_table_with_status_or_showtitle(
            _type='tvshow',
            status='staged',
            showtitle=showtitle
        )
        self.progressdialog.close_progressdialog()
        notification(STR_ALL_x_EPISODES_REMOVED)

    # TODO: CONTINUE HERE

    def remove_and_block_show(self, showtitle, season, episode):
        """Remove all itens from staged and add to blocked list."""
        raise NotImplementedError("Fix in future")
        # self.remove_all_shows
        # self.remove_all_seasons(showtitle)
        # self.remove_all_episodes
        # self.database.add_blocked_item(
        #     showtitle,
        #     'tvshow'
        # )

    # TODO: this method need update to follow dict style

    def episode_options(self, item, season):
        """Provide options for a single staged episode in a dialog window."""
        # TODO: rename associated metadata when renaming
        # TODO: rename show title
        # TODO: remove item (including metadata)
        STR_ADD = get_string(32048)
        STR_REMOVE = get_string(32017)
        STR_REMOVE_AND_BLOCK_EPISODE = get_string(32079)
        # STR_RENAME = getstring(32050)
        STR_GENERATE_METADATA_ITEM = get_string(32052)
        STR_BACK = get_string(32011)
        STR_STAGED_EPISODE_OPTIONS = get_string(32080)
        lines = [
            STR_ADD, STR_REMOVE,
            # STR_RENAME,
            STR_GENERATE_METADATA_ITEM,
            STR_BACK
        ]
        ret = xbmcgui.Dialog().select(
            f"{STR_STAGED_EPISODE_OPTIONS} - {color(bold(item.showtitle()), 'skyblue')} - {color(bold(item.episode_id()), 'green')}",
            lines
        )
        if ret >= 0:
            if lines[ret] == STR_ADD:
                item.add_to_library()
                self.view_episodes(item.showtitle(), season)
            elif lines[ret] == STR_REMOVE:
                item.delete()
                self.view_episodes(item.showtitle(), season)
            elif lines[ret] == STR_REMOVE_AND_BLOCK_EPISODE:
                item.remove_and_block()
                self.view_episodes(item.showtitle(), season)
            # elif lines[ret] == STR_RENAME:
                # self.rename_dialog(item)
                self.episode_options(item, season)
            elif lines[ret] == STR_GENERATE_METADATA_ITEM:
                item.create_metadata_item()
                self.episode_options(item, season)
            elif lines[ret] == STR_BACK:
                self.view_episodes(item.showtitle(), season)
                return
        else:
            self.view_episodes(item.showtitle(), season)

    def view_episodes(self, showtitle, season):
        STR_NO_STAGED_x_EPISODES = get_string(32065)
        STR_STAGED_x_EPISODES = get_string(32070)
        staged_episodes = list(
            self.database.get_episode_items(
                status='staged',
                showtitle=showtitle,
                season=season
            )
        )
        OPTIONS = {
            32066: [self.add_all_staged_episodes_to_library, staged_episodes],
            32029: [self.remove_all_episodes, showtitle],
            32068: [self.remove_and_block_show, showtitle],
            # 32069: [self.rename_episodes_using_metadata, staged_episodes],
        }
        if not staged_episodes:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_STAGED_x_EPISODES % color(bold(showtitle), 'skyblue')
            )
            self.view_shows()
            return
        sel = Select(
            f"{ADDON_NAME} - {STR_STAGED_x_EPISODES % color(bold(showtitle), 'skyblue')}"
        )
        sel.items([str(x) for x in staged_episodes])
        sel.extra_options([get_string(x) for x in OPTIONS])
        selection = sel.show(
            useDetails=False,
            preselect=False,
            back=True,
        )
        if selection:
            if selection['type'] == 'item':
                self.episode_options(
                    staged_episodes[selection['index1']],
                    season
                )
            elif selection['type'] == 'opt':
                command = OPTIONS[list(OPTIONS.keys())[selection['index1']]]
                command[0](command[1])
            self.view_shows()

    def view_seasons(self, showtitle):
        STR_STAGED_x_SEASONS = get_string(32176)
        STR_NO_STAGED_x_SEASONS = get_string(32170)
        OPTIONS = {
            32177: self.add_all_staged_seasons_to_library,
            32171: self.remove_all_seasons,
            32068: self.remove_and_block_show,
        }
        staged_seasons = list(
            self.database.get_season_items(
                status='staged',
                showtitle=showtitle
            )
        )
        sel = Select(
            heading=f"{ADDON_NAME} - {STR_STAGED_x_SEASONS % color(bold(showtitle), 'skyblue')}"
        )
        sel.items(
            [f'Season {x}' for x in {x.season() for x in staged_seasons}]
        )
        sel.extra_options(list(map(get_string, OPTIONS)))
        if not staged_seasons:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_STAGED_x_SEASONS % color(
                    bold(showtitle),
                    'skyblue'
                )
            )
            self.view_shows()
            return
        selection = sel.show(
            useDetails=False,
            preselect=False,
            back=True,
        )
        if selection:
            if selection['type'] == 'item':
                self.view_episodes(
                    showtitle,
                    season=''.join(
                        filter(str.isdigit, selection['str'])
                    )
                )
            elif selection['type'] == 'opt':
                command = OPTIONS[list(OPTIONS.keys())[selection['index1']]]
                command(showtitle)

    def view_shows(self):
        """Display all managed tvshows, which are selectable and lead to options."""
        STR_NO_STAGED_TV_SHOWS = get_string(32054)
        STR_STAGED_TV_SHOWS = get_string(32005)
        OPTIONS = {
            32055: self.add_all_staged_shows_to_library,
            32057: self.remove_all_shows,
        }
        staged_tvshows = list(
            self.database.get_all_shows('staged')
        )
        sel = Select(
            heading=f"{ADDON_NAME} - {color(bold(STR_STAGED_TV_SHOWS), 'lightblue')}"
        )
        sel.items([str(x) for x in staged_tvshows])
        sel.extra_options([get_string(x) for x in OPTIONS])
        if not staged_tvshows:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_STAGED_TV_SHOWS
            )
            return
        selection = sel.show(
            useDetails=False,
            preselect=False,
            back=True,
        )
        if selection:
            if selection['type'] == 'item':
                self.view_seasons(selection['str'])
            elif selection['type'] == 'opt':
                command = OPTIONS[list(OPTIONS.keys())[selection['index1']]]
                command()
