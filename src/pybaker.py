#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines

"""
A program to change the metadata of a PyPlate project and create a dist

This module sets the project metadata in each of the files, according to the
data present in the conf files. It then sets up the dist folder with all
necessary files to create a complete distribution of the project.

Run pybaker -h for more options.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
import gettext
import locale
from pathlib import Path
import re
import shutil
import sys

# cnlib imports
from cnformatter import CNFormatter
import cnfunctions as F
from cninstall import CNInstall
from cnpot import CNPotPy
from cntree import CNTree
from cnvenv import CNVenv

# ------------------------------------------------------------------------------
# local imports

# pylint: disable=wrong-import-position

# fudge the path to import conf stuff
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
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class PyBaker:
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class implements all the needed functionality of PyBaker, to create a
    distribution from a PyPlate project.
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

    # ide option strings
    S_ARG_IDE_OPTION = "-i"
    S_ARG_IDE_ACTION = "store_true"
    S_ARG_IDE_DEST = "IDE_DEST"
    # I18N help string for ide cmd line option
    S_ARG_IDE_HELP = _("ask for project folder when running in IDE")

    # about string
    S_ABOUT = (
        "\n"
        f"{'PyPlate/PyBaker'}\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        f"https://github.com/cyclopticnerve/PyPlate\n"
    )

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help") + "\n"

    # I18N cmd line instructions string
    S_EPILOG = _(
        "Run this program from the parent directory of the project you want "
        "to build."
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
        self._ide = False

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

        # backup for debug changes
        self._dict_dbg_old = {}

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

        # load current metadata from conf
        self._get_project_info()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_fix()

        # do replacements in final project location
        self._do_fix()

        # do extra stuff to final dir after fix
        self._do_after_fix()

        # copy project files into dist folder
        self._do_dist()

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

        # add ide option
        parser.add_argument(
            self.S_ARG_IDE_OPTION,
            dest=self.S_ARG_IDE_DEST,
            help=self.S_ARG_IDE_HELP,
            action=self.S_ARG_IDE_ACTION,
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
        self._ide = dict_args.get(self.S_ARG_IDE_DEST, False)

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

        # if yes, ask for prj name
        if self._ide:
            # ask for prj name rel to cwd
            in_str = PP.S_ASK_IDE.format(self._dir_prj)
            while True:
                prj_name = input(in_str)
                if prj_name == "":
                    continue

                # if running in ide, cwd is pyplate prj dir, so move up and down
                tmp_dir = Path(self._dir_prj / prj_name).resolve()
                if not tmp_dir.exists():
                    e_str = PP.S_ERR_NOT_EXIST.format(tmp_dir)
                    print(e_str)
                    continue

                self._dir_prj = tmp_dir
                break

        # FIXME: REMOVE BEFORE FLIGHT
        # do not run pybaker in pyplate dir
        if self._dir_prj.is_relative_to(self.P_DIR_PP):
            print(PP.S_ERR_PRJ_DIR_IS_PP)
            sys.exit()

        # check if dir_prj has pyplate folder for a valid prj
        path_pyplate = self._dir_prj / PP.S_PRJ_PP_DIR
        if not path_pyplate.exists():
            print(PP.S_ERR_NOT_PRJ)
            sys.exit()

        # ----------------------------------------------------------------------

        # set switch dicts to defaults
        self._dict_sw_block = dict(PP.D_SW_BLOCK_DEF)
        self._dict_sw_line = dict(PP.D_SW_LINE_DEF)

        # get global and calculated settings dicts in private.json
        path_prv = self._dir_prj / PP.S_PRJ_PRV_CFG
        self._dict_prv = F.load_dicts([path_prv], {})
        self._dict_prv_all = self._dict_prv[PP.S_KEY_PRV_ALL]
        self._dict_prv_prj = self._dict_prv[PP.S_KEY_PRV_PRJ]

        # get individual dicts in project.json
        path_pub = self._dir_prj / PP.S_PRJ_PUB_CFG
        self._dict_pub = F.load_dicts([path_pub], {})
        self._dict_pub_bl = self._dict_pub[PP.S_KEY_PUB_BL]
        self._dict_pub_dbg = self._dict_pub[PP.S_KEY_PUB_DBG]
        self._dict_pub_dist = self._dict_pub[PP.S_KEY_PUB_DIST]
        self._dict_pub_i18n = self._dict_pub[PP.S_KEY_PUB_I18N]
        self._dict_pub_meta = self._dict_pub[PP.S_KEY_PUB_META]

        # debug turns off all post processing to speed up process
        self._dict_dbg_old = self._dict_pub_dbg.copy()
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

        Here we just make sure the user has edited the appropriate config
        files.
        """

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
            PP.S_KEY_PUB_DBG: self._dict_dbg_old,
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
        # venv freeze

        # if venv flag is set
        if self._dict_pub_dbg[PP.S_KEY_DBG_VENV]:

            print(PP.S_ACTION_VENV, end="", flush=True)

            # get name ov venv folder and reqs file
            dir_venv = self._dict_prv_prj["__PP_NAME_VENV__"]
            file_reqs = self._dir_prj / PP.S_FILE_REQS

            # do the thing with the thing
            cv = CNVenv(self._dir_prj, dir_venv)
            try:
                cv.freeze(file_reqs)
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
                str_domain=self._dict_prv_prj["__PP_NAME_PRJ_SMALL__"],
                str_version=self._dict_pub_meta["__PP_VERSION__"],
                str_author=self._dict_prv_all["__PP_AUTHOR__"],
                str_email=self._dict_prv_all["__PP_EMAIL__"],
                # base prj dir
                dir_prj=self._dir_prj,
                # in
                list_src=self._dict_pub_i18n[PP.S_KEY_I18N_SRC],
                # out
                dir_pot=PP.S_PATH_POT,
                dir_po=PP.S_PATH_PO,
                dir_locale=PP.S_PATH_LOCALE,
                # optional in
                str_tag=PP.S_I18N_TAG,
                dict_clangs=self._dict_pub_i18n[PP.S_KEY_I18N_CLANGS],
                dict_no_ext=self._dict_pub_i18n[PP.S_KEY_I18N_NO_EXT],
                list_wlangs=self._dict_pub_i18n[PP.S_KEY_I18N_WLANGS],
                charset=self._dict_pub_i18n[PP.S_KEY_I18N_CHAR],
            )

            # make .pot, .po, and .mo files
            potpy.main()

            # do the thing
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
                dir_docs_out.mkdir(parents=True)

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
            with open(file_tree, "w", encoding=PP.S_DEF_ENCODING) as a_file:
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
            with open(file_tree, "w", encoding=PP.S_DEF_ENCODING) as a_file:
                a_file.write(tree_str)

            # we are done
            print(PP.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # fix install/uninstall cfg files

        # if install flag is set
        if self._dict_pub_dbg[PP.S_KEY_DBG_INST]:
            a_path = self._dir_prj / PP.S_FILE_INST_CFG
            if a_path.exists():
                self._fix_content(a_path)
            a_path = self._dir_prj / PP.S_FILE_UNINST_CFG
            if a_path.exists():
                self._fix_content(a_path)

    # --------------------------------------------------------------------------
    # Copy fixed files to final location
    # --------------------------------------------------------------------------
    def _do_dist(self):
        """
        Copy fixed files to final location

        Gets dirs/files from project and copies them to the dist/assets dir.
        """

        # print info
        print(PP.S_ACTION_DIST, end="", flush=True)

        # call conf before dist
        self._dict_prv, self._dict_pub = PP.do_before_dist(
            self._dir_prj, self._dict_prv, self._dict_pub
        )

        # update dicts after change
        self._reload_dicts()

        # get small name and format w/ version
        # find old dist? nuke it from orbit! it's the only way to be sure!
        a_dist = self._dir_prj / PP.S_DIR_DIST
        if a_dist.is_dir():
            shutil.rmtree(a_dist)

        # make child dir in case we nuked
        name_fmt = self._dict_prv_prj["__PP_DIST_FMT__"]
        p_dist = a_dist / name_fmt
        p_dist.mkdir(parents=True)

        # for each key, val (type, dict)
        for key, val in self._dict_pub_dist.items():

            # if it is our project type
            if key == self._dict_prv_prj["__PP_TYPE_PRJ__"]:

                # get the contents of the dict
                for k2, v2 in val.items():

                    # get src/dst rel to prj dir/dist dir
                    src = self._dir_prj / k2
                    dst = p_dist / v2
                    if not dst.exists():
                        dst.mkdir(parents=True)
                    dst = dst / src.name

                    # do the copy
                    if src.exists() and src.is_dir():
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                    elif src.exists() and src.is_file():
                        shutil.copy2(src, dst)

        # ----------------------------------------------------------------------
        # do copy lib dict

        # get list of libs for this prj type
        prj_type_short = self._dict_prv_prj["__PP_TYPE_PRJ__"]
        val = PP.D_COPY_LIB.get(prj_type_short, [])

        # copy libs
        for item in val:

            # get src/dst
            src = self.P_DIR_PP / "lib" / item
            dst = p_dist / PP.S_DIR_ASSETS / PP.S_DIR_LIB / item

            # copy dir/file
            if src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        # ----------------------------------------------------------------------
        # call conf after dist

        PP.do_after_dist(self._dir_prj, self._dict_prv, self._dict_pub)

        # update dicts after change
        self._reload_dicts()

        # done copying project files
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
        with open(path, "r", encoding=PP.S_DEF_ENCODING) as a_file:
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
        with open(path, "w", encoding=PP.S_DEF_ENCODING) as a_file:
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
    # Check if new version number is semantic
    # --------------------------------------------------------------------------
    def _check_version(self, version):
        """
        Check if new version number is semantic

        Args:
            version: New version number to check

        Returns:
            True if a valid version is found, False otherwise

        This method checks to see if the version string passed is valid for
        semantic versioning.
        """

        # match semantic version from start of string
        pattern = PP.S_SEMVER_VALID
        return re.match(pattern, version)

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
        self._dict_pub_meta = self._dict_pub[PP.S_KEY_PUB_META]


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create object
    pb = PyBaker()

    # run main method with args
    pb.main()

# -)
