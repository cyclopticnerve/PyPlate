#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pyplate.py                                            |     ()     |
# Date    : 05/31/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ cd [path to directory of this file]
foo@bar:~[path to directory of this file] ./pyplate.py [cmd line]

or if installed in a global location:

foo@bar:~$ pyplate [cmd line]

Typical usage is show in the main() method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# local imports
from pyplate_base import _
from pyplate_base import PyplateBase

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class Pyplate(PyplateBase):
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class does the most of the work of a typical CLI program. It parses
    command line options, loads/saves config files, and performs the operations
    required for the program.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------


    # cmd line options

    # enable option strings
    # S_ARG_X_OPTION = "-x"
    # S_ARG_X_ACTION = "store_true"
    # S_ARG_X_DEST = "X_DEST"
    # # I18N: enable mode help
    # S_ARG_X_HELP = _("do x")

    # --------------------------------------------------------------------------
    # Dictionaries

    # set default config dict
    D_CFG_DEF = {}

    # # ------------------------------------------------------------------------
    # # Initialize the new object
    # # ------------------------------------------------------------------------
    # def __init__(self):
    #     """
    #     Initialize the new object

    #     Initializes a new instance of the class, setting the default values
    #     of its properties, and any other code that needs to run to create a
    #     new object.
    #     """

    #     # do super init
    #     super().__init__()

    #     # set default cfg dict
    #     self._dict_cfg = self.D_CFG_DEF.copy()

    #     # NB: add class properties here
    #     self._foo = True

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main method of the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        The main method of the program

        This method is the main entry point for the program, initializing the
        program, and performing its steps.
        """

        # call boilerplate code
        # add our options first
        # then add common options (from super)
        self._setup()

        # do something with -x option
        # if self._dict_args[self.S_ARG_X_DEST]:
        #     pass
        # ----------------------------------------------------------------------
        # main stuff

        # do the thing with the thing
        print(self._func())

        # ----------------------------------------------------------------------
        # teardown

        # call boilerplate code
        self._teardown()

        # ----------------------------------------------------------------------
        # Private methods
        # ----------------------------------------------------------------------

        # NB: these are the main steps, called in order from main

        # # ----------------------------------------------------------------------
        # # Boilerplate to use at the start of main
        # # ----------------------------------------------------------------------
        # def _setup(self):
        #     """
        #     Boilerplate to use at the start of main

        #     Perform some mundane stuff like setting properties.
        #     If you implement this function. make sure to call super() LAST!!!
        #     """

        # # add debug option
        # self._parser.add_argument(
        #     self.S_ARG_DBG_OPTION,
        #     action=self.S_ARG_DBG_ACTION,
        #     dest=self.S_ARG_DBG_DEST,
        #     help=self.S_ARG_DBG_HELP,
        # )

        # # add config option
        # self._parser.add_argument(
        #     self.S_ARG_CFG_OPTION,
        #     dest=self.S_ARG_CFG_DEST,
        #     help=self.S_ARG_CFG_HELP,
        #     metavar=self.S_ARG_CFG_METAVAR
        # )

        # add x option
        # self._parser.add_argument(
        #     self.S_ARG_X_OPTION,
        #     action=self.S_ARG_X_ACTION,
        #     dest=self.S_ARG_X_DEST,
        #     help=self.S_ARG_X_HELP,
        # )

        # NB: do setup last
        # super()._setup()

        # NB: self._dict_args are now available
        # as well as self._dict_cfg

    # --------------------------------------------------------------------------
    # Short description
    # --------------------------------------------------------------------------
    def _func(self):
        """
        Short description

        Args:
            var_name: Short description

        Returns:
            Description

        Raises:
            exception_type(vars): Description

        Long description (including HTML).
        """

        # self._logger.info("func")

        # debug_foo
        if self._arg_debug:
            # I18N: context for this string
            return _("this is func (DEBUG)")

        # no debug, return normal result
        # I18N: context for this string
        return _("this is func")

    # # --------------------------------------------------------------------------
    # # Boilerplate to use at the end of main
    # # --------------------------------------------------------------------------
    # def _teardown(self, errcode: int=0):
    #     """
    #     Boilerplate to use at the end of main

    #     Perform some mundane stuff like saving properties.
    #     If you implement this function. make sure to call super() LAST!!!
    #     """

    #     # save a prop
    #     self._dict_cfg["foo"] = "bar"

    #     # do teardown
    #     super()._teardown(errcode)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    obj = Pyplate()

    # run the instance
    obj.main()

# -)
