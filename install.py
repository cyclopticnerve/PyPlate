# ------------------------------------------------------------------------------
# Project : __CN_BIG_NAME__                                        /          \
# Filename: install.py                                            |     ()     |
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
        "name":                         "__CN_BIG_NAME__"
    },
    "preflight": [
    ],
    "sys_reqs": [
    ],
    "py_reqs": [
    ],
    "dirs": [
        "${HOME}/.__CN_SMALL_NAME__"
    ],
    "files": {
        "${SRC}/LICENSE":               "${HOME}/.__CN_SMALL_NAME__",
        "${SRC}/uninstall.py":          "${HOME}/.__CN_SMALL_NAME__",
        "${SRC}/__CN_SMALL_NAME__.py":  "${HOME}/.__CN_SMALL_NAME__"
    },
    "postflight": [
    ]
}

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# This happens when we run script from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # instantiate installerator class
    inst = installerator.installerator.Installerator()

    # # run the instance
    inst.run(dict_user)

# -)