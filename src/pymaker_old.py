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
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# add lib path to import search
PATH_LIB = Path(__file__).parents[1] / "lib"
sys.path.append(str(PATH_LIB))

# add PyPlate path to import search
PATH_CONF = Path(__file__).parents[1]
sys.path.append(str(PATH_CONF))

from cnlib.cnformatter import CNFormatter  # type: ignore
from cnlib.cntree import CNTree  # type: ignore
from cnlib.cnpot import CNPotPy  # type: ignore
from conf import settings as S

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=import-error
# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by pybaker.py (from pyplate/conf/settings.json)
# NB: these are one-time settings created by pymaker and should not be edited
# dunders will be used for string replacement here, and checking in pybaker
# also, some entries are moved here from S.DICT_USER for convenience
# others are calculated from user entries in the cli
DICT_SETTINGS = {
    "__PP_AUTHOR__": S.DICT_USER["__PP_AUTHOR__"],
    "__PP_EMAIL__": S.DICT_USER["__PP_EMAIL__"],
    "__PP_LICENSE_NAME__": S.DICT_USER["__PP_LICENSE_NAME__"],
    "__PP_LICENSE_FILE__": S.DICT_USER["__PP_LICENSE_FILE__"],
    "__PP_DATE_FMT__": S.DICT_USER["__PP_DATE_FMT__"],
    "__PP_README_FILE__": S.DICT_README["RM_FILENAME"],
    "__PP_TYPE_PRJ__": "",  # 'c'
    "__PP_DIR_PRJ__": "",  # '~/Documents/Projects/Python/CLIs/PyPlate'
    "__PP_NAME_BIG__": "",  # PyPlate
    "__PP_NAME_SMALL__": "",  # pyplate
    "__PP_NAME_MOD__": "",  # module1.py
    "__PP_DATE__": "",  # 12/08/2022
    "__PP_NAME_CLASS__": "",  # Pascal case name for classes
    "__PP_DIR_LIB__": S.DIR_LIB,  # location of cnlibs dir
}


# parse command line
DICT_ARGS = {}

# DEBUG flag on command line
DEBUG = False

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------


# version string for -h/-v option (to be fixed in _fix_help)
S_HELP_VERSION = ""

# version option strings
S_VER_OPTION = "v"
S_VER_OPTION_LONG = "version"
S_VER_ACTION = "version"
S_VER_VERSION = S_HELP_VERSION

# config debug strings
S_DBG_OPTION = "d"
S_DBG_OPTION_LONG = "debug"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP = "enable debugging option"

