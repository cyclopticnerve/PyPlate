# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pyplate.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines

"""
This module separates out the constants from pymaker.py. It also includes hook
functions to extend the functionality of pymaker.py and pybaker.py.
This file, and the template folder, are the main ways to customize PyPlate.
"""

# FIXME: I18N tags
# FIXME: format params

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import locale
from pathlib import Path
import re
import tarfile

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ABSOLUTE CURRENT PATH OF PyPlate
P_DIR_PP = Path(__file__).parents[1].resolve()

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py

T_DOMAIN = "pyplate"
T_DIR_PRJ = Path(__file__).parents[1].resolve()
T_DIR_LOCALE = f"{T_DIR_PRJ}/i18n/locale"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------
# Bools
# ------------------------------------------------------------------------------

# global debug flag
B_DEBUG = False
# create a git using S_CMD_GIT
# B_CMD_GIT = True
# # create a venv using S_VENV_CREATE
# B_CMD_VENV = True
# # do i18n
# B_CMD_I18N = True
# # create a tree and save it to S_TREE_FILE
# B_CMD_TREE = True
# # create docs
# B_CMD_DOCS = True
# # do install/uninstall
# B_CMD_INST = True

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

# default encoding
S_ENCODING = "UTF-8"
# I18N: date format
S_DATE_FMT = _("%m/%d/%Y")
# I18N: make version pretty
# NB: format param is D_PUB_META["__PP_VERSION__"]
S_VER_FMT = _("Version {}")

# I18N: ask user for project name
S_ASK_NAME = _("Project name: ")
# NB: format params are L_TYPES[item][0] and L_TYPES[item][1]
S_TYPE_FMT = "{} ({})"
# join each project type in L_TYPES with this
S_TYPE_JOIN = " | "
# I18N: ask for project type
# NB: format param is joined list of project types from L_TYPES
S_ASK_TYPE = _("Project type [{}]: ")
# I18N: ask for module name in pkg project
# NB: format param is __PP_NAME_PRJ_SMALL__
S_ASK_SEC_P = _("Module name (default: {}): ")
# I18N: ask for window class name in gui project
# NB: format param is __PP_NAME_PRJ_SMALL__
S_ASK_SEC_G = _("Window class name (default: {}): ")

# I18N: sk for project name when running from vscode run/debug
# NB: format param is current working dir
S_ASK_IDE = _("Project name: (Relative to {}): ")

# error strings

# I18N: user entered wrong project type
# NB: format param is joined list of project types from L_TYPES
S_ERR_TYPE = _("Type must be one of {}")
# I18N: project name is too short
S_ERR_LEN = _("Project names must be more than 1 character")
# I18N: project name must start with letter
S_ERR_START = _("Project names must start with a letter")
# I18N: project names must end with a letter or number
S_ERR_END = _("Project names must end with a letter or number")
# I18N: project name contains invalid characters
S_ERR_MID = _(
    "Project names must contain only letters, numbers, dashes (-), or "
    "underscores (_)"
)
# I18N: project already exists
# NB: format param is __PP_NAME_PRJ_BIG__
S_ERR_EXIST = _('Project "{}" already exists')
# I18N:project does not exist (when pb run from ide)
# NB: format param is full path to user entry (when pb run from ide)
S_ERR_NOT_EXIST = _('Project "{}" does not exist')
# I18N: running pybaker on an invalid project
S_ERR_NOT_PRJ = _(
    "This folder does not have a 'pyplate' folder.\nAre you sure this is a "
    "PyPlate project?"
)
# I18N: invalid semantic version format
S_ERR_VERS = _("Version must be n.n.n(xxx)")
# I18N:don't run pm in pyplate prj dir
S_ERR_PRJ_DIR_IS_PP = _("Cannot run pymaker in PyPlate dir")
# I18N: invalid category in .desktop file
# NB: format param is item in L_CATS
S_ERR_DESK_CAT = (
    '"{}" is not a valid desktop category, see '
    "https://specifications.freedesktop.org/menu-spec/latest/apa.html"
)

# ------------------------------------------------------------------------------

# output msg for steps
S_ACTION_COPY = _("Copy template files... ")
S_ACTION_BEFORE = _("Do before fix... ")
S_ACTION_FIX = _("Do fix... ")
S_ACTION_AFTER = _("Do after fix... ")
S_ACTION_GIT = _("Make git folder... ")
S_ACTION_VENV = _("Make venv folder... ")
S_ACTION_LIB = _("Install libs in venv... ")
S_ACTION_I18N = _("Make i18n folder... ")
S_ACTION_DESK = _("Fixing desktop file... ")
S_ACTION_DOCS = _("Make docs folder... ")
S_ACTION_TREE = _("Make tree file... ")
S_ACTION_INST_PKG = _("Install package in venv... ")
S_ACTION_DIST = _("Make dist folder... ")
S_ACTION_INST = _("Make install file... ")
S_ACTION_DONE = _("Done")
S_ACTION_FAIL = _("Failed")

# debug-specific strings
# I18N: warn user that they are running in debug mode
S_MSG_DEBUG = _(
    "WARNING! YOU ARE IN DEBUG MODE!\nIT IS POSSIBLE TO OVERWRITE EXISTING "
    "PROJECTS!\n"
)

# ------------------------------------------------------------------------------

# keys for pybaker private dict
S_KEY_PRV_ALL = "PRV_ALL"
S_KEY_PRV_PRJ = "PRV_PRJ"

# keys for metadata, blacklist, i18n in pybaker dev dict
S_KEY_PUB_META = "PUB_META"
S_KEY_PUB_BL = "PUB_BL"
S_KEY_PUB_I18N = "PUB_I18N"
S_KEY_PUB_INSTALL = "PUB_INSTALL"
S_KEY_PUB_DIST = "PUB_DIST"
S_KEY_PUB_DBG = "PUB_DBG"

# keys for blacklist
S_KEY_SKIP_ALL = "SKIP_ALL"
S_KEY_SKIP_CONTENTS = "SKIP_CONTENTS"
S_KEY_SKIP_HEADER = "SKIP_HEADER"
S_KEY_SKIP_CODE = "SKIP_CODE"
S_KEY_SKIP_PATH = "SKIP_PATH"
S_KEY_SKIP_TREE = "SKIP_TREE"

