# -*- coding: utf-8 -*-

"""
The Movie module brings together classes that separately
control everything needed to manage movies.
"""

import logging
from dataclasses import asdict, dataclass
from os.path import basename

import xbmcvfs
from resources.lib import MANAGED_FOLDER
from resources.lib.content.content import Content
from resources.lib.filesystem import join, mk_dir, remove_dir

LOG = logging.getLogger(basename(__file__))


@dataclass
class Movie(Content):
    """docstring for Movie"""

    @property
    def managed_movie_diretory(self):
        """Create and return managed_movie_diretory.

        Returns:
            str: managed_movie_diretory id MANAGED_FOLDER/movies/movie (year).
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
    """
    Create files related with content item Movie.
    https://kodi.wiki/view/NFO_files/Creating
    https://kodi.wiki/view/NFO_files/Templates
    """

    _current_nfo_string: str = None
    _unicode_heading: str = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

    def build_movie_nfo_string(self):
        """Method to format the .nfo body with the required attributes."""
        self._current_nfo_string = "\n".join(
            [
                self._unicode_heading,
                "<movie>",
                f"\t<title>{self.title}</title>",
                f"\t<year>{self.year}</year>",
                f"\t<original_filename>{self.file}</original_filename>",
                "</movie>\n",
            ]
        )

    def create_nfo(self) -> bool:
        """Create stream file with self.file at self.movie_strm filepath."""
        mk_dir(self.managed_movie_diretory)
        with xbmcvfs.File(self.movie_nfo, "w+") as nfo_file:
            try:
                if self._current_nfo_string:
                    nfo_file.write(self._current_nfo_string)
                    LOG.info("Created NFO file %s", self.movie_nfo)
                    return True
            except Exception:
                LOG.exception("CreateNfo.create:")
            finally:
                self._current_nfo_string = ""
                nfo_file.close()
        return None

    def create_strm(self):
        """Create stream file with self.file at self.movie_strm filepath."""
        self.create_managed_movie_diretory()
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

    def create_managed_movie_diretory(self) -> bool:
        """Create the managed_movie_diretory for content."""
        return mk_dir(self.managed_movie_diretory)

    def delete_managed_movie_diretory(self) -> bool:
        """Delete movie nfo file."""
        return remove_dir(self.managed_movie_diretory)

    def delete_nfo(self) -> bool:
        """Delete movie nfo file."""
        return xbmcvfs.delete(self.movie_nfo)

    def delete_strm(self) -> bool:
        """Delete movie strm file."""
        return xbmcvfs.delete(self.movie_strm)

    @property
    def asdict(self) -> dict:
        """Return a dict from dataclass.
        Returns:
            dict: dict with dataclass properties.
        """
        return asdict(self)
