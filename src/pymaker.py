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
P_DIR_PYPLATE = Path(__file__).parents[1].resolve()
P_DIR_PP_LIB = P_DIR_PYPLATE / "lib"
sys.path.append(str(P_DIR_PYPLATE))
sys.path.append(str(P_DIR_PP_LIB))

# local imports
from conf import pymaker_conf as C  # type: ignore
from cnlib import cnfunctions as F  # type: ignore
from cnlib.cnformatter import CNFormatter  # type: ignore
from cnlib.cntree import CNTree  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# this is our metadata bootstrap

# get names
S_PP_NAME_BIG = "PyMaker"
S_PP_NAME_SMALL = "pymaker"
S_PP_SHORT_DESC = "A program to create a PyPlate project from a few variables"

# formatted version
S_PP_VER_FMT = f"Version {C.S_VERSION}"

# about string
S_PP_ABOUT = (
    f"{S_PP_NAME_SMALL}\n"
    f"{S_PP_SHORT_DESC}\n"
    f"{S_PP_VER_FMT}\n"
    f"https://www.github.com/cyclopticnerve/PyPlate"
)

# debug option strings
S_DBG_OPTION = "-d"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP = "enable debugging option"

# path to prj pyplate files
S_PP_PRV = "pyplate/conf/private.json"
S_PP_PRJ = "pyplate/conf/project.json"

# ------------------------------------------------------------------------------
# Path objects
# ------------------------------------------------------------------------------

# get fixed paths to PyPlate and folders

# Path to PyPlate libs
# (e.g. /home/cyclopticnerve/Documents/Projects/Python/PyPlate/lib)
P_DIR_PP_LIB = P_DIR_PYPLATE / "lib"

# Path to PyPlate template
# (e.g. /home/cyclopticnerve/Documents/Projects/Python/PyPlate/template/)
P_DIR_PP_TEMPLATE = P_DIR_PYPLATE / "template"

