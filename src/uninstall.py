# ------------------------------------------------------------------------------
# Project : __CN_BIG_NAME__                                        /          \
# Filename: uninstall.py                                          |     ()     |
# Date    : __CN_DATE__                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import installerator

# NB: requires:
# installerator

# the user dict
dict_user = {
    "general": {
        "name": "__CN_BIG_NAME__"
    },
    "preflight": [
    ],
    "dirs": [
        "${HOME}/.s__CN_SMALL_NAME"
    ],
    "files": {
    },
    "postflight": [
    ]
}

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# This happens when we run script from comand line
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # instantiate uninstallerator class
    uninst = installerator.uninstallerator.Uninstallerator()

    # # run the instance
    uninst.run(dict_user)

# -)
