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

# run the real pybaker with the prj dir
DIR_HOME = str(Path.home()).rstrip("/")
DIR_SRC = f"{DIR_HOME}/Documents/Projects/Python/PyPlate/src/"

# add paths to import search
sys.path.append(str(DIR_SRC))

# import my stuff
from pybaker import PyBaker # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

p = PyBaker()
p.main()

# -)
