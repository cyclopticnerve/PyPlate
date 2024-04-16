#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pymaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module gets the project type, the project's destination dir, copies the
required dirs/files for the project type from the template to the specified
destination, and performs some initial fixes/replacements of text and path
names in the resulting files.

Run pymaker.py -h for more options.
"""

# TODO: all dict keys that are currently dunders need to be constants
# put dunders in separate .py file to share with pybaker
# figure out a regex to do this
# TODO: moving blacklist from Paths to strs and back is a PITA
# where do we need each? which do we need more?
# definitely paths in do_fix
# also this fucks up project/pyplate/conf/settings.json
# we should be storing the list from settings.py
# just do the glob/abs/ in do_fix in a tmp dict
# also see if empty blacklist sections are getting dropped after json write
# if they are, try adding None to D_BLACKLIST empty lists
# TODO: do as little computation here as possible - move it all to settings.py
# TODO: should we run potpy on a fresh project? any benefit?

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

# path to this project
# parent is src, parents[1] is PyPlate
# NB: needed to get imports from conf (bootstrap)
P_DIR_PYPLATE = Path(__file__).parents[1]
sys.path.append(str(P_DIR_PYPLATE))

# load this first so we can get lib dir name
from conf import settings as S

# add lib path to import search
sys.path.append(str(S.P_DIR_LIB))

from conf import keys as K  # type: ignore
from cnlib import cnfunctions as F  # type: ignore
from cnlib.cnformatter import CNFormatter  # type: ignore
from cnlib.cntree import CNTree  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

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
        self._dict_pp_meta = {}
        self._debug = False
        # self._path_settings = None
        # self._path_settings_def = None

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
        self._setup()

        # ----------------------------------------------------------------------
        #  do the work

        # get info
        self._get_project_info()

        # copy template
        self._copy_template()

        # copy any files that may need to be fixed
        self._do_before_fix()

        # do replacements in final project location
        self._do_fix()

        # if debug, we are done
        if self._debug:
            sys.exit()

        # do extra stuff to final dir after fix
        self._do_after_fix()

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

        # ----------------------------------------------------------------------
        # set pp cmd line stuff

        # get cmd line args
        dict_args = self._run_parser()

        # check for debug flag
        self._debug = dict_args[S.S_DBG_DEST]

        # ----------------------------------------------------------------------
        # load pp metadata

        # load from conf/metadata.json
        self._dict_pp_meta = F.load_dicts([S.P_PP_METADATA])

        # ----------------------------------------------------------------------
        # fix pp toml

        # fix our own toml file
        self._fix_pp_toml()

    # --------------------------------------------------------------------------
    # Set up and run the command line parser
    # --------------------------------------------------------------------------
    def _run_parser(self):
        """
        Set up and run the command line parser

        Returns:
            A dictionary of command line arguments

        This method sets up and runs the command line parser to minimize code
        in the main method.
        """

        # create the command line parser
        parser = argparse.ArgumentParser(formatter_class=CNFormatter)

        # add args
        self._add_args(parser)

        # get namespace object
        args = parser.parse_args()

        # convert namespace to dict
        return vars(args)

    # --------------------------------------------------------------------------
    # Add arguments to argparse parser
    # --------------------------------------------------------------------------
    def _add_args(self, parser):
        """
        Add arguments to argparse parser

        Arguments:
            parser: The parser for which to add arguments

        This method is teased out for better code maintenance.
        """

        # load description and version from metadata
        s_desc = self._dict_pp_meta["__PM_SHORT_DESC__"]
        s_ver_fmt = S.D_PRJ_DEF["__PD_VER_FMT__"]
        s_ver_num = self._dict_pp_meta['__PM_VERSION__']
        s_ver = s_ver_fmt.format(s_ver_num)
        s_url = S.D_PRJ_DEF["__PD_URL__"]

        # format help/version string
        help_ver = (
            f"{S.S_NAME_SMALL}\n"
            + f"{s_desc}\n"
            + f"{s_ver}\n"
            + f"{s_url}/{S.S_NAME_BIG}"
        )

        # set help string
        parser.description = help_ver

        # add version option
        parser.add_argument(
            f"-{S.S_VER_OPTION}",
            action=S.S_VER_ACTION,
            version=help_ver,
        )

        # add debug option
        parser.add_argument(
            f"-{S.S_DBG_OPTION}",
            action=S.S_DBG_ACTION,
            dest=S.S_DBG_DEST,
            help=S.S_DBG_HELP,
        )

    # --------------------------------------------------------------------------
    # Replace text in the pyproject.toml file
    # --------------------------------------------------------------------------
    def _fix_pp_toml(self):
        """
        Replace text in the pyproject.toml file

        Replaces things like the short description, version keywords,
        requirements, etc. in the toml file.
        """

        # check if the toml file exists
        path_toml = S.P_DIR_PYPLATE / S.S_FILE_TOML

        # default text if we can't open file
        text = ""

        # open file and get contents
        with open(path_toml, "r", encoding="UTF-8") as f:
            text = f.read()

        # NB: we do a dunder replace here because putting a dunder as the
        # default name in the toml file causes the linter to choke, so we use a
        # dummy name

        # replace name
        str_pattern = S.R_TOML_NAME
        str_val = S.S_NAME_SMALL
        str_rep = S.R_TOML_NAME_REP.format(str_val)
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        str_pattern = S.R_TOML_VERSION
        str_val = self._dict_pp_meta["__PM_VERSION__"]
        str_rep = S.R_TOML_VERSION_REP.format(str_val)
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace short description
        str_pattern = S.R_TOML_DESC
        str_val = self._dict_pp_meta["__PM_SHORT_DESC__"]
        str_rep = S.R_TOML_DESC_REP.format(str_val)
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace keywords array
        str_pattern = S.R_TOML_KEYS
        pp_keywords = self._dict_pp_meta["__PM_KEYWORDS__"]
        str_pp_keywords = [f'"{item}"' for item in pp_keywords]
        str_pp_keywords = ", ".join(str_pp_keywords)
        str_rep = S.R_TOML_KEYS_REP.format(str_pp_keywords)
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace dependencies array
        str_pattern = S.R_TOML_DEPS
        pp_py_deps = self._dict_pp_meta["__PM_PY_DEPS__"]
        list_py_deps = [item for item in pp_py_deps.keys()]
        str_pp_py_deps = [f'"{item}"' for item in list_py_deps]
        str_pp_py_deps = ", ".join(str_pp_py_deps)
        str_rep = S.R_TOML_DEPS_REP.format(str_pp_py_deps)
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # save file
        with open(path_toml, "w", encoding="UTF-8") as f:
            f.write(text)

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        S.D_PRJ_CFG.
        """

        # ----------------------------------------------------------------------
        # first question is type

        # sanity check
        type_prj = ""

        # get possible types
        list_types = [f"{key} ({val[0]})" for (key, val) in S.D_TYPES.items()]
        str_types = " | ".join(list_types)
        in_type = f"{S.S_PRJ_TYPE} [{str_types}]: "

        # loop forever until we get a valid type (or user presses Ctrl+C)
        while True:
            # ask for type of project
            type_prj = input(in_type)

            # check for valid type
            if self._check_type(type_prj):
                # at this point, type is valid so exit loop
                break

        # save project type
        S.D_PRJ_CFG["__PC_TYPE_PRJ__"] = type_prj

        # get output subdir
        dir_type = S.D_TYPES[type_prj][1]

        # ----------------------------------------------------------------------
        # next question is name
        # NB: keep asking until we get a response that is a valid name and does
        # not already exist

        # sanity check
        name_prj = ""

        # loop forever until we get a valid name (or user presses Ctrl+C)
        while True:
            # ask for name of project
            name_prj = input(f"{S.S_PRJ_NAME}: ")

            # check for valid name
            if self._check_name(name_prj):
                # set up for existence check
                tmp_dir = S.P_DIR_BASE / dir_type / name_prj

                # kill the dir if debugging
                if self._debug and tmp_dir.exists():
                    shutil.rmtree(tmp_dir)

                # check if project already exists
                if tmp_dir.exists():
                    # tell the user that the old name exists
                    print(S.S_PRJ_NAME_ERR.format(name_prj, dir_type))
                else:
                    break

        # calculate final project location
        S.D_PRJ_CFG["__PC_DIR_PRJ__"] = str(
            S.P_DIR_BASE / dir_type / name_prj
        )

        # at this point, both dir and name are valid, so store both and exit
        # NB: make sure to store the project dir as a string, so it can be
        # saved to file
        S.D_PRJ_CFG["__PC_NAME_BIG__"] = name_prj

        # calculate small name
        info_name_small = name_prj.lower()
        S.D_PRJ_CFG["__PC_NAME_SMALL__"] = info_name_small

        # ----------------------------------------------------------------------
        # here we figure out the default module name for a pkg

        # sanity check
        name_mod = info_name_small

        # if it is a project type that needs a module name, ask for it
        if S.D_PRJ_CFG["__PC_TYPE_PRJ__"] in S.L_PKG:

            # loop forever until we get a valid name (or user presses Ctrl+C)
            while True:

                # ask for name of module
                name_mod = input(f"{S.S_PRJ_NAME_MOD}: ")

                # check for valid name
                if self._check_name(name_mod):
                    break

        # set the property
        S.D_PRJ_CFG["__PC_NAME_MOD__"] = name_mod

        # ----------------------------------------------------------------------
        # here we figure out the default class name for a cli

        # sanity check
        name_class = info_name_small

        # first split if any underscores
        split_name = name_class.replace("_", " ")

        # capitalize with word in name
        split_name = split_name.title()

        # patch title together
        new_name = split_name.replace(" ", "")

        # set name in dict
        S.D_PRJ_CFG["__PC_NAME_CLASS__"] = new_name

        # ----------------------------------------------------------------------
        # calculate initial project date
        # NB: this is the initial create date for all files in the template
        # new files added to the project will have their dates set to the date
        # when pybaker was last run
        now = datetime.now()
        fmt_date = S.D_PRJ_DEF["__PD_DATE_FMT__"]
        info_date = now.strftime(fmt_date)
        S.D_PRJ_CFG["__PC_DATE__"] = info_date

        # have settings calculate user paths
        S.get_user_paths()

    # --------------------------------------------------------------------------
    # Copy template files to final location
    # --------------------------------------------------------------------------
    def _copy_template(self):
        """
        Copy template files to final location

        Gets dirs/files from template and copies them to the project dir.
        """

        # get the project final dir
        dir_prj = Path(S.D_PRJ_CFG["__PC_DIR_PRJ__"])

        # ----------------------------------------------------------------------
        # do all

        # get input dir for common dirs/files
        dir_in = S.P_DIR_TEMPLATE / S.S_DIR_ALL

        # copy common stuff
        shutil.copytree(dir_in, dir_prj)

        # ----------------------------------------------------------------------
        # iterate template type and copy/merge to project dir

        # get a path to the template dir for this project type
        prj_type = S.D_PRJ_CFG["__PC_TYPE_PRJ__"]

        # get the src dir in the template dir
        dir_template = S.P_DIR_TEMPLATE / S.D_TYPES[prj_type][2]

        # get all top level folders/files in the template type
        list_src = list(Path.iterdir(dir_template))

        # for each top level dir/file
        for item_src in list_src:

            # get destination name
            dst = dir_prj / item_src.name

            # template item is a file
            if item_src.is_file():
                # copy or overwrite
                shutil.copy2(item_src, dst)

            # template item is a dir
            else:
                # dest does not exist, copy dir
                if not dst.exists():
                    shutil.copytree(item_src, dst)

                # dest exists, merge from template to proj
                else:
                    # get all first-level items
                    list_merge = list(Path.iterdir(item_src))
                    # copy each file or dir to dest proj dir
                    for item_merge in list_merge:
                        if item_merge.is_file():
                            shutil.copy2(item_merge, dst)
                        else:
                            shutil.copytree(item_merge, dst)

    # --------------------------------------------------------------------------
    # Copy/create any other files before running _do_fix
    # --------------------------------------------------------------------------
    def _do_before_fix(self):
        """
        Copy/create any other files before running do_fix

        Adds dirs/files to the project before running the _do_fix method.
        """

        # project directory
        path_prj = S.D_PRJ_CFG["__PC_DIR_PRJ__"]
        path_prj = Path(path_prj)

        # TODO: move these computations to settings
        # path to project settings/defs
        self._path_settings = (
            path_prj / S.S_DIR_PP / S.S_DIR_CONF / S.S_FILE_SETTINGS
        )
        self._path_settings_def = (
            path_prj
            / S.S_DIR_PP
            / S.S_DIR_CONF
            / S.S_DIR_CONF_DEFS
            / S.S_FILE_SETTINGS_DEF
        )

        # path to project metadata/defs
        path_metadata = (
            path_prj / S.S_DIR_PP / S.S_DIR_CONF / S.S_FILE_METADATA
        )
        path_metadata_def = (
            path_prj
            / S.S_DIR_PP
            / S.S_DIR_CONF
            / S.S_DIR_CONF_DEFS
            / S.S_FILE_METADATA_DEF
        )

        # create pybaker's settings dict
        dict_settings = {
            K.S_KEY_PROJECT: S.D_PRJ_CFG,
            K.S_KEY_BLACKLIST: S.D_BLACKLIST,
        }

        # create all conf files and defaults
        F.save_dict([self._path_settings], dict_settings)
        F.save_dict([self._path_settings_def], dict_settings)
        F.save_dict([path_metadata], S.D_PRJ_META)
        F.save_dict([path_metadata_def], S.D_PRJ_META)

        # copy linked files
        for key, val in S.D_COPY.items():

            # first get full source path
            path_in = S.P_DIR_PYPLATE / key

            # then get full dest path
            path_out = path_prj / val

            # copy file
            if path_in.is_dir():
                shutil.copytree(path_in, path_out)
            else:
                shutil.copy(path_in, path_out)

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

        # fix up blacklist and convert relative or glob paths to absolute Path
        # objects
        self._fix_blacklist_paths()

        # TODO: we must do fix with 3 sets of dunders:
        # 1. D_PRJ_DEF
        # 2. D_PRJ_CFG
        # 3. D_METADATA

        # just shorten the names
        skip_all = S.D_BLACKLIST[K.S_KEY_SKIP_ALL]
        skip_contents = S.D_BLACKLIST[K.S_KEY_SKIP_CONTENTS]
        skip_header = S.D_BLACKLIST[K.S_KEY_SKIP_HEADER]
        skip_text = S.D_BLACKLIST[K.S_KEY_SKIP_TEXT]
        skip_path = S.D_BLACKLIST[K.S_KEY_SKIP_PATH]

        # project directory
        path_prj = S.D_PRJ_CFG["__PC_DIR_PRJ__"]
        path_prj = Path(path_prj)

        # ----------------------------------------------------------------------
        # do the fixes top down

        # walk from project dir
        # NB: note that root is a full path, dirs and files are relative to
        # root
        for root, root_dirs, root_files in os.walk(path_prj):

            # convert root into Path object
            root = Path(root)

            # skip dir if in skip_all
            if root in skip_all:
                root_dirs.clear()
                continue

            # convert files into Paths
            files = [root / f for f in root_files]

            # for each file item (not dirs, they will be handled on the next
            # iter)
            for item in files:
                # skip file if in skip_all
                if item in skip_all:
                    continue

                # fix README if it is the top-level README.md
                # NB: need to do before any other stuff, requires special
                # treatment
                if root == path_prj and item.name == S.D_README["RM_FILENAME"]:
                    self._fix_readme(item)

                # if we shouldn't skip contents
                if root not in skip_contents and item not in skip_contents:
                    # fix headers
                    if root not in skip_header and item not in skip_header:
                        self._fix_header(item)

                    # fix text
                    if root not in skip_text and item not in skip_text:
                        self._fix_text(item)

        # ----------------------------------------------------------------------
        # do the renaming bottom up

        # NB: topdown=False is required for the renaming, as we don't want to
        # rename (and thus clobber) a directory name before we rename all its
        # child dirs/files
        # note that root is a full path, dirs and files are relative to root
        for root, root_dirs, root_files in os.walk(path_prj, topdown=False):

            # convert root into Path object
            root = Path(root)

            # skip dir if in skip_all
            if root in skip_all:
                root_dirs.clear()
                continue
            # _dict_to_file(S.D_BLACKLIST, self._path_blacklist)
            # _dict_to_file(S.D_BLACKLIST, self._path_blacklist_def)
            # convert files into Paths
            files = [root / f for f in root_files]

            # for each file item (not dirs, they will be handled on the next
            # iter)
            for item in files:
                # skip file if in skip_all
                if item in skip_all:
                    continue

                # fix path
                if item not in skip_path:
                    self._fix_path(item)

            # fix current dir path
            if root not in skip_path:
                self._fix_path(root)

        # ----------------------------------------------------------------------

        # replace any dunders in blacklist after renaming files
        self._fix_blacklist_dunders()

    # --------------------------------------------------------------------------
    # Add extra dirs/files to new project after walk
    # --------------------------------------------------------------------------
    def _do_after_fix(self):
        """
        Add extra dirs/files to new project after walk

        Adds a .git (repository) dir and a .venv (virtual environment) dir to
        the project, and sets them up as necessary. These files do NOT need to
        be modified by do_fix, so we do them last.
        """

        # project directory
        path_prj = Path(S.D_PRJ_CFG["__PC_DIR_PRJ__"])

        # ----------------------------------------------------------------------
        # tree

        # get path to tree
        path_tree = path_prj / S.S_DIR_MISC
        file_tree = path_tree / S.S_FILE_TREE

        # create the file so it includes itself
        with open(file_tree, "w", encoding="UTF-8") as a_file:
            a_file.write("")

        # create tree object and call
        tree_obj = CNTree()
        tree_str = tree_obj.build_tree(
            str(path_prj),
            filter_list=S.D_BLACKLIST[K.S_KEY_SKIP_TREE],
            dir_format=S.S_TREE_DIR_FORMAT,
            file_format=S.S_TREE_FILE_FORMAT,
        )

        # write to file
        with open(file_tree, "w", encoding="UTF-8") as a_file:
            a_file.write(tree_str)

        # ----------------------------------------------------------------------
        # git

        # add git dir
        # F.sh(f"git init {str(path_prj)} -q")
        str_cmd = S.S_CMD_GIT.format(str(path_prj))
        F.sh(str_cmd)

        # ----------------------------------------------------------------------
        # venv

        # set up venv
        path_venv = path_prj / S.S_DIR_VENV
        str_cmd = S.S_CMD_VENV.format(str(path_venv))
        F.sh(str_cmd)

    # --------------------------------------------------------------------------
    # Convert items in blacklist to absolute Path objects
    # --------------------------------------------------------------------------
    def _fix_blacklist_paths(self):
        """
        Convert items in blacklist to absolute Path objects

        Strip any path separators and get absolute paths for all entries in the
        blacklist.
        """

        # project directory
        path_prj = S.D_PRJ_CFG["__PC_DIR_PRJ__"]
        path_prj = Path(path_prj)

        # remove path separators
        # NB: this is mostly for glob support, as globs cannot end in path
        # separators
        for key in S.D_BLACKLIST:
            S.D_BLACKLIST[key] = [
                item.rstrip(os.sep) for item in S.D_BLACKLIST[key]
            ]

        # support for absolute/relative/glob
        # NB: taken from cntree.py

        # for each section of blacklist
        for key, val in S.D_BLACKLIST.items():
            # convert all items in list to Path objects
            paths = [Path(item) for item in val]

            # move absolute paths to one list
            abs_paths = [item for item in paths if item.is_absolute()]

            # move relative/glob paths to another list
            other_paths = [item for item in paths if not item.is_absolute()]

            # convert relative/glob paths back to strings
            other_strings = [str(item) for item in other_paths]

            # get glob results as generators
            glob_results = [path_prj.glob(item) for item in other_strings]

            # start with absolutes
            result = abs_paths

            # for each generator
            for item in glob_results:
                # add results as whole shebang
                result += list(item)

            # set the list as the result list
            S.D_BLACKLIST[key] = result

    # --------------------------------------------------------------------------
    # Fix license/image and remove unnecessary parts of the README file
    # --------------------------------------------------------------------------
    def _fix_readme(self, path):
        """
        Fix license/image and remove unnecessary parts of the README file

        Arguments:
            path: Path for the README to remove text

        Fixes the license/image according to the S.D_PRJ_CFG settings, and
        also removes sections of the README file that are not appropriate to
        the specified type of project, such as Module/Package or CLI/GUI.
        """

        # ----------------------------------------------------------------------
        # first fix license/image

        # default text if we can't open file
        text = ""

        # open and read file
        with open(path, "r", encoding="UTF-8") as a_file:
            text = a_file.read()

        # get replacement value
        pp_license_name = S.D_PRJ_DEF["__PD_LICENSE_NAME__"]
        pp_license_img = S.D_PRJ_DEF["__PD_LICENSE_IMG__"]
        pp_license_link = S.D_PRJ_DEF["__PD_LICENSE_LINK__"]

        # the default license value
        pp_license_full = (
            f"[![{pp_license_name}]"  # alt text
            f"({pp_license_img}"  # img src
            f' "{pp_license_link}"'  # img tooltip
            f")]({pp_license_link})"  # img link
        )

        # find the license block
        str_pattern = S.R_README

        # replace text
        str_rep = S.R_README_REP.format(pp_license_full)
        text = re.sub(str_pattern, str_rep, text, flags=re.S)

        # save file
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.write(text)

        # ----------------------------------------------------------------------
        # NB: the strategy here is to go through the full README and only copy
        # lines that are:
        # 1) not in any block
        # or
        # 2) in the block we want
        # the most efficient way to do this is to have an array that receives
        # wanted lines, then return that array
        # we use a new array vs. in-situ replacement here b/c we are removing A
        # LOT OF LINES, which in-situ would result in A LOT OF BLANK LINES and
        # while that would look *ok* in the resulting Markdown, looks UGLY in
        # the source code
        # so we opt for not copying those lines.

        # just a boolean flag to say if we are kajiggering
        # if True, we are in a block we don't want to copy
        # assume False to say we want to copy
        ignore = False
        rm_delete_start = ""
        rm_delete_end = ""

        # what to ignore in the text
        # first get type of project
        type_prj = S.D_PRJ_CFG["__PC_TYPE_PRJ__"]
        for key, val in S.D_README.items():
            if type_prj == key:
                # get values for keys
                rm_delete_start = val["RM_DELETE_START"]
                rm_delete_end = val["RM_DELETE_END"]
                break

        # where to put the needed lines
        new_lines = []

        # open and read file
        with open(path, "r", encoding="UTF-8") as a_file:
            lines = a_file.readlines()

        # for each line
        for line in lines:
            # check if we have entered an invalid block
            if rm_delete_start in line:
                ignore = True

            # we're (still) in a valid block
            if not ignore:
                # iadd stuff inside valid block or outside any block
                new_lines.append(line)

            # check if we have left the invalid block
            if rm_delete_end in line:
                ignore = False

        # save lines to README.md
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.writelines(new_lines)

    # --------------------------------------------------------------------------
    # Replace dunders inside headers
    # --------------------------------------------------------------------------
    def _fix_header(self, path):
        """
        Replace dunders inside headers

        Arguments:
            path: Path for replacing header text

        Replaces header text inside a file. Given a Path object, it iterates
        the lines one by one, replacing the value found in the form of a key in
        the S.D_PRJ_CFG dictionary as it goes. When it is done, it saves the
        new lines back to the file. This replaces the __PD/__PM dunders inside
        headers. Using this method, we preserve any right-aligned text in each
        header row (see the header in this file for an example). Adapting this
        method to your style of header should be easy by modifying the regex
        pattern, and modifying L_HEADER to suit.

        NOTE: This method relies HEAVILY on the fact that the value exists, if
        using right-aligned text.

        This method will also preserve file extensions in the replaced text.

        If your files do not use any right-aligned text, then the value can be
        empty. If the value contains text which is NOT a key in S.D_PRJ_CFG,
        it will remain unchanged. This is mostly useful for the files in the
        S.D_COPY dictionary, where you want to change other header values
        but leave the filename unchanged.
        """

        # default lines
        lines = []

        # open and read file
        with open(path, "r", encoding="UTF-8") as a_file:
            lines = a_file.readlines()

        # for each line in header
        for index, line in enumerate(lines):
            # for each header key
            # for item in S.L_HEADER:
            for key, val in S.D_HEADER.items():

                # look for a header key
                str_pattern = S.R_HEADER.format(key)

                # find first instance of header pattern
                res = re.search(str_pattern, line)

                # no res, keep going
                if not res:
                    continue

                # val_found in file is group 7
                val_found = res.group(7)

                # ext (or files that start wit ha dot) is group 8
                ext = res.group(8)

                # if val is a key in S.D_PRJ_CFG
                if val_found in S.D_PRJ_CFG:
                    # get val's val (does that make sense?)
                    # so if val == '__PC_NAME_BIG__", we get the S.D_PRJ_CFG
                    # value of the key "__PC_NAME_BIG__" regardless of the key
                    # ("Project") we found
                    # that way keys ("Project") aren't tied to the values
                    # ("__PC_NAME_BIG__")
                    repl = S.D_PRJ_CFG[val_found]

                # val_found is not in S.D_PRJ_CFG
                else:
                    # the text to replace should be the text found (ie. leave
                    # it alone)
                    repl = val_found

                    # if we're looking at the Filename key
                    if key == "Filename":
                        # if it's blank (check also ext for files that start
                        # with a dot, like '.gitignore')
                        if len(val) == 0 and len(ext) == 0:
                            # use the filename of the file
                            repl = path.name
                        else:
                            # if it's not blank and not a val_found, it was
                            # probably set intentionally
                            continue

                # count what we will need without spaces
                len_res = (
                    len(res.group(1))
                    + len(repl)
                    + len(res.group(8))
                    + len("")
                    + len(res.group(10))
                )

                # make spaces
                # NB: this looks funky but it works:
                # 1. get the length of the old line (NOT always 80 since we
                # can't have trailing spaces)
                # 2. subtract 1 for newline
                # 3. subtract the other match lengths
                len_padding = len(line) - 1 - len_res
                padding = " " * len_padding

                # replace text in the line
                # str_rep = rf"\g<1>{repl}\g<8>{padding}\g<10>"
                str_rep = S.R_HEADER_REP.format(repl, padding)
                lines[index] = re.sub(str_pattern, str_rep, line)

        # save lines to file
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.writelines(lines)

    # --------------------------------------------------------------------------
    # Replace dunders inside files
    # --------------------------------------------------------------------------
    def _fix_text(self, path):
        """
        Replace dunders inside files

        Arguments:
            path: Path for replacing text

        Replaces text inside a file. Given a Path object, it iterates the lines
        one by one, replacing dunders as it goes. When it is done, it saves the
        new lines as the old file. This replaces the __PD/__PC dunders inside
        the file, excluding headers (which are already handled).
        """

        # default lines
        lines = []

        # open and read file
        with open(path, "r", encoding="UTF-8") as a_file:
            lines = a_file.readlines()

        # for each line in array
        for index, line in enumerate(lines):

            # ------------------------------------------------------------------

            # replace all text in line
            for key, val in S.D_PRJ_CFG.items():
                # find every match in line (for authors/emails in
                # pyproject.toml)
                if key in line:
                    # replace text with new value
                    line = line.replace(key, val)

            # ------------------------------------------------------------------

            # set new line with all replacements
            lines[index] = line

            # ------------------------------------------------------------------

        # save lines to file
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.writelines(lines)

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
        S.D_PRJ_CFG.
        """

        # first get the path name (we only want to change the last component)
        last_part = path.name

        # replace dunders in last path component
        for key, val in S.D_PRJ_CFG.items():
            if key in last_part:
                # replace last part with val
                last_part = last_part.replace(key, val)

        # replace the name
        path_new = path.parent / last_part

        # if it hasn't changed, skip to avoid overhead
        if path_new == path:
            return

        # do rename
        path.rename(path_new)

    # --------------------------------------------------------------------------
    # Replace any dunders in blacklist after writing them to the project dir
    # --------------------------------------------------------------------------
    def _fix_blacklist_dunders(self):
        """
        Replace any dunders in blacklist after writing them to the project dir

        Check the blacklist files for any items that contain dunders, and
        replace them, since no files in the project should have dunders in the
        name.
        """

        # project directory as a Path object
        path_prj = S.D_PRJ_CFG["__PC_DIR_PRJ__"]
        path_prj = Path(path_prj)

        def _fix_file(path_to):

            # get blacklist from settings file
            dict_all = F.load_dicts([path_to])

            # get current blacklist (as Paths)
            dict_bl = S.D_BLACKLIST

            # the fixed-up dict of replaced strings to save to file
            dict_bl_str = {}

            # for each dunder/replacement in settings
            for key_set, val_set in S.D_PRJ_CFG.items():

                # skip i18n dunder
                # TODO: get rid of this string, use proj key from K
                if key_set == "__PC_I18N__":
                    continue

                # for each key of blacklist
                for key_bl, list_bl in dict_bl.items():

                    # create a new list by replacing any dunders with
                    # their replacement values
                    list_bl_str = []

                    # each item is a Path object
                    for old_path in list_bl:

                        # so change to string
                        old_str = str(old_path)

                        # then replace
                        new_str = old_str.replace(key_set, val_set)

                        # then back to Path
                        new_path = Path(new_str)

                        # TODO: this is hacky
                        # pylint: disable=modified-iterating-list

                        # put the string in the new dict
                        list_bl_str.append(new_str)

                        # swap the Path objects in the existing list
                        list_bl.append(new_path)
                        list_bl.remove(old_path)

                        # pylint: enable=modified-iterating-list
                        # put the string list in the string dict
                        dict_bl_str[key_bl] = list_bl_str

            # save string blacklist to settings file
            dict_all[K.S_KEY_BLACKLIST] = dict_bl_str
            F.save_dict([path_to], dict_all)

        # replace stuff in regular file
        _fix_file(self._path_settings)

        # replace stuff in backup file
        _fix_file(self._path_settings_def)

    # --------------------------------------------------------------------------
    # Check project type for allowed characters
    # --------------------------------------------------------------------------
    def _check_type(self, type_prj):
        """
        Check project type for allowed characters

        Arguments:
            type_prj: Type to check for allowed characters

        Returns:
            Whether the type is valid to use

        Checks the passed type to see if it is one of the allowed project
        types.
        """

        # must have length of 1
        if len(type_prj) == 1:
            # get first char and lower case it
            char = type_prj[0]
            char = char.lower()

            # we got a valid type
            if char in S.D_TYPES:
                return True

        # nope, fail
        print(S.S_PRJ_TYPE_INVALID)
        return False

    # --------------------------------------------------------------------------
    # Check project name for allowed characters
    # --------------------------------------------------------------------------
    def _check_name(self, name_prj):
        """
        Check project name for allowed characters

        Arguments:
            name_prj: Name to check for allowed characters

        Returns:
            Whether the name is valid to use

        Checks the passed name for these criteria:
        1. non-blank name
        2. longer than 1 char
        3. starts with an alpha char
        4. ends with an alphanumeric char
        5. contains only alphanumeric chars or dash(-)/underscore (_)
        """

        # NB: there is an easier way to do this with regex:
        # ^([a-zA-Z]+[a-zA-Z\d\-_]*[a-zA-Z\d]+)$ AND OMG DID IT TAKE A LONG
        # TIME TO FIND IT! in case you were looking for it. It will give you a
        # quick yes-no answer. I don't use it here because I want to give the
        # user as much feedback as possible, so I break down the regex into
        # steps where each step explains which part of the name is wrong.

        # check for blank name
        if name_prj == "":
            return False

        if len(name_prj) == 1:
            print(S.S_PRJ_NAME_LEN)
            return False

        # match start or return false
        pattern = r"(^[a-zA-Z])"
        res = re.search(pattern, name_prj)
        if not res:
            print(S.S_PRJ_NAME_START)
            return False

        # match end or return false
        pattern = r"([a-zA-Z\d]$)"
        res = re.search(pattern, name_prj)
        if not res:
            print(S.S_PRJ_NAME_END)
            return False

        # match middle or return false
        pattern = r"(^[a-zA-Z\d\-_]*$)"
        res = re.search(pattern, name_prj)
        if not res:
            print(S.S_PRJ_NAME_CONTAIN)
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

    # run main method
    pm = PyMaker()
    pm.main()

# -)
