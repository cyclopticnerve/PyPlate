#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PC_NAME_BIG__                                        /          \
# Filename: uninstall.py                                          |     ()     |
# Date    : __PC_DATE__                                           |            |
# Author  : __PD_AUTHOR__                                         |   \____/   |
# License : __PD_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
This module defines the options for Uninstallerator and runs it
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import installerator

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# define the uninstall settings
g_dict_uninstall = {
    "general": {"name": "__PC_NAME_BIG__"},
    "preflight": [],
    "dirs": ["${HOME}/.cyclopticnerve/__PC_NAME_SMALL__"],
    "files": {},
    "postflight": [],
}


# ------------------------------------------------------------------------------
# Public functions
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
    uninstaller.run(g_dict_uninstall)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    #     Code to run when called from command line

    #     This is the top level code of the program, called when the Python file
    #     is invoked from the command line.

    main()

# -)
