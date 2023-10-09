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
destination, and performs some initial fixes/replacements of text and path names
in the resulting files.
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

# local imports
from cntree import CNTree

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = True

# some useful constants
_DIR_SELF = Path(__file__).parent  # /some/dir/pyplate

# this is the dir above where the script is being run from (e.g.
# ~/Documents/Projects/Python/PyPlate/)
_DIR_PYPLATE = _DIR_SELF.parent

# this is the dir where the template files are located relative to this script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
_DIR_TEMPLATE = _DIR_PYPLATE / "template"

# this is the location where the project's subdir will be (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
_DIR_BASE = _DIR_PYPLATE.parent

# the dict of user info to be replaced in the headers and text of a new project
# they are placed here to be easily modified by subsequent users
# they are then copied to G_DICT_SETTINGS to be used here and copied to the
# project dir for use by pybaker.py
DICT_USER = {
    # the author name, used in headers and pyproject.toml
    "__PP_AUTHOR__": "cyclopticnerve",
    # the author's email, used in headers and pyproject.toml
    "__PP_EMAIL__": "cyclopticnerve@gmail.com",
    # the license name, used in headers, README.md, and pyproject.toml
    "__PP_LICENSE_NAME__": "WTFPLv2",
    # the license image source, used in README.md
    "__PP_LICENSE_IMG__": "https://img.shields.io/badge/License-WTFPL-brightgreen.svg",
    # the url for license image click
    "__PP_LICENSE_LINK__": "http://www.wtfpl.net",
    # the screenshot to use in the README
    "__PP_SCREENSHOT__": "",
    # NB: the struggle here is that using the fixed format results in a
    # four-digit year, but using the locale format ('%x') results in a two-digit
    # year (at least for my locale, which in 'en_US').
    # so what to do? what i really want is a locale format that uses four-digit
    # years everywhere. so i am faced with a 'cake and eat it too' situation.
    # not sure how to proceed but i think for now i will leave this as a
    # user-editable string and place it in the realm of 'edit it before you run'
    # along with author/email/license/etc
    "__PP_DATE_FMT__": "%m/%d/%Y",
}

# the types of projects this script can create
# key is the short type name (used for entry)
# val[0] is the long type name (used for display)
# val[1] is the subdir name under _DIR_BASE where the project will be created
# val[2] is the dir(s) under 'template' to get the files
# order is arbitrary, just decided to make it alphabetical
DICT_TYPES = {
    "c": ["CLI", "CLIs", "cli"],
    "g": ["GUI", "GUIs", "gui"],
    "p": ["Package", "Packages", "pkg"],
}

# the list of keys to replace in the header of each file
# these values are used to find matching lines in the file that are assumed to
# be header lines, if they match the pattern used in _fix_header()
# the file header line should contain lines that match the pattern:
# '# <Key>: <val> ...'
# or
# '<!-- <key>:<val> ...'
# where <key> is one of the items here, and <val> is one of the keys from
# G_DICT_SETTINGS
# if <key> does not match one of these items or <val> does not match one of the
# keys from G_DICT_SETTINGS, it is left untouched
# see the source of template/all/README.md for an example
# an example header:
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__.py                                  |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------
# spaces don't matter, but the colon does. also, right aligned text at the end
# of each line will be preserved.
LIST_HEADER = [
    "Project",  # PyPlate
    "Filename",  # pyplate.py
    "Date",  # 12/08/2022
    "Author",  # cyclopticnerve
    "License",  # WTFPLv2
]

# the dict of sections to remove in the README file
# key is the project type we are making (may contain multiple project types)
# or a special section of the readme
# rm_delete_start is the tag at the start of the section to remove
# rm_delete_end is the tag at the end of the section to remove
# NB: these tags start with 'RM' instead of 'PP' because most 'PP' keys will
# remain in the file, and we don't want pybaker to report their presence as an
# error
# this way you can have different sections in the readme for things like
# installation instructions, depending on whether your project is a python
# package or a cli/gui app
DICT_README = {
    "license": {
        "RM_LICENSE_START": "<!-- __RM_LICENSE_START__ -->",
        "RM_LICENSE_END": "<!-- __RM_LICENSE_END__ -->",
    },
    "cg": {
        "RM_DELETE_START": "<!-- __RM_PKG_START__ -->",
        "RM_DELETE_END": "<!-- __RM_PKG_END__ -->",
    },
    "p": {
        "RM_DELETE_START": "<!-- __RM_APP_START__ -->",
        "RM_DELETE_END": "<!-- __RM_APP_END__ -->",
    },
}

