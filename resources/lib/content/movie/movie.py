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
    def managed_movie_diretory(self):
        """Create and return managed_movie_dir.

        Returns:
            str: managed_movie_dir id MANAGED_FOLDER/movies/movie (year).
        """
        return join(MANAGED_FOLDER, "movies", self.formed_title)

    @property
    def movie_nfo(self):
        """Create and return the path to movie.nfo file."""
        return f"{self.managed_movie_diretory}/{self.formed_title}.nfo"

    @property
    def movie_strm(self):
        """Create and return the path to movie.strm file."""
        return f"{self.managed_movie_diretory}/{self.formed_title}.strm"


@dataclass
class MovieFileManager(Movie):
    """Create files related with content item Movie."""

    def nfo_body_string(self) -> str:
        """Return str title formated with file path."""
        nfo_info_body = "".join(
            [
                f"\t<title>{self.title}</title>\n",
                f"\t<year>{self.year}</year>\n",
                f"\t<original_filename>{self.file}</original_filename>\n",
            ]
        )
        return f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<movie>\n{nfo_info_body}</movie>'

    @property
    def asdict(self) -> dict:
        """Return a dict from dataclass.
        Returns:
            dict: dict with dataclass properties.
        """
        return asdict(self)

    def create_nfo(self) -> bool:
        """Create stream file with self.file at self.movie_strm filepath."""
        mkdir(self.managed_movie_diretory)
        with xbmcvfs.File(self.movie_nfo, "w+") as nfofile:
            try:
                nfofile.write(self.nfo_body_string())
                LOG.info("Created NFO file %s", self.movie_nfo)
                # TODO: What was the reason for updating the title? Do not remember.
                # self.update_item_title(file=self.file, _type="movie", title=self.title)
                return True
            except Exception:
                LOG.exception("CreateNfo.create:")
            finally:
                nfofile.close()
        return None

    def create_strm(self):
        """Create stream file with self.file at self.movie_strm filepath."""
        mkdir(self.managed_movie_dir)
        with xbmcvfs.File(self.movie_strm, "w+") as strm:
            try:
                strm.write(self.file)
                LOG.debug("Created STRM file %s", self.movie_strm)
                return True
            except Exception:
                LOG.exception("filesystem.create_stream_file:")
            finally:
                strm.close()
        return None
