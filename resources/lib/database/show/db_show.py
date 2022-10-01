# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-

"""Defines the DatabaseHandler class."""

import logging
from distutils.log import debug
from functools import reduce
from os.path import basename
from sqlite3 import Cursor

from resources.lib.database.connection import DBConnection
from resources.lib.database.database import DBCommon
from resources.lib.menus import show

# from resources.lib import AUTO_ADD_MOVIES, AUTO_ADD_TVSHOWS
# from resources.lib import (build_contentitem, build_contentmanager,
#                            build_json_item)
# from resources.lib.items.blocked import BlockedItem
# from resources.lib.items.synced import SyncedItem

LOG = logging.getLogger(basename(__file__))


class DBShows(DBCommon):
    """Class with common query's for all type of contents."""

    def get_content_items(self, status: str, content_type: str) -> dict:
        """
        Perform database query for all items and return as dict

        keyword arguments:
            status: string, 'managed' or 'staged'
            content_type: string, 'movie' or 'tvshow'
        return:
            dict: Return a dict with showtitle as key and a list
            of all values with all episodes.
        """
        self.cursor.execute(
            f"{self._default_queries.get('select')[content_type]} WHERE status=:status",
            {"status": status},
        )
        result: list = self.cursor.fetchall()
        shows = {list(x.keys())[0]: [] for x in result}
        for value in result:
            for item in list(shows):
                values = value.get(item)
                if values:
                    shows[item].append(values)
        return shows

    def get_all_shows(self, status):
        """
        Query Content table for all (not null) distinct showtitles.
            Cast results as list of strings.
        """
        # Query database
        self.cursor.execute(
            """
            SELECT DISTINCT
                showtitle
            FROM
                tvshow
            WHERE
                status=:status
            ORDER BY
                (
                    CASE WHEN
                        showtitle
                    LIKE
                        'the %'
                    THEN
                        substr(showtitle,5)
                    ELSE
                        showtitle
                    END
                ) COLLATE NOCASE""",
            {"status": status},
        )
        for item in self.cursor.fetchall():
            yield item[0]