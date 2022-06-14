#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main exectable module."""

import logging
import sys
from os.path import basename

from resources.lib import logger
from resources.lib.menus.main import MainMenu
from resources.test.tests import run_tests

LOG = logging.getLogger(basename(__file__))
logger.logging_setup()


def main():
    """Main entry point for addon."""
    if "test" in sys.argv:
        run_tests()
        return
    try:
        MainMenu().show()
    except Exception:  # pylint: disable=broad-except
        LOG.exception("Main menu error")


if __name__ == "__main__":
    main()
