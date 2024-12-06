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
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# ------------------------------------------------------------------------------
# option 1:

# path to dir above <package name>
P_DIR_PRJ = Path(__file__).parents[1].resolve()
P_DIR_SRC = P_DIR_PRJ / "__PP_DEV_SRC__"

# add paths to import search
sys.path.append(str(P_DIR_SRC))

# import my stuff
from __PP_NAME_SMALL__ import __PP_NAME_SEC__  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function
    res = __PP_NAME_SEC__.func()
    print(res)

# -)
