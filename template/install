#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __CN_BIG_NAME__                                        /          \
# Filename: install.py                                            |     ()     |
# Date    : __CN_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import installerator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# define the install settings
dict_install = {
    'general': {
        'name': '__CN_BIG_NAME__'
    },
    'preflight': [
    ],
    'sys_reqs': [
    ],
    'py_reqs': [
        '__CN_PY_DEPS__'
    ],
    'dirs': [
        '${HOME}/.cyclopticnerve/__CN_SMALL_NAME__'
    ],
    'files': {
        'LICENSE.txt': '${HOME}/.cyclopticnerve/__CN_SMALL_NAME__',
        'uninstall.py': '${HOME}/.cyclopticnerve/__CN_SMALL_NAME__'
    },
    'postflight': [
    ]
}

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Run the Installer module
# ------------------------------------------------------------------------------
def main():

    """
        Run the Installer module

        This is the main installer function, which creates an instance of the
        Installer class and runs it's main function, with the global
        dictionary created above.
    """

    # instantiate installerator class
    # package.module.class
    installer = installerator.installerator.Installerator()

    # # run the instance
    # class.method
    installer.run(dict_install)


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
