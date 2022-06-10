# -*- coding: utf-8 -*-

"""Custon xbmcgui.Dialog.select."""

import xbmc
import xbmcgui
from resources import ADDON, ADDON_NAME


class Select(xbmcgui.Dialog):
    """Module to provide a Constom xbmcgui.Dialog.

    return:
        Key ESC/Backspace will return -> None
        Key Back will return          -> 'back'
        All other options, returns their representation in the dictionary are all.
    """

    def __init__(
        self,
        heading=ADDON_NAME,
        turnbold=False,
        back_option=32011,
    ) -> None:
        """CustonDialogSelect __init__."""
        super(__class__, self).__init__()
        self.options_dict: dict = {}
        self.options_strings: list = []
        self.back_option = {back_option: "back"}
        self.heading = self.bold(heading) if not turnbold else heading

    @staticmethod
    def bold(normal_string):
        """Return a bold string."""
        return f"[B]{normal_string}[/B]"

    @staticmethod
    def get_string(string_id):
        """Shortcut function to return string from String ID."""
        xbmc_string = xbmc.getLocalizedString(string_id).title()
        if xbmc_string:
            return xbmc_string
        return ADDON.getLocalizedString(string_id)

    def _parse_options(self, options: dict, turnbold=False):
        """Convert a dict key to string."""
        for key in options:
            item_string = key if isinstance(key, str) else self.get_string(key)
            if turnbold:
                item_string = self.bold(item_string)
            self.options_strings.append(item_string)

    def options(self, options, turnbold=True):
        """Add item lines to dialog select."""
        self.options_dict.update(options)
        self._parse_options(options=options, turnbold=turnbold)

    def extra_options(self, options):
        """Add option lines to dialog select."""
        self.options_dict.update(options)
        self._parse_options(options=options)

    def show(self, autoclose=False, useDetails=False, preselect=False) -> tuple:
        """Open dialog select with all params."""
        # False returns "Programs" string
        # check if self.back_option key is not False
        if False not in self.back_option:
            self.options_dict.update(self.back_option)
            self._parse_options(self.back_option)
        selected = self.select(
            heading=self.heading,
            list=self.options_strings,
            autoclose=autoclose,
            preselect=preselect,
            useDetails=useDetails,
        )
        # If ESC/Backspace or option Back...
        if selected == -1:
            return None
        for index, option in enumerate(self.options_dict.items()):
            if selected == index:
                return index, *option
        return None