# config update strings
S_UPD_OPTION = "u"
S_UPD_OPTION_LONG = "update"
S_UPD_ACTION = "store_true"
S_UPD_DEST = "UPD_DEST"
S_UPD_HELP = "update installed libs"


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Main function of the program
# ------------------------------------------------------------------------------
def main():
    """
    Main function of the program

    Main entry point for the program, initializing the program, and performing
    its steps.
    """

    # fix help string/toml file
    _fix_help_and_toml()

    # get cmd line args
    global DICT_ARGS
    DICT_ARGS = _setup_parser()

    # check for debug flag
    if DICT_ARGS.get(S_DBG_DEST, False):
        # set the global
        global DEBUG
        DEBUG = True

    # check for update flag
    if DICT_ARGS.get(S_UPD_DEST, False):
        # copy latest libs from here to project
        shutil.copytree(PATH_LIB, S.DIR_LIB, dirs_exist_ok=True)
        print(S.S_PRJ_UPDATE.format(S.DIR_LIB))
        sys.exit()


    # get info
    get_project_info()

    # copy template
    copy_template()

    # do i18n stuff
    if DICT_SETTINGS["__PP_TYPE_PRJ__"] in S.LIST_I18N:
        do_i18n()

    # copy any files that may need to be fixed
    do_before_fix()

    # do replacements in final project location
    do_fix()

    # do extra stuff to final dir after fix
    do_after_fix()


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_project_info():
    """
    Get project info

    Asks the user for project info, such as type and name, to be saved to
    DICT_SETTINGS.
    """

    # --------------------------------------------------------------------------

    # first question is type
    # NB: keep asking until we get a response that is one of the types

    # sanity check
    type_prj = ""

    # get possible types
    list_types = [f"{key} ({val[0]})" for (key, val) in S.DICT_TYPES.items()]
    str_types = " | ".join(list_types)
    in_type = f"{S.S_PRJ_TYPE} [{str_types}]: "

    # loop forever until we get a valid type (or user presses Ctrl+S)
    while True:
        # ask for type of project
        type_prj = input(in_type)

        # check for valid type
        if _check_type(type_prj):
            # at this point, type is valid so exit loop
            break

    # save project type
    DICT_SETTINGS["__PP_TYPE_PRJ__"] = type_prj

    # get output subdir
    dir_type = S.DICT_TYPES[type_prj][1]

    # --------------------------------------------------------------------------

    # next question is name
    # NB: keep asking until we get a response that is a valid name and does not
    # already exist

    # sanity check
    name_prj = ""

    # loop forever until we get a valid name (or user presses Ctrl+S)
    while True:
        # ask for name of project
        name_prj = input(f"{S.S_PRJ_NAME}: ")

        # check for valid name
        if _check_name(name_prj):
            # set up for existence check
            tmp_dir = S.DIR_BASE / dir_type / name_prj

            # check if project already exists
            if tmp_dir.exists():
                print(S.S_NAME_ERR.format(name_prj, dir_type))
            else:
                break

    # calculate final project location
    DICT_SETTINGS["__PP_DIR_PRJ__"] = str(S.DIR_BASE / dir_type / name_prj)

    # at this point, both dir and name are valid, so store both and exit
    # NB: make sure to store the project dir as a string, so it can be saved
    # to file
    DICT_SETTINGS["__PP_NAME_BIG__"] = name_prj

    # calculate small name
    info_name_small = name_prj.lower()
    DICT_SETTINGS["__PP_NAME_SMALL__"] = info_name_small

    # --------------------------------------------------------------------------
    # here we figure out the default module name for a pkg

    # sanity check
    name_mod = info_name_small

    # if it is a project type that needs a module name, ask for it
    if DICT_SETTINGS["__PP_TYPE_PRJ__"] in S.LIST_PKG:

        # loop forever until we get a valid name (or user presses Ctrl+S)
        while True:

            # ask for name of module
            name_mod = input(f"{S.S_MOD_NAME}: ")

            # check for valid name
            if _check_name(name_mod):
                break

    # set the property
    DICT_SETTINGS["__PP_NAME_MOD__"] = name_mod

    # --------------------------------------------------------------------------
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
    DICT_SETTINGS["__PP_NAME_CLASS__"] = new_name

    # --------------------------------------------------------------------------

    # calculate current date (format assumed from constants above)
    # NB: this gives us a create date that we cannot get reliably from Linux
    # later this may be changed to modified date
    now = datetime.now()
    fmt_date = S.DICT_USER["__PP_DATE_FMT__"]
    info_date = now.strftime(fmt_date)
    DICT_SETTINGS["__PP_DATE__"] = info_date


# ------------------------------------------------------------------------------
# Copy template files to final location
# ------------------------------------------------------------------------------
def copy_template():
    """
    Copy template files to final location

    Gets dirs/files from template and copies them to the project dir.
    """

    # copy latest libs from here to project
    shutil.copytree(PATH_LIB, S.DIR_LIB, dirs_exist_ok=True)

    # get the project final dir
    dir_prj = Path(DICT_SETTINGS["__PP_DIR_PRJ__"])

    # --------------------------------------------------------------------------
    # do all

    # get input dir for common dirs/files
    dir_in = S.DIR_TEMPLATE / S.S_DIR_ALL

    # copy common stuff
    shutil.copytree(dir_in, dir_prj)

    # --------------------------------------------------------------------------
    # iterate template type and copy/merge to project dir

    # get a path to the template dir for this project type
    prj_type = DICT_SETTINGS["__PP_TYPE_PRJ__"]

    # get the src dir in the template dir
    dir_template = S.DIR_TEMPLATE / S.DICT_TYPES[prj_type][2]

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


