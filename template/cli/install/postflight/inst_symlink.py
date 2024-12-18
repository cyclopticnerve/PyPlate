#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: inst_symlink.py                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
Standard CLI install postflight script

This is the standard postflight script for a CLI program. It places a symlink
in the ~/.local/bin folder, which points to the real script, usually located in
~/.config/<PROJECT>/src.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import subprocess

# ------------------------------------------------------------------------------
# The good stuff
# ------------------------------------------------------------------------------

# construct soft link cmd
CMD = (
    "ln -s "
    # the real script to run
    "$HOME/__PP_USR_CONF__/__PP_DEV_SRC__/__PP_NAME_SMALL__.py "
    # the symlinked script
    "$HOME/__PP_USR_BIN__/__PP_NAME_SMALL__"
)

# get result of running the shell command or bubble up an error
try:
    res = subprocess.run(
        # the array of commands produced by shlex.split
        CMD,
        # if check is True, an exception will be raised if the return code
        # is not 0
        # if check is False, no exception is raised but res will be None,
        # meaning you have to test for it in the calling function
        # but that also means you have no information on WHY it failed
        check=True,
        # convert stdout/stderr from bytes to text
        text=True,
        # put stdout/stderr into res
        capture_output=True,
        # whether the call is a file w/ params (False) or a direct shell
        # input (True)
        shell=True,
    )

# this is the return code check
except subprocess.CalledProcessError as e:
    print(e)

# -)
