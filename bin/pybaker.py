#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 02/20/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ pybaker [cmd line]

when placed in a folder that is in the default $PATH, ie:
/usr/bin
~/.local/bin
etc.

(The extension will be removed by the installer)\n
All command line options will be passed to the main class, usually located at
~/.local/share/pyplate/src/pybaker.py.

Typical usage is show in the main() method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# NB: pure python
from pathlib import Path
import subprocess
import sys

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# find path to prj/lib
P_DIR_USR_INST = Path.home() / ".local/share/pyplate"

# ------------------------------------------------------------------------------
# Classes
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
    file, activating the venv and calling the main program.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # commands
    # NB: format params are inst dir, venv name, prog name, and cmd line
    S_CMD = (
        # cd to prj dir
        "cd {};"
        # activate prj venv
        ". .venv-pyplate/bin/activate;"
        # cd to old cwd
        "cd {};"
        # call prj with full path
        "{}/src/pybaker.py {}"
    )

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

        # save project path to return after venv activate
        start_dir = Path.cwd()

        # get args
        args = sys.argv

        # remove our path
        args = args[1:]

        # quote any args with spaces
        args = [f'"{item}"' if " " in item else item for item in args]

        # put args back together with spaces
        args = " ".join(args)

        # ----------------------------------------------------------------------

        # build cmd
        cmd = self.S_CMD.format(
            P_DIR_USR_INST, start_dir, P_DIR_USR_INST, args
        )

        # run cmd
        try:
            subprocess.run(cmd, shell=True, check=True)
        except (FileNotFoundError, subprocess.CalledProcessError):
            sys.exit(-1)


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
