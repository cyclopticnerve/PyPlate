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
        program, and performing it's steps.
    """

    # NB: use this if you need to
    # parse args
    # args = _parse_args()

    # call the steps in order
    func()


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
def func():
    """
        Short description

        Paramaters:
            var_name [type]: description

        Returns:
            [type]: description

        Raises:
            exception_type(vars): description

        Long description
    """

    return ('this is a test')


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Parses the command line
# ------------------------------------------------------------------------------
def _parse_args():
    """
        Parses the command line

        Returns:
            [dict]: A dict of command line options and their values

        This function parses the command line and collates required/optional
        values
    """

    # always print prog name/version
    print('__PP_NAME_BIG__ version PP_VERSION')

    # create the pasrser
    parser = argparse.ArgumentParser(
        description='PP_SHORT_DESC'
    )

    # add default cmd-line args
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='PP_VERSION'
    )

    # add any position/optional args\
    _add_args()

    # parse the cmd-line args
    args = parser.parse_args()

    # convert args to dict
    ret_args = vars(args)

    # if no args, print usage
    if len(ret_args) == 0:
        parser.print_usage()

    # return the parsed args
    return ret_args


# ------------------------------------------------------------------------------
# Add arguments to command-line parser
# ------------------------------------------------------------------------------
def _add_args(parser):

    # NB: add args here
    # https://docs.python.org/3/library/argparse.html
    # parser.add_argument(
    #     '--bar'
    # )

    # used in case above code is commented (like pass)
    return


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.
    """

    main()

# -)
