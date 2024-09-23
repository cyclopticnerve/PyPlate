#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: docs.sh                                               |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

#
# A script to run your documentation program
#

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/nope/reqs_freeze.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../..

# activate the project's venv and freeze reqs there
. __PP_NAME_VENV__/bin/activate
python -m pdoc --html -f -o __PP_DOCS_NAME__ src

# -)