# keys for i18n
S_KEY_CHARSET = "CHARSET"
S_KEY_CLANGS = "CLANGS"
S_KEY_WLANGS = "WLANGS"
S_KEY_NO_EXT = "NO_EXT"
S_KEY_LOCALE = "LOCALE"
S_KEY_PO = "PO"
S_KEY_MO = "MO"

# keys for D_PUB_DBG
S_KEY_DBG_GIT = "DBG_GIT"
S_KEY_DBG_VENV = "DBG_VENV"
S_KEY_DBG_I18N = "DBG_I18N"
S_KEY_DBG_DOCS = "DBG_DOCS"
S_KEY_DBG_INST = "DBG_INST"
S_KEY_DBG_TREE = "DBG_TREE"

# python header/split dict keys
S_KEY_HDR = "S_KEY_HDR"
S_KEY_LEAD = "S_KEY_GRP_LEAD"
S_KEY_VAL = "S_KEY_GRP_VAL"
S_KEY_PAD = "S_KEY_GRP_PAD"
S_KEY_SWITCH = "S_KEY_SWITCH"
S_KEY_COMM = "S_KEY_COMM"
S_KEY_SPLIT = "S_KEY_SPLIT"
S_KEY_SPLIT_INDEX = "S_KEY_SPLIT_INDEX"

# constants for _check_name()
S_KEY_NAME_START = "S_KEY_NAME_START"
S_KEY_NAME_END = "S_KEY_NAME_END"
S_KEY_NAME_MID = "S_KEY_NAME_MID"

# dir names, relative to PP template, or project dir
# NB: if you change anything in the template structure, you should revisit this
# and make any appropriate changes
# also make sure that these names don't appear in the blacklist, or else
# pymaker won't touch them
S_DIR_TEMPLATE = "template"
S_DIR_ALL = "all"
S_DIR_BIN = "bin"
S_DIR_LIB = "lib"
S_DIR_GIT = ".git"
S_DIR_CONF = "conf"
S_DIR_VENV = ".venv"
S_DIR_DOCS = "docs"
S_DIR_DOCS_TPLT = "pdoc3"
S_DIR_MISC = "misc"
S_DIR_README = "readme"
S_DIR_SRC = "src"
S_DIR_SUPPORT = "support"
S_DIR_UI = "ui"
S_DIR_I18N = "i18n"
S_DIR_IMAGES = "images"
S_DIR_LOCALE = "locale"
S_DIR_PO = "po"
S_DIR_MO = "mo"
S_DIR_TESTS = "tests"
S_DIR_SCRATCH = "scratch"
S_DIR_GUI = "gui"
S_DIR_DESKTOP = "desktop"
S_DIR_DIST = "dist"
S_DIR_ASSETS = "assets"
S_DIR_INSTALL = "install"
S_DIR_UNINSTALL = "uninstall"

# common file names, rel to prj dir or pyplate dir
S_FILE_LICENSE = "LICENSE.txt"
S_FILE_README = "README.md"
S_FILE_TOML = "pyproject.toml"
S_FILE_REQS = "requirements.txt"
S_FILE_INST_CFG = "install.json"
S_FILE_UNINST_CFG = "uninstall.json"
S_FILE_INST_PY = "install.py"
S_FILE_UNINST_PY = "uninstall.py"
S_FILE_LOGO = "logo.mako"

# i18n stuff
S_I18N_TAG = "I18N"

# concatenate some paths
S_PATH_TMP_ALL = f"{S_DIR_TEMPLATE}/{S_DIR_ALL}"
S_PATH_INST_CFG = f"{S_DIR_INSTALL}/{S_FILE_INST_CFG}"
S_PATH_UNINST_CFG = f"{S_DIR_UNINSTALL}/{S_FILE_UNINST_CFG}"

# fix reqs cmds
S_FILE_REQS_ALL = f"{S_DIR_TEMPLATE}/{S_DIR_ALL}/{S_FILE_REQS}"
# NB: format param is L_TYPES[item][2] (long prj type, subdir in template)
S_FILE_REQS_TYPE = f"{S_DIR_TEMPLATE}/" + "{}/" + f"{S_FILE_REQS}"

# .desktop stuff
S_NAME_DSK_TMP = "template"
S_FILE_DSK_TMP = (
    f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_DESKTOP}/{S_NAME_DSK_TMP}.desktop"
)

# I18N stuff
S_PATH_LOCALE = str(Path(S_DIR_I18N) / S_DIR_LOCALE)
S_PATH_PO = str(Path(S_DIR_I18N) / S_DIR_PO)
S_PATH_MO = str(Path(S_DIR_I18N) / S_DIR_MO)

# paths relative to end user home only
S_USR_SHARE = ".local/share"  # bulk of the program goes here
S_USR_APPS = ".local/share/applications"  # for .desktop out file
S_USR_BIN = ".local/bin"  # where to put the binary

# formats for tree
S_TREE_NAME = "tree.txt"
S_TREE_FILE = f"{S_DIR_MISC}/{S_TREE_NAME}"
S_TREE_DIR_FORMAT = " [] $NAME/"
S_TREE_FILE_FORMAT = " [] $NAME"

# format for venv
# NB: format param is __PP_NAME_PRJ_SMALL__
S_VENV_FMT_NAME = ".venv-{}"

# switch constants
S_SW_ENABLE = "enable"
S_SW_DISABLE = "disable"
S_SW_REPLACE = "replace"

# path to prj pyplate files, relative to prj dir
# NB: leave as string, no start dir yet
S_PRJ_PP_DIR = "pyplate"
S_PRJ_PUB_CFG = f"{S_PRJ_PP_DIR}/project.json"
S_PRJ_PRV_DIR = f"{S_PRJ_PP_DIR}/private"
S_PRJ_PRV_CFG = f"{S_PRJ_PRV_DIR}/private.json"

# ------------------------------------------------------------------------------
# commands for _do_after_fix

