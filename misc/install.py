#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: install.py                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
This module defines the options for Installerator and runs it
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import installerator

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# define the install settings
g_dict_install = {
    'general': {
        'name': '__PP_NAME_BIG__'
    },
    'preflight': [
    ],
    'deps_py': [
    ],
    'deps_sys': [
    ],
    'dirs': [
        '${HOME}/.cyclopticnerve/__PP_NAME_SMALL__'
    ],
    'files': {
        'LICENSE.txt': '${HOME}/.cyclopticnerve/__PP_NAME_SMALL__',
        'uninstall.py': '${HOME}/.cyclopticnerve/__PP_NAME_SMALL__'
    },
    'postflight': [
    ]
}


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Run the Installer module
# ------------------------------------------------------------------------------
def main():
    """
        Run the Installer module

        This is the main installer function, which creates an instance of the
        Installer class and runs its main function, with the global
        dictionary created above.
    """

    # instantiate installerator class
    # package.module.class
    installer = installerator.installerator.Installerator()

    # # run the instance
    # class.method
    installer.run(g_dict_install)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # call the main function
    main()

# -)
