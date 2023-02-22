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
DIR_SRC = os.path.dirname(os.path.abspath(__file__))

# this is the dir where the template files are located rel to the script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
DIR_TEMPLATE = os.path.abspath(f'{DIR_SRC}/../template')

# this is the dir for project location (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
DIR_BASE = os.path.abspath(f'{DIR_SRC}/../../')

# this is the current user home dir
# (e.g. /home/cyclopticnerve/)
DIR_USER = os.path.expanduser('~')

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
dict_settings = {
    'project': {
        'type': '',                 # m (Module), p (Package), c (CLI), g (GUI)
        'path': '',                 # path to project (DIR_BASE/type_dir/Foo)
    },
    'reps': {
        '__CN_NAME_BIG__':   '',    # Foo
        '__CN_NAME_SMALL__': '',    # foo
        '__CN_DATE__':       '',    # 12/08/2022
    },
    'files': {                      # files to include in project
        'common': [                 # common to all projects
            'misc/',
            'tests/',
            '.gitignore',
            'LICENSE.txt',
            'metadata.py',
            'README.md',
            'requirements.txt',
        ],
        'm': [                      # for module projects
            'src/__CN_NAME_SMALL__.mod.py',
            'MANIFEST.in',
            'pyproject.toml',
        ],
        'p': [                      # for package projects
            'src/__CN_NAME_SMALL__/',
            'MANIFEST.in',
            'pyproject.toml',
        ],
        'c': [                      # for cli projects
            'src/__CN_NAME_SMALL__.app.py',
            'argparse.py'
            'install.py',
            'uninstall.py',
        ],
        'g': [                      # for gui projects
            'gui/',
            'src/__CN_NAME_SMALL__.app.py',
            'argparse.py'
            'install.py',
            'uninstall.py',
        ],
    }
}

# ------------------------------------------------------------------------------
# Functions
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

    # call each step
    get_project_info()
    copy_template()
    recurse(dict_settings['project']['path'])
    add_extras()


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
        proj_type = input('Project type: [M]odule | [P]ackage | [C]LI | '
                          '[G]UI: ')

        # check for blank type
        proj_type = proj_type.strip()
        if proj_type == '':
            continue

        # check for valid type
        proj_type = proj_type.lower()[0]
        if proj_type not in 'mpcg':
            continue

        # store valid type and move on
        dict_settings['project']['type'] = proj_type
        break

    # configure subdir
    type_dir = ''
    if proj_type in 'mp':
        type_dir = 'Libs/'
    else:
        type_dir = 'Apps/'

    # loop forever until we get a valid name and path
    while True:

        # ask for project name
        prj_name = input('Project name: ')

        # check for blank name
        prj_name = prj_name.strip()
        if prj_name == '':
            continue

        # check for valid name
        if not validate_name(prj_name):
            continue

        # assume entered name is final
        prj_name_big = prj_name
        dict_settings['reps']['__CN_NAME_BIG__'] = prj_name_big

        # calculate final proj location
        prj_path = os.path.join(DIR_BASE, type_dir, prj_name_big)

        # check if project already exists
        if os.path.exists(prj_path):
            print(f'Project {prj_path} already exists')
            continue

        # if name is valid, move on
        dict_settings['project']['path'] = prj_path
        break

    # calculate small name
    prj_name_small = prj_name_big.lower()
    dict_settings['reps']['__CN_NAME_SMALL__'] = prj_name_small

    # calculate current date
    dict_settings['reps']['__CN_DATE__'] = datetime.now().strftime('%m/%d/%Y')


