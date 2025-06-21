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

# system imports
from pathlib import Path
import sys

# local imports
PATH_PRJ = Path(__file__).parents[1].resolve()
PATH_SRC = PATH_PRJ / "__PP_NAME_PRJ_SMALL__"
sys.path.append(str(PATH_SRC))

# NB: i know this looks bad, but it WILL work
# pylint: disable=import-error
# pylint: disable=wrong-import-position

import __PP_NAME_SEC_SMALL__  # type: ignore

# pylint: enable=import-error
# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function
    RES = __PP_NAME_SEC_SMALL__.func()
    print(RES)

# -)
