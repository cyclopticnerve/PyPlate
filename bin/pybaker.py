#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 02/20/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                               \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ pybaker [cmd line]

when placed in a folder that is in the default $PATH, ie:
/usr/bin
~/.local/bin
etc.

All command line options will be passed to the main class, usually located at
~/.local/share/pyplate/src/pybaker.py. 

Typical usage is show in the main() method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from pathlib import Path
import subprocess
import sys

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class PyBaker:
    """
    The entry point class, responsible for launching the program

    Public methods:
        main: The main method of the program

    This class starts the program from the command line when it is installed in
    directories that are defined in the $PATH variable. These are places like
    /usr/bin, ~/.local/bin, etc. and can be called from the command line
    regardless of the current working directory. It is basically a "bootstrap"
    file.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # find path to prj/lib
    # P_DIR_PRJ = Path.home() / ".local/share/pyplate"
    P_DIR_PRJ = Path.home() / "Documents/Projects/Python/PyPlate"

    # commands to run
    S_CMD_ACTIVATE = f". {P_DIR_PRJ}/.venv-pyplate/bin/activate"
    S_CMD_RUN = f"{P_DIR_PRJ}/src/pybaker.py"
    S_CMD_RUN_ARGS = "{} {}"

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main method of the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        The main method of the program

        This method is the main entry point for the program, initializing the
        program, and performing its steps.

        It then calls the real main module, located in the install dir.
        """

        # ----------------------------------------------------------------------

        # get args
        args = sys.argv

        # remove our path
        args = args[1:]

        # quote an args with spaces
        args = [f'"{item}"' if " " in item else item for item in args]

        # put args back together with spaces
        args = " ".join(args)

        # def cmd line - no args
        src_run = self.S_CMD_RUN

        # add args if present
        if len(args) > 0:
            src_run = self.S_CMD_RUN_ARGS.format(self.S_CMD_RUN, args)

        # ----------------------------------------------------------------------

        # build cmd
        cmd = (
            # activate venv
            f"{self.S_CMD_ACTIVATE};"
            # call src w/ args
            f"{src_run}"
        )

        # run cmd
        subprocess.run(cmd, shell=True, check=True)

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    obj = PyBaker()

    # run the new object
    obj.main()

# -)
