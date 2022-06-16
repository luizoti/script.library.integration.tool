# -*- coding: utf-8 -*-
"""Custon xbmcgui.DialogProgress."""

import logging
import sys

import xbmc
import xbmcgui

# from resources.lib.misc import notification

LOG = logging.getLogger(__name__)


class ProgressBar(xbmcgui.DialogProgress):
    """Module to provide a Constom xbmcgui.DialogProgress."""

    def __init__(self) -> None:
        """ProgressBar __init__."""
        super(__class__, self).__init__()
        LOG.debug("""ProgressBar started.""")

    def __del__(self) -> None:
        LOG.debug("""ProgressBar closed.""")

    def create_progressdialog(self, head=None, msg=""):
        """Method to create ProgressBar window"""
        if not head:
            xbmc.log("Select() head argument cannot be None", xbmc.LOGDEBUG)
            return
        self.create(head, msg)

    def update_progressdialog(self, perc, msg):
        """Method to update ProgressBar window."""
        if self.iscanceled():
            self._iscanceled_close()
        self.update(int(100 * perc), msg)
        xbmc.sleep(200)

    def _iscanceled_close(self):
        """Close method to close progress by cancel button."""
        self.close()
        # notification("Desfazendo ultumas ações!", 3000)
        # Exec operations
        sys.exit()

    def close_progressdialog(self):
        """Close method to close progress by normal progress finish."""
        self.close()


class BGProgressBar(xbmcgui.DialogProgressBG):
    """Module to provide a Constom xbmcgui.DialogProgressBG."""

    def __init__(self):
        """BGProgressBar __init__."""
        super(__class__, self).__init__()
        LOG.debug("""BGProgressBar __init__.""")

    def create_progress_bar(self, head=None, msg=""):
        """Method to create BGProgressBar window"""
        if not head:
            xbmc.log("Select() head argument cannot be None", xbmc.LOGDEBUG)
            return
        self.create(head, msg)

    def update_progress_bar(self, perc, msg):
        """Method to update BGProgressBar window."""
        if self.isFinished():
            xbmc.sleep(100)
            self._isFinished_close()
        self.update(int(perc), msg)

    def _isfinished_close(self):
        """Close method to close progress by cancel button."""
        self.close()
        # notification("Background Desfazendo ultumas ações!", 3000)
        # Exec operations
        sys.exit()

    def close_progress_bar(self):
        """Close method to close progress by normal progress finish."""
        self.close()
