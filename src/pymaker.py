#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pymaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: get path to template
# TODO: get path to base python projects dir

# TODO: what files to add to install.py when copying
# (i.e. apps/cli need to copy files to ~/.cyclopticnerve/proj/app and
# !/.cyclopticnerve/proj/app/gui)

# TODO: get rid of import tests after ensuring __init__.py works as expected

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
from datetime import datetime
import os
import shlex
import shutil
import subprocess

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# get the current user name
USER = os.path.expanduser('~')

# this is the dir where the script is being run from
# (~/Documents/Projects/Python/PyPlate/src/)
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

# this is the dir where the template files are located rel to the script
# (~/Documents/Projects/Python/PyPlate/template/)
TEMPLATE_DIR = os.path.abspath(f'{CURR_DIR}/../template')

# this is the user entered base dir for python stuff
# (~/Documents/Projects/Python/)
# TODO: this may change on user input
BASE_DIR = os.path.abspath(f'{CURR_DIR}/../../')

# subdirs for different types of projects
APPS_DIR = os.path.join(BASE_DIR, 'Apps')
LIBS_DIR = os.path.join(BASE_DIR, 'Libs')

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the settings to use to create the project
settings = {
    'project_type':             '',  # m (Module), p (Package), c (CLI), g (GUI)
    'project_dir':              '',  # /Libs/Test/ or /Apps/Test/
    'project_reps': {
        '__CN_BIG_NAME__':      '',  # Test
        '__CN_SMALL_NAME__':    '',  # test
        '__CN_DATE__':          '',  # MM/DD/YYYY
        '__CN_SHORT_DESC__':    '',  # 'A simple program to foo your bar'
        '__CN_GUI_EXEC__':      '',  # foo_gui.py
        '__CN_GUI_ICON__':      ''   # foo_gui.png
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
    get_info()
    copy_and_prune()
    recurse_rename(settings['project_dir'])
    recurse_replace(settings['project_dir'])
    # add_git_venv()


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_info():

    """
        Get project info

        Asks the user for project info, such as type, name, etc.
    """

    global settings

    # ask what type of project
    prj_type = input('Type of project: [M]odule | [P]ackage | [C]LI | [G]UI: ')
    prj_type = prj_type.strip()
    if prj_type == '':
        exit()
    prj_type = prj_type.lower()[0]
    if prj_type not in 'mpcg':
        exit()
    settings['project_type'] = prj_type

    # ask for project name
    prj_name_big = input('Project name: ')
    prj_name_big = prj_name_big.strip()
    if prj_name_big == '':
        exit()
    prj_name_big = prj_name_big.capitalize()
    settings['project_reps']['__CN_BIG_NAME__'] = prj_name_big

    # calculate project path
    if settings['project_type'] in 'mp':
        type_dir = LIBS_DIR
    else:
        type_dir = APPS_DIR

    # check if project folder exists
    settings['project_dir'] = os.path.join(type_dir, prj_name_big)
    if os.path.exists(settings['project_dir']):
        print(f'Project {settings["project_dir"]} already exists')
        exit()

    # calculate small name
    prj_name_small = prj_name_big.lower()
    settings['project_reps']['__CN_SMALL_NAME__'] = prj_name_small

    # calculate current date
    prj_date = datetime.now().strftime('%m/%d/%Y')
    settings['project_reps']['__CN_DATE__'] = prj_date

    # get short description
    prj_desc = input('Short description of project (Optional): ')
    prj_desc = prj_desc.strip()
    settings['project_reps']['__CN_SHORT_DESC__'] = \
        prj_desc.capitalize()

    # calculate gui location
    settings['project_reps']['__CN_GUI_EXEC__'] = \
        f'{USER}/.cyclopticnerve/{prj_name_small}/gui/{prj_name_small}_gui.py'

    # calculuate icon location
    settings['project_reps']['__CN_GUI_ICON__'] = \
        f'{USER}/.local/share/icons/cyclopticnerve/{prj_name_small}.png'


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
    shutil.copytree(TEMPLATE_DIR, settings['project_dir'])

    # switch to project path
    os.chdir(settings['project_dir'])

    # remove for module
    if (settings['project_type'] == 'm'):

        shutil.rmtree('gui', ignore_errors=True)

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)
        os.remove('src/__CN_SMALL_NAME___app.py')

        os.remove('tests/import_test_pkg.py')

        os.remove('install.py')
        os.remove('uninstall.py')

    # remove for package
    elif (settings['project_type'] == 'p'):
        shutil.rmtree('gui', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___app.py')
        os.remove('src/__CN_SMALL_NAME___mod.py')

        os.remove('tests/import_test_mod.py')

        os.remove('install.py')
        os.remove('uninstall.py')

    # remove for CLI
    elif (settings['project_type'] == 'c'):
        shutil.rmtree('gui', ignore_errors=True)

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___mod.py')

        os.remove('tests/import_test_mod.py')
        os.remove('tests/import_test_pkg.py')

        os.remove('MANIFEST.in')
        os.remove('pyproject.toml')
        os.remove('requirements.txt')

    # remove for GUI
    elif (settings['project_type'] == 'g'):

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
    reps = settings['project_reps']

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
    reps = settings['project_reps']

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
    reps = settings['project_reps']

    # set up an ugly array of header stuff
    line_rep = [
        ['# Project : ', '__CN_BIG_NAME__',   '/          \\ '],
        ['# Filename: ', '__CN_SMALL_NAME__', '|     ()     |'],
        ['# Date    : ', '__CN_DATE__',       '|            |'],
        ['<!-- Project : ', '__CN_BIG_NAME__',   '/          \\  -->'],
        ['<!-- Filename: ', '__CN_SMALL_NAME__', '|     ()     | -->'],
        ['<!-- Date    : ', '__CN_DATE__',       '|            | -->']
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
    prj_type = settings['project_type']

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
    if prj_type in 'mp':
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
    os.chdir(settings['project_dir'])

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
        is invoked from the command line, e.g. "python pymaker.py".
    """

    main()

# -)
