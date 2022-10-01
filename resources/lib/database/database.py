# pylint: disable=too-few-public-methods
# -*- coding: utf-8 -*-

"""Defines the DatabaseHandler class."""

import logging
from functools import reduce
from os.path import basename

from resources.lib.database.connection import DBConnection

# from resources.lib import AUTO_ADD_MOVIES, AUTO_ADD_TVSHOWS
# from resources.lib import (build_contentitem, build_contentmanager,
#                            build_json_item)
# from resources.lib.items.blocked import BlockedItem
# from resources.lib.items.synced import SyncedItem

LOG = logging.getLogger(basename(__file__))


class DBCommon(DBConnection):
    """Class with common query's for all type of contents."""

    # def __init__(self) -> None:
    #     super(DBCommon, self).__init__()

    def get_content_items(self, status: str, content_type: str) -> dict:
        """
        Perform database query for all items and return as dict

        keyword arguments:
            status: string, 'managed' or 'staged'
            content_type: string, 'movie' or 'tvshow'
        return:
            dict: Return a dict with content name (title or showtitle)
            and value is as dict with all other database values.
        """
        self.cursor.execute(
            f"{self._default_queries.get('select')[content_type]} WHERE status=:status",
            {"status": status},
        )
        try:
            return reduce(lambda a, b: {**a, **b}, self.cursor.fetchall())
        except TypeError:
            pass
        return {}

    def update_status(self, file, content_type, status):
        """Update a status for a single entries in database."""
        self.cursor.execute(
            f"{self._default_queries.get('update')[content_type]} SET status=:status WHERE file=:file",
            {"file": file, "status": status},
        )
        self.connection.commit()

    # def update_title(self, file, content_type, title):
    #     """Update a title for a single entries in database."""
    #     self.cursor.execute(
    #         f"{self._default_queries.get('update')[content_type]} SET title=:title WHERE file=:file",
    #         {"file": file, "title": title},
    #     )
    #     self.connection.commit()

    def delete(self, file, content_type):
        """Delete an entry in the table using the 'file' key, regardless of status."""
        self.cursor.execute(
            f"DELETE FROM {content_type} WHERE file=:file",
            {"file": file},
        )
        self.connection.commit()

    def block(self, value, content_type):
        """Add an item to blocked with the specified values."""
        # TODO: block with title only? maybe is necessary use url to block.
        self.cursor.execute(
            "INSERT INTO blocked (value, type) VALUES (:value, :type)",
            {"value": value, "type": content_type},
        )
        self.connection.commit()

    # def check_if_is_blocked(self, value, content_type=None):
    #     """Check if value exist in blocked and return True else None"""
    #     self.cursor.execute(
    #             "SELECT * FROM blocked WHERE value=:value AND type=:type",
    #         {"value": value, "type": content_type},
    #     )
    #     return True if self.cursor.fetchone() else None


# class Database:
#     """Database class with all database methods."""

#     # TODO: Reimplement blocked keywords
#     # TODO: Combine remove_content_item functions using **kwargs
#     def __init__(self):
#         """__init__ database."""
#         # Connect to database
#         LOG.info("DATABASE PATH: %s", DATABASE_PATH)
#         self.conn = sqlite3.connect(DATABASE_PATH)
#         self.conn.row_factory = self._dict_factory
#         self.conn.text_factory = str
#         self.cur = self.conn.cursor()
#         self.UPDATE_DICT_QUERY = {
#             "movie": "UPDATE movie",
#             "tvshow": "UPDATE tvshow",
#             "music": "UPDATE music",
#         }
#         self.DELETE_DICT_QUERY = {
#             "movie": "DELETE FROM movie",
#             "tvshow": "DELETE FROM tvshow",
#             "music": "DELETE FROM music",
#         }
#         self.INSERT_DICT_QUERY = {
#             "movie": "INSERT OR IGNORE INTO movie",
#             "tvshow": "INSERT OR IGNORE INTO tvshow",
#             "music": "INSERT OR IGNORE INTO music",
#         }
#         self.SELECT_DICT_QUERY = {
#             "movie": "SELECT * FROM movie",
#             "tvshow": "SELECT * FROM tvshow",
#             "music": "SELECT * FROM music",
#             "blocked": "SELECT * FROM blocked",
#             "synced": "SELECT * FROM synced",
#             "content": "SELECT * FROM content",
#         }

