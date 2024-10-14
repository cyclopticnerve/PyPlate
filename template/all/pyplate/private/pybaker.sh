#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: pybaker.sh                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

#
# A script to run the real pybaker.py in PyPlate src directory
#

# get the project directory (should always be two levels up)
PRJ_DIR=$(cd ../.. && pwd)

# pass the project dir to the real pybaker.py
~/__PP_DEV_PP__/src/pybaker.py $PRJ_DIR

# -)
