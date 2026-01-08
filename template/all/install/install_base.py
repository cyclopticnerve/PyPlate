# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_NAME_PRJ_SMALL___base.py                         |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The base file for a cli or gui program

This file contains all the boring boilerplate code for making a robust CLI/GUI
application. It is not intended to be run directly, but rather subclassed. The
subclass should contain, at minimum, the main method and the top-level run code
(examples are given in the cli/src and gui/src subdirectories of the template
directory).
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
import gettext
import json
import locale
from pathlib import Path
import sys

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# project dir
P_DIR_PRJ = Path(__file__).parents[1].resolve()

# get dirs
P_FILE_CFG_UNINST = P_DIR_PRJ / "__PP_DIR_INSTALL__/__PP_FILE_INST_CFG__"

# for json
S_ENCODING = "UTF-8"

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI and GUI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py

# ------------------------------------------------------------------------------
# A global function to manage each class's path to locale
# ------------------------------------------------------------------------------
def get_i18n(i18n_dir):
    """docstring"""

    # path to project dir
    t_dir_prj = i18n_dir

    # init gettext
    t_domain = "__PP_NAME_PRJ_SMALL__"
    t_dir_locale = t_dir_prj / "__PP_PATH_LOCALE__"
    t_translation = gettext.translation(t_domain, t_dir_locale, fallback=True)
    res = t_translation.gettext

    # fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
    # use for CLI in the interest of common code)
    locale.bindtextdomain(t_domain, t_dir_locale)

    return res

