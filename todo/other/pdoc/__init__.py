# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
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
    "PyPlate.install": False,
    "PyPlate.lib": False,
    "PyPlate.misc": False,
    "PyPlate.pyplate": False,
    "PyPlate.tests": False,
    "PyPlate.uninstall": False,
}

# -)
