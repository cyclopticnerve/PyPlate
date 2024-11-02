# ------------------------------------------------------------------------------
# Project : CNInstallLib                                           /          \
# Filename: cnuninstall.py                                        |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The class to use for uninstalling

Note that scripts in the preflight and postflight sections of the conf dict
should have their executable bits set and also have a shebang, so they can be
run directly by the run_scripts method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

#  global imports
import json
from pathlib import Path
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
S_KEY_SYS_REQS = "SYS_REQS"
S_KEY_PY_REQS = "PY_REQS"
S_KEY_META = "META"
S_KEY_NAME = "NAME"
S_KEY_VERSION = "VERSION"
S_KEY_PREFLIGHT = "PREFLIGHT"
S_KEY_POSTFLIGHT = "POSTFLIGHT"
S_KEY_CONTENT = "CONTENT"
# values
S_VAL_PIP = "python3-pip"
# cmds
S_CMD_SUDO = "sudo echo -n"

# NB: format param is file path
S_ERR_INST_NOT_FOUND = "Install file {} not found"
S_ERR_INST_NOT_JSON = "Install file {} is not a JSON file"
S_ERR_INST_REQS_SYS = "Could not install system requirement {}"
S_ERR_INST_REQS_PY = "Could not install python requirement {}"
# NB: format param is file path
S_ERR_UNINST_NOT_FOUND = "UniInstall file {} not found"
S_ERR_UNINST_NOT_JSON = "Uninstall file {} is not a JSON file"
S_ERR_UNINST_REQS_SYS = "Could not uninstall system requirement {}"
S_ERR_UNINST_REQS_PY = "Could not uninstall python requirement {}"

S_ERR_NO_SUDO = "Could not get sudo permission"
# these strings make errors look nicer
S_ERR_PREFLIGHT = "preflight"
S_ERR_POSTFLIGHT = "postflight"
# NB: format params are one of the strings above and file path
S_ERR_RUN_SCRIPT = (
    "Could not run {} script {}. Make sure the script has its executable bit "
    "set and has a shebang"
)

# NB: format params are prog_name nad prog_version
S_MSG_INST_START = "Installing {} version {}"
# NB: format params are prog_name
S_MSG_INST_END = "{} installed"
S_MSG_INST_SYS = "Installing system requirements"
S_MSG_INST_PY = "Installing Python requirements"
# NB: format param is item name
S_MSG_INST_ONE = "Installing {}... "

# NB: format params are prog_name nad prog_version
S_MSG_UNINST_START = "Uninstalling {} version {}"
# NB: format params are prog_name
S_MSG_UNINST_END = "{} uninstalled"
S_MSG_UNINST_SYS = "Uninstalling system requirements"
S_MSG_UNINST_PY = "Uninstalling Python requirements"
# NB: format param is item name
S_MSG_UNINST_ONE = "Uninstalling {}... "

S_MSG_INST_SYS_CMD = "sudo apt-get install {} -qq > /dev/null"
S_MSG_INST_PY_CMD = "python -m pip install -q {} > /dev/null"
# NB: format param is key
S_MSG_RUN_SCRIPT = "Running {} scripts"
# NB: format param is val
S_MSG_RUN_SCRIPT_ONE = "Running {}... "
S_MSG_DONE = "Done"

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
    def __init__(self, exception, repr_str):
        """
        Initialize the class

        Arguments:
            exception: The original exception
            repr_str: A custom string to print for clarity.

        Creates a new instance of the object and initializes its properties.
        """

        # set properties
        self.exception = exception
        self.__repr__ = repr_str