# this is the set of dirs/files we don't mess with in the final project
# each item can be a full path , relative to the project directory, or glob
# NB: you can use dunders here since the path is the last thing to get fixed
# these dir/file names should match what's in the template dir (before any
# modifications, hence using dunder keys)
DICT_BLACKLIST = {
    # skip header, skip text, skip path (0 0 0)
    # NB: this is mostly to speed up processing by not even looking at them
    "PP_SKIP_ALL": [
        ".git",
        ".venv",
        ".vscode",
        "docs",
        "misc",
        "README",
        "tests",
        "locale",
        "CHANGELOG.md",
        "LICENSE.txt",
        "requirements.txt",
        "**/__pycache__",
    ],
    # skip header, skip text, fix path (0 0 1)
    # NB: this is used mostly for non-text files
    "PP_SKIP_CONTENTS": [
        "__PP_NAME_SMALL__.png",
    ],
    # skip header, fix text, fix path (0 1 1)
    # NB: not sure what this is useful for, but here it is
    "PP_SKIP_HEADER": [],
    # fix header, skip text, fix path (1 0 1)
    # NB: mostly used for files that contain dunders that will be replaced later
    # or files we only want to replace headers in
    "PP_SKIP_TEXT": [
        "conf",
        "MANIFEST.in",
        "**/.gitignore",
    ],
    # fix header, fix text, skip path (1 1 0)
    # not really useful, since we always want to fix paths with dunders
    "PP_SKIP_PATH": [],
}

# the metadata that the final project will use for pybaker.py
# NB: all of these values will need to be set later before running pybaker.py
DICT_METADATA = {
    # the version number to use in README.md and pyproject.toml
    "__PP_VERSION__": "",
    # the short description to use in README.md and pyproject.toml
    "__PP_SHORT_DESC__": "",
    # the keywords to use in pyproject.toml and github
    "__PP_KEYWORDS__": [],
    # the python dependencies to use in README.md, pyproject.toml, github, and
    # install.py
    "__PP_PY_DEPS__": {},
    # the system dependencies to use in README.md, github.com, and install.py
    "__PP_SYS_DEPS__": [],
    # the categories to use in .desktop for gui apps
    "__PP_GUI_CATEGORIES__": [],
}

# dict of files that should be copied from the PyPlate project to the resulting
# project (outside of the template dir)
# this is so that when you update a file in the PyPlate project, it gets copied
# to the project, and cuts down on duplicate files
# key is the relative path to the source file in PyPlate
# val is the relative path to the dest file in the project dir
DICT_LINKS = {
    ".gitignore": ".gitignore",
    "misc/checklist.txt": "misc/checklist.txt",
    "misc/snippets.txt": "misc/snippets.txt",
    "misc/style.txt": "misc/style.txt",
    "pyplate/pybaker.py": "conf/pybaker.py",
    "pyplate/cntree.py": "conf/cntree.py",
}

# list of dirs/files to ignore in output dir when creating the initial tree
# each item can be a partial path relative to the project directory, or a glob
# see https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob
LIST_TREE_IGNORE = [
    ".git",
    ".venv",
    ".vscode",
    ".VSCodeCounter",
    "**/__pycache__",
]

# in case we decide to switch to, eg., .rst or LaTeX
# NB: this file will only be fixed if it is in the top-level dir of the project
README_NAME = "README.md"

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by pybaker.py (from misc/settings.json)
# NB: these are one-time settings created by pymaker and should not be edited
# dunders will be used for string replacement here, and checking in pybaker
# also, some entries are moved here from DICT_USER for convenience
# others are calculated from user entries in the cli
G_DICT_SETTINGS = {
    "__PP_AUTHOR__": DICT_USER["__PP_AUTHOR__"],
    "__PP_EMAIL__": DICT_USER["__PP_EMAIL__"],
    "__PP_LICENSE_NAME__": DICT_USER["__PP_LICENSE_NAME__"],
    "__PP_DATE_FMT__": DICT_USER["__PP_DATE_FMT__"],
    "__PP_TYPE_PRJ__": "",  # 'c'
    "__PP_DIR_PRJ__": "",  # '~/Documents/Projects/Python/CLIs/PyPlate'
    "__PP_NAME_BIG__": "",  # PyPlate
    "__PP_NAME_SMALL__": "",  # pyplate
    "__PP_DATE__": "",  # 12/08/2022
    "__PP_TREE_IGNORE__": LIST_TREE_IGNORE,
}

# the output project directory as a Path object (we use this A LOT)
G_DIR_PRJ = Path('')

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

