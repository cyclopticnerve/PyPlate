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

# DONE: make pybaker an entry in .vscode/launch.json
# DONE: add a .vscode launch for each prj type w/prj name small (or whatever
# default file)
# DONE: no full paths in dist files (any file that goes to end user)
# DONE: _fix_settings_dunders()
# DONE: MANIFEST.in, .gitignore header not fixed
# DONE: _fix header(): author/license padding wrong (works in test)
# DONE: rename pyplate/conf/project.py to private.py (private for pymaker)
# DONE: rename pyplate/conf/settings.py to pyplate.py (public for pymaker/pybaker)
# DONE: rename prj/pyplate/project.json to pybaker.json (private for pybaker)
# DONE: rename prj/pyplate/settings.json to project.json (public for pybaker)

# FIXME: make fix_header WAY simpler
# only match exactly MY headers
# of make match both w/ boolean
# or make match, auto detect rat
# if we go with rat only for me, what to do about blacklist?
# headers and text should still be used, but public fix_header should only do
# simple string replacement

# TODO: where do we use match? only where we need to check len (ie rat)
# everywhere else should just use sub for string replacements

# TODO: how does bool flag affect files in skip_headers blacklist?
#  flag  |  rat  |  res
# ---------------------
#   0    |   0   |
#   0    |   1   |
#   1    |   0   |
#   1    |   1   |

# TODO: what if you move project? what if you move PyPlate? vals should be
# updated every run and store in a dev file
# TODO: make a pyplate folder in PyPlate, put in fake pybaker so we can run
# pybaker on PyPlate project
# also need to add bl/i18n/meta file named "project.json"
# and a file with WHAT??? named "private.json"
# TODO: bools to turn on/off git, venv, tree
# TODO: print warning when in debug mode
# TODO  print warning/ask if in debug and about to clobber a dir
# TODO: flesh out use of verbose option
# TODO: move get info input format to settings.py
# TODO: move _check_name regex to settings
# TODO: make a regex tester to run regex on toml, readme, header
# TODO: make a flow list of all funcs in here
# TODO: make sure all runnable files have shebang/chmod +x
# TODO: what pybaker functions do we need here (ie. _fix_toml is normally run
# from pybaker.py)
# TODO: combine before and after fix - what REALLY needs to be done before fix?
# TODO: write a tool to scan for unused keys/consts


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
from conf import private as P

# add lib path to import search
sys.path.append(str(P.P_DIR_LIB))

