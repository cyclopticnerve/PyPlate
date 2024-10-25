# ------------------------------------------------------------------------------
# Project : CNInstall                                              /          \
# Filename: cninstaller.py                                        |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The class to use for installing.
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
# NB: this assumes cninstall is a "sister" folder to cnlib
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

class CNInstaller:
    """
    The class to use for installing.
    """

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    def __init__(self, dir_assets, debug=False):
        """
        The default initialization of the class

        Creates a new instance of the class and set initial properties.
        """

        # default properties
        self._dict_conf = {}

        # new properties
        # the dir where the install.py is being run
        self._dir_assets = dir_assets
        # set debug prop
        self._debug = debug

    # --------------------------------------------------------------------------
    # Run the install process using a file path
    # --------------------------------------------------------------------------
    def run_file(self, a_file):
        """
        Run the install process using a file path
        """

        # set conf dict
        try:
            with open(a_file, "r", encoding="utf8") as a_file:
                a_dict = json.load(a_file)
                self.run_dict(a_dict)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Install file could not be found or is not a JSON file")
            sys.exit(-1)

    # --------------------------------------------------------------------------
    # Run the install process using a dict
    # --------------------------------------------------------------------------
    def run_dict(self, a_dict):
        """
        Run the install process using a dict

        This method is the main function of the class. It performs the
        various steps required to install a python program, and should be
        the only method called by your install.py file.
        """

        # set dict property
        self._dict_conf = a_dict

        # check if pip necessary
        sys_reqs = self._dict_conf.get("sys_reqs", [])
        py_reqs = self._dict_conf.get("py_reqs", [])
        if py_reqs and len(py_reqs):
            sys_reqs.append("python3-pip")

        # check if we need sudo password
        if len(sys_reqs) or len(py_reqs):
            cmd = "sudo echo -n"
            F.sh(cmd)

        # show some text
        prog_name = self._dict_conf["meta"]["name"]
        prog_version = self._dict_conf["meta"]["version"]

        # TODO: check for version number? needs to be stored on user's comp
        # somewhere
        # don't install older version

        print(f"Installing {prog_name} version {prog_version}")

        # do each part of conf dict
        self._run_scripts("preflight")
        self._do_sys_reqs()
        self._do_py_reqs()
        self._do_content()
        self._run_scripts("postflight")

        # done installing
        print(f"{prog_name} installed")

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Install system requirements
    # --------------------------------------------------------------------------
    def _do_sys_reqs(self):
        """
        Install system requirements

        This method uses the conf dict to install any system requirements
        (i.e. non-python packages) necessary to run your program.
        """

        # check for empty/no list
        items = self._dict_conf.get("sys_reqs", None)
        if not items or len(items) == 0:
            return

        # show some text
        print("Installing system requirements")

        # get system requirements
        for item in items:

            # show that we are doing something
            print(f"Installing {item}... ", end="")

            # install apt reqs
            if not self._debug:
                cmd = f"sudo apt-get install {item} -qq > /dev/null"
                F.sh(cmd)

            # done
            print("Done")

    # --------------------------------------------------------------------------
    # Install Python requirements
    # --------------------------------------------------------------------------
    def _do_py_reqs(self):
        """
        Install Python requirements

        This method uses the conf dict to install any python requirements
        (i.e. installed with pip) necessary to run your program.
        """

        # check for empty/no list
        items = self._dict_conf.get("py_reqs", None)
        if not items or len(items) == 0:
            return

        # show some text
        print("Installing Python requirements")

        # get python requirements
        for item in items:

            # show that we are doing something
            print(f"Installing {item}... ", end="")

            # install pip reqs
            if not self._debug:
                cmd = f"python -m pip install -q {item} > /dev/null"
                F.sh(cmd)

            # done
            print("Done")

    # --------------------------------------------------------------------------
    # Copy source files/folders
    # --------------------------------------------------------------------------
    def _do_content(self):
        """
        Copy source files/folders

        This method copies files and folders from the assets folder of the
        source to their final locations in the user's folder structure.
        """

        # get source dir and user home
        inst_src = Path(self._dir_assets)
        inst_home = Path.home()

        # content list from dict
        content = self._dict_conf.get("content", None)
        if not content:
            return

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
                    # TODO: make sure the dst dir exists
                    shutil.copy2(src, dst)
                else:
                    print(f"copy2 {src} to {dst}")

    # --------------------------------------------------------------------------
    # Runs the scripts from preflight or postflight
    # --------------------------------------------------------------------------
    def _run_scripts(self, step):
        """
        Runs the scripts from preflight or postflight

        Arguments:
            step [str]: The step to run, either "preflight" or "postflight"

        This method is the common code for running preflight/postflight
        scripts. It takes the step (specified by the key name) and runs the
        scripts in the order they are specified.
        """

        # check for empty/no list
        items = self._dict_conf.get(step, None)
        if not items or len(items) == 0:
            return

        # show some text
        print(f"Running {step} scripts")

        for item in self._dict_conf[step]:

            # show that we are doing something
            print(f"Running {item}... ", end="")

            # get item as cmd line array
            if not self._debug:
                F.sh(item)

            # done
            print("Done")

# -)
