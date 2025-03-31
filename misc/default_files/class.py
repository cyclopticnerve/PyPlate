# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename:                                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
docstring
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
class Main:
    """
    Short description

    Methods:
        set_zaz(new_zaz): Sets the new value of _zaz
        get_zaz(): Gets the current value of _zaz

    Long description (including HTML).
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

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

        # create a property and set the initial value
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

        Args:
            var_name: Description

        Returns:
            Description

        Raises:
            exception_type(vars): Description

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

        Args:
            new_zaz: The new value of zaz

        Returns:
            None: none
        
        Raises:
            None: none

        Long description (including HTML).
        """

        # print new value
        print(f"public set_zaz: {new_zaz}")

        # set the new value of zaz
        self._zaz = new_zaz


# -)
