#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: uninstall.py                                          |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The uninstall script for this project

THis module uninstalls the project, removing its files and folders to the
appropriate locations on the user's computer.

This file is real ugly b/c we can't access the venv, so we do it manually.
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
import shutil
import sys

# ------------------------------------------------------------------------------
# add assets dir to path

P_DIR_PRJ = Path(__file__).parent.resolve()

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py

# path to project dir
T_DIR_PRJ = P_DIR_PRJ

# init gettext
T_DOMAIN = "__PP_NAME_PRJ_SMALL__"
T_DIR_LOCALE = T_DIR_PRJ / "__PP_PATH_LOCALE__"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# get dirs
P_DIR_USR_INST = Path.home() / "__PP_USR_INST__"

# get files
P_FILE_CFG_UNINST = P_DIR_USR_INST / "__PP_UNINST_CONF_FILE__"


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
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The class to use for installing/uninstalling
# ------------------------------------------------------------------------------
class CNUninstall:
    """
    The class to use for uninstalling

    This class performs the uninstall operation.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # keys
    S_KEY_INST_NAME = "INST_NAME"
    S_KEY_INST_VER = "INST_VER"
    S_KEY_INST_DESK = "INST_DESK"
    S_KEY_INST_CONT = "INST_CONT"

    # short description
    # I18N: short desc in installer
    S_PP_SHORT_DESC = _("__PP_SHORT_DESC__")

    # version string
    S_PP_VERSION = "__PP_VER_MMR__"

    # debug option strings
    S_ARG_DRY_OPTION = "-d"
    S_ARG_DRY_ACTION = "store_true"
    S_ARG_DRY_DEST = "DRY_DEST"
    # I18N help string for debug cmd line option
    S_ARG_DRY_HELP = _("enable dry run mode")

    # config option strings
    S_ARG_HLP_OPTION = "-h"
    S_ARG_HLP_ACTION = "store_true"
    S_ARG_HLP_DEST = "HLP_DEST"
    # I18N: help option help
    S_ARG_HLP_HELP = _("show this help message and exit")

    # about string (to be set by subclass)
    S_ABOUT = (
        "\n"
        "__PP_NAME_PRJ_BIG__\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        "__PP_URL__/__PP_NAME_PRJ_BIG__\n"
    )

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help")

    # cmd line instructions string (to be set by subclass)
    S_EPILOG = ""

    # --------------------------------------------------------------------------

    # messages

    # NB: format param is prog_name
    # I18N: uninstall the program
    S_MSG_UNINST_START = _("Uninstalling {}")
    # NB: format param is prog_name
    # I18N: done uninstalling
    S_MSG_UNINST_END = _("{} uninstalled")
    # I18N: done with step
    S_MSG_DONE = _("Done")
    # I18N: step failed
    S_MSG_FAIL = _("Fail")
    # I18N: show the copy step
    S_MSG_DEL_START = _("Deleting files... ")
    # I18N: uninstall aborted
    S_MSG_ABORT = _("Uninstallation aborted")

    # questions

    # NB: format parma is prog name
    # I18N: ask to overwrite same version
    S_ASK_UNINST = _(
        "This will uninstall {}.\nDo you want to continue? [y/N] "
    )
    # I18N: confirm overwrite install
    S_ASK_CONFIRM = _("y")

    # errors

    # NB: format param is file path
    # I18N: config file not found
    S_ERR_NOT_FOUND = _("File {} not found")
    # NB: format param is file path
    # I18N: config file is not valid json
    S_ERR_NOT_JSON = _("File {} is not a JSON file")

    # dry run messages

    # NB: format param is file or dir path
    S_DRY_REMOVE = "\nremove\n{}"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the class

        Creates a new instance of the object and initializes its properties.
        """

        # set arg properties
        self._dict_args = {}
        self._dry_run = False

        # project stuff
        self._dir_usr_inst = Path()
        self._path_cfg_uninst = Path()

        # config stuff
        self._dict_cfg = {}

        # cmd line stuff
        # NB: placeholder to avoid comparing to None
        self._parser = argparse.ArgumentParser()

    # ------------------------------------------------------------------------------
    # Uninstall the program
    # ------------------------------------------------------------------------------
    def main(self, dir_usr_inst, path_cfg_uninst):
        """
        Uninstall the program

        Args:
            dir_usr_inst: The program's install folder in which files are
            placed
            path_cfg_uninst: Path to the currently installed program's
            uninstall dict info

        Runs the uninstall operation.
        """

        # set props from params
        if dir_usr_inst:
            dir_usr_inst = Path(dir_usr_inst)
            if not dir_usr_inst.is_absolute():
                # make abs rel to self
                dir_usr_inst = P_DIR_PRJ / dir_usr_inst
        self._dir_usr_inst = dir_usr_inst

        if path_cfg_uninst:
            path_cfg_uninst = Path(path_cfg_uninst)
            if not path_cfg_uninst.is_absolute():
                # make abs rel to self
                path_cfg_uninst = P_DIR_PRJ / path_cfg_uninst
        self._path_cfg_uninst = path_cfg_uninst

        # do setup
        self._setup()

        # parse cmd line and get args
        self._do_cmd_line()

        # get prj info from cfg
        self._get_project_info()

        # create an instance of the class
        self._uninstall_content()

        # wind down
        self._teardown()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # NB: these are the main steps, called in order from main()

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    def _setup(self):
        """
        Boilerplate to use at the start of main

        Perform some mundane stuff like setting properties.
        """

        # print default about text
        print(self.S_ABOUT)

        # create a parser object in case we need it
        self._parser = argparse.ArgumentParser(
            add_help=False,
            epilog=self.S_EPILOG,
            formatter_class=CNFormatter,
        )

        # add help text to about block
        print(self.S_ABOUT_HELP)

        # add help option
        self._parser.add_argument(
            self.S_ARG_HLP_OPTION,
            dest=self.S_ARG_HLP_DEST,
            help=self.S_ARG_HLP_HELP,
            action=self.S_ARG_HLP_ACTION,
        )

        # add dry run option
        self._parser.add_argument(
            self.S_ARG_DRY_OPTION,
            dest=self.S_ARG_DRY_DEST,
            help=self.S_ARG_DRY_HELP,
            action=self.S_ARG_DRY_ACTION,
        )

    # --------------------------------------------------------------------------
    # Parse the arguments from the command line
    # --------------------------------------------------------------------------
    def _do_cmd_line(self):
        """
        Parse the arguments from the command line

        Parse the arguments from the command line, after the parser has been
        set up.
        """

        # get namespace object
        args = self._parser.parse_args()

        # convert namespace to dict
        self._dict_args = vars(args)

        # if -h passed, this will print and exit
        if self._dict_args.get(self.S_ARG_HLP_DEST, False):
            self._parser.print_help()
            sys.exit()

        # no -h, print epilog
        print(self.S_EPILOG)

        # ----------------------------------------------------------------------

        # get the args
        self._dry_run = self._dict_args.get(self.S_ARG_DRY_DEST, False)

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Get the install info from the config file.
        """

        # get project info
        self._dict_cfg = self._get_dict_from_file(self._path_cfg_uninst)

        # get prg name/version
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]

        # ask to install same version
        str_ask = input(self.S_ASK_UNINST.format(prog_name))

        # user hit enter or typed anything else except "y"
        if (
            len(str_ask) == 0
            or str_ask.lower()[0] != self.S_ASK_CONFIRM
        ):
            print(self.S_MSG_ABORT)
            sys.exit()

        # print start msg
        print(self.S_MSG_UNINST_START.format(prog_name))

    # uninstall

    # --------------------------------------------------------------------------
    # Uninstall the program
    # --------------------------------------------------------------------------
    def _uninstall_content(self):
        """
        Uninstall the program

        Runs the uninstall operation.
        """

        # uninstall

        # show some info
        print(self.S_MSG_DEL_START, flush=True, end="")

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_INST_CONT, [])

        # for each key, value
        for item in content:

            # get full path of destination
            src = Path.home() / item

            # debug may omit certain assets
            if not src.exists():
                continue

            # (maybe) do delete
            if self._dry_run:
                print(self.S_DRY_REMOVE.format(item))
            else:

                # if the source is a dir
                if src.is_dir():
                    # remove dir
                    shutil.rmtree(src)

                # if the source is a file
                else:
                    # copy file
                    src.unlink()

        # show some info
        print(self.S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Boilerplate to use at the end of main
    # --------------------------------------------------------------------------
    def _teardown(self):
        """
        Boilerplate to use at the end of main

        Perform some mundane stuff like saving config files.
        """

        # just show we are done
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]
        print(self.S_MSG_UNINST_END.format(prog_name))

    # --------------------------------------------------------------------------
    # These are the minor steps, called from major steps for support
    # --------------------------------------------------------------------------

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

        # get dict from file
        try:
            with open(a_file, "r", encoding="UTF-8") as a_file:
                a_dict = json.load(a_file)

        # file not found
        except FileNotFoundError as e:
            raise OSError(self.S_ERR_NOT_FOUND.format(a_file)) from e

        # not valid json in file
        except json.JSONDecodeError as e:
            raise OSError(self.S_ERR_NOT_JSON.format(a_file)) from e

        # return result
        return a_dict


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    inst = CNUninstall()

    # run the instance
    try:
        inst.main(
            P_DIR_USR_INST,
            P_FILE_CFG_UNINST,
        )
    except Exception as e:
        raise e

# -)
