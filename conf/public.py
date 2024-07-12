# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: public.py                                             |     ()     |
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
import os
from pathlib import Path
import re

# ------------------------------------------------------------------------------
# Bools
# ------------------------------------------------------------------------------

# create a tree and save it to S_TREE_FILE
B_CMD_TREE = True
# create a git using S_GIT_CMD
B_CMD_GIT = True
# create a venv using S_VENV_CMD
B_CMD_VENV = True

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# path sep
S = os.sep

# base dir for project type folders, relative to dev home
S_DIR_BASE = f"Documents{S}Projects{S}Python"

# NB: format params are L_TYPES[0], L_TYPES[1]
S_TYPE_FMT = "{} ({})"
# join each project type with this
S_TYPE_JOIN = " | "

# NB: format param is joined list of project types
S_ASK_TYPE = "Project type [{}]: "
S_ASK_NAME = "Project name: "
# NB: format params are D_TYPE_SEC[prj_type], __PP_NAME_SMALL__
S_ASK_SEC = "{} name (default: {}): "

# error strings
S_ERR_TYPE = "Please enter a valid project type"
S_ERR_LEN = "Project names must be more than 1 character"
S_ERR_START = "Project names must start with a letter"
S_ERR_END = "Project names must end with a letter or number"
S_ERR_CONTAIN = (
    "Project names must contain only letters, numbers,"
    "dashes (-), or underscores (_)"
)
# NB: format param arise dir_type/(proj type dir)
S_ERR_EXIST = 'Project "{}" already exists'

# debug-specific strings
S_ERR_DEBUG = (
    "\n"
    "WARNING! YOU ARE IN DEBUG MODE!\n"
    "IT IS POSSIBLE TO OVERWRITE EXISTING PROJECTS!\n"
)

# NB: keys should really be private, need to keep them here to avoid circular
# imports

# TODO: which keys need to be global/which are only used once?
# keys for pybaker private dict
S_KEY_PRJ_DEF = "PRJ_DEF"
S_KEY_PRJ_ADD = "PRJ_ADD"
S_KEY_PRJ_CFG = "PRJ_CFG"

# keys for metadata, blacklist, i18n in pybaker dev dict
S_KEY_META = "META"
S_KEY_BLACKLIST = "BLACKLIST"
S_KEY_I18N = "I18N"

# keys for blacklist
S_KEY_SKIP_ALL = "SKIP_ALL"
S_KEY_SKIP_CONTENTS = "SKIP_CONTENTS"
S_KEY_SKIP_HEADER = "SKIP_HEADER"
S_KEY_SKIP_CODE = "SKIP_CODE"
S_KEY_SKIP_PATH = "SKIP_PATH"
S_KEY_SKIP_TREE = "SKIP_TREE"

# keys for i18n
S_KEY_CHARSET = "CHARSET"
S_KEY_TYPES = "TYPES"
S_KEY_CLANGS = "CLANGS"
S_KEY_NO_EXT = "NO_EXT"
S_KEY_LOCALE = "LOCALE"
S_KEY_PO = "PO"

# header dict keys
S_KEY_HDR_SEARCH = "S_KEY_HDR_SEARCH"
S_KEY_HDR_REPLACE = "S_KEY_HDR_REPLACE"
S_KEY_GRP_VAL = "S_KEY_GRP_VAL"
S_KEY_GRP_PAD = "S_KEY_GRP_PAD"
S_KEY_FMT_VAL_PAD = "S_KEY_FMT_VAL_PAD"

# dir names, relative to PP template, or project dir
# NB: if you change anything in the template structure, you should revisit this
# and make any appropriate changes
# also make sure that these names don't appear in the blacklist, or else
# pymaker won't touch them
S_ALL_VENV = ".venv"
S_ALL_CONF = "conf"
S_ALL_DIST = "dist"
S_ALL_DOCS = "docs"
S_ALL_MISC = "misc"
S_ALL_README = "README"
S_ALL_SRC = "src"
S_ALL_SUPPORT = "support"
S_ALL_I18N = "i18n"
S_ALL_IMAGES = "images"
S_ALL_LOCALE = "locale"
S_ALL_PO = "po"
S_ALL_TESTS = "tests"

