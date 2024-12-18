#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: install.py                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The install script for this project

THis module installs the project, copying its files and folders to the
appropriate locations on the user's computer. It also provides for hooks to run
Python (or other language) scripts before and after the actual install process.
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

DIR_SELF = Path(__file__).parent.resolve()
DIR_ASSETS = DIR_SELF / "__PP_INST_ASSETS__"
FILE_CFG_NEW = DIR_ASSETS / "__PP_INST_CONF_FILE__"
FILE_CFG_OLD = Path.home() / "__PP_USR_CONF__" / "__PP_INST_CONF_FILE__"
DIR_LIB = DIR_ASSETS / "_PP_DIR_LIB__"

# add paths to import search
sys.path.append(str(DIR_LIB))

# import my stuff
import cnlib.cninstall as C # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Run the main function
# ------------------------------------------------------------------------------
def main():
    """
    Run the main function
    """

    # create an instance of the class
    inst = C.CNInstall()

    # run the instance
    try:
        inst.install(DIR_ASSETS, FILE_CFG_NEW, FILE_CFG_OLD)
    except C.CNInstallError as e:
        print(e)

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()

# -)
