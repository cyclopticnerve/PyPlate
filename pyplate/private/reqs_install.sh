#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: venv_install.sh                                       |     ()     |
# Date    : 09/29/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/private/venv_install.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../..

# activate the project's venv and install reqs there
. .venv-pyplate/bin/activate
python -m pip install -r requirements.txt

# -)
