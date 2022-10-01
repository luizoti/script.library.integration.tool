# -*- coding: utf-8 -*-

"""Color enum module."""

from os.path import join

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.gui.colors import Colors


def notification(
    message,
    time=3000,
    icon=join(xbmcaddon.Addon().getAddonInfo("path"), "ntf_icon.png"),
):
    """Provide a shorthand for xbmc builtin notification with addon name."""
    xbmcgui.Dialog().notification(
        xbmcaddon.Addon().getAddonInfo("name"), str(message), icon, time, True
    )


def get_string(string_id) -> str:
    """Shortcut function to return string from String ID."""
    xbmc_string = xbmc.getLocalizedString(string_id).title()
    if xbmc_string:
        return xbmc_string
    return xbmcaddon.Addon().getLocalizedString(string_id)


def title_with_color(label, year=None, colorname=Colors.MEDIUMSLATEBLUE) -> str:
    """Create a string to use in title Dialog().select."""
    # TODO: this function can be better, maybe led generic,
    # now, this func add color and year to movie title,
    # and any of this actions can be split
    if year:
        return str(f"[COLOR {colorname}][B]{label} ({year})[/B][/COLOR]")
    return str(f"[COLOR {colorname}][B]{label}[/B][/COLOR]")


def colorize(string, colorname=Colors.MEDIUMSLATEBLUE) -> str:
    """Return string formatted with a selected color.

    Args:
        string (str): Any string.
        colorname (str, optional): Kodi colorname. Defaults to Colors.MEDIUMSLATEBLUE.

    Returns:
        str: Return a string formatted in a color tag.
    """
    return f"[COLOR {colorname}]{string}[/COLOR]"


def bold(string) -> str:
    """Return string formatted with bold.

    Args:
        string (str): Any string.

    Returns:
        str: formatted with bold tag.
    """
    return f"[B]{string}[/B]"
