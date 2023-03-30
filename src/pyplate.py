#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pyplate.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
import json
import os
import re
import shlex
import shutil
import subprocess

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# this is the dir where the script is being run from
# (e.g. ~/Documents/Projects/Python/PyPlate/src/)
path = os.path.abspath(__file__)
DIR_CURR = os.path.dirname(path)

# this is the dir where the template files are located rel to the script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
path = os.path.join(DIR_CURR, '..', 'template')
DIR_TEMPLATE = os.path.abspath(path)

# this is the dir for project location (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
path = os.path.join(DIR_CURR, '..', '..')
DIR_PRJ_BASE = os.path.abspath(path)

# this is the current user home dir
# (e.g. /home/cyclopticnerve/)
DIR_USER = os.path.expanduser('~')

# date format
PRJ_DATE = '%m/%d/%Y'

# files to include in project
# paths are relative to DIR_TEMPLATE
DICT_FILES = {
    'common': [                 # common to all projects
        'docs',
        'misc',
        'tests',
        '.gitignore',
        'LICENSE.txt',
        'README.md',
        'requirements.txt',
    ],
    'm': [                      # for module projects
        'src/__PP_NAME_SMALL__.mod.py',
        'MANIFEST.in',
        'pyproject.toml',
    ],
    'p': [                      # for package projects
        'src/__PP_NAME_SMALL__',
        'MANIFEST.in',
        'pyproject.toml',
    ],
    'c': [                      # for cli projects
        'src/__PP_NAME_SMALL__.app.py',
        'install.py',
        'uninstall.py',
    ],
    'g': [                      # for gui projects
        'gui',
        'src/__PP_NAME_SMALL__.app.py',
        'install.py',
        'uninstall.py',
    ],
}

# the array of header strings to match for replacement
LIST_HEADER = [
    ['Project',  '__PP_NAME_BIG__'],
    ['Filename', '__PP_NAME_SMALL__'],
    ['Date',     '__PP_DATE__'],
]

# the dict of README sections/tags to remove
DICT_README = {
    'mp': {
        'delete_start': '<!-- __PP_APP_START__ -->',
        'delete_end':   '<!-- __PP_APP_END__ -->',
        'delete_tag':   '<!-- __PP_MOD_',
    },
    'cg': {
        'delete_start': '<!-- __PP_MOD_START__ -->',
        'delete_end':   '<!-- __PP_MOD_END__ -->',
        'delete_tag':   '<!-- __PP_APP_',
    },
}

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by metadata.py (from misc/settings.json)

# 'project' and 'info' are set using get_project_info()
# 'metadata' will be edited by the user through 'misc/settings.json'

# the following caveats apply to 'metadata':

# PP_VERSION = '0.1.0'
# this is the canonical (only and absolute) version number string for this
# project
# this should provide the absolute version number string (in semantic notation)
# of this project, and all other version numbers should be superceded by this
# string
# format is N.N.N

# PP_SHORT_DESC = ''
# PP_KEYWORDS = ''
# PP_SYS_DEPS = ''
# PP_PY_DEPS = ''
# these are the short description, keywords, and dependencies for the project
# they are stored here for projects that don't use pyproject.toml
# these will be used in the GitHub repo and README.md
# delimiters for PP_KEYWORDS and PP_XXX_DEPS MUST be comma

# PP_GUI_CATEGORIES = ''
# gui categories MUST be seperated by semicolon and MUST end with semicolon,
# athough the final ';' will be added if necessary
# this is mostly for desktops that use a windows-stylew menu/submenu, not for
# Ubuntu-style overviews

# PP_GUI_EXEC = ''
# PP_GUI_ICON = ''
# if exec/icon paths are not absolute, they will be found in standard paths
# these paths vary, but I will add them here in the comments when I figure them
# out

