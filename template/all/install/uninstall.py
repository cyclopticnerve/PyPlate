#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: uninstall.py                                          |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE__                                         \          /
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

# system imports
from pathlib import Path
import shutil
import sys

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# get prj dir
P_DIR_PRJ = Path(__file__).parent.resolve()

# get dirs
P_DIR_INSTALL = P_DIR_PRJ / "__PP_DIR_INSTALL__"

# get files
P_FILE_CFG = P_DIR_PRJ / "__PP_FILE_INST_CFG__"
# NB: path changes after dist
P_FILE_CFG_DIST = P_DIR_INSTALL / "__PP_FILE_INST_CFG__"

P_FILE_PRE = P_DIR_INSTALL / "__PP_INST_PRE__"
P_FILE_POST = P_DIR_INSTALL / "__PP_INST_POST__"

# ------------------------------------------------------------------------------
# Local imports
# ------------------------------------------------------------------------------

# fudge path to load base
sys.path.append(str(P_DIR_INSTALL))

# local imports
# pylint: disable=wrong-import-position
from install_base import _  # type: ignore
from install_base import CNInstallBase  # type: ignore

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

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
    # Class constants
    # --------------------------------------------------------------------------

    # strings
    # NB: format param is prog_name
    # I18N: uninstall the program
    S_MSG_UNINST_START = _("Uninstalling {}")
    # I18N: show the copy step
    S_MSG_DEL_START = _("Deleting files... ")
    # NB: format param is prog_name
    # I18N: done uninstalling
    S_MSG_UNINST_END = _("{} uninstalled")

    # questions
    # NB: format param is prog name
    # I18N: ask to uninstall
    S_ASK_UNINST = _("This will uninstall {}.\nDo you want to continue?")

    # dry run messages
    # NB: format param is file or dir path
    S_DRY_REMOVE = "\nremove\n{}"

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

    # ------------------------------------------------------------------------------
    # Uninstall the program
    # ------------------------------------------------------------------------------
    def main(self):
        """
        Uninstall the program

        Runs the uninstall operation.
        """

        # do setup
        self._setup()

        # get prj info from cfg
        self._get_project_info()

        # do pre uninstall
        self._do_external(P_FILE_PRE)

        # create an instance of the class
        self._uninstall_content()

        # wind down
        self._teardown()

        # do pre uninstall
        self._do_external(P_FILE_POST)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # NB: these are the main steps, called in order from main

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    # def _setup(self):
    #     """
    #     Boilerplate to use at the start of main

    #     Perform some mundane stuff like setting properties.
    #     If you implement this function. make sure to call super() LAST!!!
    #     """

    #     # do setup
    #     super()._setup()

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Get the install info from the config file.
        """

        # get path to config (ide or dist)
        path_cfg = P_FILE_CFG
        if not path_cfg.exists():
            path_cfg = P_FILE_CFG_DIST

        try:
            # get project info
            self._dict_cfg = self._get_dict_from_file(path_cfg)
        except OSError as e:
            print(self.S_ERR_ERR, e)

        # get prg name/version
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]

        # check for force to skip question
        force = self._dict_args.get(self.S_ARG_FORCE_DEST, False)
        if not force:

            # ask to uninstall
            str_ask = self._dialog(
                self.S_ASK_UNINST.format(prog_name),
                [self.S_ASK_YES, self.S_ASK_NO],
                self.S_ASK_NO,
            )

            # user hit enter or typed "n/N"
            if str_ask != self.S_ASK_YES:
                print(self.S_MSG_ABORT)
                sys.exit(0)

        # print start msg
        print()
        print(self.S_MSG_UNINST_START.format(prog_name))

    # --------------------------------------------------------------------------
    # Uninstall the program
    # --------------------------------------------------------------------------
    def _uninstall_content(self):
        """
        Uninstall the program

        Runs the uninstall operation.
        """

        # uninstall

        # show some info
        print(self.S_MSG_DEL_START, flush=True, end="")

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_UNINST_CONT, [])

        # for each key, value
        for item in content:

            # get full path of destination
            src = Path.home() / item

            # check for dry run
            if self._dry_run:
                print(self.S_DRY_REMOVE.format(item))
                continue

            # debug may omit certain assets
            if not src.exists():
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
        print(self.S_MSG_DONE)

        # just show we are done
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]
        print(self.S_MSG_UNINST_END.format(prog_name))


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
