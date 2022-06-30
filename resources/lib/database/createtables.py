# -*- coding: utf-8 -*-

import logging
from os.path import basename

from resources.lib.database.connection import DBConnection

LOG = logging.getLogger(basename(__file__))


class DBCreateTables(DBConnection):
    """Create database and tables if not exist."""

    def __init__(self) -> None:
        super().__init__()
        # Create tables if they doesn't exist
        table_map = {
            "movie": {
                "file": "TEXT PRIMARY KEY",
                "title": "TEXT",
                "type": "TEXT",
                "status": "TEXT",
                "year": "TEXT",
            },
            "tvshow": {
                "file": "TEXT PRIMARY KEY",
                "title": "TEXT",
                "type": "TEXT",
                "status": "TEXT",
                "year": "TEXT",
                "showtitle": "TEXT",
                "season": "TEXT",
                "episode": "TEXT",
            },
            "synced": {
                "file": "TEXT PRIMARY KEY",
                "label": "TEXT",
                "type": "TEXT",
            },
            "blocked": {
                "value": "TEXT NOT NULL",
                "type": "TEXT NOT NULL",
            },
        }
        for table_name, table_fields in table_map.items():
            try:
                self.cursor.execute(self.__convert_to_query(table_name, table_fields))
                self.conection.commit()
            except Exception:  # pylint: disable=broad-except
                LOG.exception("CreateTables Error:")

    @staticmethod
    def __convert_to_query(table_name, table_fields):
        fields = [" ".join(x) for x in table_fields.items()]
        return f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(fields)})"