# ------------------------------------------------------------------------------
# Do i18n stuff if the project is a GUI
# ------------------------------------------------------------------------------
def do_i18n():
    """
    Do i18n stuff if the project is a GUI
    """

    # check kif we need to do this
    if DICT_SETTINGS["__PP_TYPE_PRJ__"] not in S.LIST_I18N:
        return

    # get project dir
    dir_prj = Path(DICT_SETTINGS["__PP_DIR_PRJ__"])

    # output dir (where the .pot and locale files will go)
    dir_locale = dir_prj / S.S_DIR_LOCALE
    dir_po = dir_prj / S.S_DIR_PO

    # create the potpy object
    potpy = CNPotPy(
        dir_prj,
        DICT_SETTINGS["__PP_NAME_BIG__"],
        "0.0.0",
        DICT_SETTINGS["__PP_EMAIL__"],
        dir_locale=dir_locale,
        dir_po=dir_po,
        str_domain=DICT_SETTINGS["__PP_NAME_BIG__"],
        dict_clangs=S.DICT_CLANGS,
        dict_no_ext=S.DICT_CLANGS_NO_EXT,
        charset=S.S_POT_CHARSET_DEF,
    )

    # I18N: run cnpot
    potpy.make_pot()
    potpy.make_pos()
    potpy.make_mos()


# ------------------------------------------------------------------------------
# Copy/create any other files before running do_fix
# ------------------------------------------------------------------------------
def do_before_fix():
    """
    Copy/create any other files before running do_fix

    Adds dirs/files to the project before running the fix function.
    """

    # project directory
    path_prj = DICT_SETTINGS["__PP_DIR_PRJ__"]
    path_prj = Path(path_prj)

    # create output paths starting at path_prj
    # NB: the same path scheme for blacklist is used in _fix_blacklist_dunders
    # MAKE SURE THEY MATCH!!!
    path_blacklist = path_prj / S.S_DIR_PP / S.S_DIR_CONF / S.S_FILE_BLACKLIST
    path_blacklist_def = (
        path_prj
        / S.S_DIR_PP
        / S.S_DIR_CONF
        / S.S_DIR_CONF_DEFS
        / S.S_FILE_BLACKLIST_DEF
    )
    path_metadata = path_prj / S.S_DIR_PP / S.S_DIR_CONF / S.S_FILE_METADATA
    path_metadata_def = (
        path_prj
        / S.S_DIR_PP
        / S.S_DIR_CONF
        / S.S_DIR_CONF_DEFS
        / S.S_FILE_METADATA_DEF
    )
    path_settings = path_prj / S.S_DIR_PP / S.S_DIR_CONF / S.S_FILE_SETTINGS
    path_settings_def = (
        path_prj
        / S.S_DIR_PP
        / S.S_DIR_CONF
        / S.S_DIR_CONF_DEFS
        / S.S_FILE_SETTINGS_DEF
    )

    # NB: we write the conf files to ensure they are the same before any
    # modifications

    def _dict_to_file(a_dict, a_file):
        with open(a_file, "w", encoding="UTF-8") as f:
            json.dump(a_dict, f, indent=4)

    # create all conf files and defaults
    _dict_to_file(S.DICT_BLACKLIST, path_blacklist)
    _dict_to_file(S.DICT_BLACKLIST, path_blacklist_def)
    _dict_to_file(S.DICT_METADATA, path_metadata)
    _dict_to_file(S.DICT_METADATA, path_metadata_def)
    _dict_to_file(DICT_SETTINGS, path_settings)
    _dict_to_file(DICT_SETTINGS, path_settings_def)

    # copy linked files
    for key, val in S.DICT_COPY.items():

        # first get full source path
        path_in = S.DIR_PYPLATE / key

        # then get full dest path
        path_out = path_prj / val

        # copy file
        if path_in.is_dir():
            shutil.copytree(path_in, path_out)
        else:
            shutil.copy(path_in, path_out)


