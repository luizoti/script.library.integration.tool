# -*- coding: utf-8 -*-

"""Collection of log functions."""

import logging

import xbmc
from resources.lib import ADDON_NAME, ADDON_VERSION


class KodiLogHandler(logging.StreamHandler):
    """
    Log Handler class.
    """

    # https://github.com/xbmc/generator-kodi-addon/blob/master/generators/app/templates/resources/lib/kodilogging.py

    def __init__(self):
        logging.StreamHandler.__init__(self)
        name = "%(name)s"
        message = "%(message)s"
        formatter = logging.Formatter(f"[{ADDON_NAME}][{name}] -> {message}")
        self.setFormatter(formatter)

    def emit(self, record):
        xbmc.log(self.format(record), xbmc.LOGDEBUG)
        levels = {
            logging.CRITICAL: xbmc.LOGFATAL,
            logging.ERROR: xbmc.LOGERROR,
            logging.WARNING: xbmc.LOGWARNING,
            logging.INFO: xbmc.LOGINFO,
            logging.DEBUG: xbmc.LOGDEBUG,
            logging.NOTSET: xbmc.LOGNONE,
        }
        try:
            xbmc.log(self.format(record), levels[record.levelno])
        except UnicodeEncodeError:
            xbmc.log(
                self.format(record).encode("utf-8", "ignore"),
                levels[record.levelno],
            )

    def flush(self):
        pass


def logging_setup():
    """Initialize and setup the log handler."""
    logger = logging.getLogger()
    logger.addHandler(KodiLogHandler())
    logger.setLevel(logging.DEBUG)
    logger.info("v%s", ADDON_VERSION)
