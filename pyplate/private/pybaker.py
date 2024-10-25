#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 09/29/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A script to run the real pybaker.py in PyPlate src directory
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# find paths to dev or user
DIR_PARENT = Path(__file__).parent.resolve()
if DIR_PARENT.name == "__PP_DEV_SRC__":
    # DIR_PRJ = DIR_PARENT.parent
    # DIR_CFG = DIR_PRJ / "__PP_DEV_CONF__"
    DIR_LIB = Path.home() / "__PP_DEV_PP__" / "lib"
    # DIR_SRC = DIR_PRJ / "__PP_DEV_SRC__" / "__PP_SUPPORT__"
else:
    DIR_HOME = Path.home()
    # DIR_CFG = DIR_HOME / "__PP_USR_CONF__"
    DIR_LIB = DIR_HOME / "__PP_USR_LIB__"
    # DIR_SRC = DIR_HOME / "__PP_USR_SRC__"

# add paths to import search
sys.path.append(str(DIR_LIB))
# sys.path.append(str(DIR_SRC))

# import my stuff
from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# get the project dir
DIR_PRJ = Path(__file__).parents[2].resolve()

# run the real pybaker with the prj dir
cmd = f"python -m ~/__PP_DEV_PP__/src/pybaker.py {DIR_PRJ}"
F.sh(cmd)

# -)
