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
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import subprocess
import sys

# add lib path to import search
PATH_LIB = Path(__file__).parents[1] / "lib"
sys.path.append(str(PATH_LIB))

# add conf path to import search
PATH_CONF = Path(__file__).parents[1]
sys.path.append(str(PATH_CONF))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
from cnlib.cntree import CNTree  # type: ignore
from cnlib.cnpot import CNPotPy  # type: ignore
from conf import pyplateconstants as C

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=import-error
# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = True

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by pybaker.py (from misc/settings.json)
# NB: these are one-time settings created by pymaker and should not be edited
# dunders will be used for string replacement here, and checking in pybaker
# also, some entries are moved here from C.DICT_USER for convenience
# others are calculated from user entries in the cli
G_DICT_SETTINGS = {
    "__PP_AUTHOR__": C.DICT_USER["__PP_AUTHOR__"],
    "__PP_EMAIL__": C.DICT_USER["__PP_EMAIL__"],
    "__PP_LICENSE_NAME__": C.DICT_USER["__PP_LICENSE_NAME__"],
    "__PP_LICENSE_FILE__": C.DICT_USER["__PP_LICENSE_FILE__"],
    "__PP_DATE_FMT__": C.DICT_USER["__PP_DATE_FMT__"],
    "__PP_README_FILE__": C.DICT_README["RM_FILENAME"],
    "__PP_TYPE_PRJ__": "",  # 'c'
    "__PP_DIR_PRJ__": "",  # '~/Documents/Projects/Python/CLIs/PyPlate'
    "__PP_NAME_BIG__": "",  # PyPlate
    "__PP_NAME_SMALL__": "",  # pyplate
    "__PP_DATE__": "",  # 12/08/2022
}

