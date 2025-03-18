#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: install.py                                            |     ()     |
# Date    : 03/15/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
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

# constants
DIR_PRJ = Path(__file__).parent.resolve()
DIR_ASSETS = DIR_PRJ / "__PP_INST_ASSETS__"
DIR_USR_INST = Path.home() / "__PP_USR_INST__"
DIR_VENV = DIR_USR_INST / "__PP_NAME_VENV__"
DIR_LIB = DIR_ASSETS / "__PP_DIR_LIB__"
sys.path.append(str(DIR_LIB))

FILE_DESK = DIR_ASSETS / "__PP_FILE_DESK__"
FILE_DESK_ICON = Path.home() / "__PP_DESK_ICON__"

FILE_CFG_INST = DIR_ASSETS / "__PP_INST_CONF_FILE__"
FILE_CFG_UNINST = DIR_USR_INST / "__PP_UNINST_CONF_FILE__"
FILE_REQS = DIR_ASSETS / "__PP_DIR_INSTALL__" / "__PP_REQS_FILE__"

# pylint: disable=wrong-import-position
# pylint: disable=import-error

# import my stuff
from cnlib.src.cninstall import CNInstall # type: ignore
from cnlib.src.cninstall import CNInstallError # type: ignore
from cnlib.src.cnformatter import CNFormatter # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=import-error

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

        # gui
        inst.fix_desktop_file(FILE_DESK, FILE_DESK_ICON, dry=dry)

        # gui, cli
        inst.install(
            DIR_ASSETS,
            DIR_LIB,
            FILE_CFG_INST,
            FILE_CFG_UNINST,
            DIR_USR_INST,
            DIR_VENV,
            FILE_REQS,
            dry=dry
        )
    except CNInstallError as e:
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
