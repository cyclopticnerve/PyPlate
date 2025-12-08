# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cncli.py                                              |     ()     |
# Date    : 04/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This is the base class for a CLI program. The template CLI and GUI programs
subclass it.

See PyPlate/template/cli/src/pyplate.py for an example.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from pathlib import Path

# cnlib imports
import cnfunctions as F
from cnformatter import CNFormatter

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

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

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
        self._dict_args = {}

        self._debug = False
        self._path_cfg = None

        self._dict_cfg = {}
        # self._path_cfg_arg = None

        # create a parser object in case we need it
        self._parser = argparse.ArgumentParser(formatter_class=CNFormatter)


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

    # get namespace object
    args = self._parser.parse_args()

    # convert namespace to dict
    self._dict_args = vars(args)

    # set debug if flag is present, else leave init default
    self._debug = self._dict_args.get(self.S_ARG_DBG_DEST, self._debug)

    # set cfg path if flag is present, else leave init default
    cfg_arg = self._dict_args.get(self.S_ARG_CFG_DEST, self._path_cfg_arg)

    # try to make cfg_arg a Path (always a string/None coming from dict)
    if cfg_arg:
        self._path_cfg_arg = Path(cfg_arg)

    # --------------------------------------------------------------------------
    # Load config dict from a json file
    # --------------------------------------------------------------------------
    def _load_config(self, path_cli, path_arg=None, path_def=None):
        """
        Load config dict from a json file

        Args:
            path_cli: The path to the subclass cli, for relative paths
            path_arg: The path to the configuration file supplied via the -c
            option (default: None)
            path_def: The path to the default config file (default: None)

        This method loads the config dict from either:
        1. the command line -c option (if present)
        or
        2. the path_def argument (if present)

        If you use the -c option, and the file exists, it will be combined with
        the existing _dict_cfg property, and processing stops.
        If you do not use the -c option, or it is not present on the command
        line, the path_def value will be used.
        If you use neither, nothing happens to the _dict_cfg property.
        """

        # accept path or str
        path_cli = Path(path_cli)

        # accept path or str
        if path_def:
            path_def = Path(path_def)
            if not path_def.is_absolute():
                # make abs rel to subclass
                path_def = path_cli / path_def

        # accept path or str
        if self._path_cfg_arg:
            self._path_cfg_arg = Path(self._path_cfg_arg)
            if not self._path_cfg_arg.is_absolute():
                # make abs rel to subclass
                self._path_cfg_arg = path_cli / self._path_cfg_arg

        # ----------------------------------------------------------------------

        # if cmd line
        if self._path_cfg_arg and self._path_cfg_arg.exists():
            self._path_cfg = self._path_cfg_arg

        # else if def
        elif path_def and path_def.exists():
            self._path_cfg = path_def

        # ----------------------------------------------------------------------

        # if one or the other, load it
        if self._path_cfg and self._path_cfg.exists():
            self._dict_cfg = F.load_paths_into_dict(
                [self._path_cfg], self._dict_cfg
            )

        # add a debug message
        if self._debug:
            print("load cfg from:", self._path_cfg)
            F.pp(self._dict_cfg, label="cfg")

    # --------------------------------------------------------------------------
    # Save config file to one of several sources
    # --------------------------------------------------------------------------
    def _save_config(self):
        """
        Save config file to a file

        This method saves the config dict to the same file it was loaded from.
        """

        # save dict to path
        if self._path_cfg:
            F.save_dict_into_paths(self._dict_cfg, [self._path_cfg])

        # add a debug message
        if self._debug:
            print("save cfg to:", self._path_cfg)
            F.pp(self._dict_cfg, label="cfg")


# -)
