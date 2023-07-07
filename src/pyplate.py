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

# some useful constants
DIR_FILE = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

# this is the dir above where the script is being run from
# (e.g. ~/Documents/Projects/Python/PyPlate/)
dir_pyplate = os.path.join(DIR_FILE, '..')
DIR_PYPLATE = os.path.abspath(dir_pyplate)

# this is the dir where the template files are located rel to the script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
DIR_TEMPLATE = os.path.join(DIR_PYPLATE, 'template')

# this is the dir for project location (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
dir_base = os.path.join(DIR_PYPLATE, '..')
DIR_BASE = os.path.abspath(dir_base)

# ------------------------------------------------------------------------------

# TODO: document that this should be changed (or put it in a file somewhere)

# for now, these values should be edited once before pyplate.py is run for the
# first time (this is a work in progress)
# STR_AUTHOR = 'foobar'
# STR_EMAIL = 'foobar@gmail.com'
# STR_LICENCE = 'WTFPLv2'

# # NB: the struggle here is that using the fixed format results in a four-digit
# # year, but using the locale format ('%x') results in a two-digit year (at least
# # for my locale, which in 'en_US'). so what to do? what i really want is a
# # locale format that uses four-digit years everywhere. so i am faced with a
# # 'cake and eat it too' situation. not sure how to proceed but i think for now
# # i will leave this as a user-editable string and place it in the realm of
# # 'edit it before you run' along with author and email...
# FMT_DATE = '%m/%d/%Y'

# TODO: remove this
DEBUG = True

# check if debug is active
# NB: with this block of code, you can set DEDBUG to True or False, or comment
# it out (same as False)
try:
    if DEBUG:
        path_user = os.path.join(DIR_PYPLATE, 'conf', 'user_pyplate.json')
    else:
        path_user = os.path.join(DIR_PYPLATE, 'conf', 'user.json')
except (NameError):
    path_user = os.path.join(DIR_PYPLATE, 'conf', 'user.json')

# load user info
DICT_USER = {}
if os.path.exists(path_user):
    with open(path_user, 'r') as f:
        try:
            DICT_USER = json.load(f)
        except (Exception):
            print(f'{f} is not a valid JSON file')
            exit()

# check for empty strings
for val in DICT_USER.values():
    if val == '':
        print(f'Values in {path_user} must not be empty')
        print('for date format, see https://strftime.org/')
        exit()

# ------------------------------------------------------------------------------

# the array of names for each project type
# NB: key is short type (displayed in get_project_info())
# val[0] is long type name (displayed in get_project_info())
# val[1] is subdirectory where project will be created
# val[2] is directory under template where project files come from
DICT_TYPE = {
    'm': ['Module',     'Modules',  'mod'],
    'p': ['Package',    'Packages', 'pkg'],
    'c': ['CLI',        'CLIs',     'cli'],
    'g': ['GUI',        'GUIs',     'gui'],
}

# folders/files to ignore when doing replacements
# NB: thes lists are explained in detail in the README file
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
        'locale',
    ],

    # dont't fix/check internals, but do fix path
    'skip_file': [
        '__PP_NAME_SMALL__.png',
    ],

    # don't fix/check headers
    'skip_header': [
    ],

    # don't fix/check text
    'skip_text': [
        'strings.json',
        'metadata.py',
        "settings.json"
    ],

    # don't fix/check path
    'skip_path': [
    ],
}

# the dict of header strings to match for replacement
DICT_HEADER = {
    'Project':  '__PP_NAME_BIG__',
    'Filename': '__PP_NAME_SMALL__',
    'Date':     '__PP_DATE__',
    "License":  '__PP_LICENSE__',
}