dict_settings = {
    'project': {
        'type': '',                # m (Module), p (Package), c (CLI), g (GUI)
        'path': '',                # path to project (DIR_PRJ_BASE/type_dir/Foo)
    },
    'info': {
        '__PP_NAME_BIG__':   '',   # Foo
        '__PP_NAME_SMALL__': '',   # foo
        '__PP_DATE__':       '',   # 12/08/2022
    },
    'metadata': {
        'PP_VERSION':        '0.1.0',  # N.N.N
        'PP_SHORT_DESC':     '',       # short description
        'PP_KEYWORDS':       '',       # Python,app,to,do,something
        'PP_PY_DEPS':        '',       # numpy,pylint,tomli
        'PP_SYS_DEPS':       '',       # python3.10,imagemagick
        'PP_GUI_CATEGORIES': '',       # Programs;Python;Utilities;
        # DIR_USR/.cyclopticnerve/__PP_NAME_BIG__/gui/__PP_NAME_SMALL__-gtk.py
        'PP_GUI_EXEC':       '',
        # DIR_USR/.cyclopticnerve/__PP_NAME_BIG__/gui/__PP_NAME_SMALL__.png
        'PP_GUI_ICON':       '',
    }
}


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Main function
# ------------------------------------------------------------------------------
def main():
    """
        Main function

        This is the main function, which calls each step in the process of
        creating a project.
    """

    # call each step to create project
    get_project_info()
    copy_template()
    add_extras()

    # call recurse to do replacements in final project location
    path = dict_settings['project']['path']
    recurse(path)


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_project_info():
    """
        Get project info

        Asks the user for project info, such as type and name.
    """

    # the settings dict (global b/c we will modify here)
    global dict_settings

    # loop forever until we get a valid type
    while True:

        # ask what type of project
        prj_type = input(
            'Project type: [m]odule | [p]ackage | [c]li | [g]ui: '
        )

        # check project type
        pattern = r'(^(m|p|c|g{1})$)'
        res = re.search(pattern, prj_type, re.I)
        if res:

            # we got a valid type
            prj_type = prj_type.lower()
            dict_settings['project']['type'] = prj_type
            break

    # configure subdir
    type_dir = ''
    if prj_type in 'mp':
        type_dir = 'Libs'
    else:
        type_dir = 'Apps'

    # loop forever until we get a valid name and path
    while True:

        # ask for project name
        prj_name_big = input('Project name: ')

        # check for valid name
        if not _validate_name(prj_name_big):
            continue

        # calculate final proj location
        prj_path = os.path.join(DIR_PRJ_BASE, type_dir, prj_name_big)

        # check if project already exists
        if os.path.exists(prj_path):
            print(f'Project {prj_path} already exists')
            continue

        # if name is valid, move on
        dict_settings['info']['__PP_NAME_BIG__'] = prj_name_big
        dict_settings['project']['path'] = prj_path
        break

    # calculate small name
    prj_name_small = prj_name_big.lower()
    dict_settings['info']['__PP_NAME_SMALL__'] = prj_name_small

    # calculate current date
    prj_date = datetime.now().strftime(PRJ_DATE)
    dict_settings['info']['__PP_DATE__'] = prj_date


