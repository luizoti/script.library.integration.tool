# -*- coding: utf-8 -*-

"""Defines the DatabaseHandler class."""

import logging
import sqlite3
from os.path import basename
from sqlite3 import Cursor

from resources.lib import DATABASE_PATH

# from resources.lib import AUTO_ADD_MOVIES, AUTO_ADD_TVSHOWS
# from resources.lib import (build_contentitem, build_contentmanager,
#                            build_json_item)
# from resources.lib.items.blocked import BlockedItem
# from resources.lib.items.synced import SyncedItem

LOG = logging.getLogger(basename(__file__))


class DBConnection:
    """A base class to connect to db."""

    def __init__(self) -> None:
        # super(DBConnection, self).__init__()

        self.conection = sqlite3.connect(DATABASE_PATH)
        LOG.info("DATABASE PATH: %s", DATABASE_PATH)
        self.conection.row_factory = self.__dict_factory
        self.conection.text_factory = str
        self.cursor = self.conection.cursor()
        self._default_querys = {
            "update": {
                "movie": "UPDATE movie",
                "tvshow": "UPDATE tvshow",
                "music": "UPDATE music",
            },
            "delete": {
                "movie": "DELETE FROM movie",
                "tvshow": "DELETE FROM tvshow",
                "music": "DELETE FROM music",
            },
            "insert": {
                "movie": "INSERT OR IGNORE INTO movie",
                "tvshow": "INSERT OR IGNORE INTO tvshow",
                "music": "INSERT OR IGNORE INTO music",
            },
            "select": {
                "movie": "SELECT * FROM movie",
                "tvshow": "SELECT * FROM tvshow",
                "music": "SELECT * FROM music",
                "blocked": "SELECT * FROM blocked",
                "synced": "SELECT * FROM synced",
                "content": "SELECT * FROM content",
            },
        }

    @staticmethod
    def __dict_factory(cursor: Cursor, row: tuple) -> dict:
        """Convert database rows into dicts.

        Args:
            cursor (Cursor): Sqlite3 cursor
            row (tuple): Database row tuple

        Returns:
            dict: A dict with column and values.
        """
        query_dict = {}
        values = [item[0] for item in cursor.description]

        for row_dict in [dict(zip(values, row))]:
            try:
                key = row_dict["showtitle"]
            except KeyError:
                key = row_dict["title"]

            query_dict[key] = row_dict
        return query_dict

    def __del__(self):
        """Close database connection."""
        try:
            self.conection.close()
            LOG.info("DBConnection sucessfuly closed.")
        except AttributeError:
            pass
        except Exception:
            LOG.exception("Database.__del__ Disconnection error:")
