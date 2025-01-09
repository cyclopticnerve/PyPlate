# ------------------------------------------------------------------------------
# Project : CNInstallLib                                           /          \
# Filename: cninstall.py                                          |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The class to use for installing/uninstalling

Note that scripts in the preflight and postflight sections of the cfg dict
should have their executable bits set and also have a shebang, so they can be
run directly by the run_scripts method.
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

# find paths to lib
DIR_SELF = Path(__file__).parent.resolve()
DIR_LIB = Path(__file__).parents[1].resolve()
sys.path.append(str(DIR_LIB))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# local imports
from cnlib import cnfunctions as F  # type: ignore
# from cnlib.cnvenv import CNVenv ## type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# keys
S_KEY_NAME = "NAME"
S_KEY_VERSION = "VERSION"
# S_KEY_DIR_PRE = "DIR_PRE"
# S_KEY_DIR_POST = "DIR_POST"
# S_KEY_ASSETS = "ASSETS"
S_KEY_DICT_INSTALL = "DICT_INSTALL"
S_KEY_LIST_UNINST = "LIST_UNINST"

# messages
# NB: format params are prog_name and prog_version
S_MSG_INST_START = "Installing {} version {}"
# NB: format param is prog_name
S_MSG_INST_END = "{} installed"
# NB: format param is prog_name
S_MSG_UNINST_START = "Uninstalling {}"
# NB: format param is prog_name
S_MSG_UNINST_END = "{} uninstalled"

# general "done" message
S_MSG_DONE = "Done"
# S_MSG_PREFLIGHT = "preflight"
# S_MSG_POSTFLIGHT = "postflight"

# # NB: format param is preflight/postflight key
# S_MSG_SCRIPTS_START = "Running {} scripts:"
# # NB: format param is preflight/postflight key
# S_MSG_SCRIPTS_END = "{} scripts done"
# # NB: format param is name of script
# S_MSG_SCRIPT_RUN = "  Running {}... "

# strings for system requirements
S_MSG_COPY_START = "Copying files... "
S_MSG_DEL_START = "Deleting files... "
S_MSG_VENV_START = "Making virtual environment... "

# strings for version compare
# NB: format param is prog name
S_MSG_VER_SAME = "The current version of {} is already installed"
S_MSG_VER_ABORT = "Installation aborted"

# errors
# NB: format param is cfg file path
S_ERR_NOT_FOUND = "File {} not found"
S_ERR_NOT_JSON = "File {} is not a JSON file"
S_ERR_NO_SUDO = "Could not get sudo permission"
# NB: format param is script file path
S_ERR_RUN_SCRIPT = (
    "Could not run script {}. Make sure the script has its executable bit "
    "set and has a shebang"
)
S_ERR_REQ = "Could not install {}"
S_ERR_VERSION = "One or both version numbers are invalid"

# debug option strings
S_DBG_OPTION = "-d"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP = "enable debugging option"

# question to ask when installing older version
S_ASK_OVER = (
    "A newer version of this program is currently installed. Do you want to "
    "overwrite? [y/N] "
)
S_ASK_CONFIRM = "y"

