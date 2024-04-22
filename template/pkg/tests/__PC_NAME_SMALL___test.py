# ------------------------------------------------------------------------------
# Project : __PC_NAME_BIG__                                        /          \
# Filename: __PC_NAME_SMALL___test.py                             |     ()     |
# Date    : __PC_DATE__                                           |            |
# Author  : __PD_AUTHOR__                                         |   \____/   |
# License : __PD_LICENSE_NAME__                                    \          /
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
DIR_PKG = Path(__file__).parents[1] / "__PD_DEV_SRC__"
sys.path.append(str(DIR_PKG))

# from <package name> import <module name>
from __PC_NAME_SMALL__ import __PC_NAME_MOD__

# ------------------------------------------------------------------------------
# option 2:

# # path to <package name>
# DIR_PKG = Path(__file__).parents[1] / "__PD_DEV_SRC__" / "__PC_NAME_SMALL__"
# sys.path.append(str(DIR_PKG))

# # import <module name>
# import __PC_NAME_MOD__

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
    __PC_NAME_MOD__.func()  # type: ignore

# -)
