#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: install.py                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
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
P_DIR_PRJ = Path(__file__).parent.resolve()

# get dirs
P_DIR_ASSETS = P_DIR_PRJ / "__PP_DIR_ASSETS__"
P_DIR_INSTALL = P_DIR_ASSETS / "__PP_DIR_INSTALL__"
P_DIR_VENV = Path.home() / "__PP_USR_INST__/__PP_NAME_VENV__"

# get files
P_FILE_CFG_UNINST = (
    Path.home() / "__PP_USR_INST__/__PP_DIR_INSTALL__/__PP_FILE_INST_CFG__"
)
P_FILE_CFG = P_DIR_INSTALL / "__PP_FILE_INST_CFG__"
P_FILE_REQS = P_DIR_INSTALL / "__PP_REQS_FILE__"
P_FILE_DESK = P_DIR_ASSETS / "__PP_FILE_DESK__"
P_FILE_DESK_ICON = P_DIR_ASSETS / "__PP_IMG_DESK__"

P_FILE_PRE = P_DIR_INSTALL / "__PP_INST_PRE__"
P_FILE_POST = P_DIR_INSTALL / "__PP_INST_POST__"

# ------------------------------------------------------------------------------
# Local imports
# ------------------------------------------------------------------------------

# fudge path to load base
sys.path.append(str(P_DIR_INSTALL))

