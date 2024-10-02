#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : GUIs_DEBUG                                             /          \
# Filename: reqs_install.sh                                       |     ()     |
# Date    : 09/29/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/nope/reqs_install.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../..

# activate the project's venv and install reqs there
. __PP_NAME_VENV__/bin/activate
python -m pip install -r __PP_REQS_FILE__

# -)
