#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pymaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

from datetime import datetime
# import json
import os
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
        'dir':  '',                 # DIR_BASE/type_dir/Foo
    },
    'reps': {
        '__CN_BIG_NAME__':   '',    # Foo
        '__CN_SMALL_NAME__': '',    # foo
        '__CN_DATE__':       '',    # 12/08/2022
    },
    'files': {                      # files to include in project
        'common': [                 # common to all projects
            'misc/',
            'tests/test.py',
            '.gitignore',
            'LICENSE.txt',
            'metadata.py',
            'README.md',
        ],
        'm': [                      # for module projects
            'src/__CN_SMALL_NAME___mod.py',
            'tests/import_test_mod.py',
            'MANIFEST.in',
            'pyproject.toml',
            'requirements.txt',
        ],
        'p': [                      # for package projects
            'src/__CN_SMALL_NAME__/',
            'tests/import_test_pkg.py',
            'MANIFEST.in',
            'pyproject.toml',
            'requirements.txt',
        ],
        'c': [                      # for cli projects
            'src/__CN_SMALL_NAME___app.py',
            'install.py',
            'uninstall.py',
        ],
        'g': [                      # for gui projects
            'gui/',
            'src/__CN_SMALL_NAME___app.py',
            'install.py',
            'uninstall.py',
        ]
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
    recurse(dict_settings['project']['dir'])
    # add_git_venv()


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

    # ask what type of project
    proj_type = input('Type of project: [M]odule | [P]ackage | [C]LI | [G]UI: ')
    proj_type = proj_type.strip()
    if proj_type == '':
        exit()
    proj_type = proj_type.lower()[0]
    if proj_type not in 'mpcg':
        exit()
    dict_settings['project']['type'] = proj_type

    # configure subdir
    if proj_type in 'mp':
        type_dir = 'Libs/'
    else:
        type_dir = 'Apps/'

    # ask for project name
    prj_name_big = input('Project name: ')
    prj_name_big = prj_name_big.strip()
    if prj_name_big == '':
        exit()
    prj_name_big = prj_name_big.capitalize()
    dict_settings['reps']['__CN_BIG_NAME__'] = prj_name_big

    # calculate final proj location
    prj_path = os.path.join(DIR_BASE, type_dir, prj_name_big)
    if os.path.exists(prj_path):
        print(f'Project {prj_path} already exists')
        exit()
    dict_settings['project']['dir'] = prj_path

    # calculate small name
    dict_settings['reps']['__CN_SMALL_NAME__'] = prj_name_big.lower()

    # calculate current date
    dict_settings['reps']['__CN_DATE__'] = datetime.now().strftime('%m/%d/%Y')


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
    prj_dir = dict_settings['project']['dir']
    os.makedirs(prj_dir)

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
            old_path = os.path.join(DIR_TEMPLATE, file)
            new_path = os.path.join(prj_dir, file)

            # if it's a dir, copy dir
            if os.path.isdir(old_path):
                shutil.copytree(old_path, new_path)
            else:

                # if it's a file, get the file's dir
                tmp_path = os.path.dirname(new_path)

                # create dir if neccessary
                os.makedirs(tmp_path, exist_ok=True)

                # then copy file
                shutil.copy2(old_path, new_path)


# ------------------------------------------------------------------------------
# Recursivly scan files/folders for rename/replace functions
# ------------------------------------------------------------------------------
def recurse(path):

    """
        Recursivly scan files/folders for rename/replace functions

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
    # NEXT: this should be editable (also skip_files? or figure out if each
    # entry is folder or file?)
    skip_dirs = ['misc']

    # returns only final path part for each entry
    dir_list = os.listdir(path)

    # for each file/folder
    for item in dir_list:

        # put path back together
        item_path = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(item_path):

            # always skip misc folder (never replace/rename)
            if item not in skip_dirs:

                # recurse itself to find more files
                recurse(item_path)

        else:
            # NEXT: do one open and pass array of lines to each function
            replace_headers(item_path)
            replace_text(item_path)

            # readme needs extra handling
            if item == 'README.md':
                fix_readme(item_path)

        # called for each file/folder
        rename(item_path)


# ------------------------------------------------------------------------------
# Replace header text inside files
# ------------------------------------------------------------------------------
def replace_headers(path):

    """
        Replace header text inside files

        Paramaters:
            path [string]: the path to file for replacing header text

        This is a function to replace header text inside a file. Given a path to
        a file, it iterates the file line by line, replacing header text as it
        goes. When it is done, it saves the file to disk. This replaces the
        __CN_.. stuff inside headers.
    """

    # an array that represents the three sections of a header line
    hdr_lines = [
        ['# Project : ', '__CN_BIG_NAME__',   '/          \\ '],
        ['# Filename: ', '__CN_SMALL_NAME__', '|     ()     |'],
        ['# Date    : ', '__CN_DATE__',       '|            |'],
        ['<!-- Project : ', '__CN_BIG_NAME__',   '/          \\  -->'],
        ['<!-- Filename: ', '__CN_SMALL_NAME__', '|     ()     | -->'],
        ['<!-- Date    : ', '__CN_DATE__',       '|            | -->'],
    ]

    # the array of dunder replacements we will use
    reps = dict_settings['reps']

    # open file as text line array
    with open(path) as file:
        lines = file.readlines()

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
                rep_str = f'{hdr_line[0]}{rep}{spaces_str}{hdr_line[2]}\n'

                # replace text in line
                lines[i] = rep_str

    # save the file with changes
    with open(path, 'w') as file:
        file.writelines(lines)


# ------------------------------------------------------------------------------
# Replace text inside files
# ------------------------------------------------------------------------------
def replace_text(path):

    """
        Replace text inside files

        Paramaters:
            path [string]: the path to the file for replacing text

        This is a function to replace text inside a file. Given a path to a
        file, it iterates the file line by line, replacing text as it goes. When
        it is done, it saves the file to disk. This replaces the __CN_... stuff
        inside the file, excluding headers (which are already handled).
    """

    # the array of dunder replacements we will use
    reps = dict_settings['reps']

    # open file as text line array
    with open(path) as file:
        lines = file.readlines()

    # for each line in array
    for i in range(0, len(lines)):

        # replace text in line
        for key in reps.keys():
            lines[i] = lines[i].replace(key, reps[key])

    # NB: i think file.readlines() strips the string, so we lose the
    # last blank line, which is part of my styling
    # so add it back in before saving
    lines.append('\n')

    # save file with replacements
    with open(path, 'w') as file:
        file.writelines(lines)


# ------------------------------------------------------------------------------
# Remove unneccesary parts of the README file
# ------------------------------------------------------------------------------
def fix_readme(path):

    """
        Remove unneccesary parts of the README file

        Paramaters:
            path [string]: the path to the README for removing text

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as Module/Package or
        CLI/GUI.
    """

    # NB: the strategy here is to go through the full README and only copy lines
    # that are 1) not in any block or 2) in the block we want
    # the most efficient way to do this is to have an array that recieves wanted
    # lines, then save that array to a file

    # what type of project are we creating?
    proj_type = dict_settings['project']['type']

    # just a boolean flag to say if we are kajiggering
    # if True, we are in a block we don't want to copy
    ignore = False

    # NB: we use a new array vs. in-situ replacement here b/c we are removing
    # A LOT OF LINES, which in-situ would result in A LOT OF BLANK LINES and
    # while that would look *ok* in the reulting README, looks UGLY in the
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

    # get the file line
    with open(path) as file:
        lines = file.readlines()

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

    # save the kajiggered line line
    with open(path, 'w') as file:
        file.writelines(new_lines)


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

    """

        if file:
            just loop over reps, replacing all, and rename old_path to new_path

        if folder:
            os.renames? replace all in all parts, and do one rename at end
            os.rename? replace current part, working back up?
    """

    # the array of dunder replacements we will use
    reps = dict_settings['reps']

    new_path = path
    changed = False

    # for each replacement key
    for key in reps.keys():

        # TODO: this prevents problems where we rename a file in a folder that
        # we (will) also renamed (not sure but it works?)
        # if key in item:

        # print('item:', item)
        # print('item_path:', item_path)

        # # do the string replace
        if key in new_path:
            new_path = new_path.replace(key, reps[key])
            changed = True

    # print('item:', new_item)
    # # # remove trailing identifiers
    # # new_item = new_item.replace('_app', '')
    # # new_item = new_item.replace('_mod', '')

    # # # create new path
    # new_path = os.path.join(path, new_item)

    # do the actual rename
    if changed:
        print(f'rename {path} to {new_path}')
    # os.rename(path, new_path)


# ------------------------------------------------------------------------------
# Add .git and venv folders to new project
# ------------------------------------------------------------------------------
def add_git_venv():

    """
        Add .git and venv folders to new project

        Adds a .git folder (repository) and a venv (virtual environment) folder
        to the project, and sets them up as necessary.
    """

    # make sure we are in current proj path w/chdir
    os.chdir(dict_settings['project']['dir'])

    # add git folder
    cmd = 'git init'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # add venv dir
    cmd = 'python -m venv venv'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line, e.g. 'python pymaker.py'.
    """

    main()

# -)
