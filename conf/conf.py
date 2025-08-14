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

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from datetime import datetime
import gettext
import locale
from pathlib import Path
import re
import shutil
import sys
import tarfile

# local imports
from cnlib import cnfunctions as F  # type: ignore
from cnlib.cnpot import CNPotPy  # type: ignore
from cnlib.cntree import CNTree  # type: ignore
from cnlib.cnvenv import CNVenv  # type: ignore

# pylint: disable=no-name-in-module
from . import mkdocs
from . import pdoc

# ------------------------------------------------------------------------------
# local imports

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order

# fudge the path to import pyplate stuff
P_DIR_PRJ = Path(__file__).parents[1].resolve()
sys.path.append(str(P_DIR_PRJ))

import src.pyplate as PP

# pylint: enable=wrong-import-order
# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ABSOLUTE CURRENT PATH OF PyPlate
P_DIR_PP = Path(__file__).parents[1].resolve()
# NB: these dirs are "blessed". if you fuck with them, bad juju will happen.
# you have been warned.
P_DIR_PP_VENV = P_DIR_PP / ".venv-pyplate"

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py

# path to project dir
T_DIR_PRJ = Path(__file__).parents[1].resolve()

# init gettext
T_DOMAIN = "pyplate"
T_DIR_LOCALE = T_DIR_PRJ / "i18n/locale"
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

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

S_WLANG = "en"
# default encoding
S_ENCODING = "UTF-8"
# I18N: default date format
S_DATE_FMT = _("%m/%d/%Y")
# I18N: def deps
S_DEPS_NONE = _("None")
# default image ext
S_IMG_EXT = ".png"

# spice up version number
S_VER_DATE_FMT = "%Y%m%d"
# NB: format param is __PP_VER_MMR__
# I18N: printable version number
S_VER_DISP_FMT = _("Version {}")
# # NB: format params are __PP_NAME_PRJ_SMALL__ and __PP_VER_MMR__
S_VER_DIST_FMT = "{}-{}"

# ask questions
# I18N: ask prj name
S_ASK_NAME = _("Project name: ")
# NB: format params are L_TYPES[item][0] and L_TYPES[item][1]
S_ASK_TYPE_FMT = "{} ({})"
# join each project type in L_TYPES with this
S_ASK_TYPE_JOIN = " | "
# NB: format param is joined list of project types from L_TYPES
# I18N: ask prj type
S_ASK_TYPE = _("Project type [{}]: ")
# NB: format param is __PP_NAME_PRJ_SMALL__
# I18N: ask module name
S_ASK_SEC_P = _("Module name (default: {}): ")
# NB: format param is __PP_NAME_PRJ_SMALL__
# I18N: ask window class name
S_ASK_SEC_G = _("Window class name (default: {}): ")
# NB: format param is current working dir
# I18N: ask prj name if running pybaker in IDE
S_ASK_IDE = _("Project name: (relative to {}): ")

# error strings
# NB: format param is joined list of project types from L_TYPES
# I18N: Type must be one of {}
S_ERR_TYPE = _("Type must be one of {}")
# I18N: Project names must be more than 1 character
S_ERR_LEN = _("Name must be more than 1 character")
# I18N: Project names must start with a letter
S_ERR_START = _("Name must start with a letter")
# I18N: Project names must end with a letter or number
S_ERR_END = _("Name must end with a letter or number")
# I18N: name contains invalid char
S_ERR_MID = _(
    "Name must contain only letters, numbers, spaces, dashes (-), "
    "or underscores (_)"
)
# NB: format param is __PP_NAME_PRJ_BIG__
# I18N: project already exists
S_ERR_EXIST = _('Project "{}" already exists')
# NB: format param is full path to user entry (when pb run from ide)
# I18N: run pybaker on project that does not exist
S_ERR_NOT_EXIST = _('Project "{}" does not exist')
# I18N: run pybaker on non-pyplate project dir
S_ERR_NOT_PRJ = _(
    "This project does not have a 'pyplate' folder.\n"
    "Are you sure this is a PyPlate project?"
)
# I18N: pyplate/private/private.json or pyplate/project.json not found
S_ERR_PP_MISSING = _("One or more PyPlate data files are missing")
# I18N: pyplate/private/private.json or pyplate/project.json not valid
S_ERR_PP_INVALID = _("One or more PyPlate data files are corrupted")
# I18N: invalid version string format
S_ERR_SEM_VER = _(
    "Warning: version number does not match S_SEM_VER_VALID\n"
    "See https://semver.org/\nDo you wish to continue?"
)
# I18N: continue with bad sem ver
S_ERR_SEM_VER_Y = _("y")
# I18N: quit if bad sem ver (the default, should be capitalized)
S_ERR_SEM_VER_N = _("N")
# I18N: Cannot run pymaker in PyPlate dir
S_ERR_PRJ_DIR_IS_PP = _("Cannot run pymaker in PyPlate dir")
# NB: format params are S_FILE_DSK_TMP and __PP_FILE_DESK__
# I18N: we want i18n but the template desktop doesn't exist
S_ERR_DESK_NO_TEMP = _("Warning: file '{}' does not exist, using '{}'")
# NB: format param is item in L_CATS
# I18N: invalid desktop category
S_ERR_DESK_CAT = _(
    '"{}" is not a valid desktop category, see '
    '"https://specifications.freedesktop.org/menu-spec/latest/apa.html"'
)
# NB: format param is S_PATH_SCREENSHOT
# I18N: alternate text for screenshot in README.md
S_ERR_NO_SCREENSHOT = _("Create the file {}")

# debug-specific strings
# I18N: warn if running in debug mode
S_MSG_DEBUG = _(
    "WARNING! YOU ARE IN DEBUG MODE!\nIT IS POSSIBLE TO \
OVERWRITE EXISTING PROJECTS!\n"
)

# error installing reqs
# I18N: need internet connection to install requirements
S_MSG_NO_INTERNET = _("Make sure you are connected to the internet")

# ------------------------------------------------------------------------------
# output msg for steps

# I18N: Copy template files
S_ACTION_COPY = _("Copy template files... ")
# I18N fix readme
S_ACTION_README = _("Fixing README... ")
# I18N: fix other files
S_ACTION_META = _("Fixing metadata... ")
# I18N: fix other files
S_ACTION_PO = _("Fixing po files... ")
# I18N: Do before fix
S_ACTION_BEFORE = _("Do before fix... ")
# I18N: Do fix
S_ACTION_FIX = _("Do fix... ")
# I18N: Do after fix
S_ACTION_AFTER = _("Do after fix... ")
# I18N: Make git folder
S_ACTION_GIT = _("Make git folder... ")
# I18N: Make venv folder
S_ACTION_VENV = _("Make venv folder... ")
# I18N: freeze venv folder
S_ACTION_FREEZE = _("Freezing venv... ")
# I18N: Install libs in venv
S_ACTION_LIB = _("Install libs in venv... ")
# I18N: Make i18n folder
S_ACTION_I18N = _("Make i18n folder... ")
# I18N: Make docs folder
S_ACTION_MAKE_DOCS = _("Make docs folder... ")
# I18N: Deploy docs folder
S_ACTION_BAKE_DOCS = _("Bake docs folder... ")
# I18N: Make tree file
S_ACTION_TREE = _("Make tree file... ")
# I18N: Install package in venv
S_ACTION_INST_PKG = _("Install package in venv... ")
# I18N: Make dist folder
S_ACTION_DIST = _("Copy dist files... ")
# I18N: Make install file
S_ACTION_INST = _("Make install/uninstall files... ")
# I18N: purge non-essential files
S_ACTION_PURGE = _("Purge non-essential files... ")
# I18N: compress files
S_ACTION_COMPRESS = _("Compress files... ")
# I18N: remove dist
S_ACTION_REM_DIST = _("Remove dist source... ")
# I18N: Done
S_ACTION_DONE = _("Done")
# I18N: Failed
S_ACTION_FAIL = _("Failed")

# ------------------------------------------------------------------------------

