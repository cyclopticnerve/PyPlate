#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_PRJ_SMALL__.py                              |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the program

This file is executable and can be called from the terminal like:

foo@bar:~$ cd [path to directory of this file]
foo@bar:~[path to directory of this file] ./__PP_NAME_PRJ_SMALL__.py [cmd line]

or if installed in a global location:

foo@bar:~$ __PP_NAME_PRJ_SMALL__ [cmd line]

Typical usage is show in the main() method.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# third party imports
from __PP_NAME_PRJ_SMALL___base import _
from __PP_NAME_PRJ_SMALL___base import __PP_NAME_PRJ_PASCAL__Base

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class __PP_NAME_PRJ_PASCAL__(__PP_NAME_PRJ_PASCAL__Base):
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

    # NB: used in _enable
    S_PRG_NAME = "__PP_NAME_PRJ_SMALL__"

    # cmd line options

    # enable option strings
    # S_ARG_X_OPTION = "-x"
    # S_ARG_X_ACTION = "store_true"
    # S_ARG_X_DEST = "X_DEST"
    # # I18N: enable mode help
    # S_ARG_X_HELP = _("do x")

    # # --------------------------------------------------------------------------
    # # Initialize the new object
    # # --------------------------------------------------------------------------
    # def __init__(self):
    #     """
    #     Initialize the new object

    #     Initializes a new instance of the class, setting the default values
    #     of its properties, and any other code that needs to run to create a
    #     new object.
    #     """

    #     # do super init
    #     super().__init__()

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

        # --------------------------------------------------------------------------
        # Private methods
        # --------------------------------------------------------------------------

        # NB: these are the main steps, called in order from main

        # # --------------------------------------------------------------------------
        # # Boilerplate to use at the start of main
        # # --------------------------------------------------------------------------
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
        if self._cmd_debug:
            # I18N: context for this string
            return _("this is func (DEBUG)")

        # no debug, return normal result
        # I18N: context for this string
        return _("this is func")

    # # --------------------------------------------------------------------------
    # # Boilerplate to use at the end of main
    # # --------------------------------------------------------------------------
    # def _teardown(self):
    #     """
    #     Boilerplate to use at the end of main

    #     Perform some mundane stuff like saving properties.
    #     If you implement this function. make sure to call super() LAST!!!
    #     """

    #     print("sub ", .f_code.co_name)

    #     # save a prop
    #     self._dict_cfg["foo"] = "bar"

    #     # do teardown
    #     super()._teardown()


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    obj = __PP_NAME_PRJ_PASCAL__()

    # run the instance
    obj.main()

# -)