# cmd for git
# NB: format param is proj dir
S_CMD_GIT_CREATE = "git init {} -q"
# NB: format params are prj dir and venv name
S_CMD_VENV_ACTIVATE = "cd {};. {}/bin/activate"
# NB: format param is prj dir
S_CMD_INSTALL_PKG = "cd {};python -m pip install -e ."
# cmd for pdoc3
# NB: format params are path to pp, path to pp venv, path to project, path to
# project's template, path to project's docs dir, and path to project's input
# (src) dir
S_CMD_DOC = (
    "cd {};"
    ". {}/bin/activate;"
    "cd {};"
    "pdoc --html --force --template-dir {} -o {} {}"
)
# cmd to install libs as editable
# NB: format param is relative path to cnlib dir
S_CMD_INST_LIB = "python -m pip install -e {}"

# ------------------------------------------------------------------------------
# regex stuff

# fix readme
S_RM_PKG = r"<!-- __RM_PKG__ -->(.*?)<!-- __RM_PKG__ -->"
S_RM_APP = r"<!-- __RM_APP__ -->(.*?)<!-- __RM_APP__ -->"

S_RM_DESC_SCH = (
    r"(<!--[\t ]*__RM_SHORT_DESC__[\t ]*-->)"
    r"(.*?)"
    r"(<!--[\t ]*__RM_SHORT_DESC__[\t ]*-->)"
)
S_RM_DESC_REP = r"\g<1>\n{}\n\g<3>"

S_RM_VER_SCH = (
    r"(<!--[\t ]*__RM_VERSION__[\t ]*-->)"
    r"(.*?)"
    r"(<!--[\t ]*__RM_VERSION__[\t ]*-->)"
)
S_RM_VER_REP = r"\g<1>\n{}\n\g<3>"

S_RM_DEPS_SCH = (
    r"(<!--[\t ]*__RM_DEPS__[\t ]*-->)"
    r"(.*?)"
    r"(<!--[\t ]*__RM_DEPS__[\t ]*-->)"
)
S_RM_DEPS_REP = r"\g<1>\n{}\g<3>"

# fix desktop
S_DESK_CAT_SCH = (
    r"(^\s*\[Desktop Entry\]\s*$)"
    r"(.*?)"
    r"(^\s*Categories[\t ]*=)"
    r"(.*?$)"
)
S_DESK_CAT_REP = r"\g<1>\g<2>\g<3>{}"

S_DESK_DESC_SCH = r"(^\s*\[Desktop Entry\]\s*$)(.*?)(^\s*Comment[\t ]*=)(.*?$)"
S_DESK_DESC_REP = r"\g<1>\g<2>\g<3>{}"

# fix gtk
S_GTK_DESC_SCH = (
    r"(<object class=\"GtkAboutDialog\".*?)"
    r"(<property name=\"comments\".*?\>)"
    r"(.*?)"
    r"(</property>)"
)
S_GTK_DESC_REP = r"\g<1>\g<2>{}\g<4>"

S_GTK_VER_SCH = (
    r"(<object class=\"GtkAboutDialog\".*?)"
    r"(<property name=\"version\">)"
    r"(.*?)"
    r"(</property>.*)"
)
S_GTK_VER_REP = r"\g<1>\g<2>{}\g<4>"

# pyproject.toml
S_TOML_VERSION_SEARCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*version[\t ]*=[\t ]*)(.*?$)"
)
S_TOML_VERSION_REPL = r'\g<1>\g<2>\g<3>"{}"'

S_TOML_SHORT_DESC_SEARCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*description[\t ]*=[\t ]*)(.*?$)"
)
S_TOML_SHORT_DESC_REPL = r'\g<1>\g<2>\g<3>"{}"'

S_TOML_KW_SEARCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*keywords[\t ]*=[\t ]*)(.*?\])"
)
S_TOML_KW_REPL = r"\g<1>\g<2>\g<3>[{}]"

# desc/version in all files
S_META_VER_SCH = r"(\s*S_PP_VERSION\s*=\s*)(.*)"
S_META_VER_REP = r'\g<1>"{}"'

S_META_DESC_SCH = r"(\s*S_PP_SHORT_DESC\s*=)(.*?\")([^\"]*)(.*)"
S_META_DESC_REP = r"\g<1>\g<2>{}\g<4>"

# make sure ver num entered in pybaker is valid
S_SEMVER_VALID = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(.*)$"

# ------------------------------------------------------------------------------
# gui stuff

# ui files/names
S_DLG_UI_FILE = "dialogs"
S_DLG_ABOUT = "dlg_about"

# NB: format param is __PP_NAME_PRJ_SMALL__
S_APP_FILE_FMT = "{}_app"
# NB: format param is __PP_NAME_SEC_SMALL__
S_WIN_FILE_FMT = "{}_win"

# NB: format param is _PP_NAME_PRJ_PASCAL__
S_APP_CLASS_FMT = "{}App"
# NB: format param is _PP_NAME_SEC_PASCAL__
S_WIN_CLASS_FMT = "{}Win"

# NB: format params are _dict_prv_all["__PP_AUTHOR__"] and __PP_NAME_PRJ_SMALL__
S_APP_ID_FMT = "org.{}.{}"

# ------------------------------------------------------------------------------
# Lists
# ------------------------------------------------------------------------------

# the types of projects this script can create
# val[0] is the char to enter for project type
# val[1] is the display name for project type
# val[2] is the template subdir to use for project type
L_TYPES = [
    [
        "c",
        "CLI",
        "cli",
    ],
    [
        "g",
        "GUI",
        "gui",
    ],
    [
        "p",
        "PKG",
        "pkg",
    ],
]

# list of file types to use md/html/xml fixer
L_EXT_MARKUP = [
    ".md",
    ".html",
    ".xml",
    ".ui",
    ".glade",
]

# file exts for pybaker
L_EXT_DESKTOP = [".desktop"]
L_EXT_GTK = [".ui", ".glade"]

# files to remove after the project is done
L_PURGE_FILES = [
    "ABOUT",
]

# dirs to remove after the project is done
L_PURGE_DIRS = {
    "p": [
        S_DIR_BIN,
        S_DIR_CONF,
        S_DIR_INSTALL,
        S_DIR_UNINSTALL,
    ]
}

