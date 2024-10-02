#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : GUIs_DEBUG                                             /          \
# Filename: install.py                                            |     ()     |
# Date    : 09/29/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to install the program on the user's computer
"""

# system imports
import json
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# get path to assets folder
P_DIR_SELF = Path(__file__).parent.resolve()
P_DIR_ASSETS = P_DIR_SELF / "__PP_ASSETS__"

# get path to lib in assets
P_DIR_LIB = P_DIR_ASSETS / "lib"
sys.path.append(str(P_DIR_LIB))

P_FILE_INST = P_DIR_ASSETS / "__PP_FILE_INST__"

# local imports
from cninstall.cninstaller import CNInstaller # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # create an instance of the class
    inst = CNInstaller(P_DIR_ASSETS)

    # run the installer
    try:
        with open(P_FILE_INST, "r", encoding="utf8") as a_file:
            dict_user = json.load(a_file)
        # run the instance
        inst.run_dict(dict_user)
    except (FileNotFoundError, json.JSONDecodeError):
        print("File not found or not JSON")
        sys.exit(-1)

# -)
