# -*- coding: utf-8 -*-

"""StagedShow docstring."""

from dataclasses import InitVar, dataclass

from resources.lib.content.show.show import EpisodeFileManager
from resources.lib.database.show.db_show import DBShows


@dataclass
class StagedShow(EpisodeFileManager):
    """
    Staged only create files, delete file methods is not necessary.
    """

    database: InitVar[DBShows] = None

    def __post_init__(self, database):
        self.database = database

    def move_to_managed(self):
        """Create nfo, strm and add item to library (managed database)."""
        self.build_tvshow_nfo_string()
        self.create_nfo()
        self.build_episode_nfo_string()
        self.create_nfo()
        self.create_strm()
        self.database.update_status(
                showtitle=self.showtitle, content_type="tvshow", status="managed"
        )

    def delete_from_staged(self):
        """Remove the item from (staged) database with optional block."""
        self.database.delete(file=self.file, content_type="tvshow")

    def delete_from_staged_and_block(self):
        """Remove the item from (staged) database with optional block."""
        self.delete_from_staged()
        self.database.block(value=self.title, content_type="tvshow")
