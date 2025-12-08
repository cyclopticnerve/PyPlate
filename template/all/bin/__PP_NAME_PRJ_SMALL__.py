#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_PRJ_SMALL__.py                              |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ __PP_NAME_PRJ_SMALL__ [cmd line]

when placed in a folder that is in the default $PATH, ie:
/usr/bin
~/.local/bin
etc.

(The extension will be removed by the installer)\n
All command line options will be passed to the main class, usually located at
~/.local/share/__PP_NAME_PRJ_SMALL__/src/__PP_NAME_PRJ_SMALL__.py.

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
P_DIR_USR_INST = Path.home() / "__PP_USR_INST__"

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class __PP_NAME_PRJ_PASCAL__:
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
    S_CMD = "cd {};. {}/bin/activate;d {};{} {}"

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
    obj = __PP_NAME_PRJ_PASCAL__()

    # run the new object
    obj.main()

# -)