# keys for pybaker private dict
S_KEY_PRV_ALL = "PRV_ALL"
S_KEY_PRV_PRJ = "PRV_PRJ"

# keys for metadata, blacklist, i18n in pybaker dev dict
S_KEY_PUB_BL = "PUB_BL"
S_KEY_PUB_DBG = "PUB_DBG"
S_KEY_PUB_DIST = "PUB_DIST"
S_KEY_PUB_DOCS = "PUB_DOCS"
S_KEY_PUB_I18N = "PUB_I18N"
S_KEY_PUB_META = "PUB_META"
S_KEY_PUB_INST = "PUB_INST"
S_KEY_PUB_UNINST = "PUB_UNINST"

# keys for blacklist
S_KEY_SKIP_ALL = "SKIP_ALL"
S_KEY_SKIP_CONTENTS = "SKIP_CONTENTS"
S_KEY_SKIP_HEADER = "SKIP_HEADER"
S_KEY_SKIP_CODE = "SKIP_CODE"
S_KEY_SKIP_PATH = "SKIP_PATH"
S_KEY_SKIP_TREE = "SKIP_TREE"

# keys for i18n
S_KEY_PUB_I18N_DOM = "DOMAIN"
S_KEY_PUB_I18N_SRC = "SOURCES"
S_KEY_PUB_I18N_CLANGS = "CLANGS"
S_KEY_PUB_I18N_NO_EXT = "NO_EXT"
S_KEY_PUB_I18N_WLANGS = "WLANGS"
S_KEY_PUB_I18N_CHAR = "CHARSET"

# keys for D_PUB_DBG
S_KEY_DBG_GIT = "DBG_GIT"
S_KEY_DBG_VENV = "DBG_VENV"
S_KEY_DBG_I18N = "DBG_I18N"
S_KEY_DBG_DOCS = "DBG_DOCS"
S_KEY_DBG_INST = "DBG_INST"
S_KEY_DBG_TREE = "DBG_TREE"
S_KEY_DBG_DIST = "DBG_DIST"

# keys for D_PUB_DOCS
S_KEY_DOCS_TOOL = "DOCS_TOOL"
S_KEY_DOCS_THEME = "DOCS_THEME"
S_KEY_DOCS_USE_RM = "DOCS_USE_RM"
S_KEY_DOCS_MAKE_API = "DOCS_MAKE_API"

# keys for meta dict
S_KEY_META_SHORT_DESC = "META_SHORT_DESC"
S_KEY_META_VERSION = "META_VERSION"
S_KEY_META_KEYWORDS = "META_KEYWORDS"
S_KEY_META_DEPS = "META_DEPS"
S_KEY_META_CATS = "META_CATS"

# python header/split dict keys
S_KEY_RULES_HASH = "S_KEY_RULES_HASH"
S_KEY_RULES_MUD = "S_KEY_RULES_MUD"
S_KEY_RULES_EXT = "S_KEY_RULES_EXT"
S_KEY_RULES_REP = "S_KEY_RULES_REP"
S_KEY_HDR_SCH = "S_KEY_HDR_SCH"
S_KEY_LEAD = "S_KEY_GRP_LEAD"
S_KEY_VAL = "S_KEY_GRP_VAL"
S_KEY_PAD = "S_KEY_GRP_PAD"
S_KEY_SW_SCH = "S_KEY_SW_SCH"
S_KEY_SW_PRE = "S_KEY_SW_PRE"
S_KEY_SW_KEY = "S_KEY_SW_KEY"
S_KEY_SW_VAL = "S_KEY_SW_VAL"
S_KEY_SPLIT = "S_KEY_SPLIT"
S_KEY_SPLIT_COMM = "S_KEY_SPLIT_COMM"

# constants for _check_name()
S_KEY_NAME_START = "S_KEY_NAME_START"
S_KEY_NAME_END = "S_KEY_NAME_END"
S_KEY_NAME_MID = "S_KEY_NAME_MID"

# keys for install/uninstall
S_KEY_INST_NAME = "INST_NAME"
S_KEY_INST_VER = "INST_VER"
S_KEY_INST_DESK = "INST_DESK"
S_KEY_INST_CONT = "INST_CONT"

# dir names, relative to PP template, or project dir
# NB: if you change anything in the template structure, you should revisit this
# and make any appropriate changes
S_DIR_TEMPLATE = "template"
S_DIR_ALL = "all"
S_DIR_BIN = "bin"
S_DIR_GIT = ".git"
S_DIR_CONF = "conf"
# NB: if you change this, it will bork mkdocs!
S_DIR_DOCS = "docs"
S_DIR_MISC = "misc"
S_DIR_README = "readme"
S_DIR_SRC = "src"
S_DIR_SUPPORT = "support"
S_DIR_TODO = "todo"
S_DIR_UI = "ui"
S_DIR_I18N = "i18n"
S_DIR_IMAGES = "img"
S_DIR_LOCALE = "locale"
S_DIR_POT = "pot"
S_DIR_PO = "po"
S_DIR_TESTS = "tests"
S_DIR_SCRATCH = "scratch"
S_DIR_GUI = "gui"
S_DIR_DESKTOP = "desktop"
S_DIR_DIST = "dist"
S_DIR_ASSETS = "assets"
S_DIR_INSTALL = "install"

# common file names, rel to prj dir or pyplate dir
S_FILE_LICENSE = "LICENSE.txt"
S_FILE_README = "README.md"
S_FILE_TOML = "pyproject.toml"
S_FILE_REQS = "requirements.txt"
S_FILE_INST_CFG = "install.json"
S_FILE_UNINST_CFG = "uninstall.json"
S_FILE_INST_PY = "install.py"
S_FILE_UNINST_PY = "uninstall.py"
S_FILE_SCREENSHOT = "screenshot.png"

# concatenate some paths for install/uninstall
S_PATH_INST_CFG = f"{S_DIR_INSTALL}/{S_FILE_INST_CFG}"
S_PATH_UNINST_CFG = f"{S_DIR_INSTALL}/{S_FILE_UNINST_CFG}"

# screenshot path for readme
S_PATH_SCREENSHOT = f"{S_DIR_IMAGES}/{S_FILE_SCREENSHOT}"

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
P_DIR_I18N = Path(S_DIR_I18N)
S_PATH_LOCALE = str(P_DIR_I18N / S_DIR_LOCALE)
S_PATH_PO = str(P_DIR_I18N / S_DIR_PO)
S_PATH_POT = str(P_DIR_I18N / S_DIR_POT)
S_I18N_TAG = "I18N"

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
# commands for do_after_fix

# cmd for git
# NB: format param is proj dir
S_CMD_GIT_CREATE = "git init {} -q"
# NB: format params are prj dir and venv name
S_CMD_VENV_ACTIVATE = "cd {};. {}/bin/activate"

# ------------------------------------------------------------------------------
# regex stuff

# fix readme
S_RM_PKG = r"<!--[\t ]*__RM_PKG__[\t ]*-->(.*?)<!--[\t ]*__RM_PKG__[\t ]*-->"
S_RM_APP = r"<!--[\t ]*__RM_APP__[\t ]*-->(.*?)<!--[\t ]*__RM_APP__[\t ]*-->"
S_RM_VER_SCH = (
    r"(<!--[\t ]*__RM_VERSION__[\t ]*-->)"
    r"(.*?)"
    r"(<!--[\t ]*__RM_VERSION__[\t ]*-->)"
)
S_RM_VER_REP = r"\g<1>\n{}\n\g<3>"
S_RM_DESC_SCH = (
    r"(<!--[\t ]*__RM_SHORT_DESC__[\t ]*-->)"
    r"(.*?)"
    r"(<!--[\t ]*__RM_SHORT_DESC__[\t ]*-->)"
)
S_RM_DESC_REP = r"\g<1>\n{}\n\g<3>"
S_RM_SS_SCH = (
    r"(<!--[\t ]*__RM_SCREENSHOT__[\t ]*-->)"
    r"(.*?)"
    r"(<!--[\t ]*__RM_SCREENSHOT__[\t ]*-->)"
)
S_RM_SS_REP = r"\g<1>\n{}\n\g<3>"
S_RM_DEPS_SCH = (
    r"(<!--[\t ]*__RM_DEPS__[\t ]*-->)"
    r"(.*?)"
    r"(<!--[\t ]*__RM_DEPS__[\t ]*-->)"
)
S_RM_DEPS_REP = r"\g<1>\n{}\n\g<3>"

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
S_UI_DESC_SCH = (
    r"(<object class=\"GtkAboutDialog\".*?)"
    r"(<property name=\"comments\".*?\>)"
    r"(.*?)"
    r"(</property>)"
)
S_UI_DESC_REP = r"\g<1>\g<2>{}\g<4>"
S_UI_VER_SCH = (
    r"(<object class=\"GtkAboutDialog\".*?)"
    r"(<property name=\"version\">)"
    r"(.*?)"
    r"(</property>.*)"
)
S_UI_VER_REP = r"\g<1>\g<2>{}\g<4>"

