#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: default_cli.py                                        |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
docstring
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse

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

    # call the steps in order
    print(func())


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

    # NB: https://docs.python.org/3/library/argparse.html
    # argparser.add_argument('-f')
    pass


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

    # the global dict of arguments
    global G_DICT_ARGS

    # create the parser
    argparser = argparse.ArgumentParser(description="__PP_SHORT_DESC__",)

    # add version argument
    argparser.add_argument(
        "-v",
        "--version",
        action="version",
        version="__PP_VERSION__",
    )

    # add arguments from the function above
    add_args(argparser)

    # parse the arg list into a Namespace object (similar to dict)
    # NB: if there is an error in the command line, this function will:
    # 1. print usage
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
