# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnformatter.py                                        |     ()     |
# Date    : 03/22/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A dummy class to combine multiple argparse formatters
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A dummy class to combine multiple argparse formatters
# ------------------------------------------------------------------------------
class CNFormatter(
    argparse.RawTextHelpFormatter, argparse.RawDescriptionHelpFormatter
):
    """
    A dummy class to combine multiple argparse formatters

    Args:
        RawTextHelpFormatter: Maintains whitespace for all sorts of help text,
        including argument descriptions.
        RawDescriptionHelpFormatter: Indicates that description and epilog are
        already correctly formatted and should not be line-wrapped.

    A dummy class to combine multiple argparse formatters.
    """


# -)
