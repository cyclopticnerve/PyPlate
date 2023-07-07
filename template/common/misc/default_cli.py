#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: default_cli.py                                        |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE__                                         \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import argparse
import os

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_FILE = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

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

    # call the steps in order
    print(func())


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
def func():
    """
        Short description

        Parameters:
            var_name: Description

        Returns:
            Description

        Raises:
            exception_type(vars): Description

        Long description (including HTML).
    """

    return ('this is a test')


# ------------------------------------------------------------------------------
# Add command line args to the parser
# ------------------------------------------------------------------------------
def add_args(argparser):
    """
        Adds command line args to the parser

        Parameters:
            argparser: The argparse object to add args to

        This function adds arguments to the parser. It is teased out to make
        editing command line parameters easier.
    """

    # https://docs.python.org/3/library/argparse.html

    # argparser.add_argument('-f')
    pass

# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Parse command line args and return the dict
# ------------------------------------------------------------------------------


def _parse_args():
    """
        Parses command line args and return the dict

        Returns:
            The dict of commands passed on the command line

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
