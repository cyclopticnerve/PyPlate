#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__.py                                  |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
This module provides the main interface to __PP_NAME_SMALL__
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from argparse import RawDescriptionHelpFormatter
from argparse import RawTextHelpFormatter

# local imports
# NB: uncomment this if you want to use config files to set defaults for command
# line options
# import cli_config as cfg

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# args are global so we can read them from any function
# they are only set once, in _parse_args
G_DICT_ARGS = {}

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# string constants
S_VERSION_DESC = (
    "__PP_NAME_SMALL__\n"
    "__PP_SHORT_DESC__\n"
    "__PP_VERSION__\n"
    "__PP_EMAIL__"
)

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main function of the program
# ------------------------------------------------------------------------------
def main():
    """
    The main function of the program

    This function is the main entry point for the program, initializing the
    program, and performing its steps.
    """

    # load config dict from file (or just keep built-in)
    # NB: uncomment this if you want to use config files to set defaults for
    # command line options
    # cfg.load_config(G_DICT_ARGS)

    # call the steps in order
    print(func())

    # save config dict to file
    # NB: uncomment this if you want to use config files to set defaults for
    # command line options
    # cfg.save_config(G_DICT_ARGS)

# ------------------------------------------------------------------------------
# Adds command line args to the parser
# ------------------------------------------------------------------------------
def add_args(argparser):
    """
    Adds command line args to the parser

    Arguments:
        argparser: The argparse object to add args to

    This function adds arguments to the parser. IT SHOULD NEVER BE CALLED IN
    CODE! It is teased out to make editing command line parameters easier.
    """

    # NB: uncomment this if you want to use config files to set defaults for
    # command line options
    # cfg.add_args(argparser)

    # add your command line options here
    # NB: https://docs.python.org/3/library/argparse.html
    # argparser.add_argument('-f')


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
def func():
    """
    Short description

    Arguments:
        var_name: Description

    Returns:
        Description

    Raises:
        exception_type(vars): Description

    Long description (including HTML).
    """

    return "this is func"


# ------------------------------------------------------------------------------
# Private classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A dummy class to combine multiple argparse formatters
# ------------------------------------------------------------------------------
class _MyFormatter(RawTextHelpFormatter, RawDescriptionHelpFormatter):
    """
    A dummy class to combine multiple argparse formatters

    Arguments:
        RawTextHelpFormatter: Maintains whitespace for all sorts of help text,
        including argument descriptions.
        RawDescriptionHelpFormatter: Indicates that description and epilog are
        already correctly formatted and should not be line-wrapped.

    A dummy class to combine multiple argparse formatters.
    """


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Parses command line args and sets the global dict
# ------------------------------------------------------------------------------
def _parse_args():
    """
    Parses command line args and sets the global dict

    This function gets the command line passed to the program, parses it,
    and sets the command line options as a global dict.
    """

    # the global dict of command line arguments
    global G_DICT_ARGS  # pylint: disable=global-statement

    # create the parser
    argparser = argparse.ArgumentParser(
        description=S_VERSION_DESC,
        formatter_class=_MyFormatter,
    )

    # add version argument
    argparser.add_argument(
        "-v",
        "--version",
        action="version",
        version=S_VERSION_DESC,
    )

    # add arguments from the function above
    add_args(argparser)

    # parse the arg list into a Namespace object (similar to dict)
    # NB: if there is an error in the command line, this function will:
    # 1. print simple usage
    # 2. print the error
    # 3. exit
    args = argparser.parse_args()

    # convert args to global dict
    G_DICT_ARGS = vars(args)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # get command-line args and set them to the global dict
    _parse_args()

    # run main function
    main()

# -)
