# -*- coding: utf-8 -*-

"""Main executable module."""

import logging
import sys
from os.path import basename

from resources.lib import logger
from resources.lib.menus.main import MainMenu
from resources.lib.test.tests import run_tests

LOG = logging.getLogger(basename(__file__))
logger.logging_setup()


# noinspection PyBroadException
def main():
    """Main entry point for addon."""
    if "test" in sys.argv:
        run_tests()
        return
    try:
        MainMenu().show()
    except:  # noqa: E261  # noqa: E261
        LOG.exception("Main menu error")


if __name__ == "__main__":
    main()
