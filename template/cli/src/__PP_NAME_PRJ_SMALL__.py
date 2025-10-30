#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_PRJ_SMALL__.py                              |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ cd [path to directory of this file]
foo@bar:~[path to directory of this file]$ ./__PP_NAME_PRJ_SMALL__.py [cmd line]

or if installed in a global location:

foo@bar:~$ __PP_NAME_PRJ_SMALL__ [cmd line]

Typical usage is show in the main() method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import locale
import logging
from pathlib import Path

# local imports
from __PP_NAME_PRJ_SMALL___base import __PP_NAME_PRJ_PASCAL__Base

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI and GUI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py

# path to project dir
T_DIR_PRJ = Path(__file__).parents[1].resolve()

# init gettext
T_DOMAIN = "__PP_NAME_PRJ_SMALL__"
T_DIR_LOCALE = T_DIR_PRJ / "__PP_PATH_LOCALE__"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class __PP_NAME_PRJ_PASCAL__(__PP_NAME_PRJ_PASCAL__Base):
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class does the most of the work of a typical CLI program. It parses
    command line options, loads/saves config files, and performs the operations
    required for the program.
    """

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    # def __init__(self):
    #     """
    #     Initialize the new object

    #     Initializes a new instance of the class, setting the default values
    #     of its properties, and any other code that needs to run to create a
    #     new object.
    #     """

    #     # do super init
    #     super().__init__()

    # NB: add class properties here

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

        super().main()

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

    # NB: these are the main steps, called in order from main

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    def _setup(self):
        """
        Boilerplate to use at the start of main

        Perform some mundane stuff like setting properties.
        """

        # do setup
        super()._setup()

        # add cfg option
        self._parser.add_argument(
            self.S_ARG_CFG_OPTION,
            dest=self.S_ARG_CFG_DEST,
            help=self.S_ARG_CFG_HELP,
            metavar=self.S_ARG_CFG_METAVAR,
        )

        # add debug option
        self._parser.add_argument(
            self.S_ARG_DBG_OPTION,
            action=self.S_ARG_DBG_ACTION,
            dest=self.S_ARG_DBG_DEST,
            help=self.S_ARG_DBG_HELP,
        )


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

        logging.info("_func")

        # check for debug flag
        if self._debug:
            # I18N: context for this string
            return _("this is func (DEBUG)")

        # no debug, return normal result
        # I18N: context for this string
        return _("this is func")

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    obj = __PP_NAME_PRJ_PASCAL__()

    # run the new object
    obj.main()

# -)