# the dict of README sections/tags to remove
# NB: we use __RM_ instead of __PP_ because some of these tags will stay in the
# README.md file and that would trigger an error in metadata.py
# we also don't want to ignore README.md becuse there ARE __PP_ tags in there
# that we want to replace
# NB: key is short project type(s)
# subkey is the command for fix_readme()
# subval is the comment to find in the README file
# anything between 'rm_delete_start' and 'rm_delete_end' will be deleted
# (including the tags themselves)
# any tag that starts with 'rm_delete_tag' will be deleted, but the contents
# will remain
DICT_README = {
    'mp': {
        'rm_delete_start':  '<!-- __RM_APP_START__ -->',
        'rm_delete_end':    '<!-- __RM_APP_END__ -->',
        'rm_delete_tag':    '<!-- __RM_MOD_',
    },
    'cg': {
        'rm_delete_start':  '<!-- __RM_MOD_START__ -->',
        'rm_delete_end':    '<!-- __RM_MOD_END__ -->',
        'rm_delete_tag':    '<!-- __RM_APP_',
    },
}

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by metadata.py (from misc/settings.json)
# NB: these are one-time seetings created by pyplate and should not be edited
g_dict_settings = {
    '__PP_NAME_BIG__':      '',  # PyPlate
    '__PP_NAME_SMALL__':    '',  # pyplate
    '__PP_AUTHOR__':        '',  # cyclopticnerve
    '__PP_EMAIL__':         '',  # cyclopticnerve@gmail.com
    '__PP_DATE__':          '',  # 12/08/2022
}

# settings that are only needed between functions in the current file

# the path to the project directory (no need to hold over for metadata.py)
# NB: the main reason we don't put this in g_dict_settings is that it will
# contain your home dir name
g_prj_dir = ''

# this setting is not needed for metadata so lets take it out
g_prj_type = ''


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

    # get info and copy template
    get_project_info()
    copy_template()

    # call recurse to do replacements in final project location
    recurse_and_fix(g_prj_dir)

    # do stuff to final dir after recurse
    do_extras()


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_project_info():
    """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        g_dict_settings and g_prj_dir.
    """

    # the settings dict (global b/c we will modify here)
    global g_dict_settings

    # the project dict (global b/c we will modify here)
    global g_prj_dir

    # the project dict (global b/c we will modify here)
    global g_prj_type

    # first get question
    str_prj = 'Projet type'

    # then get types
    arr_type = [f'({key}) {val[0]}' for (key, val) in DICT_TYPE.items()]
    str_type = ' | '.join(arr_type)
    str_in = f'{str_prj} [{str_type}]: '

    # sanity check
    type_prj = ''

    # loop forever until we get a valid type (or user presses Ctrl+C)
    while True:

        # build a project type string and ask what type of project
        type_prj = input(str_in)

        # check project type
        # first, is there an entry?
        if len(type_prj) > 0:

            # get first (or only) char and lowercase it
            type_prj = type_prj[0]
            type_prj = type_prj.lower()

            # get array of acceptable lowercase types
            arr_type_lower = [item.lower() for item in DICT_TYPE.keys()]

            # we got a valid type
            if type_prj in arr_type_lower:
                g_prj_type = type_prj
                break

    # sanity check
    dir_type = DICT_TYPE[type_prj][1]

    # loop forever until we get a valid name and path (or user presses Ctrl+C)
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

        # if name is valid, store name
        g_dict_settings['__PP_NAME_BIG__'] = info_name_big

        # then store path
        g_prj_dir = dir_prj
        break

    # calculate small name
    info_name_small = info_name_big.lower()
    g_dict_settings['__PP_NAME_SMALL__'] = info_name_small

    # set author/email (assumed from constants above)
    g_dict_settings['__PP_AUTHOR__'] = DICT_USER['PP_AUTHOR']
    g_dict_settings['__PP_EMAIL__'] = DICT_USER['PP_EMAIL']

    # calculate current date (format assumed from constants above)
    info_date = datetime.now().strftime(DICT_USER['PP_DATE_FMT'])
    g_dict_settings['__PP_DATE__'] = info_date


