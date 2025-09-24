#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_PRJ_SMALL___test.py                         |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
A simple script to test a package from within the project itself
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# local imports

# pylint: disable=import-error
from __PP_NAME_PRJ_SMALL__ import __PP_NAME_SEC_SMALL__
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function
    res = __PP_NAME_SEC_SMALL__.func()
    print(res)

# -)
