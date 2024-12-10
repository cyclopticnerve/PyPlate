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

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# A class to make handling of venv folders easier
# ------------------------------------------------------------------------------
class CNVenv:
    """
    A class to make handling of venv folders easier

    Public methods:
        create: Make a new venv folder for a project
        freeze: Collects all packages needed for this project
        install: Installs all packages needed for this project

    This class provides methods to create, freeze, and install dependencies
    in the project's venv folder.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, dir_prj, dir_venv):
        """
        Initialize the new object

        Arguments:
            dir_prj: The path to the project's root dir (can be a string or a
            Path object)
            dir_venv: The path or name of the resulting venv folder (can be a
            string or a Path object, absolute or relative to dir_prj)
            file_reqs: The path or name of the requirements file ((can be a
            string or a Path object, absolute or relative to dir_prj)

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # save prj dir
        self._dir_prj = Path(dir_prj)

        # if param is not abs, make abs rel to prj dir
        self._dir_venv = Path(dir_venv)
        if not self._dir_venv.is_absolute():
            self._dir_venv = Path(self._dir_prj) / dir_venv

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Create a new venv given the __init__ params
    # --------------------------------------------------------------------------
    def create(self):
        """
        Create a new venv given the __init__ params

        Raises:
            cnfunctions.CNShellError if an error occurs

        Creates a new venv folder with the parameters provided at create time.
        """

        # the command to create a venv
        cmd = f"python -Xfrozen_modules=off -m venv {self._dir_venv}"
        try:
            F.sh(cmd)
        except F.CNShellError as e:
            raise e

    # --------------------------------------------------------------------------
    # Install packages to venv from the reqs_file property
    # --------------------------------------------------------------------------
    def install(self, file_reqs):
        """
        Install packages to venv from the reqs_file property

        Arguments:
            file_reqs: File to load requirements

        Raises:
            cnfunctions.CNShellError if an error occurs

        This method takes requirements in the reqs_file property and installs
        them in the dir_venv property.
        """

        # if param is not abs, make abs rel to prj dir
        file_reqs = Path(file_reqs)
        if not file_reqs.is_absolute():
            file_reqs = Path(self._dir_prj) / file_reqs

        # the command to install packages to venv from reqs
        cmd = (
            f"cd {self._dir_venv.parent}; "
            f". ./{self._dir_venv.name}/bin/activate; "
            "python -m pip install "
            f"-r {file_reqs}"
        )
        try:
            F.sh(cmd, shell=True)
        except F.CNShellError as e:
            raise e

    # --------------------------------------------------------------------------
    # Freeze packages in the venv folder to the file_reqs property
    # --------------------------------------------------------------------------
    # def freeze(self, file_reqs):
    #     """
    #     Freeze packages in the venv folder to the file_reqs property

    #     Arguments:
    #         file_reqs: File to save requirements

    #     Raises:
    #         cnfunctions.CNShellError if an error occurs

    #     Freezes current packages in the venv dir into a file for easy
    #     installation.
    #     """

    #     # if param is not abs, make abs rel to prj dir
    #     file_reqs = Path(file_reqs)
    #     if not file_reqs.is_absolute():
    #         file_reqs = Path(self._dir_prj) / file_reqs

    #     # the command to freeze a venv
    #     cmd = (
    #         f"cd {self._dir_venv.parent}; "
    #         f". ./{self._dir_venv.name}/bin/activate; "
    #         "python "
    #         "-Xfrozen_modules=off "
    #         "-m pip freeze "
    #         "-l --exclude-editable "
    #         "--require-virtualenv "
    #         "> "
    #         f"{file_reqs}"
    #     )
    #     try:
    #         F.sh(cmd, shell=True)
    #     except F.CNShellError as e:
    #         raise e


# -)
