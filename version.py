# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: version.py                                            |     ()     |
# Date    : 12/22/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
    Single canonical version number
"""

__version__ = '0.1.0'


# ------------------------------------------------------------------------------
# Returns the canonical version number of this project
# ------------------------------------------------------------------------------
def get_version():

    """
        Returns the canonical version number of this project

        This is the canonical (only and absolute) version number string for this
        project. This sjould provide the absolute version number string (in
        semantic notation) of this project, and all other version numbers should
        be superceded by this string.
    """

    return __version__

# -)