# ------------------------------------------------------------------------------
# Copy template files to final location
# ------------------------------------------------------------------------------
def copy_template():
    """
        Copy template files to final location

        Get file paths/names from dict_settings and copy them to the project
        folder.
    """

    # create target folder
    prj_path = dict_settings['project']['path']
    os.makedirs(prj_path)

    # get project type
    proj_type = dict_settings['project']['type']

    # the group of files, common and type
    groups = [
        DICT_FILES['common'],
        DICT_FILES[proj_type]
    ]

    # for each group, common and type
    items = [item for group in groups for item in group]
    for item in items:

        # build old path/new path
        path_old = os.path.join(DIR_TEMPLATE, item)
        path_new = os.path.join(prj_path, item)

        # if it's a dir, copy dir
        if os.path.isdir(path_old):
            shutil.copytree(path_old, path_new)
        else:

            # if it's a file, get the file's dir and create
            dir_new = os.path.dirname(path_new)
            os.makedirs(dir_new, exist_ok=True)

            # then copy file
            shutil.copy2(path_old, path_new)

    # write dict_settings to a file in misc
    file_path = os.path.join(prj_path, 'misc', 'settings.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        dict_str = json.dumps(dict_settings, indent=4)
        f.write(dict_str)


# ------------------------------------------------------------------------------
# Add .git and .venv folders to new project
# ------------------------------------------------------------------------------
def add_extras():
    """
        Add .git and .venv folders to new project

        Adds a .git folder (repository) and a .venv (virtual environment) folder
        to the project, and sets them up as necessary.
    """

    # make sure we are in current proj path
    curr_dir = os.getcwd()
    dir = dict_settings['project']['path']
    os.chdir(dir)

    # add git folder
    cmd = 'git init'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # add venv dir
    # use '.venv' to be compatible with VSCodium
    cmd = 'python -m venv .venv'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # go back to old dir
    os.chdir(curr_dir)


# ------------------------------------------------------------------------------
# Recursively scan files/folders for replace/rename functions
# ------------------------------------------------------------------------------
def recurse(path):
    """
        Recursively scan files/folders for replace/rename functions

        Parameters:
            path [string]: the folder to start recursively scanning from

        This is a recursive function to scan for files/folders under a given
        folder. It iterates over the contents of the 'path' folder, checking if
        each item is a file or a folder. If it encounters a folder, it calls
        itself recursively, passing that folder as the parameter. If it
        encounters a file, it calls methods to do text replacement of headers,
        then other text. Finally it renames the file if the name contains a
        replacement key. Once all files are renamed, it will then bubble up to
        rename all folders.
    """

    # blacklist
    # don't replace headers, text, or path names for these items
    skip_all = [
        '.venv',
        '.git',
    ]
    skip_headers = [
    ]
    skip_text = [
        'metadata.py',
        'settings.json',
        'checklist.txt',
    ]
    skip_rename = [
    ]

    # remove all trailing slashes
    skip_all = [item.rstrip('/') for item in skip_all]
    skip_headers = [item.rstrip('/') for item in skip_headers]
    skip_text = [item.rstrip('/') for item in skip_text]
    skip_rename = [item.rstrip('/') for item in skip_rename]

    # get list of file names in dest dir
    items = [item for item in os.listdir(path) if item not in skip_all]
    for item in items:

        # put path back together
        path_item = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(path_item):

            # recurse itself to find more files
            recurse(path_item)

        else:

            # open file and get lines
            with open(path_item, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # replace headers from lines
                if item not in skip_headers:
                    lines = _replace_headers(lines)

                # replace text from lines
                if item not in skip_text:
                    lines = _replace_text(lines)

                # readme needs extra handling
                if item == 'README.md':
                    lines = _fix_readme(lines)

            # save lines
            with open(path_item, 'w', encoding='utf-8') as f:
                f.writelines(lines)

        # called for each file/folder
        if item not in skip_rename:
            _rename(path_item)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Check project name for allowed characters
# ------------------------------------------------------------------------------
def _validate_name(name):
    """
        Check project name for allowed characters

        Parameters:
            name [string]: the name to check for allowed characters

        Returns:
            [bool]: whether the name is valid to use

        This function checks the passed name for four criteria:
        1. blank name
        2. starts with an alpha char
        3. ends with an alphanumeric char
        4. contains only alphanumeric chars
    """

    # 1. check for blank name
    if name == '':
        return False

    # 2. match start or return false
    pattern = r'(^[a-zA-Z])'
    res = re.search(pattern, name)
    if not res:
        print('Project names must start with a letter')
        return False

    # 3. match end or return false
    pattern = r'([a-zA-Z0-9]$)'
    res = re.search(pattern, name)
    if not res:
        print('Project names must end with a letter or number')
        return False

    # 4. match middle or return false
    pattern = r'(^[a-zA-Z0-9]*$)'
    res = re.search(pattern, name)
    if not res:
        print('Project names must contain only letters or numbers')
        return False

    # if we made it this far, return true
    return True


# ------------------------------------------------------------------------------
# Replace header text inside files
# ------------------------------------------------------------------------------
def _replace_headers(lines):
    """
        Replace header text inside files

        Parameters:
            lines [list]: the list of file lines for replacing header text

        Returns:
            [list]: the list of replaced lines in the file

        This is a function to replace header text inside a file. Given a list of
        file lines, it iterates the list line by line, replacing header text as
        it goes. When it is done, it returns lhe list of lines. This replaces
        the __PP_.. stuff inside headers.
    """

    # the array of dunder replacements we will use
    prj_info = dict_settings['info']

    # for each line in array
    for i in range(0, len(lines)):

        # for each repl line
        for hdr_pair in LIST_HEADER:

            # pattern
            pattern = (
                r'(# |<!-- )'
                rf'({hdr_pair[0]})'
                r'( *: )'
                rf'({hdr_pair[1]})'
                r'([^ ]*)'
                r'( *)'
                r'(.*)'
            )
            res = re.search(pattern, lines[i])

            if res:

                # get the new value from settings
                rep = prj_info[hdr_pair[1]]

                # count what we will need without spaces
                key_cnt = (
                    len(res.group(1)) +
                    len(res.group(2)) +
                    len(res.group(3)) +
                    len(rep) +
                    len(res.group(5)) +
                    len(res.group(7))
                )

                # make spaces
                # NB: this looks funky but it works:
                # 1. get the length of the old line (NOT always 80 since we
                # can't have trailing spaces)
                # 2. subtract 1 for the newline
                # 3. subtract the other match lengths
                spaces = (
                    len(lines[i]) - 1 - key_cnt
                )
                spaces_str = ' ' * spaces

                # replace text in the line
                rep_str = rf'\g<1>\g<2>\g<3>{rep}\g<5>{spaces_str}\g<7>'
                lines[i] = re.sub(pattern, rep_str, lines[i])

    # return the changed lines
    return lines


# ------------------------------------------------------------------------------
# Replace text inside files
# ------------------------------------------------------------------------------
def _replace_text(lines):
    """
        Replace text inside files

        Parameters:
            lines [list]: the list of file lines for replacing text

        Returns:
            [list]: the list of replaced lines in the file

        This is a function to replace text inside a file. Given a list of file
        lines, it iterates the list line by line, replacing text as it goes.
        When it is done, it returns the list of lines. This replaces the
        __PP_... stuff inside the file, excluding headers (which are already
        handled).
    """

    # the array of dunder replacements we will use
    prj_info = dict_settings['info']

    # for each line in array
    for i in range(0, len(lines)):

        # replace text in line
        for key in prj_info.keys():
            if key in lines[i]:
                lines[i] = lines[i].replace(key, prj_info[key])

    # save file with replacements
    return lines


# ------------------------------------------------------------------------------
# Remove unnecessary parts of the README file
# ------------------------------------------------------------------------------
def _fix_readme(lines):
    """
        Remove unnecessary parts of the README file

        Parameters:
            lines [list]: the list of file lines for removing README text

        Returns:
            [list]: the list of replaced lines in the file

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as Module/Package or
        CLI/GUI.
    """

    # the strategy here is to go through the full README and only copy lines
    # that are 1) not in any block or 2) in the block we want
    # the most efficient way to do this is to have an array that receives wanted
    # lines, then return that array

    # NB: we use a new array vs. in-situ replacement here b/c we are removing
    # A LOT OF LINES, which in-situ would result in A LOT OF BLANK LINES and
    # while that would look *ok* in the resulting Markdown, looks UGLY in the
    # source code. so we opt for not copying those lines.

    # just a boolean flag to say if we are kajiggering
    # if True, we are in a block we don't want to copy
    ignore = False

    # where to put the needed lines
    new_lines = []

    # what type of project are we creating?
    prj_type = dict_settings['project']['type']

    # what to ignore in the text
    for key in DICT_README.keys():
        if prj_type in key:

            delete_start = DICT_README[key]['delete_start']
            delete_end = DICT_README[key]['delete_end']
            delete_tag = DICT_README[key]['delete_tag']

    # for each line
    for line in lines:

        # check if we have entered an invalid block
        if delete_start in line:
            ignore = True

        # we're still in a valid block
        if not ignore:

            # ignore block wrapper lines
            if delete_tag not in line:
                new_lines.append(line)

        # check if we have left the invalid block
        if delete_end in line:
            ignore = False

    # return the new set of lines
    return new_lines


# ------------------------------------------------------------------------------
# Function for renaming files/folders
# ------------------------------------------------------------------------------
def _rename(path):
    """
        Function for renaming files/folders

        Parameters:
            path [string]: the path to file/folder for renaming

        This is a function to rename files/folders. Given a path to a
        file/folder, it renames the path by replacing keys in the dict_settings
        keys with their appropriate replacements.
    """

    # the array of dunder replacements we will use
    prj_info = dict_settings['info']

    # store paths before changing
    old_path = path
    new_path = path

    # replace all replacements in path
    for key in prj_info.keys():
        new_path = new_path.replace(key, prj_info[key])

    # remove erroneous exts
    new_path = _remove_exts(new_path)

    # do the replacement in os (test exists for already renamed)
    if not os.path.exists(new_path):
        os.renames(old_path, new_path)


# ------------------------------------------------------------------------------
# Function for removing extraneous exts (for duplicate files in template)
# ------------------------------------------------------------------------------
def _remove_exts(path):
    """
        Function for removing extraneous exts (for duplicate files in template)

        Parameters:
            path [string]: the path to file/folder for removing exts

        Returns:
            [string]: the file with only the last ext

        This is a function to remove extraneous extensions. Given a path to a
        file/folder, it renames the path by removing extraneous extensions.
    """

    # split dir/file
    dir_name = os.path.dirname(path)
    base = os.path.basename(path)

    # split file name by dot
    file_array = base.split('.')

    # if there is at least one dot
    if len(file_array) > 2:

        # the result is the pre-dot plus last dot
        base = file_array[0] + '.' + file_array[-1]

    return os.path.join(dir_name, base)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.
    """

    main()

# -)
