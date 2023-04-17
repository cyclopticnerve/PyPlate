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

# date format
PRJ_DATE = '%m/%d/%Y'

# files to include in project
# paths are relative to DIR_TEMPLATE
DICT_FILES = {

    # common to all projects
    'common': [
        'conf',
        'docs',
        'misc',
        'tests',
        '.gitignore',
        'LICENSE.txt',
        'README.md',
        'requirements.txt',
    ],

    # for module projects
    'm': [
        'src/__PP_NAME_SMALL__.mod.py',
        'MANIFEST.in',
        'pyproject.toml',
    ],

    # for package projects
    'p': [
        'src/__PP_NAME_SMALL__.pkg',
        'MANIFEST.in',
        'pyproject.toml',
    ],

    # for cli projects
    'c': [
        'src/__PP_NAME_SMALL__.cli.py',
    ],

    # for gui projects
    'g': [
        'src/__PP_NAME_SMALL__.gui',
        'src/__PP_NAME_SMALL__.gui.py',
    ],
}

# folders/files to ignore when doing replacements
DICT_BLACKLIST = {

    # don't do anything with these files/folders
    'skip_all': [
        '.venv',
        '.git',
        'dist',
        'docs',
        'misc',
        'tests',
        '__pycache__',
        'PKG-INFO',
    ],

    # dont't fix internals, but path is ok
    'skip_file': [
        '__PP_NAME_SMALL__.png',
    ],

    # don't fix/check headers
    'skip_headers': [
    ],

    # don't fix/check text
    'skip_text': [
        'metadata.json',
        'metadata.py',
        "settings.json",
    ],

    # don't fix/check path
    'skip_path': [
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
        'delete_start': '<!-- __RM_APP_START__ -->',
        'delete_end':   '<!-- __RM_APP_END__ -->',
        'delete_tag':   '<!-- __RM_MOD_',
    },
    'cg': {
        'delete_start': '<!-- __RM_MOD_START__ -->',
        'delete_end':   '<!-- __RM_MOD_END__ -->',
        'delete_tag':   '<!-- __RM_APP_',
    },
}

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by metadata.py (from misc/settings.json)

# 'project' and 'info' are set using get_project_info()
# 'skip' is used by recurse()

g_dict_settings = {
    'project': {
        # m (Module), p (Package), c (CLI), g (GUI)
        'type':                 '',
        # path to project (DIR_PRJ_BASE/type_dir/Foo)
        'path':                 '',
    },
    'info': {
        '__PP_NAME_BIG__':      '',     # MyProject
        '__PP_NAME_SMALL__':    '',     # myproject
        '__PP_DATE__':          '',     # 12/08/2022
    },
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
    path = g_dict_settings['project']['path']
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
    global g_dict_settings

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
            g_dict_settings['project']['type'] = prj_type
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
        g_dict_settings['info']['__PP_NAME_BIG__'] = prj_name_big
        g_dict_settings['project']['path'] = prj_path
        break

    # calculate small name
    prj_name_small = prj_name_big.lower()
    g_dict_settings['info']['__PP_NAME_SMALL__'] = prj_name_small

    # calculate current date
    prj_date = datetime.now().strftime(PRJ_DATE)
    g_dict_settings['info']['__PP_DATE__'] = prj_date


# ------------------------------------------------------------------------------
# Copy template files to final location
# ------------------------------------------------------------------------------
def copy_template():
    """
        Copy template files to final location

        Get file paths/names from g_dict_settings and copy them to the project
        folder.
    """

    # create target folder
    prj_path = g_dict_settings['project']['path']
    os.makedirs(prj_path)

    # get project type
    proj_type = g_dict_settings['project']['type']

    # the group of files, common and type
    groups = [
        DICT_FILES['common'],
        DICT_FILES[proj_type]
    ]

    # for each group, common and type
    items = [item.strip(os.sep) for group in groups for item in group]
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

    # write g_dict_settings to conf file
    file_path = os.path.join(prj_path, 'conf', 'settings.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        dict_str = json.dumps(g_dict_settings, indent=4)
        f.write(dict_str)

    # write DICT_BLACKLIST to conf file
    file_path = os.path.join(prj_path, 'conf', 'blacklist.json')
    with open(file_path, 'w', encoding='utf-8') as f:
        dict_str = json.dumps(DICT_BLACKLIST, indent=4)
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
    dir = g_dict_settings['project']['path']
    os.chdir(dir)

    # add git folder
    cmd = 'git init'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # add venv dir
    # NB: use '.venv' to be compatible with VSCodium
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
    # skip_all = DICT_BLACKLIST['skip_all']
    # skip_file = DICT_BLACKLIST['skip_file']
    # skip_headers = DICT_BLACKLIST['skip_headers']
    # skip_text = DICT_BLACKLIST['skip_text']
    # skip_path = DICT_BLACKLIST['skip_path']

    # remove all trailing slashes
    skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_all']]
    skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_file']]
    skip_headers = [item.strip(os.sep)
                    for item in DICT_BLACKLIST['skip_headers']]
    skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_text']]
    skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_path']]

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

            # only open files we should be mucking in
            if item not in skip_file:

                # open file and get lines
                with open(path_item, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                    # replace headers from lines
                    if item not in skip_headers:
                        lines = _fix_headers(lines)

                    # replace text from lines
                    if item not in skip_text:
                        lines = _fix_text(lines)

                    # readme needs extra handling
                    if item == 'README.md':
                        lines = _fix_readme(lines)

                # save lines
                with open(path_item, 'w', encoding='utf-8') as f:
                    f.writelines(lines)

        # fix path/ext
        if item not in skip_path:
            new_path = _fix_path(path_item)

            # if a rename is required
            if path_item != new_path:

                # do the rename
                os.rename(path_item, new_path)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Replace header text inside files
# ------------------------------------------------------------------------------
def _fix_headers(lines):
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
    prj_info = g_dict_settings['info']

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
def _fix_text(lines):
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
    prj_info = g_dict_settings['info']

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
    prj_type = g_dict_settings['project']['type']

    # what to ignore in the text
    for key in DICT_README.keys():
        if prj_type in key:

            # get values for keys
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
def _fix_path(path):
    """
        Function for renaming files/folders

        Parameters:
            path [string]: the path to the file/folder for renaming

        Returns:
            [string]: the new path for the specified folder/file

        This is a function to rename files/folders. Given a path to a
        file/folder, it renames the path by replacing keys in the
        g_dict_settings keys with their appropriate replacements, and also
        removes any extraneous exts. This allows us to have different files and
        folders with the same name/ext, but quialifiers in between, thus:
        __PP_NAME_SMALL__.gui.py
        __PP_NAME_SMALL__.cli.py
        can cexist in the template, but will both end up as:
        __PP_NAME_SMALL__.py
        in the project.
    """

    # the array of dunder replacements we will use
    prj_info = g_dict_settings['info']

    # split the path into everything up to last part, and last part itself
    old_dir, old_file = os.path.split(path)

    # replace dunders in last path component
    for key in prj_info.keys():
        old_file = old_file.replace(key, prj_info[key])

    # split last part by dot
    dot_array = old_file.split('.')

    # if there are two or more dots
    # foo.bar.py
    if len(dot_array) > 2:

        # put back together using main name and last ext
        old_file = dot_array[0] + '.' + dot_array[-1]

    # if there is only one dot, and it's a folder
    # foo.bar/
    elif len(dot_array) > 1 and os.path.isdir(path):

        # just use main name
        old_file = dot_array[0]

    # put new name back with the 'up to last part'
    new_path = os.path.join(old_dir, old_file)

    # return the new path name
    return new_path


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
