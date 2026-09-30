#! /usr/bin/env python3
# ------------------------------------------------------------------------------
# Package :__PP_NAME_PRJ_BIG__                                    /          \
# Filename: develop.py                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The develop script for this project

THis file sets up a virtual environment for developing the project. The main
purpose is to get the venv name right.

This file is real ugly b/c we can't access the venv, so we do it manually.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# NB: pure python
# system imports
import gettext
import locale
from pathlib import Path
import subprocess
import sys

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# get prj dir path
P_DIR_PRJ = Path(__file__).parent.resolve()

# ------------------------------------------------------------------------------
# gettext stuff for CLI

T_DOMAIN = "__PP_NAME_PRJ_SMALL__"
# FIXME: find this in conf
T_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.setlocale(locale.LC_ALL, "")
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The class to use for developing
# ------------------------------------------------------------------------------
class CNDevelop:
    """
    The class to use for developing a PyPlate program

    This class creates a virtual environment and fills it using
    requirements.txt. For package projects, it also installs itself as
    editable, for testing real-world installations.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # venv and reqs names
    S_NAME_VENV = "__PP_NAME_VENV__"
    S_FILE_REQS = "__PP_REQS_FILE__"

    # messages

    # I18N: done with step
    S_MSG_DONE = _("Done")
    # I18N: step failed
    S_MSG_FAIL = _("Failed")
    # I18N: show the venv step
    S_MSG_VENV_START = _("Making venv folder... ")
    # I18N: show the reqs step
    S_MSG_REQS_START = _("Installing requirements... ")

    # errors

    # I18N: an error occurred
    S_ERR_ERR = _("Error: ")

    # commands

    # NB: format param is dir_venv
    S_CMD_CREATE = "python3 -m venv {}"
    # install reqs/self
    S_CMD_TYPE_INST = "__PP_DEV_INST__"

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        Run the program

        Runs the developer install operation.
        """

        # make the venv on the user's comp
        self._make_venv()

        # install reqs
        self._install_reqs()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Make venv for this program on user's computer
    # --------------------------------------------------------------------------
    def _make_venv(self):
        """
        Make venv for this program on user's computer

        Makes a .venv-XXX folder on the user's computer.
        """

        # show progress
        print(self.S_MSG_VENV_START, flush=True, end="")

        # the command to create a venv
        cmd = self.S_CMD_CREATE.format(self.S_NAME_VENV)
        self._do_command(cmd)

    # --------------------------------------------------------------------------
    # Install requirements.txt
    # --------------------------------------------------------------------------
    def _install_reqs(self):
        """
        Install requirements.txt

        Installs the contents of a requirements.txt file into the program's
        venv.
        """

        # show progress
        print(self.S_MSG_REQS_START, end="", flush=True)

        # the cmd to install the reqs
        # NB: for apps, the last two fmt params are ignored (no self install)
        cmd = self.S_CMD_TYPE_INST.format(
            P_DIR_PRJ,
            self.S_NAME_VENV,
            self.S_FILE_REQS,  # for reqs
            P_DIR_PRJ,
            self.S_NAME_VENV,  # for self
        )
        self._do_command(cmd)

    # --------------------------------------------------------------------------
    # Common code to run a shell command
    # --------------------------------------------------------------------------
    def _do_command(self, cmd):
        """
        Common code to run a shell command
        """

        try:
            # NB: hide output
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(self.S_MSG_DONE)
        except (
            FileNotFoundError,
            subprocess.CalledProcessError,
        ) as e:
            print(self.S_MSG_FAIL)
            print()
            print(self.S_ERR_ERR, e)
            sys.exit(-1)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create an instance of the class
    inst = CNDevelop()

    # run the instance
    inst.main()

# -)
