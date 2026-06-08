#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: install.py                                            |     ()     |
# Date    : 03/29/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The install script for this project

This module installs the project, copying its files and folders to the
appropriate locations on the user's computer.

This file is real ugly b/c we can't access the venv, so we do it manually.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# NB: pure python
# system imports
from pathlib import Path
import re
import shutil
import subprocess
import sys

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# get prj dir
P_DIR_PARENT = Path(__file__).parent.resolve()

# get in dirs
P_DIR_ASSETS = P_DIR_PARENT / "assets"
P_DIR_INSTALL = P_DIR_ASSETS / "install"

# get in files
# NB: use local uninstall
P_FILE_UNINST = P_DIR_ASSETS / "uninstall.py"
P_FILE_REQS = P_DIR_INSTALL / "requirements.txt"
P_FILE_DESK = P_DIR_ASSETS / "src/gui/desktop/PyPlate.desktop"
P_FILE_DESK_ICON = P_DIR_ASSETS / ".local/share/pyplate/images/pyplate.png"
P_FILE_CFG_NEW = P_DIR_INSTALL / "install.json"

# get out dirs
P_DIR_VENV = Path.home() / ".local/share/pyplate/.venv-pyplate"
P_DIR_CONF = Path.home() / ".config/pyplate/pyplate"

# get out files
P_FILE_CFG_OLD = Path.home() / ".local/share/pyplate/install/install.json"

# get pre/post files
# NB: uncomment these and pybaker will replace them
# P_FILE_PRE = P_DIR_INSTALL / "__PP_INST_PRE__"
# P_FILE_POST = P_DIR_INSTALL / "__PP_INST_POST__"

# ------------------------------------------------------------------------------
# Local imports
# ------------------------------------------------------------------------------

# fudge path to load base
sys.path.append(str(P_DIR_INSTALL))

# local imports
# pylint: disable=wrong-import-position, import-error
from install_base import CNInstallBase  # type: ignore

