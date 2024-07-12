#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL___test.py                             |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
A quick and dirty script to test a package
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=import-error

# my imports
# add custom import paths

# NB: package names below will give pylance error when viewed in the template
# DO NOT IGNORE THEM! WE NEED TO CHECK THE REPLACEMENT NAMES IN FINAL PROJECT!

# ------------------------------------------------------------------------------
# option 1:

# path to dir above <package name>
DIR_PRJ = Path(__file__).parents[1].resolve()
DIR_SRC = DIR_PRJ / "__PP_DEV_SRC__"
sys.path.append(str(DIR_SRC))

# from <package name> import <module name>
from __PP_NAME_SMALL__ import __PP_NAME_SEC__

# ------------------------------------------------------------------------------
# option 2:

# # path to <package name>
# DIR_PRJ = Path(__file__).parents[1].resolve()
# DIR_SRC = DIR_PRJ / "__PP_DEV_SRC__" / "__PP_NAME_SMALL__"
# sys.path.append(str(DIR_SRC))

# # import <module name>
# import __PP_NAME_SEC__

# ------------------------------------------------------------------------------

# pylint: enable=wrong-import-position
# pylint: enable=import-error


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function
    __PP_NAME_SEC__.func()  # type: ignore

# -)
