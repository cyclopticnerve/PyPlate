# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pyplateconstants.py                                   |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module separates out the constants from pymaker.py/pybaker.py.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_SELF = Path(__file__).parent  # /some/dir/pyplate

# this is the dir above where the script is being run from (e.g.
# ~/Documents/Projects/Python/PyPlate/)
DIR_PYPLATE = DIR_SELF.parent

# this is the dir where the template files are located relative to this script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
DIR_TEMPLATE = DIR_PYPLATE / "template"

# this is the location where the project's subdir will be (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
DIR_BASE = DIR_PYPLATE.parent

# the dict of user info to be replaced in the headers and text of a new project
# they are placed here to be easily modified by subsequent users
# they are then copied to G_DICT_SETTINGS to be used here and copied to the
# project dir for use by pybaker.py
DICT_USER = {
    # the author name, used in headers and pyproject.toml
    "__PP_AUTHOR__": "cyclopticnerve",
    # the author's email, used in headers and pyproject.toml
    "__PP_EMAIL__": "cyclopticnerve@gmail.com",
    # the license name, used in headers, README.md, and pyproject.toml
    "__PP_LICENSE_NAME__": "WTFPLv2",
    # the license image source, used in README.md
    "__PP_LICENSE_IMG__": "https://img.shields.io/badge/License-WTFPL-brightgreen.svg",
    # the url for license image click
    "__PP_LICENSE_LINK__": "http://www.wtfpl.net",
    # the license file to use
    "__PP_LICENSE_FILE__": "LICENSE.txt",
    # the screenshot to use in  README.md
    "__PP_SCREENSHOT__": "",
    # NB: the struggle here is that using the fixed format results in a
    # four-digit year, but using the locale format ('%x') results in a two-digit
    # year (at least for my locale, which in 'en_US').
    # so what to do? what i really want is a locale format that uses four-digit
    # years everywhere. so i am faced with a 'cake and eat it too' situation.
    # not sure how to proceed but i think for now i will leave this as a
    # user-editable string and place it in the realm of 'edit it before you run'
    # along with author/email/license/etc
    "__PP_DATE_FMT__": "%m/%d/%Y",
}

# the types of projects this script can create
# key is the short type name (used for entry)
# val[0] is the long type name (used for display)
# val[1] is the subdir name under _DIR_BASE where the project will be created
# val[2] is the dir(s) under 'template' to get the files
# order is arbitrary, just decided to make it alphabetical
DICT_TYPES = {
    "c": ["CLI", "CLIs", "cli"],
    "g": ["GUI", "GUIs", "gui"],
    "p": ["Package", "Packages", "pkg"],
}

# the types of projects that will have i18n applied
LIST_I18N = ["g"]

# the type of projects that will ask for a module name
LIST_PKG = ["p"]

# the list of keys to replace in the header of each file
# these values are used to find matching lines in the file that are assumed to
# be header lines, if they match the pattern used in _fix_header()
# the file header line should contain lines that match the pattern:
# '# <Key>: <val> ...'
# or
# '<!-- <key>: <val> ...'
# where <key> is one of the items here, and <val> is one of the keys from
# G_DICT_SETTINGS
# if <key> does not match one of these items, the line is left untouched
# an example header:
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__.py                                  |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------
# spaces don't matter, but the colon does
# right aligned text at the end of each line will be preserved
# the first entry in each sub-list is the key to look for, and the second entry
# is the default G_DICT_SETTINGS key to use if the value is empty
# NB: The Filename key requires special handling
# That is, if the value for Filename is blank and has no ext, it will be
# replaced by the file's name (including extension)
# If the value is something besides a dunder (with or without extension) it will
# be left alone
LIST_HEADER = [
    [
        "Project",
        "__PP_NAME_BIG__",
    ],  # PyPlate
    [
        "Filename",
        "__PP_NAME_SMALL__",
    ],  # pyplate.py
    [
        "Date",
        "__PP_DATE__",
    ],  # 12/08/2022
    [
        "Author",
        "__PP_AUTHOR__",
    ],  # cyclopticnerve
    [
        "License",
        "__PP_LICENSE_NAME__",
    ],  # WTFPLv2
]