G_STRINGS = {
    "S_PRJ_TYPE": "Project type",
    "S_PRJ_NAME": "Project name",
    "S_NAME_ERR": "Project \"{}\" already exists in \"{}\"",
    "S_DIR_FORMAT": " [] $NAME/",
    "S_FILE_FORMAT": " [] $NAME",
    "S_PRJ_LEN": "Project names must be more than 1 character",
    "S_PRJ_START": "Project names must start with a letter",
    "S_PRJ_END": "Project names must end with a letter or number",
    "S_PRJ_CONTAIN": (
        "Project names must contain only letters, numbers,"
        "dashes (-), or underscores (_)"
    ),
}

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

    # ---------------------------------------------------------------

    # first question is type
    # NB: keep asking until we get a response that is one of the types

    # sanity check
    type_prj = ""

    # get possible types
    list_types = [f"{key} ({val[0]})" for (key, val) in DICT_TYPES.items()]
    str_types = " | ".join(list_types)
    in_type = f"{G_STRINGS['S_PRJ_TYPE']} [{str_types}]: "

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
    dir_type = DICT_TYPES[type_prj][1]

    # ---------------------------------------------------------------

    # next question is name
    # NB: keep asking until we get a response that is a valid name and does not
    # already exist

    # sanity check
    name_prj = ""

    # loop forever until we get a valid name (or user presses Ctrl+C)
    while True:
        # ask for name of project
        name_prj = input(f"{G_STRINGS['S_PRJ_NAME']}: ")

        # check for valid name
        if _check_name(name_prj):
            # set up for existence check
            tmp_dir = _DIR_BASE / dir_type / name_prj

            # ------------------------------------------------------------------

            # TODO: remove after debugging all project types
            if DEBUG:
                if tmp_dir.exists():
                    shutil.rmtree(tmp_dir)

            # ------------------------------------------------------------------

            # check if project already exists
            if tmp_dir.exists():
                print(G_STRINGS['S_NAME_ERR'].format(name_prj, dir_type))
            else:
                break

    # calculate final project location
    global G_DIR_PRJ
    # NB: weird thing about python and globals: you can use a global dict
    # WITHOUT using the 'global' keyword, as long as you're not assigning to the
    # actual dict variable, only its contents
    # in this case though, we are assigning to a scalar value, and so must use
    # the 'global' keyword above
    G_DIR_PRJ = _DIR_BASE / dir_type / name_prj

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
    fmt_date = DICT_USER["__PP_DATE_FMT__"]
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
    dir_in = _DIR_TEMPLATE / "all"

    # copy common stuff
    shutil.copytree(dir_in, G_DIR_PRJ)

    # get a path to the template dir for this project type
    prj_type = G_DICT_SETTINGS["__PP_TYPE_PRJ__"]
    dir_in = _DIR_TEMPLATE / DICT_TYPES[prj_type][2]

    # create a package dir in project
    dir_out = G_DIR_PRJ / G_DICT_SETTINGS["__PP_NAME_SMALL__"]

    # copy project type stuff
    shutil.copytree(dir_in, dir_out)


# ------------------------------------------------------------------------------
# Copy/create any other files before running do_fix
# ------------------------------------------------------------------------------
def do_before_fix():
    """
    Copy/create any other files before running do_fix

    Adds dirs/files to the project before running the fix function.
    """

    # write DICT_BLACKLIST to conf file
    path_to = G_DIR_PRJ / "conf" / "blacklist.json"
    with open(path_to, "w", encoding="UTF8") as a_file:
        dict_blacklist = json.dumps(DICT_BLACKLIST, indent=4)
        a_file.write(dict_blacklist)

    # write DICT_METADATA to conf file
    path_to = G_DIR_PRJ / "conf" / "metadata.json"
    with open(path_to, "w", encoding="UTF8") as a_file:
        dict_metadata = json.dumps(DICT_METADATA, indent=4)
        a_file.write(dict_metadata)

    # write G_DICT_SETTINGS to conf file
    path_to = G_DIR_PRJ / "conf" / "settings.json"
    with open(path_to, "w", encoding="UTF8") as a_file:
        dict_settings = json.dumps(G_DICT_SETTINGS, indent=4)
        a_file.write(dict_settings)

    # copy linked files
    for key, val in DICT_LINKS.items():
        # first get full source path
        path_in = _DIR_PYPLATE / key

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

    # fix uo the blacklist and convert to absolute Path objects
    _fix_blacklist()

    # just shorten the names
    skip_all = DICT_BLACKLIST["PP_SKIP_ALL"]
    skip_contents = DICT_BLACKLIST["PP_SKIP_CONTENTS"]
    skip_header = DICT_BLACKLIST["PP_SKIP_HEADER"]
    skip_text = DICT_BLACKLIST["PP_SKIP_TEXT"]
    skip_path = DICT_BLACKLIST["PP_SKIP_PATH"]

    # walk from project dir
    # NB: topdown=False is required for the renaming, as we don't want to rename
    # (and thus clobber) a directory name before we rename all its child
    # dirs/files
    # it should have no effect on the other fixes
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
            if root == G_DIR_PRJ and item.name == README_NAME:
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


