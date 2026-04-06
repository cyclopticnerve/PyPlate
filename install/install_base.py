# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: install_base.py                                       |     ()     |
# Date    : 03/29/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
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
import re
import shlex
import shutil
import subprocess
import sys

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI and GUI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py

# path to project dir
T_DIR_PRJ = Path(__file__).parents[1].resolve()

# init gettext
T_DOMAIN = "pyplate"
T_DIR_LOCALE = T_DIR_PRJ / "i18n/locale"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

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

    # NB: used for logger
    S_APP_NAME = "pyplate"

    # short description
    # pylint: disable=line-too-long
    # NB: need to keep on one line for replacement
    S_PP_SHORT_DESC = "A program for creating and building CLI/GUI/Packages in Python from a template"
    # pylint: enable=line-too-long

    # version string
    S_PP_VERSION = "Version 1.1.0"

    # dry option strings
    S_ARG_DRY_OPTION = "-d"
    S_ARG_DRY_ACTION = "store_true"
    S_ARG_DRY_DEST = "DRY_DEST"
    # I18N: dry mode help
    S_ARG_DRY_HELP = _("enable dry run mode")

    # force option strings
    S_ARG_FORCE_OPTION = "-f"
    S_ARG_FORCE_ACTION = "store_true"
    S_ARG_FORCE_DEST = "FORCE_DEST"
    # I18N: force option help
    S_ARG_FORCE_HELP = _("force install this program")

    # quiet option strings
    S_ARG_QUIET_OPTION = "-q"
    S_ARG_QUIET_ACTION = "store_true"
    S_ARG_QUIET_DEST = "QUIET_DEST"
    # I18N: quiet option help
    S_ARG_QUIET_HELP = _("do not print any messages")

    # help option strings
    S_ARG_HLP_OPTION = "-h"
    S_ARG_HLP_ACTION = "store_true"
    S_ARG_HLP_DEST = "HLP_DEST"
    # I18N: help option help
    S_ARG_HLP_HELP = _("show this help message and exit")

    # about string
    S_ABOUT = (
        "PyPlate\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        "https://github.com/cyclopticnerve/PyPlate"
    )

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help")

    # keys
    S_KEY_INST_NAME = "INST_NAME"
    S_KEY_INST_VER = "INST_VER"
    S_KEY_INST_DESK = "INST_DESK"
    S_KEY_INST_CONT = "INST_CONT"
    S_KEY_UNINST_CONT = "UNINST_CONT"
    S_KEY_CFG_CONT = "CFG_CONT"

    # --------------------------------------------------------------------------
    # for json

    S_ENCODING = "UTF-8"

    # --------------------------------------------------------------------------
    # questions

    # I18N: dialog fmt (params are question and buttons)
    S_ASK_FMT = _("{} [{}]: ")
    S_ASK_BTN_SEP = "/"
    S_ASK_VER_SAME = _(
        # I18N: ask to overwrite same version
        "The current version of this program is already installed.\nDo you "
        "want to overwrite?"
    )
    S_ASK_VER_OLDER = _(
        # I18N: ask to overwrite newer version
        "A newer version of this program is currently installed.\nDo you want "
        "to overwrite?"
    )
    # NB: format param is prog name
    # I18N: ask to uninstall
    S_ASK_UNINST = _("This will uninstall {}.\nDo you want to continue?")
    # I18N: answer yes
    S_ASK_YES = _("y")
    # I18N: answer no
    S_ASK_NO = _("N")

    # --------------------------------------------------------------------------
    # commands

    # NB: format param is dir_venv
    S_CMD_CREATE = "python -m venv {}"
    # NB: format params are path to prj, path to venv, and path to reqs file
    S_CMD_TYPE_INST = "cd {};. {}/bin/activate;python -m pip install -r {}"

    # --------------------------------------------------------------------------
    # dry run messages

    S_DRY_VENV = "venv cmd:\n"
    S_DRY_REQS = "reqs cmd:\n"
    # NB: format params are source and destination file/dir
    S_DRY_COPY = "copy:\n{}\nto\n{}"
    # NB: format param is path to icon
    S_DRY_DESK_ICON = "set desktop icon:\n"
    # NB: format param is file or dir path
    S_DRY_REMOVE = "remove:\n"
    # NB: format param is ext file
    S_DRY_EXT = "external:\n"

    # --------------------------------------------------------------------------
    # error messages

    # I18N: an error occurred
    S_ERR_ERR = _("Error:")
    # NB: format param is file path
    # I18N: config file not found
    S_ERR_NOT_FOUND = _("File not found:")
    # NB: format param is file path
    # I18N: config file is not valid json
    S_ERR_NOT_JSON = _("File is not a JSON file:")
    # I18N: version numbers invalid
    S_ERR_VERSION = _("One or both version numbers are invalid")
    # NB: format param is source path
    # I18N: src path invalid
    S_ERR_SRC_PATH = _("Source path can not be {}")
    # NB: format param is dest path
    # I18N: dst path invalid
    S_ERR_DST_PATH = _("Destination path can not be {}")
    # I18N: can't find .desktop
    S_ERR_NO_DESK = _("No desktop files present")

    # --------------------------------------------------------------------------
    # messages

    # I18N: done with step
    S_MSG_DONE = _("Done")
    # I18N: step failed
    S_MSG_FAIL = _("Failed")
    # I18N: process aborted
    S_MSG_ABORT = _("Aborted")
    # NB: format param is script name
    # I18N: run external script
    S_MSG_RUN_EXT = _("Running {}... ")

    # NB: format params are prog_name and prog_version
    # I18N: install the program
    S_MSG_INST_START = _("Installing {} Version {}")
    # I18N: show the copy file step
    S_MSG_COPY_START = _("Copying files... ")
    # I18N: show the copy config step
    S_MSG_CONF_START = _("Copying config... ")
    # I18N: show the venv step
    S_MSG_VENV_START = _("Making venv folder... ")
    # I18N: show the reqs step
    S_MSG_REQS_START = _("Installing requirements... ")
    # I18N: show desktop step
    S_MSG_DSK_START = _("Fixing .desktop file... ")
    # NB: format param is __PP_NAME_PRJ_SMALL__
    # I18N: done installing
    S_MSG_INST_END = _("{} installed")

    # NB: format param is prog_name
    # I18N: uninstall the program
    S_MSG_UNINST_START = _("Uninstalling {}")
    # I18N: start deleting old program
    S_MSG_DEL_PRG_START = _("Deleting old program files... ")
    # I18N: start deleting old config
    S_MSG_DEL_CFG_START = _("Deleting old configuration... ")
    # NB: format param is prog_name
    # I18N: done uninstalling
    S_MSG_UNINST_END = _("{} uninstalled")

    # --------------------------------------------------------------------------
    # regex stuff

    # version check results
    I_VER_OLDER = -1
    I_VER_SAME = 0
    I_VER_NEWER = 1
    I_VER_ERROR = -2

    # regex for adding user's home to icon path
    R_ICON_SCH = r"^(Icon=)(.*)$"
    R_ICON_REP = r"\g<1>{}"  # Icon=<home/__PP_IMG_DESK__>

    # regex to compare version numbers
    R_VERSION_VALID = (
        r"^"
        r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
        r"(?:-("
        r"(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)"
        r"(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*"
        r"))?"
        r"(?:\+("
        r"[0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*"
        r"))?"
        r"$"
    )
    R_VERSION_GROUP_MAJ = 1
    R_VERSION_GROUP_MIN = 2
    R_VERSION_GROUP_REV = 3
    R_VERSION_GROUP_PRE = 4
    R_VERSION_GROUP_META = 5

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

        # set arg defaults
        self._dict_args = {}
        self._arg_dry = False
        self._arg_force = False
        self._arg_quiet = False

        # contents of install.json
        self._dict_cfg = {}

        # cmd line stuff
        self._parser = argparse.ArgumentParser(
            formatter_class=CNFormatter, add_help=False, prog=self.S_APP_NAME
        )

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

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """

        # ----------------------------------------------------------------------
        # use cmd line

        # add dry run option
        self._parser.add_argument(
            self.S_ARG_DRY_OPTION,
            dest=self.S_ARG_DRY_DEST,
            help=self.S_ARG_DRY_HELP,
            action=self.S_ARG_DRY_ACTION,
        )

        # add force option
        self._parser.add_argument(
            self.S_ARG_FORCE_OPTION,
            action=self.S_ARG_FORCE_ACTION,
            dest=self.S_ARG_FORCE_DEST,
            help=self.S_ARG_FORCE_HELP,
        )

        # add quiet option
        self._parser.add_argument(
            self.S_ARG_QUIET_OPTION,
            action=self.S_ARG_QUIET_ACTION,
            dest=self.S_ARG_QUIET_DEST,
            help=self.S_ARG_QUIET_HELP,
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
        args = None
        try:
            # NB: will always print usage and "unrecognized arg" msg
            args = self._parser.parse_args()
        except SystemExit:

            # print "use -h" and bail
            print()
            print(self.S_ABOUT_HELP)
            self._teardown(-1)

        # convert namespace to dict
        self._dict_args = vars(args)

        # ----------------------------------------------------------------------
        # check for one-shot args

        # if -h passed, this will print and exit
        if self._dict_args.get(self.S_ARG_HLP_DEST, False):

            # print usage and arg info and exit
            print()
            print(self.S_ABOUT)
            print()
            self._parser.print_help()
            self._teardown()

        # ----------------------------------------------------------------------
        # set props from args

        # get the args
        self._arg_dry = self._dict_args.get(self.S_ARG_DRY_DEST, self._arg_dry)
        self._arg_force = self._dict_args.get(
            self.S_ARG_FORCE_DEST, self._arg_force
        )
        self._arg_quiet = self._dict_args.get(
            self.S_ARG_QUIET_DEST, self._arg_quiet
        )

        # print default about text
        if not self._arg_quiet:
            print()
            print(self.S_ABOUT)
            print()
            print(self.S_ABOUT_HELP)

        # ready to go
        # NB: not sure how do do this the other way around
        if self._arg_dry or (self._arg_force and self._arg_quiet):
            pass
        else:
            print()

    # --------------------------------------------------------------------------
    # Boilerplate to use at the end of main
    # --------------------------------------------------------------------------
    def _teardown(self, errcode: int=0):
        """
        Boilerplate to use at the end of main

        Perform some mundane stuff like saving config files.
        """

        # ----------------------------------------------------------------------
        # call this at the end of subclass teardown

        if not self._arg_quiet:
            print()
        sys.exit(errcode)

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
            with open(a_file, "r", encoding=self.S_ENCODING) as a_file:
                a_dict = json.load(a_file)

        # file not found
        except FileNotFoundError as e:
            raise OSError(self.S_ERR_NOT_FOUND, a_file) from e

        # not valid json in file
        except json.JSONDecodeError as e:
            raise OSError(self.S_ERR_NOT_JSON, a_file) from e

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
        btn_sep=S_ASK_BTN_SEP,
        msg_fmt=S_ASK_FMT,
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

            # no input (empty)
            if inp == "" and default != "":
                return default

            # input a button
            for item in buttons:
                if inp.lower() == item.lower():
                    return item

            # ------------------------------------------------------------------
            # wrong answer

            # no loop, return blank
            if not loop:
                return ""

    # --------------------------------------------------------------------------
    # Run an external command at some point
    # --------------------------------------------------------------------------
    def _do_external(self, cmd: str, hide: bool = False):
        """
        Run an external command at some point

        Args:
            cmd: Command to run
            hide: Whether to hide the command's output
        """

        # if it's a dry run, don't do anything
        # dry_run = self._dict_args.get(self.S_ARG_DRY_DEST, False)
        if self._arg_dry:
            print(self.S_DRY_EXT, cmd)
            print()
            return

        if not self._arg_quiet:
            print(self.S_MSG_RUN_EXT, cmd, flush=True, end="")

        # run the external command
        try:
            # NB: maybe hide output
            cmd_list = shlex.split(cmd)
            subprocess.run(cmd_list, check=True, capture_output=hide)
            if not self._arg_quiet:
                print(self.S_MSG_DONE)
        except (FileNotFoundError, subprocess.CalledProcessError) as e:
            if not self._arg_quiet:
                print(self.S_MSG_FAIL)
            # fatal error, print and quit
            # NB: print even if quiet
            print()
            print(self.S_ERR_ERR, e)
            self._teardown(-1)

    # --------------------------------------------------------------------------
    # Compare two semantic versions
    # --------------------------------------------------------------------------
    def _comp_sem_ver(self, ver_old: str, ver_new: str) -> int:
        """
        Compare two semantic versions

        Args:
            ver_old: The old version to compare
            ver_new: The new version to compare

        Returns:
            An integer showing the relationship between the two version

        Compare two semantic versions
        """

        # sanity checks
        if not ver_old or ver_old == "":
            return self.I_VER_ERROR
        if not ver_new or ver_new == "":
            return self.I_VER_ERROR
        if ver_old == ver_new:
            return self.I_VER_SAME

        # --------------------------------------------------------------------------

        # compare version string parts (only x.x.x)
        res_old = re.search(self.R_VERSION_VALID, ver_old)
        res_new = re.search(self.R_VERSION_VALID, ver_new)

        # if either version string is None
        if not res_old or not res_new:
            return self.I_VER_ERROR

        # make a list of groups to check
        lst_groups = [
            self.R_VERSION_GROUP_MAJ,
            self.R_VERSION_GROUP_MIN,
            self.R_VERSION_GROUP_REV,
        ]

        # for each part as int
        for group in lst_groups:
            old_val = int(res_old.group(group))
            new_val = int(res_new.group(group))

            # slide out at the first difference
            if old_val < new_val:
                return self.I_VER_NEWER
            if old_val > new_val:
                return self.I_VER_OLDER

        # ----------------------------------------------------------------------

        # still going, check pre
        pre_old = res_old.group(self.R_VERSION_GROUP_PRE)
        pre_new = res_new.group(self.R_VERSION_GROUP_PRE)

        # simple pre rule compare
        if not pre_old and pre_new:
            return self.I_VER_OLDER
        if pre_old and not pre_new:
            return self.I_VER_NEWER
        if not pre_old and not pre_new:
            return self.I_VER_SAME

        # ----------------------------------------------------------------------

        # if pre_old and pre_new:

        # split pre on dots
        lst_pre_old = pre_old.split(".")
        lst_pre_new = pre_new.split(".")

        # get number of parts
        len_pre_old = len(lst_pre_old)
        len_pre_new = len(lst_pre_new)

        # get shorter of two
        shortest = len_pre_old if len_pre_old <= len_pre_new else len_pre_new

        # for each part in shortest
        for index in range(shortest):

            # get each value at position
            old_val = lst_pre_old[index]
            new_val = lst_pre_new[index]

            # 1. both numbers
            if old_val.isdigit() and new_val.isdigit():
                tmp_old_val = int(old_val)
                tmp_new_val = int(new_val)

                # slide out at the first difference
                if tmp_old_val > tmp_new_val:
                    return self.I_VER_OLDER
                if tmp_old_val < tmp_new_val:
                    return self.I_VER_NEWER

            # 2. both alphanumeric
            if not old_val.isdigit() and not new_val.isdigit():
                lst_alpha = [old_val, new_val]
                lst_alpha.sort()

                idx_old = lst_alpha.index(old_val)
                idx_new = lst_alpha.index(new_val)

                if idx_old > idx_new:
                    return self.I_VER_OLDER
                if idx_old < idx_new:
                    return self.I_VER_NEWER

            # 3 num vs alphanumeric
            if old_val.isdigit() and not new_val.isdigit():
                return self.I_VER_OLDER
            if not old_val.isdigit() and new_val.isdigit():
                return self.I_VER_NEWER

            # 4 len
            if len_pre_old > len_pre_new:
                return self.I_VER_OLDER
            if len_pre_new > len_pre_old:
                return self.I_VER_NEWER

        # ----------------------------------------------------------------------

        # error in one or both versions
        return self.I_VER_ERROR

    # --------------------------------------------------------------------------
    # Uninstall the program, but not the config stuff
    # --------------------------------------------------------------------------
    def _uninstall_cont(self, quiet: bool):
        """
        Uninstall the contents (but not config) of program

        Runs the uninstall operation.
        """

        # show some progress
        if not quiet and not self._arg_dry:
            print(self.S_MSG_DEL_PRG_START, flush=True, end="")

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_UNINST_CONT, [])

        # for each key, value
        for item in content:

            # get full path of destination
            src = Path.home() / item

            # debug may omit certain assets
            if not src.exists():
                continue

            # if it's a dry run, don't do anything
            if self._arg_dry:
                print(self.S_DRY_REMOVE, item)
                continue

            # if the source is a dir
            if src.is_dir():
                # remove dir
                shutil.rmtree(src)

            # if the source is a file
            else:
                # copy file
                src.unlink()

        # show some info
        if not quiet and not self._arg_dry:
            print(self.S_MSG_DONE)

        # for make pretty
        if self._arg_dry:
            print()


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line
    print("WRONG CLASS, SIR !!!")

# -)
