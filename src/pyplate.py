# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pyplate.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pyplate: replace=False

"""
A class to be the base for pymaker/pybaker

This is the base class that contains code common to both PyMaker and PyBaker.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
import gettext
import locale
import logging
from pathlib import Path
import re
import sys

# local imports
import cnlib.cnfunctions as F  # type: ignore
from cnlib.cnformatter import CNFormatter  # type: ignore

# ------------------------------------------------------------------------------
# local imports

# pylint: disable=wrong-import-position

# fudge the path to import conf stuff
P_DIR_PRJ = Path(__file__).parents[1].resolve()
sys.path.append(str(P_DIR_PRJ))

import conf.conf as C  # type: ignore

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./py[m|b]aker.py

# path to project dir
T_DIR_PRJ = P_DIR_PRJ

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
class PyPlate:
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class implements all the needed functionality of PyMaker, to create a
    PyPlate project from a template.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # path to default log file
    # NB: if not using, set to None
    P_LOG_DEF = P_DIR_PRJ / "log/pyplate.log"

    # pyplate: replace=True

    # short description
    # pylint: disable=line-too-long
    # NB: need to keep on one line for replacement
    S_PP_SHORT_DESC = "A program for creating and building CLI/GUI/Packages in Python from a template"
    # pylint enable=line-too-long

    # version string
    S_PP_VERSION = "Version 0.0.10"

    # pyplate: replace=False

    # debug option strings
    S_ARG_DBG_OPTION = "-d"
    S_ARG_DBG_ACTION = "store_true"
    S_ARG_DBG_DEST = "DBG_DEST"
    # I18N help string for debug cmd line option
    S_ARG_DBG_HELP = _("enable debugging mode")

    # config option strings
    S_ARG_HLP_OPTION = "-h"
    S_ARG_HLP_ACTION = "store_true"
    S_ARG_HLP_DEST = "HLP_DEST"
    # I18N: help option help
    S_ARG_HLP_HELP = _("show this help message and exit")

    # about string (to be set by subclass)
    S_ABOUT = ""

    # I18N if using argparse, add help at end of about
    S_ABOUT_HELP = _("Use -h for help") + "\n"

    # cmd line instructions string (to be set by subclass)
    S_EPILOG = ""

    # default format af log files
    S_LOG_FMT = "%(asctime)s [%(levelname)-7s] %(message)s"
    S_LOG_DATE_FMT = "%Y-%m-%d %I:%M:%S %p"

    # error strings
    # I18N: general error start
    S_ERR_ERR = _("Error:")

    # --------------------------------------------------------------------------
    # Instance methods
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
        self._dict_pub_docs = {}
        self._dict_pub_i18n = {}
        self._dict_pub_meta = {}
        self._dict_pub_inst = {}
        self._dict_pub_uninst = {}

        # dictionary to hold current pm/pb debug settings
        self._dict_dbg = {}

        # log stuff
        self._logger = logging.getLogger(__name__)
        logging.basicConfig(
            filename=self.P_LOG_DEF,
            level=logging.INFO,
            format=self.S_LOG_FMT,
            datefmt=self.S_LOG_DATE_FMT,
        )

        # cmd line stuff
        # NB: placeholder to avoid comparing to None (to be set by subclass)
        self._parser = argparse.ArgumentParser(
            add_help=False,
            epilog=self.S_EPILOG,
            formatter_class=CNFormatter,
        )
        self._dict_args = {}
        self._cmd_debug = False

        # ----------------------------------------------------------------------
        # set self._dir_prj

        # assume we are running in the project dir
        # this is used in a lot of places, so just shorthand it
        self._dir_prj = Path.cwd()

        # ----------------------------------------------------------------------

        # set switch dicts to defaults
        self._dict_sw_block = dict(C.D_SWITCH_DEF)
        self._dict_sw_line = dict(C.D_SWITCH_DEF)

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
        print(self.S_ABOUT_HELP)

        # ----------------------------------------------------------------------
        # use cmd line

        # add debug option
        self._parser.add_argument(
            self.S_ARG_DBG_OPTION,
            dest=self.S_ARG_DBG_DEST,
            help=self.S_ARG_DBG_HELP,
            action=self.S_ARG_DBG_ACTION,
        )

        # add help option
        self._parser.add_argument(
            self.S_ARG_HLP_OPTION,
            dest=self.S_ARG_HLP_DEST,
            help=self.S_ARG_HLP_HELP,
            action=self.S_ARG_HLP_ACTION,
        )

        # run the parser
        args = self._parser.parse_args()
        self._dict_args = vars(args)

        # ----------------------------------------------------------------------
        # check for one-shot args

        # if -h passed, this will print and exit
        if self._dict_args.get(self.S_ARG_HLP_DEST, False):

            # print usage and arg info and exit
            self._parser.print_help()
            print()
            sys.exit(0)

        # no -h, print epilog
        print(self.S_EPILOG)
        print()

        # ----------------------------------------------------------------------
        # debug stuff

        # get the args
        self._cmd_debug = self._dict_args.get(
            self.S_ARG_DBG_DEST, self._cmd_debug
        )

        # set debug flags in cnfunctions and conf
        F.B_DEBUG = self._cmd_debug
        C.B_DEBUG = self._cmd_debug

        # maybe yell
        if self._cmd_debug:

            # yup, yell
            F.printc(C.S_MSG_DEBUG, bg=F.C_BG_RED, fg=F.C_FG_WHITE, bold=True)
            print()

    # ------------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # ------------------------------------------------------------------------------
    def _teardown(self):
        """
        Boilerplate to use at the end of main

        Perform some mundane stuff like saving properties.
        """

        # ----------------------------------------------------------------------
        # save private

        try:
            # save private settings
            path_prv = self._dir_prj / C.S_PRJ_PRV_CFG
            F.save_dict_into_paths(self._dict_prv, [path_prv])
        except OSError as e:  # from save_dict
            F.printd(self.S_ERR_ERR, str(e))

        # ----------------------------------------------------------------------
        # save public

        try:
            # save public settings
            path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
            F.save_dict_into_paths(self._dict_pub, [path_pub])
        except OSError as e:  # from save_dict
            F.printd(self.S_ERR_ERR, str(e))

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

        C.do_before_fix(
            self._dir_prj,
            self._dict_prv,
            self._dict_pub,
            self._dict_dbg,
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
        print(C.S_ACTION_FIX, end="", flush=True)

        # last chance to do shit w/ dicts
        self._fix_dicts()

        # ----------------------------------------------------------------------

        # fix up blacklist and convert relative or glob paths to absolute Path
        # objects

        # get a read-only copy of the blacklist
        dict_bl = dict(self._dict_pub_bl)

        # for each section of blacklist
        for key, val in dict_bl.items():

            # convert all items in list to Path objects
            list_res = []
            for item in val:
                res = list(self._dir_prj.glob(item))
                list_res.extend(res)

            dict_bl[key] = list_res

        # just shorten the names
        skip_all = dict_bl[C.S_KEY_SKIP_ALL]
        skip_contents = dict_bl[C.S_KEY_SKIP_CONTENTS]
        skip_header = dict_bl[C.S_KEY_SKIP_HEADER]
        skip_code = dict_bl[C.S_KEY_SKIP_CODE]

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
                self._dict_sw_block = dict(C.D_SWITCH_DEF)
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

                # handle file paths with dunders
                self._fix_path(item)

            # handle dirs with dunders
            self._fix_path(root)

        # done
        F.printc(C.S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)

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

        C.do_after_fix(
            self._dir_prj,
            self._dict_prv,
            self._dict_pub,
            self._dict_dbg,
        )

    # --------------------------------------------------------------------------
    # These are minor steps called from the main steps
    # --------------------------------------------------------------------------

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
        self._dict_type_rules = get_type_rules(path)
        if not self._dict_type_rules or len(self._dict_type_rules) == 0:

            # do the basic replace (file got here after skip_all/skip_contents
            # BUT NOT skip_hdr/skip_code)
            self._fix_text(path)
            return

        # default lines
        lines = []

        # open and read file
        with open(path, "r", encoding=C.S_ENCODING) as a_file:
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
            split_sch = self._dict_type_rules.get(C.S_KEY_SPLIT, None)
            split_grp = self._dict_type_rules.get(C.S_KEY_SPLIT_COMM, None)

            # only process files with split
            if split_sch and split_grp:

                # there may be multiple matches per line (ignore quoted markers)
                matches = re.finditer(split_sch, line)

                # only use matches that have the right group
                matches = [
                    match for match in matches if match.group(split_grp)
                ]
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
                check_switches(
                    code,
                    comm,
                    self._dict_type_rules,
                    self._dict_sw_block,
                    self._dict_sw_line,
                )

                # check for block or line replace switch
                repl = False
                if (
                    self._dict_sw_block[C.S_SW_REPLACE] is True
                    and self._dict_sw_line[C.S_SW_REPLACE] is True
                ) or self._dict_sw_line[C.S_SW_REPLACE] is True:
                    repl = True

                # switch says no, gtfo
                if not repl:
                    continue

            # ------------------------------------------------------------------
            # check for header

            # check if blacklisted for headers
            if not bl_hdr:

                # check if it matches header pattern
                str_pattern = self._dict_type_rules[C.S_KEY_HDR_SCH]
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
        with open(path, "w", encoding=C.S_ENCODING) as a_file:
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
        str_pattern = self._dict_type_rules[C.S_KEY_HDR_SCH]
        res = re.search(str_pattern, line)
        if not res:
            return line

        # pull out lead, val, and pad using group match values from M
        lead = res.group(self._dict_type_rules[C.S_KEY_LEAD])
        val = res.group(self._dict_type_rules[C.S_KEY_VAL])
        pad = res.group(self._dict_type_rules[C.S_KEY_PAD])

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

        Replaces text inside a file. This is a qnd function to replace any
        dunder in any file, regardless of D_TYPE_RULES. Think of it as an
        oubliette for files you just want to 'undunderize'.
        """

        # default lines
        lines = []

        # open and read file
        with open(path, "r", encoding=C.S_ENCODING) as a_file:
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
        with open(path, "w", encoding=C.S_ENCODING) as a_file:
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
    # Make reps, save public, fix public dunders, reload sub dicts
    # --------------------------------------------------------------------------
    def _fix_dicts(self):
        """
        Make reps, save/fix public dunders, reload sub dicts

        Make reps, save/fix public dunders, reload sub dicts
        """

        # ----------------------------------------------------------------------
        # get prv subs
        self._dict_prv_all = self._dict_prv[C.S_KEY_PRV_ALL]
        self._dict_prv_prj = self._dict_prv[C.S_KEY_PRV_PRJ]

        # ----------------------------------------------------------------------
        # get prv subs
        self._dict_rep = self._dict_prv_all | self._dict_prv_prj

        # ----------------------------------------------------------------------
        # save/fix/load public

        try:
            # save public settings
            path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
            F.save_dict_into_paths(self._dict_pub, [path_pub])
        except OSError as e:  # from save_dict
            F.printd(self.S_ERR_ERR, str(e))

        # fix dunders in dict_pub
        self._fix_contents(path_pub)

        try:
            # load public settings
            path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
            self._dict_pub = F.load_paths_into_dict([path_pub])
        except OSError as e:  # from load dict
            F.printd(self.S_ERR_ERR, str(e))

        # ----------------------------------------------------------------------
        # get pub subs
        self._dict_pub_bl = self._dict_pub[C.S_KEY_PUB_BL]
        self._dict_pub_dbg = self._dict_pub[C.S_KEY_PUB_DBG]
        self._dict_pub_dist = self._dict_pub[C.S_KEY_PUB_DIST]
        self._dict_pub_docs = self._dict_pub[C.S_KEY_PUB_DOCS]
        self._dict_pub_i18n = self._dict_pub[C.S_KEY_PUB_I18N]
        self._dict_pub_meta = self._dict_pub[C.S_KEY_PUB_META]
        self._dict_pub_inst = self._dict_pub[C.S_KEY_PUB_INST]
        self._dict_pub_uninst = self._dict_pub[C.S_KEY_PUB_UNINST]


        # set initial debug
        self._dict_dbg = dict(self._dict_pub_dbg)

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
        if len(prj_type) == 1:

            # get first char and lower case it
            first_char = prj_type[0].lower()

            # check if it's one of ours
            first_char_test = [item[0].lower() for item in C.L_TYPES]
            if first_char in first_char_test:
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
        # ^([a-zA-Z]+[a-zA-Z\d\-_ ]*[a-zA-Z\d]+)$ AND OMG DID IT TAKE A LONG
        # TIME TO FIND IT! in case you were looking for it. It will give you a
        # quick yes-no answer. I don't use it here because I want to give the
        # user as much feedback as possible, so I break down the regex into
        # steps where each step explains which part of the name is wrong.

        # check for name length
        if len(name_prj.strip(" ")) < 2:
            print(C.S_ERR_LEN)
            return False

        # match start or return false
        pattern = C.D_NAME[C.S_KEY_NAME_START]
        res = re.search(pattern, name_prj)
        if not res:
            print(C.S_ERR_START)
            return False

        # match end or return false
        pattern = C.D_NAME[C.S_KEY_NAME_END]
        res = re.search(pattern, name_prj)
        if not res:
            print(C.S_ERR_END)
            return False

        # match middle or return false
        pattern = C.D_NAME[C.S_KEY_NAME_MID]
        res = re.search(pattern, name_prj)
        if not res:
            print(C.S_ERR_MID)
            return False

        # if we made it this far, return true
        return True

    # --------------------------------------------------------------------------
    # Combine reqs from template/all and template/prj_type
    # --------------------------------------------------------------------------
    def _merge_reqs(self, prj_type_long):
        """
        Combine reqs from template/all and template/prj_type

        Args:
            prj_type_long: the folder in template for the current project type

        This method combines reqs from the all dir used by all projects, and
        those used by specific project type (gui needs pygobject, etc).
        """

        # get sources and filter out sources that don't exist
        reqs_prj = P_DIR_PRJ / C.S_FILE_REQS_TYPE.format(prj_type_long)

        # get src
        src = [
            P_DIR_PRJ / C.S_FILE_REQS_ALL,
            P_DIR_PRJ / reqs_prj,
        ]
        src = [str(item) for item in src if item.exists()]

        # get dst to put file lines
        dst = self._dir_prj / C.S_FILE_REQS

        # ----------------------------------------------------------------------

        # the new set of lines for requirements.txt
        new_file = []

        # read reqs files and put in result
        for item in src:
            with open(item, "r", encoding=C.S_ENCODING) as a_file:
                old_file = a_file.readlines()
                old_file = [line.rstrip() for line in old_file]
                uniq = set(new_file + old_file)
                new_file = list(uniq)

        # put combined reqs into final file
        joint = "\n".join(new_file)
        with open(dst, "w", encoding=C.S_ENCODING) as a_file:
            a_file.writelines(joint)

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------

