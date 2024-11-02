#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pyplate_test.py                                       |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
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
# once you are sure the name is correct, you can add "# type: ignore" to the
# line to ignore the error

# ------------------------------------------------------------------------------
# option 1:

# path to dir above <package name>
DIR_PRJ = Path(__file__).parents[1].resolve()
DIR_SRC = DIR_PRJ / "src"
sys.path.append(str(DIR_SRC))

# from <package name> import <module name>
from pyplate import pyplate

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
    pyplate.func()  # type: ignore

# -)
