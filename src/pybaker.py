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
# import json
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
DIR_SELF = Path(__file__).parent.resolve()
P_DIR_PYPLATE = Path(__file__).parents[1].resolve()
P_DIR_PP_LIB = P_DIR_PYPLATE / "lib"
sys.path.append(str(P_DIR_PYPLATE))
sys.path.append(str(P_DIR_PP_LIB))

# local imports
from conf import pymaker_conf as M  # type:ignore
from conf import pybaker_conf as B  # type:ignore
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
S_PP_NAME_BIG = "PyBaker"
S_PP_NAME_SMALL = "pybaker"
S_PP_SHORT_DESC = (
    "A program to set the metadata of a PyPlate project and create a dist"
)

# formatted version
S_PP_VER_FMT = f"Version {M.S_VERSION}"

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

# folder option strings
S_PRJ_OPTION = "-f"
S_PRJ_METAVAR = "PROJECT DIR"
S_PRJ_DEST = "PRJ_DEST"
S_PRJ_HELP = "the project directory to bake"

# path to prj pyplate files
# NB: leave as string, no start dir yet
S_PP_PRV = "pyplate/conf/private.json"
S_PP_PRJ = "pyplate/conf/project.json"

# ------------------------------------------------------------------------------
# Public classes
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
    distribution of a project from a settings file.
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
        self._dir_prj = Path()
        self._dict_rep = {}
        self._is_html = False
        self._dict_sw_block = {}
        self._dict_sw_line = {}

        self._dict_prj = {}
        self._dict_meta = {}
        self._dict_prv = {}
        self._dict_cfg = {}

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

        # load current metadata from conf or user input
        self._get_project_info()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_fix()

        # fix metadata in files
        self._do_fix()

        # do extra stuff to final dir after fix
        self._do_after_fix()

        # copy project files into dist folder
        self._copy_files()

        # do extra stuff not related to changing files
        self._do_extras()

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
        self._debug = self._d_args.get(S_DBG_DEST, False)

        # debug turns off some _do_after_fix features
        if self._debug:
            M.B_CMD_TREE = False

        # set flag dicts to defaults
        self._dict_sw_block = dict(M.D_SW_BLOCK_DEF)
        self._dict_sw_line = dict(M.D_SW_LINE_DEF)

      # ----------------------------------------------------------------------

        # check for folder
        dst = dict_args[S_PRJ_DEST]
        if dst:
            self._dir_prj = Path(dst)
            if not self._dir_prj.exists():
                print("project dir does not exist")
                sys.exit()
        else:
            print("project dir not provided")
            sys.exit()

      # ----------------------------------------------------------------------

        # if debug, use test project
        if self._debug:
            self._dir_prj = Path(
                "/home/dana/Documents/Projects/Python/CLIs/CLIs_DEBUG"
            )
            return

    # --------------------------------------------------------------------------
    # Load the config files
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Load the config files

        Get required config files and load them into the dictionaries required
        by the program. These files may sometimes be edited by users, so we
        need to check that they:
        (1. exist)
        and
        (2. are valid JSON).
        Both of these are handled by F.load_dicts.
        """

        # TODO use dunders here
        # get individual dicts in the project file
        path_to_conf = self._dir_prj / S_PP_PRJ
        self._dict_prj = F.load_dicts([path_to_conf], {})
        self._dict_meta = self._dict_prj[M.S_KEY_PRJ_META]

        # get main settings dict in private.json
        path_to_conf = self._dir_prj / S_PP_PRV
        self._dict_prv = F.load_dicts([path_to_conf], {})
        self._dict_cfg = self._dict_prv[M.S_KEY_PRV_CFG]

        # TODO: ask for some/all metadata?

        # # NEXT: enforce semantic versioning (_check_version)
        # # first get old version from metadata
        # # NB: if no version key, use default of "0.0.1"
        # old_version = self._d_metadata.get("__PP_VERSION__", "")
        # if old_version == "":
        #     old_version = "0.0.0"

        # # now ask user for new number or default
        # fmt_str = B.S_ASK_VER.format(old_version)
        # new_version = input(fmt_str)
        # if new_version == "":
        #     new_version = old_version

        # # save new version to metadata
        # self._d_metadata["__PP_VERSION__"] = new_version
        # self._version = new_version
        # # TODO: save new version to file

    # --------------------------------------------------------------------------
    # Dummy function to call "subclass" function (function in conf/public.py)
    # --------------------------------------------------------------------------
    def _do_before_fix(self):
        """
        Dummy function to call "subclass" function (function in conf/public.py)

        This function is here just so i can follow the flow of the program in
        my head better. I will be making a flowchart soon...
        """

        # call public before fix function
        M.do_before_fix(self._dict_meta, self._dict_cfg)

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
            [
                self._dict_prv[M.S_KEY_PRV_DEF],
                self._dict_prv[M.S_KEY_PRV_DIST_DIRS],
                self._dict_prv[M.S_KEY_PRV_EXTRA],
                self._dict_cfg,
                self._dict_meta,
            ],
            self._dict_rep,
        )

        # fix up blacklist and convert relative or glob paths to absolute Path
        # objects
        dict_paths = self._get_blacklist_paths()

        # just shorten the names
        skip_all = dict_paths[M.S_KEY_SKIP_ALL]
        skip_contents = dict_paths[M.S_KEY_SKIP_CONTENTS]
        skip_header = dict_paths[M.S_KEY_SKIP_HEADER]
        skip_code = dict_paths[M.S_KEY_SKIP_CODE]
        skip_path = dict_paths[M.S_KEY_SKIP_PATH]

        # ----------------------------------------------------------------------
        # do the fixes bottom up
        # NB: topdown=False is required for the renaming, as we don't want to
        # rename (and thus clobber) a directory name before we rename all its
        # child dirs/files
        # note that root is a full path, dirs and files are relative to root
        for root, root_dirs, root_files in self._dir_prj.walk(top_down=False):

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

                # if we shouldn't skip contents
                if root not in skip_contents and item not in skip_contents:

                    # for each new file, reset block and line switches to def
                    self._dict_sw_block = dict(M.D_SW_BLOCK_DEF)
                    self._dict_sw_line = dict(M.D_SW_LINE_DEF)

                    # check for header bl
                    bl_hdr = True
                    if root not in skip_header and item not in skip_header:
                        bl_hdr = False

                    # check for code blacklist
                    bl_code = True
                    if root not in skip_code and item not in skip_code:
                        bl_code = False

                    # do md/html/xml separately (needs special handling)
                    d_repl = M.D_PY_REPL
                    wo_dot = item.suffix.lstrip(".")
                    w_dot = "." + wo_dot
                    if wo_dot in M.L_MARKUP or w_dot in M.L_MARKUP:
                        d_repl = M.D_MU_REPL

                    # fix content with appropriate dict
                    self._fix_content(item, bl_hdr, bl_code, d_repl)

                # --------------------------------------------------------------

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

        # TODO: combine w/ pybaker

        # ----------------------------------------------------------------------
        # save project settings

        # save fixed settings
        dict_no_edit = {
            M.S_KEY_PRV_DEF: M.D_PRV_DEF,
            M.S_KEY_PRV_DIST_DIRS: M.D_PRV_DIST_DIRS,
            M.S_KEY_PRV_EXTRA: M.D_PRV_EXTRA,
            M.S_KEY_PRV_CFG: M.D_PRV_CFG,
        }
        path_no_edit = self._dir_prj / S_PP_PRV
        F.save_dict(dict_no_edit, [path_no_edit])

        # save editable settings (blacklist/i18n etc.)
        path_edit = self._dir_prj / S_PP_PRJ
        dict_edit = {
            M.S_KEY_PRJ_BL: self._dict_prj[M.S_KEY_PRJ_BL],
            M.S_KEY_PRJ_I18N: self._dict_prj[M.S_KEY_PRJ_I18N],
        }
        F.save_dict(dict_edit, [path_edit])

        # ----------------------------------------------------------------------
        # fix dunders in bl/i18n

        # replace dunders in blacklist and i18n
        self._fix_content(path_edit, False, False,self._dict_rep)

        # reload dict from fixed file
        dict_edit = F.load_dicts([path_edit])

        # ----------------------------------------------------------------------
        # save meta

        # put in metadata and save back to file
        dict_edit[M.S_KEY_PRJ_META] = self._dict_meta
        F.save_dict(dict_edit, [path_edit])

        # ----------------------------------------------------------------------
        # everything else

        # call public after fix
        M.do_after_fix(self._dir_prj, self._dict_rep)  # fix readme

    # --------------------------------------------------------------------------
    # Copy fixed files to final location
    # --------------------------------------------------------------------------
    def _copy_files(self):
        """
        Copy fixed files to final location

        Gets dirs/files from project and copies them to the dist dir.
        """

        # list of files/folders from project to include in dist
        src = [
            "conf",
            "README",
            "src",
            "LICENSE.txt",
            "README.md",
        ]

        # path to project's dist folder
        dst = Path(self._dir_prj) / "dist"

        # copy files/folders
        for item in src:
            new_src = Path(self._dir_prj) / item
            new_dst = dst / item
            if new_src.is_dir():
                shutil.copytree(new_src, new_dst, dirs_exist_ok=True)
            elif new_src.is_file():
                shutil.copy2(new_src, new_dst)

        # copy lib
        new_src = P_DIR_PP_LIB
        new_dst = dst / "lib"
        shutil.copytree(new_src, new_dst, dirs_exist_ok=True)

    # --------------------------------------------------------------------------
    # Make any necessary changes after all fixes have been done
    # --------------------------------------------------------------------------
    def _do_extras(self):
        """
        docstring
        """

        # ----------------------------------------------------------------------
        # purge

        # TODO: maybe don't?
        # for item in M.L_PURGE:
        #     path_del = self._dir_prj / item
        #     if path_del.exists():
        #         path_del.unlink()

        # ----------------------------------------------------------------------
        # git

        # TODO: maybe don't?
        # if git flag is set
        # if M.B_CMD_GIT:

        #     # add git dir
        #     str_cmd = M.S_GIT_CMD.format(str(self._dir_prj))
        #     F.sh(str_cmd)

        # ----------------------------------------------------------------------
        # venv

        # TODO: maybe don't?
        # if venv flag is set
        # if M.B_CMD_VENV:
        #     path_venv = self._dir_prj / M.S_ALL_VENV
        #     str_cmd = M.S_VENV_CMD.format(str(path_venv))
        #     F.sh(str_cmd)

        # ----------------------------------------------------------------------
        # requirements.txt

        # TODO: need to be in prj .venv to do this
        # req_path = self._dir_prj / "requirements.txt"
        # F.sh(f"python -Xfrozen-modules=off -m pip freeze > {req_path}")

        # ----------------------------------------------------------------------
        # tree
        # NB: run last so it includes .git and .venv folders
        # NB: this will wipe out all previous checks (maybe good?)

        # if tree flag is set
        if M.B_CMD_TREE:
            # get path to tree
            file_tree = self._dir_prj / M.S_TREE_FILE

            # create the file so it includes itself
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write("")

            # create tree object and call
            tree_obj = CNTree()
            tree_str = tree_obj.build_tree(
                str(self._dir_prj),
                filter_list=M.D_BLACKLIST[M.S_KEY_SKIP_TREE],
                dir_format=M.S_TREE_DIR_FORMAT,
                file_format=M.S_TREE_FILE_FORMAT,
            )

            # write to file
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write(tree_str)

        # also dont just go for all .desktop - don't edit template
        # pp_name_small = self._dict_cfg["__PP_NAME_SMALL__"]

        for root, _root_dirs, root_files in self._dir_prj.walk():

            # convert files into Paths
            files = [root / f for f in root_files]

            # check if readme
            if root == self._dir_prj:
                # for each file item
                for item in files:
                    if item.name == "README.md":
                        self._fix_readme(item)
                    if item.name == "pyproject.toml":
                        self._fix_pyproject(item)

            # TODO: this need to be better - don't depend on _PP__NAME_SMALL__
            # to be the filename
            pp_name_small = self._dict_cfg["__PP_NAME_SMALL__"]
            if root.name == M.S_ALL_SRC:
                # for each file item
                for item in files:
                    if item.name == f"{pp_name_small}.desktop":
                        self._fix_desktop(item)
                    if item.suffix == "ui" or item.suffix == ".glade":
                        self._fix_gtk3(item)

        # reqs.txt, CHANGELOG.md, tree.txt, docs,
# def do_extras():
#     """
#     Do extras functions to update project dir after recurse

