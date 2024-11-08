#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: uninstall.py                                          |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The uninstall script for this project

THis module uninstalls the project, removing its files and folders to the
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
DIR_LIB = DIR_SELF / "lib"
FILE_INSTALL = DIR_SELF / "conf/install.json"

# add paths to import search
sys.path.append(str(DIR_LIB))

# import my stuff
import cninstalllib.cninstall as C # type: ignore

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
    inst = C.CNInstall(FILE_INSTALL)

    # run the instance
    try:
        inst.uninstall(debug=True)
    except C.CNInstallError as e:
        print(e)

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# -)