# get list of approved categories
# https://specifications.freedesktop.org/menu-spec/latest/apa.html
L_CATS = [
    "AudioVideo",
    "Audio",
    "Video",
    "Development",
    "Education",
    "Game",
    "Graphics",
    "Network",
    "Office",
    "Science",
    "Settings",
    "System",
    "Utility",
    "Building",
    "Debugger",
    "IDE",
    "GUIDesigner",
    "Profiling",
    "RevisionControl",
    "Translation",
    "Calendar",
    "ContactManagement",
    "Database",
    "Dictionary",
    "Chart",
    "Email",
    "Finance",
    "FlowChart",
    "PDA",
    "ProjectManagement",
    "Presentation",
    "Spreadsheet",
    "WordProcessor",
    "2DGraphics",
    "VectorGraphics",
    "RasterGraphics",
    "3DGraphics",
    "Scanning",
    "OCR",
    "Photography",
    "Publishing",
    "Viewer",
    "TextTools",
    "DesktopSettings",
    "HardwareSettings",
    "Printing",
    "PackageManager",
    "Dialup",
    "InstantMessaging",
    "Chat",
    "IRCClient",
    "Feed",
    "FileTransfer",
    "HamRadio",
    "News",
    "P2P",
    "RemoteAccess",
    "Telephony",
    "TelephonyTools",
    "VideoConference",
    "WebBrowser",
    "WebDevelopment",
    "Midi",
    "Mixer",
    "Sequencer",
    "Tuner",
    "TV",
    "AudioVideoEditing",
    "Player",
    "Recorder",
    "DiscBurning",
    "ActionGame",
    "AdventureGame",
    "ArcadeGame",
    "BoardGame",
    "BlocksGame",
    "CardGame",
    "KidsGame",
    "LogicGame",
    "RolePlaying",
    "Shooter",
    "Simulation",
    "SportsGame",
    "StrategyGame",
    "Art",
    "Construction",
    "Music",
    "Languages",
    "ArtificialIntelligence",
    "Astronomy",
    "Biology",
    "Chemistry",
    "ComputerScience",
    "DataVisualization",
    "Economy",
    "Electricity",
    "Geography",
    "Geology",
    "Geoscience",
    "History",
    "Humanities",
    "ImageProcessing",
    "Literature",
    "Maps",
    "Math",
    "NumericalAnalysis",
    "MedicalSoftware",
    "Physics",
    "Robotics",
    "Spirituality",
    "Sports",
    "ParallelComputing",
    "Amusement",
    "Archiving",
    "Compression",
    "Electronics",
    "Emulator",
    "Engineering",
    "FileTools",
    "FileManager",
    "TerminalEmulator",
    "Filesystem",
    "Monitor",
    "Security",
    "Accessibility",
    "Calculator",
    "Clock",
    "TextEditor",
    "Documentation",
    "Adult",
    "Core",
    "KDE",
    "GNOME",
    "XFCE",
    "DDE",
    "GTK",
    "Qt",
    "Motif",
    "Java",
    "ConsoleOnly",
    "Screensaver",
    "TrayIcon",
    "Applet",
    "Shell",
]

# which prj types need an install.json?
L_APP_INSTALL = [
    "c",
    "g",
]

# install pkg in venv after making
L_PKG_INSTALL = ["p"]

# ------------------------------------------------------------------------------
# Dictionaries
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Private dictionaries
# ------------------------------------------------------------------------------

# these are the settings that should be set before you run pymaker.py
# consider them the "all projects" settings
# they are used for all projects, and should not be changed after a project is
# created, as pybaker.py will not update them

# if you need to adjust any of these values in a function, use do_before_fix()
# in this file

D_PRV_ALL = {
    # the author name, used in headers and pyproject.toml
    "__PP_AUTHOR__": "cyclopticnerve",
    # the base url for all projects, used in pyproject.toml and GUI about dlg
    "__PP_URL__": "https://github.com/cyclopticnerve",
    # the author's email, used in headers and pyproject.toml
    "__PP_EMAIL__": "cyclopticnerve@gmail.com",
    # the license name, used in headers and pyproject.toml
    "__PP_LICENSE_NAME__": "WTFPLv2",
    # the license url, used in gui about dialog
    "__PP_LICENSE_URL__": "http://www.wtfpl.net",
    # the license image/link to use in __PP_README_FILE__
    "__PP_RM_LICENSE__": (
        "[!"  # open image tag
        "[License: WTFPLv2]"  # alt text
        "(https://img.shields.io/badge/License-WTFPL-brightgreen.svg)"  # img src
        "]"  # close image tag
        "(http://www.wtfpl.net)"  # click url
    ),
    # dummy value to use in headers
    "__PP_DUMMY__": "",
    # version format string for command line
    # NB: format param is __PP_VERSION__ from metadata
    "__PP_VER_FMT__": S_VER_FMT,
    # NB: the struggle here is that using the fixed format results in a
    # four-digit year, but using the locale format ('%x') results in a
    # two-digit year (at least for my locale, which in 'en_US'). so what to do?
    # what i really want is a locale format that uses four-digit years
    # everywhere. so i am faced with a 'cake and eat it too' situation. not
    # sure how to proceed but i think for now i will leave this as a
    # user-editable string and place it in the realm of 'edit it before you
    # run' along with author/email/license/etc
    "__PP_DATE_FMT__": S_DATE_FMT,
    # file names replaced in various places, rel to prj dir
    "__PP_LICENSE_FILE__": S_FILE_LICENSE,
    "__PP_README_FILE__": S_FILE_README,
    "__PP_TOML_FILE__": S_FILE_TOML,
    "__PP_REQS_FILE__": S_FILE_REQS,
    "__PP_DIR_LIB__": S_DIR_LIB,
    "__PP_INST_ASSETS__": S_DIR_ASSETS,
    "__PP_DIR_INSTALL__": S_DIR_INSTALL,
    "__PP_LOGO_FILE__": f"{S_DIR_DOCS_TPLT}/{S_FILE_LOGO}",
    "__PP_INST_CONF_FILE__": f"{S_DIR_INSTALL}/{S_FILE_INST_CFG}",
    "__PP_UNINST_CONF_FILE__": f"{S_DIR_UNINSTALL}/{S_FILE_UNINST_CFG}",
    # --------------------------------------------------------------------------
    # these paths are relative to the dev's prj name
    # i.e. /home/dev/Documents/Projects/Python/MyProject
    "__PP_DIR_SRC__": S_DIR_SRC,
    "__PP_PATH_LOCALE__": S_PATH_LOCALE,
    "__PP_PATH_MO__": S_PATH_MO,
    # --------------------------------------------------------------------------
    # these paths are relative to the user's home dir
    "__PP_NAME_DSK_TMP__": S_NAME_DSK_TMP,
    "__PP_USR_APPS__": S_USR_APPS,  # for .desktop file
    "__PP_USR_BIN__": S_USR_BIN,  # where to put the binary
    # --------------------------------------------------------------------------
    # gui stuff
    "__PP_DIR_GUI__": f"{S_DIR_SRC}/{S_DIR_GUI}",
    "__PP_DIR_UI__": f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_UI}",
    "__PP_DLG_FILE__": S_DLG_UI_FILE,
    "__PP_DLG_ABOUT__": S_DLG_ABOUT,
}

