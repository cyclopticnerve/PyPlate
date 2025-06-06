#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pyplate: replace=False

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

# local imports
from cnformatter import CNFormatter
import cnfunctions as F

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

    # pyplate: replace=True

    # I18N: short description
    S_PP_SHORT_DESC = _(
        "A program for creating and building CLI/Package/GUI projects in "
        "Python from a template"
    )

    # version string
    S_PP_VERSION = "Version 0.0.1+20250507.9"

    # pyplate: replace=False

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
        self._dict_type_rules = {}
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

        # dictionary to hold current debug settings
        self._dict_debug = {}

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

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_dist()

        # copy project files into dist folder
        self._do_dist()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_after_dist()

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

        # debug turns off some post processing to speed up processing
        # NB: changing values in self._dict_pub_dbg (through the functions in
        # pyplate.py) will not affect the current session when running pymaker
        # in debug mode. to do that, change the values of D_DBG_PM in
        # pyplate.py
        self._dict_debug = self._dict_pub_dbg
        if self._debug:
            self._dict_debug = PP.D_DBG_PB
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

        # ----------------------------------------------------------------------

        # set switch dicts to defaults
        self._dict_sw_block = dict(PP.D_SWITCH_DEF)
        self._dict_sw_line = dict(self._dict_sw_block)

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Check that the PyPlate data is present and correct, so we don't crash
        looking for non-existent files.
        """

        # check if dir_prj has pyplate folder for a valid prj
        path_pyplate = self._dir_prj / PP.S_PRJ_PP_DIR
        if not path_pyplate.exists():
            print(PP.S_ERR_NOT_PRJ)
            sys.exit()

        # check if data files exist
        path_prv = self._dir_prj / PP.S_PRJ_PRV_CFG
        path_pub = self._dir_prj / PP.S_PRJ_PUB_CFG
        if not path_prv.exists() or not path_pub.exists():
            print(PP.S_ERR_PP_MISSING)
            sys.exit()

        # check if files are valid json
        try:
            # get global and calculated settings dicts in private.json
            self._dict_prv = F.load_dicts([path_prv], {})

            # get individual dicts in project.json
            self._dict_pub = F.load_dicts([path_pub], {})

            # reload dict pointers after dict change
            self._reload_dicts()
        except OSError:
            print(PP.S_ERR_PP_INVALID)
            sys.exit()

    # --------------------------------------------------------------------------
    # Do any work before fix
    # --------------------------------------------------------------------------
    def _do_before_fix(self):
        """
        Do any work before fix

        Do any work before fix. This method is called just before _do_fix,
        after all dunders have been configured, but before any files have been
        modified.\n
        It is mostly used to make final adjustments to the 'dict_prv' and
        'dict_pub' dicts before any replacement occurs.
        """

        PP.do_before_fix(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_debug
        )

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

        # check version before we start
        version = self._dict_pub_meta[PP.S_KEY_META_VERSION]
        if not self._check_sem_ver(version):
            res = input(PP.S_ERR_SEM_VER).strip()
            if res in ["", PP.S_ERR_SEM_VER_N]:
                sys.exit()

        # combine dicts for string replacement
        self._dict_rep = F.combine_dicts(
            [self._dict_prv_all, self._dict_prv_prj]
        )

        # save private.json and project.json after all fixes have been done
        self._save_project_info()

        # make sure pyplate in in skip_all
        skip_all = self._dict_pub_bl[PP.S_KEY_SKIP_ALL]
        if not PP.S_PRJ_PP_DIR in skip_all:
            skip_all.append(PP.S_PRJ_PP_DIR)

        # fix up blacklist and convert relative or glob paths to absolute Path
        # objects
        self._fix_blacklist_paths(self._dict_pub_bl)

        # just shorten the names
        skip_all = self._dict_pub_bl[PP.S_KEY_SKIP_ALL]
        skip_contents = self._dict_pub_bl[PP.S_KEY_SKIP_CONTENTS]
        skip_header = self._dict_pub_bl[PP.S_KEY_SKIP_HEADER]
        skip_code = self._dict_pub_bl[PP.S_KEY_SKIP_CODE]
        skip_path = self._dict_pub_bl[PP.S_KEY_SKIP_PATH]

        # ----------------------------------------------------------------------
        # do the fixes
        # NB: root is a full path, dirs and files are relative to root
        for root, root_dirs, root_files in self._dir_prj.walk():

            # handle dirs in skip_all
            if root in skip_all:
                # NB: don't recurse into subfolders
                root_dirs.clear()
                continue

            # convert files into Paths
            files = [root / f for f in root_files]

            # for each file item
            for item in files:

                # for each new file, reset block and line switches to def
                # NB: line switches always default to current block switches
                self._dict_sw_block = dict(PP.D_SWITCH_DEF)
                self._dict_sw_line = dict(self._dict_sw_block)

                # handle files in skip_all
                if item in skip_all:
                    continue

                # handle dirs/files in skip_contents
                if not root in skip_contents and not item in skip_contents:

                    # handle dirs/files in skip_header
                    bl_hdr = root in skip_header or item in skip_header

                    # handle dirs/files in skip_code
                    bl_code = root in skip_code or item in skip_code

                    # fix content with appropriate dict
                    self._fix_contents(item, bl_hdr, bl_code)

                # handle files in skip_path
                if not item in skip_path:
                    self._fix_path(item)

            # handle dirs in skip_path
            if not root in skip_path:
                self._fix_path(root)

        # done
        print(PP.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # Do any work after fix
    # --------------------------------------------------------------------------
    def _do_after_fix(self):
        """
        Do any work after fix

        Do any work after fix. This method is called just after _do_after_fix,
        after all files have been modified.\n
        It is mostly used to tweak files once all the normal fixes have been
        applied.
        """

        PP.do_after_fix(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_debug
        )

    # --------------------------------------------------------------------------
    # Do any work before making dist
    # --------------------------------------------------------------------------
    def _do_before_dist(self):
        """
        Do any work before making dist

        Do any work on the dist folder before it is created. This method is
        called after _do_after_fix, and before _do_dist.
        """

        PP.do_before_dist(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_debug
        )

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

        # ----------------------------------------------------------------------
        # do common dist stuff

        # find old dist? nuke it from orbit! it's the only way to be sure!
        a_dist = self._dir_prj / PP.S_DIR_DIST
        if a_dist.is_dir():
            shutil.rmtree(a_dist)

        # make child dir in case we nuked
        name_fmt = self._dict_prv_prj["__PP_DIST_DIR__"]
        p_dist = a_dist / name_fmt
        p_dist.mkdir(parents=True)

        # for each key, val (type, dict)
        for key, val in self._dict_pub_dist.items():

            # get src/dst rel to prj dir/dist dir
            src = self._dir_prj / key
            dst = p_dist / val
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

        # done copying project files
        print(PP.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # Do any work after making dist
    # --------------------------------------------------------------------------
    def _do_after_dist(self):
        """
        Do any work after making dist

        Do any work on the dist folder after it is created. This method is
        called after _do_dist. Currently, this method purges any "ABOUT" file
        used as placeholders for github syncing. It also tars the source folder
        if it is a package, making for one (or two) less steps in the user's
        install process.
        """

        PP.do_after_dist(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_debug
        )

    # --------------------------------------------------------------------------
    # These are minor steps called from the main steps
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Convert items in blacklist to absolute Path objects
    # --------------------------------------------------------------------------
    def _fix_blacklist_paths(self, dict_bl):
        """
        Convert items in blacklist to absolute Path objects

        Get absolute paths for all entries in the blacklist.
        """

        # make a copy and remove path separators in one shot
        # NB: this is mostly for glob support, as globs cannot end in path
        # separators
        for key in dict_bl:
            dict_bl[key] = [item.rstrip("/") for item in dict_bl[key]]

        # support for absolute/relative/glob
        # NB: taken from cntree.py

        # for each section of blacklist
        for key, val in dict_bl.items():
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
            dict_bl[key] = result

    # --------------------------------------------------------------------------
    # Fix header or code for each line in a file
    # --------------------------------------------------------------------------
    def _fix_contents(self, path, bl_hdr=False, bl_code=False):
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

        # check for unknown file types
        self._get_type_rules(path)
        if not self._dict_type_rules or len(self._dict_type_rules) == 0:

            # do the basic replace (file got here after skip_all/skip_contents
            # BUT NOT skip_bl/skip/code)
            self._fix_text(path)
            return

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
            # split the line into code and comm

            # we will split the line into two parts
            # NB: assume code is whole line (i.e. no trailing comment)
            split_pos = 0
            code = line
            comm = ""

            # find split sequence
            split_sch = self._dict_type_rules.get(PP.S_KEY_SPLIT, None)
            split_grp = self._dict_type_rules.get(PP.S_KEY_SPLIT_COMM, None)

            # only process files with split
            if split_sch and split_grp:

                # there may be multiple matches per line (ignore quoted markers)
                matches = re.finditer(split_sch, line)

                # only use matches that have the right group
                matches = [match for match in matches if match.group(split_grp)]
                for match in matches:

                    # split the line into code and comment (include delimiter)
                    split_pos = match.start(split_grp)
                    code = line[:split_pos]
                    comm = line[split_pos:]

                # ------------------------------------------------------------------
                # check for switches

                # reset line switch values to block switch values
                self._dict_sw_line = dict(self._dict_sw_block)

                # check switches
                self._check_switches(
                    code,
                    comm,
                    self._dict_type_rules,
                    self._dict_sw_block,
                    self._dict_sw_line,
                )

                # check for block or line replace switch
                repl = False
                if (
                    self._dict_sw_block[PP.S_SW_REPLACE] is True
                    and self._dict_sw_line[PP.S_SW_REPLACE] is True
                ) or self._dict_sw_line[PP.S_SW_REPLACE] is True:
                    repl = True

                # switch says no, gtfo
                if not repl:
                    continue

            # ------------------------------------------------------------------
            # check for header

            # check if blacklisted for headers
            if not bl_hdr:

                # check if it matches header pattern
                str_pattern = self._dict_type_rules[PP.S_KEY_HDR_SCH]
                res = re.search(str_pattern, line)
                if res:

                    # fix it
                    lines[index] = self._fix_header(line)

                    # no more processing for header line
                    continue

            # ------------------------------------------------------------------
            # not a blank, header or switch, must be code

            # check if blacklisted for code
            if not bl_code:

                # fix dunders in real code lines
                code = self._fix_code(code)

                # --------------------------------------------------------------
                # put the line back together
                lines[index] = code + comm

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
        str_pattern = self._dict_type_rules[PP.S_KEY_HDR_SCH]
        res = re.search(str_pattern, line)
        if not res:
            return line

        # pull out lead, val, and pad using group match values from M
        lead = res.group(self._dict_type_rules[PP.S_KEY_LEAD])
        val = res.group(self._dict_type_rules[PP.S_KEY_VAL])
        pad = res.group(self._dict_type_rules[PP.S_KEY_PAD])

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
    def _fix_code(self, code):
        """
        Replace dunders inside a file's contents

        Args:
            code: The code portion of the line to replace text in

        Returns:
            The new line of code

        Replaces text inside the code portion of a  line. Given a line,
        replaces dunders as it goes. When it is done, it returns the new line.
        This replaces the __PP dunders inside the file, excluding blank lines,
        headers, and flag switches (all of which are previously handled in
        _fix_contents).
        """

        # replace content using current flag setting
        for key, val in self._dict_rep.items():
            if isinstance(val, str):
                code = code.replace(key, val)

        # return the (maybe replaced) line
        return code

    # --------------------------------------------------------------------------
    # Replace dunders inside a file's contents
    # --------------------------------------------------------------------------
    def _fix_text(self, path):
        """
        Replace dunders inside a file's contents

        Args:
            path: The path to the file to fix text

        Returns:
            The new line of code

        Replaces text inside the a file. This is a qnd function to replace any
        dunder in any file, regardless of D_TYPE_RULES. Think of it as an
        oubliette for fi;es you just want to 'undunderize'.
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

            # replace content using current flag setting
            for key, val in self._dict_rep.items():
                if isinstance(val, str):
                    line = line.replace(key, val)

            # put new line back in file
            lines[index] = line

        # open and write file
        with open(path, "w", encoding=PP.S_ENCODING) as a_file:
            a_file.writelines(lines)

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
    def _check_switches(
        self, code, comm, dict_type_rules, dict_sw_block, dict_sw_line
    ):
        """
        Check if line or trailing comment is a switch

        Args:
            comm: The comment part of a line to check for switches
            dict_type_rules: Dictionary containing the regex to look for
            dict_sw: Dictionary of switch values for either block or line
            switches

        This method checks to see if a line or trailing comment contains a
        valid switch for the values in dict_type_rules. If a valid switch is
        found, it sets the appropriate flag in either dict_sw_block or
        dict_sw_line.
        """

        # switch does not appear anywhere in line
        res = re.search(dict_type_rules[PP.S_KEY_SW_SCH], comm)
        if not res:
            return

        # find all matches (case insensitive)
        matches = re.finditer(
            dict_type_rules[PP.S_KEY_SW_SCH], comm, flags=re.I
        )

        # for each match
        for match in matches:

            # get key/val of switch
            key = match.group(dict_type_rules[PP.S_KEY_SW_KEY])
            val = match.group(dict_type_rules[PP.S_KEY_SW_VAL])

            # try a bool conversion
            # NB: in honor of John Valby (ddg him!)
            val_b = val.lower()
            if val_b == "true":
                val = True
            elif val_b == "false":
                val = False

            # pick a dict based on if there is preceding code
            if code.strip() == "":
                dict_sw_block[key] = val
            else:
                dict_sw_line[key] = val

    # --------------------------------------------------------------------------
    # Check project type for allowed characters
    # --------------------------------------------------------------------------
    def _check_sem_ver(self, version):
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
        pattern = PP.S_SEM_VER_VALID
        return re.search(pattern, version)

    # --------------------------------------------------------------------------
    # Reload dicts after any outside changes
    # --------------------------------------------------------------------------
    def _reload_dicts(self):
        """
        Reload dicts after any outside changes

        This function is called when a dict is passed to another function, in
        order to keep it synced with the internal dict.
        """

        # update individual dicts in dict_prv
        self._dict_prv_all = self._dict_prv[PP.S_KEY_PRV_ALL]
        self._dict_prv_prj = self._dict_prv[PP.S_KEY_PRV_PRJ]

        # update individual dicts in dict_pub
        self._dict_pub_bl = self._dict_pub[PP.S_KEY_PUB_BL]
        self._dict_pub_dbg = self._dict_pub[PP.S_KEY_PUB_DBG]
        self._dict_pub_dist = self._dict_pub[PP.S_KEY_PUB_DIST]
        self._dict_pub_i18n = self._dict_pub[PP.S_KEY_PUB_I18N]
        self._dict_pub_meta = self._dict_pub[PP.S_KEY_PUB_META]

        # update debug dict
        if not self._debug:
            self._dict_debug = self._dict_pub_dbg

    # --------------------------------------------------------------------------
    # Save project info before fix
    # --------------------------------------------------------------------------
    def _save_project_info(self):
        """
        Save project info before fix

        Saves the private.json and project.json files after all modifications,
        and reloads them to use in _do_fix.
        """

        # ----------------------------------------------------------------------
        # save project settings

        # create private settings
        dict_prv = {
            PP.S_KEY_PRV_ALL: self._dict_prv_all,
            PP.S_KEY_PRV_PRJ: self._dict_prv_prj,
        }

        # save private settings
        path_prv = self._dir_prj / PP.S_PRJ_PRV_CFG
        F.save_dict(dict_prv, [path_prv])

        # create public settings
        dict_pub = {
            PP.S_KEY_PUB_BL: self._dict_pub_bl,
            PP.S_KEY_PUB_DBG: self._dict_pub_dbg,
            PP.S_KEY_PUB_DIST: self._dict_pub_dist,
            PP.S_KEY_PUB_I18N: self._dict_pub_i18n,
            PP.S_KEY_PUB_META: self._dict_pub_meta,
        }

        # save public settings
        path_pub = self._dir_prj / PP.S_PRJ_PUB_CFG
        F.save_dict(dict_pub, [path_pub])

        # ----------------------------------------------------------------------
        # fix dunders in dict_pub w/o _dict_rep (project.json)
        self._fix_contents(path_pub)

        # reload dict from fixed file
        dict_pub = F.load_dicts([path_pub])
        self._reload_dicts()

    # --------------------------------------------------------------------------
    # Get the filetype-specific regexes (headers, comments. switches)
    # --------------------------------------------------------------------------
    def _get_type_rules(self, path):
        """
        Get the filetype-specific regexes (headers, comments. switches)

        Args:
            path: Path of the file go get the dict of regexes for

        Returns:
            The dict of regexes for this file type. This dict contains
            language-specific regexes for matching header lines, comments, and
            switches.
        """

        # default result is empty dict (to match declaration in __init__)
        # NB: empty dict means unknown type rep
        self._dict_type_rules = {}

        # iterate over reps
        for _key, val in PP.D_TYPE_RULES.items():

            # fix ets if necessary
            exts = val[PP.S_KEY_RULES_EXT]
            exts = [
                f".{item}" if not item.startswith(".") else item
                for item in exts
            ]
            exts = [item.lower() for item in exts]

            # if we match ext, return only rep stuff
            # NB: also handles dot files (FUUUUUUCK)
            if path.suffix.lower() in exts or path.name.lower() in exts:
                self._dict_type_rules = val[PP.S_KEY_RULES_REP]
                return


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
