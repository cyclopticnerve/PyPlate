# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: settings.py                                           |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module separates out the constants from pymaker.py/pybaker.py.
"""

# TODO: all dict keys that are currently dunders need to be constants
# put dunders in separate .py file to share with pybaker
# NEXT: put i18n back in for error messages and file/dir names

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path

# pylint: disable=no-name-in-module

# my imports
from . import keys as K  # type: ignore

# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# help/version strings
S_NAME_BIG = "PyMaker"
S_NAME_SMALL = "pymaker"

# version option strings
S_VER_OPTION = "v"
S_VER_ACTION = "version"

# debug option strings
S_DBG_OPTION = "d"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP = "enable debugging option"

# string constants for pymaker
S_PRJ_NAME = "Project/Package name"
S_PRJ_NAME_MOD = "Module name"
S_PRJ_NAME_ERR = 'Project "{}" already exists in "{}"'
S_PRJ_NAME_LEN = "Project names must be more than 1 character"
S_PRJ_NAME_START = "Project names must start with a letter"
S_PRJ_NAME_END = "Project names must end with a letter or number"
S_PRJ_NAME_CONTAIN = (
    "Project names must contain only letters, numbers,"
    "dashes (-), or underscores (_)"
)
S_PRJ_TYPE = "Project type"
S_PRJ_TYPE_INVALID = "Please enter a valid project type"

# formats for tree
S_TREE_DIR_FORMAT = " [] $NAME/"
S_TREE_FILE_FORMAT = " [] $NAME"

# dir names, relative to PyPlate or project dir
S_DIR_VENV = ".venv"
S_DIR_ALL = "all"
S_DIR_LIB = "lib"
S_DIR_MISC = "misc"
S_DIR_PP = "pyplate"
S_DIR_TEMPLATE = "template"
S_DIR_CONF = "conf"
S_DIR_CONF_DEFS = "defaults"

# paths relative to end user only
S_USR_CONF = ".config"
S_USR_SHARE = ".local/share"

# file names
S_FILE_TOML = "pyproject.toml"
S_FILE_METADATA = "metadata.json"
S_FILE_METADATA_DEF = "metadata_default.json"
S_FILE_SETTINGS = "settings.json"
S_FILE_SETTINGS_DEF = "settings_default.json"
S_FILE_TREE = "tree.txt"
S_FILE_README = "README.md"

# commands for _do_after_fix
S_CMD_GIT = "git init {} -q"
S_CMD_VENV = "python -m venv {}"

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------

# this is the dir above where the script is being run from (e.g.
# ~/Documents/Projects/Python/PyPlate/)
P_DIR_PYPLATE = Path(__file__).parents[1]

# path to lib project (e.g. ~/Documents/Projects/Python/PyPlate/lib)
P_DIR_LIB = P_DIR_PYPLATE / S_DIR_LIB

# this is the dir where the template files are located relative to this script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
P_DIR_TEMPLATE = P_DIR_PYPLATE / S_DIR_TEMPLATE

# this is the location where the project's subdir will be (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
P_DIR_BASE = P_DIR_PYPLATE.parent

# the location of pyplate's metadata (we update this at runtime)
P_PP_METADATA = P_DIR_PYPLATE / S_DIR_CONF / S_FILE_METADATA

# ------------------------------------------------------------------------------
# Lists
# ------------------------------------------------------------------------------

# the type of projects that will ask for a module name
L_PKG = ["p"]

# ------------------------------------------------------------------------------
# Dictionaries
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by pybaker.py (from
# <project>/pyplate/conf/settings.json)
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
    # the license name, used in headers, S_FILE_README, and pyproject.toml
    "__PD_LICENSE_NAME__": "WTFPLv2",
    # the license image source, used in S_FILE_README
    "__PD_LICENSE_IMG__": "https://img.shields.io/badge/License-WTFPL-brightgreen.svg",
    # the url for license image click
    "__PD_LICENSE_LINK__": "http://www.wtfpl.net",
    # the license file to use
    "__PD_LICENSE_FILE__": "LICENSE.txt",
    # the screenshot to use in  S_FILE_README
    "__PD_SCREENSHOT__": "README/screenshot.png",
    # version format string for command line
    "__PD_VER_FMT__": "Version {}",
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
    "__PD_README_FILE__": S_FILE_README,
    # absolute path of libs in PP
    "__PD_DEV_LIB__": str(P_DIR_LIB),
    # location of config files, relative to the project dir
    "__PD_DEV_CONF__": S_DIR_CONF,
    # location of src files, relative to the project dir
    "__PD_DEV_SRC__": "src",
    # --------------------------------------------------------------------------
    # these paths are relative to the user's home dir
    "__PD_USR_APPS__": ".local/share/applications",  # for .desktop file
    "__PD_USR_BIN__": ".local/bin",  # where to put the exe
}

D_PRJ_CFG = {
    # --------------------------------------------------------------------------
    # these items will be filled in by _get_project_info
    "__PC_TYPE_PRJ__": "",  # 'c'
    "__PC_DIR_PRJ__": "",  # '~/Documents/Projects/Python/CLIs/PyPlate'
    "__PC_NAME_BIG__": "",  # PyPlate
    "__PC_NAME_SMALL__": "",  # pyplate
    "__PS.NAME_MOD__": "",  # module1.py
    "__PC_NAME_CLASS__": "",  # Pascal case name for classes
    "__PC_DATE__": "",  # the date eac__PPh file was created, updated every time
    # --------------------------------------------------------------------------
    # these paths are calculated at runtime relative to the user's home dir
    "__PC_USR_CONF__": "",  # config dir
    "__PC_USR_LIB__": "",  # location of cnlibs dir
    "__PC_USR_SRC__": "",  # where the program will keep it's source
    # --------------------------------------------------------------------------
    # I18N dict calculated further down
    "__PC_I18N__": {},
}

# the default metadata that the final project will use for pybaker.py
# NB: all of these values will need to be set later before running pybaker.py
D_PRJ_META = {
    # the version number to use in S_FILE_README and pyproject.toml
    "__PM_VERSION__": "",
    # the short description to use in S_FILE_README and pyproject.toml
    "__PM_SHORT_DESC__": "",
    # the keywords to use in pyproject.toml and github
    "__PM_KEYWORDS__": [],
    # the python dependencies to use in S_FILE_README, pyproject.toml, github,
    # and install.py
    "__PM_PY_DEPS__": {},
    # the system dependencies to use in S_FILE_README, github.com, and
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
        ".venv",
        ".vscode",
        "docs",
        "misc",
        "README",
        "CHANGELOG.md",
        "LICENSE.txt",
        "requirements.txt",
        "**/__pycache__",
        "lib",
        "pyplate",
        "locale",
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
        ".venv",
        ".vscode",
        ".VSCodeCounter",
        "**/__pycache__",
        "lib",
    ],
}

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
    K.S_KEY_LOCALE: "locale",
    K.S_KEY_PO: "po",
}
D_PRJ_CFG["__PC_I18N__"] = D_I18N

# dict of files ""that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project, it gets copied
# to the project, and cuts down on duplicate files
# key is the relative path to the source file in PyPlate
# val is the relative path to the dest file in the project dir
D_COPY = {
    "misc/snippets.txt": "misc/snippets.txt",
    "misc/style.txt": "misc/style.txt",
    "src/pybaker.py": "pyplate/pybaker.py",
    "conf/keys.py": "pyplate/conf/keys.py",
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

# the dict of keys to replace in the header of each file
# these values are used to find matching lines in the file that are assumed to
# be header lines, if they match the pattern used in _fix_header()
# the file header line should contain lines that match the pattern:
# '# <Key>: <val> ...'
# or
# '<!-- <key>: <val> ... -->'
# where <key> is one of the keys here, and <val> is one of the dunders from
# PyMaker's _dict_prj dictionary
# if <key> does not match one of these items, the line is left untouched
# an example header:
# ------------------------------------------------------------------------------
# Project : __PC_NAME_BIG__                                        /          \
# Filename: __PC_NAME_SMALL__.py                                  |     ()     |
# Date    : __PC_DATE__                                           |            |
# Author  : __PD_AUTHOR__                                         |   \____/   |
# License : __PD_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------
# spaces don't matter, but the colon does right aligned text at the end of each
# line will be preserved the key in each item is the key to look for, and the
# value is the key in  _dict_prj to replace it with NB: The Filename key
# requires special handling that is, if the value for Filename is blank, it
# will be replaced by the file's name (including extension) If the value is
# something besides a dunder (with or without extension) it will be left alone
# an example, assuming __PC_NAME_SMALL__ = 'foobar' and the file's name is
# 'some_file.py':
# ------------------------------------------------------------------------------
# before                         | after
# ------------------------------------------------------------------------------
# Filename:                      | # Filename: some_file.py
# Filename: some_file            | # Filename: some_file
# Filename: some_file.py         | # Filename: some_file.py
# Filename: __PC_NAME_SMALL__    | # Filename: foobar
# Filename: __PC_NAME_SMALL__.py | # Filename: foobar.py
# ------------------------------------------------------------------------------
D_HEADER = {
    "Project": "__PC_NAME_BIG__",  # PyPlate
    "Filename": "__PC_NAME_SMALL__",  # pyplate.py
    "Date": "__PC_DATE__",  # 12/08/2022
    "Author": "__PD_AUTHOR__",  # cyclopticnerve
    "License": "__PD_LICENSE_NAME__",  # WTFPLv2
}

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
    "RM_FILENAME": S_FILE_README,
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

# regex strings for toml
R_TOML_NAME = r"(^\s*\[project\]\s*$)(.*?)(^\s*name[\t ]*=[\t ]*)(.*?$)"
R_TOML_NAME_REP = r'\g<1>\g<2>\g<3>"{}"'
R_TOML_VERSION = r"(^\s*\[project\]\s*$)(.*?)(^\s*version[\t ]*=[\t ]*)(.*?$)"
R_TOML_VERSION_REP = r'\g<1>\g<2>\g<3>"{}"'
R_TOML_DESC = r"(^\s*\[project\]\s*$)(.*?)(^\s*description[\t ]*=[\t ]*)(.*?$)"
R_TOML_DESC_REP = r'\g<1>\g<2>\g<3>"{}"'
R_TOML_KEYS = r"(^\s*\[project\]\s*$)(.*?)(^\s*keywords[\t ]*=[\t ]*)(.*?\])"
R_TOML_KEYS_REP = r"\g<1>\g<2>\g<3>[{}]"
R_TOML_DEPS = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*dependencies[\t ]*=[\t ]*)(.*?\])"
)
R_TOML_DEPS_REP = r"\g<1>\g<2>\g<3>[{}]"

# regex strings for readme
R_RM_START = D_README["RM_LICENSE"]["RM_LICENSE_START"]
R_RM_END = D_README["RM_LICENSE"]["RM_LICENSE_END"]
R_README = rf"({R_RM_START})(.*?)({R_RM_END})"
R_README_REP = r"\g<1>\n{}\n\g<3>"

# regex strings for headers
R_HEADER = (
    # key = item[0]
    r"("  # start group 1
    r"("  # start group 2
    r"\s*"  # group 2
    r"(#|<!--)"  # group 3 (comment marker)
    r"\s*"  # group 2
    r")"  # end group 2
    r"({})"  # group 4 (key)
    r"(\s*:\s*)"  # group 5
    r")"  # end group 1
    r"("  # start group 6
    r"([^\.\s]*)"  # group 7 (dunder)
    r"([\.\S]*)"  # group 8 (file extension, if present)
    r"(\s*)"  # group 9 (padding for right-aligned text)
    r"([^\n]*)"  # group 10 (right aligned text)
    r")"  # end group 6
)
R_HEADER_REP = r"\g<1>{}\g<8>{}\g<10>"

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Set up user paths
# ------------------------------------------------------------------------------
def get_user_paths():
    """
    Set up user paths

    Here we calculate the different paths to use for dunder replacement. It is
    done as a function so we can call it after the project name has been set.
    """

    # get values after pymaker has set them
    author = D_PRJ_DEF["__PD_AUTHOR__"]
    name_small = D_PRJ_CFG["__PC_NAME_SMALL__"]

    # paths relative to the end user's (or dev's) useful folders
    D_PRJ_CFG["__PC_USR_CONF__"] = f"{S_USR_CONF}/{name_small}"
    D_PRJ_CFG["__PC_USR_LIB__"] = f"{S_USR_SHARE}/{author}/{S_DIR_LIB}"
    D_PRJ_CFG["__PC_USR_SRC__"] = f"{S_USR_SHARE}/{name_small}"


# -)