# these are settings that will be calculated for you while running pymaker.py
# consider them the "each project" settings
# they are used for an individual project, and should not be changed after a
# project is created, as pybaker.py will not update them
D_PRV_PRJ = {
    "__PP_TYPE_PRJ__": "",  # 'c'
    "__PP_NAME_PRJ__": "",  # My Project
    "__PP_NAME_PRJ_BIG__": "",  # My_Project
    "__PP_NAME_PRJ_SMALL__": "",  # my_project
    "__PP_NAME_PRJ_PASCAL__": "",  # MyProject
    "__PP_NAME_SEC_BIG__": "",  # My_Win
    "__PP_NAME_SEC_SMALL__": "",  # my_win
    "__PP_NAME_SEC_PASCAL__": "",  # MyWin
    "__PP_DATE__": "",  # the date each file was created, updated every time
    "__PP_NAME_VENV__": "",  # venv folder name

    "__PP_FILE_APP__": "",  # my_project_app
    "__PP_CLASS_APP__": "",  # MyProjectApp
    "__PP_FILE_WIN__": "",  # my_project_win
    "__PP_CLASS_WIN__": "",  # MyProjectWin

    # --------------------------------------------------------------------------
    # these paths are calculated at runtime relative to the dev's home dir
    "__PP_DEV_PP__": "",  # location of PyPlate src dir, rel to dev home
    # --------------------------------------------------------------------------
    # these paths are calculated in do_before_fix, relative to the user's home
    # dir
    "__PP_USR_CONF__": "",  # config dir
    "__PP_DIST_FMT__": "",  # format name of the dist ([name_small]_[version])
    "__PP_CMD_RUN__": "",
    # --------------------------------------------------------------------------
    # these strings are calculated in do_before_fix
    # NB: technically this should be metadata but we don't want dev editing,
    # only use metadata to recalculate these on every build
    "__PP_VER_DISP__": "",  # formatted version string, ie. "Version 0.0.1"
    "__PP_FILE_DESK__": "",  # final desk file, not template
    "__PP_PDOC_START__": "",  # start doc search at this folder
}

# ------------------------------------------------------------------------------
# Public dictionaries
# ------------------------------------------------------------------------------

# these are settings that will be changed before running pybaker.py
# consider them the "each build" settings
D_PUB_META = {
    # the version number to use in __PP_README_FILE__ and pyproject.toml
    "__PP_VERSION__": "0.0.0",
    # the short description to use in __PP_README_FILE__ and pyproject.toml
    "__PP_SHORT_DESC__": "Short description",
    # the keywords to use in pyproject.toml and github
    "__PP_KW_STR__": [],
    # the python dependencies to use in __PP_README_FILE__, pyproject.toml,
    # github, and install.py
    # key is dep name, val is link to dep (optional)
    "__PP_PY_DEPS__": {},
    # the system dependencies to use in __PP_README_FILE__, github.com, and
    # install.py
    # key is dep name, val is link to dep (optional)
    "__PP_SYS_DEPS__": {},
    # the categories to use in .desktop for gui apps (found in pybaker_conf.py)
    "__PP_GUI_CATS__": [],
}

# dict of files to put in dist folder (defaults, written by pymaker, edited by
# hand, read by pybaker)
# NB: key is src, rel to prj dir
# NB: val is dst, rel to dist dir
D_PUB_DIST = {
    "c": {
        # basic stuff (put in assets folder)
        S_DIR_BIN: S_DIR_ASSETS,
        S_DIR_SRC: S_DIR_ASSETS,
        S_FILE_LICENSE: S_DIR_ASSETS,
        S_FILE_README: S_DIR_ASSETS,
        # extended stuff (put in assets folder)
        S_DIR_CONF: S_DIR_ASSETS,
        S_PATH_LOCALE: f"{S_DIR_ASSETS}/{S_DIR_I18N}",
        f"{S_DIR_INSTALL}/{S_FILE_INST_PY}": "",  # install.py at top level
        # install.json in assets/install folder
        "__PP_INST_CONF_FILE__": f"{S_DIR_ASSETS}/{S_DIR_INSTALL}",
        S_DIR_UNINSTALL: S_DIR_ASSETS,
        # requirements.txt in assets/install folder
        S_FILE_REQS: f"{S_DIR_ASSETS}/{S_DIR_INSTALL}",
    },
    "g": {
        # basic stuff (put in assets folder)
        S_DIR_BIN: S_DIR_ASSETS,
        S_DIR_SRC: S_DIR_ASSETS,
        S_FILE_LICENSE: S_DIR_ASSETS,
        S_FILE_README: S_DIR_ASSETS,
        # extended stuff (put in assets folder)
        S_DIR_CONF: S_DIR_ASSETS,
        S_PATH_LOCALE: f"{S_DIR_ASSETS}/{S_DIR_I18N}",
        f"{S_DIR_INSTALL}/{S_FILE_INST_PY}": "",  # install.py at top level
        # install.json in assets/install folder
        "__PP_INST_CONF_FILE__": f"{S_DIR_ASSETS}/{S_DIR_INSTALL}",
        S_DIR_UNINSTALL: S_DIR_ASSETS,
        # requirements.txt in assets/install folder
        S_FILE_REQS: f"{S_DIR_ASSETS}/{S_DIR_INSTALL}",
        # extended readme folder (screenshots, etc.)
        S_DIR_README: S_DIR_ASSETS,
    },
    "p": {
        # basic stuff (put at top level)
        S_DIR_SRC: "",
        S_FILE_LICENSE: "",
        S_FILE_README: "",
        S_DIR_DOCS: "",
        S_FILE_TOML: "",
    },
}

