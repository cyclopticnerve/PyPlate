# ------------------------------------------------------------------------------
# Project : CNInstall                                              /          \
# Filename: cninstall.py                                          |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""docstring"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
import json
from pathlib import Path
import sys

# find paths to lib
# NB: this assumes cnlib is a "sister" folder to cnapplib
DIR_CNLIB = Path(__file__).parents[1].resolve()

# add paths to import search
sys.path.append(str(DIR_CNLIB))

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
# Define the main class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Dummy class for error class
# ------------------------------------------------------------------------------
class CNInstallError(Exception):
    """
    Dummy class for error class
    """

# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------
class CNInstall:
    """
    The base class for cninstaller/cnuninstaller. Should not be used by
    ANYBODY, EVER. Serious harm may occur. You have been warned, young Jedi.
    """

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self, path_conf):

        """
            The default initialization of the class

            The base method does nothing. It is provided only as a convention.
        """

        # default conf dict
        self._dict_conf = {}

        # set conf dict
        # TODO: catch exc
        with open(path_conf, "r", encoding="utf8") as a_file:
            self._dict_conf = json.load(a_file)

    # --------------------------------------------------------------------------
    # Run the script
    # --------------------------------------------------------------------------
    # def run(self, dict_user):
    #     """
    #     Runs the setup using the supplied user dictionary

    #     Paramaters:
    #         dict_user [dict]: the user dict to get options from

    #     This method takes the user dictionary and does some housekeeping,
    #     such as creating the substitution directory. It also uses
    #     configurator to merge the default and user dicts and apply the
    #     substitutions.
    #     """

    # the defs dict
    # dict_defs = {
    #     "general": {"name": ""},
    #     "preflight": [],
    #     "sys_reqs": [],
    #     "py_reqs": [],
    #     "dirs": [],
    #     "files": {},
    #     "postflight": [],
    # }

    # get current user's home dir
    # home_dir = os.path.expanduser("~")

    # # get location
    # src_dir = os.path.dirname(os.path.abspath(__file__))

    # # the default dict of substitutions
    # dict_subs = {"${HOME}": home_dir, "${SRC}": src_dir}

    # do the config merge
    # NB: allow_user_extras is here for the 'files' section, which will have
    # keys (filenames) we don't know about yet
    # self.dict_conf = configurator.load(
    #     dict_defs, dict_user, dict_subs, allow_user_extras=True
    # )
    # self._dict_conf = dict_user

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Check if we are going to need sudo password and get it now
    # --------------------------------------------------------------------------
    # def _check_sudo(self):

    #     """
    #         Checks if we need sudo permission early in the install

    #         Returns:
    #             [bool]: True if we need sudo permission, False if we don't

    #         This method is used to check if we will need sudo (for sys_reqs or
    #         py_reqs) and ask for the sudo password early in the install process.
    #         This gives a better visual appearance to the process.
    #     """

    # if either of theses steps is required, we need sudo
    # if self._needs_step('sys_reqs') or self._needs_step('py_reqs'):

    #     # ask for sudo password now (no try block 'cause f*** it)
    #     cmd = 'sudo echo -n'
    #     cmd_array = shlex.split(cmd)
    #     subprocess.run(cmd_array, check=True)

    # --------------------------------------------------------------------------
    # Run preflight scripts
    # --------------------------------------------------------------------------
    def _do_preflight(self):

        """
            Run preflight scripts (before we do the heavy lifting)

            This method runs any scripts specified in the preflight section of
            the user dict, in the order they are specified.
        """

        # run preflight scripts
        self._run_scripts('preflight')

    # --------------------------------------------------------------------------
    # Run postflight scripts
    # --------------------------------------------------------------------------
    def _do_postflight(self):

        """
            Run postflight scripts (after we do the heavy lifting)

            This method runs any scripts specified in the postflight section of
            the user dict, in the order they are specified.
        """

        # run postflight scripts
        self._run_scripts('postflight')

    # --------------------------------------------------------------------------
    # Check if a step needs to be performed or can be skipped
    # --------------------------------------------------------------------------
    def _needs_step(self, step):

        """
            Check if an entry in the defs/user needs to be run

            Paramaters:
                step [str]: the step to check for in the final dict

            Returns:
                [bool]:True if the dict contains the step, False otherwise

            This method checks to see if a step (specified by the key name) is
            needed, or if the value is empty. This saves us from printing info
            about a step that will not actually be performed (such as not having
            any preflight scripts to run, etc.).
        """

        # if the section is present
        if step in self._dict_conf:

            # if there are entries in the section
            step_conf = self._dict_conf[step]
            if len(step_conf):
                return True

        # otherwise we can skip this step
        return False

    # --------------------------------------------------------------------------
    # Run preflight/postflight scripts
    # --------------------------------------------------------------------------
    def _run_scripts(self, step):

        """
        Runs the scripts from preflight or postflight

        Paramaters:
            step [str]: The step to run, either preflight or postflight

        This method is the common code for running preflight/postflight
        scripts. It takes the step (specified by the key name) and runs the
        scripts in the order they are specified.
        """

        # check for empty/no list
        if not self._needs_step(step):
            return

        # show some text
        print(f'install running {step} scripts')

        for item in self._dict_conf[step]:

            # show that we are doing something
            print(f'install running {item}... ', end='')

            # get item as cmd line array
            F.sh(item)

            # done
            print("Done")

# -)
