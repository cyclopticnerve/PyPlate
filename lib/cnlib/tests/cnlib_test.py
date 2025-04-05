#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnlib_test.py                                         |     ()     |
# Date    : 03/31/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A simple script to test a package

Note that you will need to activate the project's venv to use this script.
If you are working in VSCode, you should:
1. Deactivate the current venv in the Terminal tab using the "deactivate"
command
2. Make sure you have the correct interpreter selected for the project (check
the status bar)
3. Switch to the "Run and Debug" tab, and select the "Pkg Test" option
4. Press the "Run" button to run the script. This will activate the project's
venv for you

If you are working in an external terminal, you should:
1. Deactivate the current venv in the Terminal tab using the "deactivate"
command
2. cd to the project directory
3*. Activate the project's venv using: *
"(source | .) .venv-cnlib/bin/activate"
4. Run the script using:
"./tests/cnlib_test.py"

* some shells accept the "source" command, while others accept the "." command.
YMMV.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# pylint: disable=import-error

import cnfunctions as F  # type: ignore

# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function
    RES = F.pascal_case("CLI Test")
    print(RES)

# -)