# ------------------------------------------------------------------------------
# Add extra dirs/files to new project after walk
# ------------------------------------------------------------------------------
def do_after_fix():
    """
    Add extra dirs/files to new project after walk

    Adds a .git (repository) dir and a .venv (virtual environment) dir to
    the project, and sets them up as necessary. These files do NOT need to
    be modified by do_fix, so we do them last.
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
        dir_tree = DICT_TYPES[prj_type][1]
        path_tree = _DIR_BASE / "trees" / dir_tree / "tree.txt"

        # make tree path
        path_tree.parent.mkdir(parents=True, exist_ok=True)

        # if not exist
        if not path_tree.exists():
            # create tree object and call
            tree_obj = CNTree()
            tree_str = tree_obj.build_tree(
                str(G_DIR_PRJ),
                filter_list=LIST_TREE_IGNORE,
                dir_format=G_STRINGS['S_DIR_FORMAT'],
                file_format=G_STRINGS['S_FILE_FORMAT'],
            )

            # write to file
            with open(path_tree, "w", encoding="UTF8") as a_file:
                a_file.write(tree_str)

    # --------------------------------------------------------------------------

    # get path to tree
    path_tree = G_DIR_PRJ / "misc" / "tree.txt"

    # create tree object and call
    tree_obj = CNTree()
    tree_str = tree_obj.build_tree(
        str(G_DIR_PRJ),
        filter_list=LIST_TREE_IGNORE,
        dir_format=G_STRINGS['S_DIR_FORMAT'],
        file_format=G_STRINGS['S_FILE_FORMAT'],
    )

    # write to file
    with open(path_tree, "w", encoding="UTF8") as a_file:
        a_file.write(tree_str)

    # add git dir
    cmd = f"git init {str(G_DIR_PRJ)} -q"
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array, check=False)

    # # set up venv
    cmd = f"python -m venv {str(G_DIR_PRJ)}/.venv"
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array, check=False)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Clean up the blacklist and get absolute paths as Path objects
# ------------------------------------------------------------------------------
def _fix_blacklist():
    """
    Clean up the blacklist and convert entries to Path objects

    Strip any path separators and get absolute paths for all entries in the
    blacklist.
    """

    # remove path separators
    # NB: this is mostly for glob support, as globs cannot end in path
    # separators
    for key in DICT_BLACKLIST:
        DICT_BLACKLIST[key] = [
            item.rstrip(os.sep) for item in DICT_BLACKLIST[key]
        ]

    # support for absolute/relative/glob
    # NB: taken from cntree.py

    # for each section of blacklist
    for key, val in DICT_BLACKLIST.items():
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
        DICT_BLACKLIST[key] = result


# ------------------------------------------------------------------------------
# Fix license/image and remove unnecessary parts of the README file
# ------------------------------------------------------------------------------
def _fix_readme(path):
    """
    Fix license/image and remove unnecessary parts of the README file

    Arguments:
        path: Path for the README to remove text

    Fixes the license/image according to the DICT_USER settings, and also
    removes sections of the README file that are not appropriate to the
    specified type of project, such as Module/Package or CLI/GUI.
    """

    # --------------------------------------------------------------------------

    # first fix license/image done in the style of pybaker, using regex/context

    # default text if we can't open file
    text = ""

    # open and read file
    with open(path, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # get replacement value
    pp_license_name = DICT_USER["__PP_LICENSE_NAME__"]
    pp_license_img = DICT_USER["__PP_LICENSE_IMG__"]
    pp_license_link = DICT_USER["__PP_LICENSE_LINK__"]

    # the default license value
    pp_license_full = (
        f"[![{pp_license_name}]"  # alt text
        f"({pp_license_img}"  # img src
        f' "{pp_license_link}"'  # img tooltip
        f")]({pp_license_link})"  # img link
    )

    # find the license block
    pattern_start = DICT_README["license"]["RM_LICENSE_START"]
    pattern_end = DICT_README["license"]["RM_LICENSE_END"]
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

    # what to ignore in the text
    # first get type of project
    type_prj = G_DICT_SETTINGS["__PP_TYPE_PRJ__"]
    for key, val in DICT_README.items():
        if type_prj in key:
            # get values for keys
            rm_delete_start = val["RM_DELETE_START"]
            rm_delete_end = val["RM_DELETE_END"]
            break

    # where to put the needed lines
    new_lines = []
    rm_delete_start = ''
    rm_delete_end = ''

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
    lines one by one, replacing header text as it goes. When it is done, it
    saves the new lines as the old file. This replaces the __PP_.. stuff inside
    headers. Using this method, we preserve any right-aligned text in each
    header row (See the header in this file for an example). Adapting this
    function to your style of header should be easy using the regex pattern, and
    modifying DICT_HEADER to suit.
    NOTE: This method relies HEAVILY on the fact that the value exists, and that
    there is AT LEAST one space before and after the value, to work.
    Example (Dashes show required spaces):
    # --------------------------------------------------------------------------
    # Project:-__PP_NAME_BIG__-...
    # --------------------------------------------------------------------------
    This function will also preserve file extensions:
    # --------------------------------------------------------------------------
    # Filename:-__PP_NAME_SMALL__.py-...
    # --------------------------------------------------------------------------
    If your files do not use any right-aligned text, then the value can be empty
    and the space after the value is not necessary.
    """

    # default lines
    lines = []

    # open and read file
    with open(path, "r", encoding="UTF8") as a_file:
        lines = a_file.readlines()

    # for each line in header
    for index, line in enumerate(lines):
        # for each header key
        for item in LIST_HEADER:
            # look for a header key
            pattern = (
                r"(\s*[#|<!--]\s*)"  # group 1: opening comment char(s)
                rf"({item})"  # group 2:key from LIST_HEADER
                r"f(\s*:\s+)"  # group 3:spaces, colon and spaces (at least 1)
                r"([^\s\.]*)"  # group 4: all not spaces and not dot (dunder)
                r"(\S*)"  # group 5: all not spaces (file ext)
                r"(\s*)"  # group 6: all spaces (padding)
                r"(.*)"  # group 7: all other chars (right-aligned text)
            )

            # find first instance of header key
            res = re.search(pattern, line)

            # no res, keep going
            if not res:
                continue

            # value is group 4
            val = res.group(4)

            # try to find key in dict_values
            # if no value or not in G_DICT_SETTINGS, leave it alone and keep
            # going
            if len(val) == 0 or val not in G_DICT_SETTINGS:
                continue

            # get the value by backtracking into G_DICT_SETTINGS
            val = G_DICT_SETTINGS[val]

            # count what we will need without spaces
            len_res = (
                len(res.group(1))
                + len(res.group(2))
                + len(res.group(3))
                + len(val)  # group 4 is val
                + len(res.group(5))
                # group 6 will be str_spaces
                + len(res.group(7))
            )

            # make spaces
            # NB: this looks funky but it works:
            # 1. get the length of the old line (NOT always 80 since we can't
            # have trailing spaces)
            # 2. subtract 1 for newline
            # 3. subtract the other match lengths
            len_spaces = len(line) - 1 - len_res
            str_spaces = " " * len_spaces

            # replace text in the line
            str_rep = rf"\g<1>\g<2>\g<3>{val}\g<5>{str_spaces}\g<7>"
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
        # replace text in line
        for key, val in G_DICT_SETTINGS.items():
            if isinstance(val, str) and key in line:
                # replace text with new value
                lines[index] = line.replace(key, val)

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
        # G_DICT_SETTINGS may contain other info, only use strings
        if isinstance(val, str):
            last_part = last_part.replace(key, val)

    # replace the name
    path_new = path.parent / last_part

    # if it hasn't changed, skip to avoid overhead
    if path_new == path:
        return

    # do rename
    path.rename(path_new)


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
        if char in DICT_TYPES:
            return True

    # nope, fail
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
        print(G_STRINGS['S_PRJ_LEN)'])
        return False

    # match start or return false
    pattern = r"(^[a-zA-Z])"
    res = re.search(pattern, name_prj)
    if not res:
        print(G_STRINGS['S_PRJ_START'])
        return False

    # match end or return false
    pattern = r"([a-zA-Z\d]$)"
    res = re.search(pattern, name_prj)
    if not res:
        print(G_STRINGS['S_PRJ_END'])
        return False

    # match middle or return false
    pattern = r"(^[a-zA-Z\d\-_]*$)"
    res = re.search(pattern, name_prj)
    if not res:
        print(G_STRINGS['S_PRJ_CONTAIN'])
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
