
# This strings will be used to ignore itens in show diretectories

import re
import json

from os.path import join
from os.path import expanduser

import xbmc
import xbmcgui

from resources import ADDON
from resources import ADDON_NAME
from resources import ADDON_PATH


SKIP_STRINGS = [
    "resumo",
    "suggested",
    "extras",
    # 'trailer',
    r"\#(?:\d{1,5}\.\d{1,5}|SP)",
]


class Colors(Enum):
    """
    Enum representation of Kodi Colors.
    COLORS: https://github.com/xbmc/xbmc/blob/master/system/colors.xml
    """

    ALICEBLUE = "fff0f8ff"
    ANTIQUEWHITE = "fffaebd7"
    AQUA = "ff00ffff"
    AQUAMARINE = "ff7fffd4"
    AZURE = "fff0ffff"
    BEIGE = "fff5f5dc"
    BISQUE = "ffffe4c4"
    BLACK = "ff000000"
    BLANCHEDALMOND = "ffffebcd"
    BLUE = "ff0000ff"
    BLUEVIOLET = "ff8a2be2"
    BROWN = "ffa52a2a"
    BURLYWOOD = "ffdeb887"
    CADETBLUE = "ff5f9ea0"
    CHARTREUSE = "ff7fff00"
    CHOCOLATE = "ffd2691e"
    CORAL = "ffff7f50"
    CORNFLOWERBLUE = "ff6495ed"
    CORNSILK = "fffff8dc"
    CRIMSON = "ffdc143c"
    CYAN = "ff00ffff"
    DARKBLUE = "ff00008b"
    DARKCYAN = "ff008b8b"
    DARKGOLDENROD = "ffb8860b"
    DARKGRAY = "ffa9a9a9"
    DARKGREEN = "ff006400"
    DARKGREY = "ffa9a9a9"
    DARKKHAKI = "ffbdb76b"
    DARKMAGENTA = "ff8b008b"
    DARKOLIVEGREEN = "ff556b2f"
    DARKORANGE = "ffff8c00"
    DARKORCHID = "ff9932cc"
    DARKRED = "ff8b0000"
    DARKSALMON = "ffe9967a"
    DARKSEAGREEN = "ff8fbc8f"
    DARKSLATEBLUE = "ff483d8b"
    DARKSLATEGRAY = "ff2f4f4f"
    DARKSLATEGREY = "ff2f4f4f"
    DARKTURQUOISE = "ff00ced1"
    DARKVIOLET = "ff9400d3"
    DEEPPINK = "ffff1493"
    DEEPSKYBLUE = "ff00bfff"
    DIMGRAY = "ff696969"
    DIMGREY = "ff696969"
    DODGERBLUE = "ff1e90ff"
    FIREBRICK = "ffb22222"
    FLORALWHITE = "fffffaf0"
    FORESTGREEN = "ff228b22"
    FUCHSIA = "ffff00ff"
    GAINSBORO = "ffdcdcdc"
    GHOSTWHITE = "fff8f8ff"
    GOLD = "ffffd700"
    GOLDENROD = "ffdaa520"
    GRAY = "ff808080"
    GREEN = "ff008000"
    GREENYELLOW = "ffadff2f"
    GREY = "ff808080"
    HONEYDEW = "fff0fff0"
    HOTPINK = "ffff69b4"
    INDIANRED = "ffcd5c5c"
    INDIGO = "ff4b0082"
    IVORY = "fffffff0"
    KHAKI = "fff0e68c"
    LAVENDER = "ffe6e6fa"
    LAVENDERBLUSH = "fffff0f5"
    LAWNGREEN = "ff7cfc00"
    LEMONCHIFFON = "fffffacd"
    LIGHTBLUE = "ffadd8e6"
    LIGHTCORAL = "fff08080"
    LIGHTCYAN = "ffe0ffff"
    LIGHTGOLDENRODYELLOW = "fffafad2"
    LIGHTGRAY = "ffd3d3d3"
    LIGHTGREEN = "ff90ee90"
    LIGHTGREY = "ffd3d3d3"
    LIGHTPINK = "ffffb6c1"
    LIGHTSALMON = "ffffa07a"
    LIGHTSEAGREEN = "ff20b2aa"
    LIGHTSKYBLUE = "ff87cefa"
    LIGHTSLATEGRAY = "ff778899"
    LIGHTSLATEGREY = "ff778899"
    LIGHTSTEELBLUE = "ffb0c4de"
    LIGHTYELLOW = "ffffffe0"
    LIME = "ff00ff00"
    LIMEGREEN = "ff32cd32"
    LINEN = "fffaf0e6"
    MAGENTA = "ffff00ff"
    MAROON = "ff800000"
    MEDIUMAQUAMARINE = "ff66cdaa"
    MEDIUMBLUE = "ff0000cd"
    MEDIUMORCHID = "ffba55d3"
    MEDIUMPURPLE = "ff9370db"
    MEDIUMSEAGREEN = "ff3cb371"
    MEDIUMSLATEBLUE = "ff7b68ee"
    MEDIUMSPRINGGREEN = "ff00fa9a"
    MEDIUMTURQUOISE = "ff48d1cc"
    MEDIUMVIOLETRED = "ffc71585"
    MIDNIGHTBLUE = "ff191970"
    MINTCREAM = "fff5fffa"
    MISTYROSE = "ffffe4e1"
    MOCCASIN = "ffffe4b5"
    NAVAJOWHITE = "ffffdead"
    NAVY = "ff000080"
    NONE = "00000000"
    OLDLACE = "fffdf5e6"
    OLIVE = "ff808000"
    OLIVEDRAB = "ff6b8e23"
    ORANGE = "ffffa500"
    ORANGERED = "ffff4500"
    ORCHID = "ffda70d6"
    PALEGOLDENROD = "ffeee8aa"
    PALEGREEN = "ff98fb98"
    PALETURQUOISE = "ffafeeee"
    PALEVIOLETRED = "ffdb7093"
    PAPAYAWHIP = "ffffefd5"
    PEACHPUFF = "ffffdab9"
    PERU = "ffcd853f"
    PINK = "ffffc0cb"
    PLUM = "ffdda0dd"
    POWDERBLUE = "ffb0e0e6"
    PURPLE = "ff800080"
    RED = "ffff0000"
    ROSYBROWN = "ffbc8f8f"
    ROYALBLUE = "ff4169e1"
    SADDLEBROWN = "ff8b4513"
    SALMON = "fffa8072"
    SANDYBROWN = "fff4a460"
    SEAGREEN = "ff2e8b57"
    SEASHELL = "fffff5ee"
    SIENNA = "ffa0522d"
    SILVER = "ffc0c0c0"
    SKYBLUE = "ff87ceeb"
    SLATEBLUE = "ff6a5acd"
    SLATEGRAY = "ff708090"
    SLATEGREY = "ff708090"
    SNOW = "fffffafa"
    SPRINGGREEN = "ff00ff7f"
    STEELBLUE = "ff4682b4"
    TAN = "ffd2b48c"
    TEAL = "ff008080"
    THISTLE = "ffd8bfd8"
    TOMATO = "ffff6347"
    TRANSPARENT = "00000000"
    TURQUOISE = "ff40e0d0"
    VIOLET = "ffee82ee"
    WHEAT = "fff5deb3"
    WHITE = "ffffffff"
    WHITESMOKE = "fff5f5f5"
    YELLOW = "ffffff00"
    YELLOWGREEN = "ff9acd32"