# ------------------------------------------------------------------------------
# Check project name for allowed characters
# ------------------------------------------------------------------------------
def validate_name(name):
    """
        Check project name for allowed characters

        Paramaters:
            name [string]: the name to check for allowed characters

        Returns:
            [bool]: whether the name is valid to use

        This function checks the passed name for three criteria:
        1. starts with an alpha char
        2. ends with an alphanumeric char
        3. contains only alphanumeric chars
    """

    # create match pattern strings
    pattern_start = r'(^[a-zA-Z])'
    pattern_end = r'([a-zA-Z0-9]$)'
    pattern_middle = r'(^[a-zA-Z0-9]*$)'

    # match start or return false
    search_start = re.search(pattern_start, name)
    if not search_start:
        print('Project names must start with a letter')
        return False

    # match end or return false
    search_end = re.search(pattern_end, name)
    if not search_end:
        print('Project names must end with a letter or number')
        return False

    # match middle or return false
    search_middle = re.search(pattern_middle, name)
    if not search_middle:
        print('Project names must contain only letters and numbers')
        return False

    # if we made it this far, return true
    return True


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
        dict_settings['files']['common'],
        dict_settings['files'][proj_type]
    ]

    # for each group, common and type
    for group in groups:

        # for each file/folder in group
        for file in group:

            # build old path/new path
            path_old = os.path.join(DIR_TEMPLATE, file)
            path_new = os.path.join(prj_path, file)

            # if it's a dir, copy dir
            if os.path.isdir(path_old):
                shutil.copytree(path_old, path_new)
            else:

                # if it's a file, get the file's dir
                dir_new = os.path.dirname(path_new)

                # create dir if neccessary
                os.makedirs(dir_new, exist_ok=True)

                # then copy file
                shutil.copy2(path_old, path_new)


