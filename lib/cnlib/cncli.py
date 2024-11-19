# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cncli.py                                              |     ()     |
# Date    : 04/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This is the base class for a CLI program. The template CLI program subclasses
it. See PyPlate/template/cli/src/__PP_NAME_SMALL__ for an example.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
from cnlib import cnformatter  # type: ignore
from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class CNCli:
    """
    The main class, responsible for the operation of the program

    Properties:

    Methods:

    This object does the most of the work of a typical CLI program. It parses
    command line options, loads/saves config files, and performs the operations
    required for the program.
    """

    # config option strings
    ARG_CFG_OPTION = "-c"
    ARG_CFG_DEST = "CFG_DEST"
    ARG_CFG_HELP = "load configuration from file"
    ARG_CFG_METAVAR = "FILE"

    # debug option strings
    ARG_DBG_OPTION = "-d"
    ARG_DBG_ACTION = "store_true"
    ARG_DBG_DEST = "DBG_DEST"
    ARG_DBG_HELP = "enable debugging option"

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
        self._dict_args = {}
        self._debug = False

        self._dict_cfg = {}
        # self._path_arg = None
        self._path_cfg = None

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Set up and run the command line parser
    # --------------------------------------------------------------------------
    def _run_parser(self):
        """
        Set up and run the command line parser

        This method sets up and runs the command line parser to minimize code
        in the subclass. It calls the subclass to add it's arguments, then it
        parses the command line and returns a dictionary.
        """

        # create the command line parser
        parser = argparse.ArgumentParser(
            formatter_class=cnformatter.CNFormatter
        )

        # call the subclass method
        self._add_args(parser)

        # get namespace object
        args = parser.parse_args()

        # convert namespace to dict
        self._dict_args = vars(args)

    # --------------------------------------------------------------------------
    # This method does nothing, it is for subclassing
    # --------------------------------------------------------------------------
    def _add_args(self, parser):
        """
        This method does nothing, it is for subclassing

        Arguments:
            parser: The ArgumentParser to add the args to

        This method is empty, but is declared here because the subclass method
        is called from _run_parser.
        """

        # dummy method to be subclassed

    # --------------------------------------------------------------------------
    # Load config dict by combining several json files
    # --------------------------------------------------------------------------
    def _load_config(self, path_arg=None, path_def=None):
        """
        Load config dict by combining several json files

        Arguments:
            path_arg: The path to a config file passed on the command line
            (default: None)
            path_def: The path to the existing config file (the one the program
            usually uses) (default: None)

        This method loads config files from several sources, and combines the
        resulting dictionaries. The order of precedence is:
        3. dict_def
        1. path_arg
        2. path_def
        """

        # load config dict from arg file, def file, or just keep built-in
        # Order of precedence is:
        # 1. The file passed to the command-line, cfg_arg, as a string
        # 2. The file set in cfg_def, the default file location
        # If neither of the above files are valid, the self._d_cfg dictionary
        # will remain unchanged.

        #  arg set | arg exist | def exist | load  | save
        # =================================================
        #     0    |     X     |     0     |   0   | P_CFG
        #     0    |     X     |     1     | P_CFG | P_CFG
        #     0    |     X     |     0     |   0   | P_CFG
        #     0    |     X     |     1     | P_CFG | P_CFG
        # -------------------------------------------------
        #     1    |     0     |     0     |   0   |  arg
        #     1    |     0     |     1     | P_CFG |  arg
        #     1    |     1     |     0     |  arg  |  arg
        #     1    |     1     |     1     | both? |  arg

        # set some defaults
        # p_arg = None
        # arg_exists = False
        # p_def = None
        # def_exists = False
        # paths_load = []

        has_arg = path_arg is not None and path_arg.exists()
        has_def = path_def is not None and path_def.exists()

        # get the flags for the truth table
        # arg_set = path_arg is not None
        # if arg_set:
        #     p_arg = Path(path_arg)
        #     arg_exists = p_arg.exists()
        # def_set = path_def is not None
        # if def_set:
        #     p_def = Path(path_def)
        #     def_exists = p_def.exists()

        # NB: we go from bottom up to avoid having to "not" everything

        comb = []
        if has_arg:
            comb.append(path_arg)
        if has_def:
            comb.append(path_def)

        # there is an arg file
        # if arg_set:
        #     # set the path to save
        #     self._arg_cfg = p_arg
        #     # we got an arg
        #     if arg_exists:
        #         if def_exists:
        #             # load both
        #             paths_load = [p_def, p_arg]  # 1 1 1
        #         else:
        #             # just load arg
        #             paths_load = [p_arg]  # 1 1 0
        #     else:
        #         if def_exists:
        #             # load def only
        #             paths_load = [p_def]  # 1 0 1
        #         else:
        #             # load nothing
        #             paths_load = []  # 1 0 0
        # # there is no arg file
        # else:
        #     # set the path to save
        #     self._arg_cfg = p_def
        #     if def_exists:
        #         # load def only
        #         paths_load = [p_def]  # 0 X 1
        #     else:
        #         # load nothing
        #         paths_load = []  # 0 X 0

        # load dict from path(s)
        # NB: paths_load is a list, no brackets
        self._dict_cfg = F.load_dicts(comb, self._dict_cfg)

    # --------------------------------------------------------------------------
    # Save config file to one of several sources
    # --------------------------------------------------------------------------
    def _save_config(self):
        """
        Save config file to a file

        This method saves the config dict to the same file it was loaded from.
        """

        # save config dict to file, def, or just lose
        # this saves _dict_cfg to whatever path we determined in _load_config

        # save dict to path
        if self._path_cfg is not None:
            F.save_dict(self._dict_cfg, [self._path_cfg])


# -)