#     def __del__(self):
#         """Close database connection."""
#         try:
#             self.conn.close()
#         except AttributeError:
#             LOG.exception("Database.__del__ Disconnection error:")

#     def get_content_items(self, status: str, content_type: str) -> dict:
#         """
#         Perform database query for all items and returno as dict

#         keyword arguments:
#             status: string, 'managed' or 'staged'
#             content_type: string, 'movie' or 'tvshow'
#         return:
#             dict: Return a dict with content name (title or showtitle)
#             and value is as dict with all other database values.
#         """
#         self.cur.execute(
#             " ".join([self.SELECT_DICT_QUERY[content_type], "WHERE status=:status"]),
#             {"status": status},
#         )
#         return reduce(lambda a, b: {**a, **b}, self.cur.fetchall())

#         # return [{x[1]: dict(zip(mediatype_keys[len(x)], x))} for x in values]
#         # for content in self.cur.fetchall():
#         #     json_item = build_json_item(content)
#         #     yield build_contentmanager(self, build_contentitem(json_item))

#     def load_item(self, file):
#         """Query a single item and return as a json."""
#         self.cur.execute(
#             " ".join([self.SELECT_DICT_QUERY["content"], "WHERE file=:file"]),
#             {"file": file},
#         )
#         # return build_json_item(self.cur.fetchone())

#     def path_exists(self, file):
#         """
#         Check if item exist in all tables.

#         If exist return a list with table and type else None.
#         """
#         table = None
#         status = None
#         for table_type in ["movie", "tvshow"]:
#             LOCAL_SELECT_DICT_QUERY = {
#                 "movie": "SELECT status FROM movie",
#                 "tvshow": "SELECT status FROM tvshow",
#             }
#             sql_comm = " ".join(
#                 [
#                     LOCAL_SELECT_DICT_QUERY[table_type],
#                     "WHERE file=:file",
#                 ]
#             )
#             result = self.cur.execute(sql_comm, {"file": file}).fetchone()
#             if result:
#                 table = table_type
#                 status = result[0]
#         if table and status:
#             return [table, status]
#         return None

#     def add_content_item(self, jsondata):
#         """Add content to library."""
#         content_type = jsondata["type"]
#         query_defs = {
#             "tvshow": (
#                 "(file,title,type,status,year,showtitle,season,episode)",
#                 "(:file,:title,:type,'staged',:year,:showtitle,:season,:episode)",
#             ),
#             "movie": (
#                 "(file,title,type,status,year)",
#                 "(:file,:title,:type,'staged',:year)",
#             ),
#             "music": ValueError("Not implemented yet, music"),
#         }
#         # sqlite named style:
#         self.cur.execute(
#             f"{self.INSERT_DICT_QUERY[content_type]} {query_defs[content_type][0]} VALUES {query_defs[content_type][1]}",
#             jsondata,
#         )
#         self.conn.commit()
#         # contentmanager = build_contentmanager(self, jsondata)
#         # if jsondata["type"] == "tvshow":
#         #     if AUTO_ADD_TVSHOWS:
#         #         contentmanager.add_to_library()
#         # elif jsondata["type"] == "movie":
#         #     if AUTO_ADD_MOVIES:
#         #         contentmanager.add_to_library()
#         # elif jsondata["type"] == "music":
#         #     # TODO: Music params
#         #     raise NotImplementedError("Not implemented yet")

#     def add_item_to_synced(self, label, path, content_type):
#         """Create an entry in synced with specified values."""
#         self.cur.execute(
#             """INSERT OR REPLACE INTO
#                     synced
#                     (file, label, type)
#                 VALUES
#                     (:file, :label, :type)
#             """,
#             {"file": path, "label": label, "type": contentcontent_type},
#         )
#         self.conn.commit()

#     def get_all_blocked_itens(self):
#         """Return all items in blocked as a list of BlockedItem objects."""
#         self.cur.execute(
#             " ".join([self.SELECT_DICT_QUERY["blocked"], "ORDER BY type, value"])
#         )
#         # return [BlockedItem(*x) for x in self.cur.fetchall()]



