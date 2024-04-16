# ------------------------------------------------------------------------------
# Project : __PC_NAME_BIG__                                        /          \
# Filename: __PC_NAME_MOD__.py                                    |     ()     |
# Date    : __PC_DATE__                                           |            |
# Author  : __PD_AUTHOR__                                         |   \____/   |
# License : __PD_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
__PM_SHORT_DESC__
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# NB: this is an example of how to use cnlibs in a package project

# system imports
from pathlib import Path
import sys

# pylint: disable=wrong-import-position

# my imports
# add custom import paths

# find paths to dev or user
DIR_PARENT = Path(__file__).parents[1]
if DIR_PARENT.name == "__PD_DEV_SRC__":
    DIR_LIB = "__PD_DEV_LIB__"
else:
    DIR_LIB = Path.home() / "__PC_USR_LIB__"

# add lib path to import search
sys.path.append(str(DIR_LIB))

from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
def func():
    """
    Short description

    Arguments:
        var_name: Description

    Returns:
        Description

    Raises:
        exception_type(vars): Description

    Long description (including HTML).
    """

    # test out using cnlib
    dict_test = {"foo": "bar"}
    F.pp(dict_test)

    # do the thing
    print("this is func")
    return _func()


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
def _func():
    """
    Short description

    Arguments:
        var_name: Description

    Returns:
        Description

    Raises:
        exception_type(vars): Description

    Long description (including HTML).
    """

    return "this is _func"


# -)