# initial location of project (to check for dups)
S_HOME = str(Path.home()).rstrip(S)
S_DIR_PRJ = (
    f"{S_HOME}{S}{S_DIR_BASE}{S}"  # /home/cn/Documents/Projects/Python/
    "{}"  # prj type dir
    f"{S}"  # /
    "{}"  # prj name
)

# paths relative to end user home only
S_USR_CONF = ".config"  # __PP_NAME_SMALL__ will be appended
S_USR_SRC = f".local{S}share"  # __PP_NAME_SMALL__ will be appended
S_USR_APPS = f".local{S}share{S}applications"  # for .desktop file
S_USR_BIN = f".local{S}bin"  # where to put the binary

# this is where the user libs will go
S_USR_LIB_NAME = "lib"
S_USR_LIB = f".local{S}share"  # __PP_AUTHOR__/S_USR_LIB_NAME will be appended

# NB: these steps are optional

# commands for _do_after_fix
# NB: format param is (proj dir)
S_GIT_CMD = "git init {} -q"
# NB: format param is (proj dir)/S_ALL_VENV
S_VENV_CMD = "python -m venv {}"

# formats for tree
S_TREE_FILE = f"{S_ALL_MISC}{S}tree.txt"
S_TREE_DIR_FORMAT = " [] $NAME/"
S_TREE_FILE_FORMAT = " [] $NAME"

# ------------------------------------------------------------------------------
# Lists
# ------------------------------------------------------------------------------

# the types of projects this script can create
# value[0] is the short display name and the char to enter
# value[1] is the long display name
# value[2] is the template folder to copy
# value[3] id the top level folder to put each project in
L_TYPES = [
    ["c", "CLI", "cli", "CLIs"],
    ["p", "Package", "pkg", "Packages"],
    ["g", "GUI", "gui", "GUIs"],
]

# list of keys to find in header
# L_HEADER = [
#     "Project",
#     "Filename",
#     "Date",
#     "Author",
#     "License",
# ]

# ------------------------------------------------------------------------------
# Dictionaries
# ------------------------------------------------------------------------------

# NB: some of these are strictly for string replacement, but some are used by
# pybaker, so don't remove anything unless you know what you are doing
# if you want to ADD a key for string replacement only, use D_PRJ_ADD

# these are the settings that should be set before you run pymaker.py
# consider them the "before create" settings

# if you need to adjust any of these values in a function, use _do_before_fix()
# in this file
D_PRJ_DEF = {
    # --------------------------------------------------------------------------
    # this stuff should only be set once
    # the author name, used in headers and pyproject.toml
    "__PP_AUTHOR__": "cyclopticnerve",
    # the web url for all projects
    "__PP_URL__": "https://github.com/cyclopticnerve",
    # the author's email, used in headers and pyproject.toml
    "__PP_EMAIL__": "cyclopticnerve@gmail.com",
    # the license name, used in headers, __PP_README_FILE__, and pyproject.toml
    "__PP_LICENSE_NAME__": "WTFPLv2",
    # the license image source, used in __PP_README_FILE__
    "__PP_LICENSE_IMG__": "https://img.shields.io/badge/License-WTFPL-brightgreen.svg",
    # the url for license image click
    "__PP_LICENSE_LINK__": "http://www.wtfpl.net",
    # the license file to use
    "__PP_LICENSE_FILE__": "LICENSE.txt",
    # the screenshot to use in  __PP_README_FILE__
    "__PP_SCREENSHOT__": f"{S_ALL_README}{S}screenshot.png",
    # version format string for command line (context for pybaker replace)
    # NB: format param is __PP_VERSION__
    "__PP_VER_FMT__": "Version {}",
    # NB: the struggle here is that using the fixed format results in a
    # four-digit year, but using the locale format ('%x') results in a
    # two-digit year (at least for my locale, which in 'en_US'). so what to do?
    # what i really want is a locale format that uses four-digit years
    # everywhere. so i am faced with a 'cake and eat it too' situation. not
    # sure how to proceed but i think for now i will leave this as a
    # user-editable string and place it in the realm of 'edit it before you
    # run' along with author/email/license/etc
    "__PP_DATE_FMT__": "%m/%d/%Y",
    # readme file used in pyproject.toml, rel to prj dir
    "__PP_README_FILE__": "README.md",
}

