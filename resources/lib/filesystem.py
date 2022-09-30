# -*- coding: utf-8 -*-
# pylint: disable=broad-except

"""Filesystem utils for Windows/Linux."""

import logging
import os
from os.path import basename, dirname

import xbmcvfs

LOG = logging.getLogger(basename(__file__))


def mk_dir(dir_path):
    """
    Create folder(s) - it will create all folders in the path.

    Like: mk_dir -p on linux.
    """
    if xbmcvfs.exists(dir_path):
        return False
    return xbmcvfs.mkdirs(dir_path)


# def mv_with_type(title_path, filetype, title_dst):
#     """Move files with wildcard between title_path & filetype to title_dst."""
#     os.system(f'mv "{title_path}"*{filetype} "{title_dst}{filetype}"')

def list_dir(dir_path_to_list, full_path=False):
    """Function to list files in dir."""
    itens = []
    for item in xbmcvfs.listdir(dir_path_to_list):
        for content in item:
            if full_path:
                full_path = join([dir_path_to_list, content])
                if isdir(full_path):
                    itens.append(full_path)
                else:
                    itens.append(join([dir_path_to_list, content], True))
            else:
                itens.append(content)
    return itens


def delete_file(file_path: str):
    """Delete a file."""
    return xbmcvfs.delete(file_path)


def delete_files_in_diretory(diretory_path: str):
    """Delete multiple files."""
    for file in [join([diretory_path, file]) for file in list_dir(diretory_path)]:
        xbmcvfs.delete(file)


def delete_with_wildcard(title_path):
    """Remove all files starting with title_path using wildcard."""
    wildcard = basename(title_path)
    directory = dirname(title_path)
    try:
        for file in list_dir(dirname(directory)):
            if wildcard in file:
                try:
                    xbmcvfs.delete(file)
                except FileNotFoundError:
                    pass
    except Exception as err:
        raise err


def isdir(path):
    """Check if folder path is a real folder (like an os.path.isdir but with xbmcvfs)."""
    is_dir_file = os.path.join(path, "is_path.txt")
    test_path_file = xbmcvfs.File(is_dir_file, "w").write("success")
    xbmcvfs.delete(is_dir_file)
    return test_path_file


def join(*args, file=False):
    """Join like os.path.join but add \\ or / if necessary."""
    joined_path = os.path.join(*args)
    if file:
        return joined_path
    return "".join([joined_path, "\\" if os.name == "nt" else "/"])


def remove_dirs(base_path):
    """Complete delete a diretory and all files and sub-dirs."""
    dirs_to_delete = []
    for path_to_delete in list_dir(base_path, True):
        # Delete a file
        xbmcvfs.delete(path_to_delete)

        # Delete a dir
        dirs_to_delete.append(path_to_delete)
        if isdir(path_to_delete):
            remove_dirs(path_to_delete)

    for diretory in dirs_to_delete:
        remove_dir(diretory)
    remove_dir(base_path)


def remove_dir(diretory_path):
    """Remove directory at dir_path."""
    diretory_path = xbmcvfs.validatePath(diretory_path)
    LOG.debug("remove_dir delete path: %s", diretory_path)
    return xbmcvfs.rmdir(diretory_path, True)
