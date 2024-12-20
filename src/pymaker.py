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

# FIXME: run pymaker from anywhere
# put in postflight script:
# ln -s $HOME/Documents/Projects/Python/PyPlate/src/pymaker.py $HOME/.local/bin/pymaker

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from datetime import datetime
import os
from pathlib import Path
import re
import shutil
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# paths to important dirs
# NB: needed to get imports from conf (bootstrap)
# NB: this is hardcoded so ln -s will work
P_DIR_PYPLATE_INST = Path.home() / ".config/pyplate"
P_DIR_PYPLATE = Path.home() / "Documents/Projects/Python/PyPlate"

P_DIR_PP_CONF = P_DIR_PYPLATE / "conf"
P_DIR_PP_LIB = P_DIR_PYPLATE / "lib"

P_DIR_PP_CONF_INST = P_DIR_PYPLATE / "conf"
P_DIR_PP_LIB_INST = P_DIR_PYPLATE / "lib"

sys.path.append(str(P_DIR_PP_CONF))
sys.path.append(str(P_DIR_PP_LIB))

sys.path.append(str(P_DIR_PP_CONF_INST))
sys.path.append(str(P_DIR_PP_LIB_INST))

# local imports
import pyplate_conf as C  # type: ignore
from cnlib import cnfunctions as F  # type: ignore
from cnlib.cnformatter import CNFormatter  # type: ignore
from cnlib.cntree import CNTree  # type: ignore
from cnlib.cnpot import CNPotPy  # type: ignore
from cnlib.cnvenv import CNVenv  # type: ignore
from cnlib.cnsphinx import CNSphinx  # type: ignore
from cnlib import cninstall as I  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# this is our metadata bootstrap
# NB: these should be the only strings in this file, as they should NOT be
# changed by dev

# name and desc for cmd line help
S_PP_NAME_BIG = "PyMaker"
S_PP_SHORT_DESC = (
    "A program for creating CLI/Package/GUI projects in Python from a template"
)
S_PP_VERSION = "0.0.1"

# formatted version
S_PP_VER_FMT = f"Version {S_PP_VERSION}"

# about string
S_PP_ABOUT = (
    f"{S_PP_NAME_BIG}\n"
    f"{S_PP_SHORT_DESC}\n"
    f"{S_PP_VER_FMT}\n"
    f"https://www.github.com/cyclopticnerve/PyPlate"
)

