#!/usr/bin/env bash
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: venv_create.sh                                        |     ()     |
# Date    : 10/11/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# change working dir to the project (which is two dirs up,
# ie. "project/pyplate/private/venv_create.sh")
SCRIPT_DIR=$(dirname $(realpath $0))
cd $SCRIPT_DIR/../../..

# create the project's venv
python -Xfrozen_modules=off -m venv $1

# -)
