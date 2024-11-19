# ------------------------------------------------------------------------------
# Project : CNInstallLib                                           /          \
# Filename: cninstall.py                                          |     ()     |
# Date    : 09/23/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The class to use for installing

Note that scripts in the preflight and postflight sections of the conf dict
should have their executable bits set and also have a shebang, so they can be
run directly by the run_scripts method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
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
from cninstalllib import cninstallbase as B  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# NB: format params are prog_name nad prog_version
S_MSG_START = "Installing {} version {}"
# NB: format param is prog_name
S_MSG_END = "{} installed"

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# The class to use for installing
# ------------------------------------------------------------------------------
class CNInstall(B.CNInstallBase):
    """
    The class to use for installing

    This class installs a PyPlate project using the install dict or file
    provided by the run_* methods.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self, path_assets, debug=False):
        """
        Initialize the class

        Arguments:
            path_assets: Path to the folder where the program files are stored
            before being installed
            debug: If True, do not copy files/folders, only print the source
            and destination values (default: False)

        Creates a new instance of the object and initializes its properties.
        """

        # init base class
        super().__init__()

        # set properties
        self._path_assets = path_assets
        self._debug = debug

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

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
        template file "template/all/install/install.json". This method is
        overridden to print custom strings before and after installing.
        """

        # show some text
        prog_name = dict_conf[B.S_KEY_META][B.S_KEY_NAME]
        prog_version = dict_conf[B.S_KEY_META][B.S_KEY_VERSION]

        # show some progress
        print(S_MSG_START.format(prog_name, prog_version))

        super().run_dict(dict_conf)

        # done installing
        print(S_MSG_END.format(prog_name))

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

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
        inst_src = self._path_assets
        inst_home = Path.home()

        # content list from dict
        content = self._dict_conf.get(B.S_KEY_CONTENT, {})

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

# -)

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    # testing
    test_self = Path(__file__).parent.resolve()

    test_assets = test_self / "test/assets"
    test_conf = test_assets / "test.json"

    i = CNInstall(test_assets, debug=True)
    i.run_file(test_conf)

# -)
