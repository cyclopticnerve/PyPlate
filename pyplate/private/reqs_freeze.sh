#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: venv_freeze.sh                                        |     ()     |
# Date    : 09/29/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

#
# A script to frreeze the current venv requirements
#

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/private/venv_freeze.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../..

# activate the project's venv and freeze reqs there
. .venv-pyplate/bin/activate
python -Xfrozen_modules=off -m pip freeze -l --exclude-editable --require-virtualenv > requirements.txt

# -)
