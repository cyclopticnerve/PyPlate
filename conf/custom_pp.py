# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: custom_pp.py                                          |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module separates out the constants from pymaker.py/pybaker.py.
This file, and the template folder, are the main ways to customize PyPlate.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import os
from pathlib import Path
import re

# pylint: disable=no-name-in-module

# my imports
from . import keys2 as K  # type: ignore

# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# I18N
# ------------------------------------------------------------------------------

_ = gettext.gettext

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# verbose option strings
S_VER_OPTION = "v"
S_VER_ACTION = "store_true"
S_VER_DEST = "VER_DEST"
S_VER_HELP = "enable verbose option"

# debug option strings
S_DBG_OPTION = "d"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP = "enable debugging option"

# base dir for project type folders, relative to dev home
S_DIR_BASE = f"Documents{os.sep}Projects{os.sep}Python"

# string constants for pymaker
S_ASK_TYPE = "Project type"
S_ASK_NAME = _("Project name")
# NB: format param is __PC_NAME_SMALL__
S_ASK_MOD = "Module name (default: {})"
S_ERR_TYPE = "Please enter a valid project type"
S_ERR_LEN = "Project names must be more than 1 character"
S_ERR_START = "Project names must start with a letter"
S_ERR_END = "Project names must end with a letter or number"
S_ERR_CONTAIN = (
    "Project names must contain only letters, numbers,"
    "dashes (-), or underscores (_)"
)
# NB: format params are __PP_NAME_BIG__ and S_DIR_BASE/(proj type dir)
S_ERR_EXIST = 'Project "{}" already exists in "{}"'

# formats for tree
S_TREE_DIR_FORMAT = " [] $NAME/"
S_TREE_FILE_FORMAT = " [] $NAME"

# dir names, relative to PP template, or project dir
# NB: if you change anything in the template structure, you should revisit this
# and make any appropriate changes
S_ALL_VENV = ".venv"
S_ALL_CONF = "conf"
S_ALL_DIST = "dist"
S_ALL_DOCS = "docs"
S_ALL_LOCALE = "locale"
S_ALL_PO = "po"
S_ALL_MISC = "misc"
S_ALL_README = "README"
S_ALL_SRC = "src"
S_ALL_TESTS = "tests"

# paths relative to end user home only
S_USR_CONF = ".config"  # __PC_NAME_SMALL__ will be appended
S_USR_SRC = f".local{os.sep}share"  # __PC_NAME_SMALL__ will be appended
S_USR_APPS = f".local{os.sep}share{os.sep}applications"  # for .desktop file
S_USR_BIN = f".local{os.sep}bin"  # where to put the binary

# this is where the user libs will go
S_USR_LIB_NAME = "lib"
S_USR_LIB = (
    f".local{os.sep}share"  # __PD_AUTHOR__/S_USR_LIB_NAME will be appended
)

# where to put the file tree
S_FILE_TREE = f"{S_ALL_MISC}{os.sep}tree.txt"

# screenshot loc
S_FILE_SS = f"{S_ALL_README}{os.sep}screenshot.png"

# commands for _do_after_fix
# NB: format param is (proj dir)
S_CMD_GIT = "git init {} -q"
# NB: format param is (proj dir)/S_ALL_VENV
S_CMD_VENV = "python -m venv {}"

# ------------------------------------------------------------------------------
# Lists
# ------------------------------------------------------------------------------

# the type of projects that will ask for a module name
L_NAME_MOD = ["p"]

# ------------------------------------------------------------------------------
# Dictionaries
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# NB: these are one-time settings that should be edited before you create your
# first project
D_PRJ_DEF = {
    # --------------------------------------------------------------------------
    # this stuff should only be set once
    # the author name, used in headers and pyproject.toml
    "__PD_AUTHOR__": "cyclopticnerve",
    # the web url for all projects
    "__PD_URL__": "https://github.com/cyclopticnerve",
    # the author's email, used in headers and pyproject.toml
    "__PD_EMAIL__": "cyclopticnerve@gmail.com",
    # the license name, used in headers, __PD_README_FILE__, and pyproject.toml
    "__PD_LICENSE_NAME__": "WTFPLv2",
    # the license image source, used in __PD_README_FILE__
    "__PD_LICENSE_IMG__": "https://img.shields.io/badge/License-WTFPL-brightgreen.svg",
    # the url for license image click
    "__PD_LICENSE_LINK__": "http://www.wtfpl.net",
    # the license file to use
    "__PD_LICENSE_FILE__": "LICENSE.txt",
    # the screenshot to use in  __PD_README_FILE__
    "__PD_SCREENSHOT__": S_FILE_SS,
    # version format string for command line (context for pybaker replace)
    "__PD_VER_FMT__": "Version __PM_VERSION__",
    # NB: the struggle here is that using the fixed format results in a
    # four-digit year, but using the locale format ('%x') results in a
    # two-digit year (at least for my locale, which in 'en_US'). so what to do?
    # what i really want is a locale format that uses four-digit years
    # everywhere. so i am faced with a 'cake and eat it too' situation. not
    # sure how to proceed but i think for now i will leave this as a
    # user-editable string and place it in the realm of 'edit it before you
    # run' along with author/email/license/etc
    "__PD_DATE_FMT__": "%m/%d/%Y",
    # readme file used in pyproject.toml
    "__PD_README_FILE__": "README.md",
    # location of config files, relative to the project dir
    "__PD_DEV_CONF__": S_ALL_CONF,
    # location of src files, relative to the project dir
    "__PD_DEV_SRC__": S_ALL_SRC,
    # --------------------------------------------------------------------------
    # these paths are relative to the user's home dir
    "__PD_USR_APPS__": S_USR_APPS,  # for .desktop file
    "__PD_USR_BIN__": S_USR_BIN,  # where to put the binary
}

