# -*- coding: utf-8 -*-

from dataclasses import InitVar, dataclass
from os import mkdir

from resources.lib.content.movie.movie import MovieFileCreator
from resources.lib.database.database import DBCommon


@dataclass
class StagedMovie(MovieFileManager):
    """Docstring for StagedMovie.

    Staged only create files, delete file methods is not necessary.
    """

    database: InitVar[DBCommon]

    def __post_init__(self, database):
        self.database = database

    def add_to_managed(self):
        """Create nfo, strm and add item to library (managed database)."""
        self.create_nfo()
        self.create_strm()
        self.database.update_item_status(
            file=self.file, _type="movie", status="managed"
        )

    def remove_and_block(self):
        """Remove item and block."""
        # Add title to blocked
        self.add_blocked_item(self.title(), "movie")
        # Delete metadata items
        removedir(self.managed_movie_dir())
        # Remove from db
        self.delete_item_from_table(file=self.file, _type="movie")

    def remove_from_library(self):
        """Remove from library."""
        removedirs(self.managed_movie_dir())

    # # don't touch here
    # def rename(self, name):
    #     """Rename item."""
    #     # TODO: Implement
    #     raise NotImplementedError("contentitem.rename(name) not implemented!")

    # def rename_using_metadata(self):
    #     """Rename item using metadata."""
    #     # TODO: Implement
    #     raise NotImplementedError("contentitem.rename(name) not implemented!")
    # # don't touch here

    def delete(self):
        """Remove the item from the database."""
        self.delete_item_from_table(file=self.file, _type="movie")

    def set_as_staged(self):
        """Set the item status as staged in database."""
        self.update_item_status(file=self.file, _type="movie", status="staged")
