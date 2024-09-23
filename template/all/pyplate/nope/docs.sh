#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: docs.sh                                               |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

#
# A script to run whatever documentation program you have
#

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/nope/docs.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../..

. __PP_NAME_VENV__/bin/activate
# run docs on project's src dir
python -m pdoc --html -f -o __PP_DOCS_NAME__ .

# -)