# the lists of dirs/files we don't mess with while running pymaker
# each item can be a full path, a path relative to the project directory, or a
# glob
# see https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
# NB: you can use dunders here since the path is the last thing to get fixed
# these dir/file names should match what's in the template dir (before any
# modifications, hence using dunder keys)
D_PUB_BL = {
    # skip header, skip text, skip path (0 0 0)
    # NB: this is mostly to speed up processing by not even looking at them
    S_KEY_SKIP_ALL: [
        ".git",
        "**/.venv*",
        ".VSCodeCounter",
        # NB: dist will have install.py in it, needs dunders
        S_DIR_DIST,
        S_DIR_DOCS,
        S_DIR_I18N,
        S_DIR_LIB,
        S_DIR_MISC,
        # S_DIR_README,
        S_FILE_LICENSE,
        S_FILE_REQS,
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
        "**/.venv*",
        ".VSCodeCounter",
        "**/__pycache__",
    ],
}

# I18N stuff to be used in pybaker
D_PUB_I18N = {
    # default charset for .pot/.po files
    S_KEY_CHARSET: S_ENCODING,
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
            "__PP_NAME_PRJ_SMALL__",
        ],
    },
    # list of written languages that are available
    S_KEY_WLANGS: ["en"],
}

# dict in project to control post processing
D_PUB_DBG = {
    S_KEY_DBG_GIT: True,
    S_KEY_DBG_VENV: True,
    S_KEY_DBG_I18N: True,
    S_KEY_DBG_DOCS: True,
    S_KEY_DBG_INST: True,
    S_KEY_DBG_TREE: True,
}

# ------------------------------------------------------------------------------
# Other dictionaries
# ------------------------------------------------------------------------------

# dict of files that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project, it gets copied
# to the project, and cuts down on duplicate files
# key is the relative path to the source file in PyPlate
# val is the relative path to the dest file in the project dir
D_COPY = {
    f"{S_DIR_MISC}/default_files": f"{S_DIR_MISC}/default_files",
    f"{S_DIR_MISC}/how_to": f"{S_DIR_MISC}/how_to",
}

# which libs to add to which type of project
# key is prj short type
# val is list of libs to add to prj type
D_COPY_LIB = {
    "c": ["cnlib"],
    "g": ["cnlib"],  # "cnguilib"],
}

# dictionary of default stuff to put in install.json
# NB: key is rel to prj, val is rel to home
# these are the defaults, they can be edited in prj/install/install.json before
# running pybaker
D_INSTALL = {
    "c": {
        S_DIR_CONF: "__PP_USR_INST__",
        S_DIR_LIB: "__PP_USR_INST__",
        S_DIR_README: "__PP_USR_INST__",
        S_DIR_SRC: "__PP_USR_INST__",
        S_DIR_I18N: "__PP_USR_INST__",
        S_FILE_LICENSE: "__PP_USR_INST__",
        S_FILE_README: "__PP_USR_INST__",
        S_DIR_UNINSTALL: "__PP_USR_INST__",
        f"{S_DIR_BIN}/__PP_NAME_PRJ_SMALL__": "__PP_USR_BIN__",
    },
    "g": {
        S_DIR_CONF: "__PP_USR_INST__",
        S_DIR_LIB: "__PP_USR_INST__",
        S_DIR_README: "__PP_USR_INST__",
        S_DIR_SRC: "__PP_USR_INST__",
        S_DIR_I18N: "__PP_USR_INST__",
        S_FILE_LICENSE: "__PP_USR_INST__",
        S_FILE_README: "__PP_USR_INST__",
        S_DIR_UNINSTALL: "__PP_USR_INST__",
        f"{S_DIR_BIN}/__PP_NAME_PRJ_SMALL__": "__PP_USR_BIN__",
        #
        S_DIR_GUI: "__PP_USR_INST__",
        "__PP_FILE_DESK__": S_USR_APPS,
    },
}

# dict to remove when uninstalling
D_UNINSTALL = {
    "c": [
        "__PP_USR_INST__",
        "__PP_USR_BIN__/__PP_NAME_PRJ_SMALL__",
    ],
    "g": [
        "__PP_USR_INST__",
        "__PP_USR_BIN__/__PP_NAME_PRJ_SMALL__",
        #
        f"{S_USR_APPS}/__PP_FILE_DESK__",
    ],
}

# the info for matching/fixing lines in markup files
D_MARKUP_REP = {
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
    S_KEY_SPLIT_INDEX: 4,
}

# the info for matching/fixing lines in non-markup files
D_PY_REP = {
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
    S_KEY_SPLIT_INDEX: 4,
}

