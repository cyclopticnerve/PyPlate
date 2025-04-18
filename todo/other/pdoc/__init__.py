# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __init__.py                                           |     ()     |
# Date    : 01/11/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module specifies folders to ignore while generating pdoc3 documentation.
This will be automated in a future release.
"""

# TODO: walk top level and exclude everything
# then add includes as needed

# dunder to specify ignored dirs/modules
__pdoc__ = {
    "__PP_NAME_PRJ_BIG__.install": False,
    "__PP_NAME_PRJ_BIG__.lib": False,
    "__PP_NAME_PRJ_BIG__.misc": False,
    "__PP_NAME_PRJ_BIG__.pyplate": False,
    "__PP_NAME_PRJ_BIG__.tests": False,
    "__PP_NAME_PRJ_BIG__.uninstall": False,
}

# -)