#     def get_season_items(self, status, showtitle):
#         """Get seasons of a show and return as ContentManager object."""
#         self.cur.execute(
#             """
#                         SELECT
#                             *
#                         FROM
#                             tvshow
#                         WHERE
#                             status=:status
#                         AND
#                             showtitle=:showtitle
#                         ORDER BY
#                         CAST(season AS INTEGER)""",
#             {
#                 "status": status,
#                 "showtitle": showtitle,
#             },
#         )
#         # for content in self.cur.fetchall():
#         #     json_item = build_json_item(content)
#         #     yield build_contentmanager(self, build_contentitem(json_item))

#     def get_episode_items(self, status, showtitle, season):
#         """Get episodes of a show and return as a ContentManager object."""
#         sql_comm = """
#                     SELECT
#                         *
#                     FROM
#                         tvshow
#                     WHERE
#                         status=:status
#                     AND
#                         showtitle=:showtitle
#                     AND
#                         season=:season
#                     ORDER BY CAST
#                         (season AS INTEGER),
#                     CAST
#                         (episode AS INTEGER)"""
#         self.cur.execute(
#             sql_comm, {"status": status, "showtitle": showtitle, "season": season}
#         )
#         # for content in self.cur.fetchall():
#         #     json_item = build_json_item(content)
#         #     yield build_contentmanager(self, build_contentitem(json_item))

#     def get_synced_dirs(self, synced_type=None):
#         """Get all itens in synced or itens by type."""
#         orderby_str = """ORDER BY
#                             (
#                                 CASE WHEN
#                                     label
#                                 LIKE
#                                     'the %'
#                                 THEN
#                                     substr(label,5)
#                                 ELSE
#                                     label
#                                 END
#                             ) COLLATE NOCASE"""
#         self.cur.execute(
#             " ".join(
#                 [
#                     self.SELECT_DICT_QUERY["select"],
#                     "WHERE type=:type" if synced_type else "",
#                     orderby_str,
#                 ]
#             ),
#             {"type": syncedcontent_type},
#         )
#         # return [SyncedItem(*x) for x in self.cur.fetchall()]

#     def delete_item_from_table_with_status_or_showtitle(
#         self, content_type, status, showtitle=None
#     ):
#         """
#         Delete an entry in the table using the 'status' and 'showtitle', key.

#         Without showtitle, all entries will be deleted.

#         Keys:
#             - status = ['staged', 'managed']
#         """
#         self.cur.execute(
#             " ".join(
#                 [
#                     self.DELETE_DICT_QUERY[content_type],
#                     "WHERE status=:status",
#                     "AND showtitle=:showtitle" if showtitle else "",
#                 ]
#             ),
#             {"status": status, "showtitle": showtitle},
#         )
#         self.conn.commit()

#     def delete_item_from_table_with_season(self, content_type, showtitle, season):
#         """Delete an entry in the table using the 'showtitle' and 'season' key."""
#         self.cur.execute(
#             " ".join(
#                 [
#                     self.DELETE_DICT_QUERY[content_type],
#                     "WHERE showtitle=:showtitle AND season=:season",
#                 ]
#             ),
#             {"season": season, "showtitle": showtitle},
#         )
#         self.conn.commit()

#     def delete_entrie_from_blocked(self, value, content_type):
#         """Delete one entrie from blocked."""
#         self.cur.execute(
#             """DELETE FROM
#                     blocked
#                 WHERE
#                     value="%s"
#                 AND
#                     type=:type""",
#             {"value": value, "type": contentcontent_type},
#         )
#         self.conn.commit()

#     def delete_all_from_synced(self):
#         """Remove all dirs from synced."""
#         self.cur.execute("DELETE FROM synced")
#         self.conn.commit()

#     def delete_dir_from_synced(self, file):
#         """Remove one dir from synced."""
#         self.cur.execute("DELETE FROM synced WHERE file=?", {"file": file})
#         self.conn.commit()


#     def update_showtitle_in_database(self, file, content_type, showtitle):
#         """Update a showtitle for a single entrie in database."""
#         self.cur.execute(
#             " ".join(
#                 [
#                     self.UPDATE_DICT_QUERY[content_type],
#                     "SET showtitle=:showtitle WHERE file=:file",
#                 ]
#             ),
#             {"file": file, "type": content_type, "showtitle": showtitle},
#         )
#         self.conn.commit()
