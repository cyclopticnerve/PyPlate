#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __CN_BIG_NAME__                                        /          \
# Filename: __CN_SMALL_NAME___gui.py                              |     ()     |
# Date    : __CN_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
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
# Short description
# ------------------------------------------------------------------------------
def main():

    """
        Short description

        Paramaters:
            var_name [type]: description
                second line

        Returns:
            [type]: description

        Raises:
            exception_type(vars): description

        Long description
    """

    pass


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# -)
