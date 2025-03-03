#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: uninstall.py                                          |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The uninstall script for this project

THis module uninstalls the project, removing its files and folders to the
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
DIR_PRJ = Path(__file__).parents[1].resolve()
DIR_LIB = DIR_PRJ / "__PP_DIR_LIB__"
sys.path.append(str(DIR_LIB))

FILE_CFG_UNINST = DIR_PRJ / "__PP_UNINST_CONF_FILE__"

# pylint: disable=wrong-import-position
# import my stuff
from cninstall import CNInstall
from cninstall import CNInstallError
from cnformatter import CNFormatter

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
        inst.uninstall(FILE_CFG_UNINST, dry=dry)
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
