# ------------------------------------------------------------------------------
# Project : __PC_NAME_BIG__                                        /          \
# Filename: default_class.py                                      |     ()     |
# Date    : __PC_DATE__                                           |            |
# Author  : __PD_AUTHOR__                                         |   \____/   |
# License : __PD_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
docstring
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# NB: this is an example of how to use cnlibs

# # system imports
# import sys

# # pylint: disable=wrong-import-position
# # pylint: disable=wrong-import-order
# # pylint: disable=no-name-in-module
# # pylint: disable=import-error

# # my imports
# # add custom import paths

# # add lib path to import search
# DIR_LIB = "__PC_USR_LIB__"
# sys.path.append(str(DIR_LIB))

# from cnlib import cnfunctions as F  # type: ignore
# from cnlib.cnformatter import CNFormatter  # type: ignore

# # pylint: enable=wrong-import-position
# # pylint: enable=wrong-import-order
# # pylint: enable=no-name-in-module
# # pylint: enable=import-error

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
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
class Main:
    """
    Short description

    Public methods:
        set_zaz(new_zaz): Sets the new value of _zaz
        get_zaz(): Gets the current value of _zaz

    Long description (including HTML).
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the new object

        Initializes a new instance of the class, setting the default values
        of its properties, and any other code that needs to run to create a
        new object.
        """

        # call super init to initialize the base class
        super().__init__()

        # set the initial value of class
        self._zaz = "zaz"

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Gets the current value of zaz
    # --------------------------------------------------------------------------
    def get_zaz(self):
        """
        Gets the current value of zaz

        Returns:
            The current value of zaz

        Long description (including HTML).
        """

        # print return value
        print(f"public get_zaz: {self._zaz}")

        # return the current value of zaz
        return self._zaz

    # --------------------------------------------------------------------------
    # Sets the new value of zaz
    # --------------------------------------------------------------------------
    def set_zaz(self, new_zaz):
        """
        Sets the new value of zaz

        Arguments:
            new_zaz: The new value of zaz

        Long description (including HTML).
        """

        # print new value
        print(f"public set_zaz: {new_zaz}")

        # set the new value of zaz
        self._zaz = new_zaz


# -)
