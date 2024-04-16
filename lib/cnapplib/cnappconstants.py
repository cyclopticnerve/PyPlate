# ------------------------------------------------------------------------------
# Project : CNAppLib                                               /          \
# Filename: cnappconstants.py                                     |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
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

# top level app keys
KEY_APP_ID = "KEY_APP_ID"
KEY_APP_LOCALE = "KEY_APP_LOCALE"
KEY_APP_CLASSES = "KEY_APP_CLASSES"
KEY_APP_WINDOWS = "KEY_APP_WINDOWS"

# values for CLOSE_ACTION
# don't save values, just close
CLOSE_ACTION_CANCEL = "CLOSE_ACTION_CANCEL"
# save values and close
CLOSE_ACTION_SAVE = "CLOSE_ACTION_SAVE"
# show dialog
CLOSE_ACTION_ASK = "CLOSE_ACTION_ASK"

# window class keys
KEY_CLS_UI_FILE = "KEY_CLS_UI_FILE"
KEY_CLS_UI_NAME = "KEY_CLS_UI_NAME"
KEY_CLS_HANDLER = "KEY_CLS_HANDLER"
KEY_CLS_CLOSE_ACTION = "KEY_CLS_CLOSE_ACTION"
KEY_CLS_SHOW_MOD = "KEY_CLS_SHOW_MOD"
KEY_CLS_MOD_CHAR = "KEY_CLS_MOD_CHAR"
KEY_CLS_MOD_FMT = "KEY_CLS_MOD_FMT"
KEY_CLS_CTLS = "KEY_CLS_CTLS"

# window instance keys
KEY_WIN_CLASS = "KEY_WIN_CLASS"
KEY_WIN_VISIBLE = "KEY_WIN_VISIBLE"
KEY_WIN_SIZE = "KEY_WIN_SIZE"
KEY_WIN_CTLS = "KEY_WIN_CTLS"

# window size keys
KEY_SIZE_W = "KEY_SIZE_W"
KEY_SIZE_H = "KEY_SIZE_H"
KEY_SIZE_M = "KEY_SIZE_M"

# window control keys
KEY_CTL_TYPE = "KEY_CTL_TYPE"
KEY_CTL_VAL = "KEY_CTL_VAL"
KEY_CTL_SET = "KEY_CTL_SET"
KEY_CTL_GET = "KEY_CTL_GET"
KEY_CTL_VAL_TYPE = "KEY_CTL_VAL_TYPE"

# value types to convert in _sanitize_user
CTL_VAL_TYPE_INT = "CTL_VAL_TYPE_INT"
CTL_VAL_TYPE_BOOL = "CTL_VAL_TYPE_BOOL"

# ------------------------------------------------------------------------------

# NB: add new control types here
# used to collate set/get functions and value types
# NB: value type defaults to text, no conversion
# if value type should be int or bool, set KEY_CTL_VAL_TYPE accordingly
# this key/value is used by _sanitize_user to ensure proper type, in case
# somebody borks the entry in the config file by hand

# all text entries use the same set/get functions
CTL_TYPE_TEXT = {
    KEY_CTL_SET: "set_text",
    KEY_CTL_GET: "get_text",
}

# all checkboxes use the same set/get functions and value type
CTL_TYPE_CHECK = {
    KEY_CTL_SET: "set_active",
    KEY_CTL_GET: "get_active",
    KEY_CTL_VAL_TYPE: CTL_VAL_TYPE_BOOL,
}

# ------------------------------------------------------------------------------
# Defaults
# ------------------------------------------------------------------------------

DEF_CLOSE_ACTION = CLOSE_ACTION_ASK
DEF_CLS_SHOW_MOD = True
DEF_CLS_MOD_CHAR = "\u29BF"
DEF_CLS_MOD_FMT = "${MOD} ${TITLE}]"
DEF_WIN_VISIBLE = True

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# strings to be localized
# I18N: the main message of the save dialog
STR_CLOSE_DLG_MAIN = _("Save changes before closing?")
# I18N: the sub message of the save dialog
STR_CLOSE_DLG_SEC = _("If you don't save, changes will be permanently lost.")
# I18N: the destructive button label (to close without saving)
STR_CLOSE_DLG_CLOSE = _("Close without saving")
# I18N: the cancel button label (to do nothing)
STR_CLOSE_DLG_CANCEL = _("Cancel")
# I18N: the save button label (to save and close)
STR_CLOSE_DLG_SAVE = _("Save")
# I18N: the save button label when the document is untitled (to save and close)
STR_CLOSE_DLG_SAVE_AS = _("Save As...")

# -)
