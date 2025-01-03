#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__                                     |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ cd [path to directory of this file]
foo@bar:~[path to directory of this file]$ ./__PP_NAME_SMALL__ [cmd line]

or if installed in a global location:

foo@bar:~$ __PP_NAME_SMALL__ [cmd line]

Typical usage is show in the main() method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# find path to lib
P_DIR_PRJ_INST = Path.home() / "__PP_USR_INST__"
P_DIR_PRJ = Path(__file__).parents[1].resolve()

P_DIR_LIB_INST = P_DIR_PRJ_INST / "__PP_DIR_LIB__"
P_DIR_LIB = P_DIR_PRJ / "__PP_DIR_LIB__"

P_DIR_GUI_INST = P_DIR_PRJ_INST / "__PP_DIR_SRC__/__PP_DIR_GUI__"
P_DIR_GUI = P_DIR_PRJ / "__PP_DIR_SRC__/__PP_DIR_GUI__"

# add paths to import search
sys.path.append(str(P_DIR_LIB_INST))
sys.path.append(str(P_DIR_LIB))
sys.path.append(str(P_DIR_GUI_INST))
sys.path.append(str(P_DIR_GUI))

# import my stuff
from cnlib import cnfunctions as F  # type: ignore
import cnlib.cncli as C  # type: ignore
from cnlib.cncli import CNCli  # type: ignore
from python.app_main import AppMain  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Required for pybaker
# ------------------------------------------------------------------------------

# globals for pb to find
S_PP_VERSION = "__PP_VERSION__"
S_PP_SHORT_DESC = "__PP_SHORT_DESC__"


# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class __PP_NAME_CLASS__(CNCli):
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class does the most of the work of a typical CLI program. It parses
    command line options, loads/saves config files, and performs the operations
    required for the program.

    It also checks for the GUI option on the command line and, if found,
    creates an object from another script to handle the GUI.
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

        # call super init to initialize the base class
        super().__init__()

        # set default property values
        # NB: commented props are from super
        # self._dict_args = {}   # set in super
        # self._dict_cfg = {}    # set in super
        # self._path_cfg = None  # set in super
        self._debug = False

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main method of the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        The main method of the program

        This method is the main entry point for the program, initializing the
        program, and performing its steps.
        """

        # ----------------------------------------------------------------------
        # setup

        # call boilerplate code
        self._setup()

        # ----------------------------------------------------------------------
        # main stuff

        # do the thing with the thing
        app = AppMain(self._dict_args)
        app.run()

        # ----------------------------------------------------------------------
        # teardown

        # call boilerplate code
        self._teardown()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    def _setup(self):
        """
        Boilerplate to use at the start of main

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """

        # call to set up and run arg parser
        super()._run_parser()

        # get other options from command line
        self._debug = self._dict_args[C.S_ARG_DBG_DEST]

        # # the default config file
        # cfg_def = str(DIR_CFG / "__PP_NAME_SMALL__.json")

        # # command line cfg is None or str
        # cfg_arg = self._dict_args[C.S_ARG_CFG_DEST]

        # # load the config file
        # # not using def path, using arg path
        # # super()._load_config(None, cfg_arg, self._d_cfg)
        # # using def path, not using arg path
        # # super()._load_config(cfg_def, dict_def=self._d_cfg)
        # # using def path, using arg path, using internal
        # super()._load_config(
        #     cfg_def, path_arg=cfg_arg, dict_def=self._dict_cfg
        # )

        # # throw in a debug test
        # if self._debug:
        #     F.pp(self._dict_cfg, label="load cfg:")

    # --------------------------------------------------------------------------
    # Add arguments to argparse parser
    # --------------------------------------------------------------------------
    def _add_args(self, parser):
        """
        Add arguments to argparse parser

        Arguments:
            parser: The ArgumentParser to add the args to

        This method is teased out for better code maintenance.
        """

        # formatted version
        # NB: done in two steps to avoid linter warnings
        ver_cfg = "__PP_VER_FMT__"
        ver_fmt = ver_cfg.format(S_PP_VERSION)

        # about string
        s_about = (
            "__PP_NAME_BIG__\n"
            f"{S_PP_SHORT_DESC}\n"
            f"{ver_fmt}\n"
            "__PP_URL__/__PP_NAME_BIG__"
        )

        # set help string
        parser.description = s_about

        # add debug option
        parser.add_argument(
            C.S_ARG_DBG_OPTION,
            action=C.S_ARG_DBG_ACTION,
            dest=C.S_ARG_DBG_DEST,
            help=C.S_ARG_DBG_HELP,
        )

        # add config (user dict) option
        parser.add_argument(
            C.S_ARG_CFG_OPTION,
            dest=C.S_ARG_CFG_DEST,
            help=C.S_ARG_CFG_HELP,
            metavar=C.S_ARG_CFG_METAVAR,
        )

    # --------------------------------------------------------------------------
    # Boilerplate to use at the end of main
    # --------------------------------------------------------------------------
    def _teardown(self):
        """
        Boilerplate to use at the end of main

        Perform some mundane stuff like saving config files.
        """

        # throw in a debug test
        if self._debug:
            F.pp(self._dict_cfg, label="save cfg:")

        # call to save config
        super()._save_config()


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    __PP_NAME_CLASS__().main()

# -)
