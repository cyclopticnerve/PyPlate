# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: default_class.py                                      |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import os

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_FILE = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

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
            foo [type]: a type to hold the foo value

        Methods:
            set_foo(foo [type]): sets the new value of foo
            [type] get_foo(): gets the current value of foo

        Long description (including HTML).
    """

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Gets the current value of foo
    # --------------------------------------------------------------------------
    def get_foo(self):
        """
            Gets the current value of foo

            Returns:
                [type]: the current value of foo

            Long description (including HTML).
        """

        # return the current value of foo
        return self.foo

    # --------------------------------------------------------------------------
    # Sets the new value of foo
    # --------------------------------------------------------------------------
    def set_foo(self, foo):
        """
            Sets the new value of foo

            Parameters:
                foo [type]: the new value of foo

            Long description (including HTML).
        """

        # set the new value of foo
        self.foo = foo

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # foo method
    # --------------------------------------------------------------------------
    def _foo():
        pass

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
        # time you call them. better to use a method that is called when/after
        # the class is fully constructed.

        # set the initial value of foo
        self.foo = 'foo'

# -)
