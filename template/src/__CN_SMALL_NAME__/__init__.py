# ------------------------------------------------------------------------------
# Project : __CN_BIG_NAME__                                        /          \
# Filename: __init__.py                                           |     ()     |
# Date    : __CN_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# this file is only for package projects (multiple modules)

"""
    __CN_SHORT_DESC__

    Modules:
        ...
"""

__version__ = '__CN_VERSION__'

print('this is the (pkg) __CN_SMALL_NAME__/__init__.py file')

# import all modules in package to get full dot notation from package import
# from <package> imoport <module>
# TODO: fix these names
from __CN_SMALL_NAME__ import mod_name_1 # noqa W0611 (unused import)
from __CN_SMALL_NAME__ import mod_name_2 # noqa W0611 (unused import)

# from <package_name> import *
# TODO: fix these names
__all__ = ['mod_name_1', 'mod_name_2']  # ['module_name', ...]

# -)
