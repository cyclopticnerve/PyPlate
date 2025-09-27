#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : CLI_Test                                               /          \
# Filename: cli_test.py                                           |     ()     |
# Date    : 09/23/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ cli_test [cmd line]

when placed in a folder that is in the default $PATH, ie:
/usr/bin
~/.local/bin
etc.

(The extension will be removed by the installer)\n
All command line options will be passed to the main class, usually located at
~/.local/share/cli_test/src/cli_test.py.

Typical usage is show in the main() method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from pathlib import Path
import subprocess
import sys

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class CliTest:
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

    # find path to prj/lib
    P_DIR_PRJ = Path.home() / ".local/share/cli_test"

    # commands to run
    S_CMD_ACTIVATE = ". .venv-cli_test/bin/activate"
    S_CMD_RUN = "./src/cli_test.py"
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

        # quote any args with spaces
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
            # cd to inst
            f"cd {self.P_DIR_PRJ};"
            # activate venv
            f"{self.S_CMD_ACTIVATE};"
            # call src w/ args
            f"{src_run}"
        )

        # run cmd
        try:
            subprocess.run(cmd, shell=True, check=True)
        except FileNotFoundError as fnfe:
            print("error:", fnfe)
            sys.exit(-1)
        except subprocess.CalledProcessError as cpe:
            print("error:", cpe.stderr)
            sys.exit(-1)

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    obj = CliTest()

    # run the new object
    obj.main()

# -)