# local imports
# pylint: disable=wrong-import-position
import install_base as B  # type: ignore
from install_base import _  # type: ignore
from install_base import CNInstallBase  # type: ignore

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

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
    # Class constants
    # --------------------------------------------------------------------------

    # strings
    # NB: format params are prog_name and prog_version
    # I18N: install the program
    S_MSG_INST_START = _("Installing {} Version {}")
    # NB: format param is prog_name
    # I18N: show the copy step
    S_MSG_COPY_START = _("Copying files... ")
    # I18N: show the venv step
    S_MSG_VENV_START = _("Making venv folder... ")
    # I18N: show the reqs step
    S_MSG_REQS_START = _("Installing requirements... ")
    # I18N: show desktop step
    S_MSG_DSK_START = _("Fixing .desktop file... ")
    # I18N: done installing
    S_MSG_INST_END = _("{} installed")

    # questions
    S_ASK_VER_SAME = _(
        # I18N: ask to overwrite same version
        "The current version of this program is already installed.\nDo you "
        "want to overwrite?"
    )
    S_ASK_VER_OLDER = _(
        # I18N: ask to overwrite newer version
        "A newer version of this program is currently installed.\nDo you want "
        "to overwrite?"
    )

    # errors
    # I18N: version numbers invalid
    S_ERR_VERSION = _("One or both version numbers are invalid")
    # NB: format param is source path
    # I18N: src path invalid
    S_ERR_SRC_PATH = _("Source path can not be {}")
    # NB: format param is dest path
    # I18N: dst path invalid
    S_ERR_DST_PATH = _("Destination path can not be {}")
    # I18N: can't find .desktop
    S_ERR_NO_DESK = _("No desktop files present")

    # dry run messages
    S_DRY_VENV = "\nvenv cmd:"
    S_DRY_REQS = "\nreqs cmd:"
    # NB: format params are source and destination file/dir
    S_DRY_COPY = "\ncopy\n{}\nto\n{}"
    # NB: format param is path to icon
    S_DRY_DESK_ICON = "set desktop icon: {}"

    # commands
    # NB: format param is dir_venv
    S_CMD_CREATE = "python -m venv {}"
    # NB: format params are path to prj, path to venv, and path to reqs file
    S_CMD_TYPE_INST = "cd {};. {}/bin/activate;python -m pip install -r {}"
    # NB: format param is post install file name
    S_CMD_RUN_EXT = "python {}"

    # regex for adding user's home to icon path
    R_ICON_SCH = r"^(Icon=)(.*)$"
    R_ICON_REP = r"\g<1>{}"  # Icon=<home/__PP_IMG_DESK__>

    # --------------------------------------------------------------------------

    # version check results
    I_VER_OLDER = -1
    I_VER_SAME = 0
    I_VER_NEWER = 1
    I_VER_ERROR = -2

    # regex to compare version numbers
    R_VERSION_VALID = (
        r"^"
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-("
        r"(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*"
        r"))?"
        r"(?:\+("
        r"[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*"
        r"))?"
        r"$"
    )
    R_VERSION_GROUP_MAJ = 1
    R_VERSION_GROUP_MIN = 2
    R_VERSION_GROUP_REV = 3
    R_VERSION_GROUP_PRE = 4
    R_VERSION_GROUP_META = 5

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

        # do pre uninstall
        self._do_external(P_FILE_PRE)

        # check for existing/old version
        self._compare_version()

        # make the venv on the user's comp
        self._make_venv()

        # install reqs
        self._install_reqs()

        # fix desktop file if present
        self._fix_desktop_file()

        # move content
        self._install_content()

        # wind down
        self._teardown()

        # do post install
        self._do_external(P_FILE_POST)

        print()

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

        try:
            # get project info
            self._dict_cfg = self._get_dict_from_file(P_FILE_CFG)
        except OSError as e:
            print(self.S_ERR_ERR, e)

        # get prg name/version
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]
        prog_version = self._dict_cfg[self.S_KEY_INST_VER]

        # print start msg
        print(self.S_MSG_INST_START.format(prog_name, prog_version))
        print()

    # --------------------------------------------------------------------------
    # Check version info
    # --------------------------------------------------------------------------
    def _compare_version(self):
        """
        Check version info

        Get the version info from the new config file and the old config file
        (if present), compare the two values, and either continue or abort.
        """

        # check for force to skip question
        force = self._dict_args.get(self.S_ARG_FORCE_DEST, False)
        if force:
            return

        # if we did pass an old conf, it must exist (if it doesn't, this could
        # be the first install but we will want to check on later updates)
        if not P_FILE_CFG_UNINST or not P_FILE_CFG_UNINST.exists():
            return

        try:
            # get info from old cfg
            dict_cfg_old = self._get_dict_from_file(P_FILE_CFG_UNINST)
        except OSError as e:
            print(self.S_ERR_ERR, e)

        # check versions
        ver_old = dict_cfg_old[self.S_KEY_INST_VER]
        ver_new = self._dict_cfg[self.S_KEY_INST_VER]

        # do the compare and get S_VER__OLDER, I_VER_SAME, I_VER_NEWER
        res = self._comp_sem_ver(ver_old, ver_new)

        # same version is installed
        if res == self.I_VER_SAME:

            # ask to install same version
            str_ask = self._dialog(
                self.S_ASK_VER_SAME,
                [self.S_ASK_YES, self.S_ASK_NO],
                self.S_ASK_NO,
            )

            # user hit enter or typed anything else except "y"
            if str_ask != self.S_ASK_YES:
                print(self.S_MSG_ABORT)
                sys.exit(0)

        # newer version is installed
        elif res == self.I_VER_OLDER:

            # ask to install old version over newer
            str_ask = self._dialog(
                self.S_ASK_VER_OLDER,
                [self.S_ASK_YES, self.S_ASK_NO],
                self.S_ASK_NO,
            )

            # user hit enter or typed anything else except "y"
            if str_ask != self.S_ASK_YES:
                print(self.S_MSG_ABORT)
                sys.exit(0)

        print()

    # --------------------------------------------------------------------------
    # Make venv for this program on user's computer
    # --------------------------------------------------------------------------
    def _make_venv(self):
        """
        Make venv for this program on user's computer

        Raises:
            subprocess.CalledProcessError if the venv creation fails

        Makes a .venv-XXX folder on the user's computer.
        """

        # show progress
        print(self.S_MSG_VENV_START, flush=True, end="")

        # the command to create a venv
        cmd = self.S_CMD_CREATE.format(P_DIR_VENV)

        # if it's a dry run, don't make venv
        if self._dry_run:
            print(self.S_DRY_VENV, cmd)
            print(self.S_MSG_DONE)
            return

        # the cmd to create the venv
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(self.S_MSG_DONE)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(self.S_MSG_FAIL)
            print()
            print(self.S_ERR_ERR, e)
            sys.exit(-1)

    # --------------------------------------------------------------------------
    # Install requirements.txt
    # --------------------------------------------------------------------------
    def _install_reqs(self):
        """
        Install requirements.txt

        Raises:
            subprocess.CalledProcessError if the reqs install fails

        Installs the contents of a requirements.txt file into the program's
        venv.
        """

        # show progress
        print(self.S_MSG_REQS_START, end="", flush=True)

        # the command to install packages to venv from reqs
        cmd = self.S_CMD_TYPE_INST.format(
            P_DIR_VENV.parent, P_DIR_VENV.name, P_FILE_REQS
        )

        # if it's a dry run, don't install
        if self._dry_run:
            print(self.S_DRY_REQS, cmd)
            print(self.S_MSG_DONE)
            return

        # the cmd to install the reqs
        try:
            # NB: hide output
            subprocess.run(cmd, shell=True, check=True, capture_output=True)
            print(self.S_MSG_DONE)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            print(self.S_MSG_FAIL)
            print()
            print(self.S_ERR_ERR, e)
            sys.exit(-1)

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

        # print info
        print(self.S_MSG_DSK_START, end="", flush=True)

        # don't mess with file
        if self._dry_run:
            print(self.S_DRY_DESK_ICON.format(P_FILE_DESK_ICON))
            print(self.S_MSG_DONE)
            return

        # sanity check (params to main might be None)
        if not P_FILE_DESK or not P_FILE_DESK_ICON:
            print(self.S_ERR_NO_DESK)
            return

        # open file
        text = ""
        with open(P_FILE_DESK, "r", encoding=B.S_ENCODING) as a_file:
            text = a_file.read()

        # find icon line and fix
        res = re.search(self.R_ICON_SCH, text, flags=re.M)
        if res:

            # get user's home and path to icon rel to prj
            path_icon = Path.home() / P_FILE_DESK_ICON

            # fix abs path to icon
            r_icon_rep = self.R_ICON_REP.format(path_icon)
            text = re.sub(self.R_ICON_SCH, r_icon_rep, text, flags=re.M)

            # ------------------------------------------------------------------

            # write fixed text back to file
            with open(P_FILE_DESK, "w", encoding=B.S_ENCODING) as a_file:
                a_file.write(text)

        # show some info
        print(self.S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Copy source files/folders
    # --------------------------------------------------------------------------
    def _install_content(self):
        """
        Copy source files/folders

        This method copies files and folders from the assets folder of the
        source to their final locations in the user's folder structure.
        """

        # show some info
        print(self.S_MSG_COPY_START, flush=True, end="")

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_INST_CONT, {})

        # for each key, value
        for k, v in content.items():

            # get full paths of source / destination
            src = P_DIR_ASSETS / k
            dst = Path.home() / v / src.name

            # debug may omit certain assets
            if not src.exists():
                continue

            # check for dry run
            if self._dry_run:
                print(self.S_DRY_COPY.format(src, dst))
            else:
                # if the source is a dir
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                # if the src is a file
                else:
                    shutil.copy(src, dst)

        # show some info
        print(self.S_MSG_DONE)

        # just show we are done
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]
        print(self.S_MSG_INST_END.format(prog_name))

    # --------------------------------------------------------------------------
    # Compare two semantic versions
    # --------------------------------------------------------------------------
    def _comp_sem_ver(self, ver_old, ver_new):
        """
        Compare two semantic versions

        Args:
            ver_old: The old version to compare
            ver_new: The new version to compare

        Returns:
            An integer showing the relationship between the two version

        Compare two semantic versions
        """

        # sanity checks
        if not ver_old or ver_old == "":
            return self.I_VER_ERROR
        if not ver_new or ver_new == "":
            return self.I_VER_ERROR
        if ver_old == ver_new:
            return self.I_VER_SAME

        # --------------------------------------------------------------------------

        # compare version string parts (only x.x.x)
        res_old = re.search(self.R_VERSION_VALID, ver_old)
        res_new = re.search(self.R_VERSION_VALID, ver_new)

        # if either version string is None
        if not res_old or not res_new:
            return self.I_VER_ERROR

        # make a list of groups to check
        lst_groups = [
            self.R_VERSION_GROUP_MAJ,
            self.R_VERSION_GROUP_MIN,
            self.R_VERSION_GROUP_REV,
        ]

        # for each part as int
        for group in lst_groups:
            old_val = int(res_old.group(group))
            new_val = int(res_new.group(group))

            # slide out at the first difference
            if old_val < new_val:
                return self.I_VER_NEWER
            if old_val > new_val:
                return self.I_VER_OLDER

        # --------------------------------------------------------------------------

        # still going, check pre
        pre_old = res_old.group(self.R_VERSION_GROUP_PRE)
        pre_new = res_new.group(self.R_VERSION_GROUP_PRE)

        # simple pre rule compare
        if not pre_old and pre_new:
            return self.I_VER_OLDER
        if pre_old and not pre_new:
            return self.I_VER_NEWER
        if not pre_old and not pre_new:
            return self.I_VER_SAME

        # ----------------------------------------------------------------------

        # if pre_old and pre_new:

        # split pre on dots
        lst_pre_old = pre_old.split(".")
        lst_pre_new = pre_new.split(".")

        # get number of parts
        len_pre_old = len(lst_pre_old)
        len_pre_new = len(lst_pre_new)

        # get shorter of two
        shortest = len_pre_old if len_pre_old <= len_pre_new else len_pre_new

        # for each part in shortest
        for index in range(shortest):

            # get each value at position
            old_val = lst_pre_old[index]
            new_val = lst_pre_new[index]

            # 1. both numbers
            if old_val.isdigit() and new_val.isdigit():
                tmp_old_val = int(old_val)
                tmp_new_val = int(new_val)

                # slide out at the first difference
                if tmp_old_val > tmp_new_val:
                    return self.I_VER_OLDER
                if tmp_old_val < tmp_new_val:
                    return self.I_VER_NEWER

            # 2. both alphanumeric
            if not old_val.isdigit() and not new_val.isdigit():
                lst_alpha = [old_val, new_val]
                lst_alpha.sort()

                idx_old = lst_alpha.index(old_val)
                idx_new = lst_alpha.index(new_val)

                if idx_old > idx_new:
                    return self.I_VER_OLDER
                if idx_old < idx_new:
                    return self.I_VER_NEWER

            # 3 num vs alphanumeric
            if old_val.isdigit() and not new_val.isdigit():
                return self.I_VER_OLDER
            if not old_val.isdigit() and new_val.isdigit():
                return self.I_VER_NEWER

            # 4 len
            if len_pre_old > len_pre_new:
                return self.I_VER_OLDER
            if len_pre_new > len_pre_old:
                return self.I_VER_NEWER

        # --------------------------------------------------------------------------

        # error in one or both versions
        return self.I_VER_ERROR


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