#     Do some extra functions like add requirements, update docs, and update
#     the CHANGELOG file for the current project.
#     """

#     # get current dir
#     dir_curr = os.getcwd()

#     # make sure we are in project path
#     os.chdir(_DIR_PRJ)

#     # add requirements
#     path_req = os.path.join(_DIR_PRJ, "requirements.txt")
#     with open(path_req, "w", encoding="UTF8") as a_file:
#         cmd = "python -m pip freeze -l --exclude-editable --require-virtualenv"
#         cmd_array = shlex.split(cmd)
#         subprocess.run(cmd_array, stdout=a_file, check=False)

#     # update CHANGELOG
#     path_chg = os.path.join(_DIR_PRJ, "CHANGELOG.md")
#     with open(path_chg, "w", encoding="UTF8") as a_file:
#         cmd = 'git log --pretty="%ad - %s"'
#         cmd_array = shlex.split(cmd)
#         subprocess.run(cmd_array, stdout=a_file, check=False)

#     # get tree path
#     path_tree = os.path.join(_DIR_PRJ, "misc", "tree.txt")

#     # if not exist
#     # if not os.path.exists(path_tree):

#     # # create tree object and call
#     # p_t = pytree.PyTree()
#     # TODO: make this use blacklist
#     # tree = p_t.build_tree(_DIR_PRJ, DICT_SETTINGS['__PP_TREE_IGNORE__'])

