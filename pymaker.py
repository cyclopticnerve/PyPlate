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
# (~/Documents/Projects/Python/PyPlate)
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

# this is the dir where the template files are located rel to the script
# (~/Documents/Projects/Python/PyPlate/template)
TEMPLATE_DIR = os.path.abspath(f'{CURR_DIR}/template')

# this is the user entered base dir for python stuff
# TODO: this may change on user input
BASE_DIR = os.path.abspath(f'{CURR_DIR}/../')

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the settings to use to create the project
settings = {
    'project_type':             '',
    'project_type_dir':         '',
    'project_dir':              '',
    'project_reps': {
        '__CN_BIG_NAME__':      '',
        '__CN_SMALL_NAME__':    '',
        '__CN_DATE__':          '',
        '__CN_VERSION__':       '0.1.0',
        '__CN_SHORT_DESC__':    '',
        '__CN_KEYWORDS__':      [
        ],
        '__CN_PY_DEPS__':       [
        ],
        '__CN_GUI_EXEC__':      '',
        '__CN_GUI_ICON__':      ''
    },
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
    fix_readme()
    fix_toml()
    add_in()


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_info():

    """
        Get project info

        Asks the user for project info, such as type, name, keywords, etc.
    """

    global settings

    # ask what type of project
    prj_type = input('Type of project: [M]odule|[P]ackage|[C]LI|[G]UI: ')
    if prj_type == '':
        exit()
    prj_type = prj_type.lower()[0]
    if prj_type not in 'mpcg':
        exit()
    settings['project_type'] = prj_type

    # ask for project name
    prj_name = input('Project name (Capitalized): ')
    if prj_name == '':
        exit()
    settings['project_reps']['__CN_BIG_NAME__'] = prj_name

    # calculate project path
    if settings['project_type'] in 'mp':
        settings['project_type_dir'] = os.path.join(BASE_DIR, 'Libs')
    else:
        settings['project_type_dir'] = os.path.join(BASE_DIR, 'Apps')

    # check if project folder exists
    settings['project_dir'] = \
        os.path.join(settings['project_type_dir'], prj_name)
    if os.path.exists(settings['project_dir']):
        print('Project already exists')
        exit()

    # calculate small name
    lower = prj_name.lower()
    settings['project_reps']['__CN_SMALL_NAME__'] = lower

    # calculate current date
    prj_date = datetime.now()
    settings['project_reps']['__CN_DATE__'] = prj_date.strftime('%m/%d/%Y')

    # get short description
    prj_desc = input('Short description of project: ')
    settings['project_reps']['__CN_SHORT_DESC__'] = prj_desc

    # get keywords/dependencies
    if settings['project_type'] in 'mp':
        get_info_keys()
        get_info_deps()

    # calculate gui location
    settings['project_reps']['__CN_GUI_EXEC__'] = \
        f'{USER}/.cyclopticnerve/{lower}/gui/{lower}_gui.py'

    # calculuate icon location
    settings['project_reps']['__CN_GUI_ICON__'] = \
        f'{USER}/.local/share/icons/cyclopticnerve/{lower}.png'


# ------------------------------------------------------------------------------
# Get project keywords
# ------------------------------------------------------------------------------
def get_info_keys():

    """
        Get project keywords

        Asks the user for project keywords.
    """

    global settings

    prj_keys = input('Keywords (semicolon seperated, optional): ')
    if prj_keys != '':
        prj_keys_list = prj_keys.split(';')
        for item in prj_keys_list:
            settings['project_reps']['__CN_KEYWORDS__'].append(item)


# ------------------------------------------------------------------------------
# Get project dependencies
# ------------------------------------------------------------------------------
def get_info_deps():

    """
        Get project dependencies

        Asks the user for project dependencies.
    """

    global settings

    prj_deps = input('Dependencies (semicolon seperated, optional): ')
    if prj_deps != '':
        prj_deps_list = prj_deps.split(';')
        for item in prj_deps_list:
            settings['project_reps']['__CN_PY_DEPS__'].append(item)


# ------------------------------------------------------------------------------
# Copy new project and remove unneccesary files
# ------------------------------------------------------------------------------
def copy_and_prune():

    """
        Copy new project and remove unneccesary files

        Copy all template files/folders to the new location, then remove the
        files/folders not used for the type of project we are creating.
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
        os.remove('src/__main__.py')

        os.remove('tests/import_test_pkg.py')

        os.remove('install.py')
        os.remove('uninstall.py')

    # remove for package
    elif (settings['project_type'] == 'p'):
        shutil.rmtree('gui', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___app.py')
        os.remove('src/__CN_SMALL_NAME___mod.py')
        os.remove('src/__init__.py')
        os.remove('src/__main__.py')

        os.remove('tests/import_test_mod.py')

        os.remove('install.py')
        os.remove('uninstall.py')

    # remove for CLI
    elif (settings['project_type'] == 'c'):
        shutil.rmtree('gui', ignore_errors=True)

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___mod.py')
        os.remove('src/__init__.py')

        os.remove('tests/import_test_mod.py')
        os.remove('tests/import_test_pkg.py')

        os.remove('MANIFEST.in')
        os.remove('pyproject.toml')
        os.remove('requirements.txt')

    # remove for GUI
    elif (settings['project_type'] == 'g'):

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME___mod.py')
        os.remove('src/__init__.py')

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

    # the replacement dict
    reps = settings['project_reps']

    # returns only final path part for each entry
    lst = os.listdir(path)

    # for each file/folder
    for item in lst:

        # put path back together
        old_path = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(old_path):

            # always skip misc folder (never replace/rename)
            if not item == 'misc':

                # recurse itself to find more files
                recurse_rename(old_path)

        # for each replacement key
        for key in reps.keys():

            # skip keywords list
            if not isinstance(reps[key], list):

                # if file/folder name contains replaceable item
                if key in item:

                    # do the string replace
                    new_name = item.replace(key, reps[key])

                    # remove trailing identifiers
                    new_name = new_name.replace('_app', '')
                    new_name = new_name.replace('_mod', '')

                    # create new path
                    new_path = os.path.join(path, new_name)

                    # do the actual rename
                    os.rename(old_path, new_path)


# ------------------------------------------------------------------------------
# Recursive function for replacing text inside files
# ------------------------------------------------------------------------------
def recurse_replace(path):

    """
        Recursive function for replacing text inside files

        Paramaters:
            path [string]: the file to replace text in

        This is a recursive function to replace text inside a file. Given a
        specific file, it iterates the file line by line, replacing test as it
        goes. When it is done, it saves the file to disk.
    """

    # the replacement dict
    reps = settings['project_reps']

    # returns only final path part for each entry
    lst = os.listdir(path)

    # for each file/folder
    for item in lst:

        # put path back together
        old_path = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(old_path):

            # always skip misc folder (never replace/rename)
            if not item == 'misc':

                # recurse itself to find more files
                recurse_replace(old_path)

        # it's a file
        else:

            # do header replacement

            # do some fancy header replacement bullshit
            line_start = {
                '# Project : ':     '__CN_BIG_NAME__',
                '# Filename: ':     '__CN_SMALL_NAME__',
                '# Date    : ':     '__CN_DATE__',
                '<!-- Project : ':  '__CN_BIG_NAME__',
                '<!-- Filename: ':  '__CN_SMALL_NAME__',
                '<!-- Date    : ':  '__CN_DATE__'
            }
            line_end = {
                '# Project : ':     '/          \\ ',
                '# Filename: ':     '|     ()     |',
                '# Date    : ':     '|            |',
                '<!-- Project : ':  '/          \\  -->',
                '<!-- Filename: ':  '|     ()     | -->',
                '<!-- Date    : ':  '|            | -->'
            }

            # open file
            with open(old_path) as file:
                data = file.readlines()

            # for line in data:
            for i in range(0, len(data)):

                # for each key, build a new string
                for key in line_start.keys():
                    if data[i].strip().startswith(key):
                        rep = reps[line_start[key]]
                        spaces = 80 - len(key) - len(rep) - len(line_end[key])
                        spaces_str = ' ' * spaces
                        data[i] = f'{key}{rep}{spaces_str}{line_end[key]}\n'

            # save file with header replacements
            with open(old_path, 'w') as file:
                file.writelines(data)

            # do regular text replacement

            # open file as text lines
            with open(old_path) as file:
                data = file.read()

            # for each key, do replace
            for key in reps.keys():

                # skip keywords list
                if not isinstance(reps[key], list):
                    data = data.replace(key, reps[key])

            # save file with replacements
            with open(old_path, 'w') as file:
                file.write(data)


# ------------------------------------------------------------------------------
# Cleans out the unneccessry parts of the README file
# ------------------------------------------------------------------------------
def fix_readme():

    """
        Cleans out the unneccessry parts of the README file

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as module/package or
        CLI/GUI.
    """

    # path to project
    dir = settings['project_dir']
    path = os.path.join(dir, 'README.md')

    # what type of project are we creating?
    project_type = settings['project_type']

    # just a boolean flag to say if we are kajiggering
    in_it = False

    # where to put the needed lines
    new_data = []

    # what to look for in the text
    start_str = '<!-- __CN_'
    end_str = start_str
    if project_type in 'mp':
        start_str += 'APP_START__ -->'
        end_str += 'APP_END__ -->'
    else:
        start_str += 'MOD_START__ -->'
        end_str += 'MOD_END__ -->'

    # get the file data
    with open(path) as file:
        data = file.readlines()

    # for each line, check if we are in a block
    for line in data:
        if line.startswith(start_str):
            in_it = True
        elif line.startswith(end_str):
            in_it = False

        # not a valid data block, just copy it
        if not in_it:
            if not line.startswith('<!-- __CN_'):
                new_data.append(line)

    # save the kajiggered data line
    with open(path, 'w') as file:
        file.writelines(new_data)


# ------------------------------------------------------------------------------
# Replace keywords in toml file
# ------------------------------------------------------------------------------
def fix_toml():

    """
        Replace keywords in toml file

        This function replaces the 'keywords' array in pyproject.toml with the
        keywords that were entered in the startup section of the program.
    """

    # path to project/toml (exit if no file)
    dir = settings['project_dir']
    path = os.path.join(dir, 'pyproject.toml')
    if not os.path.exists(path):
        return

    # build a keyword string
    new_str = ''
    for item in settings['project_reps']['__CN_KEYWORDS__']:
        new_str += '\"' + item + '\",\n\t'

    # chop off last comma/newline
    new_str = new_str[:-3]

    # get the file data
    with open(path) as file:
        data = file.read()

    # replace the string in the file
    data = data.replace('\"__CN_KEYWORDS__\"', new_str)

    # save the file
    with open(path, 'w') as file:
        file.write(data)

    # build a deps string
    new_str = ''
    for item in settings['project_reps']['__CN_PY_DEPS__']:
        new_str += '\"' + item + '\",\n\t'

    # chop off last comma/newline
    new_str = new_str[:-3]

    # get the file data
    with open(path) as file:
        data = file.read()

    # replace the string in the file
    data = data.replace('\"__CN_PY_DEPS__\"', new_str)

    # save the file
    with open(path, 'w') as file:
        file.write(data)


# ------------------------------------------------------------------------------
# Add venv and .git folders to new project
# ------------------------------------------------------------------------------
def add_in():

    """
        Add venv and .git folders to new project

        Adds a .git folder (repository) and a venv (virtual environment) folder
        to the project, and sets them up as necessary.
    """

    # make sure we are in current proj path w/chdir
    dir = settings['project_dir']
    os.chdir(dir)

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