# the type of projects that will ask for a second name
D_NAME_SEC = {
    # "p": [S_ASK_SEC_P, S_ASK_SEC_P_DEF],
    # "g": [S_ASK_SEC_G, S_ASK_SEC_G_DEF],
    "p": S_ASK_SEC_P,
    "g": S_ASK_SEC_G,
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
    S_KEY_NAME_MID: r"(^[a-zA-Z\d\-_ ]*$)",
}

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Do any work before fix
# ------------------------------------------------------------------------------
def do_before_fix(_dir_prj, dict_prv, dict_pub):
    """
    Do any work before fix

    Args:
        dir_prj: The root of the new project (reserved for future use)
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data

    Returns:
        The modified dicts to be synced with the caller

    Do any work before fix. This method is called at the beginning of _do_fix,
    after all dunders have been configured, but before any files have been
    modified.\n
    It is mostly used to make final adjustments to the 'D_PRV_PRJ' dunder dict
    before any replacement occurs.
    """

    # --------------------------------------------------------------------------
    # these paths are formatted here because they are complex and may be
    # changed by dev

    # get sub-dicts we need
    dict_prv_all = dict_prv[S_KEY_PRV_ALL]
    dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]
    dict_pub_meta = dict_pub[S_KEY_PUB_META]

    # get values after pymaker has set them
    name_prj_small = dict_prv_prj["__PP_NAME_PRJ_SMALL__"]

    # paths relative to the end user's (or dev's) useful folders
    usr_inst = f"{S_USR_SHARE}/{name_prj_small}"
    dict_prv_prj["__PP_USR_INST__"] = usr_inst

    # k/v to fix desktop
    dict_prv_prj["__PP_DESK_ICON__"] = (
        f"{usr_inst}/{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_DESKTOP}/{name_prj_small}.png"
    )
    name_big = dict_prv_prj["__PP_NAME_PRJ_BIG__"]
    dict_prv_prj["__PP_FILE_DESK__"] = (
        f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_DESKTOP}/{name_big}.desktop"
    )

    author = dict_prv_all["__PP_AUTHOR__"]
    dict_prv_prj["__PP_APP_ID__"] = S_APP_ID_FMT.format(author, name_prj_small)

    # formatted version string
    # NB: done in two steps to avoid linter errors
    version = dict_pub_meta["__PP_VERSION__"]
    ver_fmt = dict_prv_all["__PP_VER_FMT__"]
    ver_disp = ver_fmt.format(version)
    dict_prv_prj["__PP_VER_DISP__"] = ver_disp

    # replace all dots with dashes in ver
    version = version.replace(".", "-")

    # format dist dir name with prj and ver
    name_fmt = f"{name_prj_small}_{version}"
    dict_prv_prj["__PP_DIST_FMT__"] = name_fmt

    # gui app/win replacements
    name_prj_pascal = dict_prv_prj["__PP_NAME_PRJ_PASCAL__"]
    name_sec_small = dict_prv_prj["__PP_NAME_SEC_SMALL__"]
    name_sec_pascal = dict_prv_prj["__PP_NAME_SEC_PASCAL__"]
    dict_prv_prj["__PP_FILE_APP__"] = S_APP_FILE_FMT.format(name_prj_small)
    dict_prv_prj["__PP_CLASS_APP__"] = S_APP_CLASS_FMT.format(name_prj_pascal)
    dict_prv_prj["__PP_FILE_WIN__"] = S_WIN_FILE_FMT.format(name_sec_small)
    dict_prv_prj["__PP_CLASS_WIN__"] = S_WIN_CLASS_FMT.format(name_sec_pascal)

    # NB: ALWAYS RETURN DICTS!
    return (dict_prv, dict_pub)


# ------------------------------------------------------------------------------
# Do any work after fix
# ------------------------------------------------------------------------------
def do_after_fix(dir_prj, dict_prv, dict_pub):
    """
    Do any work after fix

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data

    Returns:
        The modified dicts to be synced with the caller

    Do any work after fix. This method is called at the end of the internal
    _do_after_fix, after all files have been modified.
    """

    # get sub-dicts we need
    dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]
    dict_pub_meta = dict_pub[S_KEY_PUB_META]

    # fix top level files
    a_file = dir_prj / D_PRV_ALL["__PP_LOGO_FILE__"]
    if a_file.exists():
        _fix_docs(a_file, dict_prv_prj, dict_pub_meta)

    a_file = dir_prj / D_PRV_ALL["__PP_README_FILE__"]
    if a_file.exists():
        _fix_readme(a_file, dict_prv_prj, dict_pub_meta)

    a_file = dir_prj / D_PRV_ALL["__PP_TOML_FILE__"]
    if a_file.exists():
        _fix_pyproject(a_file, dict_prv_prj, dict_pub_meta)

    # fix deep files
    for root, _root_dirs, root_files in dir_prj.walk():

        # get full path to file
        items = [root / f for f in root_files]

        # test each file
        for item in items:

            # fix ui files
            if item.suffix in L_EXT_GTK:
                _fix_ui(item, dict_prv_prj, dict_pub_meta)

            # fix ,desktop files
            if item.suffix in L_EXT_DESKTOP:
                _fix_desktop(item, dict_prv_prj, dict_pub_meta)


    # --------------------------------------------------------------------------
    # remove some extra stuff

    # first purge all dummy files
    for root, root_dirs, _root_files in dir_prj.walk():

        # convert files into Paths
        dirs = [root / f for f in root_dirs]

        # for each file item
        for item in dirs:

            # if it is in purge list, delete it
            if item.name in L_PURGE_DIRS:
                Path.unlink(item)


    # NB: ALWAYS RETURN DICTS!
    return (dict_prv, dict_pub)


# ------------------------------------------------------------------------------
# Do any work before making dist
# ------------------------------------------------------------------------------
def do_before_dist(_dir_prj, dict_prv, dict_pub):
    """
    Do any work before making dist

    Args:
        dir_prj: The root of the new project (reserved for future use)
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data

    Returns:
        The modified dicts to be synced with the caller

    Do any work on the dist folder before it is created.
    """

    # NB: ALWAYS RETURN DICTS!
    return (dict_prv, dict_pub)


# ------------------------------------------------------------------------------
# Do any work after making dist
# ------------------------------------------------------------------------------
def do_after_dist(dir_prj, dict_prv, dict_pub):
    """
    Do any work after making dist

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data (reserved for
        future use)

    Returns:
        The modified dicts to be synced with the caller

    Do any work on the dist folder after it is created. Currently, this method
    purges any "ABOUT" file used as placeholders for github syncing. It also
    tars the source folder if it is a package, making for one (or two) less
    steps in the user's install process.
    """

    # get dist dir for all operations
    dist = Path(dir_prj) / S_DIR_DIST
    name_fmt = dict_prv[S_KEY_PRV_PRJ]["__PP_DIST_FMT__"]
    p_dist = dist / name_fmt

    # --------------------------------------------------------------------------
    # remove all "ABOUT" files

    # first purge all dummy files
    for root, _root_dirs, root_files in p_dist.walk():

        # convert files into Paths
        files = [root / f for f in root_files]

        # for each file item
        for item in files:

            # if it is in purge list, delete it
            if item.name in L_PURGE_FILES:
                Path.unlink(item)

    # --------------------------------------------------------------------------
    # check for compression in dist

    ext = ".tar.gz"

    # get prj type
    name_small = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_PRJ_SMALL__"]

    # remove ext from bin file
    old_bin = p_dist / S_DIR_ASSETS / S_DIR_BIN / f"{name_small}.py"
    new_bin = p_dist / S_DIR_ASSETS / S_DIR_BIN / f"{name_small}"
    if old_bin.exists():
        old_bin.rename(new_bin)

    # now do normal dist tar
    in_dir = p_dist
    out_file = Path(S_DIR_DIST) / f"{in_dir}{ext}"

    with tarfile.open(out_file, mode="w:gz") as tar:
        tar.add(in_dir, arcname=Path(in_dir).name)

    # FIXME: REMOVE BEFORE FLIGHT
    # delete the origin dir
    # if not B_DEBUG:
    #     shutil.rmtree(in_dir)

    # NB: ALWAYS RETURN DICTS!
    return (dict_prv, dict_pub)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Remove/replace parts of the docs logo.mako file
