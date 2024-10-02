#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : GUIs_DEBUG                                             /          \
# Filename: docs.sh                                               |     ()     |
# Date    : 09/29/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

#
# A script to run your documentation program
#

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/nope/reqs_freeze.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../..

# activate the project's venv and freeze reqs there
. .venv-pyplate/bin/activate
python -m pdoc --html -f -o docs src

# -)
