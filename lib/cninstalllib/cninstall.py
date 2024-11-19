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

# FIXME: version check - if already installed:
# if inst version older, continue
# if inst version newer - ask overwrite
#       if yes - continue
#       if no - print "aborted", exit

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
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
S_KEY_META = "META"
S_KEY_INSTALL = "INSTALL"
S_KEY_UNINSTALL = "UNINSTALL"
S_KEY_NAME = "NAME"
S_KEY_VERSION = "VERSION"
S_KEY_PREFLIGHT = "PREFLIGHT"
S_KEY_POSTFLIGHT = "POSTFLIGHT"
S_KEY_CONTENT = "CONTENT"
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

# cmds
S_CMD_SUDO = "sudo echo -n"
# NB: format param is req name
S_CMD_SYS_REQ = "sudo apt-get install {} -qq > /dev/null"
# NB: format param is req name
S_CMD_PY_REQ = "python -m pip install -q {} > /dev/null"


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
        self._debug = False
        self._path_assets = None
        self._dict_meta = {}
        self._dict_func = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Install using file path
    # --------------------------------------------------------------------------
    def install_file(self, path_assets, path_conf, debug=False):
        """
        Install using file path

        Arguments:
            path_assets: Path to the assets folder where all of the program
            files are put in dist
            path_conf: Path to the file that contains the install dict info
            debug: If True, do not copy files, ony print the action (default:
            False)

        Runs the installer using a file.
        """

        # set properties
        self._installing = True
        self._debug = debug
        self._path_assets = path_assets

        # get dicts from file
        dict_conf = self._get_dict_from_file(path_conf)
        self._dict_meta = dict_conf[S_KEY_META]
        self._dict_func = dict_conf[S_KEY_INSTALL]

        # run dict
        self._run_dict()

    # --------------------------------------------------------------------------
    # Install using dict
    # --------------------------------------------------------------------------
    def install_dict(self, path_assets, dict_conf, debug=False):
        """
        Install using dict

        Arguments:
            path_assets: Path to the assets folder where all of the program
            files are put in dist
            dict_conf: The install dict info
            debug: If True, do not copy files, ony print the action (default:
            False)

        Runs the installer using a dict.
        """

        # set properties
        self._installing = True
        self._debug = debug
        self._path_assets = path_assets
        self._dict_meta = dict_conf[S_KEY_META]
        self._dict_func = dict_conf[S_KEY_INSTALL]

        # run dict
        self._run_dict()

    # --------------------------------------------------------------------------
    # Uninstall using file path
    # --------------------------------------------------------------------------
    def uninstall_file(self, path_conf, debug=False):
        """
        Uninstall using file path

        Arguments:
            path_conf: Path to the file that contains the uninstall dict info
            debug: If True, do not remove files, ony print the action (default:
            False)

        Runs the uninstaller using a file.
        """

        # set properties
        self._installing = False
        self._debug = debug

        # set dicts from file
        dict_conf = self._get_dict_from_file(path_conf)
        self._dict_meta = dict_conf[S_KEY_META]
        self._dict_func = dict_conf[S_KEY_UNINSTALL]

        # run dict
        self._run_dict()

    # --------------------------------------------------------------------------
    # Uninstall using dict
    # --------------------------------------------------------------------------
    def uninstall_dict(self, dict_conf, debug=False):
        """
        Uninstall using dict

        Arguments:
            dict_conf: The install dict info
            debug: If True, do not remove files, ony print the action (default:
            False)
        Runs the uninstaller using a dict.
        """

        # set properties
        self._installing = False
        self._debug = debug
        self._dict_meta = dict_conf[S_KEY_META]
        self._dict_func = dict_conf[S_KEY_UNINSTALL]

        # run dict
        self._run_dict()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the install process using a file path
    # --------------------------------------------------------------------------
    def _get_dict_from_file(self, path_conf):
        """
        Get the config dict using a file path

        Arguments:
            path_conf: Path to the file containing the install dict

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
        except FileNotFoundError as e:
            error = CNInstallError(e, S_ERR_NOT_FOUND.format(path_conf))
            raise error from e
        except json.JSONDecodeError as e:
            error = CNInstallError(e, S_ERR_NOT_JSON.format(path_conf))
            raise error from e

    # --------------------------------------------------------------------------
    # Run the (un)install process using a dict
    # --------------------------------------------------------------------------
    def _run_dict(self):
        """
        Run the (un)install process using a dict

        Raises:
            CNInstallError if something went wrong

        Runs the (un)install process using a dict. The dict specification is in
        the template file "template/all/install/install.json".
        """

        # get prog name
        prog_name = self._dict_meta[S_KEY_NAME]

        # show some progress
        if self._installing:
            prog_version = self._dict_meta[S_KEY_VERSION]
            print(S_MSG_INST_START.format(prog_name, prog_version))
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
                    error = CNInstallError(e, S_ERR_NO_SUDO)
                    raise error from e

        # do each part of conf dict
        self._run_scripts(S_KEY_PREFLIGHT)
        if self._installing:
            self._do_sys_reqs()
            self._do_py_reqs()
            self._do_install_content()
        else:
            self._do_uninstall_content()
        self._run_scripts(S_KEY_POSTFLIGHT)

        # done installing
        if self._installing:
            print(S_MSG_INST_END.format(prog_name))
        else:
            print(S_MSG_UNINST_END.format(prog_name))

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
                    error = CNInstallError(e, S_ERR_RUN_SCRIPT.format(item))
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
                    error = CNInstallError(e, S_ERR_REQ.format(item))
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
                    error = CNInstallError(e, S_ERR_REQ.format(item))
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

        # get source dir and user home
        inst_src = self._path_assets
        inst_home = Path.home()

        # content list from dict
        content = self._dict_func.get(S_KEY_CONTENT, {})

        # for each key, value
        for k, v in content.items():

            # get full paths of source / destination
            src = inst_src / k
            dst = inst_home / v

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

        # get source dir and user home
        inst_home = Path.home()

        # content list from dict
        content = self._dict_func.get(S_KEY_CONTENT, {})

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


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # testing
    test_self = Path(__file__).parent.resolve()

    test_assets = test_self / "test/assets"
    test_conf = test_assets / "test.json"

    i = CNInstall()
    # i.install_file(test_assets, test_conf, debug=True)
    i.uninstall_file(test_conf, debug=True)


# -)
