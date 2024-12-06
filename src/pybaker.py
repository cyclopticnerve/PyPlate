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

# FIXME: run pybaker from prj dir

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
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
P_DIR_PP_CONF = P_DIR_PYPLATE / "conf"
P_DIR_PP_LIB = P_DIR_PYPLATE / "lib"
sys.path.append(str(P_DIR_PP_CONF))
sys.path.append(str(P_DIR_PP_LIB))

# local imports
import pyplate_conf as M  # type:ignore
from cnlib import cnfunctions as F  # type: ignore
from cnlib.cnformatter import CNFormatter  # type: ignore
from cnlib.cntree import CNTree  # type: ignore
from cnlib.cnpot import CNPotPy  # type: ignore
from cnlib.cnvenv import CNVenv  # type: ignore
from cnlib.cnsphinx import CNSphinx  # type: ignore

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
S_PP_NAME_BIG = "PyBaker"
S_PP_SHORT_DESC = (
    "A program to set the metadata of a PyPlate project and create a dist"
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

# folder positional strings
S_PRJ_OPTION = "DIR"  # key in dict_args
S_PRJ_HELP = "the project directory to bake"  # display in help

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
        self._dict_args = {}
        self._debug = False
        self._dir_prj = Path()

        self._dict_rep = {}
        self._is_html = False
        self._dict_sw_block = {}
        self._dict_sw_line = {}
        self._dict_type_rep = {}

        # private.json dicts
        self._dict_prv = {}
        self._dict_prv_all = {}
        self._dict_prv_prj = {}

        # project.json dicts
        self._dict_pub = {}
        self._dict_pub_meta = {}
        self._dict_pub_dist = {}
        self._dict_pub_bl = {}
        self._dict_pub_i18n = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main method of the program
    # --------------------------------------------------------------------------
    def main(self, dir_prj, debug=False):
        """
        The main method of the program

        Arguments:
            dir_prj: Path to the project dir
            debug: Whether to run in debug mode (default: False)

        This method is the main entry point for the program, initializing the
        program, and performing its steps.
        """

        # ----------------------------------------------------------------------
        #  do the work

        # store properties
        self._dir_prj = Path(dir_prj)
        self._debug = debug

        # print about info
        print(S_PP_ABOUT)
        print()

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
        self._do_copy()

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

        Perform some mundane stuff like checking the arg parser and setting
        properties.
        """

        # ----------------------------------------------------------------------

        # debug turns off some _do_after_fix features
        if self._debug:
            M.B_CMD_GIT = False
            M.B_CMD_VENV = False
            M.B_CMD_I18N = False
            M.B_CMD_DOCS = False
            M.B_CMD_TREE = False

        # set flag dicts to defaults
        self._dict_sw_block = dict(M.D_SW_BLOCK_DEF)
        self._dict_sw_line = dict(M.D_SW_LINE_DEF)

        # remove home dir from PyPlate path
        h = str(Path.home())
        p = str(P_DIR_PYPLATE)
        p = p.lstrip(h).strip("/")
        # NB: change global val
        M.D_PRV_PRJ["__PP_DEV_PP__"] = p

        # ----------------------------------------------------------------------

        # check for folder
        if self._dir_prj and not self._dir_prj.exists():
            print(M.S_ERR_PRJ_DIR_NO_EXIST.format(self._dir_prj))
            sys.exit(-1)
        if "pyplate" in str(self._dir_prj).lower():
            print(M.S_ERR_PRJ_DIR_IS_PP)
            sys.exit(-1)

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Get required config files and load them into the dictionaries required
        by the program. These files may sometimes be edited by users, so we
        need to check that they:
        1. exist
        and
        2. are valid JSON.\n
        Both of these are handled by F.load_dicts.
        """

        # get global and calculated settings dict in private.json
        path_prv = self._dir_prj / M.S_PRJ_PRV_CFG
        self._dict_prv = F.load_dicts([path_prv], {})
        self._dict_prv_all = self._dict_prv[M.S_KEY_PRV_ALL]
        self._dict_prv_prj = self._dict_prv[M.S_KEY_PRV_PRJ]

        # get individual dicts in the public file
        path_pub = self._dir_prj / M.S_PRJ_PUB_CFG
        self._dict_pub = F.load_dicts([path_pub], {})
        self._dict_pub_meta = self._dict_pub[M.S_KEY_PUB_META]
        self._dict_pub_bl = self._dict_pub[M.S_KEY_PUB_BL]
        self._dict_pub_i18n = self._dict_pub[M.S_KEY_PUB_I18N]
        # self._dict_pub_install = self._dict_pub[M.S_KEY_PUB_INSTALL]
        self._dict_pub_dist = self._dict_pub[M.S_KEY_PUB_DIST]

    # --------------------------------------------------------------------------
    # A function to do stuff before fix
    # --------------------------------------------------------------------------
    def _do_before_fix(self):
        """
        A function to do stuff before fix

        This function does some more changes before the actual fix. Mostly it
        is used to call the do_before_fix method in pyplate_conf.py.
        """

        print(M.S_ACTION_BEFORE, end="", flush=True)

        # call function to update kw/readme deps
        M.do_before_fix(self._dir_prj, self._dict_prv, self._dict_pub)

        print(M.S_ACTION_DONE)

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

        print(M.S_ACTION_FIX, end="", flush=True)

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
        skip_all = dict_paths[M.S_KEY_SKIP_ALL]
        skip_contents = dict_paths[M.S_KEY_SKIP_CONTENTS]
        skip_header = dict_paths[M.S_KEY_SKIP_HEADER]
        skip_code = dict_paths[M.S_KEY_SKIP_CODE]
        skip_path = dict_paths[M.S_KEY_SKIP_PATH]

        # ----------------------------------------------------------------------
        # do the fixes
        # note that root is a full path, dirs and files are relative to root
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
                    self._dict_type_rep = M.D_PY_REPL
                    suffix = (
                        f".{item.suffix}"
                        if not item.suffix.startswith(".")
                        else item.suffix
                    )
                    if suffix in M.L_EXT_MARKUP:
                        self._dict_type_rep = M.D_MU_REPL

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

        print(M.S_ACTION_DONE)

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

        # save fixed settings
        dict_prv = {
            M.S_KEY_PRV_ALL: self._dict_prv_all,
            M.S_KEY_PRV_PRJ: self._dict_prv_prj,
        }
        path_prv = self._dir_prj / M.S_PRJ_PRV_CFG
        F.save_dict(dict_prv, [path_prv])

        # save editable settings (blacklist/i18n etc.)
        dict_pub = {
            M.S_KEY_PUB_BL: self._dict_pub_bl,
            M.S_KEY_PUB_I18N: self._dict_pub_i18n,
            M.S_KEY_PUB_DIST: self._dict_pub_dist,
        }
        path_pub = self._dir_prj / M.S_PRJ_PUB_CFG
        F.save_dict(dict_pub, [path_pub])

        # ----------------------------------------------------------------------
        # fix dunders in bl/i18n
        self._fix_content(path_pub)

        # reload dict from fixed file
        dict_pub = F.load_dicts([path_pub])

        # ----------------------------------------------------------------------
        # save meta

        # put in metadata and save back to file
        dict_pub[M.S_KEY_PUB_META] = self._dict_pub_meta
        F.save_dict(dict_pub, [path_pub])

        # ----------------------------------------------------------------------
        # call conf after fix

        print(M.S_ACTION_AFTER, end="", flush=True)
        M.do_after_fix(self._dir_prj, self._dict_prv, self._dict_pub)
        print(M.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # freeze requirements
        if M.B_CMD_VENV:

            print(M.S_ACTION_VENV, end="", flush=True)

            # get name ov venv folder and reqs file
            dir_venv = self._dict_prv_prj["__PP_NAME_VENV__"]
            file_reqs = M.S_FILE_REQS

            # do the thing with the thing
            cv = CNVenv(self._dir_prj, dir_venv, file_reqs)
            try:
                cv.freeze()
                print(M.S_ACTION_DONE)
            except F.CNShellError as e:
                print(M.S_ACTION_FAIL)
                print(e.message)

        # ----------------------------------------------------------------------
        # i18n
        # if i18n flag is set
        if M.B_CMD_I18N:

            print(M.S_ACTION_I18N, end="", flush=True)

            # create CNPotPy object
            potpy = CNPotPy(
                dir_src=self._dir_prj / M.S_DIR_SRC,
                str_appname=self._dict_prv_prj["__PP_NAME_BIG__"],
                str_version=self._dict_pub_meta["__PP_VERSION__"],
                str_author=self._dict_prv_all["__PP_AUTHOR__"],
                str_email=self._dict_prv_all["__PP_EMAIL__"],
                dir_locale=self._dir_prj / M.S_DIR_LOCALE,
                dir_po=self._dir_prj / M.S_DIR_PO,
                str_domain=self._dict_prv_prj["__PP_NAME_SMALL__"],
                dict_clangs=self._dict_pub_i18n[M.S_KEY_CLANGS],
                dict_no_ext=self._dict_pub_i18n[M.S_KEY_NO_EXT],
                list_wlangs=self._dict_pub_i18n[M.S_KEY_WLANGS],
                charset="UTF-8",
            )

            # this .pot, .po, and .mo files
            potpy.main()

            # make .desktop file
            path_desk = self._dir_prj / M.S_DIR_DESKTOP
            if path_desk.exists():
                path_template = self._dir_prj / M.S_FILE_DESK_TEMPLATE
                name_small = self._dict_prv_prj["__PP_NAME_SMALL__"]
                path_out_name = M.S_FILE_DESK_OUT.format(name_small)
                path_out = self._dir_prj / path_out_name
                potpy.make_desktop(path_template, path_out)

            # we are done
            print(M.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # update docs

        # if docs flag is set
        if M.B_CMD_DOCS:

            print(M.S_ACTION_DOCS, end="", flush=True)

            # get path to project's venv
            venv = self._dict_prv_prj["__PP_NAME_VENV__"]

            # do the thing with the thing
            cs = CNSphinx(self._dir_prj, M.S_DIR_SRC, M.S_DIR_DOCS)
            try:
                cs.build(venv)
                print(M.S_ACTION_DONE)
            except F.CNShellError as e:
                print(M.S_ACTION_FAIL)
                print(e.message)

        # ----------------------------------------------------------------------
        # tree
        # NB: run last so it includes .git and .venv folders
        # NB: this will wipe out all previous checks (maybe good?)

        # if tree flag is set
        if M.B_CMD_TREE:

            print(M.S_ACTION_TREE, end="", flush=True)

            # get path to tree
            file_tree = self._dir_prj / M.S_TREE_FILE

            # create the file so it includes itself
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write("")

            # create tree object and call
            tree_obj = CNTree()
            tree_str = tree_obj.build_tree(
                str(self._dir_prj),
                filter_list=self._dict_pub_bl[M.S_KEY_SKIP_TREE],
                dir_format=M.S_TREE_DIR_FORMAT,
                file_format=M.S_TREE_FILE_FORMAT,
            )

            # write to file
            with open(file_tree, "w", encoding="UTF-8") as a_file:
                a_file.write(tree_str)

            print(M.S_ACTION_DONE)

        # ----------------------------------------------------------------------
        # fix dunders in install
        path_inst = self._dir_prj / M.S_FILE_INSTALL_CFG
        if path_inst.exists():
            self._fix_content(path_inst)

    # --------------------------------------------------------------------------
    # Copy fixed files to final location
    # --------------------------------------------------------------------------
    def _do_copy(self):
        """
        Copy fixed files to final location

        Gets dirs/files from project and copies them to the dist/assets dir.
        """

        print(M.S_ACTION_COPY, end="", flush=True)

        # find old dist? nuke it from orbit! it's the only way to be sure!
        p_dist = self._dir_prj / M.S_DIR_DIST
        if p_dist.is_dir():
            shutil.rmtree(p_dist)
        Path.mkdir(p_dist, parents=True)

        # for each key, val (type, dict)
        for key, val in self._dict_pub_dist.items():

            # get src/dst rel to prj dir/dist dir
            src = self._dir_prj / key
            dst = p_dist / val
            if not dst.exists():
                Path.mkdir(dst, parents=True)
            dst = dst / src.name

            # do the copy
            if src.exists() and src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif src.exists() and src.is_file():
                shutil.copy2(src, dst)

        # done copying project files
        print(M.S_ACTION_DONE)

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

            # skip blank lines, obv
            if line.strip() == "":
                continue

            # ------------------------------------------------------------------
            # check for block switches

            # param is True if we are looking for block switch vs line switch
            if self._check_switches(line, True):
                continue

            # ------------------------------------------------------------------
            # check for header

            # check if blacklisted for headers
            if not bl_hdr:

                # check if it matches header pattern
                str_pattern = self._dict_type_rep[M.S_KEY_HDR]
                res = re.search(str_pattern, line)
                if res:

                    # fix it
                    lines[index] = self._fix_header(line)

                    # stop on first match
                    continue

            # ------------------------------------------------------------------
            # skip any other comment lines

            str_pattern = self._dict_type_rep[M.S_KEY_COMM]
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
            line: The line of the file to replace text in

        Returns:
            The new line of code

        Replaces text inside a header line, using a regex to match specific
        lines. Given a line, it replaces the found pattern withe the
        replacement as it goes.
        """

        # break apart header line
        # NB: gotta do this again, can't pass res param
        str_pattern = self._dict_type_rep[M.S_KEY_HDR]
        res = re.search(str_pattern, line)
        if not res:
            return line

        # pull out lead, val, and pad (OXFORD COMMA FTW!)
        lead = res.group(self._dict_type_rep[M.S_KEY_LEAD])
        val = res.group(self._dict_type_rep[M.S_KEY_VAL])
        pad = res.group(self._dict_type_rep[M.S_KEY_PAD])

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
    def _fix_code(self, line):
        """
        Replace dunders inside a markup file's contents

        Arguments:
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
        matches = re.finditer(self._dict_type_rep[M.S_KEY_SPLIT], line)
        for match in matches:
            # if there is a match group for hash mark (meaning we found a
            # trailing comment)
            if match.group(4):
                # split the line (comm includes hash mark as first char, code
                # get space between)
                split = match.start(4)
                code = line[:split]
                comm = line[split:]

        # ----------------------------------------------------------------------
        # check for line switches

        # for each line, reset line dict
        self._dict_sw_line = dict(M.D_SW_LINE_DEF)

        # do the check
        self._check_switches(comm, False)

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

        # replace version
        ver = self._dict_pub_meta["__PP_VERSION__"]
        str_sch = M.S_META_VER_SEARCH
        str_rep = M.S_META_VER_REPL.format(ver)
        line = re.sub(str_sch, str_rep, line)

        # replace short desc
        desc = self._dict_pub_meta["__PP_SHORT_DESC__"]
        str_sch = M.S_META_SD_SEARCH
        str_rep = M.S_META_SD_REPL.format(desc)
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
        match = re.match(self._dict_type_rep[M.S_KEY_SWITCH], line)
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

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # NB: argparse code placed here so we can run the script from the command
    # line or use it as an object

    # create the parser
    parser = argparse.ArgumentParser(formatter_class=CNFormatter)

    # set help string
    parser.description = S_PP_ABOUT

    # add debug option
    parser.add_argument(
        M.S_DBG_OPTION,
        action=M.S_DBG_ACTION,
        dest=M.S_DBG_DEST,
        help=M.S_DBG_HELP,
    )

    # add project dir
    parser.add_argument(
        S_PRJ_OPTION,  # args key
        help=S_PRJ_HELP,
    )

    # get namespace object
    args = parser.parse_args()

    # convert namespace to dict
    dict_args = vars(args)

    # --------------------------------------------------------------------------

    # get the args
    a_dir_prj = dict_args.get(S_PRJ_OPTION, None)
    a_debug = dict_args.get(M.S_DBG_DEST, False)

    # create object
    pb = PyBaker()

    # run main method with args
    pb.main(a_dir_prj, a_debug)

# -)
