# ------------------------------------------------------------------------------
# Project : CNInstallLib                                           /          \
# Filename: cninstallbase.py                                      |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The base class to use for installing/uninstalling

Note that scripts in the preflight and postflight sections of the conf dict
should have their executable bits set and also have a shebang, so they can be
run directly by the run_scripts method.
"""

# FIXME: version check - if already installed:
# if inst version older, continue
# if inst version newer - ask overwrite
#       if yes - continue
#       if no - print "aborted", exit

# FIXME - put subclasses back together to see if that is easier to understand

# FIXME - flowchart of subclasses

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
import json
from pathlib import Path
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
# The base class to use for installing/uninstalling
# ------------------------------------------------------------------------------
class CNInstallBase:
    """
    The base class to use for installing/uninstalling

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
        self._dict_conf = {}
        self._debug = False

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the install process using a file path
    # --------------------------------------------------------------------------
    def run_file(self, path_conf):
        """
        Run the install process using a file path

        Arguments:
            path_conf: Path to the file containing the install dict

        Raises:
            CNInstallError if something goes wrong

        Runs the installer using a path to a file. This file should contain
        only one dict, and that dict should have the format specified in ???.
        If your install dict is contained in another dict, consider teasing it
        out and using run_dict.
        """

        # set conf dict
        try:
            with open(path_conf, "r", encoding="UTF-8") as a_file:
                a_dict = json.load(a_file)
                self.run_dict(a_dict)
        except FileNotFoundError as e:
            error = CNInstallError(e, S_ERR_NOT_FOUND.format(path_conf))
            raise error from e
        except json.JSONDecodeError as e:
            error = CNInstallError(e, S_ERR_NOT_JSON.format(path_conf))
            raise error from e

    # --------------------------------------------------------------------------
    # Run the (un)install process using a dict
    # --------------------------------------------------------------------------
    def run_dict(self, dict_conf):
        """
        Run the uninstall process using a dict

        Arguments:
            dict_conf: Dict containing install information

        Raises:
            CNInstallError if something went wrong

        Runs the uninstaller using a dict. The dict specification is in the
        template file "template/all/install/install.json".
        """

        # set class property
        self._dict_conf = dict_conf

        # check if pip necessary
        sys_reqs = dict_conf.get(S_KEY_SYS_REQS, [])
        py_reqs = dict_conf.get(S_KEY_PY_REQS, [])
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
        self._do_sys_reqs()
        self._do_py_reqs()
        self._do_content()
        self._run_scripts(S_KEY_POSTFLIGHT)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

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
        items = self._dict_conf.get(key, [])
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

        # print output for all scripts
        # title = out.title()
        # print(S_MSG_SCRIPTS_END.format(title), flush=True)

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
        items = self._dict_conf.get(S_KEY_SYS_REQS, [])
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

        # done
        # print(S_MSG_SYS_END, flush=True)

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
        items = self._dict_conf.get(S_KEY_PY_REQS, [])
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

        # done
        # print(S_MSG_PY_END, flush=True)

    # --------------------------------------------------------------------------
    # Dummy function to be overridden
    # --------------------------------------------------------------------------
    def _do_content(self):
        """
        Dummy function to be overridden

        The base implementation of this method does nothing. It should be
        overridden by subclasses to copy or remove contents.
        """

# -)
