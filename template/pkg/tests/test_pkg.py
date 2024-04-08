# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: pkg_test.py                                           |     ()     |
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

# NB package names will give pylance error when viewed in the template
# DO NOT IGNORE THEM! WE NEED TO CHECK THE REPLACEMENT NAMES IN FINAL PROJECT!
# also the "src" path value in the paths below must match the name of your
# source directory in order for python to find the module
# it would be too much trouble to have pymaker replace these, but if you go
# with a different folder name, you can just replace it in the template and it
# will work fine

# ------------------------------------------------------------------------------
# options 1:

# path to dir above <package name>
DIR_PKG = Path(__file__).parents[1] / "src"
sys.path.append(str(DIR_PKG))

# from <package name> import <module name>
from __PP_NAME_SMALL__ import __PP_NAME_MOD__

# NB: path to cn libs is "__PP_DIR_LIB__"

# ------------------------------------------------------------------------------
# option 2:

# # path to <package name>
# DIR_PKG = Path(__file__).parents[1] / "src" / "__PP_NAME_SMALL__"
# sys.path.append(str(DIR_PKG))

# # import <module name>
# import __PP_NAME_MOD__

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
    __PP_NAME_MOD__.func()

# -)
