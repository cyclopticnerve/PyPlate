# ------------------------------------------------------------------------------
# Project : CNInstallLib                                           /          \
# Filename: cninstall.py                                          |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The class to use for installing/uninstalling

Note that scripts in the preflight and postflight sections of the conf dict
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
DIR_LIB = Path(__file__).parents[1].resolve()
sys.path.append(str(DIR_LIB))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# local imports
from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# keys
S_KEY_META = "META"
S_KEY_INSTALL = "INSTALL"
S_KEY_UNINSTALL = "UNINSTALL"
S_KEY_NAME = "NAME"
S_KEY_VERSION = "VERSION"
S_KEY_PREFLIGHT = "PREFLIGHT"
S_KEY_POSTFLIGHT = "POSTFLIGHT"
S_KEY_ASSETS = "ASSETS"
S_KEY_SYS_REQS = "SYS_REQS"
S_KEY_PY_REQS = "PY_REQS"

# values
S_VAL_PIP = "python3-pip"

# messages
# NB: format params are prog_name nad prog_version
S_MSG_INST_START = "Installing {} version {}"
# NB: format param is prog_name
S_MSG_INST_END = "{} installed"  #
S_MSG_UNINST_START = "Uninstalling {}"
S_MSG_UNINST_END = "{} uninstalled"

# general "done" message
S_MSG_DONE = "Done"

# NB: format param is preflight/postflight key
S_MSG_SCRIPTS_START = "Running {} scripts:"
# NB: format param is preflight/postflight key
S_MSG_SCRIPTS_END = "{} scripts done"
# NB: format param is name of script
S_MSG_SCRIPT_RUN = "  Running {}... "

# strings for system requirements
S_MSG_SYS_START = "Installing system requirements:"
S_MSG_SYS_END = "System requirements done"
# strings for python requirements
S_MSG_PY_START = "Installing python requirements:"
S_MSG_PY_END = "Python requirements done"
# NB: format param is req name
S_MSG_REQ_RUN = "  Installing {}... "
S_MSG_COPY_START = "Copying files... "
S_MSG_DELETE_START = "Deleting files... "

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

