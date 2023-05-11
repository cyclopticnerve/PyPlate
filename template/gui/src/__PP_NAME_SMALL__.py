#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__.py                                  |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import argparse
import os
import sys

# this is the dir where the script is being run from
# # (e.g. ~/Documents/Projects/Python/Apps/__PP_NAME_BIG__)
dir_curr = os.path.dirname(__file__)

# this is the dir where the gui files are located relative to the script
# (e.g. ~/Documents/Projects/Python/Apps/__PP_NAME_BIG__/gui)
dir_gui = os.path.join(dir_curr, 'gui')

# add gui path to sys path to import handler
sys.path.insert(0, dir_gui)

import __PP_NAME_BIG__Handler as handler  # noqa: E402 (import not at top of file)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------


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

    # NB: uncomment this line and add args to _add_args()
    # args = _parse_args()

    # show the window
    __PP_NAME_SMALL__App = __PP_NAME_BIG__handler.__PP_NAME_BIG__App()  # noqa: E602 (undefined name)
    __PP_NAME_SMALL__App.run()


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
def func():
    """
        Short description

        Parameters:
            var_name [type]: description

        Returns:
            [type]: description

        Raises:
            exception_type(vars): description

        Long description (including HTML).
    """

    return ('this is a test')


# ------------------------------------------------------------------------------
# Add command line args to the parser
# ------------------------------------------------------------------------------
def add_args(argparser):
    """
        Add command line args to the parser

        Parameters:
            argparser [ArgumentParser]: the argparse object to add args to

        This function adds arguments to the parser. It is teased out to make
        editing command line parameters easier.
    """

    # https://docs.python.org/3/library/argparse.html

    # argparser.add_argument('-f')


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Parse command line args and return the dict
# ------------------------------------------------------------------------------
def _parse_args():
    """
        Parse command line args and return the dict

        Returns:
            [dict]: the dict of commands passed on the command line

        This function gets the command line passed to the program, parses it,
        and returns the command line options as a dict.
    """

    # create the parser
    argparser = argparse.ArgumentParser(
        description='PP_SHORT_DESC'
    )

    # always print prog name/version
    print('__PP_NAME_BIG__ version PP_VERSION')

    # add arguments from the function above
    add_args(argparser)

    # parse the arg list into a Namespace object (similar to dict)
    # NB: if there is an error in the command line, this function will:
    # 1. print usage
    # 2. print the error
    # 3. exit
    args = argparser.parse_args()

    # if we made it this far, cmd line is ok so print usage
    argparser.print_usage()

    # convert agrs to dict
    dict_args = vars(args)

    # return the object for inspection
    return dict_args


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.
    """

    # run main function
    main()

# -)