D_PRJ_CFG = {
    # --------------------------------------------------------------------------
    # these items will be filled in by _get_project_info
    "__PC_TYPE_PRJ__": "",  # 'c'
    "__PC_NAME_BIG__": "",  # PyPlate
    "__PC_NAME_SMALL__": "",  # pyplate
    "__PC_NAME_MOD__": "",  # module1.py
    "__PC_NAME_CLASS__": "",  # Pascal case name for classes
    "__PC_DATE__": "",  # the date eac__PPh file was created, updated every time
    "__PC_FILENAME__": "",  # filename after fixing path
    # --------------------------------------------------------------------------
    # these paths are calculated at runtime relative to the dev's home dir
    "__PC_DEV_LIB__": "",  # location of cnlibs dir in PyPlate
    "__PC_PYBAKER__": "",  # location of real pybaker in PyPlate
    # --------------------------------------------------------------------------
    # these paths are calculated at runtime relative to the user's home dir
    "__PC_USR_CONF__": "",  # config dir
    "__PC_USR_LIB__": "",  # location of cnlibs dir
    "__PC_USR_SRC__": "",  # where the program will keep it's source
}

# the default metadata that the final project will use for pybaker.py
# NB: all of these values will need to be set later before running pybaker.py
D_PRJ_META = {
    # the version number to use in __PD_README_FILE__ and pyproject.toml
    "__PM_VERSION__": "",
    # the short description to use in __PD_README_FILE__ and pyproject.toml
    "__PM_SHORT_DESC__": "",
    # the keywords to use in pyproject.toml and github
    "__PM_KEYWORDS__": [],
    # the python dependencies to use in __PD_README_FILE__, pyproject.toml, github,
    # and install.py
    "__PM_PY_DEPS__": {},
    # the system dependencies to use in __PD_README_FILE__, github.com, and
    # install.py
    "__PM_SYS_DEPS__": [],
    # the categories to use in .desktop for gui apps
    "__PM_GUI_CATS__": [],
}

# this is the set of dirs/files we don't mess with in the final project
# each item can be a full path, a path relative to the project directory, or
# glob
# see https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
# NB: you can use dunders here since the path is the last thing to get fixed
# these dir/file names should match what's in the template dir (before any
# modifications, hence using dunder keys)
D_BLACKLIST = {
    # skip header, skip text, skip path (0 0 0)
    # NB: this is mostly to speed up processing by not even looking at them
    K.S_KEY_SKIP_ALL: [
        ".git",
        S_ALL_VENV,
        ".VSCodeCounter",
        S_ALL_CONF,
        S_ALL_DIST,
        S_ALL_DOCS,
        S_ALL_LOCALE,
        S_ALL_MISC,
        S_ALL_README,
        "CHANGELOG.md",
        "LICENSE.txt",
        "requirements.txt",
        "**/__pycache__",
    ],
    # skip header, skip text, fix path (0 0 1)
    # NB: this is used mostly for non-text files
    K.S_KEY_SKIP_CONTENTS: [
        "**/*.png",
        "**/*.jpg",
        "**/*.jpeg",
    ],
    # skip header, fix text, fix path (0 1 1)
    # NB: not sure what this is useful for, but here it is
    K.S_KEY_SKIP_HEADER: [],
    # fix header, skip text, fix path (1 0 1)
    # NB: mostly used for files that contain dunders that will be replaced
    # later or files we only want to replace headers in
    K.S_KEY_SKIP_TEXT: [
        "MANIFEST.in",
        ".gitignore",
    ],
    # fix header, fix text, skip path (1 1 0)
    # NB: not really useful, since we always want to fix paths with dunders,
    # but included for completeness
    K.S_KEY_SKIP_PATH: [],
    # list of dirs/files to ignore in output dir when creating the initial tree
    # NB: each item can be a partial path relative to the project directory, or
    # a glob
    K.S_KEY_SKIP_TREE: [
        ".git",
        S_ALL_VENV,
        ".vscode",
        ".VSCodeCounter",
        "**/__pycache__",
    ],
}

