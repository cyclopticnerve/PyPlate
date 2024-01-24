# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: cli_config.py                                         |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
This module provides config file support to __PP_NAME_SMALL__
It mostly moves boilerplate code for config files out of the the main cli file
The G_DICT_CONFIG dictionary can be loaded from:
1. the file passed to the command line using the S_CFG_OPTION or
S_CFG_OPTION_LONG strings
2. the file set in the PATH_CONFIG_DEF constant
If neither of the above files are valid, the G_DICT_CONFIG dictionary will
remain unchanged.

Do not comment out any constants/globals/strings in this file. If you don not
wish to use one of them, set it's value to "" or None.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import json
from pathlib import Path

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# the key in args for the config file (shown in help)
ARG_KEY_PATH_CONFIG = "PATH_CONFIG"

# the path to the default config file
# NB: the underscore hides my home path from docs
# NB: uncomment this if you want to use config files to set defaults for
# command line options
PATH_CONFIG_DEF = (
    ""  # Path.home() / ".config" / "__PP_NAME_BIG__" / "config.json"
)

# if True, show file load/save errors
# else show nothing
SHOW_ERRORS = False

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the global config dict (built-in or loaded from config file)
# it is set once in load_config()
# order of precedence is:
# 1. command line flag -c
# 2. file at _PATH_CONFIG_DEF
# 3. this definition
# when the app quits, the config dict is saved to a file in this order:
# 1. command line flag -c
# 2. file at _PATH_CONFIG_DEF
# 3. none
G_DICT_CONFIG = {}

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# string constants
S_CFG_OPTION = "-c"
S_CFG_OPTION_LONG = "--config-file"
S_CFG_METAVAR = "FILE"
S_CFG_HELP = "load configuration from file"
S_CFG_ERR_EXIST = "load config: config file '{}' does not exist"
S_CFG_ERR_VALID = "load config: config file '{}' is not a valid JSON file"
S_CFG_ERR_CREATE = "save config: config file '{}' could not be created"

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Adds command line args to the parser
# ------------------------------------------------------------------------------
def add_args(argparser):
    """
    Adds command line args to the parser

    Arguments:
        argparser: The argparse object to add args to

    This function adds arguments to the parser. IT SHOULD NEVER BE CALLED IN
    CODE! It is teased out to make editing command line arguments easier.
    """

    # NB: https://docs.python.org/3/library/argparse.html
    if S_CFG_OPTION_LONG == "":
        # do only short option
        argparser.add_argument(
            S_CFG_OPTION,
            dest=ARG_KEY_PATH_CONFIG,
            help=S_CFG_HELP,
            metavar=S_CFG_METAVAR,
        )
    else:
        # do short and long option
        argparser.add_argument(
            S_CFG_OPTION,
            S_CFG_OPTION_LONG,
            dest=ARG_KEY_PATH_CONFIG,
            help=S_CFG_HELP,
            metavar=S_CFG_METAVAR,
        )


# ------------------------------------------------------------------------------
# Loads config file from first found path, or use built-in
# ------------------------------------------------------------------------------
def load_config(args):
    """
    Loads config file from first found path, or use built-in

    Arguments:
        args: The dictionary of parsed arguments from the calling cli module

    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not a valid JSON file

    Load the global config from a file at the found location.
    Order of precedence is:
    1. The file passed to the command-line using the S_CFG_OPTION or
    S_CFG_OPTION_LONG strings
    2. The file set in the PATH_CONFIG_DEF constant
    If neither of the above files are valid, the G_DICT_CONFIG dictionary will
    remain unchanged.
    """

    # the global dict to set
    global G_DICT_CONFIG  # pylint: disable=global-statement

    for item in [args[ARG_KEY_PATH_CONFIG], PATH_CONFIG_DEF]:
        # try each option
        try:
            # sanity check
            if item is not None and item != "":
                # get value of cmdline arg
                item = Path(item)

                # make sure path is absolute
                if not item.is_absolute:
                    if SHOW_ERRORS:
                        print(S_CFG_ERR_EXIST.format(item))
                    continue

                # open the file
                with open(item, "r", encoding="UTF-8") as a_file:
                    # load dict from file
                    G_DICT_CONFIG = json.load(a_file)

                    # yay!
                    return

        # file not found
        except FileNotFoundError:
            if SHOW_ERRORS:
                print(S_CFG_ERR_EXIST.format(item))

        # file mot JSON
        except json.JSONDecodeError:
            if SHOW_ERRORS:
                print(S_CFG_ERR_VALID.format(item))


# ------------------------------------------------------------------------------
# aves config file to first found path
# ------------------------------------------------------------------------------
def save_config(args):
    """
    Saves config file to first found path

    Arguments:
        args: The dictionary of parsed arguments from the calling cli module

    Raises:
        Exception: If the file does not exist and can't be created

    Save the global config to a file at the found location.
    Order of precedence is:
    1. The file passed to the command-line using the S_CFG_OPTION or
    S_CFG_OPTION_LONG strings
    2. The file set in the PATH_CONFIG_DEF constant
    If neither of the above files are valid, the G_DICT_CONFIG dictionary will
    be lost.
    """

    for item in [args[ARG_KEY_PATH_CONFIG], PATH_CONFIG_DEF]:
        # try each option
        try:
            # sanity check
            if item is not None and item != "":
                # get value of cmdline arg
                item = Path(item)

                # make sure path is absolute
                if not item.is_absolute():
                    if SHOW_ERRORS:
                        print(S_CFG_ERR_CREATE.format(item))
                    continue

                # first make dirs
                item.parent.mkdir(parents=True, exist_ok=True)

                # open the file
                with open(item, "w", encoding="UTF-8") as a_file:
                    # save dict tp file
                    json.dump(G_DICT_CONFIG, a_file, indent=4)

                    # yay!
                    return
        except OSError:
            if SHOW_ERRORS:
                print(S_CFG_ERR_CREATE.format(item))


# -)
