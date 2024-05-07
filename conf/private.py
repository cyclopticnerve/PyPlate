# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: private.py                                            |     ()     |
# Date    : 04/21/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module acts as a header for pymaker.py/pybaker.py.
This file should only be edited if you know what you are doing.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import os
from pathlib import Path

# ------------------------------------------------------------------------------
# Required for pybaker
# ------------------------------------------------------------------------------

# globals for pb to find
PB_SHORT_DESC = "__PM_SHORT_DESC__"
PB_VERSION = "__PM_VERSION__"

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# this is our metadata bootstrap

# get names
S_PP_NAME_BIG = "PyMaker"
S_PP_NAME_SMALL = "pymaker"

# formatted version
S_PP_VER_FMT = f"Version {PB_VERSION}"

# about string
S_PP_ABOUT = (
    f"{S_PP_NAME_SMALL}\n"
    f"{PB_SHORT_DESC}\n"
    f"{S_PP_VER_FMT}\n"
    f"https://www.github.com/cyclopticnerve/{S_PP_NAME_BIG}"
)

# debug option strings
S_DBG_OPTION = "-d"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP = "enable debugging option"

# ------------------------------------------------------------------------------
# other strings

# shorten sepK_
S = os.sep

# path to prj pyplate files
S_PP_PRV = f"pyplate{S}private.json"
S_PP_PRJ = f"pyplate{S}project.json"

# ------------------------------------------------------------------------------
# Path objects
# ------------------------------------------------------------------------------

# get fixed paths to PyPlate and folders

# Path to PyPlate
# (e.g. /home/cyclopticnerve/Documents/Projects/Python/PyPlate/)
P_DIR_PP = Path(__file__).parents[1]

# Path to PyPlate libs
# (e.g. /home/cyclopticnerve/Documents/Projects/Python/PyPlate/lib)
P_DIR_PP_LIB = P_DIR_PP / "lib"

# Path to PyPlate template
# (e.g. /home/cyclopticnerve/Documents/Projects/Python/PyPlate/template/)
P_DIR_PP_TMP = P_DIR_PP / "template"

# Path to PyPlate template/all
# (e.g. /home/cyclopticnerve/Documents/Projects/Python/PyPlate/template/all)
P_DIR_PP_ALL = P_DIR_PP_TMP / "all"

# -)