from conf import keys2 as K  # type: ignore
from conf import custom_pp as S  # type: ignore
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
        self._verbose = False
        self._dict_repls = {}

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

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """

        # ----------------------------------------------------------------------
        # housekeeping

        # load from conf/metadata.json
        self._dict_pp_meta = F.load_dicts([P.P_FILE_META])

        # fix our own toml file
        self._fix_pp_toml()

        # ----------------------------------------------------------------------
        # set pp cmd line stuff

        # get cmd line args
        dict_args = self._run_parser()

        # check for flags
        self._debug = dict_args[S.S_DBG_DEST]
        self._verbose = dict_args[S.S_VER_DEST]

        # ----------------------------------------------------------------------
        # fix pp toml

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
        in_type = f"{S.S_ASK_TYPE} [{str_types}]: "

        # loop forever until we get a valid type
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

        # normal mode
        if not self._debug:

            # loop forever until we get a valid name that does not exist
            while True:
                # ask for name of project
                name_prj = input(f"{S.S_ASK_NAME}: ")

                # check for valid name
                if self._check_name(name_prj):
                    # set up for existence check
                    tmp_dir = Path.home() / S.S_DIR_BASE / dir_type / name_prj

                    # check if project already exists
                    if tmp_dir.exists():
                        # tell the user that the old name exists
                        print(S.S_ERR_EXIST.format(name_prj, dir_type))
                    else:
                        break

        # debug mode
        else:
            name_prj = f"{type_prj}_TEST"
            # kill the dir if debugging
            tmp_dir = Path.home() / S.S_DIR_BASE / dir_type / name_prj
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir)

        # calculate final project location
        p_prj = f"{S.S_DIR_BASE}{os.sep}{dir_type}{os.sep}{name_prj}"
        S.D_PRJ_CFG["__PC_DIR_PRJ__"] = str(p_prj)

        # at this point, both dir and name are valid, so store both and exit
        # NB: make sure to store the project dir as a string, so it can be
        # saved to file
        S.D_PRJ_CFG["__PC_NAME_BIG__"] = name_prj

        # calculate small name
        name_small = name_prj.lower()
        S.D_PRJ_CFG["__PC_NAME_SMALL__"] = name_small

        # ----------------------------------------------------------------------
        # here we figure out the binary/package name for a project

        # NB: for a cli, the binary name is the project name lowercased
        # TODO: for a gui...
        # for a package, the package name is the project name lowercased
        # the first module in the package needs a name to be replaced in
        # test_pkg.py (default is to use package name)
        # so if you give a module name, you would have:
        # <Project_Name>
        # |
        # - <project_name>
        #   |
        #   - <module_name.py>
        #
        # or else the default:
        # <Project_Name>
        # |
        # - <project_name>
        #   |
        #   - <project_name.py>

        # sanity check
        name_mod = name_small

        # if it is a project type that needs a module name, ask for it
        if S.D_PRJ_CFG["__PC_TYPE_PRJ__"] in S.L_NAME_MOD:

            # normal mode
            if not self._debug:
                # loop forever until we get a valid name or empty string
                while True:

                    # ask for name of module
                    s_mod = S.S_ASK_MOD.format(name_small)
                    name_mod = input(f"{s_mod}: ")
                    if name_mod == "":
                        name_mod = name_small

                    # check for valid name
                    if self._check_name(name_mod):
                        break

        # set the property
        S.D_PRJ_CFG["__PC_NAME_MOD__"] = name_mod

        # ----------------------------------------------------------------------
        # here we figure out the Pascal cased project name for files with a
        # class

        # create a new var that is a copy of name_small
        name_class = name_small

        # first split if any underscores
        name_class = name_class.replace("_", " ")

        # capitalize each word in name
        name_class = name_class.title()

        # put each word in name back together
        name_class = name_class.replace(" ", "")

        # set name in dict
        S.D_PRJ_CFG["__PC_NAME_CLASS__"] = name_class

        # ----------------------------------------------------------------------
        # calculate initial project date
        # NB: this is the initial create date for all files in the template
        # new files added to the project will have their dates set to the date
        # when pybaker was last run
        now = datetime.now()
        fmt_date = S.D_PRJ_DEF["__PD_DATE_FMT__"]
        info_date = now.strftime(fmt_date)
        S.D_PRJ_CFG["__PC_DATE__"] = info_date

        # ----------------------------------------------------------------------
        # now that we have all project info, have settings.py calculate user
        # paths
        P.get_user_paths()

    # --------------------------------------------------------------------------
    # Copy template files to final location
    # --------------------------------------------------------------------------
    def _copy_template(self):
        """
        Copy template files to final location

        Gets dirs/files from template and copies them to the project dir.
        """

        # get the project final dir
        dir_prj = Path.home() / Path(S.D_PRJ_CFG["__PC_DIR_PRJ__"])

        # ----------------------------------------------------------------------
        # do template/all

        # copy common stuff
        shutil.copytree(P.P_DIR_ALL, dir_prj)

        # ----------------------------------------------------------------------
        # do template/type

        # get a path to the template dir for this project type
        prj_type = S.D_PRJ_CFG["__PC_TYPE_PRJ__"]

        # get the src dir in the template dir
        dir_template = P.P_DIR_TEMPLATE / S.D_TYPES[prj_type][2]

        # get all top level folders/files in the template type
        list_src = list(Path.iterdir(dir_template))

        # for each top level dir/file
        for item_src in list_src:

            # get destination name
            dst = dir_prj / item_src.name

            # template item is a file
            if item_src.is_file():
                # copy file
                shutil.copy2(item_src, dst)

            # template item is a dir
            else:
                # NB: this is used if there is a dir in "all" and also a dir in
                # template with the same name
                # eg. "all" has a folder named "foo" and template has a folder
                # named "foo", the template folder's contents will be combined
                # with "all"'s contents

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
        Copy/create any other files before running _do_fix

        Adds dirs/files to the project before running the _do_fix method.
        """

        # combine dicts for string replacement
        F.combine_dicts(self._dict_repls, [S.D_PRJ_DEF, S.D_PRJ_CFG])

        # project directory
        path_prj = Path.home() / Path(S.D_PRJ_CFG["__PC_DIR_PRJ__"])

        # copy linked files
        d_copy = F.combine_dicts(S.D_COPY, [P.D_COPY])
        for key, val in d_copy.items():

            # first get full source path
            path_in = P.P_DIR_PYPLATE / key

            # then get full dest path
            path_out = path_prj / val

            # copy file
            if path_in.is_dir():
                shutil.copytree(path_in, path_out)
            else:
                shutil.copy2(path_in, path_out)

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
        dict_paths = self._get_blacklist_paths()

        # just shorten the names
        skip_all = dict_paths[K.S_KEY_SKIP_ALL]
        skip_contents = dict_paths[K.S_KEY_SKIP_CONTENTS]
        skip_header = dict_paths[K.S_KEY_SKIP_HEADER]
        skip_text = dict_paths[K.S_KEY_SKIP_TEXT]
        skip_path = dict_paths[K.S_KEY_SKIP_PATH]

        # project directory
        path_prj = Path.home() / S.D_PRJ_CFG["__PC_DIR_PRJ__"]

        # ----------------------------------------------------------------------
        # do the fixes top down

        # # walk from project dir
        # # NB: note that root is a full path, dirs and files are relative to
        # # root
        # for root, root_dirs, root_files in os.walk(path_prj):

        #     # convert root into Path object
        #     root = Path(root)

        #     # skip dir if in skip_all
        #     if root in skip_all:
        #         root_dirs.clear()
        #         continue

        #     # convert files into Paths
        #     files = [root / f for f in root_files]

        #     # for each file item (not dirs, they will be handled on the next
        #     # iter)
        #     for item in files:
        #         # skip file if in skip_all
        #         if item in skip_all:
        #             continue

        #         # fix README if it is the top-level README.md
        #         # NB: need to do before any other stuff, requires special
        #         # treatment
        #         if root == path_prj and item.name == S.D_README["RM_FILENAME"]:
        #             self._fix_readme(item)

        #         # if we shouldn't skip contents
        #         if root not in skip_contents and item not in skip_contents:
        #             # fix headers
        #             if root not in skip_header and item not in skip_header:
        #                 if S.B_HDR_RAT:
        #                     P.fix_header(item)

        #             # fix text
        #             if root not in skip_text and item not in skip_text:
        #                 self._fix_text(item)

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
                if (
                    root == path_prj
                    and item.name == S.D_PRJ_DEF["__PD_README_FILE__"]
                ):
                    self._fix_readme(item)

                # if we shouldn't skip contents
                if root not in skip_contents and item not in skip_contents:
                    # fix headers
                    if root not in skip_header and item not in skip_header:
                        if P.B_HDR_RAT:
                            P.fix_header(item)

                    # fix text
                    if root not in skip_text and item not in skip_text:
                        self._fix_text(item)

                # fix path
                if root not in skip_path and item not in skip_path:
                    r = self._fix_path(item)

                    if r:
                        print("fixed", str(item))
                        # store name in dict for string replacement
                        # S.D_PRJ_CFG["__PC_FILENAME__"] = item.name

                        # # in case we had __PC_FILENAME__
                        # if S.B_HDR_RAT:
                        #     P.fix_header(item)
                        # self._fix_text(item)

            # fix current dir path
            if root not in skip_path:
                r = self._fix_path(root)

                if r:
                    print("fixed", str(root))

    # --------------------------------------------------------------------------
    # Make any necessary changes after all fixes have been done
    # --------------------------------------------------------------------------
    def _do_after_fix(self):
        """
        Make any necessary changes after all fixes have been done

        This method is called after all fixes have been completed. There should
        be no dunders in the file contents or path names. Do any further
        project modification here.
        """

        dict_bl = F.combine_dicts(S.D_BL_AFTER, [P.D_BL_AFTER])
        F.pp(dict_bl)

        # add any final entries to blacklist
        for key, val in S.D_BL_AFTER.items():
            # add blacklist entries that we needed to fix once
            for item in val:
                S.D_BLACKLIST[key].append(item)

        # ----------------------------------------------------------------------
        # save project settings

        # project directory
        path_prj = Path.home() / S.D_PRJ_CFG["__PC_DIR_PRJ__"]

        # save project settings
        p_no_edit = path_prj / P.S_PP_PRJ
        dict_no_edit = {
            K.S_KEY_PRJ_DEF: S.D_PRJ_DEF,
            K.S_KEY_PRJ_CFG: S.D_PRJ_CFG,
        }
        F.save_dict([p_no_edit], dict_no_edit)

        # save editable settings (only blacklist and i18n for now)
        path_edit = path_prj / P.S_PP_CFG
        dict_edit = {
            K.S_KEY_BLACKLIST: S.D_BLACKLIST,
            K.S_KEY_I18N: S.D_I18N,
        }
        F.save_dict([path_edit], dict_edit)

        # replace dunders in blacklist and i18n
        self._fix_text(path_edit)

        # reload dict from fixed file
        dict_edit = F.load_dicts([path_edit])

        # put in metadata and save back to file
        dict_edit[K.S_KEY_META] = S.D_PRJ_META
        F.save_dict([path_edit], dict_edit)

        # ----------------------------------------------------------------------
        # tree

        # get path to tree
        file_tree = path_prj / S.S_FILE_TREE

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
        # purge

        dir_prj = Path.home() / S.D_PRJ_CFG["__PC_DIR_PRJ__"]
        path_prj = Path(dir_prj)

        # remove any files from settings for this project type
        prj_type = S.D_PRJ_CFG["__PC_TYPE_PRJ__"]
        list_del = S.D_PURGE.get(prj_type, [])
        for item in list_del:
            path_del = path_prj / item
            path_del.unlink()

        # ----------------------------------------------------------------------

        # if debug, we are done
        if self._debug:
            return

        # ----------------------------------------------------------------------
        # git

        # add git dir
        str_cmd = S.S_CMD_GIT.format(str(path_prj))
        F.sh(str_cmd)

        # ----------------------------------------------------------------------
        # venv

        # set up venv
        path_venv = path_prj / S.S_ALL_VENV
        str_cmd = S.S_CMD_VENV.format(str(path_venv))
        F.sh(str_cmd)

    # NB: these are minor steps called from the main steps

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
        path_toml = P.P_DIR_PYPLATE / P.S_FILE_TOML

        # default text if we can't open file
        text = ""

        # open file and get contents
        with open(path_toml, "r", encoding="UTF-8") as f:
            text = f.read()

        # replace name
        str_pattern = P.R_TOML_NAME
        str_val = P.S_NAME_SMALL
        str_rep = P.R_TOML_NAME_REP.format(str_val)
        text = re.sub(str_pattern, str_rep, text, flags=P.R_TOML_SUB_FLAGS)

        # replace version
        str_pattern = P.R_TOML_VERSION
        str_val = self._dict_pp_meta["__PM_VERSION__"]
        str_rep = P.R_TOML_VERSION_REP.format(str_val)
        text = re.sub(str_pattern, str_rep, text, flags=P.R_TOML_SUB_FLAGS)

        # replace short description
        str_pattern = P.R_TOML_DESC
        str_val = self._dict_pp_meta["__PM_SHORT_DESC__"]
        str_rep = P.R_TOML_DESC_REP.format(str_val)
        text = re.sub(str_pattern, str_rep, text, flags=P.R_TOML_SUB_FLAGS)

        # replace keywords array
        str_pattern = P.R_TOML_KEYS
        pp_keywords = self._dict_pp_meta["__PM_KEYWORDS__"]
        str_pp_keywords = [f'"{item}"' for item in pp_keywords]
        str_pp_keywords = ", ".join(str_pp_keywords)
        str_rep = P.R_TOML_KEYS_REP.format(str_pp_keywords)
        text = re.sub(str_pattern, str_rep, text, flags=P.R_TOML_SUB_FLAGS)

        # replace dependencies array
        str_pattern = P.R_TOML_DEPS
        pp_py_deps = self._dict_pp_meta["__PM_PY_DEPS__"]
        list_py_deps = [item for item in pp_py_deps.keys()]
        str_pp_py_deps = [f'"{item}"' for item in list_py_deps]
        str_pp_py_deps = ", ".join(str_pp_py_deps)
        str_rep = P.R_TOML_DEPS_REP.format(str_pp_py_deps)
        text = re.sub(str_pattern, str_rep, text, flags=P.R_TOML_SUB_FLAGS)

        # save file
        with open(path_toml, "w", encoding="UTF-8") as f:
            f.write(text)

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
        s_ver_num = self._dict_pp_meta["__PM_VERSION__"]
        s_ver = s_ver_fmt.format(s_ver_num)
        s_url = S.D_PRJ_DEF["__PD_URL__"]

        # format help/version string
        s_ver_help = (
            f"{P.S_NAME_SMALL}\n"
            f"{s_desc}\n"
            f"{s_ver}\n"
            f"{s_url}/{P.S_NAME_BIG}"
        )

        # set help string
        parser.description = s_ver_help

        # add version option
        parser.add_argument(
            f"-{S.S_VER_OPTION}",
            action=S.S_VER_ACTION,
            dest=S.S_VER_DEST,
            help=S.S_VER_HELP,
        )

        # add debug option
        parser.add_argument(
            f"-{S.S_DBG_OPTION}",
            action=S.S_DBG_ACTION,
            dest=S.S_DBG_DEST,
            help=S.S_DBG_HELP,
        )

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
        print(S.S_ERR_TYPE)
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
            print(S.S_ERR_LEN)
            return False

        # match start or return false
        pattern = r"(^[a-zA-Z])"
        res = re.search(pattern, name_prj)
        if not res:
            print(S.S_ERR_START)
            return False

        # match end or return false
        pattern = r"([a-zA-Z\d]$)"
        res = re.search(pattern, name_prj)
        if not res:
            print(S.S_ERR_END)
            return False

        # match middle or return false
        pattern = r"(^[a-zA-Z\d\-_]*$)"
        res = re.search(pattern, name_prj)
        if not res:
            print(S.S_ERR_CONTAIN)
            return False

        # if we made it this far, return true
        return True

    # --------------------------------------------------------------------------
    # Convert items in blacklist to absolute Path objects
    # --------------------------------------------------------------------------
    def _get_blacklist_paths(self):
        """
        Convert items in blacklist to absolute Path objects

        Strip any path separators and get absolute paths for all entries in the
        blacklist.
        """

        # def result
        res = {}

        # project directory
        path_prj = Path.home() / S.D_PRJ_CFG["__PC_DIR_PRJ__"]

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
            res[key] = result

        # return dict with path objects
        return res

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
        text = re.sub(str_pattern, str_rep, text, flags=S.R_RM_SUB_FLAGS)

        # save file
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.write(text)

        # ----------------------------------------------------------------------
        # NB: the strategy here is to go through the full README and only copy
        # lines that are:
        # 1. not in any block
        # or
        # 2. in the block we want
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
            for key, val in self._dict_repls.items():
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

        Returns: A bool indication whether the name changed (Note that this
        does not mean the file was renamed, only that it should be)
        Rename dirs/files. Given a path, it renames the dir/file by replacing
        dunders in the path with their appropriate replacements from
        _dict_repls.
        """

        # first get the path name (we only want to change the last component)
        last_part = path.name

        # replace dunders in last path component
        for key, val in self._dict_repls.items():
            if key in last_part:
                # replace last part with val
                last_part = last_part.replace(key, val)

        # replace the name
        path_new = path.parent / last_part

        # if it hasn't changed, skip to avoid overhead
        if path_new == path:
            return False

        # do rename
        path.rename(path_new)
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
