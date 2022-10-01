# -*- coding: utf-8 -*-

"""Custom xbmcgui.Dialog.select."""

from typing import TypeVar

import xbmc
import xbmcaddon
import xbmcgui

type_var = TypeVar('type_var', None, tuple)


class Select(xbmcgui.Dialog):
    """Module to provide a Custom xbmcgui.Dialog.

    return:
        Key ESC/Backspace will return -> None
        Key Back will return          -> 'back'
        All other options, returns their representation in the dictionary are all.
    """

    def __init__(
            self,
            heading=None,
            turn_bold=False,
            back_option=32011,
    ) -> None:
        """CustomDialogSelect __init__."""
        super(__class__, self).__init__()
        if not heading:
            xbmc.log("Select() heading argument cannot be None", xbmc.LOGDEBUG)
            return
        self.back_option: int = back_option
        self.options_dict: dict = {}
        self.options_strings: list = []
        self.heading = self.bold(heading) if not turn_bold else heading

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
        return xbmcaddon.Addon().getLocalizedString(string_id)

    def _parse_options(self, options: dict, turn_bold=False):
        """Convert a dict key to string."""
        item_string: str = ""
        for key in options:
            item_string: str = key if isinstance(key, str) else self.get_string(key)
            if turn_bold:
                item_string = self.bold(item_string)
            self.options_strings.append(item_string)
        # return last value of options list, for back_option
        return {item_string: "back"}

    def options(self, options, turn_bold=True):
        """Add item lines to dialog select."""
        self.options_dict.update(options)
        self._parse_options(options=options, turn_bold=turn_bold)

    def extra_options(self, options):
        """Add option lines to dialog select."""
        self.options_dict.update(options)
        self._parse_options(options=options)

    def show(self, auto_close=False, use_details=False, pre_select=99999) -> type_var:
        """
        Open xbmcgui.Dialog with custom settings.

        pre_select: 99999, It seems to force the api to not choose any options.
        """
        # False returns "Programs" string
        # check if self.back_option key is not False
        if self.back_option:
            self.back_option = self._parse_options({self.back_option: "back"})
            self.options_dict.update(self.back_option)
        selected = self.select(
                heading=self.heading,
                list=self.options_strings,
                autoclose=auto_close,
                preselect=pre_select,
                useDetails=use_details,
        )
        # If ESC/Backspace or option Back...
        if selected == -1:
            return None
        for index, option in enumerate(self.options_dict.items()):
            if selected == index:
                return index, *option
        return None
