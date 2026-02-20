# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_PRJ_SMALL___base.py                         |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The base file for a cli or gui program

This file contains all the boring boilerplate code for making a robust CLI/GUI
application. It is not intended to be run directly, but rather subclassed. The
subclass should contain, at minimum, the main method and the top-level run code
(examples are given in the cli/src and gui/src subdirectories of the template
directory).
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

# cnlib imports
from cnlib import cnfunctions as F
from cnlib.cnformatter import CNFormatter

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# project dir
P_DIR_PRJ = Path(__file__).parents[1].resolve()

# conf dir
P_DIR_CONF = P_DIR_PRJ / "__PP_DIR_CONF__"
P_DIR_LOG = P_DIR_PRJ / "__PP_DIR_LOG__"

# path to default config file
# NB: if not using, set to None
P_CFG_DEF = P_DIR_CONF / "__PP_NAME_PRJ_SMALL__.json"

# path to default log file
# NB: if not using, set to None
P_LOG_DEF = P_DIR_PRJ / "__PP_DIR_LOG__/__PP_NAME_PRJ_SMALL__.log"

# path to uninst
P_UNINST = P_DIR_PRJ / "__PP_DIR_INSTALL__/__PP_NAME_UNINST__"
# NB: path changes after dist
P_UNINST_DIST = P_DIR_PRJ / "__PP_NAME_UNINST__"

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