# ------------------------------------------------------------------------------
# The class to use for uninstalling
# ------------------------------------------------------------------------------
class CNUninstall:
    """
    The class to use for uninstalling

    This class uninstalls a PyPlate project using the uninstall dict or file
    provided by the run_* methods.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The default initialization of the class
    # --------------------------------------------------------------------------
    def __init__(self, debug=False):
        """
        The default initialization of the class

        Arguments:
            debug: If True, do not uninstall, only print debug info. If False
            (the default), uninstall the program normally. (default: False)

        Creates a new instance of the class and sets the initial properties.
        """

        # new properties
        self._debug = debug

        # default properties
        self._dict_conf = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the uninstall process using a file path
    # --------------------------------------------------------------------------
    def run_file(self, path_conf):
        """
        Run the uninstall process using a file path

        Arguments:
            path_conf: Path to the file containing the uninstall dict

        Raises:
            CNInstallError if something goes wrong

        Runs the uninstaller using a path to a file. This file should contain
        only one dict, and that dict should have the format specified in ???.
        If your uninstall dict is contained in another dict, consider teasing
        it out and using run_dict.
        """

        # set conf dict
        try:
            with open(path_conf, "r", encoding="utf8") as a_file:
                a_dict = json.load(a_file)
                self.run_dict(a_dict)
        except FileNotFoundError as e:
            error = CNInstallError(e, S_ERR_UNINST_NOT_FOUND.format(a_file))
            raise error from e
        except json.JSONDecodeError as e:
            error = CNInstallError(e, S_ERR_UNINST_NOT_JSON.format(a_file))
            raise error from e

    # --------------------------------------------------------------------------
    # Run the uninstall process using a dict
    # --------------------------------------------------------------------------
    def run_dict(self, dict_conf):
        """
        Run the uninstall process using a dict

        Arguments:
            dict_conf: Dict containing install information

        Raises:
            CNInstallError if something went wrong

        Runs the uninstaller using a dict. That dict should have the format
        specified in ???.
        """

        # set dict property
        self._dict_conf = dict_conf

        # check if pip necessary
        sys_reqs = self._dict_conf.get(S_KEY_SYS_REQS, [])
        py_reqs = self._dict_conf.get(S_KEY_PY_REQS, [])
        if len(py_reqs):
            sys_reqs.append(S_VAL_PIP)

        # check if we need sudo password
        if len(sys_reqs) or len(py_reqs):
            try:
                cmd = S_CMD_SUDO
                F.sh(cmd)
            except F.CNShellError as e:
                error = CNInstallError(e, S_ERR_NO_SUDO)
                raise error from e

        # show some text
        prog_name = self._dict_conf[S_KEY_META][S_KEY_NAME]
        prog_version = self._dict_conf[S_KEY_META][S_KEY_VERSION]

        # show some progress
        print(S_MSG_UNINST_START.format(prog_name, prog_version))

        # do each part of conf dict
        self._run_scripts(S_KEY_PREFLIGHT, S_ERR_PREFLIGHT)
        # self._do_sys_reqs()
        # self._do_py_reqs()
        self._do_content()
        self._run_scripts(S_KEY_POSTFLIGHT, S_ERR_POSTFLIGHT)

        # done installing
        print(S_MSG_UNINST_END.format(prog_name))

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Remove source files/folders
    # --------------------------------------------------------------------------
    def _do_content(self):
        """
        Remove source files/folders

        This method remove files and folders from the various folders of the
        # source from their final locations in the user's folder structure.
        """

        # get source dir and user home
        # inst_src = Path(self._dir_assets)
        inst_home = Path.home()

        # content list from dict
        content = self._dict_conf.get(S_KEY_CONTENT, {})
        if len(content) == 0:
            return

        # for each key, value
        for _k, v in content.items():

            # get full paths of destination
            dst = inst_home / v

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
                    print(f"delete{dst}")

    # --------------------------------------------------------------------------
    # Run the scripts from preflight or postflight
    # --------------------------------------------------------------------------
    def _run_scripts(self, step, err):
        """
        Run the scripts from preflight or postflight

        Arguments:
            step: The step to run, either S_KEY_PREFLIGHT or S_KEY_POSTFLIGHT
            err: the name of the step, to make errors look better

        This method is the common code for running preflight/postflight
        scripts. It takes the step (specified by the key name) and runs the
        scripts in the order they are specified.
        """

        # check for empty/no list
        items = self._dict_conf.get(step, [])
        if len(items) == 0:
            return

        # show some text
        print(S_MSG_RUN_SCRIPT.format(err))

        for item in self._dict_conf[step]:

            # show that we are doing something
            print(S_MSG_RUN_SCRIPT_ONE.format(item), end="")

            # get item as cmd line array
            if not self._debug:
                try:
                    F.sh(item)
                except F.CNShellError as e:
                    error = CNInstallError(
                        e, S_ERR_RUN_SCRIPT.format(err, item)
                    )
                    raise error from e

            # done
            print(S_MSG_DONE)

# -)
