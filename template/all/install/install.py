#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: install.py                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The install script for this project

THis module installs the project, copying its files and folders to the
appropriate locations on the user's computer.

This file is real ugly b/c we can't access the venv, so we do it manually.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from pathlib import Path
import sys

# ------------------------------------------------------------------------------
# local imports

# pylint: disable=import-error
# pylint: disable=wrong-import-position

# add assets lib to path
P_DIR_PRJ = Path(__file__).parent.resolve()
P_DIR_ASSETS = P_DIR_PRJ / "assets"
P_DIR_LIB = P_DIR_ASSETS / "lib"
sys.path.append(str(P_DIR_LIB))

# local imports
from cnlib.src.cninstall import CNInstall  # type: ignore
from cnlib.src.cnformatter import CNFormatter  # type: ignore

# pylint: enable=import-error
# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# get dirs
P_DIR_USR_INST = Path.home() / "__PP_USR_INST__"
P_DIR_VENV = P_DIR_USR_INST / "__PP_NAME_VENV__"

# get files
P_FILE_DESK = P_DIR_ASSETS / "__PP_FILE_DESK__"
P_FILE_DESK_ICON = Path.home() / "__PP_IMG_DESK__"
P_FILE_CFG_INST = P_DIR_ASSETS / "__PP_INST_CONF_FILE__"
P_FILE_CFG_UNINST = P_DIR_USR_INST / "__PP_UNINST_CONF_FILE__"
P_FILE_REQS = P_DIR_ASSETS / "__PP_DIR_INSTALL__" / "__PP_REQS_FILE__"


# ------------------------------------------------------------------------------
# Run the main function
# ------------------------------------------------------------------------------
def main(dry=False):
    """
    Run the main function

    Args:
        dry: If True, run in dry-run mode (default: False)

    The main entry point for the program.
    """

    # create an instance of the class
    inst = CNInstall()

    # run the instance
    try:
        # NB: ORDER IS IMPORTANT! (at least for .desktop)
        # you must fix the .desktop file before install b/c path to .desktop is
        # rel to assets

        # fix desktop file if present
        inst.fix_desktop_file(P_FILE_DESK, P_FILE_DESK_ICON, dry=dry)

        # gui, cli
        inst.install(
            P_DIR_ASSETS,
            P_DIR_LIB,
            P_FILE_CFG_INST,
            P_FILE_CFG_UNINST,
            P_DIR_USR_INST,
            P_DIR_VENV,
            P_FILE_REQS,
            dry=dry,
        )
    except Exception as e:
        raise e


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create the parser
    parser = argparse.ArgumentParser(formatter_class=CNFormatter)

    # add dry-run option
    parser.add_argument(
        CNInstall.S_DRY_OPTION,
        action=CNInstall.S_DRY_ACTION,
        dest=CNInstall.S_DRY_DEST,
        help=CNInstall.S_DRY_HELP,
    )

    # get namespace object
    args = parser.parse_args()

    # convert namespace to dict
    dict_args = vars(args)

    # --------------------------------------------------------------------------

    # get the args
    a_dry = dict_args.get(CNInstall.S_DRY_DEST, False)

    # run main function
    main(a_dry)

# -)
