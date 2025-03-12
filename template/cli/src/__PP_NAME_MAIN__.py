#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_MAIN__.py                                   |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ cd [path to directory of this file]
foo@bar:~[path to directory of this file]$ ./__PP_NAME_MAIN__.py [cmd line]

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
from pathlib import Path

# import my stuff
import cnfunctions as F
from cncli import CNCli

# find path to prj
# NB: keep this global for i18n stuff
P_DIR_PRJ = Path(__file__).parents[1].resolve()

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# ------------------------------------------------------------------------------

# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py
DOMAIN = "__PP_NAME_PRJ_SMALL__"
DIR_LOCALE = P_DIR_PRJ / "__PP_PATH_LOCALE__"
TRANSLATION = gettext.translation(DOMAIN, DIR_LOCALE, fallback=True)
_ = TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(DOMAIN, DIR_LOCALE)

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class __PP_NAME_PRJ_PASCAL__(CNCli):
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class does the most of the work of a typical CLI program. It parses
    command line options, loads/saves config files, and performs the operations
    required for the program.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # globals for pb to find
    # NB: you may edit these by hand, but they will be overwritten by PyBaker

    # version string
    S_PP_VERSION = "__PP_VERSION__"

    # I18N: short description
    S_PP_SHORT_DESC = _("__PP_SHORT_DESC__")

    # formatted version string
    # NB: done in two steps to avoid linter errors
    S_VER_FMT = "__PP_VER_FMT__"
    S_VER_OUT = S_VER_FMT.format(S_PP_VERSION)

    # about string
    S_ABOUT = (
        f"{'__PP_NAME_PRJ__'}\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_VER_OUT}\n"
        "__PP_URL__/__PP_NAME_PRJ_BIG__\n"
    )

    # path to default config file
    P_CFG_DEF = None

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
        _fix = "__PP_NAME_PRJ_BIG__"

        # pyplate: disable=replace
        _dont_fix = "__PP_NAME_PRJ_BIG__"
        # pyplate: enable=replace

        _fix = "__PP_NAME_PRJ_BIG__"

        _dont_fix = "__PP_NAME_PRJ_BIG__"  # pyplate: disable=replace

        _fix = "__PP_NAME_PRJ_BIG__"

        # pyplate: disable=replace
        _fix = "__PP_NAME_PRJ_BIG__"  # pyplate: enable=replace
        # pyplate: enable=replace

        # check for debug flag
        if self._debug:
            # I18N: context for this string
            return _("this is func (DEBUG)")

        # no debug, return normal result
        # I18N: context for this string
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

        # set default about text
        s_about = self.S_ABOUT

        # ----------------------------------------------------------------------

        # use cmd line

        # add help text to about block
        s_about = self.S_ABOUT + self.S_ABOUT_HELP
        self._parser.description = s_about

        # add some options
        self._add_cfg_arg()
        self._add_dbg_arg()

        # run the parser
        # NB: if -h passed, this will print and exit
        self._run_parser()

        # ----------------------------------------------------------------------

        # print about msg on every run (but only after checking for -h)
        print(s_about)

        # super load config file (or not, if no param and not using -c)
        # NB: first param is path to us (for rel path)
        # NB: second param is path to def file or none
        parent_dir = Path(__file__).parent.resolve()
        self._load_config(parent_dir, self.P_CFG_DEF)

        # throw in a debug test
        if self._debug:
            F.pp(self._dict_cfg, label="load cfg")

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
            F.pp(self._dict_cfg, label="save cfg")

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
    obj = __PP_NAME_PRJ_PASCAL__()

    # run the new object
    obj.main()

# -)
