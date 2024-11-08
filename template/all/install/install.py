#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: install.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The install script for this project

THis module installs the project, copying its files and folders to the
appropriate locations on the user's computer. It also provides for hooks to run
Python (or other language) scripts before and after the actual install process.
"""

# f00_bar = {
#     C.S_KEY_META: {
#         "NAME": "PyPlate",        
#         "VERSION": "0.0.1"         
#     },
#     C.S_KEY_PREFLIGHT: ["preflight_script_1"],
#     C.S_KEY_SYS_REQS: ["sys_reqs_1"],
#     C.S_KEY_PY_REQS: ["py_reqs_1"],
#     C.S_KEY_CONTENT: {
#         "conf": ".conf/pyplate",          
#         "spaceoddity.py": ".pyplate",          
#         "LICENSE": ".pyplate",          
#         "VERSION": ".pyplate",          
#         "uninstall.py": ".pyplate",          
#         "uninstall.json": ".pyplate",          
#         "cron_uninstall.py": ".config/.pyplate",          
#     },
#     C.S_KEY_POSTFLIGHT: ["postflight_script_1"],
# }

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
DIR_LIB = DIR_ASSETS / "lib"
FILE_INSTALL = DIR_ASSETS / "conf/install.json"

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
        inst.install(DIR_ASSETS, debug=True)
    except C.CNInstallError as e:
        print(e)

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# -)
