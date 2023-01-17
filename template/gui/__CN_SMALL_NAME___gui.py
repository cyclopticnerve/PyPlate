#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __CN_BIG_NAME__                                        /          \
# Filename: __CN_SMALL_NAME___gui.py                              |     ()     |
# Date    : __CN_DATE__                                           |            |
# Author  : __CN_AUTHOR__                                         |   \____/   |
# License : __CN_LICENSE__                                         \          /
# ------------------------------------------------------------------------------

# TODO: flesh this out more once we use it for a gui app

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import os
import sys

# import main py file
curr_dir = os.path.abspath(os.path.dirname(__file__))
up_one = os.path.abspath(os.path.join(curr_dir, '..'))
sys.path.insert(1, up_one)
import __CN_SMALL_NAME__.py # noqa E402 (import not at top of file)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main function of the program
# ------------------------------------------------------------------------------
def main():

    """
        The main function of the program

        This function is the main entry point for the program, initializing the
        GUI and attaching it to the underlying Python program.
    """

    pass


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line, e.g. "python __CN_SMALL_NAME___gui.py".
    """

    main()

# -)
