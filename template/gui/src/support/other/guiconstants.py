# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: guiconstants.py                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
A file to hold constants for the rest of the application
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext

# ------------------------------------------------------------------------------
# Macros
# ------------------------------------------------------------------------------

_ = gettext.gettext

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# class constants
# name of window in ui file
CLS_UI_NAME = "win_main"

# window constants
# class of window in DICT_APP
WIN_MAIN_CLASS = "win_main_class"
# name of a window instance
WIN_MAIN_INST = "win_main_instance"

# control names
WIN_MAIN_ENTRY_TEST = "entry_test"
WIN_MAIN_CHECK_TEST = "check_test"

# the name for the about dialog
DLG_ABOUT = "dlg_about"

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# config load/save error strings
S_GUI_ERR_EXIST = _("load config: config file '{}' does not exist")
S_GUI_ERR_VALID = _("load config: config file '{}' is not a valid JSON file")
S_GUI_ERR_CREATE = _("save config: config file '{}' could not be created")

# -)