# these values are string replace only
# NB: constant values moved here so we can change them easier
D_PRJ_ADD = {
    # --------------------------------------------------------------------------
    # these paths are relative to the dev's home dir
    # location of config files, relative to the project dir
    "__PP_DEV_CONF__": S_ALL_CONF,
    # location of src files, relative to the project dir
    "__PP_DEV_SRC__": S_ALL_SRC,
    # --------------------------------------------------------------------------
    # these paths are relative to the user's home dir
    "__PP_USR_APPS__": S_USR_APPS,  # for .desktop file
    "__PP_USR_BIN__": S_USR_BIN,  # where to put the binary
    "__PP_DUMMY__": "",  # dummy value to use in headers
    "__PP_SUPPORT__": S_ALL_SUPPORT,  # where is rest of code
    "__PP_IMAGES__": S_ALL_IMAGES,  # where gui images are stored
}

# these are settings that will be calculated for you while running pymaker.py
# consider them the "during create" settings
D_PRJ_CFG = {
    # --------------------------------------------------------------------------
    # these items will be filled in by _get_project_info
    "__PP_TYPE_PRJ__": "",  # 'c'
    "__PP_NAME_BIG__": "",  # PyPlate
    "__PP_NAME_SMALL__": "",  # pyplate
    "__PP_NAME_SEC__": "",  # module1.py
    "__PP_NAME_CLASS__": "",  # Pascal case name for classes
    "__PP_DATE__": "",  # the date each file was created, updated every time
    # --------------------------------------------------------------------------
    # these paths are calculated at runtime relative to the dev's home dir
    # "__PP_DEV_LIB__": "",  # location of cnlibs dir in PyPlate
    "__PP_DEV_PP__": "",  # location of real pybaker in PyPlate, rel to dev home
    # --------------------------------------------------------------------------
    # these paths are calculated at runtime relative to the user's home dir
    "__PP_USR_CONF__": "",  # config dir
    "__PP_USR_LIB__": "",  # location of cnlibs dir
    "__PP_USR_SRC__": "",  # where the program will keep it's source
}

# these are settings that will be changed before running pybaker.py
# consider them the "after create" settings
D_PRJ_META = {
    # the version number to use in __PP_README_FILE__ and pyproject.toml
    "__PP_VERSION__": "0.0.0",
    # the short description to use in __PP_README_FILE__ and pyproject.toml
    "__PP_SHORT_DESC__": "",
    # the keywords to use in pyproject.toml and github
    "__PP_KEYWORDS__": [],
    # the python dependencies to use in __PP_README_FILE__, pyproject.toml, github,
    # and install.py
    "__PP_PY_DEPS__": {},
    # the system dependencies to use in __PP_README_FILE__, github.com, and
    # install.py
    "__PP_SYS_DEPS__": [],
    # the categories to use in .desktop for gui apps
    "__PP_GUI_CATS__": [],
}

