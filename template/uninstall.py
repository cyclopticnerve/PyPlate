#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __CN_NAME_BIG__                                        /          \
# Filename: uninstall                                             |     ()     |
# Date    : __CN_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import installerator

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# define the uninstall settings
dict_uninstall = {
    'general': {
        'name': '__CN_NAME_BIG__'
    },
    'preflight': [
    ],
    'dirs': [
        '${HOME}/.cyclopticnerve/__CN_NAME_SMALL__'
    ],
    'files': {
    },
    'postflight': [
    ]
}

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Run the Uninstaller module
# ------------------------------------------------------------------------------
def main():
    """
        Run the Uninstaller module

        This is the main uninstaller function, which creates an instance of the
        Uninstaller class and runs it's main function, with the global
        dictionary created above.
    """

    # instantiate uninstallerator class
    # package.module.class
    uninstaller = installerator.uninstallerator.Uninstallerator()

    # # run the instance
    # class.method
    uninstaller.run(dict_uninstall)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.
    """

    main()

# -)
