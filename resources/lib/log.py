#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Collection of log functions."""

import xbmc

from resources import ADDON_NAME
from resources import ADDON_VERSION
from resources import IN_DEVELOPMENT
from resources import DEFAULT_LOG_LEVEL


def log_msg(msg, loglevel=DEFAULT_LOG_LEVEL):
    """Log message with addon name and version to kodi log."""
    xbmc.log("{0} v{1} --> {2}".format(ADDON_NAME,
    xbmc.log(f"{ADDON_NAME} v{ADDON_VERSION} --> {msg}", level=loglevel)


def logged_function(func):
    """Decorator for logging function call and return values (at default log level)."""
    # TODO: option to have "pre-" and "post-" logging
    def wrapper(*args, **kwargs):
        """function wrapper."""
        # Call the function and get the return value
        ret = func(*args, **kwargs)
        # Only log if IN_DEVELOPMENT is set
        if IN_DEVELOPMENT:
            # Define the string for the function call (include class name for methods)
            is_method = args and hasattr(args[0].__class__, func.__name__)
            parent = args[0].__class__.__name__ if is_method else func.__module__.replace(
                'resources.lib.', ''
            )
            # Pretty formating for argument string
            arg_list = []
            for arg in args[1 if is_method else 0:]:
                arg_list.append(f"'{arg}'")
            for key, val in kwargs.items():
                arg_list.append(f'{key}={0}'.format(f"'{val}'"))
            arg_str = f"({', '.join(arg_list)})"
            # Add line breaks and limit output if ret value is iterable
            if isinstance(ret, str):
                ret_str = f"'{ret}'"
            else:
                try:
                    ret_list = ['\n' + str(x) for x in ret[:5]]
                    if len(ret) > 5:
                        ret_list += [f"\n+{len(ret) - 5} more items..."]
                    ret_str = "".join(ret_list)
                except TypeError:
                    ret_str = str(ret)
            # Log message at default loglevel
            log_msg(f"{parent}.{func.__name__}{arg_str}: {ret_str}")
        # Return ret value from wrapper
        return ret
    return wrapper
