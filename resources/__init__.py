# -*- coding: utf-8 -*-

"""Resources __init__ module."""

import logging
from os.path import basename

import xbmc
import xbmcvfs

from resources.lib import MANAGED_FOLDER
from resources.lib.database.createtables import DBCreateTables
from resources.lib.filesystem import join, mk_dir, isdir
from resources.lib.gui.gui_utils import notification, get_string, bold

LOG = logging.getLogger(basename(__file__))


def create_base_diretories():
    """Create sub-dirs in managed folder if not exist."""
    if not xbmcvfs.exists(MANAGED_FOLDER):
        mk_dir(MANAGED_FOLDER)
        LOG.info(get_string(32187) % bold(MANAGED_FOLDER))

    # Create folders if they don't exist
    folders = [
        "movies",
        "tvshows",
    ]
    # MANAGED_FOLDER
    created_status = False
    for diretory in folders:
        content_dir = join(MANAGED_FOLDER, diretory)
        if isdir(content_dir):
            continue
        dir_created_string = get_string(32188) % bold(diretory)
        LOG.info(dir_created_string)
        notification(dir_created_string)
        mk_dir(content_dir)
        created_status = True

    if created_status:
        notification(get_string(32127))
        xbmc.sleep(1)


# Create all LIT dirs, managed_folder, movies and tvshows
create_base_diretories()
# A quick way to create the tables on opening the script
# avoids the need to call this function in multiple different locations
DBCreateTables()