# ------------------------------------------------------------------------------
# Scan dirs/files in the project for replacing text
# ------------------------------------------------------------------------------
def do_fix():
    """
    Scan dirs/files in the project for replacing text

    Scans for dirs/files under the project's location. For each dir/file it
    encounters, it passes the path to a filter to determine if the file
    needs fixing based on its appearance in the blacklist.
    """

    # fix up blacklist and convert relative or glob paths to absolute Path
    # objects
    _fix_blacklist_paths()

    # just shorten the names
    skip_all = S.DICT_BLACKLIST["PP_SKIP_ALL"]
    skip_contents = S.DICT_BLACKLIST["PP_SKIP_CONTENTS"]
    skip_header = S.DICT_BLACKLIST["PP_SKIP_HEADER"]
    skip_text = S.DICT_BLACKLIST["PP_SKIP_TEXT"]
    skip_path = S.DICT_BLACKLIST["PP_SKIP_PATH"]

    # project directory
    path_prj = DICT_SETTINGS["__PP_DIR_PRJ__"]
    path_prj = Path(path_prj)

    # --------------------------------------------------------------------------
    # do the fixes top down

    # walk from project dir
    # NB: note that root is a full path, dirs and files are relative to root
    for root, root_dirs, root_files in os.walk(path_prj):

        # convert root into Path object
        root = Path(root)

        # skip dir if in skip_all
        if root in skip_all:
            root_dirs.clear()
            continue

        # convert files into Paths
        files = [root / f for f in root_files]

        # for each file item (not dirs, they will be handled on the next iter)
        for item in files:
            # skip file if in skip_all
            if item in skip_all:
                continue

            print("fixing: ", item)

            # fix README if it is the top-level README.md
            # NB: need to do before any other stuff, requires special treatment
            if root == path_prj and item.name == S.DICT_README["RM_FILENAME"]:
                _fix_readme(item)

            # if we shouldn't skip contents
            if root not in skip_contents and item not in skip_contents:
                # fix headers
                if root not in skip_header and item not in skip_header:
                    _fix_header(item)

                # fix text
                if root not in skip_text and item not in skip_text:
                    _fix_text(item)

    # --------------------------------------------------------------------------
    # do the renaming bottom up

    # topdown=False is required for the renaming, as we don't want to rename
    # (and thus clobber) a directory name before we rename all its child
    # dirs/files
    # it should have no effect on the other fixes
    # NB: note that root is a full path, dirs and files are relative to root
    for root, root_dirs, root_files in os.walk(path_prj, topdown=False):

        # convert root into Path object
        root = Path(root)

        # skip dir if in skip_all
        if root in skip_all:
            root_dirs.clear()
            continue

        # convert files into Paths
        files = [root / f for f in root_files]

        # for each file item (not dirs, they will be handled on the next iter)
        for item in files:
            # skip file if in skip_all
            if item in skip_all:
                continue

            # fix path
            if item not in skip_path:
                _fix_path(item)

        # fix current dir path
        if root not in skip_path:
            _fix_path(root)

    # --------------------------------------------------------------------------

    # replace any dunders in blacklist before writing
    _fix_blacklist_dunders()