# the dict of sections to remove in the README file
# key is the project type we are making (may contain multiple project types)
# or a special section of the readme
# rm_delete_start is the tag at the start of the section to remove
# rm_delete_end is the tag at the end of the section to remove
# NB: these tags start with 'RM' instead of 'PP' because most 'PP' keys will
# remain in the file, and we don't want pybaker to report their presence as an
# error
# this way you can have different sections in the readme for things like
# installation instructions, depending on whether your project is a package or a
# cli/gui app
DICT_README = {
    "RM_FILENAME": "README.md",
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

# this is the set of dirs/files we don't mess with in the final project
# each item can be a full path, a path relative to the project directory, or
# glob
# see https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
# NB: you can use dunders here since the path is the last thing to get fixed
# these dir/file names should match what's in the template dir (before any
# modifications, hence using dunder keys)
DICT_BLACKLIST = {
    # skip header, skip text, skip path (0 0 0)
    # NB: this is mostly to speed up processing by not even looking at them
    "PP_SKIP_ALL": [
        ".git",
        ".venv",
        ".vscode",
        "docs",
        "misc",
        "README",
        "**/locale",
        "CHANGELOG.md",
        "LICENSE.txt",
        "requirements.txt",
        "**/__pycache__",
        "lib",
    ],
    # skip header, skip text, fix path (0 0 1)
    # NB: this is used mostly for non-text files
    "PP_SKIP_CONTENTS": [
        "**/*.png",
        "**/*.jpg",
        "**/*.jpeg",
    ],
    # skip header, fix text, fix path (0 1 1)
    # NB: not sure what this is useful for, but here it is
    "PP_SKIP_HEADER": [],
    # fix header, skip text, fix path (1 0 1)
    # NB: mostly used for files that contain dunders that will be replaced later
    # or files we only want to replace headers in
    "PP_SKIP_TEXT": [
        "conf/*",
        "MANIFEST.in",
        ".gitignore",
    ],
    # fix header, fix text, skip path (1 1 0)
    # NB: not really useful, since we always want to fix paths with dunders, but
    # included for completeness
    "PP_SKIP_PATH": [],
    # list of dirs/files to ignore in output dir when creating the initial tree
    # NB: each item can be a partial path relative to the project directory, or
    # a glob
    "PP_SKIP_TREE": [
        ".git",
        ".venv",
        ".vscode",
        ".VSCodeCounter",
        "**/__pycache__",
        "lib",
    ],
}

# the default metadata that the final project will use for pybaker.py
# NB: all of these values will need to be set later before running pybaker.py
DICT_METADATA = {
    # the version number to use in README.md and pyproject.toml
    "__PP_VERSION__": "",
    # the short description to use in README.md and pyproject.toml
    "__PP_SHORT_DESC__": "",
    # the keywords to use in pyproject.toml and github
    "__PP_KEYWORDS__": [],
    # the python dependencies to use in README.md, pyproject.toml, github, and
    # install.py
    "__PP_PY_DEPS__": {},
    # the system dependencies to use in README.md, github.com, and install.py
    "__PP_SYS_DEPS__": [],
    # the categories to use in .desktop for gui apps
    "__PP_GUI_CATEGORIES__": [],
}

# dict of files that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project, it gets copied
# to the project, and cuts down on duplicate files
# key is the relative path to the source file in PyPlate
# val is the relative path to the dest file in the project dir
DICT_COPY = {
    ".gitignore": ".gitignore",
    "misc/checklist.txt": "misc/checklist.txt",
    "misc/snippets.txt": "misc/snippets.txt",
    "misc/style.txt": "misc/style.txt",
    "src/pybaker.py": "conf/pybaker.py",
    "lib/cnlib": "lib/cnlib",
}

# string constants for pymaker
S_PRJ_TYPE = "Project type"
S_PRJ_NAME = "Project name"
S_MOD_NAME = "Module name"
S_NAME_ERR = 'Project "{}" already exists in "{}"'
S_NAME_VENV = ".venv"
S_PRJ_TYPE_INVALID = "Please enter a valid project type"
S_PRJ_NAME_LEN = "Project names must be more than 1 character"
S_PRJ_NAME_START = "Project names must start with a letter"
S_PRJ_NAME_END = "Project names must end with a letter or number"
S_PRJ_NAME_CONTAIN = (
    "Project names must contain only letters, numbers,"
    "dashes (-), or underscores (_)"
)

# formats for tree
S_TREE_DIR_FORMAT = " [] $NAME/"
S_TREE_FILE_FORMAT = " [] $NAME"

# directory names
S_DIR_ALL = "all"
S_DIR_TESTS = "tests"
S_DIR_CONF = "conf"
S_DIR_DEFS = "defaults"
S_DIR_MISC = "misc"
S_DIR_LOCALE = "locale"

# file names
S_FILE_TREE = "tree.txt"
S_FILE_BLACKLIST = "blacklist.json"
S_FILE_METADATA = "metadata.json"
S_FILE_SETTINGS = "settings.json"
S_FILE_BLACKLIST_DEF = "blacklist_default.json"
S_FILE_METADATA_DEF = "metadata_default.json"
S_FILE_SETTINGS_DEF = "settings_default.json"

# config file paths
S_PATH_BLACKLIST = f"{S_DIR_CONF}/{S_FILE_BLACKLIST}"
S_PATH_BLACKLIST_DEF = f"{S_DIR_CONF}/{S_DIR_DEFS}/{S_FILE_BLACKLIST_DEF}"
S_PATH_METADATA = f"{S_DIR_CONF}/{S_FILE_METADATA}"
S_PATH_METADATA_DEF = f"{S_DIR_CONF}/{S_DIR_DEFS}/{S_FILE_METADATA_DEF}"
S_PATH_SETTINGS = f"{S_DIR_CONF}/{S_FILE_SETTINGS}"
S_PATH_SETTINGS_DEF = f"{S_DIR_CONF}/{S_DIR_DEFS}/{S_FILE_BLACKLIST_DEF}"

# -)