# NB: these functions are used in pyplate/pymaker/pybaker, but also used in
# conf. they are placed here and made public because they are not user-defined.


# ------------------------------------------------------------------------------
# Check if line or trailing comment is a switch
# ------------------------------------------------------------------------------
def check_switches(code, comm, dict_type_rules, dict_sw_block, dict_sw_line):
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
    res = re.search(dict_type_rules[C.S_KEY_SW_SCH], comm)
    if not res:
        return

    # find all matches (case insensitive)
    matches = re.finditer(dict_type_rules[C.S_KEY_SW_SCH], comm, flags=re.I)

    # for each match
    for match in matches:

        # get key/val of switch
        key = match.group(dict_type_rules[C.S_KEY_SW_KEY])
        val = match.group(dict_type_rules[C.S_KEY_SW_VAL])

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


# ------------------------------------------------------------------------------
# Get the filetype-specific regexes (headers, comments. switches)
# ------------------------------------------------------------------------------
def get_type_rules(path):
    """
    Get the filetype-specific regexes (headers, comments. switches)

    Args:
        path: Path of the file to get the dict of regexes for

    Returns:
        The dict of regexes for this file type
    """

    # iterate over reps
    for _key, val in C.D_TYPE_RULES.items():

        # fix ets if necessary
        exts = val[C.S_KEY_RULES_EXT]

        # lower case all exts
        l_exts = [item.lower() for item in exts]

        # add dots
        l_exts = [
            f".{item}" if not item.startswith(".") else item for item in l_exts
        ]

        # check if the suffix or the filename (for dot files) matches
        # NB: also checks for dot files
        if path.suffix.lower() in l_exts or path.name.lower() in l_exts:
            return val[C.S_KEY_RULES_REP]

    # default result is py rep
    return {}


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line
    print("WRONG GLASS, SIR !!!")

# -)

# Dr. Manhattan can divide by zero. Fight me.