# ------------------------------------------------------------------------------
# Add extra dirs/files to new project after walk
# ------------------------------------------------------------------------------
def do_after_fix():
    """
    Add extra dirs/files to new project after walk

    Adds a .git (repository) dir and a .venv (virtual environment) dir to the
    project, and sets them up as necessary. These files do NOT need to be
    modified by do_fix, so we do them last.
    """

    # project directory
    path_prj = Path(DICT_SETTINGS["__PP_DIR_PRJ__"])

    # --------------------------------------------------------------------------
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
        filter_list=S.DICT_BLACKLIST["PP_SKIP_TREE"],
        dir_format=S.S_TREE_DIR_FORMAT,
        file_format=S.S_TREE_FILE_FORMAT,
    )

    # write to file
    with open(file_tree, "w", encoding="UTF-8") as a_file:
        a_file.write(tree_str)

    # --------------------------------------------------------------------------
    # git

    # add git dir
    cmd = f"git init {str(path_prj)} -q"
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array, check=False)

    # --------------------------------------------------------------------------
    # venv

    # set up venv
    cmd = f"python -m venv {str(path_prj)}/{S.S_NAME_VENV}"
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array, check=False)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Replace text in the help cmd line option and pyproject.toml file
# ------------------------------------------------------------------------------
def _fix_help_and_toml():
    """
    Replace text in the help cmd line option and pyproject.toml file

    Replaces things like the short description, version keywords, requirements,
    etc. in both the command line help and the toml file.
    """

    # --------------------------------------------------------------------------
    # load metadata

    # load from conf/metadata.json
    path_meta = S.DIR_PYPLATE / S.S_PP_DIR_CONF / S.S_PP_FILE_METADATA
    dict_meta = {}
    with open(path_meta, "r", encoding="UTF-8") as f:
        dict_meta = json.load(f)

    # --------------------------------------------------------------------------
    # set the version help string

    global S_HELP_VERSION
    S_HELP_VERSION = (
        "pyplate\n"
        +f'{ dict_meta["__PP_SHORT_DESC__"]}\n'
        + f'{dict_meta["__PP_VERSION__"]}\n'
        + S.DICT_USER["__PP_EMAIL__"]
    )

    # --------------------------------------------------------------------------
    # fix toml file

    # check if the toml file exists
    path_toml = S.DIR_PYPLATE / S.S_PP_FILE_TOML
    if not path_toml.exists():
        return

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path_toml, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # NB: we do a dunder replace here because putting a dunder as the
    # default name in the toml file causes the linter to choke, so we use a
    # dummy name

    # replace name
    str_pattern = (
        r"(^\s*\[project\]\s*$)(.*?)(^\s*name[\t ]*=[\t ]*)(.*?$)"
    )
    pp_name_small ="pyplate"
    str_rep = rf'\g<1>\g<2>\g<3>"{pp_name_small}"'
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace version
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*version[\t ]*=[\t ]*)"
        r"(.*?$)"
    )
    pp_version = dict_meta["__PP_VERSION__"]
    if pp_version == "":
        pp_version = "0.0.0"
    str_rep = rf'\g<1>\g<2>\g<3>"{pp_version}"'
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*description[\t ]*=[\t ]*)"
        r"(.*?$)"
    )
    pp_short_desc = dict_meta["__PP_SHORT_DESC__"]
    str_rep = rf'\g<1>\g<2>\g<3>"{pp_short_desc}"'
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # # replace keywords array
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*keywords[\t ]*=[\t ]*)"
        r"(.*?\])"
    )

    # convert dict to string
    pp_keywords = dict_meta["__PP_KEYWORDS__"]
    str_pp_keywords = [f'"{item}"' for item in pp_keywords]
    str_pp_keywords = ", ".join(str_pp_keywords)

    # replace string
    str_rep = rf"\g<1>\g<2>\g<3>[{str_pp_keywords}]"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace dependencies array
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*dependencies[\t ]*=[\t ]*)"
        r"(.*?\])"
    )

    # convert dict to string (only using keys)
    pp_py_deps = dict_meta["__PP_PY_DEPS__"]

    # NB: this is not conducive to a dict (we don't need links, only names)
    # so don't do what we did in README, keep it simple
    list_py_deps = [item for item in pp_py_deps.keys()]
    str_pp_py_deps = [f'"{item}"' for item in list_py_deps]
    str_pp_py_deps = ", ".join(str_pp_py_deps)

    # replace text
    str_rep = rf"\g<1>\g<2>\g<3>[{str_pp_py_deps}]"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_toml, "w", encoding="UTF8") as a_file:
        a_file.write(text)


# --------------------------------------------------------------------------
# Sets up the command line parser
# --------------------------------------------------------------------------
def _setup_parser():
    """
    Sets up the command line parser

    This method sets up the command line parser to minimize code in
    main().
    """

    # create the command line parser
    parser = argparse.ArgumentParser(
        # use the string constant for help/version and the custom formatter
        # class
        description=S_HELP_VERSION,
        formatter_class=CNFormatter,
    )

    # call the _add_args method to add args (teased out for easier code
    # maintenance)
    _add_args(parser)

    # get namespace object
    args = parser.parse_args()

    # convert namespace to dict
    return vars(args)