# ------------------------------------------------------------------------------
# Recursivly scan files/folders for replace/rename functions
# ------------------------------------------------------------------------------
def recurse(path):
    """
        Recursivly scan files/folders for replace/rename functions

        Paramaters:
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

    # don't rename these dirs or files, or change file contents
    # NB: must not end in '/'!!!
    skip_dirs = [
        'misc'
    ]

    # get list of replaceable file names
    items = [item for item in os.listdir(path) if item not in skip_dirs]
    for item in items:

        # put path back together
        path_item = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(path_item):

            # recurse itself to find more files
            recurse(path_item)

        else:

            # open file and get lines
            with open(path_item) as file:
                lines = file.readlines()

            # replace headers/text from lines
            lines = replace_headers(lines)
            lines = replace_text(lines)

            # readme needs extra handling
            if item == 'README.md':
                lines = fix_readme(lines)

            # save lines
            with open(path_item, 'w') as file:
                file.writelines(lines)

        # called for each file/folder
        rename(path_item)


# ------------------------------------------------------------------------------
# Replace header text inside files
# ------------------------------------------------------------------------------
def replace_headers(lines):
    """
        Replace header text inside files

        Paramaters:
            lines [list]: the list of file lines for replacing header text

        Returns:
            [list]: the list of replaced lines in the file

        This is a function to replace header text inside a file. Given a list of
        file lines, it iterates the list line by line, replacing header text as
        it goes. When it is done, it returns lhe list of lines. This replaces
        the __CN_.. stuff inside headers.
    """

    # NEXT: this could be done better with regex

    # an array that represents the three sections of a header line
    # NB: we keep the trailing spaces here to accurately count the number of
    # spaces needed to format
    # we will strip them later to avoid pylama reporting trialing spaces
    hdr_lines = [
        ['# Project : ', '__CN_NAME_BIG__',   '/          \\ '],
        ['# Filename: ', '__CN_NAME_SMALL__', '|     ()     |'],
        ['# Date    : ', '__CN_DATE__',       '|            |'],
        ['<!-- Project : ', '__CN_NAME_BIG__',   '/          \\  -->'],
        ['<!-- Filename: ', '__CN_NAME_SMALL__', '|     ()     | -->'],
        ['<!-- Date    : ', '__CN_DATE__',       '|            | -->'],
    ]

    # the array of dunder replacements we will use
    reps = dict_settings['reps']

    # for each line in array
    for i in range(0, len(lines)):

        # for each repl line
        for hdr_line in hdr_lines:

            # build start str
            key = hdr_line[0] + hdr_line[1]

            # if the key is in the line
            if key in lines[i]:

                # replace the dunder
                rep = reps[hdr_line[1]]

                # calculate spaces
                spaces = 80 - (len(hdr_line[0]) + len(rep) + len(hdr_line[2]))
                spaces_str = ' ' * spaces

                # create replacement string (with newline!!!)
                rep_s = f'{hdr_line[0]}{rep}{spaces_str}{hdr_line[2].strip()}\n'

                # replace text in line
                lines[i] = rep_s

    # return the changed lines
    return lines


# ------------------------------------------------------------------------------
# Replace text inside files
# ------------------------------------------------------------------------------
def replace_text(lines):
    """
        Replace text inside files

        Paramaters:
            lines [list]: the list of file lines for replacing text

        Returns:
            [list]: the list of replaced lines in the file

        This is a function to replace text inside a file. Given a list of file
        lines, it iterates the list line by line, replacing text as it goes.
        When it is done, it returns the list of lines. This replaces the
        __CN_... stuff inside the file, excluding headers (which are already
        handled).
    """

    # the array of dunder replacements we will use
    reps = dict_settings['reps']

    # for each line in array
    for i in range(0, len(lines)):

        # replace text in line
        for key in reps.keys():
            if key in lines[i]:
                lines[i] = lines[i].replace(key, reps[key])

    # save file with replacements
    return lines


# ------------------------------------------------------------------------------
# Remove unneccesary parts of the README file
# ------------------------------------------------------------------------------
def fix_readme(lines):
    """
        Remove unneccesary parts of the README file

        Paramaters:
            lines [list]: the list of file limnes for removing README text

        Returns:
            [list]: the list of replaced lines in the file

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as Module/Package or
        CLI/GUI.
    """

    # the strategy here is to go through the full README and only copy lines
    # that are 1) not in any block or 2) in the block we want
    # the most efficient way to do this is to have an array that recieves wanted
    # lines, then save that array to a file

    # what type of project are we creating?
    proj_type = dict_settings['project']['type']

    # just a boolean flag to say if we are kajiggering
    # if True, we are in a block we don't want to copy
    ignore = False

    # we use a new array vs. in-situ replacement here b/c we are removing
    # A LOT OF LINES, which in-situ would result in A LOT OF BLANK LINES and
    # while that would look *ok* in the reulting Markdown, looks UGLY in the
    # source code. so we opt for not copying those lines.

    # where to put the needed lines
    new_lines = []

    # what to ignore in the text
    if proj_type in 'mp':
        start_str = '<!-- __CN_APP_START__ -->'
        end_str = '<!-- __CN_APP_END__ -->'
        ignore_str = '<!-- __CN_MOD_'
    else:
        start_str = '<!-- __CN_MOD_START__ -->'
        end_str = '<!-- __CN_MOD_END__ -->'
        ignore_str = '<!-- __CN_APP_'

    # for each line
    for line in lines:

        # check if we are in a block
        if start_str in line:
            ignore = True

        # it's a valid line block, just copy it
        if not ignore:

            # ignore block wrapper lines
            if ignore_str not in line:
                new_lines.append(line)

        # check if we have left the block
        if end_str in line:
            ignore = False

    # return the new set of lines
    return new_lines


# ------------------------------------------------------------------------------
# Function for renaming files/folders
# ------------------------------------------------------------------------------
def rename(path):
    """
        Function for renaming files/folders

        Paramaters:
            path [string]: the path to file/folder for renaming

        This is a function to rename files/folders. Given a path to a
        file/folder, it renames the path by replacing keys in the dict_settings
        keys with their appropriate replacements.
    """

    # the array of dunder replacements we will use
    reps = dict_settings['reps']

    # replace all replacements in path
    new_path = path
    for key in reps.keys():
        new_path = new_path.replace(key, reps[key])

    # fix filenames with extras added on (.app, .mod, etc.)
    new_path = remove_exts(new_path)

    # do the replacement in os (test exists for already renamed)
    if os.path.exists(path):
        os.renames(path, new_path)


# ------------------------------------------------------------------------------
# Function for removinf extraneous exts (for duplicate files in template)
# ------------------------------------------------------------------------------
def remove_exts(path):
    """
        Function to remove extraneous exts (for duplicate files in template)

        Paramaters:
            path [string]: the path to file/folder for removing exts

        Returns:
            [string]: the file with only the last ext

        This is a function to remove extraneous extensions. Given a path to a
        file/folder, it renames the path by removing extranious extensions.
    """

    # split dir/file
    dir = os.path.dirname(path)
    base = os.path.basename(path)

    # split file name by dot
    file_array = base.split('.')

    # if there is at least one dot
    if len(file_array) > 2:

        # no ext for app file
        if file_array[1] == 'app':
            base = file_array[0]
        else:

            # the result is the pre-dot plus last dot
            base = file_array[0] + '.' + file_array[-1]

    return os.path.join(dir, base)


# ------------------------------------------------------------------------------
# Add .git and venv folders to new project
# ------------------------------------------------------------------------------
def add_extras():
    """
        Add .git and venv folders to new project

        Adds a .git folder (repository) and a venv (virtual environment) folder
        to the project, and sets them up as necessary.
    """

    dir = dict_settings['project']['path']

    # make sure we are in current proj path w/chdir
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
