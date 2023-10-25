# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: default_class.py                                      |     ()     |
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

# system imports

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Class
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
class Main(object):
    """
    Short description

    Properties:
        zaz: A type to hold the zaz value

    Methods:
        set_zaz(new_zaz): Sets the new value of zaz
        get_zaz(): Gets the current value of zaz

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

        # NB: something i learned the hard way from c++ coding: you want to do
        # AS LITTLE coding in the constructor method because the whole class may
        # not exist at this point! you should definitely not call get/set
        # methods to init controls. these methods/controls may not exist at the
        # time you call them. so to initialize scalar properties, set them
        # empirically rather than using setter methods.

        # set the initial value of class
        self.zaz = "zaz"

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

        # return the current value of zaz
        return f"this is public: {self.zaz}"

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

        # set the new value of zaz
        self.zaz = new_zaz

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Short description
    # --------------------------------------------------------------------------
    def _zaz(self):
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

        return f"this is private: {self.zaz}"


# -)
