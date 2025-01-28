#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: install.py                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The install script for this project

THis module installs the project, copying its files and folders to the
appropriate locations on the user's computer.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

DIR_SELF = Path(__file__).parent.resolve()
DIR_ASSETS = DIR_SELF / "__PP_INST_ASSETS__"

FILE_CFG_NEW = DIR_ASSETS / "__PP_INST_CONF_FILE__"
FILE_DESK = DIR_ASSETS / "__PP_FILE_DESK__"
FILE_REQS = DIR_ASSETS / "__PP_DIR_INSTALL__" / "__PP_REQS_FILE__"
DIR_LIB = DIR_ASSETS / "__PP_DIR_LIB__"

DIR_USR_INST = Path.home() / "__PP_USR_INST__"
DIR_VENV = DIR_USR_INST / "__PP_NAME_VENV__"
FILE_CFG_OLD = DIR_USR_INST / "__PP_UNINST_CONF_FILE__"
FILE_DESK_ICON = Path.home() / "__PP_DESK_ICON__"

# add paths to import search
sys.path.append(str(DIR_LIB))

# import my stuff
import cnlib.cninstall as C  # type: ignore
from cnlib.cnformatter import CNFormatter  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error


# ------------------------------------------------------------------------------
# Run the main function
# ------------------------------------------------------------------------------
def main(debug=False):
    """
    Run the main function

    Args:
        debug: If True, run in debug mode (default: False)

    The main entry point for the program.
    """

    # create an instance of the class
    inst = C.CNInstall()

    # run the instance
    try:
        # NB: ORDER IS IMPORTANT! (at least for .desktop)
        # you must fix the .desktop file before install b/c path to .desktop is
        # rel to assets

        # gui
        inst.fix_desktop_file(FILE_DESK, FILE_DESK_ICON)
        # gui, cli
        # inst.make_venv(DIR_USR_INST, DIR_VENV, FILE_REQS)
        # gui, cli
        inst.install(DIR_ASSETS, FILE_CFG_NEW, FILE_CFG_OLD, DIR_USR_INST, DIR_VENV, FILE_REQS, debug=debug)
    except C.CNInstallError as e:
        print(e)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # NB: argparse code placed here so we can run the script from the command
    # line or use it as an object

    # create the parser
    parser = argparse.ArgumentParser(formatter_class=CNFormatter)

    # add debug option
    parser.add_argument(
        C.CNInstall.S_DBG_OPTION,
        action=C.CNInstall.S_DBG_ACTION,
        dest=C.CNInstall.S_DBG_DEST,
        help=C.CNInstall.S_DBG_HELP,
    )

    # get namespace object
    args = parser.parse_args()

    # convert namespace to dict
    dict_args = vars(args)

    # --------------------------------------------------------------------------

    # get the args
    a_debug = dict_args.get(C.CNInstall.S_DBG_DEST, False)

    # run main function
    main(a_debug)

# -)
