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

# ------------------------------------------------------------------------------
# Define the install settings
# ------------------------------------------------------------------------------
dict_install = {
    "general": {
        "name": "__CN_BIG_NAME__"
    },
    "preflight": [
    ],
    "sys_reqs": [
    ],
    "py_reqs": [
    ],
    "dirs": [
        "${HOME}/.cyclopticnerve/__CN_SMALL_NAME__"
    ],
    "files": {
        "${SRC}/LICENSE": "${HOME}/.cyclopticnerve/__CN_SMALL_NAME__",
        "${SRC}/uninstall.py": "${HOME}/cyclopticnerve/.__CN_SMALL_NAME__",
        "${SRC}/__CN_SMALL_NAME__.py": "${HOME}/.cyclopticnerve/__CN_SMALL_NAME__"
    },
    "postflight": [
    ]
}

# ------------------------------------------------------------------------------
# Run the main class if we are called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # instantiate installerator class
    installer = installerator.installerator.Installerator()

    # # run the instance
    installer.run(dict_install)

# -)
