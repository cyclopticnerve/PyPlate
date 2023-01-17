#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pymaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: Module/Package: get rid of import tests after ensuring __init__.py works
# as expected
# TODO: CLI/GUI: what files to add to install.py when copying
# (i.e. apps/cli need to copy files to ~/.cyclopticnerve/proj/app and
# !/.cyclopticnerve/proj/app/gui)

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
import json
import os
import shlex
import shutil
import subprocess

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# this is the dir where the script is being run from
# (~/Documents/Projects/Python/PyPlate/src/)
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

# these are the default dirs for project location
# (~/Documents/Projects/Python/) (above PyPlate)
BASE_DIR = os.path.abspath(f'{CURR_DIR}/../../')

# the default date format to use in headers
DATE_FMT = '%Y-%m-%d'

# this is the default dir where the template files are located rel to the script
# (~/Documents/Projects/Python/PyPlate/template/)
TEMPLATE_DIR = os.path.abspath(f'{CURR_DIR}/../template')

# default autthor is user's login name
AUTHOR = os.getlogin()

# get the current user home dir
USER_DIR = os.path.expanduser('~')

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default conf settings for project paths
dict_conf = {
    'conf_base': BASE_DIR,
    'conf_libs': '',
    'conf_apps': '',
    'conf_date': DATE_FMT,
    'conf_auth': AUTHOR,
    'conf_mail': '',
    'conf_lcns': ''
}

