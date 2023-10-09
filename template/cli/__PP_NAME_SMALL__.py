#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__.py                                  |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
import os

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_SELF = os.path.dirname(__file__)

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# args are global so we can read them from any function
# they are only set once, in __name__()
g_dict_args = {}

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------

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

    return ('this is func')

# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# The main function of the program
# ------------------------------------------------------------------------------
def _main():
    """
        The main function of the program

        This function is the main entry point for the program, initializing the
        program, and performing its steps.
    """

    # get command-line args and set them to the global dict
    _parse_args()

    # call the steps in order
    print(func())

# ------------------------------------------------------------------------------
# Adds command line args to the parser
# ------------------------------------------------------------------------------
def _add_args(argparser):
    """
        Adds command line args to the parser

        Parameters:
            argparser: The argparse object to add args to

        This function adds arguments to the parser. IT SHOULD NEVER BE CALLED IN
        CODE! It is teased out to make editing command line parameters easier.
    """

    # NB: https://docs.python.org/3/library/argparse.html
    # argparser.add_argument('-f')
    pass

# ------------------------------------------------------------------------------
# Parses command line args and set the global dict
# ------------------------------------------------------------------------------
def _parse_args():
    """
        Parses command line args and set the global dict

        This function gets the command line passed to the program, parses it,
        and sets the command line options as a global dict.
    """

    # the global dict of arguments
    global g_dict_args

    # create the parser
    argparser = argparse.ArgumentParser(
        description='__PP_SHORT_DESC__'
    )

    # always print prog name/version
    print('__PP_NAME_BIG__ version __PP_VERSION__')

    # add arguments from the function above
    _add_args(argparser)

    # parse the arg list into a Namespace object (similar to dict)
    # NB: if there is an error in the command line, this function will:
    # 1. print usage
    # 2. print the error
    # 3. exit
    args = argparser.parse_args()

    # if we made it this far, cmd line is ok so print usage
    argparser.print_usage()

    # convert agrs to global dict
    g_dict_args = vars(args)

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
    _main()

# -)