# the lists of dirs/files we don't mess with while running pymaker
# each item can be a full path, a path relative to the project directory, or a
# glob
# see https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
# NB: you can use dunders here since the path is the last thing to get fixed
# these dir/file names should match what's in the template dir (before any
# modifications, hence using dunder keys)
D_BLACKLIST = {
    # skip header, skip text, skip path (0 0 0)
    # NB: this is mostly to speed up processing by not even looking at them
    S_KEY_SKIP_ALL: [
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
    S_KEY_SKIP_CONTENTS: [
        "**/*.png",
        "**/*.jpg",
        "**/*.jpeg",
    ],
    # skip header, fix text, fix path (0 1 1)
    # NB: not sure what this is useful for, but here it is
    S_KEY_SKIP_HEADER: [],
    # fix header, skip text, fix path (1 0 1)
    # NB: mostly used for files that contain dunders that will be replaced
    # later or files we only want to replace headers in
    S_KEY_SKIP_CODE: [
        "MANIFEST.in",
        ".gitignore",
    ],
    # fix header, fix text, skip path (1 1 0)
    # NB: not really useful, since we always want to fix paths with dunders,
    # but included for completeness
    S_KEY_SKIP_PATH: [],
    # list of dirs/files to ignore in output dir when creating the initial tree
    # NB: each item can be a partial path relative to the project directory, or
    # a glob
    S_KEY_SKIP_TREE: [
        ".git",
        S_ALL_VENV,
        ".vscode",
        ".VSCodeCounter",
        "**/__pycache__",
    ],
}

# entries to be remove fom/added to blacklist after project is created
# this happens after _do_fix, but before writing to pb's project file
# NB: key is blacklist section, val is an array of strings
# NOTE: can't use dunders here (anything that would need a dunder should use
# replacement value from D_PRJ_CFG)
# D_BL_ADD = {S_KEY_SKIP_ALL: [".vscode", S_ALL_TESTS]}
# D_BL_REM = {}

# I18N stuff to be used in pybaker
D_I18N = {
    # default charset for .pot/.po files
    S_KEY_CHARSET: "UTF-8",
    # the types of projects that will have i18n applied
    S_KEY_TYPES: ["g"],
    # computer languages
    S_KEY_CLANGS: {
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
    S_KEY_NO_EXT: {
        "Python": [
            "__PP_NAME_SMALL__",
        ],
    },
    S_KEY_LOCALE: S_ALL_LOCALE,
    S_KEY_PO: S_ALL_PO,
}

# dict of files that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project, it gets copied
# to the project, and cuts down on duplicate files
# key is the relative path to the source file in PyPlate
# val is the relative path to the dest file in the project dir
D_COPY = {
    f"{S_ALL_MISC}{S}snippets.txt": f"{S_ALL_MISC}{S}snippets.txt",
    f"{S_ALL_MISC}{S}style.txt": f"{S_ALL_MISC}{S}style.txt",
}

# files to remove after the project is done
# paths are relative to project dir
# key is prj type key from L_TYPES[0]
# val is path relative to dir_prj
D_PURGE = {"p": [Path(S_ALL_TESTS) / "ABOUT"]}

# the dict of sections to remove in the README file
# key is the project type we are making (from L_TYPES[2], the template src dir)
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
    "cli": {
        "RM_DELETE_START": "<!-- __RM_PKG_START__ -->",
        "RM_DELETE_END": "<!-- __RM_PKG_END__ -->",
    },
    "gui": {
        "RM_DELETE_START": "<!-- __RM_PKG_START__ -->",
        "RM_DELETE_END": "<!-- __RM_PKG_END__ -->",
    },
    "pkg": {
        "RM_DELETE_START": "<!-- __RM_APP_START__ -->",
        "RM_DELETE_END": "<!-- __RM_APP_END__ -->",
    },
}

# the info for matching/fixing header lines
D_HEADER = {
    S_KEY_HDR_SEARCH: (
        r"^((#|<!--) \S* *: )"  # 1/2 keyword
        r"(\S+( \S+)*)"  # 3/4 value (multi word)
        r"( *)"  # 5 padding (if any)
        r"(.*)"  # 6 rat (if any)
    ),
    # format param is fmt_val_pad result
    S_KEY_HDR_REPLACE: r"\g<1>{}\g<6>",
    S_KEY_GRP_VAL: 3,
    S_KEY_GRP_PAD: 5,
    # format params are grp_val and grp_pad result
    S_KEY_FMT_VAL_PAD: "{}{}",
}

# the type of projects that will ask for a second name
D_NAME_SEC = {
    "p": "Module",
    "g": "Window class",
}

# ------------------------------------------------------------------------------
# Regex strings
# ------------------------------------------------------------------------------

# if not using rat, and your headers are simple, you can use a regex like:

# group 1 is the keyword from L_HEADER
# group 2 is value
# group 2 will have its text replaced and passed to R_HDR_REP
# R_HDR_SCH = r"^(# {}\s*: )(\S*)"
# R_HDR_REP = r"\g<1>{}"
# R_HDR_VAL = 2

# or even simpler:
# the whole match will have its text replaced and passed to R_HDR_REP
# R_HDR_SCH = r"^# {}\s*: \S*"
# R_HDR_REP = r"{}"
# R_HDR_VAL = 0

# if you are using right-aligned text, you will need at least 3 groups:
# 1. everything before the value (keyword, colon, etc)
# 2. the value and the padding
# 3. the rat
# then your replacement string should look like:
# R_HDR_REP = r"\g<1>{}\g<3>
# and you should set R_HDR_VAL = 2

# this is my setup:

# the regex to split val/pad
# NB: format params will be val and pad
# NB: done first to reuse in R_HDR_SCH
# R_VP_SCH = r"(\S+( \S+)*)(\s*)"
# R_VP_REP = "{}{}"
# R_VAL_GRP = 1
# R_PAD_GRP = 3

# the regex to split a line
# group 1 is keyword/colon
# group 2/3/4/5 is value and padding (multi word support)
# group 6 is rat
# NB: format params are comment str and item from L_HEADER
# NB: make sure this uses R_MULTI_WORD
# NB: note that R_VP_SCH is 3 groups, adjust group indexes
# private
# R_HDR_SCH = (
#     r"^({} {}\s*: )"  # keyword
#     rf"({R_VP_SCH})"  # value/padding
#     r"(.*)"  # rat
# )
# # NB: format param is contents of group R_HDR_VAL after string replacement
# R_HDR_REP = r"\g<1>{}\g<6>"
# R_HDR_VAL = 2

# regex to find dunders in files
# R_CODE_DUN = r"__\S\S_\S*__"

# regex strings for readme to replace license image
R_RM_START = D_README["RM_LICENSE"]["RM_LICENSE_START"]
R_RM_END = D_README["RM_LICENSE"]["RM_LICENSE_END"]
R_README = rf"({R_RM_START})(.*?)({R_RM_END})"
# NB: format param is full license string
R_README_REP = r"\g<1>\n{}\n\g<3>"

# search and sub flags
# NB: need S for matches that span multiple lines (R_README)
R_RM_SUB_FLAGS = re.S


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Do any work before fix
# ------------------------------------------------------------------------------
def do_before_fix():
    """
    Do any work before fix

    Do any work before fix. This method is called at the beginning of _do_fix,
    after all dunders have been configured, but before any files have been
    modified.
    """

    # TODO: move all stuff that should not be built-in from
    # _get_project_info/_do_fix into here

    # TODO: do this stuff in pybaker

    # get values after pymaker has set them
    author = D_PRJ_DEF["__PP_AUTHOR__"]
    name_small = D_PRJ_CFG["__PP_NAME_SMALL__"]

    # paths relative to the end user's (or dev's) useful folders
    D_PRJ_CFG["__PP_USR_CONF__"] = f"{S_USR_CONF}{S}{name_small}"
    D_PRJ_CFG["__PP_USR_SRC__"] = f"{S_USR_SRC}{S}{name_small}"
    D_PRJ_CFG["__PP_USR_LIB__"] = f"{S_USR_LIB}{S}{author}{S}{S_USR_LIB_NAME}"


# --------------------------------------------------------------------------
# Do any work after fix
# --------------------------------------------------------------------------
def do_after_fix():
    """
    Do any work after fix

    Do any work after fix. This method is called at the end of the internal _do_after_fix, after
    all files have been modified.
    """

    # TODO: move _fix_readme call from _do_fix to here - should not be built-in
    # TODO: move any stuff that should not be built-in in _do_after_fix to
    # here


# ------------------------------------------------------------------------------
# Return a string of a Path object without dev home
# ------------------------------------------------------------------------------
# def get_no_home(path):
#     """
#     Return a string of a Path object without dev home

#     Arguments:
#         path: The Path object to remove the home folder from

#     Remove the home folder component from a path object and return the string
#     representation. It is here so it can be used anywhere.
#     """

#     h = str(Path.home())
#     s = str(path)
#     s = s.replace(h, "")
#     s = s.lstrip(S)
#     return s


# -)
