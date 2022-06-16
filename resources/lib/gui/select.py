# -*- coding: utf-8 -*-

"""Custon xbmcgui.Dialog.select."""

import xbmc
import xbmcaddon
import xbmcgui


class Select(xbmcgui.Dialog):
    """Module to provide a Constom xbmcgui.Dialog.

    return:
        Key ESC/Backspace will return -> None
        Key Back will return          -> 'back'
        All other options, returns their representation in the dictionary are all.
    """

    def __init__(
        self,
        heading=None,
        turnbold=False,
        back_option=32011,
    ) -> None:
        """CustonDialogSelect __init__."""
        super(__class__, self).__init__()
        if not heading:
            xbmc.log("Select() heading argument cannot be None", xbmc.LOGDEBUG)
            return
        self.back_option: int = back_option
        self.options_dict: dict = {}
        self.options_strings: list = []
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
        return xbmcaddon.Addon().getLocalizedString(string_id)

    def _parse_options(self, options: dict, turnbold=False):
        """Convert a dict key to string."""
        item_string: str
        for key in options:
            item_string = key if isinstance(key, str) else self.get_string(key)
            if turnbold:
                item_string = self.bold(item_string)
            self.options_strings.append(item_string)
        # return last value of options list, for back_option
        return {item_string: "back"}

    def options(self, options, turnbold=True):
        """Add item lines to dialog select."""
        self.options_dict.update(options)
        self._parse_options(options=options, turnbold=turnbold)

    def extra_options(self, options):
        """Add option lines to dialog select."""
        self.options_dict.update(options)
        self._parse_options(options=options)

    def show(self, autoclose=False, useDetails=False, preselect=99999) -> tuple:
        """
        Open xbmcgui.Dialog with custom settings.

        preselect: 99999, It seems to force the api to not choose any options.
        """
        # False returns "Programs" string
        # check if self.back_option key is not False
        if self.back_option:
            self.back_option = self._parse_options({self.back_option: "back"})
            self.options_dict.update(self.back_option)
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
