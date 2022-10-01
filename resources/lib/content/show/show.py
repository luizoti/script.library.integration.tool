# -*- coding: utf-8 -*-

"""
The Show module brings together classes that separately
control everything needed to manage show/episodes.
"""

import logging
from dataclasses import InitVar, asdict, dataclass
from os.path import basename
from typing import TypeVar

import xbmcvfs

from resources.lib import MANAGED_FOLDER
from resources.lib.content.content import Content
from resources.lib.database.database import DBCommon
from resources.lib.filesystem import join, mk_dir, remove_dir

LOG = logging.getLogger(basename(__file__))

type_var = TypeVar("type_var", None, bool)


# TODO: use cleaner
# showtitle: str = None
# season: int = None
# episode: int = None

# def __post_init__(self):
# self.cleaner = Cleaner()

# noinspection PyBroadException

@dataclass
class Episode(Content):
    """
    The plan is to treat each episode like a movie, just like resources.lib.content.movie.movie.
    """

    showtitle: str
    season: int
    episode: int
    episode_title: str = None
    database: InitVar[DBCommon] = None

    def __post_init__(self, database: DBCommon):
        # Originally it would not be necessary to provide a database here,
        # but the _post __init__ ends up forcing its presence without
        # it is would not be possible to correct the self.episode_title and self.title
        self.database = database
        if self.type == "tvshow":
            self.episode_title = self.title
            self.title = self.showtitle

    @property
    def formed_episode_id(self):
        """Create and return episode_id.

        Returns:
            str: episode_id is S0XE0Y (X is self.season and Y is self.episode).
        """
        return f"S0{self.season}E0{self.episode}"

    @property
    def formed_episode_title(self):
        """Create and return formed_episode_title.

        Returns:
            str: formed_episode_title is showtitle - formed_episode_id - episode_title

            showtitle   is self.formed_title
            spisodeid   is self.formed_episode_id
            episodename is self.episode_title

            .
        """
        return f"{self.formed_title} - {self.formed_episode_id} - {self.episode_title}"

    @property
    def formed_season(self):
        """Create and return formed_season.

        Returns:
            str: formed_season is Season X (X is self.season).
        """
        return f"Season {self.season}"

    @property
    def managed_show_diretory(self):
        """Create and return managed_episode_diretory.

        Returns:
            str: managed_episode_diretory is MANAGED_FOLDER/tvshows/show (year).
        """
        return join(MANAGED_FOLDER, "tvshows", self.formed_title)

    @property
    def managed_season_diretory(self):
        """Create and return managed_season_diretory.

        Returns:
            str: managed_episode_diretory is MANAGED_FOLDER/tvshows/show (year)/season x.
        """
        return join(self.managed_show_diretory, self.formed_season)

    @property
    def tvshow_nfo(self):
        """Create and return the path to tvshow.nfo."""
        return f"{self.managed_show_diretory}/tvshow.nfo"

    @property
    def episode_nfo(self):
        """Create and return the path to episode.nfo."""
        return f"{self.managed_season_diretory}/{self.formed_episode_title}.nfo"

    @property
    def episode_strm(self):
        """Create and return the path to episode.strm."""
        return f"{self.managed_season_diretory}/{self.formed_episode_title}.strm"


@dataclass
class EpisodeFileManager(Episode):
    """
    Create files related with content item Episode.
    https://kodi.wiki/view/NFO_files/Creating
    https://kodi.wiki/view/NFO_files/Templates
    """

    _current_nfo_diretory: str = None
    _current_nfo_path: str = None
    _current_nfo_string: str = None

    _unicode_heading: str = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

    def build_tvshow_nfo_string(self):
        """Method to format the .nfo body with the required attributes."""
        self._current_nfo_diretory: str = self.managed_show_diretory
        self._current_nfo_path: str = self.tvshow_nfo

        self._current_nfo_string = "\n".join(
                [
                    self._unicode_heading,
                    "<tvshow>",
                    f"\t<title>{self.showtitle}</title>\n",
                    f"\t<showtitle>{self.showtitle}</showtitle>\n",
                    f"\t<year>{self.year}</year>\n",
                    "</tvshow>\n",
                ]
        )

    def build_episode_nfo_string(self):
        """Method to format the .nfo body with the required attributes."""
        self._current_nfo_diretory: str = self.managed_season_diretory
        self._current_nfo_path: str = self.episode_nfo

        self._current_nfo_string = "\n".join(
                [
                    self._unicode_heading,
                    "<episodedetails>",
                    f"\t<title>{self.title}</title>\n",
                    f"\t<showtitle>{self.showtitle}</showtitle>\n",
                    f"\t<season>{self.season}</season>\n",
                    f"\t<episode>{self.episode}</episode_number>\n",
                    f"\t<year>{self.year}</year>\n",
                    f"\t<original_filename>{self.file}</original_filename>\n",
                    "</episodedetails>\n",
                ]
        )

    def create_nfo(self) -> type_var:
        """Create stream file with self.file at nfo filepath."""
        mk_dir(self._current_nfo_diretory)
        with xbmcvfs.File(self._current_nfo_path, "w+") as nfo_file:
            try:
                if self._current_nfo_string:
                    nfo_file.write(self._current_nfo_string)
                    LOG.info("Created NFO file %s", self._current_nfo_path)
                    return True
            except:  # noqa: E261
                LOG.exception("CreateNfo.create:")
            finally:
                self._current_nfo_string = ""
                self._current_nfo_diretory = ""
                self._current_nfo_path = ""
                nfo_file.close()
        return None

    def create_strm(self):
        """Create stream file with self.file at self.episode_nfo filepath."""
        self.create_managed_season_diretory()
        with xbmcvfs.File(self.episode_strm, "w+") as strm:
            try:
                strm.write(self.file)
                LOG.debug("Created STRM file %s", self.episode_strm)
                return True
            except:  # noqa: E261
                LOG.exception("filesystem.create_stream_file:")
            finally:
                strm.close()
        return None

    def create_managed_show_diretory(self) -> bool:
        """Create the managed_movie_diretory for content."""
        return mk_dir(self.managed_show_diretory)

    def delete_managed_show_diretory(self) -> bool:
        """Delete managed_show_diretory nfo file."""
        return remove_dir(self.managed_show_diretory)

    def create_managed_season_diretory(self) -> bool:
        """Create the managed_season_diretory for content."""
        return mk_dir(self.managed_season_diretory)

    def delete_managed_season_diretory(self) -> bool:
        """Delete managed_season_diretory nfo file."""
        return remove_dir(self.managed_season_diretory)

    def delete_tvshow_nfo(self) -> bool:
        """Delete tvshow nfo file."""
        return xbmcvfs.delete(self.tvshow_nfo)

    def delete_episode_nfo(self) -> bool:
        """Delete episode nfo file."""
        return xbmcvfs.delete(self.episode_nfo)

    def delete_strm(self) -> bool:
        """Delete episode strm file."""
        return xbmcvfs.delete(self.episode_strm)

    @property
    def asdict(self) -> dict:
        """Return a dict from dataclass.
        Returns:
            dict: dict with dataclass properties.
        """
        return asdict(self)
