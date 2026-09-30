# ------------------------------------------------------------------------------
# Package :PyPlate                                                /          \
# Filename: conf.py                                               |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines

"""
This module separates out the variables from pymaker.py.
This file, and the template folder, are the main ways to customize PyPlate.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# lib imports
from cnlib import cnfunctions

# # local imports
import ppglobals

# ------------------------------------------------------------------------------
# I18N
# ------------------------------------------------------------------------------

# get underscore function
_ = ppglobals._

# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Start customization
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Integers
# ------------------------------------------------------------------------------

# rotating log stuff
I_LOG_SIZE = 2097152  # max log file size in bytes (2 Mb)
I_LOG_COUNT = 5  # max number of log files

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# basic developer info

# author info
S_AUTHOR = "cyclopticnerve"
S_EMAIL = "cyclopticnerve@gmail.com"
S_URL = "https://github.com/cyclopticnerve"
# license info
S_LICENSE_NAME = "WTFPLv2"
S_LICENSE_URL = "http://www.wtfpl.net"
# license badge for readme
S_LICENSE_BADGE_URL = (
    "https://img.shields.io/badge/License-WTFPL-brightgreen.svg"
)
S_RM_LICENSE = (
    "[!"  # open image tag
    f"[License: {S_LICENSE_NAME}]"  # alt text
    f"({S_LICENSE_BADGE_URL})"  # img src
    "]"  # close image tag
    f"({S_LICENSE_URL})"  # click url
)

# ------------------------------------------------------------------------------
# spice up version number

# NB: format param is __PP_VER_MMR__
# I18N: printable version number
S_VER_DISP_FMT = _("Version {}")
# NB: format params are __PP_NAME_PRJ_SMALL__ and __PP_VER_MMR__
S_VER_DIST_FMT = "{}-{}"

# ------------------------------------------------------------------------------
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
S_ASK_SEC_P = _("Module name ({}): ")
# NB: format param is __PP_NAME_PRJ_SMALL__
# I18N: ask window class name
S_ASK_SEC_G = _("Window class name ({}): ")
# NB: format param is current working dir
# I18N: ask prj name if running pybaker in IDE
S_ASK_IDE = _("Project name: (relative to {}): ")
# NB: param is current version
# I18N: ask for new version
S_ASK_VER = _("Version ({}): ")
# NB: format param is prog name
# I18N: ask to uninstall
S_ASK_UNINST = _("This will uninstall {}.\nDo you want to continue?")
# I18N: ask to overwrite
# NB: format param is file name
S_ASK_OVER = _("The file {} already exists. Do you want to overwrite it?")

# placeholder files
# NB: this should be the same as the ones preexisting in template
# I18N: the name of the placeholder file
S_PH_NAME = _("ABOUT")
# I18N: the text to put in the default placeholder file
S_PH_TEXT = _(
    "A placeholder file since GitHub does not allow syncing empty folders\n"
    "These files are automatically managed by PyPlate"
)

# error strings
# I18N: general error start
S_ERR_ERR = _("Error:")
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
    "See https://semver.org/"
)
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
# I18N: uninstall not found
S_ERR_NO_UNINST = _("Uninstall files not found")
# NB: format param is file path
# I18N: could not find -c file
S_ERR_NO_CFG = _("Config file {} not found")
# I18N: language already exists in project.json and i18n folder
S_ERR_LANG_EXIST = _("Language file {} already exists")
# I18N: could not find lang code in .po file
S_ERR_NO_LANG = _("Could not get language code from {}")
# I18N: ctrl-c in spinner
S_ERR_CTRL_C = _("Keyboard interrupt (Ctrl-C)")
# I18N: there was an error when making
# NB: fmt param is prj name big
S_ERR_MAKE = _("There were errors making {}")
# I18N: there was an error when baking
# NB: fmt param is prj name big
S_ERR_BAKE = _("There were errors baking {}")
# I18N: common message to use debug mode
S_ERR_USE_D = _("Use -d for more information")
# I18N: switch value error
# NB: format params are file path, bad val, list of val keys in def dict
S_ERR_SW_VAL = _("{}: {} is not a valid switch value, should be one of: {}")
# I18N: switch name error
# NB: format params are file path, bad name, list of name keys in def dict
S_ERR_SW_NAME = _("{}: () is not a valid switch name, should be one of: {}")
# I18N: control c
S_ERR_CTRL_C = _("Keyboard interrupt (Ctrl-C)")

# log formats
S_LOG_FMT = "%(asctime)s [%(levelname)-7s] %(message)s"
S_LOG_DATE_FMT = "%Y-%m-%d %I:%M:%S"

# messages

# I18N: process aborted
S_MSG_ABORT = _("Aborted")
# make msg
# NB: param is name of project folder
S_MSG_MAKE = _("Making {}")
# NB: param is name of project folder
# I18N: done baking
S_MSG_MAKE_DONE = _("Done making {}")
# NB: param is name of project folder
# I18N: start baking
S_MSG_BAKE = _("Baking {}")
# NB: param is name of project folder
# I18N: done baking
S_MSG_BAKE_DONE = _("Done baking {}")
# NB: format param is file name
# I18N: add language at cmd line
S_MSG_LANG_ADD = _("Adding language file {}...")

# ------------------------------------------------------------------------------
# commands for do_after_fix

# cmd for git
# NB: format param is proj dir
S_CMD_GIT_CREATE = "cd {}; git init -q"
# NB: format params are prj dir and venv name
S_CMD_VENV_INST_SELF = "cd {};. {}/bin/activate;python3 -m pip install -e ."
# NB: format params are prj dir, venv name, and reqs file
S_CMD_VENV_INST_REQS = "cd {};. {}/bin/activate;python3 -m pip install -r {}"

# some mkdocs stuff

# cmd for mkdocs
# NB: format param is path to project
S_CMD_DOC_BUILD = "cd {};mkdocs build"
# cmd for mkdocs
# NB: format param is path to project
S_CMD_DOC_DEPLOY = "cd {};mkdocs gh-deploy"

# file ext for in/out
S_MK_EXT_IN = ".py"
S_MK_EXT_OUT = ".md"

# default to include mkdocstrings content in .md file
# NB: format params are file name and formatted pkg name, done in make_docs
S_MK_DEF_FILE = "# {}\n::: {}"
S_MK_INDEX = "index.md"
S_MK_DIR_IMG = "img"

# ------------------------------------------------------------------------------
# output msg for steps

# I18N: Make venv folder
S_ACTION_VENV = _("Making venv folder")
# I18N: Make venv folder
S_ACTION_REQS = _("Installing requirements")
# I18N: Make git folder
S_ACTION_GIT = _("Making git folder")
# I18N: Make install file
S_ACTION_INST = _("Making install/uninstall files")
# I18N: purge unnecessary files
S_ACTION_PURGE = _("Purging unnecessary files")
# I18N: Make i18n folder
S_ACTION_I18N = _("Making i18n folder")
# I18N: fix other files
S_ACTION_META = _("Fixing metadata")
# I18N: Make placeholder files
S_ACTION_PLACE = _("Fixing placeholder files")
# I18N: install package in own venv
S_ACTION_EDIT = _("Installing package")
# I18N: Make docs folder
S_ACTION_MAKE_DOCS = _("Making docs folder")
# I18N: Make tree file
S_ACTION_TREE = _("Making tree file")
# I18N: freeze venv folder
S_ACTION_FREEZE = _("Freezing venv")
# I18N: Build docs folder
S_ACTION_BAKE_DOCS = _("Baking docs folder")
# I18N: Deploy docs site
S_ACTION_DEPLOY_DOCS = _("Deploying docs site")
# I18N: compress files
S_ACTION_COMPRESS = _("Compressing files")
# I18N: remove dist
S_ACTION_REM_DIST = _("Removing dist source")
# I18N: Copy template files
S_ACTION_COPY = _("Copying template files")
# I18N: Do fix
S_ACTION_FIX = _("Fixing dunders")
# I18N: Make dist folder
S_ACTION_DIST = _("Copying dist files")
# I18N: skipped action
S_ACTION_SKIP = _("Skipped")
# I18N: Done
S_ACTION_DONE = _("Done")
# I18N: Failed
S_ACTION_FAIL = _("Failed")

# ------------------------------------------------------------------------------

# TODO: get these out (not user editable)
# NB: DO NOT DELETE/CHANGE S_KEY_XXX !!!
# ONLY ADD !!!

# keys for pybaker private dict
S_KEY_PRV_ALL = "PRV_ALL"
S_KEY_PRV_PRJ = "PRV_PRJ"

# keys for metadata, blacklist, i18n in pybaker dev dict
S_KEY_PUB_META = "PUB_META"
S_KEY_PUB_BL = "PUB_BL"
S_KEY_PUB_DIST = "PUB_DIST"
S_KEY_PUB_DOCS = "PUB_DOCS"
S_KEY_PUB_I18N = "PUB_I18N"
S_KEY_PUB_INST = "PUB_INST"
S_KEY_PUB_ACT = "PUB_ACT"

# keys for blacklist
S_KEY_SKIP_ALL = "SKIP_ALL"
S_KEY_SKIP_CONTENTS = "SKIP_CONTENTS"
S_KEY_SKIP_HEADER = "SKIP_HEADER"
S_KEY_SKIP_CODE = "SKIP_CODE"
S_KEY_SKIP_TREE = "SKIP_TREE"

# keys for i18n
S_KEY_PUB_I18N_SRC = "SOURCES"
S_KEY_PUB_I18N_DIR = "OUTPUT"
S_KEY_PUB_I18N_TAG = "TAG"
S_KEY_PUB_I18N_CHAR = "CHARSET"
S_KEY_PUB_I18N_CLANGS = "CLANGS"

# keys for D_PUB_ACT
S_KEY_ACT_VENV = "ACT_VENV"
S_KEY_ACT_REQS = "ACT_REQS"
S_KEY_ACT_GIT = "ACT_GIT"
S_KEY_ACT_INST = "ACT_INST"
S_KEY_ACT_PURGE = "ACT_PURGE"
S_KEY_ACT_I18N = "ACT_I18N"
S_KEY_ACT_META = "ACT_META"
S_KEY_ACT_PLACE = "ACT_PLACE"
S_KEY_ACT_EDIT = "ACT_EDIT"
S_KEY_ACT_DOCS_MAKE = "ACT_MAKE_DOCS"
S_KEY_ACT_TREE = "ACT_TREE"
S_KEY_ACT_FREEZE = "ACT_FREEZE"
S_KEY_ACT_DOCS_BAKE = "ACT_BAKE_DOCS"
S_KEY_ACT_DOCS_DEPLOY = "ACT_DEPLOY_DOCS"
S_KEY_ACT_COMPRESS = "ACT_COMPRESS"
S_KEY_ACT_REM_DIST = "ACT_REM_DIST"

# keys for D_PUB_DOCS
S_KEY_DOCS_THEME = "DOCS_THEME"
S_KEY_DOCS_USE_RM = "DOCS_USE_RM"
S_KEY_DOCS_MAKE_API = "DOCS_MAKE_API"
S_KEY_DOCS_DIR_API = "DOCS_DIR_API"

# keys for meta dict
S_KEY_META_SHORT_DESC = "META_SHORT_DESC"
S_KEY_META_VERSION = "META_VERSION"
S_KEY_META_KEYWORDS = "META_KEYWORDS"
S_KEY_META_DEPS = "META_DEPS"
S_KEY_META_CATS = "META_CATS"

# python header/split dict keys
S_KEY_RULES_HASH = "S_KEY_RULES_HASH"
S_KEY_RULES_MARKUP = "S_KEY_RULES_MARKUP"
S_KEY_RULES_DOUBLE_SLASH = "S_KEY_RULES_DS"
S_KEY_RULES_EXT = "S_KEY_RULES_EXT"
S_KEY_RULES_REP = "S_KEY_RULES_REP"
S_KEY_HDR_SCH = "S_KEY_HDR_SCH"
S_KEY_LEAD = "S_KEY_GRP_LEAD"
S_KEY_VAL = "S_KEY_GRP_VAL"
S_KEY_CAPTION_PAD = "S_KEY_GRP_PAD"
S_KEY_SW_SCH = "S_KEY_SW_SCH"
S_KEY_SW_VAL = "S_KEY_SW_VAL"
S_KEY_SW_NAME = "S_KEY_SW_NAME"
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
S_KEY_UNINST_CONT = "UNINST_CONT"
S_KEY_CFG_CONT = "CFG_CONT"

# spinner keys
S_KEY_FRAMES = "S_KEY_FRAMES"
S_KEY_INTERVAL = "S_KEY_INTERVAL"
S_KEY_SKIP = "S_KEY_SKIP"
S_KEY_DONE = "S_KEY_DONE"
S_KEY_FAIL = "S_KEY_FAIL"
S_KEY_RES = "S_KEY_RES"
S_KEY_FG = "S_KEY_FG"

# dir names, relative to PP template, or project dir
# NB: if you change anything in the template structure, you should revisit this
# and make any appropriate changes
S_DIR_TEMPLATE = "template"
S_DIR_ALL = "all"
S_DIR_BIN = "bin"
S_DIR_GIT = ".git"
S_DIR_CONF = "conf"
S_DIR_LOG = "log"
S_DIR_API = "API"
S_DIR_MISC = "misc"
S_DIR_README = "readme"
S_DIR_DOCS = "docs"
S_DIR_SITE = "site"
S_DIR_SRC = "src"
S_DIR_SUPPORT = "support"
S_DIR_TODO = "todo"
S_DIR_UI = "ui"
S_DIR_I18N = "i18n"
S_DIR_IMAGES = "images"
S_DIR_TESTS = "tests"
S_DIR_GUI = "gui"
S_DIR_PYTHON = "python"
S_DIR_DESKTOP = "desktop"
S_DIR_DIST = "dist"
S_DIR_ASSETS = "assets"
S_DIR_INSTALL = "install"
S_DIR_SCRIPTS = "scripts"

# common file names, rel to prj dir or pyplate dir
S_FILE_LICENSE = "LICENSE.txt"
S_FILE_README = "README.md"
S_FILE_INDEX = "index.md"
S_FILE_TOML = "pyproject.toml"
S_FILE_REQS = "requirements.txt"
S_FILE_INST_CFG = "install.json"
S_FILE_INST_PY = "install.py"
S_FILE_UNINST_PY = "uninstall.py"
S_FILE_SCREENSHOT = "screenshot.png"
S_FILE_DSK_TMP = "template.desktop"
S_FILE_DEV_VENV = "develop.py"
S_FILE_INST_PRE = "pre_install.py"
S_FILE_INST_POST = "post_install.py"
S_FILE_UNINST_PRE = "pre_uninstall.py"
S_FILE_UNINST_POST = "post_uninstall.py"
S_FILE_MKDOCS_YML = "mkdocs.yml"

# paths relative to end user home only
S_USR_APPS = ".local/share/applications"  # for .desktop out file
S_USR_BIN = ".local/bin"  # where to put the binary
S_USR_CONF = ".config"  # where to put config files
S_USR_SHARE = ".local/share"  # bulk of the program goes here

# formats for tree
S_TREE_TEXT_NAME = "tree.txt"
S_TREE_TEXT_FILE = f"{S_DIR_MISC}/{S_TREE_TEXT_NAME}"
S_TREE_HTML_NAME = "tree.html"
S_TREE_HTML_FILE = f"{S_DIR_MISC}/{S_TREE_HTML_NAME}"
S_TREE_DIR_FORMAT = " [] $NAME/"
S_TREE_FILE_FORMAT = " [] $NAME"

# switch keys
S_SW_ENABLE = "enable"
S_SW_DISABLE = "disable"
# switch values
S_SW_REPLACE = "replace"

# path to prj pyplate files, relative to prj dir
# NB: leave as string, no start dir yet
S_PRJ_PP_DIR = "pyplate"
S_PRJ_PUB_CFG = f"{S_PRJ_PP_DIR}/project.json"
S_PRJ_PRV_DIR = f"{S_PRJ_PP_DIR}/private"
S_PRJ_PRV_CFG = f"{S_PRJ_PRV_DIR}/private.json"

# spinner stuff

# terminal escape commands
S_HIDE_CURSOR = "\033[?25l"
S_SHOW_CURSOR = "\033[?25h"
S_CLEAR_LINE = "\033[0K"

# message format
# NB: format params are message and frame
S_MSG_FMT = "{}{} "

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

# pot files
S_PO_VER_SCH = r"(\"Project-Id-Version: )(.*?)(\\n\")"
S_PO_VER_REP = r"\g<1>{}\g<3>"
S_PO_LANG_SCH = r"(\"Language: )(.*?)(\\n\")"

# pyproject.toml
S_TOML_VER_SCH = r"(^\s*\[project\]\s*$)(.*?)(^\s*version[\t ]*=[\t ]*)(.*?$)"
S_TOML_VER_REP = r'\g<1>\g<2>\g<3>"{}"'
S_TOML_DESC_SCH = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*description[\t ]*=[\t ]*)(.*?$)"
)
S_TOML_DESC_REP = r'\g<1>\g<2>\g<3>"{}"'
S_TOML_KW_SCH = r"(^\s*\[project\]\s*$)(.*?)(^\s*keywords[\t ]*=[\t ]*)(.*?\])"
S_TOML_KW_REP = r"\g<1>\g<2>\g<3>[{}]"
S_TOML_PKGS_SCH = (
    r"(^\s*\[tool\.setuptools\]\s*$)(.*?)(^\s*packages[\t ]*=[\t ]*)(.*?$)"
)
S_TOML_PKGS_REP = r"\g<1>\g<2>\g<3>{}"

# short desc/version in all files
S_SRC_DESC_SCH = r"(S_PP_SHORT_DESC\s*=.*\")(.*)(\".*\n)"
S_SRC_DESC_REP = r"\g<1>{}\g<3>"
S_SRC_VER_SCH = r"(S_PP_VERSION\s*=.*\")(.*)(\".*)"
S_SRC_VER_REP = r"\g<1>{}\g<3>"

# make sure ver num entered in pybaker is valid
S_SEM_VER_VALID = (
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
S_SEM_VER_PYPRJ = r"\g<1>.\g<2>.\g<3>"

# mkdocs.yml
S_THEME_SCH = r"(theme:)(.*)"
S_THEME_REP = r"\g<1> {}"

# ------------------------------------------------------------------------------
# random stuff

# S_WLANG = "en"
S_ENCODING = "UTF-8"
S_DIST_MODE = "zip"
# I18N: default date format
S_DATE_FMT = _("%m/%d/%Y")
# I18N: def deps
S_DEPS_NONE = _("None")
# default image ext
S_IMG_FMT = "{}.png"

# screenshot path for readme
S_PATH_SCREENSHOT = f"{S_DIR_IMAGES}/{S_FILE_SCREENSHOT}"
# NB: format params are alt text and path to image
S_RM_SCREENSHOT = "![{}]({})"

# fix reqs cmds
S_FILE_REQS_ALL = f"{S_DIR_TEMPLATE}/{S_DIR_ALL}/{S_FILE_REQS}"
# NB: format param is L_TYPES[item][2] (long prj type, subdir in template)
S_FILE_REQS_TYPE = f"{S_DIR_TEMPLATE}/" + "{}/" + f"{S_FILE_REQS}"

# .desktop stuff
S_PATH_DSK_TMP = f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_DESKTOP}/{S_FILE_DSK_TMP}"

# I18N stuff
S_I18N_TAG = "I18N"

# format for venv
# NB: format param is __PP_NAME_PRJ_SMALL__
S_VENV_FMT_NAME = ".venv-{}"
# NB format param is self._dir_venv
S_CMD_CREATE = "python3 -Xfrozen_modules=off -m venv {}"
# NB: format params are venv.parent, venv.name, path to reqs file
S_CMD_INSTALL = "cd {};. {}/bin/activate;python3 -m pip install -r {}"
# NB: format params are venv.parent, venv.name, path to reqs file
S_CMD_FREEZE = (
    "cd {}; "
    ". {}/bin/activate; "
    "python3 -Xfrozen_modules=off -m "
    "pip freeze -l --exclude-editable --require-virtualenv "
    "> {}"
)

# error messages
# NB: format param is dir_prj
S_ERR_NOT_ABS = "Path {} is not absolute"
# NB: format param is dir_prj
S_ERR_NOT_DIR = "Path {} is not a directory"

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

# file exts for do_after_fix
L_EXT_PY = [".py"]
L_EXT_PO = [".po", ".pot"]
L_EXT_DESK = [".desktop"]
L_EXT_GUI = [".ui", ".glade"]

# list of filetypes that use hash (#) for comments
L_EXT_HASH = [
    ".py",
    ".toml",
    ".gitignore",
    ".desktop",
    ".yml",
]

# list of file types to use md/html/xml comments (<!-- ... -->)
L_EXT_MARKUP = [
    ".md",
    ".html",
    ".xml",
    ".ui",
    ".glade",
]

# list of filetypes that have c type comments
L_EXT_DOUBLE_SLASH = [
    ".json",
    ".jsonc",
]

# prj type(s) for making an install.json
L_APP_INSTALL = [
    "c",
    "g",
]

# prj type(s) to install in own venv (packages mostly)
L_INST_SELF = ["p"]

# (short) prj types for making i18n stuff
L_MAKE_I18N = ["c", "g", "p"]

# prj type(s) for making screenshot in README
L_SCREENSHOT = ["g"]

# if in list, use S_DIR_SRC, else use __PP_NAME_PRJ_SMALL__
L_TOML_USE_SRC = ["c", "g"]

# files to remove from dist after bake is done
L_PURGE_DIST = [f"**/{S_PH_NAME}", "**/__pycache__", f"**/{S_FILE_DSK_TMP}"]

# skip placeholder files in these dirs
L_PH_SKIP = [S_DIR_GIT, ".venv*"]

# remove exts from bin files
L_DIST_REMOVE_EXT = [f"{S_DIR_ASSETS}/{S_DIR_BIN}/*.py"]

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
    # --------------------------------------------------------------------------
    # the author name, used in headers and pyproject.toml
    "__PP_AUTHOR__": S_AUTHOR,
    # the author's email, used in headers and pyproject.toml
    "__PP_EMAIL__": S_EMAIL,
    # the base url for all projects, used in pyproject.toml and GUI about dlg
    "__PP_URL__": S_URL,
    # the license name, used in headers and pyproject.toml
    "__PP_LICENSE_NAME__": S_LICENSE_NAME,
    # the license url, used in gui about dialog
    "__PP_LICENSE_URL__": S_LICENSE_URL,
    # the license badge to use in README.md
    "__PP_RM_LICENSE__": S_RM_LICENSE,
    # ------------------------------------------------------------------------------
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
    "__PP_DIR_ASSETS__": S_DIR_ASSETS,
    # --------------------------------------------------------------------------
    # these paths are relative to the dev's prj name
    # i.e. /home/user/Projects/Python/MyProject
    "__PP_DIR_CONF__": S_DIR_CONF,
    "__PP_DIR_LOG__": S_DIR_LOG,
    "__PP_DIR_SRC__": S_DIR_SRC,
    # NB: do not change "locale" (hard coded into cnpot)
    "__PP_DIR_LOCALE__": f"{S_DIR_I18N}/locale",
    "__PP_DIR_DIST__": S_DIR_DIST,
    "__PP_DIR_BIN__": S_DIR_BIN,
    "__PP_DIR_MISC__": S_DIR_MISC,
    "__PP_DIR_TESTS__": S_DIR_TESTS,
    # --------------------------------------------------------------------------
    # these paths are relative to the user's home dir
    "__PP_USR_APPS__": S_USR_APPS,  # /home/user/.local/applications
    "__PP_USR_BIN__": S_USR_BIN,  # /home/user/.local/bin
    "__PP_USR_CONF__": S_USR_CONF,  # /home/user/.config
    "__PP_NAME_DSK_TMP__": S_FILE_DSK_TMP,
    "__PP_NAME_UNINST__": S_FILE_UNINST_PY,
    # --------------------------------------------------------------------------
    # gui stuff
    "__PP_DIR_GUI__": f"{S_DIR_SRC}/{S_DIR_GUI}",
    "__PP_DIR_UI__": f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_UI}",
    "__PP_DIR_GUI_SRC__": f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_PYTHON}",
    "__PP_DIR_DESK__": f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_DESKTOP}",
    "__PP_FILE_DLG__": S_DLG_UI_FILE,
    "__PP_DLG_ABOUT__": S_DLG_ABOUT,
    # --------------------------------------------------------------------------
    # install stuff
    "__PP_DIR_INSTALL__": S_DIR_INSTALL,
    "__PP_DIR_SCRIPTS__": S_DIR_SCRIPTS,
    "__PP_FILE_INST_CFG__": S_FILE_INST_CFG,
    "__PP_INST_PRE__": S_FILE_INST_PRE,
    "__PP_INST_POST__": S_FILE_INST_POST,
    "__PP_UNINST_PRE__": S_FILE_UNINST_PRE,
    "__PP_UNINST_POST__": S_FILE_UNINST_POST,
    # --------------------------------------------------------------------------
    # mkdocs stuff
    "__PP_DIR_DOCS__": S_DIR_DOCS,
    "__PP_DIR_SITE__": S_DIR_SITE,
}

# TODO: get these out (not user editable)
# these are settings that will be calculated for you while running pymaker.py
# consider them the "each project" settings
# they are used for an individual project, and should not be changed after a
# project is created, as pybaker.py will not update them

# DO NOT use dunders in the values here, they will not be fixed

# if you need to adjust any of these values based on a dunder, use
# do_before_fix() in the hooks.py file
D_PRV_PRJ = {
    "__PP_VERSION_PP__": "",  # version of pp we are using
    # --------------------------------------------------------------------------
    # get_project_info
    "__PP_TYPE_PRJ__": "",  # 'c'
    "__PP_NAME_PRJ__": "",  # My Project
    "__PP_NAME_PRJ_BIG__": "",  # My_Project
    "__PP_NAME_PRJ_SMALL__": "",  # my_project
    "__PP_NAME_PRJ_PASCAL__": "",  # MyProject
    "__PP_NAME_SEC_BIG__": "",  # My_Win
    "__PP_NAME_SEC_SMALL__": "",  # my_win
    "__PP_NAME_SEC_PASCAL__": "",  # MyWin
    "__PP_NAME_VENV__": "",  # venv folder name
    # --------------------------------------------------------------------------
    # do_before_fix
    # NB: interesting side effect: this does not change unless pybaker passes
    "__PP_DATE__": "",  # the date each file was created, updated every time
    # --------------------------------------------------------------------------
    # gui stuff
    "__PP_FILE_APP__": "",  # my_project_app
    "__PP_CLASS_APP__": "",  # MyProjectApp
    "__PP_FILE_WIN__": "",  # my_project_win
    "__PP_CLASS_WIN__": "",  # MyProjectWin
    "__PP_APP_ID__": "",
    # --------------------------------------------------------------------------
    # folders
    "__PP_USR_INST__": "",  # /home/user/.local/share/app_name
    # --------------------------------------------------------------------------
    # files
    "__PP_FILE_DESK__": "",  # final desk file, not template
    # --------------------------------------------------------------------------
    # images
    "__PP_IMG_README__": "",  # image for readme file logo
    "__PP_IMG_DESK__": "",  # image for .desktop logo
    "__PP_IMG_DASH__": "",  # image for dash/win logo
    "__PP_IMG_ABOUT__": "",  # image for about logo
    # --------------------------------------------------------------------------
    # NB: technically this should be metadata but we don't want dev editing,
    # only use metadata to recalculate these on every build
    "__PP_VER_MMR__": "",  # semantic version string, ie. "0.0.13"
    "__PP_VER_DISP__": "",  # formatted version string, ie. "Version 0.0.1"
    "__PP_FMT_DIST__": "",
    "__PP_DEV_INST__": "",  # develop.py to install reqs or self/reqs
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
    S_KEY_META_DEPS: {"Python 3.14+": "https://python.org"},
    # the categories to use in .desktop for gui apps (found in pybaker_conf.py)
    S_KEY_META_CATS: [],
}

# the lists of dirs/files we don't mess with while running pymaker
# each item can be a path relative to the project directory, or a glob
# NB: you can use dunders here since the path is the last thing to get fixed
# these dir/file names should match what's in the template dir (before any
# modifications, hence using dunder keys)
D_PUB_BL = {
    # skip header, skip text, skip path (0 0 0)
    # NB: this is mostly to speed up processing by not even looking at them
    S_KEY_SKIP_ALL: [
        S_DIR_GIT,
        ".venv*",
        ".VSCodeCounter",
        "*.code-workspace",
        S_DIR_DIST,
        S_DIR_DOCS,
        S_DIR_I18N,
        S_DIR_MISC,
        S_DIR_SITE,
        S_DIR_TODO,
        S_FILE_LICENSE,
        S_FILE_REQS,
        "**/__pycache__",
        "**/*.egg-info",
        S_PRJ_PP_DIR,
    ],
    # skip header, skip text, fix path (0 0 1)
    # NB: this is used mostly for non-text files
    S_KEY_SKIP_CONTENTS: [
        "**/*.png",
        "**/*.jpg",
        "**/*.jpeg",
        "**/*.ico",
    ],
    # skip header, fix text, fix path (0 1 1)
    S_KEY_SKIP_HEADER: [],
    # fix header, skip text, fix path (1 0 1)
    S_KEY_SKIP_CODE: [
        S_DIR_CONF,
    ],
    # list of dirs/files to ignore in output dir when creating the initial tree
    S_KEY_SKIP_TREE: [
        S_DIR_GIT,
        ".venv*",
        ".VSCodeCounter",
        S_DIR_DIST,
        S_DIR_SITE,
        S_DIR_DOCS,
        "**/__pycache__",
        "**/*.egg-info",
    ],
}

# dict of files to put in dist folder (defaults, written by pymaker, edited by
# hand, read by pybaker)
# NB: tbd by do_after_template based on prj type
D_PUB_DIST = {}

# mkdocs settings
D_PUB_DOCS = {
    S_KEY_DOCS_THEME: "readthedocs",  # "readthedocs", "" (default), etc.
    S_KEY_DOCS_USE_RM: False,  # initially use dummy file
    S_KEY_DOCS_MAKE_API: True,
    S_KEY_DOCS_DIR_API: [],  # tbd by do_after_template
}

# cnpot settings
D_PUB_I18N = {
    # list of sources per domain
    S_KEY_PUB_I18N_SRC: [],  # tbd by do_after_template
    S_KEY_PUB_I18N_DIR: S_DIR_I18N,
    S_KEY_PUB_I18N_TAG: S_I18N_TAG,
    # default charset for .pot/.po files
    S_KEY_PUB_I18N_CHAR: S_ENCODING,
    # computer languages
    S_KEY_PUB_I18N_CLANGS: {
        "Python": L_EXT_PY,
        "Glade": L_EXT_GUI,
        "Desktop": L_EXT_DESK,
    },
}

# default dict for install/uninstall
# NB: tbd by do_after_template based on prj type
D_PUB_INST = {}

# initial dict in project to control baking
# NB: this is what goes into a project's 'project.json' file  when it is
# created by pymaker and that dict controls a particular project when baking
# all values should be True unless you have a good reason (such as, you will
# never need a .git folder or a venv, or you don't use documentation tools, or
# i18n tools, etc.)
# remember that this dict is only read by pybaker AFTER the project has been
# created. to change the actions tha pymaker uses, see D_PM_ACT in pymaker.py.
D_PUB_ACT = {
    S_KEY_ACT_VENV: True,
    S_KEY_ACT_REQS: True,
    S_KEY_ACT_GIT: True,
    S_KEY_ACT_INST: True,
    S_KEY_ACT_PURGE: True,
    S_KEY_ACT_I18N: True,
    S_KEY_ACT_META: True,
    S_KEY_ACT_PLACE: True,
    S_KEY_ACT_EDIT: True,
    S_KEY_ACT_DOCS_MAKE: True,
    S_KEY_ACT_TREE: True,
    S_KEY_ACT_FREEZE: True,
    S_KEY_ACT_DOCS_BAKE: True,
    S_KEY_ACT_DOCS_DEPLOY: True,
    S_KEY_ACT_COMPRESS: True,
    S_KEY_ACT_REM_DIST: True,
}

# ------------------------------------------------------------------------------
# Other dictionaries
# ------------------------------------------------------------------------------

# dict of files that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project itself (not the
# template), it gets copied to the project, and cuts down on duplicate files
# key is the relative path to the source file/dir in PyPlate
# val is the relative path to the dest file/dir in the project dir
D_COPY = {f"{S_DIR_MISC}": f"{S_DIR_MISC}"}

# NB: key is src, rel to prj dir
# NB: val is dst, rel to dist dir
D_TYPE_DIST = {
    "c": {
        # basic stuff (put in assets folder)
        S_DIR_BIN: S_DIR_ASSETS,
        S_DIR_CONF: S_DIR_ASSETS,
        S_DIR_I18N: S_DIR_ASSETS,
        S_DIR_IMAGES: S_DIR_ASSETS,
        S_DIR_INSTALL: S_DIR_ASSETS,
        S_DIR_SRC: S_DIR_ASSETS,
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
        S_FILE_REQS: f"{S_DIR_ASSETS}/{S_DIR_INSTALL}",
    },
    "p": {
        # basic stuff (put at top level)
        "__PP_NAME_PRJ_SMALL__": "",
        S_FILE_TOML: "",
    },
}

# dictionary of default stuff to put in install.json
# NB: in S_KEY_INST_CONT, key is rel to assets, val is rel to home
D_TYPE_INST = {
    "c": {
        S_KEY_INST_NAME: "__PP_NAME_PRJ_BIG__",
        S_KEY_INST_VER: "__PP_VER_MMR__",
        S_KEY_INST_DESK: False,
        S_KEY_INST_CONT: {
            f"{S_DIR_BIN}/__PP_NAME_PRJ_SMALL__": "__PP_USR_BIN__",
            S_DIR_I18N: "__PP_USR_INST__",
            S_DIR_IMAGES: "__PP_USR_INST__",
            S_DIR_INSTALL: "__PP_USR_INST__",
            S_DIR_SRC: "__PP_USR_INST__",
            S_FILE_UNINST_PY: "__PP_USR_INST__",
        },
        S_KEY_UNINST_CONT: [
            "__PP_USR_BIN__/__PP_NAME_PRJ_SMALL__",
            "__PP_USR_INST__",
        ],
        S_KEY_CFG_CONT: {
            S_DIR_CONF: "__PP_USR_CONF__/__PP_NAME_PRJ_SMALL__",
        },
    },
    "g": {
        S_KEY_INST_NAME: "__PP_NAME_PRJ_BIG__",
        S_KEY_INST_VER: "__PP_VER_MMR__",
        S_KEY_INST_DESK: True,
        S_KEY_INST_CONT: {
            f"{S_DIR_BIN}/__PP_NAME_PRJ_SMALL__": "__PP_USR_BIN__",
            S_DIR_I18N: "__PP_USR_INST__",
            S_DIR_IMAGES: "__PP_USR_INST__",
            S_DIR_INSTALL: "__PP_USR_INST__",
            S_DIR_SRC: "__PP_USR_INST__",
            S_FILE_UNINST_PY: "__PP_USR_INST__",
            # NB: extra for gui
            "__PP_FILE_DESK__": "__PP_USR_APPS__",
        },
        S_KEY_UNINST_CONT: [
            "__PP_USR_BIN__/__PP_NAME_PRJ_SMALL__",
            "__PP_USR_INST__",
            # NB: extra for gui
            "__PP_USR_APPS__/__PP_NAME_PRJ_BIG__.desktop",
        ],
        S_KEY_CFG_CONT: {
            S_DIR_CONF: "__PP_USR_CONF__/__PP_NAME_PRJ_SMALL__",
        },
    },
}

# list of i18n files/folders per prj type
D_TYPE_I18N = {
    "c": {
        S_KEY_PUB_I18N_SRC: [
            S_DIR_BIN,
            S_DIR_INSTALL,
            S_DIR_SRC,
            S_FILE_DEV_VENV,
        ],
    },
    "g": {
        S_KEY_PUB_I18N_SRC: [
            S_DIR_BIN,
            S_DIR_INSTALL,
            S_DIR_SRC,
            S_FILE_DEV_VENV,
        ],
    },
    "p": {
        S_KEY_PUB_I18N_SRC: [
            "__PP_NAME_PRJ_SMALL__",
            S_FILE_DEV_VENV,
        ],
    },
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
            S_KEY_CAPTION_PAD: 3,
            # code stuff
            # NB: match first occurrence of unquoted marker to end of line
            S_KEY_SPLIT: r"[\'\"].*?[\'\"]|(#.*)",
            S_KEY_SPLIT_COMM: 1,
            # switch stuff
            S_KEY_SW_SCH: r"pyplate\s*:\s*(\S*)\s*=\s*(\S*)",
            S_KEY_SW_VAL: 1,
            S_KEY_SW_NAME: 2,
        },
    },
    S_KEY_RULES_MARKUP: {
        S_KEY_RULES_EXT: L_EXT_MARKUP,
        S_KEY_RULES_REP: {
            # header stuff
            S_KEY_HDR_SCH: r"^(\s*<!--\s*\S*\s*:\s*)(\S+)(.*-->.*)$",
            S_KEY_LEAD: 1,
            S_KEY_VAL: 2,
            S_KEY_CAPTION_PAD: 3,
        },
    },
    S_KEY_RULES_DOUBLE_SLASH: {
        S_KEY_RULES_EXT: L_EXT_DOUBLE_SLASH,
        S_KEY_RULES_REP: {
            # header stuff
            S_KEY_HDR_SCH: r"^(\s*//\s*\S*\s*:\s*)(\S+)(.*)$",
            S_KEY_LEAD: 1,
            S_KEY_VAL: 2,
            S_KEY_CAPTION_PAD: 3,
        },
    },
}

# the type of projects that will ask for a second name
D_NAME_SEC = {
    "p": S_ASK_SEC_P,
    "g": S_ASK_SEC_G,
}

# map switch val strs to actual vals (i.e. "enable": True, "disable": False)
D_SWITCH_VALS = {
    S_SW_ENABLE: True,
    S_SW_DISABLE: False,
}

# default dict of switches
# NB: key should be switch name (e.g. "replace" or S_SW_REPLACE)
# NB: value should be True if present and enabled, False if present and
# disabled, or this (default) if not present
D_SWITCH_DEF = {
    S_SW_REPLACE: True,  # assume we want to replace
}

# regex's to match project name
D_NAME = {
    S_KEY_NAME_START: r"(^[a-zA-Z])",
    S_KEY_NAME_END: r"([a-zA-Z\d]$)",
    S_KEY_NAME_MID: r"(^[a-zA-Z\d\-_ ]*$)",
}

# dirs to remove after the project is fixed by either pm or pb
D_PURGE_MAKE = {
    "p": [
        S_DIR_BIN,
        S_DIR_CONF,
        S_DIR_LOG,
        S_DIR_INSTALL,
        S_DIR_SRC,
    ]
}

# where to search for docs api
D_DOCS_DIR_API = {
    "c": [S_DIR_SRC],
    "g": [S_DIR_SRC],
    "p": ["__PP_NAME_PRJ_SMALL__"],
}

# ------------------------------------------------------------------------------
# spinner stuff

# settings for spinner
D_SPIN = {
    S_KEY_FRAMES: ["", ".", "..", "..."],
    S_KEY_INTERVAL: 0.5,
    S_KEY_SKIP: {
        S_KEY_RES: S_ACTION_SKIP,
        S_KEY_FG: cnfunctions.C_FG_YELLOW
    },
    S_KEY_DONE: {
        S_KEY_RES: S_ACTION_DONE,
        S_KEY_FG: cnfunctions.C_FG_GREEN
    },
    S_KEY_FAIL: {
        S_KEY_RES: S_ACTION_FAIL,
        S_KEY_FG: cnfunctions.C_FG_RED
    }
}

# -)
