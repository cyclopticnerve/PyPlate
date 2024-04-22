# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: project.py                                            |     ()     |
# Date    : 04/21/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module separates out the constants from pymaker.py/pybaker.py.
This file should only be edited if you know what you are doing.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import os
from pathlib import Path
import re

# pylint: disable=no-name-in-module

# my imports
from . import keys2 as K  # type: ignore
from . import custom_pp as S  # type: ignore

# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# Path objects
# ------------------------------------------------------------------------------

# this is the dir above where this script is being run from, relative to dev
# home (e.g. Documents/Projects/Python/PyPlate/)
P_DIR_PYPLATE = Path(__file__).parents[1]

# path to lib project (e.g. ~/Documents/Projects/Python/PyPlate/lib)
P_DIR_LIB = P_DIR_PYPLATE / "lib"

# this is the dir where the template files are located relative to this script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
P_DIR_TEMPLATE = P_DIR_PYPLATE / "template"

# the common folder from template
P_DIR_ALL = P_DIR_TEMPLATE / "all"

# the location of pyplate's metadata (we update this at runtime)
P_FILE_META = P_DIR_PYPLATE / "pyplate" / "project.json"

# get path to rat file
P_FILE_RAT = Path.home() / ".config" / "pyplate" / "B_HDR_RAT"

# ------------------------------------------------------------------------------
# Bools
# ------------------------------------------------------------------------------

# a switch to do extra work if using right aligned text in headers
# check if rat file exists
B_HDR_RAT = P_FILE_RAT.exists()

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# keys for pybaker private dict
S_KEY_PRJ_DEF = "PRJ_DEF"
S_KEY_PRJ_CFG = "PRJ_CFG"

# keys for metadata, blacklist, i18n in pybaker dev dict
S_KEY_META = "META"
S_KEY_BLACKLIST = "BLACKLIST"
S_KEY_I18N = "I18N"

# keys for blacklist
S_KEY_SKIP_ALL = "SKIP_ALL"
S_KEY_SKIP_CONTENTS = "SKIP_CONTENTS"
S_KEY_SKIP_HEADER = "SKIP_HEADER"
S_KEY_SKIP_TEXT = "SKIP_TEXT"
S_KEY_SKIP_PATH = "SKIP_PATH"
S_KEY_SKIP_TREE = "SKIP_TREE"

# keys for i18n
S_KEY_CHARSET = "CHARSET"
S_KEY_TYPES = "TYPES"
S_KEY_CLANGS = "CLANGS"
S_KEY_NO_EXT = "NO_EXT"
S_KEY_LOCALE = "LOCALE"
S_KEY_PO = "PO"

# meta keys

# prj keys

# just moved out of file

# help/version strings
S_NAME_BIG = "PyMaker"
S_NAME_SMALL = "pymaker"

# the path to the pyplate's toml
S_FILE_TOML = "pyproject.toml"

# path to prj pyplate files
S_PP_PRJ = f"pyplate{os.sep}private.json"
S_PP_CFG = f"pyplate{os.sep}project.json"

# ------------------------------------------------------------------------------
# Lists
# ------------------------------------------------------------------------------

# the list of keys to replace in the header of each file
# NB: All entries must have values when using RAT
# if you want the entry blank afterwards, use "__PP_DUMMY__"
L_HEADER = [
    "Project",  # PyPlate
    "Filename",  # pyplate.py
    "Date",  # 12/08/2022
    "Author",  # cyclopticnerve
    "License",  # WTFPLv2
]

# ------------------------------------------------------------------------------
# Dictionaries
# ------------------------------------------------------------------------------

# some keys used in string replacement
D_PRJ_PRJ = {
    # dummy value to use in headers with right aligned text
    "__PP_DUMMY__": "",
}

# entries to be put in blacklist before writing to project
# NBL key is blacklist section, val is an array of strings
D_BL_AFTER = {K.S_KEY_SKIP_ALL: ["pyplate"]}

# dict of files that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project, it gets copied
# to the project, and cuts down on duplicate files
# key is the relative path to the source file in PyPlate
# val is the relative path to the dest file in the project dir
D_COPY = {
    # f"conf{os.sep}keys.py": f"pyplate{os.sep}keys.py",
}

# ------------------------------------------------------------------------------
# Regex strings
# ------------------------------------------------------------------------------

