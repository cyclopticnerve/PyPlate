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

# add custom import paths
DIR_PKG = Path(__file__).parents[1]
sys.path.append(str(DIR_PKG))

# my imports
# from <package name> import <module name>
from __PP_NAME_SMALL__ import __PP_NAME_MOD__

# NB: alternatively, you can do this:
# # path to <package name>
# DIR_PKG = Path(__file__).parents[1] / "__PP_NAME_SMALL__"
# sys.path.append(str(DIR_PKG))

# # import <module name>
# import __PP_NAME_MOD__ # type: ignore

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
