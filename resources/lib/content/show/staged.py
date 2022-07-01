# -*- coding: utf-8 -*-

"""StagedEpisode docstring."""

from dataclasses import InitVar, dataclass

from resources.lib.content.show.show import EpisodeFileManager
from resources.lib.database.database import DBCommon


@dataclass
class StagedEpisode(EpisodeFileManager):
    """Docstring for StagedEpisode.

    Staged only create files, delete file methods is not necessary.
    """

    database: InitVar[DBCommon] = None

    def __post_init__(self, database: DBCommon):
        self.database = database

    def move_to_managed(self):
        """Create nfo, strm and add item to library (managed database)."""
        self.build_tvshow_nfo_string()
        self.create_nfo()
        self.build_episode_nfo_string()
        self.create_nfo()
        self.create_strm()
        self.database.update_status(file=self.file, _type="tvshow", status="managed")

    def delete_from_staged(self):
        """Remove the item from (staged) database with optional block."""
        self.database.delete(file=self.file, _type="tvshow")

    def delete_from_staged_and_block(self):
        """Remove the item from (staged) database with optional block."""
        self.delete_from_staged()
        self.database.block(value=self.title, _type="tvshow")