# entries to be put in blacklist before writing to project
# NBL key is blacklist section, val is an array of strings
D_BL_AFTER = {K.S_KEY_SKIP_ALL: [".vscode", S_ALL_TESTS]}

# I18N stuff to be used in pybaker
D_I18N = {
    # default charset for .pot/.po files
    K.S_KEY_CHARSET: "UTF-8",
    # the types of projects that will have i18n applied
    K.S_KEY_TYPES: ["g"],
    # computer languages
    K.S_KEY_CLANGS: {
        "Python": [
            "py",
        ],
        "Glade": [
            ".ui",
            ".glade",
        ],
        "Desktop": [".desktop"],
    },
    # dict of clangs and no exts (ie file names)
    K.S_KEY_NO_EXT: {
        "Python": [
            "__PC_NAME_SMALL__",
        ],
    },
    K.S_KEY_LOCALE: S_ALL_LOCALE,
    K.S_KEY_PO: S_ALL_PO,
}

# dict of files that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project, it gets copied
# to the project, and cuts down on duplicate files
# key is the relative path to the source file in PyPlate
# val is the relative path to the dest file in the project dir
D_COPY = {
    f"{S_ALL_MISC}{os.sep}snippets.txt": f"{S_ALL_MISC}{os.sep}snippets.txt",
    f"{S_ALL_MISC}{os.sep}style.txt": f"{S_ALL_MISC}{os.sep}style.txt",
    
}

# the types of projects this script can create
# key is the short type name (used for entry)
# val[0] is the long type name (used for display)
# val[1] is the subdir name under _DIR_BASE where the project will be created
# val[2] is the dir(s) under 'template' to get the files
# order is arbitrary, just decided to make it alphabetical
D_TYPES = {
    "c": ["CLI", "CLIs", "cli"],
    "g": ["GUI", "GUIs", "gui"],
    "p": ["Package", "Packages", "pkg"],
}

# files to remove after the project is done
# paths are relative to project dir
D_PURGE = {"p": [Path(S_ALL_TESTS) / "ABOUT"]}

# the dict of sections to remove in the README file
# key is the project type we are making (may contain multiple project types)
# or a special section of the readme
# rm_delete_start is the tag at the start of the section to remove
# rm_delete_end is the tag at the end of the section to remove
# NB: these tags start with 'RM' instead of 'PP' because most 'PP' keys will
# remain in the file, and we don't want pybaker to report their presence as an
# error
# this way you can have different sections in the readme for things like
# installation instructions, depending on whether your project is a package or
# a cli/gui app
D_README = {
    "RM_LICENSE": {
        "RM_LICENSE_START": "<!-- __RM_LICENSE_START__ -->",
        "RM_LICENSE_END": "<!-- __RM_LICENSE_END__ -->",
    },
    "c": {
        "RM_DELETE_START": "<!-- __RM_PKG_START__ -->",
        "RM_DELETE_END": "<!-- __RM_PKG_END__ -->",
    },
    "g": {
        "RM_DELETE_START": "<!-- __RM_PKG_START__ -->",
        "RM_DELETE_END": "<!-- __RM_PKG_END__ -->",
    },
    "p": {
        "RM_DELETE_START": "<!-- __RM_APP_START__ -->",
        "RM_DELETE_END": "<!-- __RM_APP_END__ -->",
    },
}

# ------------------------------------------------------------------------------
# Regex strings
# ------------------------------------------------------------------------------

# M: caret matches newline
# off: ^(\w) matches A in A\nN
# on: ^(\w) matches A and B in A\nB
# breaks string into list at \n and iterates it, starting the caret match again

# S: dot matches newlines
# off: (.*) matches A, (e), B, (e) in A\nB
# on: (.*) matches A\nB in A\nB

# regex strings for readme to replace license image
R_RM_START = D_README["RM_LICENSE"]["RM_LICENSE_START"]
R_RM_END = D_README["RM_LICENSE"]["RM_LICENSE_END"]
R_README = rf"({R_RM_START})(.*?)({R_RM_END})"
# NB: format param is full license string
R_README_REP = r"\g<1>\n{}\n\g<3>"

# search and sub flags
# NB: need S for matches that span multiple lines (R_README)
R_RM_SUB_FLAGS = re.S

# -)