# --------------------------------------------------------------------------
# Add arguments to argparse parser
# --------------------------------------------------------------------------
def _add_args(parser):
    """
    Add arguments to argparse parser

    Arguments:
        parser: The parser to add arguments to

    This method is teased out for better code maintenance.
    """

    # add version option
    parser.add_argument(
        f"-{S_VER_OPTION}",
        f"--{S_VER_OPTION_LONG}",
        action=S_VER_ACTION,
        version=S_VER_VERSION,
    )

    # add debug option
    parser.add_argument(
        f"-{S_DBG_OPTION}",
        f"--{S_DBG_OPTION_LONG}",
        action=S_DBG_ACTION,
        dest=S_DBG_DEST,
        help=S_DBG_HELP,
    )

    # add update option
    parser.add_argument(
        f"-{S_UPD_OPTION}",
        f"--{S_UPD_OPTION_LONG}",
        action=S_UPD_ACTION,
        dest=S_UPD_DEST,
        help=S_UPD_HELP,
    )


# ------------------------------------------------------------------------------
# Convert items in blacklist to absolute Path objects
# ------------------------------------------------------------------------------
def _fix_blacklist_paths():
    """
    Convert items in blacklist to absolute Path objects

    Strip any path separators and get absolute paths for all entries in the
    blacklist.
    """

    # project directory
    path_prj = DICT_SETTINGS["__PP_DIR_PRJ__"]
    path_prj = Path(path_prj)

    # remove path separators
    # NB: this is mostly for glob support, as globs cannot end in path
    # separators
    for key in S.DICT_BLACKLIST:
        S.DICT_BLACKLIST[key] = [
            item.rstrip(os.sep) for item in S.DICT_BLACKLIST[key]
        ]

    # support for absolute/relative/glob
    # NB: taken from cntree.py

    # for each section of blacklist
    for key, val in S.DICT_BLACKLIST.items():
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
        S.DICT_BLACKLIST[key] = result


# ------------------------------------------------------------------------------
# Fix license/image and remove unnecessary parts of the README file
# ------------------------------------------------------------------------------
def _fix_readme(path):
    """
    Fix license/image and remove unnecessary parts of the README file

    Arguments:
        path: Path for the README to remove text

    Fixes the license/image according to the S.DICT_USER settings, and also
    removes sections of the README file that are not appropriate to the
    specified type of project, such as Module/Package or CLI/GUI.
    """

    # --------------------------------------------------------------------------

    # first fix license/image

    # default text if we can't open file
    text = ""

    # open and read file
    with open(path, "r", encoding="UTF-8") as a_file:
        text = a_file.read()

    # get replacement value
    pp_license_name = S.DICT_USER["__PP_LICENSE_NAME__"]
    pp_license_img = S.DICT_USER["__PP_LICENSE_IMG__"]
    pp_license_link = S.DICT_USER["__PP_LICENSE_LINK__"]

    # the default license value
    pp_license_full = (
        f"[![{pp_license_name}]"  # alt text
        f"({pp_license_img}"  # img src
        f' "{pp_license_link}"'  # img tooltip
        f")]({pp_license_link})"  # img link
    )

    # find the license block
    pattern_start = S.DICT_README["RM_LICENSE"]["RM_LICENSE_START"]
    pattern_end = S.DICT_README["RM_LICENSE"]["RM_LICENSE_END"]
    str_pattern = rf"({pattern_start})(.*?)({pattern_end})"

    # replace text
    str_rep = rf"\g<1>\n{pp_license_full}\n\g<3>"
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # save file
    with open(path, "w", encoding="UTF-8") as a_file:
        a_file.write(text)

    # --------------------------------------------------------------------------

    # NB: the strategy here is to go through the full README and only copy lines
    # that are:
    # 1) not in any block
    # or
    # 2) in the block we want
    # the most efficient way to do this is to have an array that receives wanted
    # lines, then return that array
    # we use a new array vs. in-situ replacement here b/c we are removing A LOT
    # OF LINES, which in-situ would result in A LOT OF BLANK LINES and while
    # that would look *ok* in the resulting Markdown, looks UGLY in the source
    # code
    # so we opt for not copying those lines.

    # just a boolean flag to say if we are kajiggering
    # if True, we are in a block we don't want to copy
    # assume False to say we want to copy
    ignore = False
    rm_delete_start = ""
    rm_delete_end = ""

    # what to ignore in the text
    # first get type of project
    type_prj = DICT_SETTINGS["__PP_TYPE_PRJ__"]
    for key, val in S.DICT_README.items():
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