# regex strings for toml
R_TOML_NAME = r"(^\s*\[project\]\s*$)(.*?)(^\s*name[\t ]*=[\t ]*)(.*?$)"
R_TOML_NAME_REP = r'\g<1>\g<2>\g<3>"{}"'
R_TOML_VERSION = r"(^\s*\[project\]\s*$)(.*?)(^\s*version[\t ]*=[\t ]*)(.*?$)"
R_TOML_VERSION_REP = r'\g<1>\g<2>\g<3>"{}"'
R_TOML_DESC = r"(^\s*\[project\]\s*$)(.*?)(^\s*description[\t ]*=[\t ]*)(.*?$)"
R_TOML_DESC_REP = r'\g<1>\g<2>\g<3>"{}"'
R_TOML_KEYS = r"(^\s*\[project\]\s*$)(.*?)(^\s*keywords[\t ]*=[\t ]*)(.*?\])"
R_TOML_KEYS_REP = r"\g<1>\g<2>\g<3>[{}]"
R_TOML_DEPS = (
    r"(^\s*\[project\]\s*$)(.*?)(^\s*dependencies[\t ]*=[\t ]*)(.*?\])"
)
R_TOML_DEPS_REP = r"\g<1>\g<2>\g<3>[{}]"

# search and sub flags
# NB: need S for multiline matches, M for caret match
R_TOML_SUB_FLAGS = re.S | re.M

# regex strings for headers
# weezer's "i got my hash pipe" plays in one of the hundreds of open tabs in my
# brain
# GET IT? HASHPIPE! like hash (#) pipe (|)!
# HA HA HA HA!
# oh god i need a life...
# NB: format param is a value from L_HEADER
R_HEADER = (
    r"^(\s*(#|<!--)\s*{}\s*:)"  # group 1/2 - ((#) Project:)
    r"(\s*)(\S*)"  # group 3/4 - (s)(__DUNDER__)
    r"(\s*)(.*)"  # group 5/6 - (s)(rat)
)

# header replacement string
# NB: format params are dunder's replacement and trailing text
R_HEADER_REP = r"\g<1>\g<3>{}{}\g<6>"

# search and sub flags
# NB: need M for caret match
R_HDR_SCH_FLAGS = re.M
R_HDR_SUB_FLAGS = re.M

# --------------------------------------------------------------------------
# Public methods
# --------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Set up user paths
# ------------------------------------------------------------------------------
def get_user_paths():
    """
    Set up user paths

    Here we calculate the different paths to use for dunder replacement. It is
    done as a function so we can call it after the project name has been set.
    """

    # get values after pymaker has set them
    author = S.D_PRJ_DEF["__PD_AUTHOR__"]
    name_small = S.D_PRJ_CFG["__PC_NAME_SMALL__"]

    # paths relative to the end user's (or dev's) useful folders
    S.D_PRJ_CFG["__PC_USR_CONF__"] = f"{S.S_USR_CONF}{os.sep}{name_small}"
    S.D_PRJ_CFG["__PC_USR_SRC__"] = f"{S.S_USR_SRC}{os.sep}{name_small}"
    S.D_PRJ_CFG["__PC_USR_LIB__"] = (
        f"{S.S_USR_LIB}{os.sep}{author}{os.sep}{S.S_USR_LIB_NAME}"
    )

    # a string of the path above, but without dev home dir
    h = str(Path.home())
    s = str(P_DIR_PYPLATE)
    s = s.replace(h, "")
    s = s.lstrip(os.sep)
    pyplate_dir = s

    # paths to real pybaker and lib
    S.D_PRJ_CFG["__PC_DEV_LIB__"] = f"{pyplate_dir}{os.sep}lib"
    S.D_PRJ_CFG["__PC_PYBAKER__"] = (
        f"{pyplate_dir}{os.sep}src{os.sep}pybaker.py"
    )


