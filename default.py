#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main exectable module."""

import gc
import sys

from resources.lib.log import log_msg
from resources.lib.utils import entrypoint

from resources.lib.progressbar import ProgressBar
from resources.lib.database import Database

from resources.test.tests import run_tests
from resources.lib.menus.main import MainMenu


@entrypoint
def main():
    """Main entry point for addon."""
    if "test" in sys.argv:
        run_tests()
    else:
        MainMenu(
            database=Database(),
            progressbar=ProgressBar()
        ).view()

if __name__ == '__main__':
    main()
