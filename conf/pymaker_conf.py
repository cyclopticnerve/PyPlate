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
# Integers
# ------------------------------------------------------------------------------

# values for line switches
I_SW_NONE = -1
I_SW_TRUE = 1
I_SW_FALSE = 0

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# current version
S_VERSION = "0.0.1"

# base dir for project type folders, relative to dev home
S_DIR_BASE = "Documents/Projects/Python"

# NB: format params are keys in D_TYPES and D_TYPES[key][0]
S_TYPE_FMT = "{} ({})"
# join each project type with this
S_TYPE_JOIN = " | "

# NB: format param is joined list of project types
S_ASK_TYPE = "Project type [{}]: "
S_ASK_NAME = "Project name: "
S_ASK_DESC = "Short description: "
# NB: format params are D_TYPE_SEC[prj_type], __PP_NAME_SMALL__
S_ASK_SEC = "{} name (default: {}): "

# error strings
S_ERR_TYPE = "Type must be one of {}"
S_ERR_LEN = "Project names must be more than 1 character"
S_ERR_START = "Project names must start with a letter"
S_ERR_END = "Project names must end with a letter or number"
S_ERR_MID = (
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

# TODO: which keys need to be global/which are only used once?
# keys for pybaker private dict
S_KEY_PRJ_DEF = "PRJ_DEF"
S_KEY_PRJ_DIST_DIRS = "PRJ_DIST_DIRS"
S_KEY_PRJ_EXTRA = "PRJ_EXTRA"
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

# python header/split dict keys
S_KEY_HDR = "S_KEY_HDR"
S_KEY_LEAD = "S_KEY_GRP_LEAD"
S_KEY_VAL = "S_KEY_GRP_VAL"
S_KEY_PAD = "S_KEY_GRP_PAD"
S_KEY_SWITCH = "S_KEY_SWITCH"
S_KEY_COMM = "S_KEY_COMM"
S_KEY_SPLIT = "S_KEY_SPLIT"

S_KEY_NAME_START = "S_KEY_NAME_START"
S_KEY_NAME_END = "S_KEY_NAME_END"
S_KEY_NAME_MID = "S_KEY_NAME_MID"

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
S_HOME = str(Path.home()).rstrip("/")
S_DIR_PRJ = (
    f"{S_HOME}/{S_DIR_BASE}/"  # /home/cn/Documents/Projects/Python/
    "{}"  # prj type dir
    f"/"  # /
    "{}"  # prj name
)

# paths relative to end user home only
S_USR_CONF = ".config"  # __PP_NAME_SMALL__ will be appended
S_USR_SRC = ".local/share"  # __PP_NAME_SMALL__ will be appended
S_USR_APPS = ".local/share/applications"  # for .desktop file
S_USR_BIN = ".local/bin"  # where to put the binary

# this is where the user libs will go
S_USR_LIB_NAME = "lib"
S_USR_LIB = ".local/share"  # __PP_AUTHOR__/S_USR_LIB_NAME will be appended

# commands for _do_after_fix
# NB: format param is (proj dir)
S_GIT_CMD = "git init {} -q"
# NB: format param is (proj dir)/S_ALL_VENV
S_VENV_CMD = "python -m venv {}"

# formats for tree
S_TREE_FILE = f"{S_ALL_MISC}/tree.txt"
S_TREE_DIR_FORMAT = " [] $NAME/"
S_TREE_FILE_FORMAT = " [] $NAME"

# switch constants
S_SW_ENABLE = "enable"
S_SW_DISABLE = "disable"
S_SW_REPLACE = "replace"

# ------------------------------------------------------------------------------
# Lists
# ------------------------------------------------------------------------------

# list of file types to use md/html/xml fixer
L_MARKUP = [
    "md",
    "html",
    "xml",
    "ui",
    "glade",
]

# files to remove after the project is done
# paths are relative to project dir
L_PURGE = [
    Path(S_ALL_SRC) / "ABOUT",
]

# ------------------------------------------------------------------------------
# Dictionaries
# ------------------------------------------------------------------------------

# NB: some of these are strictly for string replacement, but some are used by
# pybaker, so don't remove anything unless you know what you are doing
# if you want to ADD a key for string replacement only, use D_PRJ_EXTRA

# these are the settings that should be set before you run pymaker.py
# consider them the "before create" settings

# if you need to adjust any of these values in a function, use _do_before_fix()
# in this file

# NB: FOR THE LOVE OF GOD, DO NOT CHANGE THE KEYS IN THESE DICTS!!!

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
    # "__PP_LICENSE_IMG__": ,
    # # the url for license image click
    # "__PP_LICENSE_LINK__": "http://www.wtfpl.net",
    # the license file to use
    "__PP_LICENSE_FILE__": "LICENSE.txt",
    # the screenshot to use in  __PP_README_FILE__
    "__PP_SCREENSHOT__": f"{S_ALL_README}/screenshot.png",
    "__PP_RM_LICENSE__": (
        "[!"
        "[License: WTFPLv2]"
        "(https://img.shields.io/badge/License-WTFPL-brightgreen.svg "
        '"http://www.wtfpl.net")'
        "]"
        "(http://www.wtfpl.net)"
    ),
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
D_PRJ_DIST_DIRS = {
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
    "__PP_SUPPORT__": S_ALL_SUPPORT,  # where is rest of code
    "__PP_IMAGES__": S_ALL_IMAGES,  # where gui images are stored
}

# these values are string replace only
# NB: constant values moved here so we can change them easier
D_PRJ_EXTRA = {}

# these are settings that will be calculated for you while running pymaker.py
# consider them the "during create" settings
D_PRJ_CFG = {
    "__PP_TYPE_PRJ__": "",  # 'c'
    "__PP_NAME_BIG__": "",  # PyPlate
    "__PP_NAME_SMALL__": "",  # pyplate
    "__PP_NAME_SEC__": "",  # module1.py
    "__PP_NAME_CLASS__": "",  # Pascal case name for classes
    "__PP_DATE__": "",  # the date each file was created, updated every time
    "__PP_DUMMY__": "",  # dummy value to use in headers
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
    "__PP_SHORT_DESC__": "Short description",
    # the keywords to use in pyproject.toml and github
    "__PP_KEYWORDS__": [],
    # the python dependencies to use in __PP_README_FILE__, pyproject.toml,
    # github, and install.py
    "__PP_PY_DEPS__": {},
    # the markup for readme deps
    "__PP_RM_DEPS__": "",
    # the system dependencies to use in __PP_README_FILE__, github.com, and
    # install.py
    "__PP_SYS_DEPS__": [],
    # the categories to use in .desktop for gui apps
    "__PP_GUI_CATS__": [],
}

# the types of projects this script can create
# key is the short display name and the char to enter
# value[0] is the long display name
# value[1] is the template folder to copy
# value[2] is the top level folder to put each project in
D_TYPES = {
    "c": ["CLI", "cli", "CLIs"],
    "p": ["Package", "pkg", "Packages"],
    "g": ["GUI", "gui", "GUIs"],
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
        "CHANGELOG.md",
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
    f"{S_ALL_MISC}/snippets.txt": f"{S_ALL_MISC}/snippets.txt",
    f"{S_ALL_MISC}/style.txt": f"{S_ALL_MISC}/style.txt",
}

# the info for matching/fixing lines in markup files
D_MU_REPL = {
    S_KEY_HDR: r"^(\s*<!--\s*\S*\s*:\s*)(\S+)(.*-->.*)$",
    S_KEY_LEAD: 1,
    S_KEY_VAL: 2,
    S_KEY_PAD: 3,
    S_KEY_SWITCH: (
        r"^[^\S\r\n]*<!--[^\S\r\n]*pyplate[^\S\r\n]*:"
        r"[^\S\r\n]*(\S*)[^\S\r\n]*=[^\S\r\n]*(\S*)[^\S\r\n]*-->$"
    ),
    S_KEY_COMM: r"^\s*<!--(.*)-->\s*$",
    S_KEY_SPLIT: r"(\'|\")([^\'\"\n]+)(\'|\")|(<!--.*-->)$",
}

# the info for matching/fixing lines in non-markup files
D_PY_REPL = {
    S_KEY_HDR: r"^(\s*#\s*\S*\s*:\s*)(\S+)(.*)$",
    S_KEY_LEAD: 1,
    S_KEY_VAL: 2,
    S_KEY_PAD: 3,
    S_KEY_SWITCH: (
        r"^[^\S\r\n]*#[^\S\r\n]*pyplate[^\S\r\n]*:"
        r"[^\S\r\n]*(\S*)[^\S\r\n]*=[^\S\r\n]*(\S*)[^\S\r\n]*$"
    ),
    S_KEY_COMM: r"^\s*#",
    S_KEY_SPLIT: r"(\'|\")([^\'\"\n]+)(\'|\")|(#.*)$",
}

# the type of projects that will ask for a second name
D_NAME_SEC = {
    "p": "Module",
    "g": "Window class",
}

# default dict of block-level switches (should be I_SW_TRUE or I_SW_FALSE)
D_SW_BLOCK_DEF = {
    S_SW_REPLACE: I_SW_TRUE,
}

# default dict of line-level switches (should be I_SW_TRUE if present and
# enabled, I_SW_FALSE if present and disabled, or I_SW_NONE if not present)
D_SW_LINE_DEF = {
    S_SW_REPLACE: I_SW_NONE,
}

# regex's to match project name
D_NAME = {
    S_KEY_NAME_START: r"(^[a-zA-Z])",
    S_KEY_NAME_END: r"([a-zA-Z\d]$)",
    S_KEY_NAME_MID: r"(^[a-zA-Z\d\-_]*$)",
}

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Do any work before fix
# ------------------------------------------------------------------------------
def do_before_fix():
    """
    Do any work before fix

    Arguments:
        dir_prj: The root of the new project

    Do any work before fix. This method is called at the beginning of _do_fix,
    after all dunders have been configured, but before any files have been
    modified.
    It is mostly used to make final adjustments to the various dunder dicts
    before any replacement occurs.
    """

    # get values after pymaker has set them
    author = D_PRJ_DEF["__PP_AUTHOR__"]
    name_small = D_PRJ_CFG["__PP_NAME_SMALL__"]

    # paths relative to the end user's (or dev's) useful folders
    D_PRJ_CFG["__PP_USR_CONF__"] = f"{S_USR_CONF}/{name_small}"
    D_PRJ_CFG["__PP_USR_SRC__"] = f"{S_USR_SRC}/{name_small}"
    D_PRJ_CFG["__PP_USR_LIB__"] = f"{S_USR_LIB}/{author}/{S_USR_LIB_NAME}"

    # fix deps for readme
    d_deps = D_PRJ_META["__PP_PY_DEPS__"]
    s_deps = "None"
    if len(d_deps):
        s_deps = ""
        for key, val in D_PRJ_META["__PP_PY_DEPS__"]:
            s_deps += f"[{key}]({val}),"
    D_PRJ_META["__PP_RM_DEPS__"] = s_deps

# --------------------------------------------------------------------------
# Do any work after fix
# --------------------------------------------------------------------------
def do_after_fix(dir_prj, _dict_rep):
    """
    Do any work after fix

    Arguments:
        dir_prj: The root of the new project
        dict_rep: The dict of dunders to replace

    Do any work after fix. This method is called at the end of the internal
    _do_after_fix, after all files have been modified.
    """

    for root, _root_dirs, root_files in dir_prj.walk():

        # convert files into Paths
        files = [root / f for f in root_files]

        # for each file item
        for item in files:
            # check if readme
            if root == dir_prj and item.name == "README.md":
                _fix_readme(item)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Edit/remove parts of the main README file
# --------------------------------------------------------------------------
def _fix_readme(path):
    """
    Edit/remove parts of the main README file

    Arguments:
        path: Path for the README to remove text
        dict_rep: The dict of dunders to replace

    Edits/removes parts of the file using the C.D_PRJ_CFG settings.
    """

    # the whole text of the file
    text = ""

    # open and read whole file
    with open(path, "r", encoding="UTF-8") as a_file:
        text = a_file.read()

    # find the remove blocks
    prj_type = D_PRJ_CFG["__PP_TYPE_PRJ__"]
    if prj_type == "c" or prj_type == "g":
        str_pattern = r"<!-- __RM_PKG_START__ -->(.*?)<!-- __RM_PKG_END__ -->"
    else:
        str_pattern = r"<!-- __RM_APP_START__ -->(.*?)<!-- __RM_APP_END__ -->"

    # replace block with empty string (equiv to deleting it)
    # NB: need S flag to make dot match newline
    text = re.sub(str_pattern, "", text, flags=re.S)

    # save file
    with open(path, "w", encoding="UTF-8") as a_file:
        a_file.write(text)


# -)