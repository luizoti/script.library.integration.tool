#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Defines the ManagedTVMenu class."""

import xbmc  # pylint: disable=import-error
import xbmcgui  # pylint: disable=import-error

from resources import ADDON_NAME
from resources.lib.log import logged_function

from resources.lib.utils import bold
from resources.lib.utils import color
from resources.lib.utils import notification
from resources.lib.utils import getlocalizedstring


class ManagedTVMenu(object):
    """
    Provide windows for displaying managed shows and episodes.

    Also tools for manipulating the objects and managed file.
    """

    def __init__(self, database, progressdialog):
        """__init__ ManagedTVMenu."""
        self.database = database
        self.progressdialog = progressdialog

    @logged_function
    def move_episodes_to_staged(self, items):
        """Remove all managed episodes in specified show from library, and add them to staged."""
        STR_MOVING_ALL_x_EPISODES_TO_STAGED = getlocalizedstring(32034)
        STR_ALL_x_EPISODES_MOVED_TO_STAGED = getlocalizedstring(
            32035)
        self.progressdialog._create(
            msg=STR_MOVING_ALL_x_EPISODES_TO_STAGED % color(items[0].showtitle)
        )
        for index, item in enumerate(items):
            self.progressdialog._update(
                index / len(items),
                message='\n'.join([color(item.showtitle), item.episode_title_with_id]
                )
            )
            item.remove_from_library()
            item.set_as_staged()
        self.progressdialog._close()
        notification(STR_ALL_x_EPISODES_MOVED_TO_STAGED %
                     color(item.showtitle, 'skyblue'))

    @logged_function
    def move_all_seasons_to_staged(self, showtitle):
        """Remove all managed episodes in specified show from library, and add them to staged."""
        STR_MOVING_ALL_x_SEASONS_TO_STAGED = getlocalizedstring(32026)
        STR_ALL_x_SEASONS_MOVED_TO_STAGED = getlocalizedstring(
            32173) % color(showtitle, 'skyblue')
        self.progressdialog._create(
            msg=STR_MOVING_ALL_x_SEASONS_TO_STAGED % color(showtitle)
        )
        items = list(
            self.database.get_content_items(
                status='managed',
                _type='tvshow'
            )
        )
        for index, item in enumerate(items):
            self.progressdialog._update(
                index / len(items),
                message='\n'.join([color(item.showtitle), item.episode_title_with_id])
            )
            item.remove_from_library()
            item.set_as_staged()
        self.progressdialog._close()
        notification(STR_ALL_x_SEASONS_MOVED_TO_STAGED)

    @logged_function
    def move_all_to_staged(self):
        """Remove all managed tvshow items from library, and add them to staged."""
        STR_MOVING_ALL_TV_SHOWS_TO_STAGED = getlocalizedstring(32026)
        STR_ALL_TV_SHOWS_MOVED_TO_STAGED = getlocalizedstring(32027)
        self.progressdialog._create(
            msg=STR_MOVING_ALL_TV_SHOWS_TO_STAGED
        )
        managed_tv_items = list(
            self.database.get_content_items(
                status='managed',
                _type='tvshow'
            )
        )
        for index, item in enumerate(managed_tv_items):
            self.progressdialog._update(
                index / len(managed_tv_items),
                msg='\n'.join([color(item.showtitle), item.episode_title_with_id]
                    )
            )
            item.remove_from_library()
            item.set_as_staged()
        self.progressdialog._close()
        notification(STR_ALL_TV_SHOWS_MOVED_TO_STAGED)

    @logged_function
    def remove_episodes(self, items):
        """Remove all episodes in specified show from library."""
        STR_REMOVING_ALL_x_EPISODES = getlocalizedstring(32032)
        STR_ALL_x_EPISODES_REMOVED = getlocalizedstring(32033)
        showtitle = items[0].showtitle
        self.progressdialog._create(
            msg=STR_REMOVING_ALL_x_EPISODES % showtitle
        )
        for index, item in enumerate(items):
            self.progressdialog._update(
                index / len(items),
                message='\n'.join([item.showtitle, item.episode_title_with_id])
            )
            item.remove_from_library()
            item.delete()
        self.progressdialog._close()
        notification(STR_ALL_x_EPISODES_REMOVED % showtitle)

    @logged_function
    def remove_seasons(self, items, showtitle):
        """Remove all seasons in specified show from library."""
        STR_REMOVING_ALL_X_SEASONS = getlocalizedstring(32168)
        STR_ALL_X_SEASONS_REMOVED = getlocalizedstring(32169)
        seasons = items[0]
        self.progressdialog._create(
            msg=STR_REMOVING_ALL_X_SEASONS % showtitle
        )
        for season in seasons:
            self.progressdialog._update(
                season / len(seasons),
                message='\n'.join([color(showtitle), str("Season: %s" % season)])
            )
            self.database.remove_from(
                _type='tvshow',
                showtitle=showtitle,
                season=season
            )
            xbmc.sleep(300)
        self.progressdialog._close()
        notification(STR_ALL_X_SEASONS_REMOVED % showtitle)

    @logged_function
    def generate_all_managed_metadata(self):
        """Create metadata for all staged tvshow items."""
        STR_GENERATING_ALL_TV_SHOW_METADATA = getlocalizedstring(32063)
        STR_ALL_TV_SHOW_METADATA_CREATED = getlocalizedstring(32064)
        self.progressdialog._create(
            msg=STR_GENERATING_ALL_TV_SHOW_METADATA
        )
        staged_tv_items = list(
            self.database.get_content_items(
                status='staged',
                _type='tvshow'
            )
        )
        for index, item in enumerate(staged_tv_items):
            self.progressdialog._update(
                index / len(staged_tv_items),
                '\n'.join([item.showtitle])
            )
            item.create_metadata_item()
        self.progressdialog._close()
        notification(STR_ALL_TV_SHOW_METADATA_CREATED)

    @logged_function
    def remove_all(self):
        """Remove all managed tvshow items from library."""
        STR_REMOVING_ALL_TV_SHOWS = getlocalizedstring(32024)
        STR_ALL_TV_SHOWS_REMOVED = getlocalizedstring(32025)
        self.progressdialog._create(
            msg=STR_REMOVING_ALL_TV_SHOWS
        )
        managed_tv_items = list(
            self.database.get_content_items(
                status='managed',
                _type='tvshow'
            )
        )
        for index, item in enumerate(managed_tv_items):
            self.progressdialog._update(
                index / len(managed_tv_items),
                message='\n'.join([color(item.showtitle), item.episode_title_with_id]
                )
            )
            item.remove_from_library()
            item.delete()
        self.progressdialog._close()
        notification(STR_ALL_TV_SHOWS_REMOVED)

    @logged_function
    def episode_options(self, item, season):
        """Provide options for a single managed episode in a dialog window."""
        STR_REMOVE = getlocalizedstring(32017)
        STR_MOVE_BACK_TO_STAGED = getlocalizedstring(32018)
        STR_BACK = getlocalizedstring(32011)
        STR_MANAGED_EPISODE_OPTIONS = getlocalizedstring(32036)
        lines = [
            STR_REMOVE,
            STR_MOVE_BACK_TO_STAGED,
            STR_BACK
        ]
        ret = xbmcgui.Dialog().select(
            '{0} - {1} - {2}'.format(
                STR_MANAGED_EPISODE_OPTIONS,
                color(item.showtitle, 'skyblue'),
                color(item.episode_title_with_id.split(
                    ' - ')[0], colorname='green')
            ), lines
        )
        if ret >= 0:
            if lines[ret] == STR_REMOVE:
                item.remove_from_library()
                item.delete()
                self.view_episodes(item.showtitle, season)
            elif lines[ret] == STR_MOVE_BACK_TO_STAGED:
                item.remove_from_library()
                item.set_as_staged()
                self.view_episodes(item.showtitle, season)
            elif lines[ret] == STR_BACK:
                self.view_episodes(item.showtitle, season)
        self.view_episodes(item.showtitle, season)

    @logged_function
    def view_episodes(self, showtitle, season):
        """
        Display all managed episodes in the specified show, which are selectable and lead to options.

        Also provides additional options at bottom of menu.
        """
        STR_NO_MANAGED_x_EPISODES = getlocalizedstring(32028)
        STR_REMOVE_ALL_EPISODES = getlocalizedstring(32029)
        STR_MOVE_ALL_EPISODES_BACK_TO_STAGED = getlocalizedstring(32172)
        STR_BACK = getlocalizedstring(32011)
        STR_MANAGED_x_EPISODES = getlocalizedstring(32031)
        managed_episodes = list(
            self.database.get_episode_items(
                status='managed',
                showtitle=showtitle,
                season=season
            )
        )
        if not managed_episodes:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_MANAGED_x_EPISODES % color(showtitle, 'skyblue')
            )
            self.view_shows()
            return
        lines = [str(x) for x in managed_episodes]
        lines += [
            STR_REMOVE_ALL_EPISODES,
            STR_MOVE_ALL_EPISODES_BACK_TO_STAGED,
            STR_BACK
        ]
        ret = xbmcgui.Dialog().select(
            '%s - %s' % (
                ADDON_NAME,
                STR_MANAGED_x_EPISODES % color(showtitle, 'skyblue')
            ), lines
        )
        if ret >= 0:
            if ret < len(managed_episodes):  # managed item
                for i, item in enumerate(managed_episodes):
                    if ret == i:
                        self.episode_options(item, season)
            elif lines[ret] == STR_REMOVE_ALL_EPISODES:
                self.remove_episodes(managed_episodes)
                self.view_shows()
            elif lines[ret] == STR_MOVE_ALL_EPISODES_BACK_TO_STAGED:
                self.move_episodes_to_staged(managed_episodes)
                self.view_shows()
            elif lines[ret] == STR_BACK:
                self.view_seasons(showtitle)
        else:
            self.view_seasons(showtitle)

    @logged_function
    def view_seasons(self, showtitle):
        """
        Display all managed seasons in the specified show, which are selectable and lead to options.

        Also provides additional options at bottom of menu.
        """
        STR_NO_MANAGED_X_SEASONS = getlocalizedstring(32170)
        STR_REMOVE_ALL_SEASONS = getlocalizedstring(32171)
        STR_MOVE_ALL_SEASONS_BACK_TO_STAGED = getlocalizedstring(32172)
        STR_BACK = getlocalizedstring(32011)
        STR_MANAGED_X_SEASONS = getlocalizedstring(32175)
        managed_seasons = list(
            self.database.get_season_items(
                status='managed',
                showtitle=showtitle
            )
        )
        if not managed_seasons:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_MANAGED_X_SEASONS % color(showtitle, 'skyblue')
            )
            self.view_shows()
            return
        season_interger_list = list(set([x.season for x in managed_seasons]))
        lines = [str('[B]Season %s[/B]' % x) for x in season_interger_list]
        lines += [
            STR_REMOVE_ALL_SEASONS,
            STR_MOVE_ALL_SEASONS_BACK_TO_STAGED,
            STR_BACK
        ]
        ret = xbmcgui.Dialog().select(
            '%s - %s' % (
                ADDON_NAME,
                STR_MANAGED_X_SEASONS % color(showtitle, 'skyblue')
            ), lines
        )
        selection = lines[ret]
        if ret >= 0:
            if selection == STR_REMOVE_ALL_SEASONS:
                self.remove_seasons(managed_seasons, showtitle)
                self.view_shows()
            elif selection == STR_MOVE_ALL_SEASONS_BACK_TO_STAGED:
                self.move_all_seasons_to_staged(showtitle)
                self.view_shows()
            elif selection == STR_BACK:
                self.view_shows()
            else:
                self.view_episodes(
                    showtitle=showtitle,
                    season=''.join(
                        filter(
                            str.isdigit,
                            selection
                        )
                    )
                )
        else:
            self.view_shows()

    @logged_function
    def view_shows(self):
        """
        Display all managed tvshows, which are selectable and lead to options.

        Also provides additional options at bottom of menu.
        """
        STR_NO_MANAGED_TV_SHOWS = getlocalizedstring(32020)
        STR_REMOVE_ALL_TV_SHOWS = getlocalizedstring(32021)
        STR_MOVE_ALL_TV_SHOWS_BACK_TO_STAGED = getlocalizedstring(32022)
        STR_GENERATE_ALL_METADATA_ITEMS = getlocalizedstring(32040)
        STR_BACK = getlocalizedstring(32011)
        STR_MANAGED_TV_SHOWS = getlocalizedstring(32023)
        managed_tvshows = list(
            self.database.get_all_shows('managed')
        )
        if not managed_tvshows:
            xbmcgui.Dialog().ok(
                ADDON_NAME,
                STR_NO_MANAGED_TV_SHOWS
            )
            return
        lines = [bold(x) for x in managed_tvshows]
        lines += [
            STR_REMOVE_ALL_TV_SHOWS,
            STR_MOVE_ALL_TV_SHOWS_BACK_TO_STAGED,
            STR_GENERATE_ALL_METADATA_ITEMS,
            STR_BACK
        ]
        ret = xbmcgui.Dialog().select(
            '%s - %s' % (
                ADDON_NAME,
                bold(STR_MANAGED_TV_SHOWS)
            ), lines
        )
        if ret >= 0:
            if ret < len(managed_tvshows):
                for showtitle in managed_tvshows:
                    if managed_tvshows[ret] == showtitle:
                        self.view_seasons(showtitle)
                        break
            elif lines[ret] == STR_REMOVE_ALL_TV_SHOWS:
                self.remove_all()
            elif lines[ret] == STR_MOVE_ALL_TV_SHOWS_BACK_TO_STAGED:
                self.move_all_to_staged()
            elif lines[ret] == STR_GENERATE_ALL_METADATA_ITEMS:
                self.generate_all_managed_metadata()
                self.view_shows()
            elif lines[ret] == STR_BACK:
                return
