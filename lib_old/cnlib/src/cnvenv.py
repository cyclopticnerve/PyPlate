# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnvenv.py                                             |     ()     |
# Date    : 10/11/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to make handling of venv folders easier
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path

# cnlib imports
import cnfunctions as F

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to make handling of venv folders easier
# ------------------------------------------------------------------------------
class CNVenv:
    """
    A class to make handling of venv folders easier

    Methods:
        create: Creates a new venv given the __init__ params
        install_reqs: Install packages to venv from the reqs_file property
        freeze: Freeze packages in the venv folder to the file_reqs property

    This class provides methods to create, freeze, and install dependencies
    in the project's venv folder.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # NB format param is self._dir_venv
    S_CMD_CREATE = "python -Xfrozen_modules=off -m venv {}"
    # NB: format params are venv.parent, venv.name, path to reqs file
    S_CMD_INSTALL = "cd {};. ./{}/bin/activate;python -m pip install -r {}"
    # NB: format params are venv.parent, venv.name, path to reqs file
    S_CMD_FREEZE = (
        "cd {}; "
        ". ./{}/bin/activate; "
        "python "
        "-Xfrozen_modules=off "
        "-m pip freeze "
        "-l --exclude-editable "
        "--require-virtualenv "
        "> "
        "{}"
    )

    # error messages
    # NB: format param is dir_prj
    S_ERR_NOT_ABS = "path {} is not absolute"
    # NB: format param is dir_prj
    S_ERR_NOT_DIR = "path {} is not a directory"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, dir_prj, dir_venv):
        """
        Initialize the new object

        Args:
            dir_prj: The path to the project's root dir (can be a string or a
            Path object)
            dir_venv: The path or name of the resulting venv folder (can be a
            string or a Path object, absolute or relative to dir_prj)

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # save prj dir
        self._dir_prj = Path(dir_prj)
        if not self._dir_prj.is_absolute():
            raise OSError(self.S_ERR_NOT_ABS.format(self._dir_prj))
        if not self._dir_prj.is_dir():
            raise OSError(self.S_ERR_NOT_DIR.format(self._dir_prj))

        # if param is not abs, make abs rel to prj dir
        self._dir_venv = Path(dir_venv)
        if not self._dir_venv.is_absolute():
            self._dir_venv = self._dir_prj / dir_venv

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Creates a new venv given the __init__ params
    # --------------------------------------------------------------------------
    def create(self):
        """
        Creates a new venv given the __init__ params

        Creates a new venv folder with the parameters provided at create time.
        """

        # the command to create a venv
        cmd = self.S_CMD_CREATE.format(self._dir_venv)
        F.sh(cmd, shell=True)

    # --------------------------------------------------------------------------
    # Install packages to venv from the reqs_file property
    # --------------------------------------------------------------------------
    def install_reqs(self, file_reqs):
        """
        Install packages to venv from the reqs_file property

        Args:
            file_reqs: File to load requirements

        This method takes requirements in the reqs_file property and installs
        them in the dir_venv property.
        """

        # if param is not abs, make abs rel to prj dir
        file_reqs = Path(file_reqs)
        if not file_reqs.is_absolute():
            file_reqs = self._dir_prj / file_reqs

        # the command to install packages to venv from reqs
        cmd = self.S_CMD_INSTALL.format(
            self._dir_venv.parent, self._dir_venv.name, file_reqs
        )
        F.sh(cmd, shell=True)

    # --------------------------------------------------------------------------
    # Freeze packages in the venv folder to the file_reqs property
    # --------------------------------------------------------------------------
    def freeze(self, file_reqs):
        """
        Freeze packages in the venv folder to the file_reqs property

        Args:
            file_reqs: File to save requirements

        Freezes current packages in the venv dir into a file for easy
        installation.
        """

        # if param is not abs, make abs rel to prj dir
        file_reqs = Path(file_reqs)
        if not file_reqs.is_absolute():
            file_reqs = self._dir_prj / file_reqs

        # the command to freeze a venv
        cmd = self.S_CMD_FREEZE.format(
            self._dir_venv.parent, self._dir_venv.name, file_reqs
        )
        F.sh(cmd, shell=True)


# -)
