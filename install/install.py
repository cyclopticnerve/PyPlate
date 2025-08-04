#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: install.py                                            |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines
"""
The install script for this project

THis module installs the project, copying its files and folders to the
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
import re
import shutil
import subprocess
import sys

# ------------------------------------------------------------------------------
# add assets dir to path

P_DIR_PRJ = Path(__file__).parent.resolve()
P_DIR_ASSETS = P_DIR_PRJ / "__PP_INST_ASSETS__"

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./pybaker.py

# path to project dir
T_DIR_PRJ = P_DIR_ASSETS

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
P_DIR_VENV = P_DIR_USR_INST / "__PP_NAME_VENV__"

# get files
P_FILE_CFG_INST = P_DIR_ASSETS / "__PP_INST_CONF_FILE__"
P_FILE_CFG_UNINST = P_DIR_USR_INST / "__PP_UNINST_CONF_FILE__"
P_FILE_REQS = P_DIR_ASSETS / "__PP_DIR_INSTALL__" / "__PP_REQS_FILE__"
P_FILE_DESK = P_DIR_ASSETS / "__PP_FILE_DESK__"
P_FILE_DESK_ICON = P_DIR_ASSETS / "__PP_DIR_IMAGES__/__PP_NAME_PRJ_SMALL__.png"


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
# The class to use for installing/uninstalling
# ------------------------------------------------------------------------------
class CNInstall:
    """
    The class to use for installing a PyPlate program

    This class performs the install operation.
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
    # NB: MUST BE ALL ON ONE LINE!!!
    # I18N: short desc in installer
    S_PP_SHORT_DESC = _("__PP_SHORT_DESC__")

    # version string
    # NB: MUST BE ALL ON ONE LINE!!!
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

    # cmd line instructions string
    S_EPILOG = ""

    # --------------------------------------------------------------------------

    # messages

    # NB: format params are prog_name and prog_version
    # I18N: install the program
    S_MSG_INST_START = _("Installing {} Version {}")
    # NB: format param is prog_name
    # I18N: done installing
    S_MSG_INST_END = _("{} installed")
    # I18N: done with step
    S_MSG_DONE = _("Done")
    # I18N: step failed
    S_MSG_FAIL = _("Fail")
    # I18N: show the copy step
    S_MSG_COPY_START = _("Copying files... ")
    # I18N: show the venv step
    S_MSG_VENV_START = _("Making venv folder... ")
    # I18N: show the reqs step
    S_MSG_REQS_START = _("Installing requirements... ")
    # I18N: show desktop step
    S_MSG_DSK_START = _("Fixing .desktop file... ")
    # I18N: install aborted
    S_MSG_ABORT = _("Installation aborted")

    # questions
    # I18N: answer yes
    S_ASK_YES = _("y")
    # I18N: answer no
    S_ASK_NO = _("n")
    # I18N: ask to overwrite same version
    S_ASK_VER_SAME = _(
        "The current version of this program is already \
                       installed.\nDo you want to overwrite?"
    )
    # I18N: ask to overwrite newer version
    S_ASK_VER_OLDER = _(
        "A newer version of this program is currently \
                        installed.\nDo you want to overwrite?"
    )
    # I18N: ask to write first version
    # S_ASK_VER_NEWER = _("The current version of this program will be \
    #                   installed.\nDo you want to continue?"
    # )

    # errors
    # NB: format param is file path
    # I18N: config file not found
    S_ERR_NOT_FOUND = _("File {} not found")
    # NB: format param is file path
    # I18N: config file is not valid json
    S_ERR_NOT_JSON = _("File {} is not a JSON file")
    # I18N: version numbers invalid
    S_ERR_VERSION = _("One or both version numbers are invalid")
    # NB: format param is source path
    # I18N: src path invalid
    S_ERR_SRC_PATH = _("Source path can not be {}")
    # NB: format param is dest path
    # I18N: dst path invalid
    S_ERR_DST_PATH = _("Destination path can not be {}")

    # dry run messages

    S_DRY_VENV = "\nvenv cmd:"
    S_DRY_REQS = "\nreqs cmd:"
    # NB: format params are source and destination file/dir
    S_DRY_COPY = "\ncopy\n{}\nto\n{}"
    # NB: format param is path to icon
    S_DRY_DESK_ICON = "set desktop icon: {}"

    # commands

    # NB: format param is dir_venv
    S_CMD_CREATE = "python -m venv {}"
    # NB: format params are path to prj, path to venv, and path to reqs file
    S_CMD_INSTALL = "cd {};. {}/bin/activate;python -m pip install -r {}"

    # regex for adding user's home to icon path
    R_ICON_SCH = r"^(Icon=)(.*)$"
    R_ICON_REP = r"\g<1>{}"  # Icon=<home/__PP_IMG_DESK__>

    # ------------------------------------------------------------------------------

    # version check results
    S_VER_OLDER = -1
    S_VER_SAME = 0
    S_VER_NEWER = 1

    # regex to compare version numbers
    R_VERSION = r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(.*)$"
    R_VERSION_GROUP_MAJ = 1
    R_VERSION_GROUP_MIN = 2
    R_VERSION_GROUP_REV = 3

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
        # NB: set to path objects to avoid comparing to None
        self._dir_assets = Path()
        self._dir_usr_inst = Path()
        self._path_cfg_inst = Path()
        self._path_cfg_uninst = Path()
        self._dir_venv = Path()
        self._path_reqs = Path()
        self._file_desk = Path()
        self._file_desk_icon = Path()

        # config stuff
        self._dict_cfg = {}

        # cmd line stuff
        # NB: placeholder to avoid comparing to None
        self._parser = argparse.ArgumentParser()

    # --------------------------------------------------------------------------
    # Install the program
    # --------------------------------------------------------------------------
    def main(
        self,
        dir_assets,
        dir_usr_inst,
        path_cfg_inst,
        path_cfg_uninst,
        dir_venv,
        path_reqs,
        file_desk=None,
        file_desk_icon=None,
    ):
        """
        Install the program

        Args:
            dir_assets: Path to the assets folder where all of the program
            files are put in dist. This is the base source path to use when
            copying files to the user's computer
            dir_usr_inst: The program's install folder in which to place files
            path_cfg_inst: Path to the file that contains the current install
            dict info
            path_cfg_uninst: Path to the currently installed program's
            uninstall dict info
            dir_venv: The path to the venv folder to create
            path_reqs: Path to the requirements.txt file to add requirements to
            the venv
            file_desk: Path to the .desktop file (if GUI) (default: None)
            file_desk_icon: Path to the .desktop file icon (if GUI) (default:
            None)

        Runs the install operation.
        """

        # set props from params
        if dir_assets:
            dir_assets = Path(dir_assets)
            if not dir_assets.is_absolute():
                # make abs rel to self
                dir_assets = P_DIR_PRJ / dir_assets
        self._dir_assets = dir_assets

        if dir_usr_inst:
            dir_usr_inst = Path(dir_usr_inst)
            if not dir_usr_inst.is_absolute():
                # make abs rel to self
                dir_usr_inst = self._dir_assets / dir_usr_inst
        self._dir_usr_inst = dir_usr_inst

        if path_cfg_inst:
            path_cfg_inst = Path(path_cfg_inst)
            if not path_cfg_inst.is_absolute():
                # make abs rel to self
                path_cfg_inst = self._dir_assets / path_cfg_inst
        self._path_cfg_inst = path_cfg_inst

        if path_cfg_uninst:
            path_cfg_uninst = Path(path_cfg_uninst)
            if not path_cfg_uninst.is_absolute():
                # make abs rel to self
                path_cfg_uninst = self._dir_assets / path_cfg_uninst
        self._path_cfg_uninst = path_cfg_uninst

        if dir_venv:
            dir_venv = Path(dir_venv)
            if not dir_venv.is_absolute():
                # make abs rel to self
                dir_venv = self._dir_assets / dir_venv
        self._dir_venv = dir_venv

        if path_reqs:
            path_reqs = Path(path_reqs)
            if not path_reqs.is_absolute():
                # make abs rel to self
                path_reqs = self._dir_assets / path_reqs
        self._path_reqs = path_reqs

        if file_desk:
            file_desk = Path(file_desk)
            if not file_desk.is_absolute():
                # make abs rel to self
                file_desk = self._dir_assets / file_desk
        self._file_desk = file_desk

        if file_desk_icon:
            file_desk_icon = Path(file_desk_icon)
            if not file_desk_icon.is_absolute():
                # make abs rel to self
                file_desk_icon = self._dir_assets / file_desk_icon
        self._file_desk_icon = file_desk_icon

        # ----------------------------------------------------------------------

        # do setup
        self._setup()

        # parse cmd line and get args
        self._do_cmd_line()

        # get prj info from cfg
        self._get_project_info()

        # check for existing/old version
        self._check_version()

        # make the venv on the user's comp
        self._make_venv()

        # install reqs
        self._install_reqs()

        # fix desktop file if present
        self._fix_desktop_file()

        # move content
        self._install_content()

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
        self._dict_cfg = self._get_dict_from_file(self._path_cfg_inst)

        # get prg name/version
        prog_name = self._dict_cfg[self.S_KEY_INST_NAME]
        prog_version = self._dict_cfg[self.S_KEY_INST_VER]

        # print start msg
        print(self.S_MSG_INST_START.format(prog_name, prog_version))

    # --------------------------------------------------------------------------
    # Check version info
    # --------------------------------------------------------------------------
    def _check_version(self):
        """
        Check version info

        Get the version info from the new config file and the old config file
        (if present), compare the two values, and either continue or abort.
        """

        # if we did pass an old conf, it must exist (if it doesn't, this could
        # be the first install but we will want to check on later updates)
        if self._path_cfg_uninst and Path(self._path_cfg_uninst).exists():

            # get info from old cfg
            dict_cfg_old = self._get_dict_from_file(self._path_cfg_uninst)

            # check versions
            ver_old = dict_cfg_old[self.S_KEY_INST_VER]
            ver_new = self._dict_cfg[self.S_KEY_INST_VER]

            # do the compare and get S_VER__OLDER, S_VER_SAME, S_VER_NEWER
            res = self._compare_version(ver_old, ver_new)

            # same version is installed
            if res == self.S_VER_SAME:

                # ask to install same version
                str_ask = self._dialog(
                    self.S_ASK_VER_SAME,
                    [self.S_ASK_YES, self.S_ASK_NO],
                    self.S_ASK_NO,
                )

                # user hit enter or typed anything else except "y"
                if str_ask == self.S_ASK_NO:
                    print(self.S_MSG_ABORT)
                    sys.exit()

            # newer version is installed
            elif res == self.S_VER_OLDER:

                # ask to install old version over newer
                str_ask = self._dialog(
                    self.S_ASK_VER_OLDER,
                    [self.S_ASK_YES, self.S_ASK_NO],
                    self.S_ASK_NO,
                )

                # user hit enter or typed anything else except "y"
                if str_ask == self.S_ASK_NO:
                    print(self.S_MSG_ABORT)
                    sys.exit()

    # --------------------------------------------------------------------------
    # Make venv for this program on user's computer
    # --------------------------------------------------------------------------
    def _make_venv(self):
        """
        Make venv for this program on user's computer

        Raises:
            subprocess.CalledProcessError if the venv creation fails

        Makes a .venv-XXX folder on the user's computer.
        """

        # show progress
        print(self.S_MSG_VENV_START, flush=True, end="")

        # the command to create a venv
        cmd = self.S_CMD_CREATE.format(self._dir_venv)

        # if it's a dry run, don't make venv
        if self._dry_run:
            print(self.S_DRY_VENV, cmd)
            print(self.S_MSG_DONE)
            return

        # the cmd to create the venv
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(self.S_MSG_DONE)
        except Exception as e:
            print(self.S_MSG_FAIL)
            raise e

    # --------------------------------------------------------------------------
    # Install requirements.txt
    # --------------------------------------------------------------------------
    def _install_reqs(self):
        """
        Install requirements.txt

        Raises:
            subprocess.CalledProcessError if the reqs install fails

        Installs the contents of a requirements.txt file into the program's
        venv.
        """

        # show progress
        print(self.S_MSG_REQS_START, end="", flush=True)

        # the command to install packages to venv from reqs
        cmd = self.S_CMD_INSTALL.format(
            self._dir_venv.parent, self._dir_venv.name, self._path_reqs
        )

        # if it's a dry run, don't install
        if self._dry_run:
            print(self.S_DRY_REQS, cmd)
            print(self.S_MSG_DONE)
            return

        # the cmd to install the reqs
        try:
            # NB: hide output
            subprocess.run(
                cmd, shell=True, check=True, stdout=subprocess.DEVNULL
            )
            print(self.S_MSG_DONE)
        except Exception as e:
            print(self.S_MSG_FAIL)
            raise e

    # --------------------------------------------------------------------------
    # Fix .desktop file, for paths and such
    # --------------------------------------------------------------------------
    def _fix_desktop_file(self):
        """
        Fix .desktop file, for paths and such

        Raises:
            OSError if one of both of the files does not exist

        Fixes entries in the .desktop file (absolute paths, etc.)
        Currently only fixes absolute path to icon.
        """

        # make sure we even care about desktop
        use_desk = self._dict_cfg.get(self.S_KEY_INST_DESK, False)
        if not use_desk:
            return

        # check both files for None and exist
        if not self._file_desk or not self._file_desk.exists():
            raise OSError(self.S_ERR_NOT_FOUND.format(self._file_desk))
        if not self._file_desk_icon or not self._file_desk_icon.exists():
            raise OSError(self.S_ERR_NOT_FOUND.format(self._file_desk_icon))

        # print info
        print(self.S_MSG_DSK_START, end="", flush=True)

        # don't mess with file
        if self._dry_run:
            print(self.S_DRY_DESK_ICON.format(self._file_desk_icon))
            print(self.S_MSG_DONE)
            return

        # open file
        text = ""
        with open(self._file_desk, "r", encoding="UTF-8") as a_file:
            text = a_file.read()

        # find icon line and fix
        res = re.search(self.R_ICON_SCH, text, flags=re.M)
        if res:

            # get user's home and path to icon rel to prj
            path_icon = Path.home() / self._file_desk_icon

            # fix abs path to icon
            r_icon_rep = self.R_ICON_REP.format(path_icon)
            text = re.sub(self.R_ICON_SCH, r_icon_rep, text, flags=re.M)

            # ------------------------------------------------------------------

            # write fixed text back to file
            with open(self._file_desk, "w", encoding="UTF-8") as a_file:
                a_file.write(text)

        # show some info
        print(self.S_MSG_DONE)

    # --------------------------------------------------------------------------
    # Copy source files/folders
    # --------------------------------------------------------------------------
    def _install_content(self):
        """
        Copy source files/folders

        This method copies files and folders from the assets folder of the
        source to their final locations in the user's folder structure.
        """

        # show some info
        print(self.S_MSG_COPY_START, flush=True, end="")

        # content list from dict
        content = self._dict_cfg.get(self.S_KEY_INST_CONT, {})

        # for each key, value
        for k, v in content.items():

            # get full paths of source / destination
            src = self._dir_assets / k
            dst = Path.home() / v / src.name

            # debug may omit certain assets
            if not src.exists():
                continue

            # check for dry run
            if self._dry_run:
                print(self.S_DRY_COPY.format(src, dst))
            else:
                # if the source is a dir
                if src.is_dir():
                    shutil.copytree(src, dst, dirs_exist_ok=True)
                # if the src is a file
                else:
                    shutil.copy(src, dst)

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
        print(self.S_MSG_INST_END.format(prog_name))

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

    # --------------------------------------------------------------------------
    # Create a dialog-like question and return the result
    # --------------------------------------------------------------------------
    def _dialog(
        self, message, buttons, default="", btn_sep="/", msg_fmt="{} [{}]: "
    ):
        """
        Create a dialog-like question and return the result
        
        Args:
            message: The message to display
            buttons: List of single char answers to the question
            default: The button item to return when the user presses Enter at the 
                question (default: "")
            btn_sep: Char to use to separate button items
            msg_fmt: Format string to present message/buttons to the user

        Returns:
            A lowercased string that matches a button (or an empty string if the \
                entered option is not in the button list)

        This method returns the string entered on the command line in response to a
        question. If the entered option does not match any of the buttons, a blank
        string is returned. If you set a default and the option entered is just the
        Return key, the default string will be returned. If no default is present,
        the entered string must match one of the buttons array values. All returned
        values are lowercased. The question will be repeatedly printed to the 
        screen until a valid entry is made.

        Note that if default == "", pressing Enter is not considered a valid entry.
        """

        # make all params lowercase
        buttons = [item.lower() for item in buttons]
        default = default.lower()

        # ----------------------------------------------------------------------

        # if we passes a default
        if default != "":

            # find the default
            if not default in buttons:

                # not found, add at end of buttons
                buttons.append(default)

            # upper case it
            buttons[buttons.index(default)] = default.upper()

        # ----------------------------------------------------------------------

        # add buttons to message
        btns_all = btn_sep.join(buttons)
        str_fmt = msg_fmt.format(message, btns_all)

        # lower everything again for compare
        buttons = [item.lower() for item in buttons]

        # ----------------------------------------------------------------------

        while True:

            # ask the question, get the result
            inp = input(str_fmt)
            inp = inp.lower()

            # # no input (empty)
            if inp == "" and default != "":
                return default

            # input a button
            if inp in buttons:
                return inp

    # --------------------------------------------------------------------------
    # Compare two version strings for relativity

    def _compare_version(self, ver_old, ver_new):
        """
        Compare two version strings for relativity

        Args:
            ver_old: Old version string
            ver_new: New version string

        Returns:
            An integer representing the relativity of the two version strings.
            S_VER_SAME means the two versions are equal,
            S_VER_NEWER means new_ver is newer than old_ver (or there is no old_ver), and
            S_VER_OLDER means new_ver is older than old_ver.

        This method compares two version strings and determines which is older,
        which is newer, or if they are equal. Note that this method converts
        only the first three parts of a semantic version string
        (https://semver.org/).
        """

        # test for new install (don't try to regex)
        if ver_old == "":
            return self.S_VER_NEWER

        # test for equal (just save some cpu cycles)
        if ver_old == ver_new:
            return self.S_VER_SAME

        # compare version string parts (only x.x.x)
        res_old = re.search(self.R_VERSION, ver_old)
        res_new = re.search(self.R_VERSION, ver_new)

        # if both version strings are valid
        if res_old and res_new:

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
                    return self.S_VER_NEWER
                elif old_val > new_val:
                    return self.S_VER_OLDER
                else:
                    continue
        else:
            raise OSError(self.S_ERR_VERSION)

        # return 0 if equal
        return 0


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create an instance of the class
    inst = CNInstall()

    # run the instance
    try:
        # run main
        inst.main(
            P_DIR_ASSETS,
            P_DIR_USR_INST,
            P_FILE_CFG_INST,
            P_FILE_CFG_UNINST,
            P_DIR_VENV,
            P_FILE_REQS,
            P_FILE_DESK,
            P_FILE_DESK_ICON,
        )
    except Exception as e:
        raise e


# -)
