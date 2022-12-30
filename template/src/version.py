# ------------------------------------------------------------------------------
# Project : __CN_BIG_NAME__                                        /          \
# Filename: version.py                                            |     ()     |
# Date    : __CN_DATE                                             |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
    Single canonical version number
"""

__version__ = '__CN_VERSION__'


# ------------------------------------------------------------------------------
# Returns the canonical version number of this project
# ------------------------------------------------------------------------------
def get_version():

    """
        Returns the canonical version number of this project

        This is the canonical (only and absolute) version number string for this
        project. This should provide the absolute version number string (in
        semantic notation) of this project, and all other version numbers should
        be superceded by this string.
    """

    return __version__

# -)
