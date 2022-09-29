# # -*- coding: utf-8 -*-

"""A service entrypoint."""

import logging
import sys
import time
from os.path import basename

import xbmc

from resources.lib import logger
from resources.lib.gui.gui_utils import notification
from resources.lib.menus.main import MainMenu
from resources.lib.test.tests import run_tests

LOG = logging.getLogger(basename(__file__))


class LitWatcher(xbmc.Monitor):
    """Service class."""

    # https://github.com/romanvm/kodi.web-pdb
    # https://forum.kodi.tv/showthread.php?tid=248758
    def __init__(self) -> None:
        super().__init__()
        while not self.abortRequested():
            # Sleep/wait for abort for 20 seconds
            if self.waitForAbort(20):
                # Abort was requested while waiting. We should exit
                break
            notification("hello addon! xxxx")


if __name__ == "__main__":
    LitWatcher()
