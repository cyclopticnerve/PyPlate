#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pymaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines

"""
A program to create a PyPlate project from a few variables

This module gets the project type, the project's destination dir, copies the
required dirs/files for the project type from the template to the specified
destination, and performs some initial fixes/replacements of text and path
names in the resulting files.

Run pymaker -h for more options.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from datetime import datetime
import gettext
import locale
from pathlib import Path
import re
import shutil
import sys

# local imports
from cnformatter import CNFormatter
import cnfunctions as F
from cninstall import CNInstall
from cnpot import CNPotPy
from cntree import CNTree
from cnvenv import CNVenv

# ------------------------------------------------------------------------------
# local imports

# pylint: disable=wrong-import-position

P_DIR_PRJ = Path(__file__).parents[1].resolve()
sys.path.append(str(P_DIR_PRJ))

import conf.pyplate as PP

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./pybaker.py

T_DOMAIN = "_pyplate"
T_DIR_PRJ = Path(__file__).parents[1].resolve()
T_DIR_LOCALE = f"{T_DIR_PRJ}/i18n/locale"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class PyMaker:
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class implements all the needed functionality of PyMaker, to create a
    project from a template.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # find path to pyplate
    P_DIR_PP = Path(__file__).parents[1].resolve()

    # --------------------------------------------------------------------------

    # I18N: short description
    S_PP_SHORT_DESC = _(
        "A program for creating and building CLI/Package/GUI projects in "
        "Python from a template"
    )

    # version string
    S_PP_VERSION = "Version 0.0.0"

    # config option strings
    S_ARG_HLP_OPTION = "-h"
    S_ARG_HLP_ACTION = "store_true"
    S_ARG_HLP_DEST = "HLP_DEST"
    # I18N: help option help
    S_ARG_HLP_HELP = _("show this help message and exit")

    # debug option strings
    S_ARG_DBG_OPTION = "-d"
    S_ARG_DBG_ACTION = "store_true"
    S_ARG_DBG_DEST = "DBG_DEST"
    # I18N help string for debug cmd line option
    S_ARG_DBG_HELP = _("enable debugging mode")

    # about string
    S_ABOUT = (
        f"{'PyPlate/PyMaker'}\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        f"https://github.com/cyclopticnerve/PyPlate\n"
    )

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help") + "\n"

    # I18N cmd line instructions string
    S_EPILOG = _(
        "Run this program from the directory where you want to create a "
        "project."
    )

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

        # set the initial values of properties

        # command line options
        self._debug = False

        # internal props
        self._dir_prj = Path()
        self._dict_rep = {}
        self._dict_type_rep = {}
        self._dict_sw_block = {}
        self._dict_sw_line = {}

        # private.json dicts
        self._dict_prv = {}
        self._dict_prv_all = {}
        self._dict_prv_prj = {}

        # project.json dicts
        self._dict_pub = {}
        self._dict_pub_bl = {}
        self._dict_pub_dbg = {}
        self._dict_pub_dist = {}
        self._dict_pub_i18n = {}
        self._dict_pub_meta = {}

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

        # ----------------------------------------------------------------------
        #  do the work

        # call boilerplate code
        self._setup()

        # ask user for project info
        self._get_project_info()

        # copy template
        self._do_template()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_fix()

        # do replacements in final project location
        self._do_fix()

        # do extra stuff to final dir after fix
        self._do_after_fix()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # NB: these are the main steps, called in order from main

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

        # ----------------------------------------------------------------------
        # use cmd line

        # create a parser object in case we need it
        parser = argparse.ArgumentParser(
            add_help=False,
            epilog=self.S_EPILOG,
            formatter_class=CNFormatter,
        )

        # add help text to about block
        print(self.S_ABOUT_HELP)

        # add help option
        parser.add_argument(
            self.S_ARG_HLP_OPTION,
            dest=self.S_ARG_HLP_DEST,
            help=self.S_ARG_HLP_HELP,
            action=self.S_ARG_HLP_ACTION,
        )

        # add debug option
        parser.add_argument(
            self.S_ARG_DBG_OPTION,
            dest=self.S_ARG_DBG_DEST,
            help=self.S_ARG_DBG_HELP,
            action=self.S_ARG_DBG_ACTION,
        )

        # get namespace object
        args = parser.parse_args()

        # convert namespace to dict
        dict_args = vars(args)

        # if -h passed, this will print and exit
        if dict_args.get(self.S_ARG_HLP_DEST, False):
            parser.print_help()
            sys.exit()

        # ----------------------------------------------------------------------

        # get the args
        self._debug = dict_args.get(self.S_ARG_DBG_DEST, False)

        # set global prop in conf
        PP.B_DEBUG = self._debug

        # ----------------------------------------------------------------------

        # maybe yell
        if self._debug:

            # yup, yell
            print(PP.S_MSG_DEBUG)

        # ----------------------------------------------------------------------
        # set self._dir_prj

        # assume we are running in the project dir
        # this is used in a lot of places, so just shorthand it
        self._dir_prj = Path.cwd()

        # do not run pyplate in pyplate dir
        if self._dir_prj.is_relative_to(self.P_DIR_PP):
            print(PP.S_ERR_PRJ_DIR_IS_PP)
            sys.exit()

        # ----------------------------------------------------------------------

        # set switch dicts to defaults
        self._dict_sw_block = dict(PP.D_SW_BLOCK_DEF)
        self._dict_sw_line = dict(PP.D_SW_LINE_DEF)

        # get global and calculated settings dicts in pyplate.py
        self._dict_prv = {
            PP.S_KEY_PRV_ALL: PP.D_PRV_ALL,
            PP.S_KEY_PRV_PRJ: PP.D_PRV_PRJ,
        }
        self._dict_prv_all = self._dict_prv[PP.S_KEY_PRV_ALL]
        self._dict_prv_prj = self._dict_prv[PP.S_KEY_PRV_PRJ]

        # get individual dicts in pyplate.py
        self._dict_pub = {
            PP.S_KEY_PUB_BL: PP.D_PUB_BL,
            PP.S_KEY_PUB_DBG: PP.D_PUB_DBG.copy(),
            PP.S_KEY_PUB_DIST: PP.D_PUB_DIST,
            PP.S_KEY_PUB_I18N: PP.D_PUB_I18N,
            PP.S_KEY_PUB_META: PP.D_PUB_META,
        }
        self._dict_pub_bl = self._dict_pub[PP.S_KEY_PUB_BL]
        self._dict_pub_dbg = self._dict_pub[PP.S_KEY_PUB_DBG]
        self._dict_pub_dist = self._dict_pub[PP.S_KEY_PUB_DIST]
        self._dict_pub_i18n = self._dict_pub[PP.S_KEY_PUB_I18N]
        self._dict_pub_meta = self._dict_pub[PP.S_KEY_PUB_META]

        # debug turns off all post processing to speed up process
        if self._debug:
            self._dict_pub_dbg[PP.S_KEY_DBG_GIT] = False
            self._dict_pub_dbg[PP.S_KEY_DBG_VENV] = False
            self._dict_pub_dbg[PP.S_KEY_DBG_I18N] = False
            self._dict_pub_dbg[PP.S_KEY_DBG_DOCS] = False
            self._dict_pub_dbg[PP.S_KEY_DBG_INST] = False
            self._dict_pub_dbg[PP.S_KEY_DBG_TREE] = False
            self._dict_pub_dbg[PP.S_KEY_DBG_DIST] = False

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        self._dict_prv_prj.
        """

        # ----------------------------------------------------------------------
        # first question is type
        # this makes the string to display in terminal

        # sanity check
        prj_type = ""

        # build the input question
        types = []
        for item in PP.L_TYPES:
            s = PP.S_TYPE_FMT.format(item[0], item[1])
            types.append(s)
        str_types = PP.S_TYPE_JOIN.join(types)

        # format the question
        in_type = PP.S_ASK_TYPE.format(str_types)

        # loop forever until we get a valid type
        while True:

            # ask for type of project (single letter)
            prj_type = input(in_type)

            # check for valid type
            if self._check_type(prj_type):
                prj_type = prj_type[0].lower()

                # at this point, type is valid so exit loop
                break

        # ----------------------------------------------------------------------
        # next question is name

        # sanity check
        cwd = Path.cwd()

        # if in debug mode
        if self._debug:

            # get long name
            for item in PP.L_TYPES:
                if item[0] == prj_type:
                    # get debug name of project
                    name_prj = f"{item[1]} DEBUG"
                    break

            # dir name, no spaces
            name_prj_big = name_prj.replace(" ", "_")

            # set up for existence check
            tmp_dir = cwd / name_prj_big

            # check if project already exists
            if tmp_dir.exists():

                # if it does exist, "nuke it from orbit! it's the only way to
                # be sure!"
                # NB: yes i know ive used this joke more than once... FUCK YOU
                # ITS FUNNY
                shutil.rmtree(tmp_dir)

        # not debug
        else:

            # loop forever until we get a valid name that does not exist
            while True:

                # ask for name of project
                name_prj = input(PP.S_ASK_NAME)
                name_prj = name_prj.strip(" ")

                # check for valid name
                if self._check_name(name_prj):

                    # dir name, no spaces
                    name_prj_big = name_prj.replace(" ", "_")

                    # set up for existence check
                    tmp_dir = cwd / name_prj_big

                    # check if project already exists
                    if tmp_dir.exists():

                        # tell the user that the old name exists
                        print(PP.S_ERR_EXIST.format(name_prj_big))
                    else:
                        break

        # save global property
        self._dir_prj = tmp_dir

        # save other names
        name_prj_small = name_prj_big.lower()
        name_prj_pascal = F.pascal_case(name_prj_small)

        # ----------------------------------------------------------------------
        # here we figure out the binary/package/window name for a project

        # NB: for a cli, the binary name is the project name lowercased
        # for a gui we should ask for the main window class name
        # for a package we should ask for the module name

        name_sec = ""
        name_sec_big = ""
        name_sec_small = ""
        name_sec_pascal = ""

        # if not debug, if need second name, ask for it
        if not self._debug and prj_type in PP.D_NAME_SEC:

            # format question for second name
            s_sec_ask = PP.D_NAME_SEC[prj_type]
            s_sec_ask_fmt = s_sec_ask.format(name_prj_small)

            # loop forever until we get a valid name or empty string
            while True:

                # ask for second name
                name_sec = input(s_sec_ask_fmt)
                name_sec = name_sec.strip(" ")

                # empty, keep default
                if name_sec == "":
                    name_sec = name_prj_small

                # check for valid name
                if self._check_name(name_sec):
                    name_sec_big = name_sec.replace(" ", "_")
                    break

            # save other names
            name_sec_small = name_sec_big.lower()
            name_sec_pascal = F.pascal_case(name_sec_small)

        # ----------------------------------------------------------------------
        # calculate initial project date
        # NB: this is the initial create date for all files in the template
        # new files added to the project will have their dates set to the date
        # when pybaker was last run

        # get current date and format it according to dev fmt
        now = datetime.now()
        fmt_date = PP.S_DATE_FMT
        info_date = now.strftime(fmt_date)

        # ----------------------------------------------------------------------
        # save stuff to prj/meta dicts

        # save project stuff
        self._dict_prv_prj["__PP_TYPE_PRJ__"] = prj_type
        self._dict_prv_prj["__PP_NAME_PRJ__"] = name_prj
        self._dict_prv_prj["__PP_NAME_PRJ_BIG__"] = name_prj_big
        self._dict_prv_prj["__PP_NAME_PRJ_SMALL__"] = name_prj_small
        self._dict_prv_prj["__PP_NAME_PRJ_PASCAL__"] = name_prj_pascal
        self._dict_prv_prj["__PP_NAME_SEC_BIG__"] = name_sec_big
        self._dict_prv_prj["__PP_NAME_SEC_SMALL__"] = name_sec_small
        self._dict_prv_prj["__PP_NAME_SEC_PASCAL__"] = name_sec_pascal
        self._dict_prv_prj["__PP_DATE__"] = info_date
        self._dict_prv_prj["__PP_NAME_VENV__"] = PP.S_VENV_FMT_NAME.format(
            name_prj_small
        )
        self._dict_prv_prj["__PP_FILE_APP__"] = PP.S_APP_FILE_FMT.format(
            name_prj_small
        )
        self._dict_prv_prj["__PP_CLASS_APP__"] = name_prj_pascal
        self._dict_prv_prj["__PP_FILE_WIN__"] = PP.S_WIN_FILE_FMT.format(
            name_sec_small
        )
        self._dict_prv_prj["__PP_CLASS_WIN__"] = name_sec_pascal

        # add dist stuff
        self._dict_pub_dist = PP.D_PUB_DIST[prj_type]

        # ----------------------------------------------------------------------

        # remove home dir from PyPlate path
        h = str(Path.home())
        p = str(self.P_DIR_PP)
        p = p.lstrip(h).strip("/")
        p = p.lstrip(h).strip("\\")
        # NB: change global val
        self._dict_prv_prj["__PP_DEV_PP__"] = p

        # blank line before printing progress
        print()

    # --------------------------------------------------------------------------
    # Copy template files to final location
    # --------------------------------------------------------------------------
    def _do_template(self):
        """
        Copy template files to final location

        Gets dirs/files from template and copies them to the project dir.
        """

        print(PP.S_ACTION_COPY, end="", flush=True)

        # ----------------------------------------------------------------------
        # do template/all

        # copy template/all
        src = self.P_DIR_PP / PP.S_PATH_TMP_ALL
        dst = self._dir_prj
        shutil.copytree(src, dst)

        # ----------------------------------------------------------------------
        # copy template/type

        # get some paths
        prj_type_short = self._dict_prv_prj["__PP_TYPE_PRJ__"]
        prj_type_long = ""

        # get parent of project
        for item in PP.L_TYPES:
            if item[0] == prj_type_short:
                prj_type_long = item[2]
                break

        # get the src dir in the template dir
        src = self.P_DIR_PP / PP.S_DIR_TEMPLATE / prj_type_long
        dst = self._dir_prj
        shutil.copytree(src, dst, dirs_exist_ok=True)

        # ----------------------------------------------------------------------
        # do copy misc

        # copy linked files
        for key, val in PP.D_COPY.items():

            # get src/dst
            src = self.P_DIR_PP / key
            dst = self._dir_prj / val

            # copy dir/file
            if src.is_dir():
                shutil.copytree(src, dst)
            elif src.is_file():
                shutil.copy2(src, dst)

        # _do_after_fix, after the venv is created
        self._fix_reqs(prj_type_long)

        print(PP.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # A function to do stuff before fix
    # --------------------------------------------------------------------------
    def _do_before_fix(self):
        """
        A function to do stuff before fix

        This function does some more changes before the actual fix. Mostly it
        is used to call the do_before_fix method in pyplate.py.
        """

        # print info
        print(PP.S_ACTION_BEFORE, end="", flush=True)

        # call public before fix function
        self._dict_prv, self._dict_pub = PP.do_before_fix(
            self._dir_prj, self._dict_prv, self._dict_pub
        )

        # reload dicts after change
        self._reload_dicts()

        # print info
        print(PP.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # Scan dirs/files in the project for replacing text
    # --------------------------------------------------------------------------
    def _do_fix(self):
        """
        Scan dirs/files in the project for replacing text

        Scans for dirs/files under the project's location. For each dir/file it
        encounters, it passes the path to a filter to determine if the file
        needs fixing based on its appearance in the blacklist.
        """

        # print info
        print(PP.S_ACTION_FIX, end="", flush=True)

        # combine dicts for string replacement
        F.combine_dicts(
            [
                self._dict_prv_all,
                self._dict_prv_prj,
                self._dict_pub_meta,
            ],
            self._dict_rep,
        )

        # fix up blacklist and convert relative or glob paths to absolute Path
        # objects
        dict_paths = self._fix_blacklist_paths()

        # just shorten the names
        skip_all = dict_paths[PP.S_KEY_SKIP_ALL]
        skip_contents = dict_paths[PP.S_KEY_SKIP_CONTENTS]
        skip_header = dict_paths[PP.S_KEY_SKIP_HEADER]
        skip_code = dict_paths[PP.S_KEY_SKIP_CODE]
        skip_path = dict_paths[PP.S_KEY_SKIP_PATH]

        # ----------------------------------------------------------------------
        # do the fixes
        # NB: root is a full path, dirs and files are relative to root
        for root, root_dirs, root_files in self._dir_prj.walk():

            # skip dir if in skip_all
            if root in skip_all:
                # NB: don't recurse into subfolders
                root_dirs.clear()
                continue

            # convert files into Paths
            files = [root / f for f in root_files]

            # for each file item
            for item in files:

                # skip file if in skip_all
                if item in skip_all:
                    continue

                # if we shouldn't skip contents
                if root not in skip_contents and item not in skip_contents:

                    # for each new file, reset block and line switches to def
                    self._dict_sw_block = dict(PP.D_SW_BLOCK_DEF)
                    self._dict_sw_line = dict(PP.D_SW_LINE_DEF)

                    # check for header in blacklist
                    bl_hdr = True
                    if root not in skip_header and item not in skip_header:
                        bl_hdr = False

                    # check for code in blacklist
                    bl_code = True
                    if root not in skip_code and item not in skip_code:
                        bl_code = False

                    # do md/html/xml separately (needs special handling)
                    self._dict_type_rep = PP.D_PY_REP
                    suffix = (
                        f".{item.suffix}"
                        if not item.suffix.startswith(".")
                        else item.suffix
                    )
                    if suffix in PP.L_EXT_MARKUP:
                        self._dict_type_rep = PP.D_MARKUP_REP

                    # fix content with appropriate dict
                    self._fix_content(item, bl_hdr, bl_code)

        # ----------------------------------------------------------------------
        # fix path
        # NB: top_down=False is required for the renaming, as we don't want to
        # rename (and thus clobber) a directory name before we rename all its
        # child dirs/files
        for root, root_dirs, root_files in self._dir_prj.walk(top_down=False):

            # skip dir if in skip_all
            if root in skip_all:
                # NB: do not recurse
                root_dirs.clear()
                continue

            # convert files into Paths
            files = [root / f for f in root_files]

            # for each file item
            for item in files:

                # skip file if in skip_all
                if item in skip_all:
                    continue

                # fix path
                if root not in skip_path and item not in skip_path:
                    self._fix_path(item)

            # fix current dir path
            if root not in skip_path:
                self._fix_path(root)

        # ----------------------------------------------------------------------
        # fix install.json version

        # get version from project.json
        version = self._dict_pub_meta["__PP_VERSION__"]

        # get install cfg
        a_file = self._dir_prj / PP.S_PATH_INST_CFG
        if a_file.exists():

            # load/change/save
            a_dict = F.load_dicts([a_file])
            a_dict[CNInstall.S_KEY_VERSION] = version
            F.save_dict(a_dict, [a_file])

        # get uninstall cfg
        a_file = self._dir_prj / PP.S_PATH_UNINST_CFG
        if a_file.exists():

            # load/change/save
            a_dict = F.load_dicts([a_file])
            a_dict[CNInstall.S_KEY_VERSION] = version
            F.save_dict(a_dict, [a_file])

        # ----------------------------------------------------------------------
        # save project settings

        # save fixed settings
        dict_prv = {
            PP.S_KEY_PRV_ALL: self._dict_prv_all,
            PP.S_KEY_PRV_PRJ: self._dict_prv_prj,
        }
        path_prv = self._dir_prj / PP.S_PRJ_PRV_CFG
        F.save_dict(dict_prv, [path_prv])

        # save editable settings (blacklist/i18n/dist, no meta)
        dict_pub = {
            PP.S_KEY_PUB_BL: self._dict_pub_bl,
            PP.S_KEY_PUB_DBG: PP.D_PUB_DBG,
            PP.S_KEY_PUB_DIST: self._dict_pub_dist,
            PP.S_KEY_PUB_I18N: self._dict_pub_i18n,
        }
        path_pub = self._dir_prj / PP.S_PRJ_PUB_CFG
        F.save_dict(dict_pub, [path_pub])

        # ----------------------------------------------------------------------
        # fix dunders in bl/i18n/dist
        self._fix_content(path_pub)

        # reload dict from fixed file
        dict_pub = F.load_dicts([path_pub])

        # ----------------------------------------------------------------------
        # save meta

        # put in metadata and save back to file
        dict_pub[PP.S_KEY_PUB_META] = self._dict_pub_meta
        F.save_dict(dict_pub, [path_pub])

        # done
        print(PP.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # Make any necessary changes after all fixes have been done
    # --------------------------------------------------------------------------
    def _do_after_fix(self):
        """
        Make any necessary changes after all fixes have been done

        This method is called after all fixes have been completed. There should
        be no dunders in the file contents or path names. Do any further
        project modification in do_after_fix in pyplate.py.
        """

        # ----------------------------------------------------------------------
        # dicts

        # reload dicts after fix
        path_prv = self._dir_prj / PP.S_PRJ_PRV_CFG
        self._dict_prv = F.load_dicts([path_prv])
        path_pub = self._dir_prj / PP.S_PRJ_PUB_CFG
        self._dict_pub = F.load_dicts([path_pub])

        # call conf after fix
        print(PP.S_ACTION_AFTER, end="", flush=True)
        self._dict_prv, self._dict_pub = PP.do_after_fix(
            self._dir_prj, self._dict_prv, self._dict_pub
        )

        # update dicts after change
        self._reload_dicts()

        # print info
        print(PP.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # git

        # if git flag
        if self._dict_pub_dbg[PP.S_KEY_DBG_GIT]:

            print(PP.S_ACTION_GIT, end="", flush=True)

            # add git dir
            cmd = PP.S_CMD_GIT_CREATE.format(self._dir_prj)
            F.sh(cmd, shell=True)

            print(PP.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # venv create

        # if venv flag is set
        if self._dict_pub_dbg[PP.S_KEY_DBG_VENV]:

            print(PP.S_ACTION_VENV, end="", flush=True)

            # get name ov venv folder and reqs file
            dir_venv = self._dict_prv_prj["__PP_NAME_VENV__"]
            file_reqs = self._dir_prj / PP.S_FILE_REQS

            # do the thing with the thing
            cv = CNVenv(self._dir_prj, dir_venv)
            try:
                cv.create()
                cv.install_reqs(file_reqs)
                print(PP.S_ACTION_DONE)
            except Exception as e:
                print(PP.S_ACTION_FAIL)
                raise e

            # ------------------------------------------------------------------
            # install libs in project venv

            print(PP.S_ACTION_LIB, end="", flush=True)

            # get activate cmd
            cmd_activate = PP.S_CMD_VENV_ACTIVATE.format(
                str(self._dir_prj), dir_venv
            )

            # start the full command
            cmd = f"{cmd_activate};"

            # get list of libs for this prj type
            prj_type_short = self._dict_prv_prj["__PP_TYPE_PRJ__"]
            val = PP.D_COPY_LIB.get(prj_type_short, [])

            # copy libs to command
            for item in val:

                # get lib
                add_path = self.P_DIR_PP / "lib" / item
                add_str = PP.S_CMD_INST_LIB.format(add_path)
                cmd += add_str + ";"

            # the command to install libs
            try:
                F.sh(cmd, shell=True)
                print(PP.S_ACTION_DONE)
            except Exception as e:
                print(PP.S_ACTION_FAIL)
                raise e

        # ----------------------------------------------------------------------
        # i18n

        # path to desktop template
        path_dsk_tmp = self._dir_prj / PP.S_FILE_DSK_TMP
        # path to desktop output
        path_dsk_out = self._dir_prj / self._dict_prv_prj["__PP_FILE_DESK__"]

        # if i18n flag is set
        if self._dict_pub_dbg[PP.S_KEY_DBG_I18N]:

            # print info
            print(PP.S_ACTION_I18N, end="", flush=True)

            # create CNPotPy object
            potpy = CNPotPy(
                # header
                str_domain=self._dict_prv_prj["__PP_NAME_PRJ_BIG__"],
                str_version=self._dict_pub_meta["__PP_VERSION__"],
                str_author=self._dict_prv_all["__PP_AUTHOR__"],
                str_email=self._dict_prv_all["__PP_EMAIL__"],
                # base prj dir
                dir_prj=self._dir_prj,
                # in
                dir_src=Path(PP.S_DIR_SRC),
                # out
                dir_i18n=self._dir_prj / PP.S_DIR_I18N,
                # optional in
                str_tag=PP.S_I18N_TAG,
                dict_clangs=self._dict_pub_i18n[PP.S_KEY_CLANGS],
                dict_no_ext=self._dict_pub_i18n[PP.S_KEY_NO_EXT],
                list_wlangs=self._dict_pub_i18n[PP.S_KEY_WLANGS],
                charset=self._dict_pub_i18n[PP.S_KEY_CHARSET],
            )

            # make .pot, .po, and .mo files
            potpy.main()

            # i18n-ify .desktop file
            if path_dsk_tmp.exists():
                potpy.make_desktop(path_dsk_tmp, path_dsk_out)

            # we are done
            print(PP.S_ACTION_DONE)

        # if no i18n, copy .desktop
        else:
            if path_dsk_tmp.exists():
                shutil.copy(path_dsk_tmp, path_dsk_out)

        # ----------------------------------------------------------------------
        # update docs

        # if docs flag is set
        if self._dict_pub_dbg[PP.S_KEY_DBG_DOCS]:

            # print info
            print(PP.S_ACTION_DOCS, end="", flush=True)

            # get template and output dirs
            dir_docs_tplt = self._dir_prj / PP.S_DIR_DOCS_TPLT
            dir_docs_out = self._dir_prj / PP.S_DIR_DOCS

            # nuke old docs
            if dir_docs_out.exists():
                shutil.rmtree(dir_docs_out)
                Path.mkdir(dir_docs_out, parents=True)

            # format cmd using pdoc template dir, output dir, and start dir
            cmd_docs = PP.S_CMD_DOC.format(
                PP.P_DIR_PP,
                f"{Path(PP.P_DIR_PP) / '.venv-pyplate'}",
                self._dir_prj,
                dir_docs_tplt,
                dir_docs_out,
                self._dir_prj / PP.S_DIR_SRC,
            )

            # the command to run pdoc
            cmd = f"{cmd_docs}"
            try:
                F.sh(cmd, shell=True)
                print(PP.S_ACTION_DONE)
            except Exception as e:
                print(PP.S_ACTION_FAIL)
                raise e

        # ----------------------------------------------------------------------
        # make install/uninstall cfg files

        # if install flag is set
        if self._dict_pub_dbg[PP.S_KEY_DBG_INST]:

            # get project type
            prj_type = self._dict_prv_prj["__PP_TYPE_PRJ__"]

            # cli/gui
            if prj_type in PP.L_APP_INSTALL:

                # show info
                print(PP.S_ACTION_INST, end="", flush=True)

                # get params
                name = self._dict_prv_prj["__PP_NAME_PRJ__"]
                version = self._dict_pub_meta["__PP_VERSION__"]

                # get an install instance
                inst = CNInstall()

                # create a template install cfg file
                dict_inst = inst.make_install_cfg(
                    name,
                    version,
                    # these are the defaults spec'd in pyplate_conf
                    # they can be edited in prj/install/install.json before
                    # running pybaker
                    PP.D_INSTALL[prj_type],
                )

                # fix dunders in inst cfg file
                path_inst = self._dir_prj / PP.S_PATH_INST_CFG
                F.save_dict(dict_inst, [path_inst])
                self._fix_content(path_inst)

                # create a template uninstall cfg file
                dict_uninst = inst.make_uninstall_cfg(
                    name,
                    version,
                    # these are the defaults spec'd in pyplate_conf
                    # they can be edited in prj/uninstall/uninstall.json before
                    # running pybaker
                    PP.D_UNINSTALL[prj_type],
                )

                # fix dunders in inst cfg file
                path_uninst = self._dir_prj / PP.S_PATH_UNINST_CFG
                F.save_dict(dict_uninst, [path_uninst])
                self._fix_content(path_uninst)

                # show info
                print(PP.S_ACTION_DONE)

            # pkg
            if prj_type in PP.L_PKG_INSTALL:

                # let user know
                print(PP.S_ACTION_INST_PKG, end="", flush=True)

                # need to activate prj venv
                dir_venv = self._dict_prv_prj["__PP_NAME_VENV__"]
                cmd_activate = PP.S_CMD_VENV_ACTIVATE.format(
                    self._dir_prj, dir_venv
                )

                # cmd to install
                cmd_install = PP.S_CMD_INSTALL_PKG.format(self._dir_prj)

                # the command to install pkg
                cmd = f"{cmd_activate};" f"{cmd_install}"
                try:
                    F.sh(cmd, shell=True)
                    print(PP.S_ACTION_DONE)
                except Exception as e:
                    print(PP.S_ACTION_FAIL)
                    raise e

        # ----------------------------------------------------------------------
        # tree
        # NB: run last so it includes .git and .venv folders
        # NB: this will wipe out all previous checks (maybe good?)

        # if tree flag is set
        if self._dict_pub_dbg[PP.S_KEY_DBG_TREE]:

            # print info
            print(PP.S_ACTION_TREE, end="", flush=True)

            # get path to tree
            file_tree = self._dir_prj / PP.S_TREE_FILE

            # create the file so it includes itself
            with open(file_tree, "w", encoding=PP.S_ENCODING) as a_file:
                a_file.write("")

            # create tree object and call
            tree_obj = CNTree(
                str(self._dir_prj),
                filter_list=self._dict_pub_bl[PP.S_KEY_SKIP_TREE],
                dir_format=PP.S_TREE_DIR_FORMAT,
                file_format=PP.S_TREE_FILE_FORMAT,
            )
            tree_str = tree_obj.main()

            # write to file
            with open(file_tree, "w", encoding=PP.S_ENCODING) as a_file:
                a_file.write(tree_str)

            # we are done
            print(PP.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # These are minor steps called from the main steps
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Convert items in blacklist to absolute Path objects
    # --------------------------------------------------------------------------
    def _fix_blacklist_paths(self):
        """
        Convert items in blacklist to absolute Path objects

        Get absolute paths for all entries in the blacklist.
        """

        # def result
        res = {}

        # remove path separators
        # NB: this is mostly for glob support, as globs cannot end in path
        # separators
        l_bl = self._dict_pub_bl
        for key in l_bl:
            l_bl[key] = [item.rstrip("/") for item in l_bl[key]]
        self._dict_pub_bl = l_bl

        # support for absolute/relative/glob
        # NB: taken from cntree.py

        # for each section of blacklist
        for key, val in self._dict_pub_bl.items():
            # convert all items in list to Path objects
            paths = [Path(item) for item in val]

            # move absolute paths to one list
            abs_paths = [item for item in paths if item.is_absolute()]

            # move relative/glob paths to another list
            other_paths = [item for item in paths if not item.is_absolute()]

            # convert relative/glob paths back to strings
            other_strings = [str(item) for item in other_paths]

            # get glob results as generators
            glob_results = [self._dir_prj.glob(item) for item in other_strings]

            # start with absolutes
            result = abs_paths

            # for each generator
            for item in glob_results:
                # add results as whole shebang
                result += list(item)

            # set the list as the result list
            res[key] = result

        # return dict with path objects
        return res

    # --------------------------------------------------------------------------
    # Fix header or code for each line in a file
    # --------------------------------------------------------------------------
    def _fix_content(self, path, bl_hdr=False, bl_code=False):
        """
        Fix header or code for each line in a file

        Args:
            path: Path for replacing text
            bl_hdr: Whether the file is blacklisted for header lines (default:
            False)
            bl_code: Whether the file is blacklisted for code lines (default:
            False)

        For the given file, loop through each line, checking to see if it is a
        header line or a code line. Ignore blank lines and comment-only lines.
        """

        # default lines
        lines = []

        # open and read file
        with open(path, "r", encoding=PP.S_ENCODING) as a_file:
            lines = a_file.readlines()

        # for each line in array
        for index, line in enumerate(lines):

            # ------------------------------------------------------------------
            # skip blank lines
            if line.strip() == "":
                continue

            # ------------------------------------------------------------------
            # check for block switches

            # second param is True if we are looking for block switch vs line
            # switch
            if self._check_switches(line, True):
                continue

            # ------------------------------------------------------------------
            # check for header

            # check if blacklisted for headers
            if not bl_hdr:

                # check if it matches header pattern
                str_pattern = self._dict_type_rep[PP.S_KEY_HDR]
                res = re.search(str_pattern, line)
                if res:

                    # fix it
                    lines[index] = self._fix_header(line)

                    # stop on first match
                    continue

            # ------------------------------------------------------------------
            # skip any other comment lines

            str_pattern = self._dict_type_rep[PP.S_KEY_COMM]
            if re.search(str_pattern, line):
                continue

            # ------------------------------------------------------------------
            # not a blank, block, header, or comment, must be code ( + comment)

            # check if blacklisted for code
            if not bl_code:

                # fix dunders in real code lines (may still have trailing
                # comments)
                lines[index] = self._fix_code(line)

        # open and write file
        with open(path, "w", encoding=PP.S_ENCODING) as a_file:
            a_file.writelines(lines)

    # --------------------------------------------------------------------------
    # Replace dunders inside a file header
    # --------------------------------------------------------------------------
    def _fix_header(self, line):
        """
        Replace dunders inside a file header

        Args:
            line: The header line of the file in which to replace text

        Returns:
            The new header line

        Replaces text inside a header line, using a regex to match specific
        lines. Given a line, it replaces the found pattern with the replacement
        as it goes.
        """

        # break apart header line
        # NB: gotta do this again, can't pass res param
        str_pattern = self._dict_type_rep[PP.S_KEY_HDR]
        res = re.search(str_pattern, line)
        if not res:
            return line

        # pull out lead, val, and pad using group match values from M
        lead = res.group(self._dict_type_rep[PP.S_KEY_LEAD])
        val = res.group(self._dict_type_rep[PP.S_KEY_VAL])
        pad = res.group(self._dict_type_rep[PP.S_KEY_PAD])

        # this is a complicated function to get the length of the spaces
        # between the key/val pair and the RAT (right-aligned text)
        tmp_val = str(val)
        old_val_len = len(tmp_val)
        for key2, val2 in self._dict_rep.items():
            if isinstance(val2, str):
                tmp_val = tmp_val.replace(key2, val2)
        new_val_len = len(tmp_val)
        val_diff = new_val_len - old_val_len

        # get new padding value based in diff key/val length
        tmp_pad = str(pad)
        tmp_rat = tmp_pad.lstrip()
        len_pad = len(tmp_pad) - len(tmp_rat) - val_diff
        pad = " " * len_pad

        # put the header line back together, adjusting for the pad len
        line = lead + tmp_val + pad + tmp_rat + "\n"

        # return
        return line

    # --------------------------------------------------------------------------
    # Replace dunders inside a file's contents
    # --------------------------------------------------------------------------
    def _fix_code(self, line):
        """
        Replace dunders inside a file's contents

        Args:
            line: The line of the file to replace text in

        Returns:
            The new line of code

        Replaces text inside a line. Given a line, replaces dunders as it goes.
        When it is done, it returns the new line. This replaces the __PP
        dunders inside the file, excluding flag switches, headers, and
        comment-only lines (all of which are previously handled in
        _fix_content).
        """

        # ----------------------------------------------------------------------
        # split the line into code and comm

        # we will split the line into two parts
        # NB: assume code is whole line (i.e. no trailing comment)
        code = line
        comm = ""

        # do the split, checking each match to see if we get a trailing comment
        split = self._dict_type_rep[PP.S_KEY_SPLIT]
        split_index = self._dict_type_rep[PP.S_KEY_SPLIT_INDEX]
        matches = re.finditer(split, line)
        for match in matches:
            # if there is a match group for hash mark (meaning we found a
            # trailing comment)
            if match.group(split_index):
                # split the line (comm includes hash mark as first char, code
                # get space between)
                split = match.start(split_index)
                code = line[:split]
                comm = line[split:]

        # ----------------------------------------------------------------------
        # check for line switches

        # for each line, reset line dict
        self._dict_sw_line = dict(PP.D_SW_LINE_DEF)

        # do the check
        self._check_switches(comm, False)

        # ----------------------------------------------------------------------

        # check for block or line replace switch
        repl = False
        if (
            self._dict_sw_block[PP.S_SW_REPLACE]
            and self._dict_sw_line[PP.S_SW_REPLACE] != PP.I_SW_FALSE
            or self._dict_sw_line[PP.S_SW_REPLACE] == PP.I_SW_TRUE
        ):
            repl = True

        # ----------------------------------------------------------------------

        # replace content using current flag setting
        if repl:
            for key, val in self._dict_rep.items():
                if isinstance(val, str):
                    code = code.replace(key, val)

        # put the line back together
        line = code + comm

        # replace version
        ver = self._dict_pub_meta["__PP_VERSION__"]
        str_sch = PP.S_META_VER_SCH
        str_rep = PP.S_META_VER_REP.format(ver)
        line = re.sub(str_sch, str_rep, line)

        # replace short desc
        desc = self._dict_pub_meta["__PP_SHORT_DESC__"]
        str_sch = PP.S_META_DESC_SCH
        str_rep = PP.S_META_DESC_REP.format(desc)
        line = re.sub(str_sch, str_rep, line)

        # return the (maybe replaced) line
        return line

    # --------------------------------------------------------------------------
    # Rename dirs/files in the project
    # --------------------------------------------------------------------------
    def _fix_path(self, path):
        """
        Rename dirs/files in the project

        Args:
            path: Path for dir/file to be renamed

        Rename dirs/files. Given a path, it renames the dir/file by replacing
        dunders in the path with their appropriate replacements from
        self._dict_rep.
        """

        # sanity check
        path = Path(path)

        # first get the path name (we only want to change the last component)
        last_part = path.name

        # # replace dunders in last path component
        for key, val in self._dict_rep.items():
            if isinstance(val, str):
                last_part = last_part.replace(key, val)

        # replace the name
        path_new = path.parent / last_part

        # if it hasn't changed, skip to avoid overhead
        if path_new == path:
            return

        # do rename
        path.rename(path_new)

    # --------------------------------------------------------------------------
    # Combine reqs from template/all and template/prj_type
    # --------------------------------------------------------------------------
    def _fix_reqs(self, prj_type_long):
        """
        Combine reqs from template/all and template/prj_type

        Args:
            prj_type_long: the folder in template for the current project type

        This method combines reqs from the all dir used by all projects, and
        those used by specific project type (gui needs pygobject, etc).
        """

        # get sources and filter out items that don't exist
        reqs_prj = PP.S_FILE_REQS_TYPE.format(prj_type_long)
        src = [
            self.P_DIR_PP / PP.S_FILE_REQS_ALL,
            self.P_DIR_PP / reqs_prj,
        ]
        src = [str(item) for item in src if item.exists()]

        # get dst to put file lines
        dst = self._dir_prj / PP.S_FILE_REQS

        # # the new set of lines for requirements.txt
        new_file = []

        # read reqs files and put in result
        for item in src:
            with open(item, "r", encoding=PP.S_ENCODING) as a_file:
                old_file = a_file.readlines()
                old_file = [line.rstrip() for line in old_file]
                new_file = new_file + old_file

        # put combined reqs into final file
        joint = "\n".join(new_file)
        with open(dst, "w", encoding=PP.S_ENCODING) as a_file:
            a_file.writelines(joint)

    # --------------------------------------------------------------------------
    # Check if line or trailing comment is a switch
    # --------------------------------------------------------------------------
    def _check_switches(self, line, block):
        """
        Check if line or trailing comment is a switch

        Args:
            line: The line to check for block switches
            block: True if we want to check a block switch, False if we want
            to check a line switch

        Returns:
            True if a valid switch is found, False otherwise

        This method checks to see if a line or trailing comment contains a
        valid switch (for either markup or regular files). If a valid switch is
        found, it sets the appropriate flag in either self._dict_sw_block or
        self._dict_sw_line and returns True.
        """

        # match  switches ('#|<!-- pyplate: enable=replace', etc)
        match = re.match(self._dict_type_rep[PP.S_KEY_SWITCH], line)
        if not match:
            return False

        # this line is a switch
        key = None
        val = None
        if match.group(1) and match.group(2):
            key = match.group(2)
            val = match.group(1)

        # which dict to modify
        dict_to_check = self._dict_sw_block
        if not block:
            dict_to_check = self._dict_sw_line

        # ditch any matches that are not valid keys/vals
        if not key or not val or not key in dict_to_check:
            return False

        # test for specific values, in case it is malformed
        if val == PP.S_SW_ENABLE:
            dict_to_check[key] = PP.I_SW_TRUE
            return True
        if val == PP.S_SW_DISABLE:
            dict_to_check[key] = PP.I_SW_FALSE
            return True

        # no valid switch found
        return False

    # --------------------------------------------------------------------------
    # Check project type for allowed characters
    # --------------------------------------------------------------------------
    def _check_type(self, prj_type):
        """
        Check project type for allowed characters

        Args:
            prj_type: Type to check for allowed characters

        Returns:
            Whether the type is valid to use

        Checks the passed type to see if it is one of the allowed project
        types.
        """

        # sanity check
        if len(prj_type) == 0:
            return False

        # get first char and lower case it
        first_char = prj_type[0].lower()

        # we got a valid type
        for item in PP.L_TYPES:
            if first_char == item[0]:
                return True

        # nope, fail
        types = []
        s = ""
        for item in PP.L_TYPES:
            types.append(item[0])
        s = ", ".join(types)
        print(PP.S_ERR_TYPE.format(s))
        return False

    # --------------------------------------------------------------------------
    # Check project name for allowed characters
    # --------------------------------------------------------------------------
    def _check_name(self, name_prj):
        """
        Check project name for allowed characters

        Args:
            name_prj: Name to check for allowed characters

        Returns:
            Whether the name is valid to use

        Checks the passed name for these criteria:
        1. longer than 1 char
        2. starts with an alpha char
        3. ends with an alphanumeric char
        4. contains only alphanumeric chars and/or dash(-) or underscore(_)
        """

        # NB: there is an easier way to do this with regex:
        # ^([a-zA-Z]+[a-zA-Z\d\-_]*[a-zA-Z\d]+)$ AND OMG DID IT TAKE A LONG
        # TIME TO FIND IT! in case you were looking for it. It will give you a
        # quick yes-no answer. I don't use it here because I want to give the
        # user as much feedback as possible, so I break down the regex into
        # steps where each step explains which part of the name is wrong.

        # check for name length
        if len(name_prj.strip(" ")) < 2:
            print(PP.S_ERR_LEN)
            return False

        # match start or return false
        pattern = PP.D_NAME[PP.S_KEY_NAME_START]
        res = re.search(pattern, name_prj)
        if not res:
            print(PP.S_ERR_START)
            return False

        # match end or return false
        pattern = PP.D_NAME[PP.S_KEY_NAME_END]
        res = re.search(pattern, name_prj)
        if not res:
            print(PP.S_ERR_END)
            return False

        # match middle or return false
        pattern = PP.D_NAME[PP.S_KEY_NAME_MID]
        res = re.search(pattern, name_prj)
        if not res:
            print(PP.S_ERR_MID)
            return False

        # if we made it this far, return true
        return True

    # --------------------------------------------------------------------------
    # Reload dicts after any outside changes
    # --------------------------------------------------------------------------
    def _reload_dicts(self):
        """
        Reload dicts after any outside changes

        This function is called when a dict is passed to another function, in
        order to keep it synced with the internal dict.
        """

        # get global and calculated settings dicts in pyplate.py
        self._dict_prv_all = self._dict_prv[PP.S_KEY_PRV_ALL]
        self._dict_prv_prj = self._dict_prv[PP.S_KEY_PRV_PRJ]

        # get individual dicts in pyplate.py
        self._dict_pub_bl = self._dict_pub[PP.S_KEY_PUB_BL]
        self._dict_pub_i18n = self._dict_pub[PP.S_KEY_PUB_I18N]
        self._dict_pub_dbg = self._dict_pub[PP.S_KEY_PUB_DBG]
        self._dict_pub_meta = self._dict_pub[PP.S_KEY_PUB_META]


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create object
    pm = PyMaker()

    # run main method with args
    pm.main()

# -)
