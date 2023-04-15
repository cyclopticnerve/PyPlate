# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: empty_class.py                                        |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

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
class Main:
    """
        Short description

        Properties:
            foo [string]: a string to hold the foo value

        Methods:
            set_foo(foo [str]): sets the new value of foo
            [str] get_foo(): gets the current value of foo

        Long description.
    """

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Sets the new value of foo
    # --------------------------------------------------------------------------
    def set_foo(self, foo):
        """
            Sets the new value of foo

            Paramaters:
                foo [str]: the new value of foo

            Long description.
        """

        # set the new value of foo
        self.foo = foo

    # --------------------------------------------------------------------------
    # Gets the current value of foo
    # --------------------------------------------------------------------------
    def get_foo(self):
        """
            Gets the current value of foo

            Returns:
                [str]: the current value of foo

            Long description.
        """

        # return the current value of foo
        return self.foo

    # --------------------------------------------------------------------------
    # Private methods
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
        # NB: do not call setter functions in constructor
        # (do everything manually)

        # set the initial value of foo
        self.foo = 'foo'

# -)