# Path to PyPlate template/all
# (e.g. /home/cyclopticnerve/Documents/Projects/Python/PyPlate/template/all)
P_DIR_PP_ALL = P_DIR_PP_TEMPLATE / "all"

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
        self._d_args = {}
        self._debug = False
        self._dict_rep = {}
        self._dir_prj = Path()
        self._in_trips = False

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

        # get info
        self._get_project_info()

        # copy template
        self._copy_template()

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

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """

        # ----------------------------------------------------------------------
        # set pp cmd line stuff

        # get cmd line args
        dict_args = self._run_parser()

        # check for flags
        self._debug = dict_args[S_DBG_DEST]

        # debug turns off some _do_after_fix features
        if self._debug:
            C.B_CMD_GIT = False
            C.B_CMD_VENV = False

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        C.D_PRJ_CFG.
        """

        # ----------------------------------------------------------------------
        # maybe yell

        if self._debug:

            # yep, yell
            print(C.S_ERR_DEBUG)

        # ----------------------------------------------------------------------
        # first question is type - this makes the string to display in term

        # sanity check
        prj_type = ""
        dir_prj_type = ""

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

            # ask for type of project
            prj_type = input(in_type)

            # check for valid type
            if self._check_type(prj_type):

                # at this point, type is valid so exit loop
                break

        # get output subdir
        for item in C.L_TYPES:
            if item[0] == prj_type:
                prj_type = item[2]
                dir_prj_type = item[3]

        # ----------------------------------------------------------------------
        # next question is name

        # sanity check
        prj_name = ""

        # if in debug mode
        if self._debug:

            # get debug name of project
            prj_name = f"{dir_prj_type}_DEBUG"

            # set up for existence check
            tmp_dir = Path(C.S_DIR_PRJ.format(dir_prj_type, prj_name))

            # check if project already exists
            if tmp_dir.exists():
                shutil.rmtree(tmp_dir)

        # not debug
        else:

            # loop forever until we get a valid name that does not exist
            while True:

                # ask for name of project
                prj_name = input(C.S_ASK_NAME)

                # check for valid name
                if self._check_name(prj_name):

                    # set up for existence check
                    tmp_dir = Path(C.S_DIR_PRJ.format(dir_prj_type, prj_name))

                    # check if project already exists
                    if tmp_dir.exists():

                        # tell the user that the old name exists
                        print(C.S_ERR_EXIST.format(tmp_dir))
                    else:
                        break

        # calculate small name
        name_small = prj_name.lower()

        # ------------------------------------------------------------------------------
        # get short description

        new_desc = input(C.S_ASK_DESC)

        # ----------------------------------------------------------------------
        # here we figure out the binary/package/window name for a project

        # NB: for a cli, the binary name is the project name lowercased
        # for a gui we should ask for the main window class name
        # for a package we should ask for the module name

        # sanity check (or debug)
        name_sec = name_small

        # if not debug, if need second name, ask for it
        if not self._debug and prj_type in C.D_NAME_SEC:

            # format question for second name
            s_name_sec = C.D_NAME_SEC[prj_type]
            s_sec_fmt = C.S_ASK_SEC.format(s_name_sec, name_sec)

            # loop forever until we get a valid name or empty string
            while True:

                # ask for second name
                name_new = input(s_sec_fmt)
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
        # we put it in D_PRJ_CFG just for string replacement
        now = datetime.now()
        fmt_date = C.D_PRJ_DEF["__PP_DATE_FMT__"]
        info_date = now.strftime(fmt_date)

        # ----------------------------------------------------------------------
        # save stuff to prj dict

        # save project stuff
        C.D_PRJ_CFG["__PP_TYPE_PRJ__"] = prj_type
        C.D_PRJ_CFG["__PP_NAME_BIG__"] = prj_name
        C.D_PRJ_CFG["__PP_NAME_SMALL__"] = name_small
        C.D_PRJ_META["__PP_SHORT_DESC__"] = new_desc
        C.D_PRJ_CFG["__PP_DATE__"] = info_date
        C.D_PRJ_CFG["__PP_NAME_CLASS__"] = name_class
        C.D_PRJ_CFG["__PP_NAME_SEC__"] = name_sec

        # remove home dir from PyPlate path
        h = str(Path.home())
        p = str(P_DIR_PYPLATE)
        p = p.lstrip(h).lstrip("/")
        C.D_PRJ_CFG["__PP_DEV_PP__"] = p

        # save global property
        self._dir_prj = tmp_dir

    # --------------------------------------------------------------------------
    # Copy template files to final location
    # --------------------------------------------------------------------------
    def _copy_template(self):
        """
        Copy template files to final location

        Gets dirs/files from template and copies them to the project dir.
        """

        # ----------------------------------------------------------------------
        # do template/all

        # copy common stuff
        shutil.copytree(P_DIR_PP_ALL, self._dir_prj)

        # ----------------------------------------------------------------------
        # do template/type

        # get a path to the template dir for this project type
        prj_type = C.D_PRJ_CFG["__PP_TYPE_PRJ__"]

        # get the src dir in the template dir
        dir_type = P_DIR_PP_TEMPLATE / prj_type

        # copy into existing dir
        shutil.copytree(dir_type, self._dir_prj, dirs_exist_ok=True)

        # ----------------------------------------------------------------------
        # do copy dict

        # copy linked files
        for key, val in C.D_COPY.items():

            # first get full source path
            path_in = P_DIR_PYPLATE / key

            # then get full dest path
            path_out = self._dir_prj / val

            # copy file
            if path_in.is_dir():
                shutil.copytree(path_in, path_out)
            else:
                shutil.copy2(path_in, path_out)

    # --------------------------------------------------------------------------
    # Dummy method to call "subclass" method (method in conf/public.py)
    # --------------------------------------------------------------------------
    def _do_before_fix(self):
        """
        Dummy function to call "subclass" function (function in conf/public.py)

        This function is here just so i can follow the flow of the program in
        my head better. I will be making a flowchart soon...
        """

        # call public before fix function
        C.do_before_fix()

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

        # combine dicts for string replacement
        F.combine_dicts(
            [C.D_PRJ_DEF, C.D_PRJ_DIST_DIRS, C.D_PRJ_CFG], self._dict_rep
        )

        # NB: q+d to add version and short desc to reps (these are strings)
        self._dict_rep["__PP_VERSION__"] = C.D_PRJ_META["__PP_VERSION__"]
        self._dict_rep["__PP_SHORT_DESC__"] = C.D_PRJ_META["__PP_SHORT_DESC__"]

        # fix up blacklist and convert relative or glob paths to absolute Path
        # objects
        dict_paths = self._get_blacklist_paths()

        # just shorten the names
        skip_all = dict_paths[C.S_KEY_SKIP_ALL]
        skip_contents = dict_paths[C.S_KEY_SKIP_CONTENTS]
        skip_header = dict_paths[C.S_KEY_SKIP_HEADER]
        skip_code = dict_paths[C.S_KEY_SKIP_CODE]
        skip_path = dict_paths[C.S_KEY_SKIP_PATH]

        # ----------------------------------------------------------------------
        # do the fixes bottom up
        # NB: topdown=False is required for the renaming, as we don't want to
        # rename (and thus clobber) a directory name before we rename all its
        # child dirs/files
        # note that root is a full path, dirs and files are relative to root
        for root, root_dirs, root_files in self._dir_prj.walk(top_down=False):

            # convert root into Path object
            # root = Path(root)

            # skip dir if in skip_all
            if root in skip_all:
                root_dirs.clear()
                continue

            # convert files into Paths
            files = [root / f for f in root_files]

            # for each file item
            for item in files:

                # skip file if in skip_all
                if item in skip_all:
                    continue

                # fix README if it is the top-level README.md
                # NB: need to do before any other stuff, requires special
                # treatment
                if item == self._dir_prj / C.D_PRJ_DEF["__PP_README_FILE__"]:
                    self._fix_readme(item)

                # if we shouldn't skip contents
                if root not in skip_contents and item not in skip_contents:

                    # check for header bl
                    bl_hdr = True
                    if root not in skip_header and item not in skip_header:
                        bl_hdr = False

                    # check for code blacklist
                    bl_code = True
                    if root not in skip_code and item not in skip_code:
                        bl_code = False

                    # fix text
                    self._fix_content(item, bl_hdr, bl_code)

                # fix path
                if root not in skip_path and item not in skip_path:
                    self._fix_path(item)

            # fix current dir path
            if root not in skip_path:
                self._fix_path(root)

    # --------------------------------------------------------------------------
    # Make any necessary changes after all fixes have been done
    # --------------------------------------------------------------------------
    def _do_after_fix(self):
        """
        Make any necessary changes after all fixes have been done

        This method is called after all fixes have been completed. There should
        be no dunders in the file or path names. Do any further project
        modification here.
        """

        # ----------------------------------------------------------------------
        # save project settings

        # save project settings
        dict_no_edit = {
            C.S_KEY_PRJ_DEF: C.D_PRJ_DEF,
            C.S_KEY_PRJ_DIST_DIRS: C.D_PRJ_DIST_DIRS,
            C.S_KEY_PRJ_CFG: C.D_PRJ_CFG,
        }
        path_no_edit = self._dir_prj / S_PP_PRV
        F.save_dict(dict_no_edit, [path_no_edit])

        # save editable settings (only blacklist and i18n for now)
        path_edit = self._dir_prj / S_PP_PRJ
        dict_edit = {
            C.S_KEY_BLACKLIST: C.D_BLACKLIST,
            C.S_KEY_I18N: C.D_I18N,
        }
        F.save_dict(dict_edit, [path_edit])

        # ----------------------------------------------------------------------
        # fix dunders in bl/i18n

        # replace dunders in blacklist and i18n
        self._fix_content(path_edit, False, False)

        # reload dict from fixed file
        dict_edit = F.load_dicts([path_edit])

        # put in metadata and save back to file
        dict_edit[C.S_KEY_META] = C.D_PRJ_META
        F.save_dict(dict_edit, [path_edit])

        # ----------------------------------------------------------------------
        # purge

        # remove any files from settings for this project type
        prj_type = C.D_PRJ_CFG["__PP_TYPE_PRJ__"]
        list_del = C.D_PURGE.get(prj_type, [])
        for item in list_del:
            path_del = self._dir_prj / item
            path_del.unlink()

        # ----------------------------------------------------------------------
        # git

        # if git flag is set
        if C.B_CMD_GIT:

            # add git dir
            str_cmd = C.S_GIT_CMD.format(str(self._dir_prj))
            F.sh(str_cmd)

        # ----------------------------------------------------------------------
        # venv

        # if venv flag is set
        if C.B_CMD_VENV:

            # set up venv
            path_venv = self._dir_prj / C.S_ALL_VENV
            str_cmd = C.S_VENV_CMD.format(str(path_venv))
            F.sh(str_cmd)

        # ----------------------------------------------------------------------
        # tree
        # NB: run last so it includes .git and .venv folders

        # if tree flag is set
        if C.B_CMD_TREE:

            # get path to tree
            file_tree = self._dir_prj / C.S_TREE_FILE

            # create the file so it includes itself
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write("")

            # create tree object and call
            tree_obj = CNTree()
            tree_str = tree_obj.build_tree(
                str(self._dir_prj),
                filter_list=C.D_BLACKLIST[C.S_KEY_SKIP_TREE],
                dir_format=C.S_TREE_DIR_FORMAT,
                file_format=C.S_TREE_FILE_FORMAT,
            )

            # write to file
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write(tree_str)

        # call public after fix
        C.do_after_fix()  # nothing

    # --------------------------------------------------------------------------
    # NB: these are minor steps called from the main steps

    # --------------------------------------------------------------------------
    # Set up and run the command line parser
    # --------------------------------------------------------------------------
    def _run_parser(self):
        """
        Set up and run the command line parser

        Returns: A dictionary of command line arguments

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
        self._d_args = vars(args)

        return self._d_args

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

        # set help string
        parser.description = S_PP_ABOUT

        # add debug option
        parser.add_argument(
            S_DBG_OPTION,
            action=S_DBG_ACTION,
            dest=S_DBG_DEST,
            help=S_DBG_HELP,
        )

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

        # must have length of 1
        # if len(prj_type) == 1:
        # get first char and lower case it
        first_char = prj_type[0]
        first_char = first_char.lower()

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
        if prj_name == "":
            return False

        if len(prj_name) == 1:
            print(C.S_ERR_LEN)
            return False

        # match start or return false
        # pattern = r"(^[a-zA-Z])"
        pattern = C.R_PRJ_START
        res = re.search(pattern, prj_name)
        if not res:
            print(C.S_ERR_START)
            return False

        # match end or return false
        # pattern = r"([a-zA-Z\d]$)"
        pattern = C.R_PRJ_END
        res = re.search(pattern, prj_name)
        if not res:
            print(C.S_ERR_END)
            return False

        # match middle or return false
        # pattern = r"(^[a-zA-Z\d\-_]*$)"
        pattern = C.R_PRJ_MID
        res = re.search(pattern, prj_name)
        if not res:
            print(C.S_ERR_CONTAIN)
            return False

        # if we made it this far, return true
        return True

    # --------------------------------------------------------------------------
    # Convert items in blacklist to absolute Path objects
    # --------------------------------------------------------------------------
    def _get_blacklist_paths(self):
        """
        Convert items in blacklist to absolute Path objects

        Get absolute paths for all entries in the blacklist.
        """

        # def result
        res = {}

        # remove path separators
        # NB: this is mostly for glob support, as globs cannot end in path
        # separators
        for key in C.D_BLACKLIST:
            C.D_BLACKLIST[key] = [
                item.rstrip("/") for item in C.D_BLACKLIST[key]
            ]

        # support for absolute/relative/glob
        # NB: taken from cntree.py

        # for each section of blacklist
        for key, val in C.D_BLACKLIST.items():
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
    # Fix license/image and remove unnecessary parts of the README file
    # --------------------------------------------------------------------------
    def _fix_readme(self, path):
        """
        Fix license/image and remove unnecessary parts of the README file

        Arguments:
            path: Path for the README to remove text

        Fixes the license/image according to the C.D_PRJ_CFG settings, and
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

        # ----------------------------------------------------------------------
        # now build the final license html

        # get replacement value
        pp_license_name = C.D_PRJ_DEF["__PP_LICENSE_NAME__"]
        pp_license_img = C.D_PRJ_DEF["__PP_LICENSE_IMG__"]
        pp_license_link = C.D_PRJ_DEF["__PP_LICENSE_LINK__"]

        # the default license value
        pp_license_full = (
            f"[![{pp_license_name}]"  # alt text
            f"({pp_license_img}"  # img src
            f' "{pp_license_link}"'  # img tooltip
            f")]({pp_license_link})"  # img link
        )

        # find the license block
        str_pattern = C.R_RM_LICENSE

        # replace text
        str_rep = C.R_RM_LICENSE_REP.format(pp_license_full)
        text = re.sub(str_pattern, str_rep, text, flags=C.R_RM_SUB_FLAGS)

        # ----------------------------------------------------------------------
        # now do description

        # find the short desc block
        str_pattern = C.R_RM_SHORT_DESC

        # get the new description
        new_desc = C.D_PRJ_META["__PP_SHORT_DESC__"]

        # replace text
        str_rep = C.R_RM_SHORT_DESC_REP.format(new_desc)
        text = re.sub(str_pattern, str_rep, text, flags=C.R_RM_SUB_FLAGS)

        # ----------------------------------------------------------------------

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
        prj_type = C.D_PRJ_CFG["__PP_TYPE_PRJ__"]
        for key, val in C.D_README.items():
            if prj_type == key:
                # get values for keys
                rm_delete_start = val["__RM_DELETE_START__"]
                rm_delete_end = val["__RM_DELETE_END__"]
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
    # Fix header or code for each line in a file
    # --------------------------------------------------------------------------
    def _fix_content(self, path, bl_hdr, bl_code):
        """
        Fix header or code for each line in a file

        Arguments:
            path: Path for replacing text
            bl_hdr: Whether the file is blacklisted for header lines
            bl_code: Whether the file is blacklisted for code lines

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

            # skip blank lines, obv (l_type = 1)
            if line.strip() == "":

                # go to next line in file
                continue

            # is this line a comment?
            if not bl_hdr:

                # check if it matches header pattern
                str_pattern = C.D_HEADER[C.S_KEY_HDR_SEARCH]
                res = re.search(str_pattern, line)
                if res:

                    # fix it
                    lines[index] = self._fix_header(line)

                    # stop on first match
                    continue

            if not bl_code:
                lines[index] = self._fix_code(line)

        # open and read file
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.writelines(lines)

    # --------------------------------------------------------------------------
    # Replace dunders inside a file header
    # --------------------------------------------------------------------------
    def _fix_header(self, line):
        """
        Replace dunders inside a file header

        Arguments:
            line: The line of the file to replace text in

        Returns:
            The new line of code

        Replaces text inside a file, using a regex to match specific lines.
        Given a line, it replaces the found pattern withe the replacement as it
        goes.
        """

        # break apart header line
        # NB: gotta do this again, can't pass res param
        str_pattern = C.D_HEADER[C.S_KEY_HDR_SEARCH]
        res = re.search(str_pattern, line)

        # pull out val and pad
        val = res.group(C.D_HEADER[C.S_KEY_GRP_VAL])
        pad = res.group(C.D_HEADER[C.S_KEY_GRP_PAD])

        # do all string replacements and measurements
        old_len_val = len(val)
        val = self._fix_code(val)
        new_len_val = len(val)

        # set default padding
        old_len_pad = len(pad)

        # only recalculate padding if val len changed
        # there is padding, must be rat
        if old_len_val != new_len_val and old_len_pad > 1:

            # get length change (+/-)
            val_diff = new_len_val - old_len_val

            # check if the amount to change is less than we've got
            # NB: invert the sign
            new_len_pad = old_len_pad + (0 - val_diff)

            # we need some padding
            if new_len_pad > 0:
                pad = " " * new_len_pad
            else:
                # always have at least one space in padding
                pad = " "

        # put the parts back together
        repl = C.D_HEADER[C.S_KEY_FMT_VAL_PAD].format(val, pad)

        # format replacement regex
        str_rep = C.D_HEADER[C.S_KEY_HDR_REPLACE].format(repl)
        line = re.sub(str_pattern, str_rep, line)

        # return
        return line

    # --------------------------------------------------------------------------
    # Replace dunders inside s file's contents
    # --------------------------------------------------------------------------
    def _fix_code(self, line):
        """
        Replace dunders inside s file's contents

        Arguments:
            line: The line of the file to replace text in

        Returns:
            The new line of code

        Replaces text inside a file. Given a line, replaces dunders as it goes.
        When it is done, it returns the new line. This replaces the __PP/__PP
        dunders inside the file, excluding headers (which are already handled).
        """

        # TODO: split line into code/comment
        # ignore comment

        # find all dunders in line
        for key, val in self._dict_rep.items():
            line = line.replace(key, val)

        # return fixed code
        return line

    def _fix_line(self, line):
        # find trips
        a_count = line.count('"""')

        # we found a trip
        if a_count > 0:

            # if it is a one-liner
            if a_count > 1:

                # single line trips, just skip
                self._in_trips = False
                return line

            # flip in_trips flag and skip
            self._in_trips = not self._in_trips
            return line

        # skip trips and their contents
        if self._in_trips:
            return line

        # --------------------------------------------------------------------------

        # ignore trailing comments
        parts = line.split("#")

        for key, val in self._dict_rep.items():
            parts[0] = parts[0].replace(key, val)
        # replace content
        # parts[0] = parts[0].replace(, )

        # rejoin trailing comments
        line = "#".join(parts)

        return line

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
        self._dict_rep.
        """

        # first get the path name (we only want to change the last component)
        last_part = path.name

        # # replace dunders in last path component
        last_part = self._fix_code(last_part)

        # replace the name
        path_new = path.parent / last_part

        # if it hasn't changed, skip to avoid overhead
        if path_new == path:
            return

        # do rename
        path.rename(path_new)


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
