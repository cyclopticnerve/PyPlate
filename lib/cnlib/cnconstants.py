# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnconstants.py                                        |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A file to hold constants for the rest of the library
"""

# TODO: do we ever localize this?

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

# ------------------------------------------------------------------------------
# cnpot constants

# default locale dir under src
POT_DEF_DIR_LOCALE = "locale"
# default po dir under src
POT_DEF_DIR_PO = "po"
# default encoding for .pot and .po files
POT_DEF_CHARSET = "UTF-8"

# this is the default subdir for GNU
# NB: DO NOT CHANGE THIS! i only put it here because it is a string
POT_DIR_MESSAGES = "LC_MESSAGES"
# the file to store all wlangs for bulk operations
# NB: DO NOT CHANGE THIS! i only put it here because it is a string
POT_FILE_LINGUAS = "LINGUAS"

# ------------------------------------------------------------------------------
# cntree constants

# console/terminal values for the individual prefix/connector chars
TREE_CHAR_VERT = "\u2502"  # vertical join (pipe)
TREE_CHAR_HORZ = "\u2500"  # horizontal join (full-width dash)
TREE_CHAR_TEE = "\u251C"  # tee join (not last item)
TREE_CHAR_ELL = "\u2514"  # elbow join (last item)
TREE_CHAR_SPACE = " "  # single space char

# char sequences for the prefix/connector char sets
# NB: these must always be equal length
TREE_PREFIX_VERT = f"{TREE_CHAR_VERT}{TREE_CHAR_SPACE}"  # next level ("| ")
TREE_PREFIX_NONE = f"{TREE_CHAR_SPACE}{TREE_CHAR_SPACE}"  # skip level ("  ")
TREE_CONNECTOR_TEE = f"{TREE_CHAR_TEE}{TREE_CHAR_HORZ}"  # next sub item ("T-")
TREE_CONNECTOR_ELL = f"{TREE_CHAR_ELL}{TREE_CHAR_HORZ}"  # last sub item ("L-")

# the default directory/file name formats
# NB: NAME alone is used for the top level directory name
# DIR is used for subdirectories and should have a leading space to separate it
# from the prefix and/or connector
# FILE has the same purpose as DIR, but for files (DUH!)
TREE_DEF_FORMAT_NAME = "$NAME"
TREE_DEF_FORMAT_DIR = f" {TREE_DEF_FORMAT_NAME}/"
TREE_DEF_FORMAT_FILE = f" {TREE_DEF_FORMAT_NAME}"

# custom error strings
# I18N: the specified value is not a directory
TREE_ERR_NOT_A_DIR = _('"{}" is not a directory')

# custom sorting order
TREE_SORT_ORDER = "_."  # sort first char of name in this order (above ord)

# config load/save error strings
CFG_ERR_NOT_EXIST = _("config file '{}' does not exist")
CFG_ERR_NOT_VALID = _("config file '{}' is not a valid JSON file")
CFG_ERR_NOT_CREATE = _("config file '{}' could not be created")

# config option strings
S_CFG_OPTION = "-c"
S_CFG_DEST = "CFG_DEST"
S_CFG_HELP = _("load configuration from file")
S_CFG_METAVAR = "FILE"

# debug option strings
S_DBG_OPTION = "-d"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP =_( "enable debugging option")

# -)
