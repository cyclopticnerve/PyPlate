#!/usr/bin/env python
# ------------------------------------------------------------------------------
# Project : Template                                                  /          \
# Filename: pymaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: waht files to add to install files when copying
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
# Globals
# ------------------------------------------------------------------------------
user = os.path.expanduser('~')
template_path = f'{user}/Documents/Projects/Python/Tools/Template'
settings = {
    'project_type':             '',
    'project_path':             '',
    'project_reps': {
        '__CN_BIG_NAME__':      '',
        '__CN_SMALL_NAME__':    '',
        '__CN_DATE__':          '',
        '__CN_VERSION__':       '0.1.0',
        '__CN_SHORT_DESC__':    '',
        '__CN_KEYWORDS__':      [
        ],
        '__CN_PY_REQS':         [
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
    get_info()
    copy_and_prune()
    rename()
    replace_text()
    fix_readme()
    fix_toml()
    add_in()


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_info():

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
        settings['project_path'] = \
            f'{user}/Documents/Projects/Python/Libs/{prj_name}'
    else:
        settings['project_path'] = \
            f'{user}/Documents/Projects/Python/Apps/{prj_name}'

    # check if project folder exists
    if os.path.exists(settings['project_path']):
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

    # get keywords
    prj_keys = input('Keywords (semicolon seperated): ')
    if prj_keys != '':
        prj_keys_list = prj_keys.split(';')
        for item in prj_keys_list:
            settings['project_reps']['__CN_KEYWORDS__'].append(item)

    # calculate gui location
    settings['project_reps']['__CN_GUI_EXEC__'] = \
        f'{user}/.cyclopticnerve/{lower}/{lower}_gui.py'

    # calculuate icon location
    settings['project_reps']['__CN_GUI_ICON__'] = \
        f'{user}/.local/share/icons/cyclopticnerve/{lower}.png'


# ------------------------------------------------------------------------------
# Copy new project and remove unneccesary files
# ------------------------------------------------------------------------------
def copy_and_prune():

    # copy template to new project
    shutil.copytree(template_path, settings['project_path'])

    # switch to project path
    os.chdir(settings['project_path'])

    # remove ancillaries
    shutil.rmtree('.git', ignore_errors=True)
    shutil.rmtree('venv', ignore_errors=True)

    # delete/remane dups
    os.remove('gitignore')
    os.rename('.gitignore_template', '.gitignore')

    os.remove('CHNAGELOG.md')
    os.rename('CHANGELOG_template.md', 'CHANGELOG.md')

    os.remove('README.md')
    os.rename('README_template.md', 'README.md')

    os.remove('VERSION.md')
    os.rename('VERSION_template.md', 'VERSIO .md')

    # remove unneccesary files

    # remove for module
    if (settings['project_type'] == 'm'):
        shutil.rmtree('gui', ignore_errors=True)

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)
        os.remove('src/__CN_SMALL_NAME__app.py')
        os.remove('src/__main__.py')
        os.remove('src/uninstall.py')

        os.remove('tests/import_test_pkg.py')

        os.remove('install.py')

    # remove for package
    elif (settings['project_type'] == 'p'):
        shutil.rmtree('gui', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME__app.py')
        os.remove('src/__CN_SMALL_NAME__mod.py')
        os.remove('src/__init__.py')
        os.remove('src/__main__.py')
        os.remove('src/uninstall.py')

        os.remove('tests/import_test_mod.py')

        os.remove('install.py')

    # remove for CLI
    elif (settings['project_type'] == 'c'):
        shutil.rmtree('gui', ignore_errors=True)

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME__mod.py')
        os.remove('src/__init__.py')

        os.remove('tests/import_test_mod.py')
        os.remove('tests/import_test_pkg.py')

        os.remove('MANIFEST.in')
        os.remove('pyproject.toml')
        os.remove('requirements.txt')

    # remove for GUI
    elif (settings['project_type'] == 'g'):

        shutil.rmtree('src/__CN_SMALL_NAME__', ignore_errors=True)

        os.remove('src/__CN_SMALL_NAME__mod.py')
        os.remove('src/__init__.py')

        os.remove('tests/import_test_mod.py')
        os.remove('tests/import_test_pkg.py')

        os.remove('MANIFEST.in')
        os.remove('pyproject.toml')
        os.remove('requirements.txt')


# ------------------------------------------------------------------------------
# Rename files/folders
# ------------------------------------------------------------------------------
def rename():

    # recursively rename folders/files
    dir = settings['project_path']
    recurse_rename(dir)


# ------------------------------------------------------------------------------
# Recursive function for renaming files/folders
# ------------------------------------------------------------------------------
def recurse_rename(dir):

    # returns only final path part
    lst = os.listdir(dir)

    # for each file/folder
    for item in lst:

        # put path back together
        old_path = os.path.join(dir, item)

        # if it's a dir
        if os.path.isdir(old_path):
            recurse_rename_dir(old_path, item)

        # it's a file
        else:
            recurse_rename_file(dir, old_path, item)


# ------------------------------------------------------------------------------
# Recursive function for renaming folders
# ------------------------------------------------------------------------------
def recurse_rename_dir(old_path, item):

    # the replacement dict
    reps = settings['project_reps']

    # keep going (skip misc dir)
    if not old_path.endswith('misc'):
        recurse_rename(old_path)

    # do folders after files (when we come back from recurse)
    for key in reps.keys():

        # skip keywords list
        if not isinstance(reps[key], list):

            # if folder name contains replaceable item
            if key in item:

                # do the string replace
                new_name = item
                new_name = new_name.replace(key, reps[key])
                new_path = os.path.join(dir, new_name)

                # do the actual rename
                os.rename(old_path, new_path)


# ------------------------------------------------------------------------------
# Recursive function for renaming files
# ------------------------------------------------------------------------------
def recurse_rename_file(dir, old_path, item):

    # the replacement dict
    reps = settings['project_reps']

    # do files first
    for key in reps.keys():

        # skip keyword list
        if not isinstance(reps[key], list):

            # if file name contains replaceable item
            if key in item:

                # do the steing replace
                new_name = item

                # split file name/ext
                file_parts = item.split('.')
                file_name = file_parts[0]
                file_ext = file_parts[1]

                # split replaceable from our forced underscore
                old_name = file_name.split('__')

                # remove anything without our forced underscore
                if old_name[2] != '_gui':
                    new_name = f'__{old_name[1]}__.{file_ext}'

                # replace the underscored name with its final name
                new_name = new_name.replace(key, reps[key])
                new_path = os.path.join(dir, new_name)

                # do the actual rename
                os.rename(old_path, new_path)


# ------------------------------------------------------------------------------
# Replcace text inside files
# ------------------------------------------------------------------------------
def replace_text():

    # recursively replace folders/files
    dir = settings['project_path']
    recurse_replace_text(dir)


# ------------------------------------------------------------------------------
# Recursive function for replacing text inside files
# ------------------------------------------------------------------------------
def recurse_replace_text(dir):

    # the replacement dict
    reps = settings['project_reps']

    # returns only final path part
    lst = os.listdir(dir)

    # for each file/folder
    for item in lst:

        # put path back together
        old_path = os.path.join(dir, item)

        # if it's a dir
        if os.path.isdir(old_path):

            # keep going (skip misc folder)
            if not old_path.endswith('misc'):
                recurse_replace_text(old_path)

        # it's a file
        else:

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

            # save file with replacements
            with open(old_path, 'w') as file:
                file.writelines(data)

            # do regular text replacement
            with open(old_path) as file:
                data = file.read()

            # for each key, do replace
            for key in reps.keys():

                # skip keyword list
                if not isinstance(reps[key], list):
                    data = data.replace(key, reps[key])

            # save file with replacements
            with open(old_path, 'w') as file:
                file.write(data)


# ------------------------------------------------------------------------------
# This function cleans out the unneccessry parts of the README file
# ------------------------------------------------------------------------------
def fix_readme():

    # path to project
    dir = settings['project_path']
    path = os.path.join(dir, 'README.md')

    # where to put the needed lines
    new_data = []

    # what type of project are we creating?
    project_type = settings['project_type']

    # just a boolean flag to say if we are kajiggering
    in_it = False

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

    # path to project
    dir = settings['project_path']
    path = os.path.join(dir, 'pyproject.toml')

    if not os.path.exists(path):
        return

    # get the file data
    with open(path) as file:
        data = file.read()

    # build a new string
    new_str = ''
    for item in settings['project_reps']['__CN_KEYWORDS__']:
        new_str += '\"' + item + '\",\n\t'
    # chop off last comma/newline
    new_str = new_str[:-3]

    # replace the string in the file
    data = data.replace('\"__CN_KEYWORDS__\"', new_str)

    # save the file
    with open(path, 'w') as file:
        file.write(data)


# ------------------------------------------------------------------------------
# Add venv and .git folders to new project
# ------------------------------------------------------------------------------
def add_in():

    # TODO: make sure we are in current proj path w/chdir
    
    # add git folder
    cmd = 'git init'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # add venv dir
    cmd = 'python -m venv venv'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # FIXME: can't source venv dir (working on it)
    # TODO: install pylama/build in venv


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    main()

# -)