# ------------------------------------------------------------------------------
# Replace dunders inside headers
# ------------------------------------------------------------------------------
def _fix_header(path):
    """
    Replace dunders inside headers

    Arguments:
        path: Path for replacing header text

    Replaces header text inside a file. Given a Path object, it iterates the
    lines one by one, replacing the value found in the form of a key in the
    DICT_SETTINGS dictionary as it goes. When it is done, it saves the new
    lines back to the file. This replaces the __PP_.. stuff inside headers.
    Using this method, we preserve any right-aligned text in each header row
    (see the header in this file for an example). Adapting this function to your
    style of header should be easy by modifying the regex pattern, and modifying
    DICT_HEADER to suit.

    NOTE: This method relies HEAVILY on the fact that the value exists, if using
    right-aligned text.

    This function will also preserve file extensions in the replaced text.

    If your files do not use any right-aligned text, then the value can be
    empty. If the value contains text which is NOT a key in DICT_SETTINGS, it
    will remain unchanged. This is mostly useful for the files in the S.DICT_COPY
    dictionary, where you want to change other header values but leave the
    filename unchanged.
    """

    # default lines
    lines = []

    # open and read file
    with open(path, "r", encoding="UTF-8") as a_file:
        lines = a_file.readlines()

    # for each line in header
    for index, line in enumerate(lines):
        # for each header key
        for item in S.LIST_HEADER:
            # look for a header key
            key = item[0]
            pattern = (
                r"("  # group 1
                r"("  # group 2
                r"\s*"  # group 2
                r"(#|<!--)"  # group 3 (comment marker)
                r"\s*"  # group 2
                r")"  # group 2
                rf"({key})"  # group 4 (key)
                r"(\s*:\s*)"  # group 5
                r")"  # group 1
                r"("  # group 6
                r"([^\.\s]*)"  # group 7 (value)
                r"([\.\S]*)"  # group 8 (file extension, if present)
                r"(\s*)"  # group 9 (padding for right-aligned text)
                r"([^\n]*)"  # group 10 (right aligned text)
                r")"  # group 6
            )

            # find first instance of header pattern
            res = re.search(pattern, line)

            # no res, keep going
            if not res:
                continue

            # value is group 7
            val = res.group(7)

            # ext (or files that start wit ha dot) is group 8
            ext = res.group(8)

            # if val is a key in DICT_SETTINGS
            if val in DICT_SETTINGS:
                # get val's val (does that make sense?)
                # so if val == '__PP_NAME_BIG__", we get the DICT_SETTINGS
                # value of the key "__PP_NAME_BIG__" regardless of the key
                # ("Project") we found
                # that way keys ("Project") aren't tied to the values
                # "__PP_NAME_BIG__"
                repl = DICT_SETTINGS[val]

            # val is not in DICT_SETTINGS
            else:
                # the text to replace should be the default dunder set in
                # LIST_HEADER
                repl = DICT_SETTINGS[item[1]]

                # if we're looking at the Filename key
                if key == "Filename":
                    # if it's blank (check also ext for files that start with a
                    # dot, like '.gitignore')
                    if len(val) == 0 and len(ext) == 0:
                        # use the filename of the file
                        repl = path.name
                    else:
                        # if it's not blank and not a dunder, it was probably
                        # set intentionally
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
            # 1. get the length of the old line (NOT always 80 since we can't
            # have trailing spaces)
            # 2. subtract 1 for newline
            # 3. subtract the other match lengths
            len_padding = len(line) - 1 - len_res
            padding = " " * len_padding

            # replace text in the line
            str_rep = rf"\g<1>{repl}\g<8>{padding}\g<10>"
            lines[index] = re.sub(pattern, str_rep, line)

    # save lines to file
    with open(path, "w", encoding="UTF-8") as a_file:
        a_file.writelines(lines)