# po files
S_PO_VER_SCH = r"(\"Project-Id-Version: )(.*?)(\\n\")"
S_PO_VER_REP = r"\g<1>{}\g<3>"

# pyproject.toml
S_TOML_VER_SCH = r"(^\s*\[project\]\s*$)(.*?)(^\s*version[\t ]*=[\t ]*)(.*?$)"
S_TOML_VER_REP = r'\g<1>\g<2>\g<3>"{}"'
S_TOML_DESC_SCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*description[\t ]*=[\t ]*)(.*?$)"
)
S_TOML_DESC_REP = r'\g<1>\g<2>\g<3>"{}"'
S_TOML_KW_SCH = r"(^\s*\[project\]\s*$)(.*?)(^\s*keywords[\t ]*=[\t ]*)(.*?\])"
S_TOML_KW_REP = r"\g<1>\g<2>\g<3>[{}]"

# desc/version in all files
S_SRC_DESC_SCH = r"(^\s*S_PP_SHORT_DESC\s*=\s*)(_\()*(.*?)(\n|\))"
S_SRC_DESC_REP = r'\g<1>\g<2>"{}"\g<4>'
S_SRC_VER_SCH = r"(^\s*S_PP_VERSION\s*=\s*)(.*)"
S_SRC_VER_REP = r'\g<1>"{}"'

# make sure ver num entered in pybaker is valid
S_SEM_VER_VALID = (
    # r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(.*)$"
    r"^"
    r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-("
    r"(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
    r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*"
    r"))?"
    r"(?:\+("
    r"[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*"
    r"))?"
    r"$"
)

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
# NB: format params are __PP_AUTHOR__ and __PP_NAME_PRJ_SMALL__
S_APP_ID_FMT = "org.{}.{}"

# ------------------------------------------------------------------------------
# dist stuff

S_DIST_EXT = ".tar.gz"
S_DIST_MODE = "w:gz"
S_DIST_REMOVE = ".py"

# ------------------------------------------------------------------------------
# readme stuff

# NB: format params are alt text and path to image
S_RM_SCREENSHOT = "![{}]({})"

# ------------------------------------------------------------------------------
# docs stuff

S_DOCS_MKDOCS = "mkdocs"
S_DOCS_PDOC3 = "pdoc3"
S_DOCS_THEME_RTD = "readthedocs"

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
        "Package",
        "pkg",
    ],
]

# list of filetypes that use hash (#) for comments
L_EXT_HASH = [
    ".py",
    ".toml",
    ".gitignore",
    ".desktop",
]

# list of file types to use md/html/xml comments (<!-- ... -->)
L_EXT_MARKUP = [
    ".md",
    ".html",
    ".xml",
    ".ui",
    ".glade",
]

# file exts for do_after_fix
L_EXT_DESKTOP = [".desktop"]
L_EXT_GTK = [".ui", ".glade"]
L_EXT_SRC = [".py"]
L_EXT_PO = [".po"]
L_EXT_HTML = [".html"]

# files to remove after the project is done
L_PURGE_FILES = [
    "ABOUT",
]

# which project types have a venv
L_MAKE_VENV = [
    "c",
    "g",
]

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
# prj type(s) for making an install.json
L_APP_INSTALL = [
    "c",
    "g",
]

# prj type(s) for making .desktop file
L_MAKE_DESK = ["g"]

# prj type(s) for making screenshot in README
L_SCREENSHOT = ["g"]

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

# DO NOT use dunders in the values here, they will not be fixed

# if you need to adjust any of these values based on a dunder, use
# do_before_fix() in this file

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
    # NB: the struggle here is that using the fixed format results in a
    # four-digit year, but using the locale format ('%x') results in a
    # two-digit year (at least for my locale, which in 'en_US'). so what to do?
    # what i really want is a locale format that uses four-digit years
    # everywhere. so i am faced with a 'cake and eat it too' situation. not
    # sure how to proceed but i think for now i will leave this as a
    # user-editable string and place it in the realm of 'edit it before you
    # run' along with author/email/license/etc
    # version format string for command line
    "__PP_DATE_FMT__": S_DATE_FMT,
    # filenames replaced in various places, rel to prj dir
    "__PP_LICENSE_FILE__": S_FILE_LICENSE,
    "__PP_README_FILE__": S_FILE_README,
    "__PP_TOML_FILE__": S_FILE_TOML,
    "__PP_REQS_FILE__": S_FILE_REQS,
    "__PP_DIR_IMAGES__": S_DIR_IMAGES,
    "__PP_INST_ASSETS__": S_DIR_ASSETS,
    "__PP_DIR_INSTALL__": S_DIR_INSTALL,
    "__PP_INST_CONF_FILE__": f"{S_DIR_INSTALL}/{S_FILE_INST_CFG}",
    "__PP_UNINST_CONF_FILE__": f"{S_DIR_INSTALL}/{S_FILE_UNINST_CFG}",
    # --------------------------------------------------------------------------
    # these paths are relative to the dev's prj name
    # i.e. /home/dev/Documents/Projects/Python/MyProject
    "__PP_DIR_CONF__": S_DIR_CONF,
    "__PP_DIR_SRC__": S_DIR_SRC,
    "__PP_PATH_LOCALE__": S_PATH_LOCALE,
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

# DO NOT use dunders in the values here, they will not be fixed

# if you need to adjust any of these values based on a dunder, use
# do_before_fix() in this file
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
    "__PP_DIST_DIR__": "",  # formatted name of the dist ([name_small]_[version])
    # --------------------------------------------------------------------------
    # these strings are calculated in do_before_fix
    "__PP_FILE_DESK__": "",  # final desk file, not template
    "__PP_IMG_README__": "",  # image for readme file logo
    "__PP_IMG_DESK__": "",  # image for .desktop logo
    "__PP_IMG_DASH__": "",  # image for dash/win logo
    "__PP_IMG_ABOUT__": "",  # image for about logo
    # NB: technically this should be metadata but we don't want dev editing,
    # only use metadata to recalculate these on every build
    "__PP_VER_MMR__": "",  # semantic version string, ie. "0.0.13"
    "__PP_VER_DISP__": "",  # formatted version string, ie. "Version 0.0.1"
}

# ------------------------------------------------------------------------------
# Public dictionaries
# ------------------------------------------------------------------------------

# these are settings that will be changed before running pybaker.py
# consider them the "each build" settings
D_PUB_META = {
    # the short description to use in __PP_README_FILE__ and pyproject.toml
    S_KEY_META_SHORT_DESC: "Short description",
    # the version number to use in __PP_README_FILE__ and pyproject.toml
    S_KEY_META_VERSION: "0.0.0",
    # the keywords to use in pyproject.toml and github
    S_KEY_META_KEYWORDS: [],
    # the python dependencies to use in __PP_README_FILE__, pyproject.toml,
    # github, and install.py
    # NB: key is dep name, val is link to dep (optional)
    S_KEY_META_DEPS: {"Python 3.10+": "https://python.org"},
    # the categories to use in .desktop for gui apps (found in pybaker_conf.py)
    S_KEY_META_CATS: [],
}

