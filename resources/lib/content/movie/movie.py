# -*- coding: utf-8 -*-

import logging
from dataclasses import asdict, dataclass
from posixpath import basename

import xbmcvfs
from resources.lib import MANAGED_FOLDER
from resources.lib.content.content import Content
from resources.lib.filesystem import join, mkdir

LOG = logging.getLogger(basename(__file__))


@dataclass
class Movie(Content):
    """docstring for Movie"""

    @property
    def managed_movie_dir(self):
        """Create and return managed_movie_dir.

        Returns:
            str: managed_movie_dir id MANAGED_FOLDER/movies/movie (year).
        """
        return join([MANAGED_FOLDER, "movies", self.formed_title])

    @property
    def movie_nfo(self):
        """Create and return the path to movie.nfo file."""
        return f"{self.managed_movie_dir}/{self.formed_title}.nfo"

    @property
    def movie_strm(self):
        """Create and return the path to movie.strm file."""
        return f"{self.managed_movie_dir}/{self.formed_title}.strm"