# ------------------------------------------------------------------------------
def _fix_docs(path, dict_prv_prj, _dict_pub_meta):
    """
    Remove/replace parts of the docs logo file

    Args:
        path: Path for the logo.mako file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file (reserved for
        future use)

    Fixes metadata in the docs logo.mako file to adjust version number and logo
    image.
    """

    # the whole text of the file
    text = ""

    # open and read whole file
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = S_RM_VER_SCH
    pp_ver_disp = dict_prv_prj["__PP_VER_DISP__"]
    str_rep = S_RM_VER_REP.format(pp_ver_disp)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Remove/replace parts of the main README file
# ------------------------------------------------------------------------------
def _fix_readme(path, dict_prv_prj, dict_pub_meta):
    """
    Remove/replace parts of the main README file

    Args:
        path: Path for the README to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Removes parts of the file not applicable to the current project type. Also
    fixes metadata in the file when dict_meta is present.
    """

    # the whole text of the file
    text = ""

    # open and read whole file
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # --------------------------------------------------------------------------
    # this part is used by pymaker to remove readme sections

    # find the remove blocks
    prj_type = dict_prv_prj["__PP_TYPE_PRJ__"]
    if prj_type == "c" or prj_type == "g":
        str_pattern = S_RM_PKG
    else:
        str_pattern = S_RM_APP

    # replace block with empty string (equiv to deleting it)
    # NB: need S flag to make dot match newline
    text = re.sub(str_pattern, "", text, flags=re.S)

    # --------------------------------------------------------------------------
    # this part is used by pybaker to replace metadata

    # replace short description
    str_pattern = S_RM_DESC_SCH
    pp_short_desc = dict_pub_meta["__PP_SHORT_DESC__"]
    str_rep = S_RM_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # replace version
    str_pattern = S_RM_VER_SCH
    pp_ver_disp = dict_prv_prj["__PP_VER_DISP__"]
    str_rep = S_RM_VER_REP.format(pp_ver_disp)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # get deps as links for readme
    d_py_deps = dict_pub_meta["__PP_PY_DEPS__"]
    l_rm_deps = [
        f"[{key}]({val})" if val != "" else key
        for key, val in d_py_deps.items()
    ]

    # get rm deps as links
    s_rm_deps = "<br>\n".join(l_rm_deps)
    if len(s_rm_deps) == 0:
        s_rm_deps = "None\n"

    # replace dependencies array
    str_pattern = S_RM_DEPS_SCH
    str_rep = S_RM_DEPS_REP.format(s_rm_deps)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# --------------------------------------------------------------------------
# Replace text in the pyproject file
# --------------------------------------------------------------------------
def _fix_pyproject(path, _dict_prv_prj, dict_pub_meta):
    """
    Replace text in the pyproject file

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict (reserved for future use)
        dict_pub_meta: the dict of metadata to replace in the file

    Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = S_TOML_VERSION_SEARCH
    pp_version = dict_pub_meta["__PP_VERSION__"]
    str_rep = S_TOML_VERSION_REPL.format(pp_version)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = S_TOML_SHORT_DESC_SEARCH
    pp_short_desc = dict_pub_meta["__PP_SHORT_DESC__"]
    str_rep = S_TOML_SHORT_DESC_REPL.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # fix keywords for pyproject.toml
    l_keywords = dict_pub_meta["__PP_KW_STR__"]
    q_keywords = [f'"{item}"' for item in l_keywords]
    s_keywords = ", ".join(q_keywords)

    # replace keywords array
    str_pattern = S_TOML_KW_SEARCH
    str_rep = S_TOML_KW_REPL.format(s_keywords)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the desktop file
# ------------------------------------------------------------------------------
def _fix_desktop(path, _dict_prv_prj, dict_pub_meta):
    """
    Replace text in the desktop file

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict (reserved for future use)
        dict_pub_meta: the dict of metadata to replace in the file

    Replaces the description (comment) and category text in a .desktop file for
    programs that use this.
    """

    # validate wanted categories into approved categories
    pp_gui_categories = []
    wanted_cats = dict_pub_meta["__PP_GUI_CATS__"]
    for cat in wanted_cats:
        # category is valid
        if cat in L_CATS:
            # add to final list
            pp_gui_categories.append(cat)
        else:
            # category is not valid, print error and increase error count
            print(S_ERR_DESK_CAT.format(cat))

    # convert list to string
    str_cat = ";".join(pp_gui_categories)
    # NB: must have trailing semicolon
    str_cat += ";"

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace categories
    str_pattern = S_DESK_CAT_SCH
    str_rep = S_DESK_CAT_REP.format(str_cat)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = S_DESK_DESC_SCH
    pp_short_desc = dict_pub_meta["__PP_SHORT_DESC__"]
    str_rep = S_DESK_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the UI files
# ------------------------------------------------------------------------------
def _fix_ui(path, _dict_prv_prj, dict_pub_meta):
    """
    Replace text in the UI files

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict (reserved for future use)
        dict_pub_meta: the dict of metadata to replace in the file

    Replace description and version number in the UI file.
    """

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace short description
    str_pattern = S_GTK_DESC_SCH
    pp_short_desc = dict_pub_meta["__PP_SHORT_DESC__"]
    str_rep = S_GTK_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace version
    str_pattern = S_GTK_VER_SCH
    pp_version = dict_pub_meta["__PP_VERSION__"]
    str_rep = S_GTK_VER_REP.format(pp_version)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# -)