# ------------------------------------------------------------------------------
# Replace dunders inside files
# ------------------------------------------------------------------------------
def _fix_text(path):
    """
    Replace dunders inside files

    Arguments:
        path: Path for replacing text

    Replaces text inside a file. Given a Path object, it iterates the lines
    one by one, replacing dunders as it goes. When it is done, it saves the new
    lines as the old file. This replaces the __PP_...  stuff inside the
    file, excluding headers (which are already handled).
    """

    # default lines
    lines = []

    # open and read file
    with open(path, "r", encoding="UTF-8") as a_file:
        lines = a_file.readlines()

    # for each line in array
    for index, line in enumerate(lines):
        # replace all text in line
        for key, val in DICT_SETTINGS.items():
            # find every match in line (for authors/emails in pyproject.toml)
            if key in line:
                # replace text with new value
                line = line.replace(key, val)

        # set new line with all replacements
        lines[index] = line

    # save lines to file
    with open(path, "w", encoding="UTF-8") as a_file:
        a_file.writelines(lines)


# ------------------------------------------------------------------------------
# Rename dirs/files in the project
# ------------------------------------------------------------------------------
def _fix_path(path):
    """
    Rename dirs/files in the project

    Arguments:
        path: Path for dir/file to be renamed

    Rename dirs/files. Given a path, it renames the dir/file by replacing
    dunders in the path with their appropriate replacements from
    DICT_SETTINGS.
    """

    # first get the path name (we only want to change the last component)
    last_part = path.name

    # replace dunders in last path component
    for key, val in DICT_SETTINGS.items():
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


# ------------------------------------------------------------------------------
# Replace any dunders in blacklist after writing them to the project dir
# ------------------------------------------------------------------------------
def _fix_blacklist_dunders():
    """
    Replace any dunders in blacklist after writing them to the project dir

    Check the blacklist files for any items that contain dunders, and replace
    them, since no files in the project should have dunders in the name.
    """

    # project directory as a Path object
    path_prj = DICT_SETTINGS["__PP_DIR_PRJ__"]
    path_prj = Path(path_prj)

    def _fix_file(path_to):
        # new dict
        dict_bl = {}

        # open blacklist file
        with open(path_to, "r", encoding="UTF-8") as a_file:
            # load file
            dict_bl = json.load(a_file)

            # for each dunder/replacement in settings
            for key_set, val_set in DICT_SETTINGS.items():
                # for each key of blacklist
                for key_bl in dict_bl:
                    # create a new value by replacing any dunders with their
                    # replacement values
                    dict_bl[key_bl] = [
                        item.replace(key_set, val_set)
                        for item in dict_bl[key_bl]
                    ]

        # open blacklist file
        with open(path_to, "w", encoding="UTF-8") as a_file:
            # write file
            json.dump(dict_bl, a_file, indent=4)

    # NB: the same path scheme for blacklist is used in do_before_fix
    # MAKE SURE THEY MATCH!!!
    path_blacklist = path_prj / S.S_DIR_PP / S.S_DIR_CONF / S.S_FILE_BLACKLIST
    path_blacklist_def = (
        path_prj
        / S.S_DIR_PP
        / S.S_DIR_CONF
        / S.S_DIR_CONF_DEFS
        / S.S_FILE_BLACKLIST_DEF
    )

    # replace stuff in regular file
    _fix_file(path_blacklist)

    # replace stuff in backup file
    _fix_file(path_blacklist_def)


# ------------------------------------------------------------------------------
# Check project type for allowed characters
# ------------------------------------------------------------------------------
def _check_type(type_prj):
    """
    Check project type for allowed characters

    Arguments:
        type_prj: Type to check for allowed characters

    Returns:
        Whether the type is valid to use

    Checks the passed type to see if it is one of the allowed project types.
    """

    # must have length of 1
    if len(type_prj) == 1:
        # get first char and lower case it
        char = type_prj[0]
        char = char.lower()

        # we got a valid type
        if char in S.DICT_TYPES:
            return True

    # nope, fail
    print(S.S_PRJ_TYPE_INVALID)
    return False


# ------------------------------------------------------------------------------
# Check project name for allowed characters
# ------------------------------------------------------------------------------
def _check_name(name_prj):
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
    # TIME TO FIND IT! in case you were looking for it. It will give you a quick
    # yes-no answer. I don't use it here because I want to give the user as much
    # feedback as possible, so I break down the regex into steps where each step
    # explains which part of the name is wrong.

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

    # run main function
    main()

# -)
