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
appropriate locations on the user's computer. It also provides for hooks to run
Python (or other language) scripts before and after the actual install process.
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
FILE_CFG_OLD = Path.home() / "__PP_USR_CONF__" / "__PP_INST_CONF_FILE__"
DIR_LIB = DIR_ASSETS / "__PP_DIR_LIB__"

# add paths to import search
sys.path.append(str(DIR_LIB))

# import my stuff
import cnlib.cnfunctions as F  # type: ignore
import cnlib.cninstall as C # type: ignore
from cnlib.cnformatter import CNFormatter # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Required for pybaker
# ------------------------------------------------------------------------------

# globals for pb to find
# NB: you may edit these by hand, but they will be overwritten by PyBaker
# S_PP_VERSION = "__PP_VERSION__"

# ------------------------------------------------------------------------------
# Run the main function
# ------------------------------------------------------------------------------
def main(debug=False):
    """
    Run the main function

    Arguments:
        debug: If True, run ijn debug mode (default: False)

    The main entry point for the program.
    """

    # create an instance of the class
    inst = C.CNInstall()

    # run the instance
    try:
        inst.install(DIR_ASSETS, FILE_CFG_NEW, FILE_CFG_OLD, debug=debug)
    except C.CNInstallError as e:
        print(e)

    # make symlink
    cmd = (
        "ln -s "
        # the real script to run
        "$HOME/__PP_USR_CONF__/__PP_DEV_SRC__/__PP_NAME_SMALL__.py "
        # the symlinked script
        "$HOME/__PP_USR_BIN__/__PP_NAME_SMALL__"
    )

    # get result of running the shell command or bubble up an error
    try:
        F.sh(cmd, shell=True)
    except F.CNShellError as e:
        print(e.message)

    # get result of running the shell command or bubble up an error
    # try:
    #     res = subprocess.run(
    #         # the array of commands produced by shlex.split
    #         CMD,
    #         # if check is True, an exception will be raised if the return code
    #         # is not 0
    #         # if check is False, no exception is raised but res will be None,
    #         # meaning you have to test for it in the calling function
    #         # but that also means you have no information on WHY it failed
    #         check=True,
    #         # convert stdout/stderr from bytes to text
    #         text=True,
    #         # put stdout/stderr into res
    #         capture_output=True,
    #         # whether the call is a file w/ params (False) or a direct shell
    #         # input (True)
    #         shell=True,
    #     )

    # # this is the return code check
    # except subprocess.CalledProcessError as e:
    #     print(e)


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

    # set help string
    # parser.description = S_PP_ABOUT

    # add debug option
    parser.add_argument(
        C.S_DBG_OPTION,
        action=C.S_DBG_ACTION,
        dest=C.S_DBG_DEST,
        help=C.S_DBG_HELP,
    )

    # get namespace object
    args = parser.parse_args()

    # convert namespace to dict
    dict_args = vars(args)

    # --------------------------------------------------------------------------

    # get the args
    # a_dir_cur = os.getcwd()
    a_debug = dict_args.get(C.S_DBG_DEST, False)

    # run main function
    main(a_debug)

# -)
