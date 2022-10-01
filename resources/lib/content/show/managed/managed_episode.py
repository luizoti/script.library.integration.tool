# -*- coding: utf-8 -*-

"""ManagedEpisode docstring."""

from dataclasses import InitVar, dataclass

from resources.lib.content.show.show import EpisodeFileManager
from resources.lib.database.database import DBCommon


@dataclass
class ManagedEpisode(EpisodeFileManager):
    """Docstring for ManagedEpisode.

    Managed create and delete files.
    """

    database: InitVar[DBCommon] = None

    def __post_init__(self, database: DBCommon):
        self.database = database

    def move_to_staged(self):
        """Remove item from managed (library), move to staged and delete all files if existed."""
        self.delete_managed_show_diretory()
        self.database.update_status(file=self.file, content_type="tvshow", status="staged")

    def remove_completely(self):
        """Complete remove item from database and all files if existed."""
        self.delete_managed_show_diretory()
        self.database.delete(file=self.file, content_type="tvshow")

    def remove_completely_and_block(self):
        """Similar to remove_completely, but block item."""
        self.remove_completely()
        self.database.block(value=self.title, content_type="tvshow")