# --------------------------------------------------------------------------
# Replace dunders inside headers
# --------------------------------------------------------------------------
def fix_header(path):
    """
    Replace dunders inside headers

    Arguments:
        path: Path for replacing header text

    Replaces header text inside a file. Given a Path object, it iterates
    the lines one by one, replacing the value found in the form of a key in
    the _dict_repls dictionary as it goes. When it is done, it saves the
    new lines back to the file. This replaces the __PD/__PM dunders inside
    headers. Using this method, we preserve any right-aligned text in each
    header row (see the header in this file for an example). Adapting this
    method to your style of header should be easy by modifying the regex
    pattern, and modifying L_HEADER to suit.

    NOTE: This method relies HEAVILY on the fact that the value exists, if
    using right-aligned text. If you do not want a value, use "__PP_DUMMY__".
    """

    # combine public and private dunders
    dict_repls = {}
    for key, val in S.D_PRJ_DEF.items():
        dict_repls[key] = val
    for key, val in S.D_PRJ_CFG.items():
        dict_repls[key] = val
    for key, val in D_PRJ_PRJ.items():
        dict_repls[key] = val

    # open and read file
    with open(path, "r", encoding="UTF-8") as a_file:
        lines = a_file.read()

    # for each header key
    for item in L_HEADER:  # "Project"

        # put keyword in regex pattern
        str_pattern = R_HEADER.format(item)

        # find first instance of header pattern
        # search for regex with "# Project : xxx...\n"
        res = re.search(str_pattern, lines, flags=R_HDR_SCH_FLAGS)

        # no res, keep going
        if not res:
            continue

        # replace bits
        repl = res.group(4)

        # save old len for padding
        old_len = len(repl)

        # do string replacement
        for key_set, val_set in dict_repls.items():
            repl = repl.replace(key_set, val_set)

        # get the new len and the difference
        new_len = len(repl)
        len_diff = new_len - old_len
        abs_diff = abs(len_diff)

        # add or remove spaces from pad
        pad = res.group(5)

        # string got longer, remove leading spaces
        if len_diff > 0:
            pad = pad[abs_diff:]
        else:
            # string got shorter, insert leading spaces
            s_pad = " " * abs_diff
            pad = s_pad + pad

        # replace text in the line
        str_rep = R_HEADER_REP.format(repl, pad)
        lines = re.sub(str_pattern, str_rep, lines, flags=R_HDR_SUB_FLAGS)

    # save lines to file
    with open(path, "w", encoding="UTF-8") as a_file:
        a_file.write(lines)

    # # default lines
    # lines = []

    # # open and read file
    # with open(path, "r", encoding="UTF-8") as a_file:
    #     lines = a_file.readlines()

    # # for each line in header
    # for index, line in enumerate(lines):

    #     # for each header key
    #     # for item in S.D_HEADER: # "Project": "__PC_NAME_BIG__"
    #     for item in S.L_HEADER: # "Project"

    #         # look for a header key
    #         str_pattern = S.R_HEADER.format(item)

    #         # find first instance of header pattern
    #         # search for regex with "# Project : xxx...\n"
    #         res = re.search(str_pattern, line)

    #         # no res, keep going
    #         if not res:
    #             continue

    #         # val_found in file is group 7
    #         # if res is '# Project : __PC_NAME_BIG__ <s>/          \\\n"
    #         # val_found is '__PC_NAME_BIG__'
    #         # if res is '# Filename: __PC_NAME_SMALL___test.py <s>|     ()     |\n"
    #         # val_found is '__PC_NAME_SMALL___test.py'
    #         val_found = res.group(7)

    #         repl = self._dict_repls.get(val_found, val_found)
    #         # pad = res.group(8)
    #         # rest = res.group(9)
    #         # nl = res.group(10)

    #         # # do all dunder replacements in val_found
    #         # # also calculate len diff if using right-aligned text
    #         # old_len = len(val_found)
    #         # for key_set, val_set in self._dict_repls.items():
    #         #     val_found = val_found.replace(key_set, val_set)
    #         # new_len = len(val_found)

    #         # pad = ""
    #         # len_diff = new_len - old_len
    #         # if len_diff > 0:
    #         #     pad = " " * len_diff
    #         # else:
    #         #     rem = " " * abs(len_diff)
    #         #     rest.ltrim(rem)

    #         # count what we will need without spaces
    #         len_res = (
    #             len(res.group(1))
    #             + len(repl)
    #             + len(res.group(8))
    #             + len(res.group(10))
    #         )

    #         # make spaces
    #         # NB: this looks funky but it works:
    #         # 1. get the length of the old line (NOT always 80 since we
    #         # can't have trailing spaces)
    #         # 3. subtract the match lengths
    #         # 2. subtract 1 for newline
    #         len_padding = len(line) - len_res - 1
    #         padding = " " * len_padding

    #         # replace text in the line
    #         str_rep = S.R_HEADER_REP.format(repl, padding)
    #         lines[index] = re.sub(str_pattern, str_rep, line)

    # # save lines to file
    # with open(path, "w", encoding="UTF-8") as a_file:
    #     a_file.writelines(lines)


# -)
