# ------------------------------------------------------------------------------
# Package :PyPlate                                                /          \
# Filename: ppvenv.py                                             |     ()     |
# Date    : 09/09/2026                                            |            |
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
import cnlib.cnfunctions as F

# local imports
import conf

# ------------------------------------------------------------------------------
# Public methods
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Creates a new venv given the __init__ params
# ------------------------------------------------------------------------------
def create(dir_prj, dir_venv):
    """
    Creates a new venv given the __init__ params

    Raises:
        cnlib.cnfunctions.CNRunError if the create fails

    Creates a new venv folder with the parameters provided at create time.
    """

    # save prj dir
    dir_prj = Path(dir_prj).resolve()
    if not dir_prj.is_absolute():
        raise OSError(conf.S_ERR_NOT_ABS.format(dir_prj))
    if not dir_prj.is_dir():
        raise OSError(conf.S_ERR_NOT_DIR.format(dir_prj))

    # if param is not abs, make abs rel to prj dir
    dir_venv = Path(dir_venv).resolve()
    if not dir_venv.is_absolute():
        dir_venv = dir_prj / dir_venv

    # the command to create a venv
    cmd = conf.S_CMD_CREATE.format(dir_venv)
    try:
        F.run(cmd, shell=True, capture_output=True)
    except F.CNRunError as e:
        raise e


# ------------------------------------------------------------------------------
# Install packages to venv from the reqs_file property
# ------------------------------------------------------------------------------
def install_reqs(dir_prj, dir_venv, file_reqs):
    """
    Install packages to venv from the reqs_file property

    Args:
        file_reqs: File to load requirements

    Raises:
        cnlib.cnfunctions.CNRunError if the reqs install fails

    This method takes requirements in the reqs_file property and installs
    them in the dir_venv property.
    """

    # if param is not abs, make abs rel to prj dir
    file_reqs = Path(file_reqs).resolve()
    if not file_reqs.is_absolute():
        file_reqs = dir_prj / file_reqs

    # ignore missing files
    # NB: fail silently
    if not file_reqs.exists():  # or file_reqs.stat().st_size == 0:
        return

    # the command to install packages to venv from reqs
    # NB: fail silently if file exists but is empty
    cmd = conf.S_CMD_INSTALL.format(dir_venv.parent, dir_venv.name, file_reqs)
    try:
        F.run(cmd, shell=True, capture_output=True)
    except F.CNRunError as e:
        raise e


# ------------------------------------------------------------------------------
# Freeze packages in the venv folder to the file_reqs property
# ------------------------------------------------------------------------------
def freeze(dir_prj, dir_venv, file_reqs):
    """
    Freeze packages in the venv folder to the file_reqs property

    Args:
        file_reqs: File to save requirements

    Raises:
        cnlib.cnfunctions.CNRunError if the freeze fails

    Freezes current packages in the venv dir into a file for easy
    installation.
    """

    # if param is not abs, make abs rel to prj dir
    file_reqs = Path(file_reqs).resolve()
    if not file_reqs.is_absolute():
        file_reqs = dir_prj / file_reqs

    # the command to freeze a venv
    cmd = conf.S_CMD_FREEZE.format(dir_venv.parent, dir_venv.name, file_reqs)
    try:
        F.run(cmd, shell=True, capture_output=True)
    except F.CNRunError as e:
        raise e


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    F.B_DEBUG = True
    ERR = False

    if ERR:

        DIR_PRJ = Path(__file__).parent.resolve() / "boobs"  # ok
        DIR_VENV = DIR_PRJ / ".venv"
        FILE_REQS = DIR_PRJ / "requirements.txt"

    else:

        DIR_PRJ = Path(__file__).parent.resolve()
        DIR_VENV = DIR_PRJ / ".venv"
        FILE_REQS = DIR_PRJ / "requirements.txt"

    create(DIR_PRJ, DIR_VENV)
    install_reqs(DIR_PRJ, DIR_VENV, FILE_REQS)
    freeze(DIR_PRJ, DIR_VENV, FILE_REQS)

# -)
