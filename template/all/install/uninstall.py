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

This module uninstalls the project, removing its files and folders to the
appropriate locations on the user's computer.

This file is real ugly b/c we can't access the venv, so we do it manually.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# NB: pure python
# system imports
from pathlib import Path
import shutil
import sys

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# get pkg dir
P_DIR_PARENT = Path(__file__).parent.resolve()

# get dirs
P_DIR_INSTALL = P_DIR_PARENT / "__PP_DIR_INSTALL__"

# get files
P_FILE_CFG_OLD = P_DIR_INSTALL / "__PP_FILE_INST_CFG__"

# get pre/post files
# NB: uncomment these and pybaker will replace them
# P_FILE_PRE = P_DIR_INSTALL / "__PP_UNINST_PRE__"
# P_FILE_POST = P_DIR_INSTALL / "__PP_UNINST_POST__"

# ------------------------------------------------------------------------------
# Local imports
# ------------------------------------------------------------------------------

# fudge path to load base
sys.path.append(str(P_DIR_INSTALL))

# local imports
# pylint: disable=wrong-import-position, import-error
from install_base import CNInstallBase  # type: ignore

# pylint: enable=wrong-import-position, import-error

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The class to use for installing/uninstalling
# ------------------------------------------------------------------------------
class CNUninstall(CNInstallBase):
    """
    The class to use for uninstalling a PyPlate program

    This class performs the uninstall operation.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the new object

        Initializes a new instance of the class, setting the default values
        of its properties, and any other code that needs to run to create a
        new object.
        """

        # always call super
        super().__init__()

        # redeclare prop for some reason?
        self._dict_cfg = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Uninstall the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        Uninstall the program

        Runs the uninstall operation.
        """

        # do setup
        self._setup()

        # get prj info from cfg
        self._get_project_info()

        # get prg name/version
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]

        # show some info
        if not self._arg_quiet:
            print(self.S_MSG_UNINST_START.format(prog_name))
            print()

        # create an instance of the class
        self._uninstall_cont(self._arg_quiet)

        # uninstall conf stuff
        self._uninstall_conf()

        # maybe show we are done
        if not self._arg_quiet:
            if not self._arg_dry:
                print()
            print(self.S_MSG_UNINST_END.format(prog_name))

        # wind down
        self._teardown()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # NB: these are the main steps, called in order from main

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Get the install info from the config file.
        """

        # ----------------------------------------------------------------------
        # get old info

        try:
            # get project info
            self._dict_cfg = self._get_dict_from_file(P_FILE_CFG_OLD)
        except OSError as e:
            # fatal error, print and quit
            # NB: print even if quiet
            print(self.S_ERR_ERR, e)
            self._teardown(-1)

        # ----------------------------------------------------------------------
        # check for reasons to skip question

        # don't ask question
        if self._arg_force:
            return

        # ----------------------------------------------------------------------

        # get prg name/version
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]

        # ask to uninstall
        str_ask = self._dialog(
            self.S_ASK_UNINST.format(prog_name),
            [self.S_ASK_YES, self.S_ASK_NO],
            self.S_ASK_NO,
        )
        print()

        # user hit enter or typed anything else except "y"
        if str_ask != self.S_ASK_YES:
            # normal error, print and quit
            if not self._arg_quiet:
                print(self.S_MSG_ABORT)
            self._teardown()

    # --------------------------------------------------------------------------
    # Uninstall the config stuff after final delete
    # --------------------------------------------------------------------------
    def _uninstall_conf(self):
        """
        Uninstall the config stuff after final delete

        Runs the uninstall operation.
        """

        # show some progress
        if not self._arg_quiet and not self._arg_dry:
            print(self.S_MSG_DEL_CFG_START, flush=True, end="")

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_CFG_CONT, {})

        # for each key, value
        for _k, v in content.items():

            # get full path of destination
            src = Path.home() / v

            # debug may omit certain assets
            if not src.exists():
                continue

            # if it's a dry run, don't do anything
            if self._arg_dry:
                print(self.S_DRY_REMOVE, src)
                continue

            # if the source is a dir
            if src.is_dir():
                # remove dir
                shutil.rmtree(src)

            # if the source is a file
            else:
                # copy file
                src.unlink()

        # show some info
        if not self._arg_quiet and not self._arg_dry:
            print(self.S_MSG_DONE)

        # for make pretty
        if self._arg_dry:
            print()


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    inst = CNUninstall()

    # run the instance
    inst.main()

# -)
