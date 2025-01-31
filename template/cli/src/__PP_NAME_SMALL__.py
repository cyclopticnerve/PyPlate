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
import gettext
import locale
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

# add paths to import search
sys.path.append(str(P_DIR_LIB_INST))
sys.path.append(str(P_DIR_LIB))

# import my stuff
from cnlib import cnfunctions as F  # type: ignore
from cnlib import cncli as C  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Required for pybaker
# ------------------------------------------------------------------------------

# globals for pb to find
# NB: you may edit these by hand, but they will be overwritten by PyBaker
S_PP_VERSION = "__PP_VERSION__"
S_PP_SHORT_DESC = "__PP_SHORT_DESC__"

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# ------------------------------------------------------------------------------

# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_SMALL__.py
DOMAIN = "__PP_NAME_SMALL__"
if P_DIR_PRJ_INST.exists():
    DIR_LOCALE = P_DIR_PRJ_INST / "__PP_PATH_LOCALE__"
else:
    DIR_LOCALE = P_DIR_PRJ / "__PP_PATH_LOCALE__"
TRANSLATION = gettext.translation(DOMAIN, DIR_LOCALE, fallback=True)
_ = TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(DOMAIN, DIR_LOCALE)

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# version string
# NB: done in two steps to avoid linter errors
S_VER_CFG = "__PP_VER_FMT__"
S_VER_FMT = S_VER_CFG.format(S_PP_VERSION)

# about string
S_ABOUT = (
    "__PP_NAME_BIG__\n"
    f"{S_PP_SHORT_DESC}\n"
    f"{S_VER_FMT}\n"
    "__PP_URL__/__PP_NAME_BIG__\n"
)

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------

# path to default config file
P_CFG_DEF = None

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class __PP_NAME_CLASS__(C.CNCli):
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class does the most of the work of a typical CLI program. It parses
    command line options, loads/saves config files, and performs the operations
    required for the program.
    """

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
        print(self._func())

        # ----------------------------------------------------------------------
        # teardown

        # call boilerplate code
        self._teardown()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Short description
    # --------------------------------------------------------------------------
    def _func(self):
        """
        Short description

        Args:
            var_name: Short description

        Returns:
            Description

        Raises:
            exception_type(vars): Description

        Long description (including HTML).
        """

        # sample of using repl switch
        # pyplate: disable=replace
        _leave_alone = "__PP_NAME_BIG__"
        # pyplate: enable=replace
        _fix_me = "__PP_NAME_BIG__"
        _leave_it = "__PP_NAME_BIG__" # pyplate: disable=replace

        # check for debug flag
        if self._debug:
            return _("this is func (DEBUG)")

        # no debug, return normal result
        return _("this is func")

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    def _setup(self):
        """
        Boilerplate to use at the start of main

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """

        # print the about string
        print(S_ABOUT)

        # call to super run arg parser
        super()._run_parser()

        # super load config file (or not, if no param and not using -c)
        super()._load_config(P_CFG_DEF)

        # throw in a debug test
        if self._debug:
            F.pp(self._dict_cfg, label="load cfg:")

    # --------------------------------------------------------------------------
    # Add arguments to argparse parser
    # --------------------------------------------------------------------------
    def _add_args(self, parser):
        """
        Add arguments to argparse parser

        Args:
            parser: The ArgumentParser to add the args to

        This method is called by the superclass's _run_parser method, and
        allows subclasses to add their own arguments to the parser.
        """

        # set help string
        parser.description = S_ABOUT

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
        self._save_config()


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    obj = __PP_NAME_CLASS__()

    # run the new object
    obj.main()

# -)