# regex to compare version numbers
R_VERSION = r"(\d).(\d).(\d)(.*)"
R_VERSION_GROUP_MAJ = 1
R_VERSION_GROUP_MIN = 2
R_VERSION_GROUP_REV = 3

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

        Arguments:
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

    Note that scripts in the preflight and postflight sections of the cfg dict
    should have their executable bits set and also have a shebang, so they can
    be run directly by the run_scripts method.
    """

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
        self._dir_base = Path()
        self._debug = False
        self._installing = True
        self._dict_cfg = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Make install file
    # --------------------------------------------------------------------------
    def make_install_cfg(
        self,
        name,
        version,
        # dir_pre, dir_post,
        dict_install,
    ):
        """
        Make install file

        Arguments:
            name: Program name
            dir_pre: Path to preflight script dir
            dir_post: Path th postflight script dir
            dict_install: Dict of assets to install

        Returns:
            A properly formatted install config dict to save to a file

        This method creates a config file for use by install.py. The dict
        format can be found below.
        """

        # create the dict using args
        dict_use = {
            S_KEY_NAME: name,
            S_KEY_VERSION: version,
            # S_KEY_DIR_PRE: dir_pre,
            # S_KEY_DIR_POST: dir_post,
            S_KEY_DICT_INSTALL: dict_install,
        }

        # return the formatted dict
        return dict_use

    # --------------------------------------------------------------------------
    # Make uninstall file
    # --------------------------------------------------------------------------
    def make_uninstall_cfg(
            self,
            name,
            version,
            # dir_pre,
            # dir_post,
            list_uninst
        ):
        """
        Make uninstall file

        Arguments:
            name: Program name
            version: Initial program version from pyplate_conf.py
            dir_pre: Path to preflight script dir
            dir_post: Path th postflight script dir
            list_uninstall: List of assets to uninstall

        Returns:
            A properly formatted uninstall config dict to save to a file

        This method creates a config file for use by uninstall.py. The dict
        format can be found below.
        """

        # create the dict using args
        dict_use = {
            S_KEY_NAME: name,
            S_KEY_VERSION: version,
            # S_KEY_DIR_PRE: dir_pre,
            # S_KEY_DIR_POST: dir_post,
            S_KEY_LIST_UNINST: list_uninst,
        }

        # return the formatted dict
        return dict_use

    # --------------------------------------------------------------------------
    # Install the program
    # --------------------------------------------------------------------------
    def install(self, dir_base, path_cfg_new, path_cfg_old, debug=False):
        """
        Install the program

        Arguments:
            dir_base: Path to the assets folder where all of the program
            files are put in dist. This is the base source path to use when
            copying files to the user's computer
            path_cfg_new: Path to the file that contains the current install
            dict info
            path_cfg_old: Path to the currently installed program's install
            dict info, or None if not installed (default: None)
            debug: If True, do not copy files, ony print the action (default:
            False)

        Runs the install operation.
        """

        # set properties
        self._dir_base = Path(dir_base).resolve()
        self._debug = debug
        self._installing = True

        # get dicts from files
        dict_cfg_new = self._get_dict_from_file(path_cfg_new)

        # if we did pass an old conf, it must exist (if it doesn't, this could
        # be the first install but we will want to check on later updates)
        if path_cfg_old and Path(path_cfg_old).exists():
            dict_cfg_old = self._get_dict_from_file(path_cfg_old)

            # check versions
            ver_old = dict_cfg_old[S_KEY_VERSION]
            ver_new = dict_cfg_new[S_KEY_VERSION]
            res = self._do_compare_versions(ver_old, ver_new)

            # same version is installed
            if res == 0:
                prog_name = dict_cfg_new[S_KEY_NAME]
                print(S_MSG_VER_SAME.format(prog_name))
                sys.exit(0)

            # newer version is installed
            elif res == -1:

                # ask to install old version over newer
                str_ask = input(S_ASK_OVER)

                # user hit enter or typed anything else except "y"
                if len(str_ask) == 0 or str_ask.lower()[0] != S_ASK_CONFIRM:
                    print(S_MSG_VER_ABORT)
                    sys.exit(0)

        # run dict
        self._dict_cfg = dict_cfg_new
        self._run_dict()

    # --------------------------------------------------------------------------
    # Uninstall the program
    # --------------------------------------------------------------------------
    def uninstall(self, path_cfg, debug=False):
        """
        Uninstall the program

        Arguments:
            path_cfg: Path to the file that contains the uninstall dict info
            debug: If True, do not remove files, ony print the action (default:
            False)

        Runs the uninstall operation.
        """

        # set properties
        self._debug = debug
        self._installing = False

        # get dict from file
        self._dict_cfg = self._get_dict_from_file(path_cfg)

        # run dict
        self._run_dict()

    # --------------------------------------------------------------------------
    # Fix desktop abs path to icon
    # --------------------------------------------------------------------------
    def fix_desktop_icon(self, desk_file):
        """
        Fix desktop abs path to icon

        Arguments:
            desk_file: abs path to desktop file

        Fixes the abs path to the desktop file's icon based on installed user's
        home dir.
        """

        # get installed user's home
        home = Path.home()

        # open file
        with open(desk_file, "r", encoding="UTF-8") as a_file:
            lines = a_file.readlines()

            # scan and fix icon path
            for index, line in enumerate(lines):
                if line.startswith("Icon="):
                    icon_rel_path = line.split("=")[1]
                    icon_abs_path = home / icon_rel_path
                    line = "Icon=" + str(icon_abs_path)
                    lines[index] = line

        # save file
        with open(desk_file, "w", encoding="UTF-8") as a_file:
            a_file.writelines(lines)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the (un)install process using dicts
    # --------------------------------------------------------------------------
    def _run_dict(self):
        """
        Run the (un)install process using a dict

        Raises:
            CNInstallError if something went wrong

        Runs the (un)install process using a dict. The dict specification is in
        the template file "template/all/install/install.json". This is the meat
        of the program, doing most of the work and/or delegating to sub
        functions.
        """

        # get prog name
        prog_name = self._dict_cfg[S_KEY_NAME]

        # show some progress
        if self._installing:
            prog_version = self._dict_cfg[S_KEY_VERSION]
            print(S_MSG_INST_START.format(prog_name, prog_version))

        # we are uninstalling, just go for it
        else:
            print(S_MSG_UNINST_START.format(prog_name))

        # do each part of conf dict

        # run preflight
        # self._run_scripts(S_KEY_DIR_PRE)

        # run content
        if self._installing:
            self._do_install_content()
        else:
            self._do_uninstall_content()

        # run postflight
        # self._run_scripts(S_KEY_DIR_POST)

        # done installing
        if self._installing:
            print(S_MSG_INST_END.format(prog_name))
        else:
            print(S_MSG_UNINST_END.format(prog_name))

    # --------------------------------------------------------------------------
    # Open a json file and return the dict inside
    # --------------------------------------------------------------------------
    def _get_dict_from_file(self, path_cfg):
        """
        Open a json file and return the dict inside

        Arguments:
            path_cfg: Path to the file containing the dict

        Returns:
            The dict contained in the file

        Raises:
            CNInstallError if something goes wrong

        Opens the specified file and returns the config dict found in it.
        """

        # set conf dict
        try:
            with open(path_cfg, "r", encoding="UTF-8") as a_file:
                return json.load(a_file)

        # file not found
        except FileNotFoundError as e:
            error = CNInstallError(S_ERR_NOT_FOUND.format(path_cfg))
            raise error from e

        # not valid json in file
        except json.JSONDecodeError as e:
            error = CNInstallError(S_ERR_NOT_JSON.format(path_cfg))
            raise error from e

    # --------------------------------------------------------------------------
    # Copy source files/folders
    # --------------------------------------------------------------------------
    def _do_install_content(self):
        """
        Copy source files/folders

        This method copies files and folders from the assets folder of the
        source to their final locations in the user's folder structure.
        """

        print(S_MSG_COPY_START, end="", flush=True)

        # get source dir and user home
        inst_src = self._dir_base
        inst_home = Path.home()

        # content list from dict
        content = self._dict_cfg.get(S_KEY_DICT_INSTALL, {})

        # for each key, value
        for k, v in content.items():

            # get full paths of source / destination
            src = inst_src / k
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

        print(S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Remove source files/folders
    # --------------------------------------------------------------------------
    def _do_uninstall_content(self):
        """
        Remove source files/folders

        This method removes files and folders from various locations in the
        user's computer.
        """

        print(S_MSG_DEL_START, end="", flush=True)

        # get source dir and user home
        inst_home = Path.home()

        # content list from dict
        content = self._dict_cfg.get(S_KEY_LIST_UNINST, {})

        # for each key, value
        for item in content:

            # get full path of destination
            dst = inst_home / item

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

        print(S_MSG_DONE)

    # --------------------------------------------------------------------------
    #
    # --------------------------------------------------------------------------
    def _make_venv(self):
        """docstring"""

        # print(S_MSG_VENV_START, flush=True, end="")

        # # FIXME: make venv and install reqs on USER'S computer

        # # get name ov venv folder and reqs file
        # dir_venv = C.D_PRV_PRJ["__PP_NAME_VENV__"]
        # file_reqs = C.D_PRV_PRJ["__PP_PATH_REQS__"]
        # file_reqs = self._dir_prj / C.S_FILE_REQS

        # # do the thing with the thing
        # cv = CNVenv(self._dir_prj, dir_venv)
        # try:
        #     cv.create()
        #     cv.install(file_reqs)
        #     print(C.S_ACTION_DONE)
        # except F.CNShellError as e:
        #     print(C.S_ACTION_FAIL)
        #     print(e.message)

        # print(S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Run the scripts from preflight or postflight
    # --------------------------------------------------------------------------
    # def _run_scripts(self, key):
    #     """
    #     Run the scripts from preflight or postflight

    #     Arguments:
    #         key: The step to run, either S_KEY_PREFLIGHT or S_KEY_POSTFLIGHT

    #     This method is the common code for running preflight/postflight
    #     scripts. It takes the step (specified by the key name) and runs the
    #     scripts in the order they are specified.
    #     """

    #     print("1")

    #     # get the subdir for the key
    #     path_scripts = self._dict_cfg.get(key, "")
    #     if path_scripts != "":
    #         path_scripts = Path(path_scripts).resolve()
    #     else:
    #         return

    #     print(path_scripts)

    #     # scan key dir
    #     for root, _root_dirs, root_files in path_scripts.walk():

    #         # convert files into Paths
    #         files = [root / f for f in root_files]

    #         # if no files, skip
    #         if len(files) == 0:
    #             continue

    #         # show some text
    #         print(S_MSG_SCRIPTS_START.format(key), flush=True)

    #         # for each script item
    #         for file in files:

    #             full_file = file.resolve()

    #             # run script entry
    #             if not self._debug:

    #                 # show that we are doing something
    #                 print(
    #                     S_MSG_SCRIPT_RUN.format(full_file.name),
    #                     end="",
    #                     flush=True,
    #                 )

    #                 # get full path rel to assets
    #                 new_item = str(full_file)

    #                 try:
    #                     F.sh(new_item)
    #                     # print output for each script
    #                     print(S_MSG_DONE, flush=True)
    #                 except F.CNShellError as e:
    #                     error = CNInstallError(
    #                         S_ERR_RUN_SCRIPT.format(new_item)
    #                     )
    #                     raise error from e

    #             else:
    #                 # print output for each script
    #                 print(f"run script: {full_file}")
    #                 print(S_MSG_DONE, flush=True)

    # --------------------------------------------------------------------------
    # Compare two version strings for relativity
    # --------------------------------------------------------------------------
    def _do_compare_versions(self, ver_old, ver_new):
        """
        Compare two version strings for relativity

        Arguments:
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
        (https://semver.org/). It also converts the string parts to integers,
        so the versions "0.0.1" and "0.0.01" are considered equal.
        """

        # test for new install (don't try to regex)
        if ver_old == "":
            return 1

        # test for equal (just save some cpu cycles)
        if ver_old == ver_new:
            return 0

        # compare version string parts (only x.x.x)
        res_old = re.search(R_VERSION, ver_old)
        res_new = re.search(R_VERSION, ver_new)

        # if both version strings are valid
        if res_old and res_new:

            # make a list of groups to check
            lst_groups = [
                R_VERSION_GROUP_MAJ,
                R_VERSION_GROUP_MIN,
                R_VERSION_GROUP_REV,
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
            raise CNInstallError(S_ERR_VERSION)

        # return 0 if equal
        return 0


# ------------------------------------------------------------------------------

if __name__ == "__main__":

    # testing

    # get parent
    test_parent = Path(__file__).parent.resolve()  # cnlib
    test_prj = test_parent / "cninstall_test"
    test_dist = test_prj / "dist"
    test_assets = test_dist / "assets"

    test_install = test_assets / "install"
    test_inst_pre = test_install / "preflight"
    test_inst_post = test_install / "postflight"

    test_uninstall = test_assets / "uninstall"
    test_uninst_pre = test_uninstall / "preflight"
    test_uninst_post = test_uninstall / "postflight"

    # create object
    i = CNInstall()

    # make inst cfg dict
    test_install_dict = i.make_install_cfg(
        "test",
        "0.0.1",
        #test_inst_pre,
        # test_inst_post,
        {"test.py": "test.py"}
    )

    # print inst cfg dict
    F.pp(test_install_dict, label="inst")

    # make inst cfg dict
    test_uninst_dict = i.make_uninstall_cfg(
        "test",
        "0.0.1",
        # test_uninst_pre,
        # test_uninst_post,
        ["test.py"],
    )

    # print inst cfg dict
    F.pp(test_uninst_dict, label="uninst")

    # call methods
    # i.install(inst_assets, inst_cfg, None, debug=True)
    # i.uninstall(inst_cfg, debug=True)


# -)