# dict of files to put in dist folder (defaults, written by pymaker, edited by
# hand, read by pybaker)
# NB: key is src, rel to prj dir
# NB: val is dst, rel to dist dir
D_PUB_DIST = {
    "c": {
        # basic stuff (put in assets folder)
        S_DIR_BIN: S_DIR_ASSETS,
        S_DIR_CONF: S_DIR_ASSETS,
        S_DIR_I18N: S_DIR_ASSETS,
        S_DIR_INSTALL: S_DIR_ASSETS,
        S_DIR_SRC: S_DIR_ASSETS,
        # requirements.txt in assets/install folder
        S_FILE_REQS: f"{S_DIR_ASSETS}/{S_DIR_INSTALL}",
    },
    "g": {
        # basic stuff (put in assets folder)
        S_DIR_BIN: S_DIR_ASSETS,
        S_DIR_CONF: S_DIR_ASSETS,
        S_DIR_I18N: S_DIR_ASSETS,
        S_DIR_IMAGES: S_DIR_ASSETS,
        S_DIR_INSTALL: S_DIR_ASSETS,
        S_DIR_SRC: S_DIR_ASSETS,
        # requirements.txt in assets/install folder
        S_FILE_REQS: f"{S_DIR_ASSETS}/{S_DIR_INSTALL}",
    },
    "p": {
        # basic stuff (put at top level)
        S_DIR_IMAGES: "",
        S_DIR_README: "",
        "__PP_NAME_PRJ_SMALL__": "",
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
        S_DIR_DIST,
        S_DIR_DOCS,
        S_DIR_I18N,
        S_DIR_MISC,
        S_FILE_LICENSE,
        S_FILE_REQS,
        S_DIR_TODO,
        "**/__pycache__",
        "site",
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
        ".gitignore",
        ".desktop",
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

# stuff to be used in pybaker
D_PUB_I18N = {
    # name of the project as domain
    S_KEY_PUB_I18N_DOM: "__PP_NAME_PRJ_SMALL__",
    # list of sources per domain
    S_KEY_PUB_I18N_SRC: [S_DIR_SRC],
    # computer languages
    S_KEY_PUB_I18N_CLANGS: {
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
    S_KEY_PUB_I18N_NO_EXT: {
        "Python": [
            "__PP_NAME_PRJ_SMALL__",
        ],
    },
    # list of written languages that are available
    S_KEY_PUB_I18N_WLANGS: [S_WLANG],
    # default charset for .pot/.po files
    S_KEY_PUB_I18N_CHAR: S_ENCODING,
}

# which docs maker to use, based on project type
D_PUB_DOCS = {
    "c": {
        S_KEY_DOCS_TOOL: S_DOCS_MKDOCS,
        S_KEY_DOCS_THEME: "",  # S_DOCS_THEME_RTD
        S_KEY_DOCS_USE_RM: True,
        S_KEY_DOCS_MAKE_API: True,
    },
    "g": {
        S_KEY_DOCS_TOOL: S_DOCS_MKDOCS,
        S_KEY_DOCS_THEME: "",  # S_DOCS_THEME_RTD
        S_KEY_DOCS_USE_RM: True,
        S_KEY_DOCS_MAKE_API: True,
    },
    "p": {
        S_KEY_DOCS_TOOL: S_DOCS_PDOC3,
    },
}

# dict in project to control post processing
D_PUB_DBG = {
    S_KEY_DBG_GIT: True,
    S_KEY_DBG_VENV: True,
    S_KEY_DBG_I18N: True,
    S_KEY_DBG_DOCS: True,
    S_KEY_DBG_INST: True,
    S_KEY_DBG_TREE: True,
    S_KEY_DBG_DIST: True,
}

# ------------------------------------------------------------------------------
# Other dictionaries
# ------------------------------------------------------------------------------

# dict in pymaker to control post processing in debug mode
D_DBG_PM = {
    S_KEY_DBG_GIT: False,
    S_KEY_DBG_VENV: False,
    S_KEY_DBG_I18N: False,
    S_KEY_DBG_DOCS: True,
    S_KEY_DBG_INST: False,
    S_KEY_DBG_TREE: False,
    S_KEY_DBG_DIST: False,
}

# dict in pybaker to control post processing in debug mode
D_DBG_PB = {
    S_KEY_DBG_GIT: False,
    S_KEY_DBG_VENV: False,
    S_KEY_DBG_I18N: False,
    S_KEY_DBG_DOCS: False,
    S_KEY_DBG_INST: False,
    S_KEY_DBG_TREE: False,
    S_KEY_DBG_DIST: False,
}

# dictionary of default stuff to put in install.json
# NB: in S_KEY_INST_CONT, key is rel to assets, val is rel to home
# these are the defaults, they can be edited in install/install.json before
# running pybaker
D_INSTALL = {
    "c": {
        S_KEY_INST_NAME: "__PP_NAME_PRJ_BIG__",
        S_KEY_INST_VER: "__PP_VER_MMR__",
        S_KEY_INST_DESK: False,
        S_KEY_INST_CONT: {
            f"{S_DIR_BIN}/__PP_NAME_PRJ_SMALL__": "__PP_USR_BIN__",
            S_DIR_CONF: "__PP_USR_INST__",
            S_DIR_I18N: "__PP_USR_INST__",
            S_DIR_IMAGES: "__PP_USR_INST__",
            S_DIR_INSTALL: "__PP_USR_INST__",
            S_DIR_SRC: "__PP_USR_INST__",
            S_FILE_UNINST_PY: "__PP_USR_INST__",
        },
    },
    "g": {
        S_KEY_INST_NAME: "__PP_NAME_PRJ_BIG__",
        S_KEY_INST_VER: "__PP_VER_MMR__",
        S_KEY_INST_DESK: True,
        S_KEY_INST_CONT: {
            f"{S_DIR_BIN}/__PP_NAME_PRJ_SMALL__": "__PP_USR_BIN__",
            S_DIR_CONF: "__PP_USR_INST__",
            S_DIR_I18N: "__PP_USR_INST__",
            S_DIR_IMAGES: "__PP_USR_INST__",
            S_DIR_INSTALL: "__PP_USR_INST__",
            S_DIR_SRC: "__PP_USR_INST__",
            S_FILE_UNINST_PY: "__PP_USR_INST__",
            # extra for gui
            "__PP_FILE_DESK__": "__PP_USR_APPS__",
        },
    },
}

# dict to remove when uninstalling
# NB: in S_KEY_INST_CONT, items are files or folders to delete
# these are the defaults, they can be edited in install/uninstall.json before
# running pybaker
D_UNINSTALL = {
    "c": {
        S_KEY_INST_NAME: "__PP_NAME_PRJ_BIG__",
        S_KEY_INST_VER: "__PP_VER_MMR__",
        S_KEY_INST_CONT: [
            "__PP_USR_INST__",
            "__PP_USR_BIN__/__PP_NAME_PRJ_SMALL__",
        ],
    },
    "g": {
        S_KEY_INST_NAME: "__PP_NAME_PRJ_BIG__",
        S_KEY_INST_VER: "__PP_VER_MMR__",
        S_KEY_INST_CONT: [
            "__PP_USR_INST__",
            "__PP_USR_BIN__/__PP_NAME_PRJ_SMALL__",
            # extra for gui
            "__PP_USR_APPS__/__PP_NAME_PRJ_BIG__.desktop",
        ],
    },
}

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

# map file ext to rep type
D_TYPE_RULES = {
    S_KEY_RULES_HASH: {
        S_KEY_RULES_EXT: L_EXT_HASH,
        S_KEY_RULES_REP: {
            # header stuff
            S_KEY_HDR_SCH: r"^(\s*#\s*\S*\s*:\s*)(\S+)(.*)$",
            S_KEY_LEAD: 1,
            S_KEY_VAL: 2,
            S_KEY_PAD: 3,
            # code stuff
            # NB: match first occurrence of unquoted marker to end of line
            S_KEY_SPLIT: r"[\'\"].*?[\'\"]|(#.*)",
            S_KEY_SPLIT_COMM: 1,
            # switch stuff
            S_KEY_SW_SCH: r"pyplate\s*:\s*(\S*)\s*=\s*(\S*)",
            S_KEY_SW_KEY: 1,
            S_KEY_SW_VAL: 2,
        },
    },
    S_KEY_RULES_MUD: {
        S_KEY_RULES_EXT: L_EXT_MARKUP,
        S_KEY_RULES_REP: {
            # header stuff
            S_KEY_HDR_SCH: r"^(\s*<!--\s*\S*\s*:\s*)(\S+)(.*-->.*)$",
            S_KEY_LEAD: 1,
            S_KEY_VAL: 2,
            S_KEY_PAD: 3,
        },
    },
}

# the type of projects that will ask for a second name
D_NAME_SEC = {
    "p": S_ASK_SEC_P,
    "g": S_ASK_SEC_G,
}

# default dict of switches
D_SWITCH_DEF = {
    S_SW_REPLACE: True,  # assume we want to replace
}

# default dict of line-level switches
# NB: value should be True if present and enabled, False if present and
# disabled, or default if not present
D_SW_LINE_DEF = {
    S_SW_REPLACE: True,  # assume we want to replace
}

# regex's to match project name
D_NAME = {
    S_KEY_NAME_START: r"(^[a-zA-Z])",
    S_KEY_NAME_END: r"([a-zA-Z\d]$)",
    S_KEY_NAME_MID: r"(^[a-zA-Z\d\-_ ]*$)",
}

# dirs to remove after the project is fixed by either pm or pb
D_PURGE_DIRS = {
    "p": [
        S_DIR_BIN,
        S_DIR_CONF,
        S_DIR_DIST,
        S_DIR_I18N,
        S_DIR_INSTALL,
        S_DIR_SRC,
    ]
}

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Do any work before template copy
# ------------------------------------------------------------------------------
def do_before_template(_dir_prj, _dict_prv, _dict_pub, _dict_dbg):
    """
    Do any work before template copy

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Do any work before copying the template. This method is called just before
    _do_template, before any files have been copied.\n
    It is mostly used to make final adjustments to the 'dict_prv' and
    'dict_pub' dicts before any copying occurs.
    """


# ------------------------------------------------------------------------------
# Do any work after template copy
# ------------------------------------------------------------------------------
def do_after_template(dir_prj, dict_prv, _dict_pub, dict_dbg):
    """
    Do any work after template copy

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Do any work after copying the template. This function is called after
    _do_template, and before _do_before_fix.\n
    Use this function to create any files that your project needs to be created
    dynamically. You can also run code that is only called by PyMaker before
    fixing, like chopping the readme file sections.
    """

    # get project type
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # --------------------------------------------------------------------------
    # venv

    # if venv flag is set
    if dict_dbg[S_KEY_DBG_VENV]:

        # venv only for certain project types
        if prj_type in L_MAKE_VENV:

            print(S_ACTION_VENV, end="", flush=True)

            # get name ov venv folder and reqs file
            dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]
            file_reqs = dir_prj / S_FILE_REQS

            # do the thing with the thing
            cv = CNVenv(dir_prj, dir_venv)
            try:
                cv.create()
                if file_reqs.exists():
                    cv.install_reqs(file_reqs)
                print(S_ACTION_DONE)
            except Exception as e:
                print(S_ACTION_FAIL)
                print(S_MSG_NO_INTERNET)
                raise e
        else:
            # no venv, no reqs
            (Path(dir_prj) / S_FILE_REQS).unlink()

    # --------------------------------------------------------------------------
    # git

    # if git flag
    if dict_dbg[S_KEY_DBG_GIT]:

        # show info
        print(S_ACTION_GIT, end="", flush=True)

        # add git dir
        cmd = S_CMD_GIT_CREATE.format(dir_prj)
        F.sh(cmd, shell=True)

        # show info
        print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # install/uninstall config files

    # if install flag is set
    if dict_dbg[S_KEY_DBG_INST]:

        # cli/gui
        if prj_type in L_APP_INSTALL:

            # show info
            print(S_ACTION_INST, end="", flush=True)

            # create a template install cfg file
            dict_inst = D_INSTALL[prj_type]

            # fix dunders in inst cfg file
            path_inst = dir_prj / S_PATH_INST_CFG
            F.save_dict(dict_inst, [path_inst])

            # create a template uninstall cfg file
            dict_uninst = D_UNINSTALL[prj_type]

            # fix dunders in uninst cfg file
            path_uninst = dir_prj / S_PATH_UNINST_CFG
            F.save_dict(dict_uninst, [path_uninst])

            # show info
            print(S_ACTION_DONE)


# ------------------------------------------------------------------------------
# Do any work before fix
# ------------------------------------------------------------------------------
def do_before_fix(_dir_prj, dict_prv, dict_pub, _dict_dbg, _pymaker):
    """
    Do any work before fix

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings
        pymaker: True if called by PyMaker, False if called by PyBaker

    Do any work before fix.\n
    This function is called by both PyMaker and PyBaker.\n
    This method is called just before_do_fix, after all dunders have been
    configured, but before any files have been modified.\n
    It is mostly used to make final adjustments to the 'dict_prv' and
    'dict_pub' dicts before any replacement occurs.
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
    name_prj_big = dict_prv_prj["__PP_NAME_PRJ_BIG__"]
    dict_prv_prj["__PP_FILE_DESK__"] = (
        f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_DESKTOP}/{name_prj_big}.desktop"
    )

    # app id for gui
    author = dict_prv_all["__PP_AUTHOR__"]
    dict_prv_prj["__PP_APP_ID__"] = S_APP_ID_FMT.format(author, name_prj_small)

    # --------------------------------------------------------------------------
    # version stuff

    # get base version
    ver_base = dict_pub_meta[S_KEY_META_VERSION]

    # set display of version
    dict_prv_prj["__PP_VER_DISP__"] = S_VER_DISP_FMT.format(ver_base)

    # semantic version with meta info
    str_sem = ver_base
    dict_prv_prj["__PP_VER_MMR__"] = str_sem

    # fix ver for dist filename
    ver_dist = str_sem

    # format dist dir name with prj and ver
    name_fmt = S_VER_DIST_FMT.format(name_prj_small, ver_dist)
    dict_prv_prj["__PP_DIST_DIR__"] = name_fmt

    # ----------------------------------------------------------------------
    # calculate current date
    # NB: this is the initial create date for all files in the template
    # new files added to the project will have their dates set to the date
    # when pybaker was last run

    # get current date and format it according to dev fmt
    now = datetime.now()
    fmt_date = S_DATE_FMT
    info_date = now.strftime(fmt_date)
    dict_prv_prj["__PP_DATE__"] = info_date

    # gui app/win replacements
    name_prj_pascal = dict_prv_prj["__PP_NAME_PRJ_PASCAL__"]
    name_sec_small = dict_prv_prj["__PP_NAME_SEC_SMALL__"]
    name_sec_pascal = dict_prv_prj["__PP_NAME_SEC_PASCAL__"]
    dict_prv_prj["__PP_FILE_APP__"] = S_APP_FILE_FMT.format(name_prj_small)
    dict_prv_prj["__PP_CLASS_APP__"] = S_APP_CLASS_FMT.format(name_prj_pascal)
    dict_prv_prj["__PP_FILE_WIN__"] = S_WIN_FILE_FMT.format(name_sec_small)
    dict_prv_prj["__PP_CLASS_WIN__"] = S_WIN_CLASS_FMT.format(name_sec_pascal)

    # various image files
    img_ext = (
        f".{S_IMG_EXT.lower()}"
        if not S_IMG_EXT.startswith(".")
        else S_IMG_EXT.lower()
    )
    dict_prv_prj["__PP_IMG_README__"] = (
        f"{S_DIR_IMAGES}/{name_prj_small}{img_ext}"
    )
    # NB: .desktop needs abs path to img
    dict_prv_prj["__PP_IMG_DESK__"] = (
        f"{usr_inst}/{S_DIR_IMAGES}/{name_prj_small}{img_ext}"
    )
    # NB: .ui files need rel path to img
    dict_prv_prj["__PP_IMG_DASH__"] = (
        f"{"../../.."}/{S_DIR_IMAGES}/{name_prj_small}{img_ext}"
    )
    dict_prv_prj["__PP_IMG_ABOUT__"] = (
        f"{"../../.."}/{S_DIR_IMAGES}/{name_prj_small}{img_ext}"
    )


# ------------------------------------------------------------------------------
# Do any work after fix
# ------------------------------------------------------------------------------
def do_after_fix(dir_prj, dict_prv, dict_pub, dict_dbg, pymaker):
    """
    Do any work after fix

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings
        pymaker: True if called by PyMaker, False if called by PyBaker

    Do any work after fix.\n
    This function is called by both PyMaker and PyBaker.\n
    This method is called just after _do_fix, after all files have been
    modified.\n
    It is mostly used to update metadata once all the normal fixes have been
    applied.
    """

    # get project type
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # --------------------------------------------------------------------------
    # metadata

    # NB: this is an example of how to use the blacklist filter in your own
    # customized fix routine

    # print info
    print(S_ACTION_META, end="", flush=True)

    # NB: this function uses the blacklist to filter files at the very end of
    # the fix process. at this point you can assume ALL dunders in ALL eligible
    # files have been fixed, as well as paths/filenames. also dict_pub and
    # dict_prv have been undunderized
    dict_bl_glob = dict_pub[S_KEY_PUB_BL]
    dict_bl = F.fix_globs(dir_prj, dict_bl_glob)

    # just shorten the names
    skip_all = dict_bl[S_KEY_SKIP_ALL]
    skip_contents = dict_bl[S_KEY_SKIP_CONTENTS]

    # --------------------------------------------------------------------------
    # do the fixes

    # NB: root is a full path, dirs and files are relative to root
    for root, root_dirs, root_files in dir_prj.walk():

        # handle dirs in skip_all
        if root in skip_all:
            # NB: don't recurse into subfolders
            root_dirs.clear()
            continue

        # convert files into Paths
        files = [root / f for f in root_files]

        # for each file item
        for item in files:

            # handle files in skip_all
            if item in skip_all:
                continue

            # handle dirs/files in skip_contents
            if not root in skip_contents and not item in skip_contents:

                # fix content with appropriate dict
                _fix_meta(item, dict_prv, dict_pub)

    # print done
    print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # readme chop section

    path_readme = dir_prj / D_PRV_ALL["__PP_README_FILE__"]
    if path_readme.exists():

        print(S_ACTION_README, end="", flush=True)

        # the whole text of the file
        text = ""

        # open and read whole file
        with open(path_readme, "r", encoding=S_ENCODING) as a_file:
            text = a_file.read()

        # find the remove blocks (opposite of prj type)
        if prj_type in L_APP_INSTALL:
            str_pattern = S_RM_PKG
        else:
            str_pattern = S_RM_APP

        # replace block with empty string (equiv to deleting it)
        # NB: need S flag to make dot match newline
        text = re.sub(str_pattern, "", text, flags=re.S)

        # save file
        with open(path_readme, "w", encoding=S_ENCODING) as a_file:
            a_file.write(text)

        # show info
        print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # i18n

    # # path to desktop template
    path_dsk_tmp = dir_prj / S_FILE_DSK_TMP
    # path to desktop output
    path_dsk_out = dir_prj / dict_prv[S_KEY_PRV_PRJ]["__PP_FILE_DESK__"]

    # if i18n flag is set
    if dict_dbg[S_KEY_DBG_I18N]:

        # print info
        print(S_ACTION_I18N, end="", flush=True)

        # ----------------------------------------------------------------------
        # do bulk of i18n

        # create CNPotPy object
        potpy = CNPotPy(
            # header
            str_domain=dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_PRJ_SMALL__"],
            str_version=dict_prv[S_KEY_PRV_PRJ]["__PP_VER_MMR__"],
            str_author=dict_prv[S_KEY_PRV_ALL]["__PP_AUTHOR__"],
            str_email=dict_prv[S_KEY_PRV_ALL]["__PP_EMAIL__"],
            # base prj dir
            dir_prj=dir_prj,
            # in
            list_src=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_SRC],
            # out
            dir_pot=S_PATH_POT,
            dir_po=S_PATH_PO,
            dir_locale=S_PATH_LOCALE,
            # optional in
            str_tag=S_I18N_TAG,
            dict_clangs=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_CLANGS],
            dict_no_ext=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_NO_EXT],
            list_wlangs=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_WLANGS],
            charset=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_CHAR],
            location=False,
        )

        # make .pot, .po, and .mo files
        potpy.main()

        # ----------------------------------------------------------------------
        # do .desktop i18n/version

        # check if we want template
        if prj_type in L_MAKE_DESK and not path_dsk_tmp.exists():

            # we want template, but does not exist
            print("\n" + S_ERR_DESK_NO_TEMP.format(path_dsk_tmp, path_dsk_out))
        else:
            # do the thing
            potpy.make_desktop(path_dsk_tmp, path_dsk_out)

        # fix version in .po files (not always recreated by pybaker)
        path_po = dir_prj / S_DIR_I18N / S_DIR_PO
        for root, root_dirs, root_files in path_po.walk():
            files = [root / file for file in root_files]
            files = [
                file
                for file in files
                if PP.is_path_ext_in_list(file, L_EXT_PO)
            ]
            for item in files:

                # get sub-dicts we need
                dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]

                # default text if we can't open file
                text = ""

                # open file and get contents
                with open(item, "r", encoding=S_ENCODING) as a_file:
                    text = a_file.read()

                # replace version
                str_pattern = S_PO_VER_SCH
                pp_version = dict_prv_prj["__PP_VER_MMR__"]
                str_rep = S_PO_VER_REP.format(pp_version)
                text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

                # save file
                with open(item, "w", encoding=S_ENCODING) as a_file:
                    a_file.write(text)

        # ----------------------------------------------------------------------
        # we are done
        print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # tree
    # NB: run last so it includes .git and .venv folders
    # NB: this will wipe out all previous checks (maybe good?)

    # if tree flag is set
    if dict_dbg[S_KEY_DBG_TREE]:

        # print info
        print(S_ACTION_TREE, end="", flush=True)

        # get path to tree
        file_tree = dir_prj / S_TREE_FILE

        # create the file so it includes itself
        with open(file_tree, "w", encoding=S_ENCODING) as a_file:
            a_file.write("")

        # create tree object and call
        tree_obj = CNTree(
            str(dir_prj),
            filter_list=dict_pub[S_KEY_PUB_BL][S_KEY_SKIP_TREE],
            dir_format=S_TREE_DIR_FORMAT,
            file_format=S_TREE_FILE_FORMAT,
        )
        tree_str = tree_obj.main()

        # write to file
        with open(file_tree, "w", encoding=S_ENCODING) as a_file:
            a_file.write(tree_str)

        # ----------------------------------------------------------------------
        # we are done
        print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # fix po files outside blacklist

    # print info
    print(S_ACTION_PO, end="", flush=True)

    # get i18n path
    path = dir_prj / S_DIR_I18N

    # get sub-dicts we need
    dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]

    for root, root_dirs, root_files in path.walk():

        root_files = [root / root_file for root_file in root_files]

        for root_file in root_files:

            # only fix po files
            # if not root_file.suffix.lower() == ".po":
            if not PP.is_path_ext_in_list(root_file, L_EXT_PO):
                continue

            # default text if we can't open file
            text = ""

            # open file and get contents
            with open(root_file, "r", encoding=S_ENCODING) as a_file:
                text = a_file.read()

            # replace version
            str_pattern = S_PO_VER_SCH
            pp_version = dict_prv_prj["__PP_VER_MMR__"]
            str_rep = S_PO_VER_REP.format(pp_version)
            text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

            # save file
            with open(root_file, "w", encoding=S_ENCODING) as a_file:
                a_file.write(text)

    # --------------------------------------------------------------------------
    # purge package dirs

    if prj_type in D_PURGE_DIRS:
        l_purge = D_PURGE_DIRS[prj_type]
        l_purge = [
            (
                Path(dir_prj) / item
                if not Path(item).is_absolute()
                else Path(item)
            )
            for item in l_purge
        ]
        for item in l_purge:
            if item.exists():
                shutil.rmtree(item)

    # print done
    print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # docs

    # if docs flag is set
    if dict_dbg[S_KEY_DBG_DOCS]:

        # get the doc tool from the project info
        # NB: doc_tool is the import file name
        str_doc_tool = dict_pub[S_KEY_PUB_DOCS][S_KEY_DOCS_TOOL]
        doc_tool = None
        if str_doc_tool == S_DOCS_PDOC3:
            doc_tool = pdoc
        elif str_doc_tool == S_DOCS_MKDOCS:
            doc_tool = mkdocs

        # if we found a tool
        if doc_tool:

            # print info
            print(S_ACTION_MAKE_DOCS, end="", flush=True)

            # the command to make pdoc/mkdocs/...
            try:
                if pymaker:
                    doc_tool.make_docs(
                        dir_prj, dict_prv, dict_pub, P_DIR_PP, P_DIR_PP_VENV
                    )
                    dict_pub[S_KEY_PUB_DOCS][S_KEY_DOCS_USE_RM] = False
                else:
                    doc_tool.bake_docs(
                        dir_prj, dict_prv, dict_pub, P_DIR_PP, P_DIR_PP_VENV
                    )
                print(S_ACTION_DONE)
            except Exception as e:
                print(S_ACTION_FAIL)
                raise e


# ------------------------------------------------------------------------------
# Do any work before making dist
# ------------------------------------------------------------------------------
def do_before_dist(dir_prj, dict_prv, _dict_pub, dict_dbg):
    """
    Do any work before making dist

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Do any work on the dist folder before it is created. This method is called
    after _do_after_fix, and before _do_dist.
    """

    # get project type
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # --------------------------------------------------------------------------
    # venv

    # if venv flag is set
    if dict_dbg[S_KEY_DBG_VENV]:

        # venv only for certain project types
        if prj_type in L_MAKE_VENV:

            # print info
            print(S_ACTION_FREEZE, end="", flush=True)

            # get name ov venv folder and reqs file
            dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]
            file_reqs = dir_prj / S_FILE_REQS

            # do the thing with the thing
            cv = CNVenv(dir_prj, dir_venv)
            try:
                cv.freeze(file_reqs)
                print(S_ACTION_DONE)
            except Exception as e:
                print(S_ACTION_FAIL)
                raise e

    # --------------------------------------------------------------------------
    # purge package dirs

    # if project type in dict
    if prj_type in D_PURGE_DIRS:

        # get list and make items absolute
        l_purge = D_PURGE_DIRS[prj_type]
        l_purge = [Path(item) for item in l_purge]
        l_purge = [
            dir_prj / item if not item.is_absolute() else item
            for item in l_purge
        ]

        # purge dirs
        for item in l_purge:
            if item.exists() and item.is_dir():
                shutil.rmtree(item)


# ------------------------------------------------------------------------------
# Do any work after making dist
# ------------------------------------------------------------------------------
def do_after_dist(dir_prj, dict_prv, _dict_pub, dict_dbg):
    """
    Do any work after making dist

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Do any work on the dist folder after it is created. This method is called
    after _do_dist. Currently, this method purges any "ABOUT" file used as
    placeholders for github syncing. It also tars the source folder if it is a
    package, making for one (or two) less steps in the user's install process.
    """

    # get dist dir for all operations
    dist = Path(dir_prj) / S_DIR_DIST
    name_fmt = dict_prv[S_KEY_PRV_PRJ]["__PP_DIST_DIR__"]
    p_dist = dist / name_fmt

    # --------------------------------------------------------------------------
    # move some files around between end of dist and start of install

    # get project type
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    if prj_type in L_APP_INSTALL:
        # move install.py to above assets
        file_inst = p_dist / S_DIR_ASSETS / S_DIR_INSTALL / S_FILE_INST_PY
        if file_inst.exists():
            shutil.move(file_inst, p_dist)

        # move uninstall.py to top of assets
        file_uninst = p_dist / S_DIR_ASSETS / S_DIR_INSTALL / S_FILE_UNINST_PY
        if file_uninst.exists():
            dest = p_dist / S_DIR_ASSETS
            shutil.move(file_uninst, dest)

    # --------------------------------------------------------------------------
    # remove all "ABOUT" files

    # print info
    print(S_ACTION_PURGE, end="", flush=True)

    # first purge all dummy files
    for root, _root_dirs, root_files in p_dist.walk():

        # convert files into Paths
        files = [root / f for f in root_files]

        # for each file item
        for item in files:

            # if it is in purge list, delete it
            if item.name in L_PURGE_FILES:
                item.unlink()

    # print info
    print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # compress dist

    # print info
    print(S_ACTION_COMPRESS, end="", flush=True)

    # get prj type
    name_small = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_PRJ_SMALL__"]

    # remove ext from bin file
    old_bin = (
        p_dist / S_DIR_ASSETS / S_DIR_BIN / f"{name_small}{S_DIST_REMOVE}"
    )
    new_bin = p_dist / S_DIR_ASSETS / S_DIR_BIN / f"{name_small}"
    if old_bin.exists():
        old_bin.rename(new_bin)

    # now do normal dist tar
    in_dir = p_dist
    out_file = Path(S_DIR_DIST) / f"{in_dir}{S_DIST_EXT}"
    with tarfile.open(out_file, mode=S_DIST_MODE) as compressed:
        compressed.add(in_dir, arcname=Path(in_dir).name)

    # print info
    print(S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # delete the origin dir, if key set

    # if debug key set
    if dict_dbg[S_KEY_DBG_DIST]:

        # print info
        print(S_ACTION_REM_DIST, end="", flush=True)

        # get dist dir for all operations
        dist = Path(dir_prj) / S_DIR_DIST
        name_fmt = dict_prv[S_KEY_PRV_PRJ]["__PP_DIST_DIR__"]
        p_dist = dist / name_fmt

        # delete folder
        shutil.rmtree(p_dist)

        # show info
        print(S_ACTION_DONE)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Fix metadata in individual files
# ------------------------------------------------------------------------------
def _fix_meta(path, dict_prv, dict_pub):
    """
    Fix metadata in individual files

    Args:
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Fixes metadata in individual files. Note that this function is only called
    for files that make it through the BL filter. Switches are your problem.
    """

    # get sub-dicts we need
    dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]
    dict_pub_meta = dict_pub[S_KEY_PUB_META]

    # do md/html/xml separately (needs special handling)
    dict_type_rules = PP.get_type_rules(path)

    # fix readme
    if path.name == S_FILE_README:
        _fix_readme(path, dict_prv_prj, dict_pub_meta, dict_type_rules)

    # fix pyproject
    if path.name == S_FILE_TOML:
        _fix_pyproject(path, dict_prv_prj, dict_pub_meta, dict_type_rules)

    # fix inst
    if path.name == S_FILE_INST_CFG:
        _fix_inst(path, dict_prv_prj, dict_pub_meta, dict_type_rules)

    # fix uninst
    if path.name == S_FILE_UNINST_CFG:
        _fix_inst(path, dict_prv_prj, dict_pub_meta, dict_type_rules)

    # fix desktop
    if PP.is_path_ext_in_list(path, L_EXT_DESKTOP):
        _fix_desktop(path, dict_prv_prj, dict_pub_meta, dict_type_rules)

    # fix ui files
    if PP.is_path_ext_in_list(path, L_EXT_GTK):
        _fix_ui(path, dict_prv_prj, dict_pub_meta, dict_type_rules)

    # fix src files
    if PP.is_path_ext_in_list(path, L_EXT_SRC):
        _fix_src(path, dict_prv_prj, dict_pub_meta, dict_type_rules)


# ------------------------------------------------------------------------------
# Remove/replace parts of the main README file
# ------------------------------------------------------------------------------
def _fix_readme(path, dict_prv_prj, dict_pub_meta, _dict_type_rules):
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

    # replace short description
    str_pattern = S_RM_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_RM_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # replace version
    str_pattern = S_RM_VER_SCH
    pp_ver_disp = dict_prv_prj["__PP_VER_DISP__"]
    str_rep = S_RM_VER_REP.format(pp_ver_disp)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # --------------------------------------------------------------------------

    # not technically metadata, but other stuff we gotta fix anyway

    # fix readme screenshot

    # get project type
    prj_type = dict_prv_prj["__PP_TYPE_PRJ__"]

    # should we futz with the readme?
    if prj_type in L_SCREENSHOT:

        # format the alt text
        s_alt = S_ERR_NO_SCREENSHOT.format(S_PATH_SCREENSHOT)
        s_img = S_RM_SCREENSHOT.format(s_alt, S_PATH_SCREENSHOT)

        # replace screenshot
        str_pattern = S_RM_SS_SCH
        str_rep = S_RM_SS_REP.format(s_img)
        text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # --------------------------------------------------------------------------
    # fix deps in readme

    # get deps as links
    d_py_deps = dict_pub_meta[S_KEY_META_DEPS]
    l_rm_deps = [
        f"[{key}]({val})" if val != "" else key
        for key, val in d_py_deps.items()
    ]

    # make a pretty string
    s_rm_deps = "<br>\n".join(l_rm_deps)
    if len(s_rm_deps) == 0:
        s_rm_deps = S_DEPS_NONE

    # replace dependencies array
    str_pattern = S_RM_DEPS_SCH
    str_rep = S_RM_DEPS_REP.format(s_rm_deps)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # --------------------------------------------------------------------------

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the pyproject file
# ------------------------------------------------------------------------------
def _fix_pyproject(path, dict_prv_prj, dict_pub_meta, _dict_type_rules):
    """
    Replace text in the pyproject file

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: the dict of metadata to replace in the file

    Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = S_TOML_VER_SCH
    str_rep = dict_prv_prj["__PP_VER_MMR__"]
    str_rep = S_TOML_VER_REP.format(str_rep)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = S_TOML_DESC_SCH
    str_rep = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_TOML_DESC_REP.format(str_rep)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # fix keywords for pyproject.toml
    l_keywords = dict_pub_meta[S_KEY_META_KEYWORDS]
    q_keywords = [f'"{item}"' for item in l_keywords]
    s_keywords = ", ".join(q_keywords)

    # replace keywords array
    str_pattern = S_TOML_KW_SCH
    str_rep = S_TOML_KW_REP.format(s_keywords)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# --------------------------------------------------------------------------
# Fix the version number in install/uninstall files
# --------------------------------------------------------------------------
def _fix_inst(path, dict_prv_prj, _dict_pub_meta, _dict_type_rules):
    """
    Fix the version number in install/uninstall files

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Fixes the version number in any file whose name matches S_FILE_INST_CFG or
    S_FILE_UNINST_CFG.
    """

    # get version from project.json
    version = dict_prv_prj["__PP_VER_MMR__"]

    # load/change/save
    a_dict = F.load_dicts([path])
    a_dict[S_KEY_INST_VER] = version
    F.save_dict(a_dict, [path])

    # load/change/save
    a_dict = F.load_dicts([path])
    a_dict[S_KEY_INST_VER] = version
    F.save_dict(a_dict, [path])


# ------------------------------------------------------------------------------
# Replace text in the desktop file
# ------------------------------------------------------------------------------
def _fix_desktop(path, _dict_prv_prj, dict_pub_meta, _dict_type_rules):
    """
    Replace text in the desktop file

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: the dict of metadata to replace in the file

    Replaces the description (comment) and category text in a .desktop file for
    programs that use this.
    """

    # the result cat list
    new_cats = []

    # check cats now
    cats = dict_pub_meta[S_KEY_META_CATS]
    for cat in cats:
        # category is not valid
        if not cat in L_CATS:
            # category is not valid, print error
            print("\n", path, ":")
            print(S_ERR_DESK_CAT.format(cat))
        else:
            new_cats.append(cat)

    # convert list to string
    str_cat = "".join(new_cats)

    # --------------------------------------------------------------------------

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace categories
    str_pattern = S_DESK_CAT_SCH
    str_rep = S_DESK_CAT_REP.format(str_cat)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description (comment)
    str_pattern = S_DESK_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_DESK_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the UI files
# ------------------------------------------------------------------------------
def _fix_ui(path, dict_prv_prj, dict_pub_meta, _dict_type_rules):
    """
    Replace text in the UI files

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: the dict of metadata to replace in the file

    Replace description and version number in the UI file.
    """

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = S_UI_VER_SCH
    pp_version = dict_prv_prj["__PP_VER_MMR__"]
    str_rep = S_UI_VER_REP.format(pp_version)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = S_UI_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_UI_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Fix the version number and short description in source files
# ------------------------------------------------------------------------------
def _fix_src(path, dict_prv_prj, dict_pub_meta, dict_type_rules):
    """
    Fix the version number and short description in source files

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Returns:
        The new line of code

    Fixes the version number and short description in any file whose extension
    is in L_EXT_SRC.
    """

    # NB: this is an example of using switches to control line replacement

    # the switch statuses
    dict_sw_block = dict(D_SWITCH_DEF)
    dict_sw_line = dict(dict_sw_block)

    # the whole text of the file
    lines = []

    # open and read whole file
    with open(path, "r", encoding=S_ENCODING) as a_file:
        lines = a_file.readlines()

    # for each line in array
    for index, line in enumerate(lines):

        # ------------------------------------------------------------------
        # skip blank lines
        if line.strip() == "":
            continue

        # ------------------------------------------------------------------
        # split the line into code and comm

        # we will split the line into two parts
        # NB: assume code is whole line (i.e. no trailing comment)
        split_pos = 0
        code = line
        comm = ""

        # find split sequence
        split_sch = dict_type_rules[S_KEY_SPLIT]
        split_grp = dict_type_rules[S_KEY_SPLIT_COMM]

        # there may be multiple matches per line (ignore quoted markers)
        matches = re.finditer(split_sch, line)

        # only use matches that have the right group
        matches = [match for match in matches if match.group(split_grp)]
        for match in matches:

            # split the line into code and comment (including delimiter)
            split_pos = match.start(split_grp)
            code = line[:split_pos]
            comm = line[split_pos:]

        # ------------------------------------------------------------------
        # check for switches

        # reset line switch values to block switch values
        dict_sw_line = dict(dict_sw_block)

        # check switches
        PP.check_switches(
            code,
            comm,
            dict_type_rules,
            dict_sw_block,
            dict_sw_line,
        )

        # check for block or line replace switch
        repl = False
        if (
            dict_sw_block[S_SW_REPLACE] is True
            and dict_sw_line[S_SW_REPLACE] is True
        ) or dict_sw_line[S_SW_REPLACE] is True:
            repl = True

        # switch says no, gtfo
        if not repl:
            continue

        # ----------------------------------------------------------------------

        # replace version in line
        ver = dict_prv_prj["__PP_VER_MMR__"]
        str_sch = S_SRC_VER_SCH
        str_rep = S_SRC_VER_REP.format(ver)
        line = re.sub(str_sch, str_rep, line, flags=re.M)

        # replace short desc in line
        desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
        str_sch = S_SRC_DESC_SCH
        str_rep = S_SRC_DESC_REP.format(desc)
        line = re.sub(str_sch, str_rep, line, flags=re.M)

        # replace line in lines
        lines[index] = line

    # save lines back to file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.writelines(lines)


# -)
