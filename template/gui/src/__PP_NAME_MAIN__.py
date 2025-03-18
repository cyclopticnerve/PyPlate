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
import argparse
import gettext
import locale
from pathlib import Path

# ------------------------------------------------------------------------------

# NB: sloppy, but fixes pdoc3
import sys

P_DIR_SELF = Path(__file__).parent.resolve()
sys.path.append(str(P_DIR_SELF))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order

# import my stuff
from cnformatter import CNFormatter
import cnfunctions as F
from gui.python.__PP_FILE_APP__ import __PP_CLASS_APP__

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# ------------------------------------------------------------------------------

# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py
DOMAIN = "__PP_NAME_PRJ_SMALL__"
P_DIR_PRJ = Path(__file__).parents[1].resolve()
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
class __PP_NAME_PRJ_PASCAL__:
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

    # config option strings
    S_ARG_HLP_OPTION = "-h"
    S_ARG_HLP_ACTION = "store_true"
    S_ARG_HLP_DEST = "HLP_DEST"
    # I18N: config file option help
    S_ARG_HLP_HELP = _("show this help message and exit")

    # config option strings
    S_ARG_CFG_OPTION = "-c"
    S_ARG_CFG_DEST = "CFG_DEST"
    # I18N: config file option help
    S_ARG_CFG_HELP = _("load configuration from file")
    # I18N: config file dest
    S_ARG_CFG_METAVAR = _("FILE")

    # debug option strings
    S_ARG_DBG_OPTION = "-d"
    S_ARG_DBG_ACTION = "store_true"
    S_ARG_DBG_DEST = "DBG_DEST"
    # I18N: debug mode help
    S_ARG_DBG_HELP = _("enable debugging mode")

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

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help") + "\n"

    # path to default config file
    P_CFG_DEF = None

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

        # set defaults

        # cmd line args
        self._dict_args = {}
        self._debug = False
        self._path_cfg_arg = None

        # the final cfg path and dict
        self._path_cfg = None
        self._dict_cfg = {}

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
        app = __PP_CLASS_APP__(self._dict_args, self._dict_cfg)
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

        # print default about text
        print(self.S_ABOUT)

        # ----------------------------------------------------------------------
        # use cmd line

        # create a parser object in case we need it
        parser = argparse.ArgumentParser(
            formatter_class=CNFormatter, add_help=False
        )

        # add help text to about block
        print(self.S_ABOUT_HELP)

        parser.add_argument(
            self.S_ARG_HLP_OPTION,
            action=self.S_ARG_HLP_ACTION,
            dest=self.S_ARG_HLP_DEST,
            help=self.S_ARG_HLP_HELP,
        )

        # add some options
        parser.add_argument(
            self.S_ARG_CFG_OPTION,
            dest=self.S_ARG_CFG_DEST,
            help=self.S_ARG_CFG_HELP,
            metavar=self.S_ARG_CFG_METAVAR,
        )

        parser.add_argument(
            self.S_ARG_DBG_OPTION,
            action=self.S_ARG_DBG_ACTION,
            dest=self.S_ARG_DBG_DEST,
            help=self.S_ARG_DBG_HELP,
        )

        # run the parser
        args = parser.parse_args()
        self._dict_args = vars(args)

        # if -h passed, this will print and exit
        if self._dict_args.get(self.S_ARG_HLP_DEST, False):
            parser.print_help()
            sys.exit()

        # set props from args
        self._debug = self._dict_args.get(self.S_ARG_DBG_DEST, self._debug)
        self._path_cfg_arg = self._dict_args.get(
            self.S_ARG_CFG_DEST, self._path_cfg_arg
        )

        # ----------------------------------------------------------------------
        # use cfg

        # fix paths and get cfg to load
        self._get_path_cfg()

        # load config file (or not, if no param and not using -c)
        self._load_config()

    # --------------------------------------------------------------------------
    # Boilerplate to use at the end of main
    # --------------------------------------------------------------------------
    def _teardown(self):
        """
        Boilerplate to use at the end of main

        Perform some mundane stuff like saving config files.
        """

        # ----------------------------------------------------------------------
        # use cfg

        # call to save config
        self._save_config()

    # --------------------------------------------------------------------------
    # Get path to config file from cmd line option or default
    # --------------------------------------------------------------------------
    def _get_path_cfg(self):
        """
        Get path to config file from cmd line option or default

        This method figures the config path from either:
        1. the command line -c option (if present)
        or
        2. the self.P_CFG_DEF value (if present)

        If you use the -c option, and the file exists, it will used as the
        _path_cfg property, and processing stops.
        If you do not use the -c option, or it is not present on the command
        line, the path_def value will be used.
        If you use neither, nothing happens to the _path_cfg property.
        """

        # accept path or str
        if self._path_cfg_arg:
            self._path_cfg_arg = Path(self._path_cfg_arg)
            if not self._path_cfg_arg.is_absolute():
                # make abs rel to self
                self._path_cfg_arg = P_DIR_SELF / self._path_cfg_arg

        # accept path or str
        path_def = self.P_CFG_DEF
        if path_def:
            path_def = Path(path_def)
            if not path_def.is_absolute():
                # make abs rel to self
                path_def = P_DIR_SELF / path_def

        # ----------------------------------------------------------------------

        # if cmd line
        if self._path_cfg_arg and self._path_cfg_arg.exists():
            self._path_cfg = self._path_cfg_arg

        # else if def
        elif path_def and path_def.exists():
            self._path_cfg = path_def

    # --------------------------------------------------------------------------
    # Load config data from a file
    # --------------------------------------------------------------------------
    def _load_config(self):
        """
        Load config data from a file

        This method loads data from a config file. It is written to load a dict
        from a json file, but it can be used for other formats as well. It uses
        the values of self._dict_cfg and self._path_cfg to load the config
        data.
        """

        # if one or the other, load it
        if self._path_cfg and self._path_cfg.exists():
            self._dict_cfg = F.load_dicts([self._path_cfg], self._dict_cfg)

        # throw in a debug test
        if self._debug:
            print("load cfg from:", self._dict_cfg)
            F.pp(self._dict_cfg, label="load cfg")

    # --------------------------------------------------------------------------
    # Save config data to a file
    # --------------------------------------------------------------------------
    def _save_config(self):
        """
        Save config data to a file

        This method saves the config data to the same file it was loaded from.
        It is written to save a dict to a json file, but it can be used for
        other formats as well. It uses the values of self._dict_cfg and
        self._path_cfg to save the config data.
        """

        # save dict to path
        if self._path_cfg:
            F.save_dict(self._dict_cfg, [self._path_cfg])

        # throw in a debug test
        if self._debug:
            print("save cfg to:", self._dict_cfg)
            F.pp(self._dict_cfg, label="save cfg")


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