# the output project directory as a Path object (we use this A LOT)
G_DIR_PRJ = Path("")

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

    # get info
    get_project_info()

    # copy template
    copy_template()

    # do i18n stuff
    if G_DICT_SETTINGS["__PP_TYPE_PRJ__"] in C.LIST_I18N:
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
    G_DICT_SETTINGS.
    """

    # --------------------------------------------------------------------------

    # first question is type
    # NB: keep asking until we get a response that is one of the types

    # sanity check
    type_prj = ""

    # get possible types
    list_types = [f"{key} ({val[0]})" for (key, val) in C.DICT_TYPES.items()]
    str_types = " | ".join(list_types)
    in_type = f"{C.S_PRJ_TYPE} [{str_types}]: "

    # loop forever until we get a valid type (or user presses Ctrl+C)
    while True:
        # ask for type of project
        type_prj = input(in_type)

        # check for valid type
        if _check_type(type_prj):
            # at this point, type is valid so exit loop
            break

    # save project type
    G_DICT_SETTINGS["__PP_TYPE_PRJ__"] = type_prj

    # get output subdir
    dir_type = C.DICT_TYPES[type_prj][1]

    # --------------------------------------------------------------------------

    # next question is name
    # NB: keep asking until we get a response that is a valid name and does not
    # already exist

    # sanity check
    name_prj = ""

    # loop forever until we get a valid name (or user presses Ctrl+C)
    while True:
        # ask for name of project
        name_prj = input(f"{C.S_PRJ_NAME}: ")

        # check for valid name
        if _check_name(name_prj):
            # set up for existence check
            tmp_dir = C.DIR_BASE / dir_type / name_prj

            # ------------------------------------------------------------------

            # TODO: remove after debugging all project types
            if DEBUG:
                if tmp_dir.exists():
                    shutil.rmtree(tmp_dir)

            # ------------------------------------------------------------------

            # check if project already exists
            if tmp_dir.exists():
                print(C.S_NAME_ERR.format(name_prj, dir_type))
            else:
                break

    # calculate final project location
    global G_DIR_PRJ  # pylint: disable=global-statement
    # NB: weird thing about python and globals: you can use a global dict
    # WITHOUT using the 'global' keyword, as long as you're not assigning to the
    # actual dict variable, only its contents
    # in this case though, we are assigning to a scalar value, and so must use
    # the 'global' keyword above
    G_DIR_PRJ = C.DIR_BASE / dir_type / name_prj

    # at this point, both dir and name are valid, so store both and exit
    # NB: make sure to store the project dir as a string, so it can be saved
    # to file
    G_DICT_SETTINGS["__PP_DIR_PRJ__"] = str(G_DIR_PRJ)
    G_DICT_SETTINGS["__PP_NAME_BIG__"] = name_prj

    # calculate small name
    info_name_small = name_prj.lower()
    G_DICT_SETTINGS["__PP_NAME_SMALL__"] = info_name_small

    # calculate current date (format assumed from constants above)
    # NB: this gives us a create date that we cannot get reliably from Linux
    # later this may be changed to modified date
    now = datetime.now()
    fmt_date = C.DICT_USER["__PP_DATE_FMT__"]
    info_date = now.strftime(fmt_date)
    G_DICT_SETTINGS["__PP_DATE__"] = info_date


# ------------------------------------------------------------------------------
# Copy template files to final location
# ------------------------------------------------------------------------------
def copy_template():
    """
    Copy template files to final location

    Gets dirs/files from template and copies them to the project dir.
    """

    # get input dir for common dirs/files
    dir_in = C.DIR_TEMPLATE / C.S_LOC_ALL

    # copy common stuff
    shutil.copytree(dir_in, G_DIR_PRJ)

    # get a path to the template dir for this project type
    prj_type = G_DICT_SETTINGS["__PP_TYPE_PRJ__"]
    dir_in = C.DIR_TEMPLATE / C.DICT_TYPES[prj_type][2]

    # create a package dir in project
    # NB: SOURCE DIR MUST BE NAMED 'SRC" FOR INSTALL -E TO WORK!!!
    dir_out = G_DIR_PRJ / "src"

    # copy project type stuff
    shutil.copytree(dir_in, dir_out)


# ------------------------------------------------------------------------------
# Do i18n stuff if the project is a GUI
# ------------------------------------------------------------------------------
def do_i18n():
    """
    Do i18n stuff if the project is a GUI
    """

    # FIXME: fix this
    # output dir (where the .pot and locale files will go)
    # dir_locale = Path(G_DIR_PRJ / C.S_DIR_LOCALE)

    # # create the potpy object
    # potpy = PotPy(G_DIR_PRJ, dir_locale)

    # # make a .pot file
    # potpy.make_pot(C.DICT_CLANGS)

    # # update any .po files to .mo files
    # potpy.make_mos()


# ------------------------------------------------------------------------------
# Copy/create any other files before running do_fix
# ------------------------------------------------------------------------------
def do_before_fix():
    """
    Copy/create any other files before running do_fix

    Adds dirs/files to the project before running the fix function.
    """

    # NB: we write the blacklist to ensure it is the same as what's in this file
    # before any modifications

    def _write_file(a_dict, a_file):
        with open(path_to, "w", encoding="UTF8") as a_file:
            json.dump(a_dict, a_file, indent=4)

    # write C.DICT_BLACKLIST to conf file
    path_to = G_DIR_PRJ / C.S_BLACKLIST
    _write_file(C.DICT_BLACKLIST, path_to)

    # default blacklist
    path_to = G_DIR_PRJ / C.S_BLACKLIST_DEF
    _write_file(C.DICT_BLACKLIST, path_to)

    # write C.DICT_METADATA to conf file
    path_to = G_DIR_PRJ / C.S_METADATA
    _write_file(C.DICT_METADATA, path_to)

    # default metadata
    path_to = G_DIR_PRJ / C.S_METADATA_DEF
    _write_file(C.DICT_METADATA, path_to)

    # write G_DICT_SETTINGS to conf file
    path_to = G_DIR_PRJ / C.S_SETTINGS
    _write_file(G_DICT_SETTINGS, path_to)

    # default settings
    path_to = G_DIR_PRJ / C.S_SETTINGS_DEF
    _write_file(G_DICT_SETTINGS, path_to)

    # copy linked files
    for key, val in C.DICT_COPY.items():
        # first get full source path
        path_in = C.DIR_PYPLATE / key

        # then get full dest path
        path_out = G_DIR_PRJ / val

        # copy file
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
    skip_all = C.DICT_BLACKLIST["PP_SKIP_ALL"]
    skip_contents = C.DICT_BLACKLIST["PP_SKIP_CONTENTS"]
    skip_header = C.DICT_BLACKLIST["PP_SKIP_HEADER"]
    skip_text = C.DICT_BLACKLIST["PP_SKIP_TEXT"]
    skip_path = C.DICT_BLACKLIST["PP_SKIP_PATH"]

    # walk from project dir
    # NB: topdown=False is required for the renaming, as we don't want to rename
    # (and thus clobber) a directory name before we rename all its child
    # dirs/files
    # it should have no effect on the other fixes
    # TODO: use Path instead of os
    for root, _dirs, files in os.walk(G_DIR_PRJ, topdown=False):
        # NB: note that root is a full path, dirs and files are relative to root

        # convert root into Path object
        root = Path(root)

        # skip dir if in skip_all
        if root in skip_all:
            continue

        # convert files into Paths
        files = [root / f for f in files]

        # for each file item (not dirs, they will be handled on the next iter)
        for item in files:
            # skip file if in skip_all
            if item in skip_all:
                continue

            # fix README if it is the top-level README.md
            # NB: need to do before any other stuff, requires special treatment
            if root == G_DIR_PRJ and item.name == C.DICT_README["RM_FILENAME"]:
                _fix_readme(item)

            # if we shouldn't skip contents
            if root not in skip_contents and item not in skip_contents:
                # fix headers
                if root not in skip_header and item not in skip_header:
                    _fix_header(item)

                # fix text
                if root not in skip_text and item not in skip_text:
                    _fix_text(item)

            # fix path
            if root not in skip_path and item not in skip_path:
                _fix_path(item)

        # fix current dir path
        if root not in skip_path:
            _fix_path(root)

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

    # --------------------------------------------------------------------------

    # TODO: remove after debugging all project types

    # first check if there is a tree for this type
    # if not, create it
    # then when all items are checked, do to the next type
    # once all types are fully checked, go back to creating a tree for each
    # project
    if DEBUG:
        # get tree path
        prj_type = G_DICT_SETTINGS["__PP_TYPE_PRJ__"]
        dir_tree = C.DICT_TYPES[prj_type][1]
        path_tree = C.DIR_BASE / "trees" / dir_tree / "tree.txt"

        # make tree path
        path_tree.parent.mkdir(parents=True, exist_ok=True)

        # if not exist
        if not path_tree.exists():
            # create tree object and call
            tree_obj = CNTree()
            tree_str = tree_obj.build_tree(
                str(G_DIR_PRJ),
                filter_list=C.DICT_BLACKLIST["PP_SKIP_TREE"],
                dir_format=" [] $NAME",
                file_format=" [] $NAME",
            )

            # write to file
            with open(path_tree, "w", encoding="UTF8") as a_file:
                a_file.write(tree_str)

    # --------------------------------------------------------------------------

    # get path to tree
    path_tree = G_DIR_PRJ / C.S_MISC / C.S_TREE

    # create the file so it includes itself
    with open(path_tree, "w", encoding="UTF8") as a_file:
        a_file.write("")

    # create tree object and call
    tree_obj = CNTree()
    tree_str = tree_obj.build_tree(
        str(G_DIR_PRJ),
        filter_list=C.DICT_BLACKLIST["PP_SKIP_TREE"],
        dir_format=C.S_DIR_FORMAT,
        file_format=C.S_FILE_FORMAT,
    )

    # write to file
    with open(path_tree, "w", encoding="UTF8") as a_file:
        a_file.write(tree_str)

    # add git dir
    cmd = f"git init {str(G_DIR_PRJ)} -q"
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array, check=False)

    # # set up venv
    cmd = f"python -m venv {str(G_DIR_PRJ)}/{C.S_NAME_VENV}"
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array, check=False)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Convert items in blacklist to absolute Path objects
# ------------------------------------------------------------------------------
def _fix_blacklist_paths():
    """
    Convert items in blacklist to absolute Path objects

    Strip any path separators and get absolute paths for all entries in the
    blacklist.
    """

    # remove path separators
    # NB: this is mostly for glob support, as globs cannot end in path
    # separators
    for key in C.DICT_BLACKLIST:
        C.DICT_BLACKLIST[key] = [
            item.rstrip(os.sep) for item in C.DICT_BLACKLIST[key]
        ]

    # support for absolute/relative/glob
    # NB: taken from cntree.py

    # for each section of blacklist
    for key, val in C.DICT_BLACKLIST.items():
        # convert all items in list to Path objects
        paths = [Path(item) for item in val]

        # move absolute paths to one list
        abs_paths = [item for item in paths if item.is_absolute()]

        # move relative/glob paths to another list
        other_paths = [item for item in paths if not item.is_absolute()]

        # convert relative/glob paths back to strings
        other_strings = [str(item) for item in other_paths]

        # get glob results as generators
        glob_results = [G_DIR_PRJ.glob(item) for item in other_strings]

        # start with absolutes
        result = abs_paths

        # for each generator
        for item in glob_results:
            # add results as whole shebang
            result += list(item)

        # set the list as the result list
        C.DICT_BLACKLIST[key] = result


# ------------------------------------------------------------------------------
# Fix license/image and remove unnecessary parts of the README file
# ------------------------------------------------------------------------------
def _fix_readme(path):
    """
    Fix license/image and remove unnecessary parts of the README file

    Arguments:
        path: Path for the README to remove text

    Fixes the license/image according to the C.DICT_USER settings, and also
    removes sections of the README file that are not appropriate to the
    specified type of project, such as Module/Package or CLI/GUI.
    """

    # --------------------------------------------------------------------------

    # first fix license/image

    # default text if we can't open file
    text = ""

    # open and read file
    with open(path, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # get replacement value
    pp_license_name = C.DICT_USER["__PP_LICENSE_NAME__"]
    pp_license_img = C.DICT_USER["__PP_LICENSE_IMG__"]
    pp_license_link = C.DICT_USER["__PP_LICENSE_LINK__"]

    # the default license value
    pp_license_full = (
        f"[![{pp_license_name}]"  # alt text
        f"({pp_license_img}"  # img src
        f' "{pp_license_link}"'  # img tooltip
        f")]({pp_license_link})"  # img link
    )

    # find the license block
    pattern_start = C.DICT_README["RM_LICENSE"]["RM_LICENSE_START"]
    pattern_end = C.DICT_README["RM_LICENSE"]["RM_LICENSE_END"]
    str_pattern = rf"({pattern_start})(.*?)({pattern_end})"

    # replace text
    str_rep = rf"\g<1>\n{pp_license_full}\n\g<3>"
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # save file
    with open(path, "w", encoding="UTF8") as a_file:
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
    type_prj = G_DICT_SETTINGS["__PP_TYPE_PRJ__"]
    for key, val in C.DICT_README.items():
        if type_prj == key:
            # get values for keys
            rm_delete_start = val["RM_DELETE_START"]
            rm_delete_end = val["RM_DELETE_END"]
            break

    # where to put the needed lines
    new_lines = []

    # open and read file
    with open(path, "r", encoding="UTF8") as a_file:
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
    with open(path, "w", encoding="UTF8") as a_file:
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
    G_DICT_SETTINGS dictionary as it goes. When it is done, it saves the new
    lines back to the file. This replaces the __PP_.. stuff inside headers.
    Using this method, we preserve any right-aligned text in each header row
    (see the header in this file for an example). Adapting this function to your
    style of header should be easy by modifying the regex pattern, and modifying
    DICT_HEADER to suit.

    NOTE: This method relies HEAVILY on the fact that the value exists, if using
    right-aligned text.

    This function will also preserve file extensions in the replaced text.

    If your files do not use any right-aligned text, then the value can be
    empty. If the value contains text which is NOT a key in G_DICT_SETTINGS, it
    will remain unchanged. This is mostly useful for the files in the C.DICT_COPY
    dictionary, where you want to change other header values but leave the
    filename unchanged.
    """

    # default lines
    lines = []

    # open and read file
    with open(path, "r", encoding="UTF8") as a_file:
        lines = a_file.readlines()

    # for each line in header
    for index, line in enumerate(lines):
        # for each header key
        for item in C.LIST_HEADER:
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

            # if val is a key in G_DICT_SETTINGS
            if val in G_DICT_SETTINGS:
                # get val's val (does that make sense?)
                # so if val == '__PP_NAME_BIG__", we get the G_DICT_SETTINGS
                # value of the key "__PP_NAME_BIG__" regardless of the key
                # ("Project") we found
                # that way keys ("Project") aren't tied to the values
                # "__PP_NAME_BIG__"
                repl = G_DICT_SETTINGS[val]

            # val is not in G_DICT_SETTINGS
            else:
                # the text to replace should be the default dunder set in
                # LIST_HEADER
                repl = G_DICT_SETTINGS[item[1]]

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
    with open(path, "w", encoding="UTF8") as a_file:
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
    with open(path, "r", encoding="UTF8") as a_file:
        lines = a_file.readlines()

    # for each line in array
    for index, line in enumerate(lines):
        # replace all text in line
        for key, val in G_DICT_SETTINGS.items():
            # find every match in line (for authors/emails in pyproject.toml)
            if key in line:
                # replace text with new value
                line = line.replace(key, val)

        # set new line with all replacements
        lines[index] = line

    # save lines to file
    with open(path, "w", encoding="UTF8") as a_file:
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
    G_DICT_SETTINGS.
    """

    # first get the path name (we only want to change the last component)
    last_part = path.name

    # replace dunders in last path component
    for key, val in G_DICT_SETTINGS.items():
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
# Replace any dunders in blacklist after writing them to the project folder
# ------------------------------------------------------------------------------
def _fix_blacklist_dunders():
    """
    Replace any dunders in blacklist after writing them to the project folder

    Check the blacklist files for any items that contain dunders, and replace
    them, since no files in the project should have dunders in the name.
    """

    def _fix_file(path_to):
        # new dict
        dict_bl = {}

        # open blacklist file
        with open(path_to, "r", encoding="UTF8") as a_file:
            # load file
            dict_bl = json.load(a_file)

            # for each dunder/replacement in settings
            for key_set, val_set in G_DICT_SETTINGS.items():
                # for each key of blacklist
                for key_bl in dict_bl:
                    # create a new value by replacing any dunders with their
                    # replacement values
                    dict_bl[key_bl] = [
                        item.replace(key_set, val_set)
                        for item in dict_bl[key_bl]
                    ]

        # open blacklist file
        with open(path_to, "w", encoding="UTF8") as a_file:
            # write file
            json.dump(dict_bl, a_file, indent=4)

    # replace stuff in regular file
    path_to = G_DIR_PRJ / C.S_BLACKLIST
    _fix_file(path_to)

    # replace stuff in backup file
    path_to = G_DIR_PRJ / C.S_BLACKLIST_DEF
    _fix_file(path_to)


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
        if char in C.DICT_TYPES:
            return True

    # nope, fail
    print(C.S_PRJ_TYPE_INVALID)
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
        print(C.S_PRJ_NAME_LEN)
        return False

    # match start or return false
    pattern = r"(^[a-zA-Z])"
    res = re.search(pattern, name_prj)
    if not res:
        print(C.S_PRJ_NAME_START)
        return False

    # match end or return false
    pattern = r"([a-zA-Z\d]$)"
    res = re.search(pattern, name_prj)
    if not res:
        print(C.S_PRJ_NAME_END)
        return False

    # match middle or return false
    pattern = r"(^[a-zA-Z\d\-_]*$)"
    res = re.search(pattern, name_prj)
    if not res:
        print(C.S_PRJ_NAME_CONTAIN)
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