# cmds
S_CMD_SUDO = "sudo echo -n"
# NB: format param is req name
S_CMD_SYS_REQ = "sudo apt-get install {} -qq > /dev/null"
# NB: format param is req name
S_CMD_PY_REQ = "python -m pip install -q {} > /dev/null"

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
            message: A custom string to print for clarity.

        Creates a new instance of the object and initializes its properties.
        """

        # call super constructor
        super().__init__(message)

        # set properties
        self.message = message

    # --------------------------------------------------------------------------
    # Provide a human-readable error message when the object is printed
    # --------------------------------------------------------------------------
    def __str__(self):
        """
        Provide a human-readable error message when the object is printed

        This method provides a string representation of the error object when
        it is passed to the print() function.
        """

        # return the message string passed to the constructor
        return self.message

# ------------------------------------------------------------------------------
# The class to use for installing/uninstalling
# ------------------------------------------------------------------------------
class CNInstall:
    """
    The class to use for installing/uninstalling

    Note that scripts in the preflight and postflight sections of the conf dict
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
        self._installing = True
        self._path_assets = None
        self._dict_meta = {}
        self._dict_func = {}
        self._debug = False

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Make install file
    # --------------------------------------------------------------------------
    def make_install_cfg(self, name, version, assets_inst=None, assets_uninst=None):
        """
        Make install file

        Arguments:
            name: The program name
            version: The program version
            assets_inst: the dict of assets to install (default: None)
            assets_uninst: The list of assets to uninstall (default: None)

        Returns:
            A properly formatted install config dict to save to a file

        This method creates a config file for use by both install.py and
        uninstall.py. The dict format can be found below.
        """

        # set default props
        if assets_inst is None:
            assets_inst = {}
        if assets_uninst is None:
            assets_uninst = []

        # create the dict using args
        dict_use = {
            S_KEY_META: {
                S_KEY_NAME: name,
                S_KEY_VERSION: version,
            },
            S_KEY_INSTALL: {
                S_KEY_PREFLIGHT: [],
                S_KEY_POSTFLIGHT: [],
                S_KEY_ASSETS: assets_inst,
                S_KEY_SYS_REQS: [],
                S_KEY_PY_REQS: [],
            },
            S_KEY_UNINSTALL: {
                S_KEY_PREFLIGHT: [],
                S_KEY_POSTFLIGHT: [],
                S_KEY_ASSETS: assets_uninst,
            },
        }

        # return the formatted dict
        return dict_use

    # --------------------------------------------------------------------------
    # Install the program
    # --------------------------------------------------------------------------
    def install(
            self, path_assets, path_conf_new, path_conf_old=None, debug=False
        ):
        """
        Install the program

        Arguments:
            path_assets: Path to the assets folder where all of the program
            files are put in dist. This is the base source path to use when
            copying files to the user's computer
            path_conf_new: Path to the file that contains the current install
            dict info
            path_conf_old: Path to the currently installed program's install
            dict info, or None if not installed (default: None)
            debug: If True, do not copy files, ony print the action (default:
            False)

        Runs the install operation.
        """

        # set properties
        self._installing = True
        self._path_assets = path_assets
        self._debug = debug

        # get dicts from files
        dict_conf_new = self._get_dict_from_file(path_conf_new)
        self._dict_meta = dict_conf_new[S_KEY_META]
        self._dict_func = dict_conf_new[S_KEY_INSTALL]

        # if we did pass an old conf, it must exist (if it doesn't, this could
        # be the first install but we will want to check on later updates)
        if path_conf_old and Path(path_conf_old).exists():
            dict_conf_old = self._get_dict_from_file(path_conf_old)

            # check versions
            ver_old = dict_conf_old[S_KEY_META][S_KEY_VERSION]
            ver_new = self._dict_meta[S_KEY_VERSION]
            res = self._do_compare_versions(ver_old, ver_new)

            # same version is installed
            if res == 0:
                prog_name = self._dict_meta[S_KEY_NAME]
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
        self._run_dict()

    # --------------------------------------------------------------------------
    # Uninstall the program
    # --------------------------------------------------------------------------
    def uninstall(self, path_conf, debug=False):
        """
        Uninstall the program

        Arguments:
            path_conf: Path to the file that contains the uninstall dict info
            debug: If True, do not remove files, ony print the action (default:
            False)

        Runs the uninstall operation.
        """

        # set properties
        self._installing = False
        self._debug = debug

        # get dict from file
        dict_conf = self._get_dict_from_file(path_conf)
        self._dict_meta = dict_conf[S_KEY_META]
        self._dict_func = dict_conf[S_KEY_UNINSTALL]

        # run dict
        self._run_dict()

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
        prog_name = self._dict_meta[S_KEY_NAME]

        # show some progress
        if self._installing:
            prog_version = self._dict_meta[S_KEY_VERSION]
            print(S_MSG_INST_START.format(prog_name, prog_version))

        # we are uninstalling, just go for it
        else:
            print(S_MSG_UNINST_START.format(prog_name))

        # fix py/sys reqs, get sudo
        if self._installing:

            # check if pip necessary
            sys_reqs = self._dict_func.get(S_KEY_SYS_REQS, [])
            py_reqs = self._dict_func.get(S_KEY_PY_REQS, [])
            # TODO: don't need this if venv activated
            if len(py_reqs):
                sys_reqs.append(S_VAL_PIP)

            # check if we need sudo password
            # TODO: don't need len(py_reqs) if venv activated
            if len(sys_reqs) or len(py_reqs):
                try:
                    cmd = S_CMD_SUDO
                    F.sh(cmd)
                except F.CNShellError as e:
                    error = CNInstallError(S_ERR_NO_SUDO)
                    raise error from e

        # do each part of conf dict
        self._run_scripts(S_KEY_PREFLIGHT)
        if self._installing:
            self._do_sys_reqs()
            self._do_py_reqs()
            self._do_install_content()
        else:
            self._do_uninstall_content()
        print(S_MSG_DONE, flush=True)
        self._run_scripts(S_KEY_POSTFLIGHT)

        # done installing
        if self._installing:
            print(S_MSG_INST_END.format(prog_name))
        else:
            print(S_MSG_UNINST_END.format(prog_name))

    # --------------------------------------------------------------------------
    # Open a json file and return the dict inside
    # --------------------------------------------------------------------------
    def _get_dict_from_file(self, path_conf):
        """
        Open a json file and return the dict inside

        Arguments:
            path_conf: Path to the file containing the dict

        Returns:
            The dict contained in the file

        Raises:
            CNInstallError if something goes wrong

        Opens the specified file and returns the config dict found in it.
        """

        # set conf dict
        try:
            with open(path_conf, "r", encoding="UTF-8") as a_file:
                return json.load(a_file)

        # file not found
        except FileNotFoundError as e:
            error = CNInstallError(S_ERR_NOT_FOUND.format(path_conf))
            raise error from e

        # not valid json in file
        except json.JSONDecodeError as e:
            error = CNInstallError(S_ERR_NOT_JSON.format(path_conf))
            raise error from e

    # --------------------------------------------------------------------------
    # Run the scripts from preflight or postflight
    # --------------------------------------------------------------------------
    def _run_scripts(self, key):
        """
        Run the scripts from preflight or postflight

        Arguments:
            key: The step to run, either S_KEY_PREFLIGHT or S_KEY_POSTFLIGHT

        This method is the common code for running preflight/postflight
        scripts. It takes the step (specified by the key name) and runs the
        scripts in the order they are specified.
        """

        # check for empty/no list
        items = self._dict_func.get(key, [])
        if len(items) == 0:
            return

        # show some text
        out = key.lower()
        print(S_MSG_SCRIPTS_START.format(out), flush=True)

        # for each script item
        for item in items:

            # show that we are doing something
            print(S_MSG_SCRIPT_RUN.format(item), end="", flush=True)

            # run script entry
            if not self._debug:
                try:
                    F.sh(item)
                    print(S_MSG_DONE, flush=True)
                except F.CNShellError as e:
                    error = CNInstallError(S_ERR_RUN_SCRIPT.format(item))
                    raise error from e
            else:
                # print output for each script
                print(S_MSG_DONE, flush=True)

    # --------------------------------------------------------------------------
    # Install system requirements
    # --------------------------------------------------------------------------
    def _do_sys_reqs(self):
        """
        Install system requirements

        Raises:
            CNInstallError: If something went wrong

        This method uses the conf dict to install any system requirements
        (i.e. non-python packages) necessary to run your program.
        """

        # check for empty/no list
        items = self._dict_func.get(S_KEY_SYS_REQS, [])
        if len(items) == 0:
            return

        # show some text
        print(S_MSG_SYS_START, flush=True)

        # get system requirements
        for item in items:

            # show that we are doing something
            print(S_MSG_REQ_RUN.format(item), end="", flush=True)

            # install apt reqs
            if not self._debug:
                try:
                    cmd = S_CMD_SYS_REQ.format(item)
                    F.sh(cmd)
                    print(S_MSG_DONE, flush=True)
                except F.CNShellError as e:
                    error = CNInstallError(S_ERR_REQ.format(item))
                    raise error from e
            else:
                # print output for each script
                print(S_MSG_DONE, flush=True)

    # --------------------------------------------------------------------------
    # Install Python requirements
    # --------------------------------------------------------------------------
    def _do_py_reqs(self):
        """
        Install Python requirements

        Raises:
            CNInstallError: If something went wrong

        This method uses the conf dict to install any python requirements
        (i.e. installed with pip) necessary to run your program.
        """

        # check for empty/no list
        items = self._dict_func.get(S_KEY_PY_REQS, [])
        if len(items) == 0:
            return

        # show some text
        print(S_MSG_PY_START, flush=True)

        # get python requirements
        for item in items:

            # show that we are doing something
            print(S_MSG_REQ_RUN.format(item), end="", flush=True)

            # install pip reqs
            if not self._debug:
                try:
                    # FIXME: activate venv
                    cmd = S_CMD_PY_REQ.format(item)
                    F.sh(cmd)
                    print(S_MSG_DONE, flush=True)
                except F.CNShellError as e:
                    error = CNInstallError(S_ERR_REQ.format(item))
                    raise error from e
            else:
                # print output for each script
                print(S_MSG_DONE, flush=True)

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
        inst_src = self._path_assets
        inst_home = Path.home()

        # content list from dict
        content = self._dict_func.get(S_KEY_ASSETS, {})

        # for each key, value
        for k, v in content.items():

            # get full paths of source / destination
            src = inst_src / k
            dst = inst_home / v / src.name

            # if the source is a dir
            if src.is_dir():
                if not self._debug:
                    # copy dir
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                else:
                    print(f"copytree {src} to {dst}")

            # if the source is a file
            else:
                if not self._debug:
                    # copy file
                    shutil.copy(src, dst)
                else:
                    print(f"copy {src} to {dst}")

    # --------------------------------------------------------------------------
    # Remove source files/folders
    # --------------------------------------------------------------------------
    def _do_uninstall_content(self):
        """
        Remove source files/folders

        This method removes files and folders from various locations in the
        user's computer.
        """

        print(S_MSG_DELETE_START, end="", flush=True)

        # get source dir and user home
        inst_home = Path.home()

        # content list from dict
        content = self._dict_func.get(S_KEY_ASSETS, {})

        # create a list of all content dests as well as extras
        l_un = [v for v in content]
        extras = self._dict_func.get(S_KEY_UNINSTALL, [])
        for item in extras:
            l_un.append(item)

        # for each key, value
        for item in l_un:

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
    test_parent = Path(__file__).parent.resolve()

    # get paths to assets and conf for install
    inst_assets = test_parent / "test/assets"
    inst_conf = inst_assets / "test.json"

    # get path to conf for uninstall
    uninst_conf = test_parent / "test/.config/test/test.json"

    # create object
    i = CNInstall()

    # call method
    i.install(inst_assets, inst_conf, uninst_conf, debug=True)
    # i.uninstall(inst_conf, debug=True)


# -)