# pylint: enable=wrong-import-position, import-error

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The class to use for installing/uninstalling
# ------------------------------------------------------------------------------
class CNInstall(CNInstallBase):
    """
    The class to use for installing a PyPlate program

    This class performs the install operation.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the new object

        Initializes a new instance of the class, setting the default values
        of its properties, and any other code that needs to run to create a
        new object.
        """

        # always call super
        super().__init__()

        # redeclare prop for some reason?
        self._dict_cfg = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Install the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        Install the program

        Runs the install operation.
        """

        # do setup
        self._setup()

        # get prj info from cfg
        self._get_project_info()

        # get prg name/version
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]
        prog_version = self._dict_cfg[self.S_KEY_INST_VER]

        # maybe show we are starting
        if not self._arg_quiet:
            print(self.S_MSG_INST_START.format(prog_name, prog_version))
            print()

        # uninstall old version (if present)
        self._uninstall_cont(True)

        # make the venv on the user's comp
        self._make_venv()

        # install reqs
        self._install_reqs()

        # fix desktop file if present
        self._fix_desktop_file()

        # move content
        cont = self._dict_cfg.get(self.S_KEY_INST_CONT, {})
        self._install(self.S_MSG_COPY_START, cont)

        # only copy conf, never overwrite
        if not P_DIR_CONF.exists():
            conf = self._dict_cfg.get(self.S_KEY_CFG_CONT, {})
            self._install(self.S_MSG_CONF_START, conf)

        # maybe show we are done
        if not self._arg_quiet:
            if not self._arg_dry:
                print()
            print(self.S_MSG_INST_END.format(prog_name))

        # wind down
        self._teardown()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # NB: these are the main steps, called in order from main()

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Get the install info from the config file.
        """

        # ----------------------------------------------------------------------
        # get new info

        try:
            # get project info
            self._dict_cfg = self._get_dict_from_file(P_FILE_CFG_NEW)
        except OSError as e:
            # fatal error, print and quit
            # NB: print even if quiet
            print(self.S_ERR_ERR, e)
            self._teardown(-1)

        # ----------------------------------------------------------------------
        # check for reasons to skip question

        # don't check for version or new install
        if self._arg_force:
            return

        # if we don't find old cfg, must be new install
        if not P_FILE_CFG_OLD or not P_FILE_CFG_OLD.exists():
            return

        # ----------------------------------------------------------------------

        # get info from old cfg
        dict_cfg_old = {}
        try:
            # get info from old cfg
            dict_cfg_old = self._get_dict_from_file(P_FILE_CFG_OLD)
        except OSError as e:
            # fatal error, print and quit
            # NB: print even if quiet
            print(self.S_ERR_ERR, e)
            self._teardown(-1)

        # check versions
        ver_old = dict_cfg_old[self.S_KEY_INST_VER]
        ver_new = self._dict_cfg[self.S_KEY_INST_VER]

        # do the compare and get S_VER__OLDER, I_VER_SAME, I_VER_NEWER
        res = self._comp_sem_ver(ver_old, ver_new)

        # check for error
        if res == self.I_VER_ERROR:
            # fatal error, print and quit
            # NB: print even if quiet
            print(self.S_ERR_VERSION)
            self._teardown(-1)

        # same version is installed
        if res == self.I_VER_SAME:

            # ask to install same version
            str_ask = self._dialog(
                self.S_ASK_VER_SAME,
                [self.S_ASK_YES, self.S_ASK_NO],
                self.S_ASK_NO,
            )
            print()

            # user hit enter or typed anything else except "y"
            if str_ask != self.S_ASK_YES:
                # normal error, print and quit
                if not self._arg_quiet:
                    print(self.S_MSG_ABORT)
                self._teardown()

        # newer version is installed
        elif res == self.I_VER_OLDER:

            # ask to install old version over newer
            str_ask = self._dialog(
                self.S_ASK_VER_OLDER,
                [self.S_ASK_YES, self.S_ASK_NO],
                self.S_ASK_NO,
            )
            print()

            # user hit enter or typed anything else except "y"
            if str_ask != self.S_ASK_YES:
                # normal error, print and quit
                if not self._arg_quiet:
                    print(self.S_MSG_ABORT)
                self._teardown()

    # --------------------------------------------------------------------------
    # Make venv for this program on user's computer
    # --------------------------------------------------------------------------
    def _make_venv(self):
        """
        Make venv for this program on user's computer

        Makes a .venv-XXX folder on the user's computer.
        """

        # the command to create a venv
        cmd = self.S_CMD_CREATE.format(P_DIR_VENV)

        # if it's a dry run, don't make venv
        if self._arg_dry:
            print(self.S_DRY_VENV, cmd)
            print()
            return

        # ----------------------------------------------------------------------

        # show progress
        if not self._arg_quiet:
            print(self.S_MSG_VENV_START, end="", flush=True)

        # the cmd to create the venv
        try:
            subprocess.run(cmd, check=True, shell=True, capture_output=True)
            if not self._arg_quiet:
                print(self.S_MSG_DONE)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            if not self._arg_quiet:
                print(self.S_MSG_FAIL)
            # fatal error, print and quit
            # NB: print even if quiet
            print()
            print(self.S_ERR_ERR, e)
            self._teardown(-1)

    # --------------------------------------------------------------------------
    # Install requirements.txt
    # --------------------------------------------------------------------------
    def _install_reqs(self):
        """
        Install requirements.txt

        Installs the contents of a requirements.txt file into the program's
        venv.
        """

        # the command to install packages to venv from reqs
        cmd = self.S_CMD_TYPE_INST.format(
            P_DIR_VENV.parent, P_DIR_VENV.name, P_FILE_REQS
        )

        # if it's a dry run, don't install
        if self._arg_dry:
            print(self.S_DRY_REQS, cmd)
            print()
            return

        # ----------------------------------------------------------------------

        # show progress
        if not self._arg_quiet:
            print(self.S_MSG_REQS_START, end="", flush=True)

        # the cmd to install the reqs
        try:
            subprocess.run(cmd, check=True, shell=True, capture_output=True)
            if not self._arg_quiet:
                print(self.S_MSG_DONE)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            if not self._arg_quiet:
                print(self.S_MSG_FAIL)
            # fatal error, print and quit
            # NB: print even if quiet
            print()
            print(self.S_ERR_ERR, e)
            self._teardown(-1)

    # --------------------------------------------------------------------------
    # Fix .desktop file, for paths and such
    # --------------------------------------------------------------------------
    def _fix_desktop_file(self):
        """
        Fix .desktop file, for paths and such

        Raises:
            OSError if one of both of the files does not exist

        Fixes entries in the .desktop file (absolute paths, etc.)
        Currently only fixes absolute path to icon.
        """

        # make sure we even care about desktop
        use_desk = self._dict_cfg.get(self.S_KEY_INST_DESK, False)
        if not use_desk:
            return

        # sanity check (params to main might be None)
        if (
            not P_FILE_DESK
            or not P_FILE_DESK.exists()
            or not P_FILE_DESK_ICON
            or not P_FILE_DESK_ICON.exists()
        ):
            print(self.S_ERR_NO_DESK)
            print()
            return

        # don't mess with file
        if self._arg_dry:
            print(self.S_DRY_DESK_ICON, P_FILE_DESK_ICON)
            print()
            return

        # ----------------------------------------------------------------------

        # print info
        if not self._arg_quiet:
            print(self.S_MSG_DSK_START, end="", flush=True)

        # open file
        text = ""
        with open(P_FILE_DESK, "r", encoding=self.S_ENCODING) as a_file:
            text = a_file.read()

        # find icon line and fix
        res = re.search(self.R_ICON_SCH, text, flags=re.M)
        if res:

            # get user's home and path to icon rel to prj
            path_icon = Path.home() / P_FILE_DESK_ICON

            # fix abs path to icon
            r_icon_rep = self.R_ICON_REP.format(path_icon)
            text = re.sub(self.R_ICON_SCH, r_icon_rep, text, flags=re.M)

            # write fixed text back to file
            with open(P_FILE_DESK, "w", encoding=self.S_ENCODING) as a_file:
                a_file.write(text)

        # show some info
        if not self._arg_quiet:
            print(self.S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Copy source files/folders
    # --------------------------------------------------------------------------
    def _install(self, msg: str, dict_cfg: dict[str, str]):
        """
        Copy source files/folders

        This method copies files and folders from the key (relative to assets)
        to the dest (relative to user home).
        """

        # show some info
        if not self._arg_quiet and not self._arg_dry:
            print(msg, flush=True, end="")

        # for each key, value
        for k, v in dict_cfg.items():

            # get full paths of source / destination
            src = P_DIR_ASSETS / k
            dst = Path.home() / v / src.name

            # sanity check
            # NB: debug may omit certain assets
            if not src.exists():
                continue

            # check for dry run
            if self._arg_dry:
                print(self.S_DRY_COPY.format(src, dst))
                print()
            else:
                # if the source is a dir
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                # if the src is a file
                else:
                    shutil.copy(src, dst)

        # show some info
        if not self._arg_quiet and not self._arg_dry:
            print(self.S_MSG_DONE)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    inst = CNInstall()

    # run the instance
    inst.main()


# -)