# ------------------------------------------------------------------------------
# Copy template files to final location
# ------------------------------------------------------------------------------
def copy_template():
    """
        Copy template files to final location

        Get files/folders from template and copy them to the project folder.
    """

    # create target folder
    os.makedirs(g_prj_dir)

    # create list of long dirs
    # add common
    lst_src = ['common']

    # add project type source
    dir_src = DICT_TYPE[g_prj_type][2]
    lst_src.append(dir_src)

    # NB: I tried this both ways:

    # 1. template/src/type/file
    # this made a cleaner tree, but an uglier code base
    # also i had to add an 'extras' folder for MANIFEST/pyproject to reduce
    # recursion/manually adding them
    # this also negated the option of combining them into a sigle loop

    # 2. template/type/src/file
    # this made the tree a little uglier, but made a cleaner code base
    # also the tree ends up reflecting the final project tree better, as
    # everything under the common folder ends up at the root level of the
    # project, and everything under the type dir alos ends up at the root level
    # of the project
    # this was also able to add everything into a single loop

    # lst_src is now ['common', project type src]
    for item in lst_src:

        # list each item in each folder in list_src
        path_in = os.path.join(DIR_TEMPLATE, item)
        items = os.listdir(path_in)

        # for each item in each folder
        for item in items:

            # build old path/new path
            path_from = os.path.join(path_in, item)
            path_to = os.path.join(g_prj_dir, item)

            # if it's a dir
            if os.path.isdir(path_from):

                # copy dir
                shutil.copytree(path_from, path_to)

            # if its not a dir
            else:

                # then copy file
                shutil.copy2(path_from, path_to)

# NB: the following commands are included in copy_template because their
# resulting files are part of the project, they are just empty to start
# whereas the stuff in do_extras MUST be initialzed AFTER the project exists

    # copy the 'starter kit' of requirements
    # NB: this is all the reqs collected while developing PyPlate
    # should be a good place to start developing a project in VSCode
    # also by copying from this project rather than hard-coding the list, it
    # will get updated every time the PyPlate project file is updated, making
    # it future-proof*
    # (* not guaranteed to be future-proof)
    # this is a file-to-file copy
    # NB: also note that these are the requirements for the venv, NOT the
    # requirements for running the resulting project (that's a task for another
    # day...)
    path_from = os.path.join(DIR_PYPLATE, 'requirements.txt')
    path_to = os.path.join(g_prj_dir, 'requirements.txt')
    shutil.copy2(path_from, path_to)

    # write DICT_BLACKLIST to conf file
    path_to = os.path.join(g_prj_dir, 'conf', 'blacklist.json')
    with open(path_to, 'w') as f:
        dict_blacklist = json.dumps(DICT_BLACKLIST, indent=4)
        f.write(dict_blacklist)

    # write g_dict_settings to conf file
    path_to = os.path.join(g_prj_dir, 'conf', 'settings.json')
    with open(path_to, 'w') as f:
        dict_settings = json.dumps(g_dict_settings, indent=4)
        f.write(dict_settings)


