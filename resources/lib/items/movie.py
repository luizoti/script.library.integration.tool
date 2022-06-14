# -*- coding: utf-8 -*-
# pylint: disable=broad-except

"""Defines the MovieItem class."""

import logging
from os.path import basename, join

from resources.lib.manipulator import Cleaner
from resources.lib.utils import MANAGED_FOLDER

LOG = logging.getLogger(basename(__file__))


class MovieItem:
    """Class to build information aboult movies."""

    def __init__(self, jsonitem, year=None):
        """__init__ MovieItem."""
        super(__class__, self).__init__()
        self.cleaner = Cleaner()
        self.jsonitem = jsonitem
        self.arg_year = year

    def file(self):
        """Return url from strm."""
        return self.jsonitem["file"]

    def title(self):
        """Return the title from content."""
        return self.cleaner.title(title=self.jsonitem["title"])

    def year(self):
        """Return the year from content."""
        return self.arg_year if self.arg_year else self.jsonitem["year"]

    def managed_movie_dir(self):
        """Return the managed_movie_dir from content."""
        return join(MANAGED_FOLDER, "movies", self.title())

    def returasjson(self):
        """Return the json with information from content."""
        try:
            return {
                "file": self.file(),
                "title": self.title(),
                "managed_movie_dir": self.managed_movie_dir(),
                "year": self.year(),
                "type": "movie",
            }
        except Exception:
            LOG.exception("MovieItem.returasjson error")
        return None
