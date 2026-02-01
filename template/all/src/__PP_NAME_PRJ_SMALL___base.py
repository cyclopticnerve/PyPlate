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
from pathlib import Path
import sys

# cnlib imports
from cnlib import cnfunctions as F
from cnlib.cnformatter import CNFormatter

# ------------------------------------------------------------------------------
# local imports

# fudge the path to import conf stuff
# sys.path.append(str(P_DIR_PRJ))

# pylint: disable=wrong-import-position
# import conf.conf as C  # type: ignore
# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# project dir
P_DIR_PRJ = Path(__file__).parents[1].resolve()

# conf dir
P_DIR_CONF = P_DIR_PRJ / "__PP_DIR_CONF__"

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
    # NB: if true, only load first file found (cmdline, conf dir, internal)
    # if false, load all and combine (internal, conf dir, cmdline)
    B_LOAD_HIGH = False
    # NB: if true, only save to file found in load
    # if false, save to all
    B_SAVE_HIGH = False

    # --------------------------------------------------------------------------
    # strings

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
    # I18N: config file dest
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
        "\n"
        "__PP_NAME_PRJ_BIG__\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        "__PP_URL__/__PP_NAME_PRJ_BIG__"
    )

    # default format af log files
    S_LOG_FMT = "%(asctime)s [%(levelname)-7s] %(message)s"
    S_LOG_DATE_FMT = "%Y-%m-%d %I:%M:%S %p"

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

        # cfg stuff
        self._path_cfg_def = P_CFG_DEF
        self._dict_cfg = {}

        # log stuff
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename=P_LOG_DEF,
            level=logging.INFO,
            format=self.S_LOG_FMT,
            datefmt=self.S_LOG_DATE_FMT,
        )

        # cmd line stuff
        self._parser = argparse.ArgumentParser(
            formatter_class=CNFormatter,
            add_help=False,
            prog="__PP_NAME_PRJ_SMALL__",
        )

        # set arg defaults
        self._dict_args = {}
        self._cmd_debug = False
        self._path_cfg_arg = None

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
            print(self.S_ABOUT)
            print()

            # print usage and arg info and exit
            self._parser.print_help()
            print()
            sys.exit(0)

        # set self and lib debug
        self._cmd_debug = self._dict_args.get(
            self.S_ARG_DBG_DEST, self._cmd_debug
        )
        F.B_DEBUG = self._cmd_debug

        # punt to uninstall func
        if self._dict_args.get(self.S_ARG_UNINST_DEST, False):

            # uninstall and exit
            self._do_uninstall()

        # ----------------------------------------------------------------------
        # set props from args

        # set cfg path
        self._path_cfg_arg = self._dict_args.get(
            self.S_ARG_CFG_DEST, self._path_cfg_arg
        )

        # sanity checks
        if self._path_cfg_def:
            self._path_cfg_def = Path(self._path_cfg_def)
            if not self._path_cfg_def.is_absolute():
                # make abs rel to self
                self._path_cfg_def = P_DIR_PRJ / self._path_cfg_def

        # accept path or str
        if self._path_cfg_arg:
            self._path_cfg_arg = Path(self._path_cfg_arg)
            if not self._path_cfg_arg.is_absolute():
                # make abs rel to self
                self._path_cfg_arg = P_DIR_PRJ / self._path_cfg_arg

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
        location), and _path_cfg_arg (file passed on command line) to
        successively load the config data.
        """

        # paths of config files
        l_paths = [self._path_cfg_arg, self._path_cfg_def]

        # ----------------------------------------------------------------------
        # load from highest order only
        if self.B_LOAD_HIGH:

            # order of saving (highest to lowest)
            for a_path in l_paths:

                # check if valid file (already resolved)
                if a_path and a_path.exists():

                    # set whole dict to file
                    try:
                        self._dict_cfg = F.load_paths_into_dict(
                            a_path, self._dict_cfg
                        )

                        # if we get here, we have loaded the highest file
                        return
                    except OSError as e:  # from load_dicts
                        F.printd(self.S_ERR_ERR, str(e))

                else:

                    # file does not exist, fall through
                    F.printd(
                        self.S_ERR_ERR,
                        self.S_ERR_NO_CFG.format(a_path),
                    )

        # ----------------------------------------------------------------------
        # load from both
        else:

            try:
                self._dict_cfg = F.load_paths_into_dict(
                    l_paths, self._dict_cfg
                )
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
        _path_cfg_arg to save the config data.
        """

        # paths of config files
        l_paths = [self._path_cfg_arg, self._path_cfg_def]

        # ----------------------------------------------------------------------
        # check class flag
        if self.B_SAVE_HIGH:

            # order of saving (highest to lowest)
            for a_path in l_paths:

                # set whole file to dict
                try:
                    F.save_dict_into_paths(self._dict_cfg, a_path)

                    # if we get here, we have saved the file
                    return
                except OSError as e:  # from save_dict
                    F.printd(self.S_ERR_ERR, str(e))

        # ----------------------------------------------------------------------
        # save to both
        else:

            try:
                F.save_dict_into_paths(self._dict_cfg, l_paths)
            except OSError as e:  # from save_dict
                F.printd(self.S_ERR_ERR, str(e))

    # --------------------------------------------------------------------------
    # Handle the --uninstall cmd line op
    # --------------------------------------------------------------------------
    def _do_uninstall(self):
        """
        Handle the --uninstall cmd line op
        """

        # ask to uninstall
        str_ask = F.dialog(
            self.S_ASK_UNINST.format("__PP_NAME_PRJ_BIG__"),
            [F.S_ASK_YES, F.S_ASK_NO],
            F.S_ASK_NO,
        )

        # user hit enter or typed "n/N"
        if str_ask != F.S_ASK_YES:
            print(self.S_MSG_ABORT)
            sys.exit(0)

        # ----------------------------------------------------------------------

        # if path exists
        path_uninst = P_UNINST
        if not path_uninst.exists():
            path_uninst = P_UNINST_DIST

        # format cmd line
        cmd = str(path_uninst) + " -f -q"
        if self._cmd_debug:
            cmd += " -d"

        # ----------------------------------------------------------------------

        try:
            F.run(cmd, shell=True)
            sys.exit(0)
        except F.CNRunError as e:
            print(e.output)
            sys.exit(e.returncode)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line
    print("WRONG GLASS, SIR !!!")

# -)
