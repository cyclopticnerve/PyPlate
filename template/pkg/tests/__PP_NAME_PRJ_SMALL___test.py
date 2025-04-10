#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_PRJ_SMALL___test.py                         |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
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
3*. Activate the project's venv using:
"(source | .) .venv-__PP_NAME_PRJ_SMALL__/bin/activate"
4. Run the script using:
"./tests/__PP_NAME_PRJ_SMALL___test.py"

* some shells accept the "source" command, while others accept the "." command.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# lib imports
import __PP_NAME_SEC_SMALL__

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main function
    res = __PP_NAME_SEC_SMALL__.func()
    print(res)

# -)
