# -*- coding: utf-8 -*-
"""Custom xbmcgui.DialogProgress."""

import logging
import sys

import xbmc
import xbmcgui

# from resources.lib.misc import notification

LOG = logging.getLogger(__name__)


class ProgressBar(xbmcgui.DialogProgress):
    """Module to provide a Custom xbmcgui.DialogProgress."""

    def __init__(self) -> None:
        """ProgressBar __init__."""
        super(__class__, self).__init__()
        LOG.debug("""ProgressBar started.""")

    def __del__(self) -> None:
        LOG.debug("""ProgressBar closed.""")

    def create_progress_dialog(self, head=None, msg=""):
        """Method to create ProgressBar window"""
        if not head:
            LOG.critical("Select() head argument cannot be None")
            return
        self.create(head, msg)

    def update_progress_dialog(self, percentage, message):
        """Method to update ProgressBar window."""
        self.update(int(100 * percentage), message)
        xbmc.sleep(200)

    def close_progress_dialog(self):
        """Close method to close progress by normal progress finish."""
        if self.iscanceled():
            self.close()
            return True
        return False


class ProgressBarBackground(xbmcgui.DialogProgressBG):
    """Module to provide a Custom xbmcgui.DialogProgressBG."""

    def __init__(self):
        """ProgressBarBackground __init__."""
        super(__class__, self).__init__()
        LOG.debug("""ProgressBarBackground __init__.""")

    def create_progress_bar(self, head=None, message=""):
        """Method to create ProgressBarBackground window"""
        if not head:
            LOG.critical("Select() head argument cannot be None")
            return
        self.create(head, message)

    def update_progress_bar(self, percentage, message):
        """Method to update ProgressBarBackground window."""
        if self.isFinished():
            xbmc.sleep(100)
            self.close_progress_bar()
        self.update(int(percentage), message)

    def close_progress_bar(self, _exit=None):
        """Close method to close progress by normal progress finish."""
        self.close()
        # notification("Background Desfazendo ultimas ações!", 3000)
        # Exec operations
        if _exit:
            sys.exit()