# ------------------------------------------------------------------------------
# Public classes
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
        self._dir_prj = Path()
        self._debug = False

        self._dir_current = Path()
        self._dict_rep = {}
        self._is_html = False
        self._dict_sw_block = {}
        self._dict_sw_line = {}
        self._dict_type_rep = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main method of the program
    # --------------------------------------------------------------------------
    def main(self, dir_current, debug=False):
        """
        The main method of the program

        Arguments:
            dir_prj: Path to dir where the project is being created
            debug: If True, run in debug mode (default: false)

        This method is the main entry point for the program, initializing the
        program, and performing its steps.
        """

        # set properties
        self._dir_current = Path(dir_current).resolve()
        self._debug = debug

        C.B_DEBUG = debug

        # ----------------------------------------------------------------------
        #  do the work

        # print about info
        print(S_PP_ABOUT)
        print()

        # call boilerplate code
        self._setup()

        # get info
        self._get_project_info()

        # copy template
        self._do_template()

        # call before fix
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

        # do not run pybaker on pyplate (we are not that meta YET...)
        if "pyplate" in str(self._dir_current).lower():
            print(C.S_ERR_PRJ_DIR_IS_PP)
            sys.exit(-1)

        # ----------------------------------------------------------------------

        # debug turns off some features to speed up project creation
        if self._debug:
            C.B_CMD_GIT = False
            C.B_CMD_VENV = False
            C.B_CMD_I18N = False
            C.B_CMD_DOCS = False
            C.B_CMD_TREE = False

        # set switch dicts to defaults
        self._dict_sw_block = dict(C.D_SW_BLOCK_DEF)
        self._dict_sw_line = dict(C.D_SW_LINE_DEF)

        # remove home dir from PyPlate path
        h = str(Path.home())
        p = str(P_DIR_PYPLATE)
        p = p.lstrip(h).strip("/")
        # NB: change global val
        C.D_PRV_PRJ["__PP_DEV_PP__"] = p

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        C.D_PRV_PRJ.
        """

        # ----------------------------------------------------------------------
        # maybe yell

        if self._debug:

            # yup, yell
            print(C.S_ERR_DEBUG)

        # ----------------------------------------------------------------------
        # first question is type
        # this makes the string to display in terminal

        # sanity check
        prj_type = ""

        # build the input question
        types = []
        for item in C.L_TYPES:
            s = C.S_TYPE_FMT.format(item[0], item[1])
            types.append(s)
        str_types = C.S_TYPE_JOIN.join(types)

        # format the question
        in_type = C.S_ASK_TYPE.format(str_types)

        # loop forever until we get a valid type
        while True:

            # ask for type of project (single letter)
            prj_type = input(in_type)

            # check for valid type
            if self._check_type(prj_type):
                prj_type = prj_type.lower()

                # at this point, type is valid so exit loop
                break

        # ----------------------------------------------------------------------
        # next question is name

        # sanity check
        prj_name = ""
        tmp_dir = ""

        # if in debug mode
        if self._debug:

            # get long name
            for item in C.L_TYPES:
                if item[0] == prj_type:
                    # get debug name of project
                    prj_name = f"{item[1]}_DEBUG"

            # set up for existence check
            tmp_dir = self._dir_current / prj_name

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
                prj_name = input(C.S_ASK_NAME)
                prj_name = prj_name.strip(" ")

                # check for valid name
                if self._check_name(prj_name):

                    # set up for existence check
                    tmp_dir = self._dir_current / prj_name

                    # check if project already exists
                    if tmp_dir.exists():

                        # tell the user that the old name exists
                        print(C.S_ERR_EXIST.format(tmp_dir))
                    else:
                        break

        # save global property
        self._dir_prj = tmp_dir

        # calculate small name
        name_small = prj_name.lower()

        # ----------------------------------------------------------------------
        # here we figure out the binary/package/window name for a project

        # NB: for a cli, the binary name is the project name lowercased
        # for a gui we should ask for the main window class name
        # for a package we should ask for the module name

        # sanity check
        def_name_sec = name_small
        name_sec = def_name_sec

        # if not debug, if need second name, ask for it
        if not self._debug and prj_type in C.D_NAME_SEC:

            # format question for second name
            s_name_sec = C.D_NAME_SEC[prj_type]
            s_sec_fmt = C.S_ASK_SEC.format(s_name_sec, def_name_sec)

            # loop forever until we get a valid name or empty string
            while True:

                # ask for second name
                name_new = input(s_sec_fmt)
                name_new = name_new.strip(" ")
                if name_new == "":
                    name_new = name_small

                # check for valid name
                if self._check_name(name_new):
                    name_sec = name_new
                    break

        # ----------------------------------------------------------------------
        # here we figure out the Pascal cased project name for files with a
        # class

        # do formatting
        name_class = name_small
        name_class = name_class.replace("_", " ")
        name_class = name_class.replace("-", " ")
        name_class = name_class.title()
        name_class = name_class.replace(" ", "")

        # ----------------------------------------------------------------------
        # calculate initial project date
        # NB: this is the initial create date for all files in the template
        # new files added to the project will have their dates set to the date
        # when pybaker was last run

        # get current date and format it according to dev fmt
        now = datetime.now()
        fmt_date = C.S_DATE_FMT
        info_date = now.strftime(fmt_date)

        # ----------------------------------------------------------------------
        # save stuff to prj/meta dicts

        # save project stuff
        C.D_PRV_PRJ["__PP_TYPE_PRJ__"] = prj_type
        C.D_PRV_PRJ["__PP_NAME_BIG__"] = prj_name
        C.D_PRV_PRJ["__PP_NAME_SMALL__"] = name_small
        C.D_PRV_PRJ["__PP_NAME_SEC__"] = name_sec
        C.D_PRV_PRJ["__PP_NAME_CLASS__"] = name_class
        C.D_PRV_PRJ["__PP_DATE__"] = info_date
        C.D_PRV_PRJ["__PP_NAME_VENV__"] = C.S_VENV_FMT_NAME.format(name_small)

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

        print(C.S_ACTION_COPY, end="", flush=True)

        # ----------------------------------------------------------------------
        # do template/all

        # copy template/all
        src = P_DIR_PYPLATE / C.S_DIR_ALL
        dst = self._dir_prj
        shutil.copytree(src, dst)

        # ----------------------------------------------------------------------
        # copy template/type

        # get some paths
        prj_type_short = C.D_PRV_PRJ["__PP_TYPE_PRJ__"]
        prj_type_long = ""

        # get parent of project
        for item in C.L_TYPES:
            if item[0] == prj_type_short:
                prj_type_long = item[2]
                break

        # get the src dir in the template dir
        src = P_DIR_PYPLATE / C.S_DIR_TEMPLATE / prj_type_long
        dst = self._dir_prj
        shutil.copytree(src, dst, dirs_exist_ok=True)

        # ----------------------------------------------------------------------
        # do copy dict

        # copy linked files
        for key, val in C.D_COPY.items():

            # get src/dst
            src = P_DIR_PYPLATE / key
            dst = self._dir_prj / val

            # copy dir/file
            if src.is_dir():
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)

        # ----------------------------------------------------------------------
        # do copy lib dict

        # go through dict to find list
        for key, val in C.D_COPY_LIB.items():

            # this is our type
            if key == C.D_PRV_PRJ["__PP_TYPE_PRJ__"]:

                # copy libs
                for item in val:

                    # get src/dst
                    src = P_DIR_PYPLATE / "lib" / item
                    dst = self._dir_prj / C.S_DIR_LIB / item

                    # copy dir/file
                    if src.is_dir():
                        shutil.copytree(src, dst)
                    else:
                        shutil.copy2(src, dst)

        # ----------------------------------------------------------------------
        # combine any reqs files
        # NB: this combines initial reqs from the "all" template folder and the
        # "type" template folder. these will then be installed during
        # _do_after_fix, after the venv is created
        self._fix_reqs(prj_type_long)

        print(C.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # A function to do stuff before fix
    # --------------------------------------------------------------------------
    def _do_before_fix(self):
        """
        A function to do stuff before fix

        This function does some more changes before the actual fix. Mostly it
        is used to call the do_before_fix method in pyplate_conf.py.
        """

        print(C.S_ACTION_BEFORE, end="", flush=True)

        # save fixed settings
        dict_prv = {
            C.S_KEY_PRV_ALL: C.D_PRV_ALL,
            C.S_KEY_PRV_PRJ: C.D_PRV_PRJ,
        }

        # save editable settings (blacklist/i18n etc.)
        type_prj = C.D_PRV_PRJ["__PP_TYPE_PRJ__"]
        dict_pub = {
            C.S_KEY_PUB_BL: C.D_PUB_BL,
            C.S_KEY_PUB_I18N: C.D_PUB_I18N,
            C.S_KEY_PUB_DIST: C.D_PUB_DIST[type_prj],
            C.S_KEY_PUB_META: C.D_PUB_META,
        }

        # call public before fix function
        C.do_before_fix(self._dir_prj, dict_prv, dict_pub)

        print(C.S_ACTION_DONE)

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

        print(C.S_ACTION_FIX, end="", flush=True)

        # combine dicts for string replacement
        F.combine_dicts(
            [
                C.D_PRV_ALL,
                C.D_PRV_PRJ,
                C.D_PUB_META,
            ],
            self._dict_rep,
        )

        # fix up blacklist and convert relative or glob paths to absolute Path
        # objects
        dict_paths = self._fix_blacklist_paths()

        # just shorten the names
        skip_all = dict_paths[C.S_KEY_SKIP_ALL]
        skip_contents = dict_paths[C.S_KEY_SKIP_CONTENTS]
        skip_header = dict_paths[C.S_KEY_SKIP_HEADER]
        skip_code = dict_paths[C.S_KEY_SKIP_CODE]
        skip_path = dict_paths[C.S_KEY_SKIP_PATH]

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
                    self._dict_sw_block = dict(C.D_SW_BLOCK_DEF)
                    self._dict_sw_line = dict(C.D_SW_LINE_DEF)

                    # check for header in blacklist
                    bl_hdr = True
                    if root not in skip_header and item not in skip_header:
                        bl_hdr = False

                    # check for code in blacklist
                    bl_code = True
                    if root not in skip_code and item not in skip_code:
                        bl_code = False

                    # do md/html/xml separately (needs special handling)
                    self._dict_type_rep = C.D_PY_REPL
                    suffix = (
                        f".{item.suffix}"
                        if not item.suffix.startswith(".")
                        else item.suffix
                    )
                    if suffix in C.L_EXT_MARKUP:
                        self._dict_type_rep = C.D_MU_REPL

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
        # save project settings

        # save fixed settings
        dict_prv = {
            C.S_KEY_PRV_ALL: C.D_PRV_ALL,
            C.S_KEY_PRV_PRJ: C.D_PRV_PRJ,
        }
        path_prv = self._dir_prj / C.S_PRJ_PRV_CFG
        F.save_dict(dict_prv, [path_prv])

        # save editable settings (blacklist/i18n etc.)
        type_prj = C.D_PRV_PRJ["__PP_TYPE_PRJ__"]
        dict_pub = {
            C.S_KEY_PUB_BL: C.D_PUB_BL,
            C.S_KEY_PUB_I18N: C.D_PUB_I18N,
            C.S_KEY_PUB_DIST: C.D_PUB_DIST[type_prj],
        }
        path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
        F.save_dict(dict_pub, [path_pub])

        # ----------------------------------------------------------------------
        # fix dunders in bl/i18n/dist
        self._fix_content(path_pub)

        # reload dict from fixed file
        dict_pub = F.load_dicts([path_pub])

        # ----------------------------------------------------------------------
        # save meta

        # put in metadata and save back to file
        dict_pub[C.S_KEY_PUB_META] = C.D_PUB_META
        F.save_dict(dict_pub, [path_pub])

        print(C.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # Make any necessary changes after all fixes have been done
    # --------------------------------------------------------------------------
    def _do_after_fix(self):
        """
        Make any necessary changes after all fixes have been done

        This method is called after all fixes have been completed. There should
        be no dunders in the file contents or path names. Do any further
        project modification in do_after_fix in pyplate_conf.py.
        """

        # ----------------------------------------------------------------------
        # call conf after fix

        path_prv = self._dir_prj / C.S_PRJ_PRV_CFG
        dict_prv = F.load_dicts([path_prv])
        path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
        dict_pub = F.load_dicts([path_pub])

        print(C.S_ACTION_AFTER, end="", flush=True)
        C.do_after_fix(self._dir_prj, dict_prv, dict_pub)
        print(C.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # git

        # if git flag
        if C.B_CMD_GIT:

            print(C.S_ACTION_GIT, end="", flush=True)

            # add git dir
            str_cmd = C.S_CMD_GIT.format(self._dir_prj)
            F.sh(str_cmd)

            print(C.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # venv

        # if venv flag is set
        if C.B_CMD_VENV:

            print(C.S_ACTION_VENV, end="", flush=True)

            # get name ov venv folder and reqs file
            dir_venv = C.D_PRV_PRJ["__PP_NAME_VENV__"]
            file_reqs = self._dir_prj / C.S_FILE_REQS

            # do the thing with the thing
            cv = CNVenv(self._dir_prj, dir_venv)
            try:
                cv.create()
                cv.install(file_reqs)
                print(C.S_ACTION_DONE)
            except F.CNShellError as e:
                print(C.S_ACTION_FAIL)
                print(e.message)

        # ----------------------------------------------------------------------
        # i18n

        # if i18n flag is set
        if C.B_CMD_I18N:

            print(C.S_ACTION_I18N, end="", flush=True)

            # create CNPotPy object
            potpy = CNPotPy(
                dir_src=self._dir_prj / C.S_DIR_SRC,
                str_appname=C.D_PRV_PRJ["__PP_NAME_BIG__"],
                str_version=C.D_PUB_META["__PP_VERSION__"],
                str_author=C.D_PRV_ALL["__PP_AUTHOR__"],
                str_email=C.D_PRV_ALL["__PP_EMAIL__"],
                dir_locale=self._dir_prj / C.S_DIR_LOCALE,
                dir_po=self._dir_prj / C.S_DIR_PO,
                str_domain=C.D_PRV_PRJ["__PP_NAME_SMALL__"],
                # NB: use dict_pub here b/c dunders have been fixed
                dict_clangs=dict_pub[C.S_KEY_PUB_I18N][C.S_KEY_CLANGS],
                dict_no_ext=dict_pub[C.S_KEY_PUB_I18N][C.S_KEY_NO_EXT],
                list_wlangs=dict_pub[C.S_KEY_PUB_I18N][C.S_KEY_WLANGS],
                charset=dict_pub[C.S_KEY_PUB_I18N][C.S_KEY_CHARSET],
            )

            # make .pot, .po, and .mo files
            potpy.main()

            # we are done
            print(C.S_ACTION_DONE)

            # make .desktop file
            path_desk = self._dir_prj / C.S_DIR_DESKTOP
            path_template = self._dir_prj / C.S_FILE_DESK_TEMPLATE

            if (
                path_desk.exists()
                and path_desk.is_dir()
                and path_template.exists()
                and path_template.is_file()
            ):

                # fix .desktop file
                print(C.S_ACTION_DESK, end="", flush=True)

                name_small = C.D_PRV_PRJ["__PP_NAME_SMALL__"]
                path_out_name = C.S_FILE_DESK_OUT.format(name_small)
                path_out = self._dir_prj / path_out_name
                potpy.make_desktop(path_template, path_out)

                # this .pot, .po, and .mo files
                potpy.main()

                # we are done
                print(C.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # update docs

        # if docs flag is set
        if C.B_CMD_DOCS:

            print(C.S_ACTION_DOCS, end="", flush=True)

            name = C.D_PRV_PRJ["__PP_NAME_SMALL__"]
            author = C.D_PRV_ALL["__PP_AUTHOR__"]
            version = C.D_PUB_META["__PP_VERSION__"]
            lib = C.D_PRV_ALL["__PP_DIR_LIB__"]
            # do the thing with the thing
            cs = CNSphinx(self._dir_prj, C.S_DIR_SRC, C.S_DIR_DOCS)
            try:
                cs.create(
                    name,
                    author,
                    version,
                    dirs_import=[lib],
                    theme=C.S_DOCS_THEME,
                )
                print(C.S_ACTION_DONE)
            except F.CNShellError as e:
                print(C.S_ACTION_FAIL)
                print(e.message)

        # ----------------------------------------------------------------------
        # tree
        # NB: run last so it includes .git and .venv folders
        # NB: this will wipe out all previous checks (maybe good?)

        # if tree flag is set
        if C.B_CMD_TREE:

            print(C.S_ACTION_TREE, end="", flush=True)

            # get path to tree
            file_tree = self._dir_prj / C.S_TREE_FILE

            # create the file so it includes itself
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write("")

            # create tree object and call
            tree_obj = CNTree()
            tree_str = tree_obj.build_tree(
                str(self._dir_prj),
                filter_list=C.D_PUB_BL[C.S_KEY_SKIP_TREE],
                dir_format=C.S_TREE_DIR_FORMAT,
                file_format=C.S_TREE_FILE_FORMAT,
            )

            # write to file
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write(tree_str)

            print(C.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # make install/uninstall cfg files

        # check if we need it
        prj_type = C.D_PRV_PRJ["__PP_TYPE_PRJ__"]

        # we need it
        if prj_type in C.L_MAKE_INSTALL:

            # show info
            print(C.S_ACTION_INST, end="", flush=True)

            # get params
            name = C.D_PRV_PRJ["__PP_NAME_BIG__"]
            version = C.D_PUB_META["__PP_VERSION__"]

            # get an install instance
            inst = I.CNInstall()

            # create a template install cfg file
            dict_inst = inst.make_install_cfg(
                name,
                version,
                # these are the defaults spec'd in pyplate_conf
                # they can be edited in prj/install/install.json before running
                # pybaker
                C.D_INSTALL,
            )

            # fix dunders in inst cfg file
            path_inst = self._dir_prj / C.S_FILE_INST_CFG
            F.save_dict(dict_inst, [path_inst])
            self._fix_content(path_inst)

            # create a template uninstall cfg file
            dict_uninst = inst.make_uninstall_cfg(
                name,
                # these are the defaults spec'd in pyplate_conf
                # they can be edited in prj/uninstall/uninstall.json before running
                # pybaker
                C.L_UNINSTALL,
            )

            # fix dunders in inst cfg file
            path_uninst = self._dir_prj / C.S_FILE_UNINST_CFG
            F.save_dict(dict_uninst, [path_uninst])
            self._fix_content(path_uninst)

            # show info
            print(C.S_ACTION_DONE)

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
        l_bl = C.D_PUB_BL
        for key in l_bl:
            l_bl[key] = [item.rstrip("/") for item in l_bl[key]]
        C.D_PUB_BL = l_bl

        # support for absolute/relative/glob
        # NB: taken from cntree.py

        # for each section of blacklist
        for key, val in C.D_PUB_BL.items():
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

        Arguments:
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
        with open(path, "r", encoding="UTF-8") as a_file:
            lines = a_file.readlines()

        # for each line in array
        for index, line in enumerate(lines):

            # ------------------------------------------------------------------
            # skip blank lines

            # skip blank lines, obvs
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
                str_pattern = self._dict_type_rep[C.S_KEY_HDR]
                res = re.search(str_pattern, line)
                if res:

                    # fix it
                    lines[index] = self._fix_header(line)

                    # stop on first match
                    continue

            # ------------------------------------------------------------------
            # skip any other comment lines

            str_pattern = self._dict_type_rep[C.S_KEY_COMM]
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
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.writelines(lines)

    # --------------------------------------------------------------------------
    # Replace dunders inside a file header
    # --------------------------------------------------------------------------
    def _fix_header(self, line):
        """
        Replace dunders inside a file header

        Arguments:
            line: The header line of the file in which to replace text

        Returns:
            The new header line

        Replaces text inside a header line, using a regex to match specific
        lines. Given a line, it replaces the found pattern with the replacement
        as it goes.
        """

        # sanity check
        str_pattern = self._dict_type_rep[C.S_KEY_HDR]
        res = re.search(str_pattern, line)
        if not res:
            return line

        # pull out lead, val, and pad using group match values from M
        lead = res.group(self._dict_type_rep[C.S_KEY_LEAD])
        val = res.group(self._dict_type_rep[C.S_KEY_VAL])
        pad = res.group(self._dict_type_rep[C.S_KEY_PAD])

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

        Arguments:
            line: The line of the file to replace text in

        Returns:
            The new line of code

        Replaces text inside a line. Given a line, replaces dunders as it goes.
        When it is done, it returns the new line. This replaces the __PP_*
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
        split = self._dict_type_rep[C.S_KEY_SPLIT]
        split_index = self._dict_type_rep[C.S_KEY_SPLIT_INDEX]
        matches = re.finditer(split, line)
        for match in matches:
            # if there is a match group for comment (meaning we found a
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
        self._dict_sw_line = dict(C.D_SW_LINE_DEF)

        # do the check
        self._check_switches(comm, False)

        # ----------------------------------------------------------------------

        # check for block or line replace switch
        repl = False
        if (
            self._dict_sw_block[C.S_SW_REPLACE]
            and self._dict_sw_line[C.S_SW_REPLACE] != C.I_SW_FALSE
            or self._dict_sw_line[C.S_SW_REPLACE] == C.I_SW_TRUE
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
        ver = C.D_PUB_META["__PP_VERSION__"]
        str_sch = C.S_META_VER_SEARCH
        str_rep = C.S_META_VER_REPL.format(ver)
        line = re.sub(str_sch, str_rep, line)

        # replace short desc
        desc = C.D_PUB_META["__PP_SHORT_DESC__"]
        str_sch = C.S_META_SD_SEARCH
        str_rep = C.S_META_SD_REPL.format(desc)
        line = re.sub(str_sch, str_rep, line)

        # return the (maybe replaced) line
        return line

    # --------------------------------------------------------------------------
    # Rename dirs/files in the project
    # --------------------------------------------------------------------------
    def _fix_path(self, path):
        """
        Rename dirs/files in the project

        Arguments:
            path: Path for dir/file to be renamed

        Rename dirs/files. Given a path, it renames the dir/file by replacing
        dunders in the path with their appropriate replacements from
        self._dict_rep.
        """

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

        Arguments:
            prj_type_long: the folder in template for the current project type

        This method combines reqs from the all dir used by all projects, and
        those used by specific project type (gui needs pygobject, etc).
        """

        # get sources and filter out items that don't exist
        reqs_prj = C.S_FILE_REQS_TYPE.format(prj_type_long)
        src = [
            P_DIR_PYPLATE / C.S_FILE_REQS_ALL,
            P_DIR_PYPLATE / reqs_prj,
        ]
        src = [str(item) for item in src if item.exists()]

        # get dst to put file lines
        dst = self._dir_prj / C.S_FILE_REQS

        # # the new set of lines for requirements.txt
        new_file = []

        # read reqs files and put in result
        for item in src:
            with open(item, "r", encoding="UTF-8") as a_file:
                old_file = a_file.readlines()
                old_file = [line.rstrip() for line in old_file]
                new_file = new_file + old_file

        # put combined reqs into final file
        joint = "\n".join(new_file)
        with open(dst, "w", encoding="UTF-8") as a_file:
            a_file.writelines(joint)

    # --------------------------------------------------------------------------
    # Check if line or trailing comment is a switch
    # --------------------------------------------------------------------------
    def _check_switches(self, line, block):
        """
        Check if line or trailing comment is a switch

        Arguments:
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

        # match  switches ('#|<!-- python: enable=replace', etc)
        match = re.match(self._dict_type_rep[C.S_KEY_SWITCH], line)
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
        if val == C.S_SW_ENABLE:
            dict_to_check[key] = C.I_SW_TRUE
            return True
        if val == C.S_SW_DISABLE:
            dict_to_check[key] = C.I_SW_FALSE
            return True

        # no valid switch found
        return False

    # --------------------------------------------------------------------------
    # Check project type for allowed characters
    # --------------------------------------------------------------------------
    def _check_type(self, prj_type):
        """
        Check project type for allowed characters

        Arguments:
            prj_type: Type to check for allowed characters

        Returns:
            Whether the type is valid to use

        Checks the passed type to see if it is one of the allowed project
        types.
        """

        if len(prj_type) == 0:
            return False

        # get first char and lower case it
        first_char = prj_type[0].lower()

        # we got a valid type
        for item in C.L_TYPES:
            if first_char == item[0]:
                return True

        # nope, fail
        types = []
        s = ""
        for item in C.L_TYPES:
            types.append(item[0])
        s = ", ".join(types)
        print(C.S_ERR_TYPE.format(s))
        return False

    # --------------------------------------------------------------------------
    # Check project name for allowed characters
    # --------------------------------------------------------------------------
    def _check_name(self, prj_name):
        """
        Check project name for allowed characters

        Arguments:
            prj_name: Name to check for allowed characters

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
        if len(prj_name.strip(" ")) < 2:
            print(C.S_ERR_LEN)
            return False

        # match start or return false
        pattern = C.D_NAME[C.S_KEY_NAME_START]
        res = re.search(pattern, prj_name)
        if not res:
            print(C.S_ERR_START)
            return False

        # match end or return false
        pattern = C.D_NAME[C.S_KEY_NAME_END]
        res = re.search(pattern, prj_name)
        if not res:
            print(C.S_ERR_END)
            return False

        # match middle or return false
        pattern = C.D_NAME[C.S_KEY_NAME_MID]
        res = re.search(pattern, prj_name)
        if not res:
            print(C.S_ERR_MID)
            return False

        # if we made it this far, return true
        return True


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # NB: argparse code placed here so we can run the script from the command
    # line or use it as an object

    # create the command line parser
    parser = argparse.ArgumentParser(formatter_class=CNFormatter)

    # set help string
    parser.description = S_PP_ABOUT

    # add debug option
    parser.add_argument(
        C.S_DBG_OPTION,
        action=C.S_DBG_ACTION,
        dest=C.S_DBG_DEST,
        help=C.S_DBG_HELP,
    )

    # get namespace object
    args = parser.parse_args()

    # convert namespace to dict
    dict_args = vars(args)

    # --------------------------------------------------------------------------

    # get the args
    a_dir_cur = os.getcwd()
    a_debug = dict_args.get(C.S_DBG_DEST, False)

    # create object
    pm = PyMaker()

    # run main method with args
    pm.main(a_dir_cur, a_debug)

# -)
