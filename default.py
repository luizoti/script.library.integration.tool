#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Main exectable module."""

import sys

from resources.lib.log import log_msg
from resources.lib.utils import entrypoint

from resources.test.tests import run_tests
from resources.lib.menus.main import MainMenu


@entrypoint
def main():
    """Main entry point for addon."""
    if "test" in sys.argv:
        log_msg("Starting tests...")
        run_tests()
        return

    MainMenu().show()

if __name__ == '__main__':
    main()