# get our local local path
_ = get_i18n(P_DIR_PRJ)

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


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class CNInstallBase:
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

    # --------------------------------------------------------------------------
    # strings

    # short description
    # pylint: disable=line-too-long
    # NB: need to keep on one line for replacement
    S_PP_SHORT_DESC = "Short description"
    # pylint: enable=line-too-long

    # version string
    S_PP_VERSION = "Version 0.0.1"

    # debug option strings
    S_ARG_DRY_OPTION = "-d"
    S_ARG_DRY_ACTION = "store_true"
    S_ARG_DRY_DEST = "DRY_DEST"
    # I18N: dry mode help
    S_ARG_DRY_HELP = _("enable dry run mode")

    # config option strings
    S_ARG_HLP_OPTION = "-h"
    S_ARG_HLP_ACTION = "store_true"
    S_ARG_HLP_DEST = "HLP_DEST"
    # I18N: help option help
    S_ARG_HLP_HELP = _("show this help message and exit")

    # about string
    S_ABOUT = (
        "\n"
        "SpaceOddity\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        "https://github.com/cyclopticnerve/SpaceOddity\n"
    )

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help")

    # keys
    S_KEY_INST_NAME = "INST_NAME"
    S_KEY_INST_VER = "INST_VER"
    S_KEY_INST_DESK = "INST_DESK"
    S_KEY_INST_CONT = "INST_CONT"
    S_KEY_UNINST_CONT = "UNINST_CONT"

    # --------------------------------------------------------------------------

    # messages
    # I18N: done with step
    S_MSG_DONE = _("Done")
    # I18N: step failed
    S_MSG_FAIL = _("Failed")
    # I18N: process aborted
    S_MSG_ABORT = _("Aborted")

    # --------------------------------------------------------------------------
    # questions
    # I18N: answer yes
    S_ASK_YES = _("y")
    # I18N: answer no
    S_ASK_NO = _("N")

    # --------------------------------------------------------------------------
    # error messages
    # I18N: an error occurred
    S_ERR_ERR = _("Error:")
    # NB: format param is file path
    # I18N: config file not found
    S_ERR_NOT_FOUND = _("File {} not found")
    # NB: format param is file path
    # I18N: config file is not valid json
    S_ERR_NOT_JSON = _("File {} is not a JSON file")

    # --------------------------------------------------------------------------
    # Instance methods
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

        # set defaults

        # cfg stuff
        self._dict_cfg = {}

        # cmd line stuff
        self._parser = argparse.ArgumentParser(
            formatter_class=CNFormatter, add_help=False
        )

        # set arg defaults
        self._dry_run = False

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    def _setup(self):
        """
        Boilerplate to use at the start of main

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """
        # print default about text
        print(self.S_ABOUT)

        # add help text to about block
        print(self.S_ABOUT_HELP)

        # add dry run option
        self._parser.add_argument(
            self.S_ARG_DRY_OPTION,
            dest=self.S_ARG_DRY_DEST,
            help=self.S_ARG_DRY_HELP,
            action=self.S_ARG_DRY_ACTION,
        )

        # always add help option
        self._parser.add_argument(
            self.S_ARG_HLP_OPTION,
            action=self.S_ARG_HLP_ACTION,
            dest=self.S_ARG_HLP_DEST,
            help=self.S_ARG_HLP_HELP,
        )

        # ----------------------------------------------------------------------
        # use cmd line
        args = self._parser.parse_args()

        # convert namespace to dict
        dict_args = vars(args)

        # ----------------------------------------------------------------------
        # check for one-shot args

        # if -h passed, this will print and exit
        if dict_args.get(self.S_ARG_HLP_DEST, False):

            # print default about text
            print(self.S_ABOUT)

            # print usage and arg info and exit
            self._parser.print_help()
            print()
            sys.exit(0)

        # get the args
        self._dry_run = dict_args.get(self.S_ARG_DRY_DEST, False)

    # --------------------------------------------------------------------------
    # Boilerplate to use at the end of main
    # --------------------------------------------------------------------------
    def _teardown(self):
        """
        Boilerplate to use at the end of main

        Perform some mundane stuff like saving config files.
        """

        # ----------------------------------------------------------------------
        # this method intentionally left blank

    # --------------------------------------------------------------------------
    # Get a dict from a file
    # --------------------------------------------------------------------------
    def _get_dict_from_file(self, a_file):
        """
        Get a dict from a file

        Args:
            a_file: The file to load the dict from

        Raises:
            OSError if the file cannot be found or is not a valid JSON file

        Returns:
            The dict found in the file

        Get a dict from a file, checking if the file exists and is a valid JSON
        file

        """
        # default result
        a_dict = {}

        try:
            # get dict from file
            with open(a_file, "r", encoding=S_ENCODING) as a_file:
                a_dict = json.load(a_file)

        # file not found
        except FileNotFoundError as e:
            raise OSError(self.S_ERR_NOT_FOUND.format(a_file)) from e

        # not valid json in file
        except json.JSONDecodeError as e:
            raise OSError(self.S_ERR_NOT_JSON.format(a_file)) from e

        # return result
        return a_dict

    # --------------------------------------------------------------------------
    # Create a dialog-like question and return the result
    # --------------------------------------------------------------------------
    def _dialog(
        self,
        message,
        buttons,
        default="",
        loop=False,
        btn_sep="/",
        msg_fmt="{} [{}]: ",
    ):
        """
        Create a dialog-like question and return the result

        Args:
            message: The message to display
            buttons: List of single char answers to the question
            default: The button item to return when the user presses Enter at \
                the question (default: "")
            loop: If True and the user enters an invalid response, keep \
                asking the question. If False, return an empty string for an \
                invalid response
            (default: False)
            btn_sep: Char to use to separate button items
            msg_fmt: Format string to present message/buttons to the user

        Returns:
            The string that matches button (or an empty string if the entered \
                option is not in the button list)

        This method returns the string entered on the command line in response
        to a question. If the entered option does not match any of the buttons,
        a blank string is returned, or the question is repeated if loop = True.
        If you set a default and the option entered is just the Return key, the
        default string will be returned. If no default is present, the entered
        string must match one of the buttons array values.

        Note that if default == "", pressing Enter is not considered a valid
        entry.
        """

        # ----------------------------------------------------------------------

        # add buttons to message
        btns_all = btn_sep.join(buttons)
        str_fmt = msg_fmt.format(message, btns_all)

        # ----------------------------------------------------------------------

        # assume loop == True
        while True:

            # ask the question, get the result
            inp = input(str_fmt)

            # # no input (empty)
            if inp == "" and default != "":
                return default

            # input a button
            if inp in buttons:
                return inp

            # ------------------------------------------------------------------
            # wrong answer

            # no loop, return blank
            if not loop:
                return ""


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line
    print("WRONG GLASS, SIR !!!")

# -)
