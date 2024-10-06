#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.sh                                            |     ()     |
# Date    : 09/29/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

#
# A script to run the real pybaker.py in PyPlate src directory
#

# get the project directory (should always be two levels up)
PRJ_DIR=$(cd ../.. && pwd)

# pass the project dir to the real pybaker.py
~/Documents/Projects/Python/PyPlate/src/pybaker.py $PRJ_DIR

# -)