# the default settings to use to create the project
dict_proj = {
    'proj_type':             '',  # m (Module), p (Package), c (CLI), g (GUI)
    'proj_dir':              '',  # conf_base/conf_libs/Foo or \
                                  # conf_base/conf_apps/Foo
    'proj_reps': {
        '__CN_BIG_NAME__':   '',  # Foo
        '__CN_SMALL_NAME__': '',  # foo
        '__CN_DATE__':       '',  # conf_date (2022-12-08)
        '__CN_AUTHOR__':     '',  # conf_auth
        '__CN_LICENSE__':    '',  # conf_lcns
        '__CN_GUI_EXEC__':   '',  # foo_gui.py
        '__CN_GUI_ICON__':   ''   # foo.png
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
    get_dict_conf()
    get_dict_proj()
    copy_and_prune()
    recurse_rename(dict_proj['proj_dir'])
    recurse_replace(dict_proj['proj_dir'])
    add_git_venv()


# ------------------------------------------------------------------------------
# Get conf settings
# ------------------------------------------------------------------------------
def get_dict_conf():

    """
        Get conf settings

        Get already saved settings from user (or create defaults if not exists)
    """

    global dict_conf

    # get conf path
    conf_path = os.path.join(CURR_DIR, 'pymaker.json')

    # create file if necessary
    if not os.path.exists(conf_path):
        with open(conf_path, 'w') as file:
            file.write(json.dumps(dict_conf, indent=4))
            print('Edit the pymaker.json file before running. See README.md')
            exit()

    # read conf dir
    with open(conf_path) as file:
        dict_conf = json.load(file)

    # apply default value if key is empty
    if dict_conf['conf_base'] == '':
        dict_conf['conf_base'] = BASE_DIR
    if dict_conf['conf_date'] == '':
        dict_conf['conf_date'] = DATE_FMT
    if dict_conf['conf_auth'] == '':
        dict_conf['conf_auth'] = AUTHOR


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_dict_proj():

    """
        Get project info

        Asks the user for project info, such as type, name, etc.
    """

    global dict_proj

    # ask what type of project
    proj_type = input('Type of project: [M]odule | [P]ackage | [C]LI | [G]UI: ')
    proj_type = proj_type.strip()
    if proj_type == '':
        exit()
    proj_type = proj_type.lower()[0]
    if proj_type not in 'mpcg':
        exit()
    dict_proj['proj_type'] = proj_type

    # calculate project subdir
    if dict_proj['proj_type'] in 'mp':
        prj_sub_dir = dict_conf['conf_libs']
    else:
        prj_sub_dir = dict_conf['conf_apps']

    # ask for project name
    prj_name_big = input('Project name: ')
    prj_name_big = prj_name_big.strip()
    if prj_name_big == '':
        exit()
    prj_name_big = prj_name_big.capitalize()
    dict_proj['proj_reps']['__CN_BIG_NAME__'] = prj_name_big

    # calculate final proj location
    conf_base = dict_conf['conf_base']
    dict_proj['proj_dir'] = os.path.join(conf_base, prj_sub_dir, prj_name_big)

    # check if project folder exists
    tmp_path = dict_proj['proj_dir']
    if os.path.exists(tmp_path):
        print(f'Project {tmp_path} already exists')
        exit()

    # calculate small name
    prj_name_small = prj_name_big.lower()
    dict_proj['proj_reps']['__CN_SMALL_NAME__'] = prj_name_small

    # calculate current date
    prj_date = datetime.now().strftime(dict_conf['conf_date'])
    dict_proj['proj_reps']['__CN_DATE__'] = prj_date

    # get author
    conf_auth = dict_conf['conf_auth']
    dict_proj['proj_reps']['__CN_AUTHOR__'] = conf_auth

    # get license
    conf_lcns = dict_conf['conf_lcns']
    dict_proj['proj_reps']['__CONF_LICENSE__'] = conf_lcns

    # calculate gui location
    dict_proj['proj_reps']['__CN_GUI_EXEC__'] = \
        f'{USER_DIR}/.{conf_auth}/{prj_name_small}/gui/{prj_name_small}_gui.py'

    # calculuate icon location
    dict_proj['proj_reps']['__CN_GUI_ICON__'] = \
        f'{USER_DIR}/.local/share/icons/{conf_auth}/{prj_name_small}.png'


# ------------------------------------------------------------------------------
# Copy new project and remove unneccesary files
# ------------------------------------------------------------------------------
def copy_and_prune():

    """
        Copy new project and remove unneccesary files

        Copy all template files/folders to the new location, then remove the
        files/folders not used for the type of project we are creating. This is
        easier than only copying files we DO need.
    """

    # copy template to new project
    shutil.copytree(TEMPLATE_DIR, dict_proj['proj_dir'])

    # switch to project path
    os.chdir(dict_proj['proj_dir'])

    # remove for module
    if (dict_proj['proj_type'] == 'm'):

        shutil.rmtree('gui', ignore_errors=True)

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)
        os.remove('src/__CN_SMALL_NAME___app.py')

        os.remove('tests/import_test_pkg.py')

        os.remove('install.py')
        os.remove('uninstall.py')

    # remove for package
    elif (dict_proj['proj_type'] == 'p'):
        shutil.rmtree('gui', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___app.py')
        os.remove('src/__CN_SMALL_NAME___mod.py')

        os.remove('tests/import_test_mod.py')

        os.remove('install.py')
        os.remove('uninstall.py')

    # remove for CLI
    elif (dict_proj['proj_type'] == 'c'):
        shutil.rmtree('gui', ignore_errors=True)

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___mod.py')

        os.remove('tests/import_test_mod.py')
        os.remove('tests/import_test_pkg.py')

        os.remove('MANIFEST.in')
        os.remove('pyproject.toml')
        os.remove('requirements.txt')

    # remove for GUI
    elif (dict_proj['proj_type'] == 'g'):

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___mod.py')

        os.remove('tests/import_test_mod.py')
        os.remove('tests/import_test_pkg.py')

        os.remove('MANIFEST.in')
        os.remove('pyproject.toml')
        os.remove('requirements.txt')


# ------------------------------------------------------------------------------
# Recursive function for renaming files/folders
# ------------------------------------------------------------------------------
def recurse_rename(path):

    """
        Recursive function for renaming files/folders

        Paramaters:
            path [string]: the folder to start recursively renaming from

        This is a recursive function to rename files under a given folder. It
        iterates over the contents of the folder, renaming files as it goes. If
        it encounters a folder, it calls itself recursively, passing that folder
        as the parameter. Once all files are renamed, it will then bubble up to
        rename all folders.
    """

    # don't rename these dirs or contents
    skip_dirs = ['misc']

    # the replacement dict
    reps = dict_proj['proj_reps']

    # returns only final path part for each entry
    lst = os.listdir(path)

    # for each file/folder
    for item in lst:

        # put path back together
        item_path = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(item_path):

            # always skip misc folder (never replace/rename)
            if item not in skip_dirs:

                # recurse itself to find more files
                recurse_rename(item_path)

        # for each replacement key
        for key in reps.keys():

            # check to make sure we should do a replacement
            # (or if it has been done already)
            if key in item:

                # do the string replace
                new_item = item.replace(key, reps[key])

                # remove trailing identifiers
                new_item = new_item.replace('_app', '')
                new_item = new_item.replace('_mod', '')

                # create new path
                new_path = os.path.join(path, new_item)

                # do the actual rename
                os.rename(item_path, new_path)


# ------------------------------------------------------------------------------
# Recursive function for replacing text inside files
# ------------------------------------------------------------------------------
def recurse_replace(path):

    """
        Recursive function for replacing text inside files

        Paramaters:
            path [string]: the file to replace text in

        This is a recursive function to replace text inside a file. Given a
        specific file, it iterates the file line by line, replacing text as it
        goes. When it is done, it saves the file to disk. This replaces the
        __CN_... stuff from the settings inside the file, as headers are
        delegated to the next function (recurse_replace_headers).
    """

    # don't rename these dirs or contents
    skip_dirs = ['misc']

    # the replacement dict
    reps = dict_proj['proj_reps']

    # returns only final path part for each entry
    lst = os.listdir(path)

    # for each file/folder
    for item in lst:

        # put path back together
        item_path = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(item_path):

            # always skip misc folder (never replace/rename)
            if item not in skip_dirs:

                # recurse itself to find more files
                recurse_replace(item_path)

        # if it's a file
        else:

            # replace headers in file
            recurse_replace_headers(item_path)

            # open file as text line array
            with open(item_path) as file:
                data = file.readlines()

            # for each line in array
            for i in range(0, len(data)):

                # replace text in line
                for key in reps.keys():
                    data[i] = data[i].replace(key, reps[key])

            # NB: i think file.read() strips the string, so we lose the
            # trailing blank line, which is part of my styling
            # so add it back in before saving
            data.append('\n')

            # save file with replacements
            with open(item_path, 'w') as file:
                file.writelines(data)

            # readme needs extra handling
            if item == 'README.md':
                fix_readme(item_path)


# ------------------------------------------------------------------------------
# Recursive function for replacing header text inside files
# ------------------------------------------------------------------------------
def recurse_replace_headers(path):

    """
        Recursive function for replacing header text inside files

        Paramaters:
            path [string]: the file to replace text in

        This is a recursive function to replace header text inside a file. Given
        a specific file, it iterates the file line by line, replacing header
        text as it goes. When it is done, it saves the file to disk. This
        replaces the __CN_.. stuff inside headers, while the previous function
        (recurse_replace) does the stuff inside the body of the file.
    """

    # the replacement dict
    reps = dict_proj['proj_reps']

    # set up an ugly array of header stuff
    line_rep = [
        ['# Project : ', '__CN_BIG_NAME__',   '/          \\ '],
        ['# Filename: ', '__CN_SMALL_NAME__', '|     ()     |'],
        ['# Date    : ', '__CN_DATE__',       '|            |'],
        ['# Author  : ', '__CN_AUTHOR__',     '|   \\____/   |'],
        ['# License : ', '__CN_LICENSE__',    ' \\          / '],
        ['<!-- Project : ', '__CN_BIG_NAME__',   '/          \\  -->'],
        ['<!-- Filename: ', '__CN_SMALL_NAME__', '|     ()     | -->'],
        ['<!-- Date    : ', '__CN_DATE__',       '|            | -->'],
        ['<!-- Author  : ', '__CN_AUTHOR__',     '|   \\____/   | -->'],
        ['<!-- License : ', '__CN_LICENSE__',    ' \\          /  -->'],
    ]

    # open file as text line array
    with open(path) as file:
        data = file.readlines()

    # for each line in array
    for i in range(0, len(data)):

        # for each repl line
        for item in line_rep:

            # build start str
            key = item[0] + item[1]

            # if the key is in the line
            if key in data[i]:

                # replace the dunder
                rep = reps[item[1]]

                # calculate spaces
                spaces = 80 - (len(item[0]) + len(rep) + len(item[2]))
                spaces_str = ' ' * spaces

                # create replacement string (with newline!!!)
                rep_str = f'{item[0]}{rep}{spaces_str}{item[2]}\n'

                # replace text in line
                data[i] = rep_str

    # save file with header replacements
    with open(path, 'w') as file:
        file.writelines(data)


# ------------------------------------------------------------------------------
# Cleans out the unneccessry parts of the README file
# ------------------------------------------------------------------------------
def fix_readme(path):

    """
        Cleans out the unneccesary parts of the README file

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as module/package or
        CLI/GUI.
    """

    # NB: the strategy here is to go through the full README and only copy lines
    # that are 1) not in any block or 2) in the block we want
    # the most efficient way to do this is to have an array that recieves wanted
    # lines, then save that array to a file

    # what type of project are we creating?
    proj_type = dict_proj['proj_type']

    # just a boolean flag to say if we are kajiggering
    # if True, we are in a block we don't want to copy
    in_it = False

    # NB: we use a new array vs. in-situ replacement here b/c we are removing
    # A LOT OF LINES, which in-situ would result in A LOT OF BLANK LINES and
    # while that would look *ok* in the reulting README, looks UGLY in the
    # source code. so we opt for not copying those lines.

    # where to put the needed lines
    new_data = []

    # what to look for in the text
    if proj_type in 'mp':
        start_str = '<!-- __CN_APP_START__ -->'
        end_str = '<!-- __CN_APP_END__ -->'
        ignore_str = '<!-- __CN_MOD_'
    else:
        start_str = '<!-- __CN_MOD_START__ -->'
        end_str = '<!-- __CN_MOD_END__ -->'
        ignore_str = '<!-- __CN_APP_'

    # get the file data
    with open(path) as file:
        data = file.readlines()

    # for each line
    for line in data:

        # check if we are in a block
        if start_str in line:
            in_it = True

        # it's a valid data block, just copy it
        if not in_it:

            # ignore block wrapper lines
            if ignore_str not in line:
                new_data.append(line)

        # check if we have left the block
        if end_str in line:
            in_it = False

    # save the kajiggered data line
    with open(path, 'w') as file:
        file.writelines(new_data)


# ------------------------------------------------------------------------------
# Add venv and .git folders to new project
# ------------------------------------------------------------------------------
def add_git_venv():

    """
        Add .git and venv folders to new project

        Adds a .git folder (repository) and a venv (virtual environment) folder
        to the project, and sets them up as necessary.
    """

    # make sure we are in current proj path w/chdir
    os.chdir(dict_proj['proj_dir'])

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