def re_search(string, tosearch=None):
    """Function check if string exist with re."""
    tosearch = tosearch if isinstance(tosearch, list) else [tosearch]
    return bool(any(re.search(rgx, string, re.I) for rgx in tosearch))


def skip_filter(contents_json, _key, toskip):
    """Function to iterate jsons in a list and filter by key with re."""
    try:
        for item in contents_json:
            if not bool(any(re.search(rgx, item[_key], re.I) for rgx in toskip)):
                yield item
    except TypeError:
        yield None


def is_season(string):
    """Function to check if item is a season."""
    return bool(re_search(string, ["season", "temporada", r"S\d{1,4}"]))


def notification(message, time=3000, icon=join(ADDON_PATH, "ntf_icon.png")):
    """Provide a shorthand for xbmc builtin notification with addon name."""
    xbmcgui.Dialog().notification(ADDON_NAME, str(message), icon, time, True)


def savetojson(data):
    """Function to create a json file."""
    try:
        filename = join(expanduser("~/"), "json_result.json")
        with open(filename, "a+", encoding="utf8") as jsonoutput:
            jsonoutput.write(str(json.dumps(data, indent=4, sort_keys=True)))
            jsonoutput.close()
    except AttributeError:
        pass


def get_string(string_id):
    """Shortcut function to return string from String ID."""
    xbmc_string = xbmc.getLocalizedString(string_id).title()
    if xbmc_string:
        return xbmc_string
    return ADDON.getLocalizedString(string_id)


def title_with_color(label, year=None, colorname='mediumslateblue'):
    """Create a string to use in title Dialog().select."""
    # COLORS: https://github.com/xbmc/xbmc/blob/master/system/colors.xml
    # TODO: this function can be better, maybe led generic,
    # now, this func add color and year to movie title,
    # and any of this actions can be splited
    if year:
        return str(f"[COLOR {colorname}][B]{label} ({year})[/B][/COLOR]")
    return str(f"[COLOR {colorname}][B]{label}[/B][/COLOR]")


def color(string, colorname='mediumslateblue'):
    """
    Return string formated with a selected color.
    lawngreen
    mediumseagreen
    """
    return str(f"[COLOR {colorname}]{string}[/COLOR]")


def bold(string):
    """
    Return string formated with a bold.
    """
    return str(f"[B]{string}[/B]")


# in future path arg will select the clean method
def videolibrary(method, database="video"):
    """A dedicated method to performe jsonrpc VideoLibrary.Scan or VideoLibrary."""
    command = {
        "scan": f"CleanLibrary({database})",
        "clean": f"UpdateLibrary({database})",
    }
    xbmc.executebuiltin(command[method])
