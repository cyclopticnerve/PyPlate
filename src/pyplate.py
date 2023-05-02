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

# this is the dir above where the script is being run from
# (e.g. ~/Documents/Projects/Python/PyPlate/src/)
dir = os.path.dirname(__file__)
dir_pyplate = os.path.join(dir, '..')
DIR_PYPLATE = os.path.abspath(dir_pyplate)

# this is the dir where the template files are located rel to the script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
DIR_TEMPLATE = os.path.join(DIR_PYPLATE, 'template')

# this is the dir for project location (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
dir_base = os.path.join(DIR_PYPLATE, '..')
DIR_BASE = os.path.abspath(dir_base)

# date format
DICT_DATE = '%m/%d/%Y'

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
        'CHANGELOG.md',
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
        'src/gui',
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
    'skip_header': [
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
        'rm_delete_start': '<!-- __RM_APP_START__ -->',
        'rm_delete_end':   '<!-- __RM_APP_END__ -->',
        'rm_delete_tag':   '<!-- __RM_MOD_',
    },
    'cg': {
        'rm_delete_start': '<!-- __RM_MOD_START__ -->',
        'rm_delete_end':   '<!-- __RM_MOD_END__ -->',
        'rm_delete_tag':   '<!-- __RM_APP_',
    },
}

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by metadata.py (from misc/settings.json)
g_dict_settings = {
    'project': {
        # m (Module), p (Package), c (CLI), g (GUI)
        'type':                 '',
        # path to project (DIR_BASE/dir_type/MyProject)
        'dir':                  '',
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
# The main function of the program
# ------------------------------------------------------------------------------
def main():
    """
        The main function of the program

        This function is the main entry point for the program, initializing the
        program, and performing its steps.
    """

    # call each step to create project
    get_project_info()
    copy_template()

    # call recurse to do replacements in final project location
    dir = g_dict_settings['project']['dir']
    recurse(dir)

    # do stuff to final dir after recurse
    do_extras()


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_project_info():
    """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        g_dict_settings.
    """

    # the settings dict (global b/c we will modify here)
    global g_dict_settings

    # loop forever until we get a valid type
    while True:

        # ask what type of project
        type_prj = input(
            'Project type: [m]odule | [p]ackage | [c]li | [g]ui: '
        )

        # check project type
        pattern = r'(^(m|p|c|g{1})$)'
        res = re.search(pattern, type_prj, re.I)
        if res:

            # we got a valid type
            type_prj = type_prj.lower()
            g_dict_settings['project']['type'] = type_prj
            break

    # configure subdir
    dir_type = ''
    if type_prj in 'mp':
        dir_type = 'Libs'
    else:
        dir_type = 'Apps'

    # loop forever until we get a valid name and path
    while True:

        # ask for project name
        info_name_big = input('Project name: ')

        # check for valid name
        if not _fix_name(info_name_big):
            continue

        # calculate final project location
        dir_prj = os.path.join(DIR_BASE, dir_type, info_name_big)

        # check if project already exists
        if os.path.exists(dir_prj):
            print(f'Project {dir_prj} already exists')
            continue

        # if name is valid, move on
        g_dict_settings['info']['__PP_NAME_BIG__'] = info_name_big
        g_dict_settings['project']['dir'] = dir_prj
        break

    # calculate small name
    info_name_small = info_name_big.lower()
    g_dict_settings['info']['__PP_NAME_SMALL__'] = info_name_small

    # calculate current date
    info_date = datetime.now().strftime(DICT_DATE)
    g_dict_settings['info']['__PP_DATE__'] = info_date


# ------------------------------------------------------------------------------
# Copy template files to final location
# ------------------------------------------------------------------------------
def copy_template():
    """
        Copy template files to final location

        Get file paths/names from DICT_FILES and copy them to the project
        folder.
    """

    # get project type
    type_prj = g_dict_settings['project']['type']

    # create target folder
    dir_prj = g_dict_settings['project']['dir']
    os.makedirs(dir_prj)

    # the group of files, common and type
    groups = [
        DICT_FILES['common'],
        DICT_FILES[type_prj]
    ]

    # for each group, common and type, remove leading/trailing slashes
    items = [item.strip(os.sep) for group in groups for item in group]
    for item in items:

        # build old path/new path
        path_old = os.path.join(DIR_TEMPLATE, item)
        path_new = os.path.join(dir_prj, item)

        # if it's a dir, copy dir
        if os.path.isdir(path_old):
            shutil.copytree(path_old, path_new)
        else:

            # if it's a file, get the file's dir and create
            dir_new = os.path.dirname(path_new)
            os.makedirs(dir_new, exist_ok=True)

            # then copy file
            shutil.copy2(path_old, path_new)

    # copy the 'starter kit' of requirements
    # NB: this is all the reqs collected while developing PyPlate
    # should be a good place to start developing a project in VSCode
    # also by copying from this project rather than hard-coding the list, it
    # will get updated every time the PyPlate project file is updated, making
    # it future-proof*
    # (* not guaranteed to be future-proof)
    path_old = os.path.join(DIR_PYPLATE, 'requirements.txt')
    path_new = os.path.join(dir_prj, 'requirements.txt')
    shutil.copy2(path_old, path_new)

    # write DICT_BLACKLIST to conf file
    path_blacklist = os.path.join(dir_prj, 'conf', 'blacklist.json')
    with open(path_blacklist, 'w', encoding='utf-8') as f:
        dict_blacklist = json.dumps(DICT_BLACKLIST, indent=4)
        f.write(dict_blacklist)

    # write g_dict_settings to conf file
    path_settings = os.path.join(dir_prj, 'conf', 'settings.json')
    with open(path_settings, 'w', encoding='utf-8') as f:
        dict_settings = json.dumps(g_dict_settings, indent=4)
        f.write(dict_settings)


# ------------------------------------------------------------------------------
# Recursively scan folders/files for replace/rename functions
# ------------------------------------------------------------------------------
def recurse(dir):
    """
        Recursively scan folders/files for replace/rename functions

        Parameters:
            dir [string]: the directory to start recursively scanning from

        This is a recursive function to scan for folders/files under a given
        folder. It iterates over the contents of the 'path' folder, checking if
        each item is a file or a folder. If it encounters a folder, it calls
        itself recursively, passing that folder as the parameter. If it
        encounters a file, it calls methods to do text replacement of headers,
        then other text. Finally it renames the file if the name contains a
        replacement key. Once all files are renamed, it will then bubble up to
        rename all folders.
    """

    # blacklist
    # don't check everything, headers, text, or path names for these items
    # remove all leading/trailing slashes
    skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_all']]
    skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_file']]
    skip_header = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_header']]
    skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_text']]
    skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_path']]

    # get list of file names in dest dir
    items = [item for item in os.listdir(dir) if item not in skip_all]
    for item in items:

        # put path back together
        path_item = os.path.join(dir, item)

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
                    if item not in skip_header:
                        lines = _fix_header(lines)

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
            path_new = _fix_path(path_item)

            # if a rename is required
            if path_item != path_new:

                # do the rename
                os.rename(path_item, path_new)


# ------------------------------------------------------------------------------
# Add extra folders/file to new project after recurse
# ------------------------------------------------------------------------------
def do_extras():
    """
        Add extra folders/files to new project after recurse

        Adds a .git folder (repository) and a .venv (virtual environment) folder
        to the project, and sets them up as necessary.
    """

    # get pyplate/src dir
    dir_curr = os.getcwd()

    # make sure we are in project path
    dir_prj = g_dict_settings['project']['dir']
    os.chdir(dir_prj)

    # add git folder
    cmd = 'git init'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # add venv dir
    # NB: use '.venv' to be compatible with VSCodium
    cmd = 'python -m venv .venv'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # create tree
    path_tree = os.path.join(dir_prj, 'misc', 'tree.txt')
    with open(path_tree, 'w', encoding='utf-8') as f:

        cmd = 'tree --dirsfirst --noreport --gitignore'
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=f)

    # go back to old dir
    os.chdir(dir_curr)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Replace header text inside files
# ------------------------------------------------------------------------------
def _fix_header(lines):
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
    info = g_dict_settings['info']

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
                rep = info[hdr_pair[1]]

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
                int_spaces = (
                    len(lines[i]) - 1 - key_cnt
                )
                str_spaces = ' ' * int_spaces

                # replace text in the line
                str_rep = rf'\g<1>\g<2>\g<3>{rep}\g<5>{str_spaces}\g<7>'
                lines[i] = re.sub(pattern, str_rep, lines[i])

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
    info = g_dict_settings['info']

    # for each line in array
    for i in range(0, len(lines)):

        # replace text in line
        for key in info.keys():
            if key in lines[i]:
                lines[i] = lines[i].replace(key, info[key])

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

    # NB: the strategy here is to go through the full README and only copy lines
    # that are 1) not in any block or 2) in the block we want
    # the most efficient way to do this is to have an array that receives wanted
    # lines, then return that array
    # we use a new array vs. in-situ replacement here b/c we are removing
    # A LOT OF LINES, which in-situ would result in A LOT OF BLANK LINES and
    # while that would look *ok* in the resulting Markdown, looks UGLY in the
    # source code. so we opt for not copying those lines.

    # just a boolean flag to say if we are kajiggering
    # if True, we are in a block we don't want to copy
    ignore = False

    # where to put the needed lines
    new_lines = []

    # what type of project are we creating?
    type_prj = g_dict_settings['project']['type']

    # what to ignore in the text
    for key in DICT_README.keys():
        if type_prj in key:

            # get values for keys
            rm_delete_start = DICT_README[key]['rm_delete_start']
            rm_delete_end = DICT_README[key]['rm_delete_end']
            rm_delete_tag = DICT_README[key]['rm_delete_tag']

    # for each line
    for line in lines:

        # check if we have entered an invalid block
        if rm_delete_start in line:
            ignore = True

        # we're still in a valid block
        if not ignore:

            # ignore block wrapper lines
            if rm_delete_tag not in line:
                new_lines.append(line)

        # check if we have left the invalid block
        if rm_delete_end in line:
            ignore = False

    # return the new set of lines
    return new_lines


# ------------------------------------------------------------------------------
# Function for renaming folders/files
# ------------------------------------------------------------------------------
def _fix_path(path):
    """
        Function for renaming folders/files

        Parameters:
            path [string]: the path to the folder/file for renaming

        Returns:
            [string]: the new path for the specified folder/file

        This is a function to rename folders/files. Given a path to a
        folder/file, it renames the path by replacing items in the
        g_dict_settings keys with their appropriate replacements, and also
        removes any extraneous exts. This allows us to have different files and
        folders with the same name/ext, but qualifiers in between, thus:
        __PP_NAME_SMALL__.gui.py
        __PP_NAME_SMALL__.cli.py
        can coexist in template/src, but will both end up as:
        project.gui.py
        project.cli.py
        after __PP_NAME_SMALL__ replacement, and then:
        project.py
        after ext replacement.
    """

    # the array of dunder replacements we will use
    info = g_dict_settings['info']

    # split the path into everything up to last part, and last part itself
    dir_old, file_old = os.path.split(path)

    # replace dunders in last path component
    for key in info.keys():
        file_old = file_old.replace(key, info[key])

    # split last part by dot
    dot_array = file_old.split('.')

    # if there are two or more dots
    # foo.bar.py
    if len(dot_array) > 2:

        # put back together using main name and last ext
        file_old = dot_array[0] + '.' + dot_array[-1]

    # if there is only one dot, and it's a folder
    # foo.bar/
    elif len(dot_array) > 1 and os.path.isdir(path):

        # just use main name
        file_old = dot_array[0]

    # put new name back with the 'up to last' part
    path_new = os.path.join(dir_old, file_old)

    # return the new path name
    return path_new


# ------------------------------------------------------------------------------
# Check project name for allowed characters
# ------------------------------------------------------------------------------
def _fix_name(name):
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

    # NB: there is an easier way to do this with regex:
    # ^([a-zA-Z]|[a-zA-Z]+[a-zA-Z\d]*[a-zA-Z\d]+)$
    # AND OMG DID IT TAKE A LONG TIME TO FIND IT!
    # in case you were looking for it. It will give you a quick yes-no answer.
    # I don't use it here because I want to give the user as much feedback as
    # possible, so I break down the regex into steps where each step explains
    # which part of the name is wrong.

    # check for blank name
    if name == '':
        return False

    # match start or return false
    pattern = r'(^[a-zA-Z])'
    res = re.search(pattern, name)
    if not res:
        print('Project names must start with a letter')
        return False

    # match end or return false
    pattern = r'([a-zA-Z\d]$)'
    res = re.search(pattern, name)
    if not res:
        print('Project names must end with a letter or number')
        return False

    # match middle or return false
    pattern = r'(^[a-zA-Z\d]*$)'
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

    # run main function
    main()

# -)
