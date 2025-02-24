# ------------------------------------------------------------------------------
# Project : CNlLib                                                 /          \
# Filename: cninstall.py                                          |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The class to use for installing/uninstalling
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
import json
from pathlib import Path
import re
import shutil
import sys

# pylint: disable=import-error
# pylint: disable=no-name-in-module

# local imports
import cnfunctions as F
from cnvenv import CNVenv

# pylint: enable=import-error
# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to wrap errors from the install/uninstall methods
# ------------------------------------------------------------------------------
class CNInstallError(Exception):
    """
    A class to wrap errors from the install/uninstall methods

    This class is used to wrap exceptions from the install/uninstall methods,
    so that a file that uses install/uninstall does not need to import or check
    for all possible failures. The original exception and its properties will
    be exposed by the 'exception' property, but printing will defer to the
    object's repr_str property.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self, message):
        """
        Initialize the class

        Args:
            message: A custom string to print for clarity

        Creates a new instance of the object and initializes its properties.
        """

        # call super constructor
        super().__init__(message)

        # set properties
        self.message = message


# ------------------------------------------------------------------------------
# The class to use for installing/uninstalling
# ------------------------------------------------------------------------------
class CNInstall:
    """
    The class to use for installing/uninstalling
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # keys
    S_KEY_NAME = "NAME"
    S_KEY_VERSION = "VERSION"
    S_KEY_DICT_INSTALL = "DICT_INSTALL"
    S_KEY_LIST_UNINST = "LIST_UNINST"

    # messages
    # NB: format params are prog_name and prog_version
    S_MSG_INST_START = "Installing {}"
    # NB: format param is prog_name
    S_MSG_INST_END = "{} installed"
    # NB: format param is prog_name
    S_MSG_UNINST_START = "Uninstalling {}"
    # NB: format param is prog_name
    S_MSG_UNINST_END = "{} uninstalled"
    # general "done" message
    S_MSG_DONE = "Done"
    # general "fail" message
    S_MSG_FAIL = "Fail"

    # strings for system requirements
    S_MSG_COPY_START = "Copying files... "
    S_MSG_DEL_START = "Deleting files... "
    S_MSG_VENV_START = "Making venv folder... "

    # strings for version compare
    # NB: format param is prog name
    S_ASK_VER_SAME = (
        "The current version of this program is already installed. Do you "
        "want to overwrite? [y/N] "
    )
    S_MSG_VER_ABORT = "Installation aborted"

    # errors
    # NB: format param is cfg file path
    S_ERR_NOT_FOUND = "File {} not found"
    S_ERR_NOT_JSON = "File {} is not a JSON file"
    S_ERR_NO_SUDO = "Could not get sudo permission"
    S_ERR_REQ = "Could not install {}"
    S_ERR_VERSION = "One or both version numbers are invalid"

    # debug option strings
    S_DBG_OPTION = "-d"
    S_DBG_ACTION = "store_true"
    S_DBG_DEST = "DBG_DEST"
    S_DBG_HELP = "enable debugging option"

    # question to ask when installing older version
    S_ASK_VER_OLDER = (
        "A newer version of this program is currently installed. Do you want "
        "to overwrite? [y/N] "
    )
    S_ASK_CONFIRM = "y"

    # regex to compare version numbers
    R_VERSION = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(.*)$"
    R_VERSION_GROUP_MAJ = 1
    R_VERSION_GROUP_MIN = 2
    R_VERSION_GROUP_REV = 3

    # regex for adding user's home to icon path
    R_ICON_SCH = r"^(Icon=)(.*)$"
    R_ICON_REP = r"\g<1>{}"  # Icon=<home/__PP_DESK_ICON__>

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the class

        Creates a new instance of the object and initializes its properties.
        """

        # set properties
        self._debug = False
        self._dict_cfg = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Make install file
    # --------------------------------------------------------------------------
    def make_install_cfg(self, name, version, dict_install):
        """
        Make install file

        Args:
            name: Program name
            version: New version number to compare to any installed version
            dict_install: Dict of assets to install

        Returns:
            A properly formatted install config dict to save to a file

        This method creates a config file for use by install.py. The dict
        format can be found below.
        """

        # create the dict using args
        dict_use = {
            self.S_KEY_NAME: name,
            self.S_KEY_VERSION: version,
            self.S_KEY_DICT_INSTALL: dict_install,
        }

        # return the formatted dict
        return dict_use

    # --------------------------------------------------------------------------
    # Make uninstall file
    # --------------------------------------------------------------------------
    def make_uninstall_cfg(self, name, version, list_uninst):
        """
        Make uninstall file

        Args:
            name: Program name
            version: Initial program version from pyplate.py
            list_uninstall: List of assets to uninstall

        Returns:
            A properly formatted uninstall config dict to save to a file

        This method creates a config file for use by uninstall.py. The dict
        format can be found below.
        """

        # create the dict using args
        dict_use = {
            self.S_KEY_NAME: name,
            self.S_KEY_VERSION: version,
            self.S_KEY_LIST_UNINST: list_uninst,
        }

        # return the formatted dict
        return dict_use

    # --------------------------------------------------------------------------
    # Fix .desktop stuff
    # --------------------------------------------------------------------------
    def fix_desktop_file(self, desk_file, path_icon):
        """
        Fix .desktop stuff

        Args:
            desk_file: abs path to desktop file
            path_icon: path to icon, rel to user home

        Fixes entries in the .desktop file (absolute paths, etc.)
        Currently only fixes absolute path to icon.
        """

        # sanity check
        # NB: in a cli or pkg, this file will not exist
        if not desk_file.exists():
            return

        # open file
        text = ""
        with open(desk_file, "r", encoding="UTF-8") as a_file:
            text = a_file.read()

        # ----------------------------------------------------------------------

        # get installed user's home
        path_icon = Path.home() / path_icon

        # fix abs path to icon
        r_icon_rep = self.R_ICON_REP.format(path_icon)

        # find icon line and fix
        res = re.search(self.R_ICON_SCH, text, flags=re.M)
        if res:
            text = re.sub(self.R_ICON_SCH, r_icon_rep, text, flags=re.M)

        # ----------------------------------------------------------------------

        # write fixed text back to file
        with open(desk_file, "w", encoding="UTF-8") as a_file:
            a_file.write(text)

    # --------------------------------------------------------------------------
    # Install the program
    # --------------------------------------------------------------------------
    def install(
        self,
        dir_assets,
        path_cfg_new,
        path_cfg_old,
        dir_usr_inst,
        dir_venv,
        path_reqs,
        debug=False,
    ):
        """
        Install the program

        Args:
            dir_assets: Path to the assets folder where all of the program
            files are put in dist. This is the base source path to use when
            copying files to the user's computer
            path_cfg_new: Path to the file that contains the current install
            dict info
            path_cfg_old: Path to the currently installed program's install
            dict info
            debug: If True, do not copy files, ony print the action (default:
            False)

        Runs the install operation.
        """

        # get dicts from files
        self._dict_cfg = self._get_dict_from_file(path_cfg_new)

        # get prg name
        prog_name = self._dict_cfg[self.S_KEY_NAME]

        # print start msg
        print(self.S_MSG_INST_START.format(prog_name))

        # set properties
        self._debug = debug

        # make the venv on the user's comp
        self._make_venv(dir_usr_inst, dir_venv, path_reqs)

        # if we did pass an old conf, it must exist (if it doesn't, this could
        # be the first install but we will want to check on later updates)
        if path_cfg_old and Path(path_cfg_old).exists():
            dict_cfg_old = self._get_dict_from_file(path_cfg_old)

            # check versions
            ver_old = dict_cfg_old[self.S_KEY_VERSION]
            ver_new = self._dict_cfg[self.S_KEY_VERSION]
            res = self._do_compare_versions(ver_old, ver_new)

            # same version is installed
            if res == 0:

                # ask to install same version
                str_ask = input(self.S_ASK_VER_SAME)

                # user hit enter or typed anything else except "y"
                if (
                    len(str_ask) == 0
                    or str_ask.lower()[0] != self.S_ASK_CONFIRM
                ):
                    print(self.S_MSG_VER_ABORT)
                    sys.exit(0)

            # newer version is installed
            elif res == -1:

                # ask to install old version over newer
                str_ask = input(self.S_ASK_VER_OLDER)

                # user hit enter or typed anything else except "y"
                if (
                    len(str_ask) == 0
                    or str_ask.lower()[0] != self.S_ASK_CONFIRM
                ):
                    print(self.S_MSG_VER_ABORT)
                    sys.exit(0)

        # print, install, make venv, print
        self._do_install_content(dir_assets)
        print(self.S_MSG_INST_END.format(prog_name))

    # --------------------------------------------------------------------------
    # Uninstall the program
    # --------------------------------------------------------------------------
    def uninstall(self, path_cfg, debug=False):
        """
        Uninstall the program

        Args:
            path_cfg: Path to the file that contains the uninstall dict info
            debug: If True, do not remove files, ony print the action (default:
            False)

        Runs the uninstall operation.
        """

        # set properties
        self._debug = debug

        # get dict from file
        self._dict_cfg = self._get_dict_from_file(path_cfg)

        # get prg name
        prog_name = self._dict_cfg[self.S_KEY_NAME]

        # print, uninstall, print
        print(self.S_MSG_UNINST_START.format(prog_name))
        self._do_uninstall_content()
        print(self.S_MSG_UNINST_END.format(prog_name))

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Make venv for this program on user's computer
    # --------------------------------------------------------------------------
    def _make_venv(self, dir_usr_inst, dir_venv, path_reqs):
        """
        Make venv for this program on user's computer

        Args:
            dir_usr_inst: The program's install folder in which to make a venv
            folder.
            dir_venv: The path tp the venv folder to create.
            path_reqs: Path to the requirements.txt file to add requirements to
            the venv.

        Makes a .venv-XXX folder on the user's computer, and installs the
        required libs.
        """

        # show progress
        print(self.S_MSG_VENV_START, flush=True, end="")

        # do the thing with the thing
        cv = CNVenv(dir_usr_inst, dir_venv)
        try:
            if not self._debug:
                cv.create()
                cv.install(path_reqs)
            print(self.S_MSG_DONE)
        except F.CNShellError as e:
            print(self.S_MSG_FAIL)
            print(e.message)

    # --------------------------------------------------------------------------
    # Open a json file and return the dict inside
    # --------------------------------------------------------------------------
    def _get_dict_from_file(self, path_cfg):
        """
        Open a json file and return the dict inside

        Args:
            path_cfg: Path to the file containing the dict

        Returns:
            The dict contained in the file

        Raises:
            CNInstallError: If something goes wrong

        Opens the specified file and returns the config dict found in it.
        """

        # set conf dict
        try:
            with open(path_cfg, "r", encoding="UTF-8") as a_file:
                return json.load(a_file)

        # file not found
        except FileNotFoundError as e:
            error = CNInstallError(self.S_ERR_NOT_FOUND.format(path_cfg))
            raise error from e

        # not valid json in file
        except json.JSONDecodeError as e:
            error = CNInstallError(self.S_ERR_NOT_JSON.format(path_cfg))
            raise error from e

    # --------------------------------------------------------------------------
    # Copy source files/folders
    # --------------------------------------------------------------------------
    def _do_install_content(self, dir_assets):
        """
        Copy source files/folders

        Args:
            dir_assets: The base dir from which to find install files

        This method copies files and folders from the assets folder of the
        source to their final locations in the user's folder structure.
        """

        print(self.S_MSG_COPY_START, end="", flush=True)

        # get source dir and user home
        inst_home = Path.home()

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_DICT_INSTALL, {})

        # for each key, value
        for k, v in content.items():

            # get full paths of source / destination
            src = dir_assets / k
            dst = inst_home / v / src.name

            # debug may omit certain assets
            if not src.exists():
                continue

            # if the source is a dir
            if src.is_dir():
                if not self._debug:
                    # copy dir
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    print(f"copy dir {src} to {dst}")

            # if the source is a file
            else:
                if not self._debug:
                    # copy file
                    shutil.copy(src, dst)
                else:
                    print(f"copy file {src} to {dst}")

        print(self.S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Remove source files/folders
    # --------------------------------------------------------------------------
    def _do_uninstall_content(self):
        """
        Remove source files/folders

        This method removes files and folders from various locations in the
        user's computer.
        """

        print(self.S_MSG_DEL_START, end="", flush=True)

        # get source dir and user home
        inst_home = Path.home()

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_LIST_UNINST, [])

        # for each key, value
        for item in content:

            # get full path of destination
            dst = inst_home / item

            # debug may omit certain assets
            if not dst.exists():
                continue

            # if the source is a dir
            if dst.is_dir():
                if not self._debug:
                    # copy dir
                    shutil.rmtree(dst)
                else:
                    print(f"rmtree {dst}")

            # if the source is a file
            else:
                if not self._debug:
                    # copy file
                    Path.unlink(dst)
                else:
                    print(f"unlink {dst}")

        print(self.S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Compare two version strings for relativity
    # --------------------------------------------------------------------------
    def _do_compare_versions(self, ver_old, ver_new):
        """
        Compare two version strings for relativity

        Args:
            ver_old: Old version string
            ver_new: New version string

        Returns:
            An integer representing the relativity of the two version strings.
            0 means the two versions are equal,
            1 means new_ver is newer than old_ver (or there is no old_ver), and
            -1 means new_ver is newer than old_ver.

        This method compares two version strings and determines which is older,
        which is newer, or if they are equal. Note that this method converts
        only the first three parts of a semantic version string
        (https://semver.org/).
        """

        # test for new install (don't try to regex)
        if ver_old == "":
            return 1

        # test for equal (just save some cpu cycles)
        if ver_old == ver_new:
            return 0

        # compare version string parts (only x.x.x)
        res_old = re.search(self.R_VERSION, ver_old)
        res_new = re.search(self.R_VERSION, ver_new)

        # if both version strings are valid
        if res_old and res_new:

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
                    return 1
                elif old_val > new_val:
                    return -1
        else:
            raise CNInstallError(self.S_ERR_VERSION)

        # return 0 if equal
        return 0


# -)