# ------------------------------------------------------------------------------
# Recursively scan folders/files for replace/rename functions
# ------------------------------------------------------------------------------
def recurse_and_fix(dir):
    """
        Recursively scans folders/files for replace/rename functions

        Parameters:
            dir: The directory to start recursively scanning from

        This is a recursive function to scan for folders/files under a given
        folder. It iterates over the contents of the 'dir' folder, checking if
        each item is a file or a folder. If it encounters a folder, it calls
        itself recursively, passing that folder as the parameter. If it
        encounters a file, it calls methods to do text replacement of headers,
        then other text. Finally it renames the file if the path contains a
        replacement key. Once all files are fixed, it will then bubble up to
        fix all folders.
    """

    # blacklist
    # remove all leading/trailing slashes
    # NB: these lists are explained in detail in the README file
    skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_all']]
    skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_file']]
    skip_header = [item.strip(os.sep)
                   for item in DICT_BLACKLIST['skip_header']]
    skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_text']]
    skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_path']]

    # get list of file names in dest dir (excluding skip_all)
    items = [item for item in os.listdir(dir) if item not in skip_all]
    for item in items:

        # put path back together
        path_item = os.path.join(dir, item)

        # if it's a dir
        if os.path.isdir(path_item):

            # recurse itself to find more files
            recurse_and_fix(path_item)

        else:

            # only open files we should be mucking in
            if item not in skip_file:

                # open file and get lines
                with open(path_item, 'r') as f:
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
                with open(path_item, 'w') as f:
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
    os.chdir(g_prj_dir)

    # add git folder
    cmd = 'git init'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # FIXME: no longer works
    # add venv dir
    # NB: use '.venv' to be compatible with VSCodium
    # cmd = 'python -m venv .venv'
    # cmd_array = shlex.split(cmd)
    # subprocess.run(cmd_array)

    # create tree
    path_tree = os.path.join(g_prj_dir, 'misc', 'tree.txt')
    with open(path_tree, 'w') as f:
        cmd = 'tree --dirsfirst --noreport'
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
        Replaces header text inside files

        Parameters:
            lines: The list of file lines for replacing header text

        Returns:
            The list of replaced lines in the file

        This is a function to replace header text inside a file. Given a list of
        file lines, it iterates the list line by line, replacing header text as
        it goes. When it is done, it returns lhe list of lines. This replaces
        the __PP_.. stuff inside headers.
        Using this method, we preserve any right-aligned text in each header
        row. See the headers in my files for an example. Adapting this function
        to your style of header should be easy using the regex, and modifying
        DICT_HEADER to suit. You can use any key in g_dict_settings as a
        replacement.
    """

    # for each line in array
    for i in range(0, len(lines)):

        # for each repl line
        for key, val in DICT_HEADER.items():

            # pattern
            pattern = (
                r'(# |<!-- )'
                rf'({key})'
                r'( *: )'
                rf'({val})'
                r'([^ ]*)'
                r'( *)'
                r'(.*)'
            )
            res = re.search(pattern, lines[i])

            if res:

                # get the new value from settings
                rep = g_dict_settings[val]

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
        Replaces text inside files

        Parameters:
            lines: The list of file lines for replacing text

        Returns:
            The list of replaced lines in the file

        This is a function to replace text inside a file. Given a list of file
        lines, it iterates the list line by line, replacing text as it goes.
        When it is done, it returns the list of lines. This replaces the
        __PP_... stuff inside the file, excluding headers (which are already
        handled).
    """

    # for each line in array
    for i in range(0, len(lines)):

        # replace text in line
        for key in g_dict_settings.keys():
            if key in lines[i]:
                lines[i] = lines[i].replace(key, g_dict_settings[key])

    # save file with replacements
    return lines


# ------------------------------------------------------------------------------
# Remove unnecessary parts of the README file
# ------------------------------------------------------------------------------
def _fix_readme(lines):
    """
        Removes unnecessary parts of the README file

        Parameters:
            lines: The list of file lines for removing README text

        Returns:
            The list of replaced lines in the file

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as Module/Package or
        CLI/GUI.
    """

    # NB: the strategy here is to go through the full README and only copy lines
    # that are
    # 1) not in any block or
    # 2) in the block we want
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

    # what to ignore in the text
    for key in DICT_README.keys():
        if g_prj_type in key:

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
        Renames folders/files in the project

        Parameters:
            path: The path to the folder/file for renaming

        Returns:
            The new path for the specified folder/file

        This is a function to rename folders/files. Given a path to a
        folder/file, it renames the path by replacing items in the
        g_dict_settings keys with their appropriate replacements.
    """

    # split the path into everything up to last part, and last part itself
    dir_old, file_old = os.path.split(path)

    # replace dunders in last path component
    for key in g_dict_settings.keys():
        file_old = file_old.replace(key, g_dict_settings[key])

    # put new name back with the 'up to last' part
    path_new = os.path.join(dir_old, file_old)

    # return the new path name
    return path_new


# ------------------------------------------------------------------------------
# Check project name for allowed characters
# ------------------------------------------------------------------------------
def _fix_name(name):
    """
        Checks project name for allowed characters

        Parameters:
            name: The name to check for allowed characters

        Returns:
            Whether the name is valid to use

        This function checks the passed name for four criteria:
        1. non-blank name
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