DIR_LOCALE = P_DIR_PRJ / "__PP_PATH_LOCALE__"
_ = F.get_underscore("__PP_NAME_PRJ_SMALL__", DIR_LOCALE)

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class __PP_NAME_PRJ_PASCAL__Base:
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

    # --------------------------------------------------------------------------
    # bools

    # set load/save oder
    # NB: if true, only load from first file found, in this order:
    # 1. cmdline (-c)
    # 2. conf dir (P_CFG_DEF)
    # 3. internal (self._dict_cfg)
    # if false, load all and combine in this order:
    # 1. internal
    # 2. conf dir
    # 3. cmdline
    B_LOAD_FIRST = False
    # NB: if true, only save to first file found, in this order:
    # 1. cmdline (-c)
    # 2. conf dir (P_CFG_DEF)
    # if false, save to all
    B_SAVE_FIRST = False

    # --------------------------------------------------------------------------
    # ints

    # rotating log stuff
    I_LOG_SIZE = 2097152  # max log file size in bytes (2 Mb)
    I_LOG_COUNT = 5  # max number of log files

    # --------------------------------------------------------------------------
    # strings

    # NB: used for logger
    S_APP_NAME = "__PP_NAME_PRJ_SMALL__"

    # short description
    # pylint: disable=line-too-long
    # NB: need to keep on one line for replacement
    S_PP_SHORT_DESC = ""
    # pylint: enable=line-too-long

    # version string
    S_PP_VERSION = ""

    # config option strings
    S_ARG_CFG_OPTION = "-c"
    S_ARG_CFG_DEST = "CFG_DEST"
    # I18N: config file option help
    S_ARG_CFG_HELP = _("load configuration from file")
    # I18N: config file dest (indicate it should be a file name/path)
    S_ARG_CFG_METAVAR = _("FILE")

    # debug option strings
    S_ARG_DBG_OPTION = "-d"
    S_ARG_DBG_ACTION = "store_true"
    S_ARG_DBG_DEST = "DBG_DEST"
    # I18N: debug mode help
    S_ARG_DBG_HELP = _("enable debugging mode")

    # config option strings
    S_ARG_HLP_OPTION = "-h"
    S_ARG_HLP_ACTION = "store_true"
    S_ARG_HLP_DEST = "HLP_DEST"
    # I18N: help option help
    S_ARG_HLP_HELP = _("show this help message and exit")

    # config option strings
    S_ARG_UNINST_OPTION = "--uninstall"
    S_ARG_UNINST_ACTION = "store_true"
    S_ARG_UNINST_DEST = "UNINST_DEST"
    # I18N: uninstall option help
    S_ARG_UNINST_HELP = _("uninstall this program")

    # about string
    S_ABOUT = (
        "__PP_NAME_PRJ_BIG__\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        "__PP_URL__/__PP_NAME_PRJ_BIG__"
    )

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help")

    # default format for log files
    S_LOG_FMT = "%(asctime)s [%(levelname)-7s] %(message)s"
    S_LOG_DATE_FMT = "%Y-%m-%d %I:%M:%S"

    # --------------------------------------------------------------------------
    # questions

    # I18N: answer yes
    S_ASK_YES = _("y")
    # I18N: answer no
    S_ASK_NO = _("N")
    # NB: format param is prog name
    # I18N: ask to uninstall
    S_ASK_UNINST = _("This will uninstall {}.\nDo you want to continue?")

    # --------------------------------------------------------------------------
    # messages

    # I18N: process aborted
    S_MSG_ABORT = _("Aborted")

    # --------------------------------------------------------------------------
    # error messages

    # I18N: an error occurred
    S_ERR_ERR = _("Error:")
    # I18N: uninstall not found
    S_ERR_NO_UNINST = _("Uninstall files not found")
    # NB: format param is file path
    # I18N: could not find -c file
    S_ERR_NO_CFG = _("Config file {} not found")

    # --------------------------------------------------------------------------
    # Instance methods
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

        # args and arg props
        self._dict_args = {}
        self._arg_cfg = None
        self._arg_debug = False

        # cfg stuff
        self._dict_cfg = {}
        self._path_cfg_def = P_CFG_DEF

        # ----------------------------------------------------------------------

        # make some folders
        if not P_DIR_CONF.exists():
            Path.mkdir(P_DIR_CONF)
        if not P_DIR_LOG.exists():
            Path.mkdir(P_DIR_LOG)

        # make a rotating handler
        handler = RotatingFileHandler(
            str(P_LOG_DEF),
            maxBytes=self.I_LOG_SIZE,
            backupCount=self.I_LOG_COUNT,
        )

        # add a formatter to rot handler
        formatter = logging.Formatter(
            self.S_LOG_FMT, datefmt=self.S_LOG_DATE_FMT
        )

        # set formatter to handler
        handler.setFormatter(formatter)

        # create logger and add rot handler
        self._logger = logging.getLogger(self.S_APP_NAME)
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(handler)

        # ----------------------------------------------------------------------

        # cmd line stuff
        self._parser = argparse.ArgumentParser(
            formatter_class=CNFormatter, add_help=False, prog=self.S_APP_NAME
        )

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # NB: these are the main steps, called in order from main()

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    def _setup(self):
        """
        Boilerplate to use at the start of main

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """

        # ----------------------------------------------------------------------
        # use cmd line

        # always add help option
        self._parser.add_argument(
            self.S_ARG_HLP_OPTION,
            action=self.S_ARG_HLP_ACTION,
            dest=self.S_ARG_HLP_DEST,
            help=self.S_ARG_HLP_HELP,
        )

        # add uninstall option
        self._parser.add_argument(
            self.S_ARG_UNINST_OPTION,
            action=self.S_ARG_UNINST_ACTION,
            dest=self.S_ARG_UNINST_DEST,
            help=self.S_ARG_UNINST_HELP,
        )

        # run the parser
        args = self._parser.parse_args()

        # convert namespace to dict
        self._dict_args = vars(args)

        # ----------------------------------------------------------------------
        # check for one-shot args

        # if -h passed, this will print and exit
        if self._dict_args.get(self.S_ARG_HLP_DEST, False):

            # print default about text
            print()
            print(self.S_ABOUT)
            print()

            # print usage and arg info and exit
            self._parser.print_help()
            print()
            sys.exit(0)

        # ----------------------------------------------------------------------
        # check for -d (debug)

        # set self and lib debug
        self._arg_debug = self._dict_args.get(
            self.S_ARG_DBG_DEST, self._arg_debug
        )
        F.B_DEBUG = self._arg_debug

        # ----------------------------------------------------------------------
        # check for --uninstall

        # punt to uninstall func
        if self._dict_args.get(self.S_ARG_UNINST_DEST, False):

            # uninstall and exit
            self._do_uninstall()
            # NB: exit is handled by _do_uninstall

        # ----------------------------------------------------------------------
        # set props from args

        # set cfg path
        self._arg_cfg = self._dict_args.get(self.S_ARG_CFG_DEST, self._arg_cfg)

        # sanity checks
        if self._path_cfg_def:
            self._path_cfg_def = Path(self._path_cfg_def)
            if not self._path_cfg_def.is_absolute():
                # make abs rel to self
                self._path_cfg_def = P_DIR_PRJ / self._path_cfg_def

        # accept path or str
        if self._arg_cfg:
            self._arg_cfg = Path(self._arg_cfg)
            if not self._arg_cfg.is_absolute():
                # make abs rel to self
                self._arg_cfg = P_DIR_PRJ / self._arg_cfg

        # ----------------------------------------------------------------------
        # use cfg
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
    # Load config data from a file
    # --------------------------------------------------------------------------
    def _load_config(self):
        """
        Load config data from a file

        This method loads data from a config file. It is written to load a dict
        from a json file, but it can be used for other formats as well. It uses
        the values of _dict_cfg (hard-coded), P_CFG_DEF (the default file
        location), and _arg_cfg (file passed on command line) to
        successively load the config data.
        """

        # paths of config files
        l_paths = [self._arg_cfg, self._path_cfg_def]

        for a_path in l_paths:

            # set whole dict to file
            try:
                self._dict_cfg = F.load_paths_into_dict(a_path, self._dict_cfg)

                # stop after first found
                if self.B_LOAD_FIRST:
                    break
            except OSError as e:  # from load_dicts
                F.printd(self.S_ERR_ERR, str(e))

    # --------------------------------------------------------------------------
    # Save config data to a file
    # --------------------------------------------------------------------------
    def _save_config(self):
        """
        Save config data to a file

        This method saves the config data to all the files it can create. It is
        written to save a dict to a json file, but it can be used for other
        formats as well. It uses the values of _dict_cfg, _path_cfg_def, and
        _arg_cfg to save the config data.
        """

        # paths of config files
        l_paths = [self._arg_cfg, self._path_cfg_def]

        # order of saving (highest to lowest)
        for a_path in l_paths:

            # set whole file to dict
            try:
                F.save_dict_into_paths(self._dict_cfg, a_path)

                # stop after first found
                if self.B_SAVE_FIRST:
                    break
            except OSError as e:  # from save_dict
                F.printd(self.S_ERR_ERR, str(e))

    # --------------------------------------------------------------------------
    # Handle the --uninstall cmd line op
    # --------------------------------------------------------------------------
    def _do_uninstall(self):
        """
        Handle the --uninstall cmd line op
        """

        # print some text
        print(self.S_ABOUT)
        print()

        # ask to uninstall
        str_ask = F.dialog(
            self.S_ASK_UNINST.format("SpaceOddity"),
            [F.S_ASK_YES, F.S_ASK_NO],
            F.S_ASK_NO,
        )

        # user hit enter or typed "n/N"
        if str_ask != F.S_ASK_YES:
            print()
            print(self.S_MSG_ABORT)
            print()
            sys.exit(0)

        # ----------------------------------------------------------------------

        # if path exists
        path_uninst = P_UNINST

        # try for install loc's uninstall
        if not path_uninst.exists():
            path_uninst = P_UNINST_DIST

            # still not found? error
            if not path_uninst.exists():
                print(self.S_ERR_NO_UNINST)
                print()
                sys.exit(-1)

        # format cmd line
        cmd = str(path_uninst) + " -f -q"
        if self._arg_debug:
            cmd += " -d"

        # ----------------------------------------------------------------------

        try:
            F.run(cmd, shell=True)
            print()
            sys.exit(0)
        except F.CNRunError as e:
            print(e.output)
            print()
            sys.exit(e.returncode)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line
    print("WRONG GLASS, SIR !!!")

# -)
