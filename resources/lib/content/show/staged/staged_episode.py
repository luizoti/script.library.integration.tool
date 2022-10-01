# -*- coding: utf-8 -*-

"""StagedEpisode docstring."""

from dataclasses import InitVar, dataclass

from resources.lib.content.show.show import EpisodeFileManager
from resources.lib.database.show.db_show import DBShows
from resources.lib.gui.colors import Colors
from resources.lib.gui.gui_utils import bold, colorize


@dataclass
class StagedEpisode(EpisodeFileManager):
    """
    Staged only create files, delete file methods is not necessary.
    """

    database: InitVar[DBShows] = None

    def __str__(self):
        # TODO: for now I will keep these cores, then
        # but I'll think about whether to keep it that way or not.
        title = bold(colorize(self.showtitle, Colors.BLUE))
        year = bold(colorize(self.formed_year, Colors.RED))
        return f"{title} {year}\n {self.formed_episode_id} - {self.episode_title}"

    def move_to_managed(self):
        """Create nfo, strm and add item to library (managed database)."""
        self.build_tvshow_nfo_string()
        self.create_nfo()
        self.build_episode_nfo_string()
        self.create_nfo()
        self.create_strm()
        self.database.update_status(file=self.file, content_type="tvshow", status="managed")

    def delete_from_staged(self):
        """Remove the item from (staged) database with optional block."""
        self.database.delete(file=self.file, content_type="tvshow")

    def delete_from_staged_and_block(self):
        """Remove the item from (staged) database with optional block."""
        self.delete_from_staged()
        self.database.block(value=self.title, content_type="tvshow")