#     # # write tree to file
#     # with open(path_tree, 'w', encoding='UTF8') as a_file:
#     #     a_file.write(tree)

#     # update docs
#     # NB: this is ugly and stupid, but it's the only way to get pdoc3 to work

#     # move into src dir
#     # dir_src = os.path.join(_DIR_PRJ, 'src')
#     # os.chdir(dir_src)

#     # # get docs dir
#     # path_docs = os.path.join('..', 'docs')
#     # path_docs = os.path.abspath(path_docs)

#     # # # update docs
#     # cmd = f'python -m pdoc --html -f -o {path_docs} .'
#     # cmd_array = shlex.split(cmd)
#     # subprocess.run(cmd_array, check=False)

#     # # go back to old dir
#     # os.chdir(dir_curr)


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

      # ----------------------------------------------------------------------

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

        # add project dir
        parser.add_argument(
            S_PRJ_OPTION,
            metavar=S_PRJ_METAVAR,
            dest=S_PRJ_DEST,
            help=S_PRJ_HELP,
        )

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
        l_bl = self._dict_prj[M.S_KEY_PRJ_BL]
        for key in l_bl:
            l_bl[key] = [item.rstrip("/") for item in l_bl[key]]
        self._dict_prj[M.S_KEY_PRJ_BL] = l_bl

        # support for absolute/relative/glob
        # NB: taken from cntree.py

        # for each section of blacklist
        for key, val in l_bl.items():
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
    def _fix_content(self, path, bl_hdr, bl_code, d_repl):
        """
        Fix header or code for each line in a file

        Arguments:
            path: Path for replacing text
            bl_hdr: Whether the file is blacklisted for header lines
            bl_code: Whether the file is blacklisted for code lines
            d_repl: the dict to use for replacement

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

            # skip blank lines, obv
            if line.strip() == "":
                continue

            # ------------------------------------------------------------------
            # check for block switches

            # param is True if we are looking for block switch vs line switch
            if self._check_switches(line, True, d_repl):
                continue

            # ------------------------------------------------------------------
            # check for header

            # check if blacklisted for headers
            if not bl_hdr:

                # check if it matches header pattern
                str_pattern = d_repl[M.S_KEY_HDR]
                res = re.search(str_pattern, line)
                if res:

                    # fix it
                    lines[index] = self._fix_header(line, d_repl)

                    # stop on first match
                    continue

            # ------------------------------------------------------------------
            # skip any other comment lines

            str_pattern = d_repl[M.S_KEY_COMM]
            if re.search(str_pattern, line):
                continue

            # ------------------------------------------------------------------
            # not a blank, block, header, or comment, must be code ( + comment)

            # check if blacklisted for code
            if not bl_code:

                # fix dunders in real code lines (may still have trailing
                # comments)
                lines[index] = self._fix_code(line, d_repl)

        # open and write file
        with open(path, "w", encoding="UTF-8") as a_file:
            a_file.writelines(lines)

        # all files in src
        # if root.name == "src":

        #     lines = []
        #     with open(item, "r", encoding="UTF-8") as a_file:
        #         lines = a_file.readlines()

        #     for index, line in enumerate(lines):

        #         pat = r"(__PB_VERSION__\s*=\s*)(.*)(\n)"
        #         repl = rf'\g<1>"{self._s_version}"\g<3>'
        #         sch = re.search(pat, line)
        #         if sch:
        #             lines[index] = re.sub(pat, repl, line)

        #         pat = r"(__PB_SHORT_DESC__\s*=\s*)(.*)(\n)"
        #         repl = rf'\g<1>"{self._s_short_desc}"\g<3>'
        #         sch = re.search(pat, line)
        #         if sch:
        #             lines[index] = re.sub(pat, repl, line)

        #     with open(item, "w", encoding="UTF-8") as a_file:
        #         a_file.writelines(lines)

        # --------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Replace dunders inside a file header
    # --------------------------------------------------------------------------
    def _fix_header(self, line, d_repl):
        """
        Replace dunders inside a file header

        Arguments:
            line: The line of the file to replace text in
            d_repl: the dict to use for replacement

        Returns:
            The new line of code

        Replaces text inside a header line, using a regex to match specific
        lines. Given a line, it replaces the found pattern withe the
        replacement as it goes.
        """

        # break apart header line
        # NB: gotta do this again, can't pass res param
        str_pattern = d_repl[M.S_KEY_HDR]

        # str_pattern = M.D_MU_REPL[M.S_KEY_HDR]
        res = re.search(str_pattern, line)
        if not res:
            return line

        # pull out lead, val, and pad (OXFORD COMMA FTW!)
        lead = res.group(d_repl[M.S_KEY_LEAD])
        val = res.group(d_repl[M.S_KEY_VAL])
        pad = res.group(d_repl[M.S_KEY_PAD])

        tmp_val = str(val)
        old_val_len = len(tmp_val)
        for key2, val2 in self._dict_rep.items():
            if isinstance(val2, str):
                tmp_val = tmp_val.replace(key2, val2)
        new_val_len = len(tmp_val)
        val_diff = new_val_len - old_val_len

        tmp_pad = str(pad)
        tmp_rat = tmp_pad.lstrip()
        len_pad = len(tmp_pad) - len(tmp_rat) - val_diff
        pad = " " * len_pad

        line = lead + tmp_val + pad + tmp_rat + "\n"

        # return
        return line

    # --------------------------------------------------------------------------
    # Replace dunders inside a markup file's contents
    # --------------------------------------------------------------------------
    def _fix_code(self, line, d_repl):
        """
        Replace dunders inside a markup file's contents

        Arguments:
            line: The line of the file to replace text in
            d_repl: the dict to use for replacement

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
        matches = re.finditer(d_repl[M.S_KEY_SPLIT], line)
        for match in matches:
            # if there is a match group for hash mark (meaning we found a
            # trailing comment)
            if match.group(4):
                # split the line (comm includes hash mark as first char, code
                # get space between)
                split = match.start(4)
                code = line[:split]
                comm = line[split:]

        # --------------------------------------------------------------
        # # check for line switches

        # for each line, reset line dict
        self._dict_sw_line = dict(M.D_SW_LINE_DEF)

        # do the check
        self._check_switches(comm, False, d_repl)

        # ----------------------------------------------------------------------

        # check for block or line replace switch
        repl = False
        if (
            self._dict_sw_block[M.S_SW_REPLACE]
            and self._dict_sw_line[M.S_SW_REPLACE] != M.I_SW_FALSE
            or self._dict_sw_line[M.S_SW_REPLACE] == M.I_SW_TRUE
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

        Returns: A bool indication whether the name changed (Note that this
        does not mean the file was renamed, only that it should be)
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
    # Check if line or trailing comment is a switch
    # --------------------------------------------------------------------------
    def _check_switches(self, line, block, d_repl):
        """
        Check if line or trailing comment is a switch

        Arguments:
            line: The line to check for block switches
            block: True if we want to check a block switch, False if we want
            to check a line switch
            d_repl: the dict to use for replacement

        Returns:
            True if a valid switch is found, False otherwise

        This method checks to see if a line or trailing comment contains a
        valid switch (for either markup or regular files). If a valid switch is
        found, it sets the appropriate flag in either self._dict_sw_block or
        self._dict_sw_line and returns True.
        """

        # match  switches ('#|<!-- python: enable=replace', etc)
        match = re.match(d_repl[M.S_KEY_SWITCH], line)
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
        if val == M.S_SW_ENABLE:
            dict_to_check[key] = M.I_SW_TRUE
            return True
        if val == M.S_SW_DISABLE:
            dict_to_check[key] = M.I_SW_FALSE
            return True

        # no valid switch found
        return False

    # --------------------------------------------------------------------------
    # Replace text in the pyproject file
    # --------------------------------------------------------------------------
    def _fix_pyproject(self, item):
        """
        Replace text in the pyproject file

        Replaces things like the keywords, requirements, etc. in the toml file.
        """

        # default text if we can't open file
        text = ""

        # open file and get contents
        with open(item, "r", encoding="UTF8") as a_file:
            text = a_file.read()

        # replace version
        str_pattern = (
            r"(^\s*\[project\]\s*$)(.*?)(^\s*version[\t ]*=[\t ]*)(.*?$)"
        )
        pp_version = self._dict_meta["__PP_VERSION__"]
        if pp_version == "":
            pp_version = M.S_VERSION
        str_rep = rf'\g<1>\g<2>\g<3>"{pp_version}"'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace short description
        str_pattern = (
            r"(^\s*\[project\]\s*$)"
            r"(.*?)"
            r"(^\s*description[\t ]*=[\t ]*)"
            r"(.*?$)"
        )
        pp_short_desc = self._dict_meta["__PP_SHORT_DESC__"]
        str_rep = rf'\g<1>\g<2>\g<3>"{pp_short_desc}"'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace keywords array
        str_pattern = (
            r"(^\s*\[project\]\s*$)"
            r"(.*?)"
            r"(^\s*keywords[\t ]*=[\t ]*)"
            r"(.*?\])"
        )
        str_rep = rf"\g<1>\g<2>\g<3>[{self._dict_prv[M.S_KEY_PRV_EXTRA]["__PP_KW_STR__"]}]"
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # # replace dependencies array
        # str_pattern = (
        #     r"(^\s*\[project\]\s*$)"
        #     r"(.*?)"
        #     r"(^\s*dependencies[\t ]*=[\t ]*)"
        #     r"(.*?\])"
        # )

        # # convert dict to string (only using keys)
        # pp_py_deps = DICT_METADATA["__PP_PY_DEPS__"]

        # # NB: this is not conducive to a dict (we don't need links, only names)
        # # so don't do what we did in README, keep it simple
        # list_py_deps = [item for item in pp_py_deps.keys()]
        # str_pp_py_deps = [f'"{item}"' for item in list_py_deps]
        # str_pp_py_deps = ", ".join(str_pp_py_deps)

        # # replace text
        # str_rep = rf"\g<1>\g<2>\g<3>[{str_pp_py_deps}]"
        # text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # save file
        with open(item, "w", encoding="UTF8") as a_file:
            a_file.write(text)

    # --------------------------------------------------------------------------
    # Replace text in the readme file
    # --------------------------------------------------------------------------
    def _fix_readme(self, item):
        """
        Replace text in the README file

        Replace short description, dependencies, and version number in the
        README file.
        """

        # default text if we can't open file
        text = ""

        # open file and get contents
        with open(item, "r", encoding="UTF8") as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = (
            r"(<!--[\t ]*__PP_SHORT_DESC__[\t ]*-->)"
            r"(.*?)"
            r"(<!--[\t ]*__PP_SHORT_DESC__[\t ]*-->)"
        )
        pp_short_desc = self._dict_meta["__PP_SHORT_DESC__"]
        str_rep = rf"\g<1>\n{pp_short_desc}\n\g<3>"
        text = re.sub(str_pattern, str_rep, text, flags=re.S)

        # replace dependencies array
        str_pattern = (
            r"(<!--[\t ]*__PP_RM_DEPS__[\t ]*-->)"
            r"(.*?)"
            r"(<!--[\t ]*__PP_RM_DEPS__[\t ]*-->)"
        )
        str_rep = rf'\g<1>\n{self._dict_prv[M.S_KEY_PRV_EXTRA]["__PP_RM_DEPS__"]}\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.S)

        # save file
        with open(item, "w", encoding="UTF8") as a_file:
            a_file.write(text)

    # ------------------------------------------------------------------------------
    # Replace text in the desktop file
    # ------------------------------------------------------------------------------
    def _fix_desktop(self, item):
        """
        Replace text in the desktop file

        Replaces the desc, exec, icon, path, and category text in a .desktop
        file for programs that use this.
        """

        # validate wanted categories into approved categories
        pp_gui_categories = []
        wanted_cats = self._dict_meta["__PP_GUI_CATS__"]
        for cat in wanted_cats:
            # category is valid
            if cat in B.L_CATS:
                # add to final list
                pp_gui_categories.append(cat)
            else:
                # category is not valid, print error and increase error count
                print(
                    f'In PP_GUI_CATEGORIES, "{cat}" is not valid, see \n'
                    "https://specifications.freedesktop.org/menu-spec/latest/apa.html"
                )

        # convert list to string
        str_cat = ";".join(pp_gui_categories)
        str_cat += ";"

        # default text if we can't open file
        text = ""

        # open file and get contents
        with open(item, "r", encoding="UTF8") as a_file:
            text = a_file.read()

        # replace categories
        str_pattern = (
            r"(^\s*\[Desktop Entry\]\s*$)"
            r"(.*?)"
            r"(^\s*Categories[\t ]*=)"
            r"(.*?$)"
        )
        str_rep = rf"\g<1>\g<2>\g<3>{str_cat}"
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace short description
        str_pattern = (
            r"(^\s*\[Desktop Entry\]\s*$)"
            r"(.*?)"
            r"(^\s*Comment[\t ]*=)"
            r"(.*?$)"
        )
        pp_short_desc = self._dict_meta["__PP_SHORT_DESC__"]
        str_rep = rf"\g<1>\g<2>\g<3>{pp_short_desc}"
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # TODO: none of this is metadata

        # # get path to install dir
        # path_home = os.path.expanduser("~")
        # author = DICT_SETTINGS["info"]["__PP_AUTHOR__"]
        # pp_name_big = DICT_SETTINGS["info"]["__PP_NAME_BIG__"]
        # path_inst = os.path.join(path_home, f".{author}", pp_name_big, "src")

        # # replace exec
        # str_pattern = (
        #     r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Exec[\t ]*=)" r"(.*?$)"
        # )
        # path_exec = os.path.join(path_inst, f"{pp_name_small}.py")
        # str_rep = rf"\g<1>\g<2>\g<3>{path_exec}"
        # text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # # replace icon
        # str_pattern = (
        #     r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Icon[\t ]*=)" r"(.*?$)"
        # )
        # path_icon = os.path.join(path_inst, f"{pp_name_small}.png")
        # str_rep = rf"\g<1>\g<2>\g<3>{path_icon}"
        # text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # # replace path
        # str_pattern = (
        #     r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Path[\t ]*=)" r"(.*?$)"
        # )
        # str_rep = rf"\g<1>\g<2>\g<3>{path_inst}"
        # text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # save file
        with open(item, "w", encoding="UTF8") as a_file:
            a_file.write(text)

    # ------------------------------------------------------------------------------
    # Replace text in the UI file
    # ------------------------------------------------------------------------------
    def _fix_gtk3(self, item):
        """
        Replace text in the UI file

        Replace description and version number in the UI file.
        """

        # default text if we can't open file
        text = ""

        # open file and get contents
        with open(item, "r", encoding="UTF-8") as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = (
            r"(<object class=\"GtkAboutDialog\".*?)"
            r"(<property name=\"comments\".*?\>)"
            r"(.*?)"
            r"(</property>)"
        )
        pp_short_desc = self._dict_meta["__PP_SHORT_DESC__"]
        str_rep = rf"\g<1>\g<2>{pp_short_desc}\g<4>"
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        str_pattern = (
            r"(<object class=\"GtkAboutDialog\".*?)"
            r"(<property name=\"version\">)"
            r"(.*?)"
            r"(</property>.*)"
        )
        pp_version = self._dict_meta["__PP_VERSION__"]
        str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # save file
        with open(item, "w", encoding="UTF8") as a_file:
            a_file.write(text)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main method
    pb = PyBaker()
    pb.main()

    # --------------------------------------------------------------------------

# # ------------------------------------------------------------------------------
# # Run xgettext over files to produce a locale template
# # ------------------------------------------------------------------------------
# # def do_gettext():
# #     """
# #     Run xgettext over files to produce a locale template

# #     Use xgettext to scan .py and .ui files for I18N strings and collect them
# #     int a .pot file in the locale folder. Only applies to gui projects at
# #     the moment.
# #     """

# #     # check if we are a gui project
# #     is_gui = DICT_SETTINGS["project"]["type"] == "g"
# #     if not is_gui:
# #         return

# #     # get locale folder and pot filename
# #     dir_locale = os.path.join(_DIR_PRJ, "src", "locale")
# #     pp_name_small = DICT_SETTINGS["info"]["__PP_NAME_SMALL__"]
# #     path_pot = os.path.join(dir_locale, f"{pp_name_small}.pot")
# #     pp_version = DICT_METADATA["__PP_VERSION__"]

# #     # remove old pot and recreate empty file
# #     if os.path.exists(path_pot):
# #         os.remove(path_pot)
# #     with open(path_pot, "w", encoding="UTF8") as a_file:
# #         a_file.write("")

# #     # build a list of files
# #     res = []
# #     exts = [".py", ".ui", ".glade"]

# #     # scan for files in src directory
# #     dir_src = os.path.join(_DIR_PRJ, "src")
# #     list_files = os.listdir(dir_src)

# #     # for each file in dir
# #     for file in list_files:
# #         # check for ext
# #         for ext in exts:
# #             if file.endswith(ext):
# #                 # rebuild complete path and add to list
# #                 path = os.path.join(dir_src, file)
# #                 res.append(path)

# #     # for each file that can be I18N'd, run xgettext
# #     author = DICT_SETTINGS["info"]["__PP_AUTHOR__"]
# #     email = DICT_SETTINGS["info"]["__PP_EMAIL__"]
# #     for file in res:
# #         cmd = (
# #             "xgettext "  # the xgettext cmd
# #             f"{file} "  # the file name
# #             "-j "  # append to current file
# #             '-c"I18N:" '  # look for tags in .py files
# #             "--no-location "  # don't print filename/line number
# #             f"-o {path_pot} "  # location of output file
# #             "-F "  # sort output by input file
# #             f"--copyright-holder={author} "
# #             f"--package-name={pp_name_small} "
# #             f"--package-version={pp_version} "
# #             f"--msgid-bugs-address={email}"
# #         )
# #         cmd_array = shlex.split(cmd)
# #         subprocess.run(cmd_array, check=False)

# #     # now lets do some text replacements to make it look nice

# #     # default text if we can't open file
# #     text = ""

# #     # open file and get contents
# #     with open(path_pot, "r", encoding="UTF8") as a_file:
# #         text = a_file.read()

# #     # replace short description
# #     str_pattern = r"(# SOME DESCRIPTIVE TITLE.)"
# #     pp_name_big = DICT_SETTINGS["info"]["__PP_NAME_BIG__"]
# #     str_rep = f"# {pp_name_big} translation template"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # replace copyright
# #     author = DICT_SETTINGS["info"]["__PP_AUTHOR__"]
# #     str_pattern = r"(# Copyright \(C\) )" r"(.*?)" rf"( {author})"
# #     year = date.today().year
# #     str_rep = rf"\g<1>{year}\g<3>"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # replace author's email
# #     str_pattern = r"(# FIRST AUTHOR )" r"(<EMAIL@ADDRESS>)" r"(, )" r"(YEAR)"
# #     email = DICT_SETTINGS["info"]["__PP_EMAIL__"]
# #     year = date.today().year
# #     str_rep = rf"\g<1>{email}\g<3>{year}"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # replace charset
# #     str_pattern = (
# #         r'("Content-Type: text/plain; charset=)' r"(CHARSET)" r'(\\n")'
# #     )
# #     charset = "UTF-8"
# #     str_rep = rf"\g<1>{charset}\g<3>"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # save file
# #     with open(path_pot, "w", encoding="UTF8") as a_file:
# #         a_file.write(text)

# # def do_pot():
# #     """docstring"""

# #     # # dict of clangs and exts
# #     dict_in = {
# #         "Python": [
# #             "py",
# #         ],
# #         "Glade": [
# #             ".ui",
# #             ".glade",
# #         ],
# #         "Desktop": [".desktop"],
# #     }

# #     # dict of clangs and no exts (ie file names)
# #     dict_blank = {
# #         "Python": [
# #             "__PP_NAME_SMALL__",
# #         ],
# #     }

# #     # the list of languages your program has been translated into (can grow
# #     # over time, adding languages as they become available)
# #     list_wlang = [
# #         "es",
# #         "xo",
# #         "pq",
# #     ]

# #     # path to src dir
# #     dir_src = Path(__file__).parent.resolve()

# #     pp = CNPotPy(
# #         dir_src,
# #         str_appname="foo",
# #         str_version="0",
# #         str_email="foo@bar.com",
# #         str_domain=f"{C_DOMAIN}",
# #         dict_clangs=dict_in,
# #         dict_no_ext=dict_blank,
# #         list_wlangs=list_wlang,
# #     )

# #     # I18N: run cnpotpy
# #     pp.make_pot()
# #     pp.make_pos()
# #     pp.make_mos()
# #     pp.make_desktop(
# #         C_GUI_DIR / "template.desktop",
# #         C_GUI_DIR / "__PP_NAME_SMALL__.desktop",
# #     )

# #     # TODO: this is for testing purposes only
# #     t = gettext.translation(
# #         M.DOMAIN, localedir=M.POT_DEF_DIR_LOCALE, languages=["es"]
# #     )
# #     t.install()
# #     _ = t.gettext

# #     # get path to config file
# #     C_PATH_GUI = C_PATH_SRC / "cfg/__PP_NAME_SMALL__.json"


    # def _make_install(self):
    #     """
    #     docstring
    #     """

    #     dict_install = {
    #         "lib": ".local/share/cyclopticnerve",  # __PP_AUTHOR__
    #         "conf": ".config/CLIs_DEBUG",  # __PP_NAME_BIG__
    #         "src/clis_debug": ".local/bin",  # __PP_NAME_SMALL__
    #     }

    #     dst = Path(self._dir_prj) / "dist" / "inst_conf.json"
    #     with open(dst, "w", encoding="UTF-8") as a_file:
    #         json.dump(dict_install, a_file, indent=4)

# # ------------------------------------------------------------------------------
# # Replace text in the install file
# # ------------------------------------------------------------------------------
# def fix_install():
#     """
#     Replace text in the install file

#     Replaces the system and Python dependencies in the install file.
#     """

#     # check if the file exists
#     path_install = _DIR_PRJ / "install.py"
#     if not path_install.exists():
#         return

#     # default text if we can't open file
#     text = ""

#     # open file and get content
#     with open(path_install, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # replace python dependencies array
#     str_pattern = (
#         r"(^\s*dict_install[\t ]*=\s*{)"
#         r"(.*?)"
#         r"(^\s*\'py_deps\'[\t ]*:)"
#         r"(.*?\])"
#     )

#     # convert dict keys to string
#     pp_py_deps = DICT_METADATA["__PP_PY_DEPS__"]
#     str_pp_py_deps = ",".join(pp_py_deps.keys())

#     # replace text
#     str_rep = rf"\g<1>\g<2>\g<3> [\n\t\t{str_pp_py_deps}\n\t]"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace system dependencies array
#     str_pattern = (
#         r"(^\s*dict_install[\t ]*=)"
#         r"(.*?)"
#         r"(^\s*\'sys_deps\'[\t ]*:)"
#         r"(.*?\])"
#     )

#     # convert dict to string
#     pp_sys_deps = DICT_METADATA["__PP_SYS_DEPS__"]
#     str_pp_sys_deps = ",".join(pp_sys_deps)

#     # replace string
#     str_rep = rf"\g<1>\g<2>\g<3> [\n\t\t{str_pp_sys_deps}\n\t]"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # save file
#     with open(path_install, "w", encoding="UTF8") as a_file:
#         a_file.write(text)
