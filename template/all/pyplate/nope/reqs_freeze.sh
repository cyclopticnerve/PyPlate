#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: reqs_freeze.sh                                        |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

#
# A script to frreeze the current venv requirements
#

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/nope/reqs_freeze.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../..

# activate the project's venv and freeze reqs there
. __PP_NAME_VENV__/bin/activate
python -Xfrozen_modules=off -m pip freeze -l --exclude-editable --require-virtualenv > __PP_REQS_FILE__

# -)
