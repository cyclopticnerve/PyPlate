#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: venv_install.sh                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/private/venv_install.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../../..

# activate the project's venv and install reqs there
. __PP_NAME_VENV__/bin/activate
python -m pip install -r __PP_REQS_FILE__

# -)
