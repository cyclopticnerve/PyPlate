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

from pyconf import add_reps
from pyheaders import replace_headers

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
# (e.g. ~/Documents/Projects/Python/PyPlate/src/)
CURR_DIR = os.path.dirname(os.path.abspath(__file__))

# this is the default dir where the template files are located rel to the script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
TEMPLATE_DIR = os.path.abspath(f'{CURR_DIR}/../template')

# these are the default dirs for project location
# (e.g. ~/Documents/Projects/Python/) (above PyPlate)
BASE_DIR = os.path.abspath(f'{CURR_DIR}/../../')

# the default date format to use in headers
DATE_FMT = '%x'

# get the current user home dir
USER_DIR = os.path.expanduser('~')

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default conf settings for project paths (updated in get_dict_conf)
# NB: the keys with values here are REQUIRED to prevent formatting errors if the
# value is an empty string
# these values will be used to replace values in dict_proj and ARE ONLY
# user-editable, and ARE ONLY strings, no programming needed
# these values are also usually only set ONCE for the life of the program,
# so making them user-editable is reasonable, since they are set-and-forget
dict_conf = {
    'conf_base': BASE_DIR,
    'conf_mods': '',
    'conf_pkgs': '',
    'conf_clis': '',
    'conf_guis': '',
    'conf_date': DATE_FMT,
    'conf_auth': '',
    'conf_mail': '',
    'conf_lcns': '',
    'conf_aftr': [
        'git init',
        'python -m venv venv',
    ],
    # FIXME: what to do with these
    # 'conf_inst': '',
    # 'conf_conf': '',
}

# the default settings to use to create the project (updated in get_dict_proj)
# NB: these values will ONLY be used to replace text in
# folder names/file names/file contents and ARE NOT user-editable
# some of these are taken from dict_conf, and some are per-project
# the per-project values will be taken from user input in get_dict_proj
dict_proj = {
    'proj_type': '',  # m (Module), p (Package), c (CLI), g (GUI)
    'proj_dir':  '',  # conf_base/conf_mods/Foo, etc.
}

dict_reps = {
    '__CN_BIG_NAME__':   '',  # Foo
    '__CN_SMALL_NAME__': '',  # foo
    '__CN_DATE__':       '',  # conf_date (12/08/2022)
    '__CN_AUTHOR__':     '',  # conf_auth (cyclopticnerve)
    '__CN_EMAIL__':      '',  # conf_mail (cyclopticnerve@gmail.com)
    '__CN_LICENSE__':    '',  # conf_lcns (WTFPLv2)
    # FIXME: what to do with these
    # '__CN_INST_DIR__':   '',  # used in install.py/unimnstall.py
    # '__CN_CONF_DIR__':   '',  # used in install.py/uninstall.py
    # '__CN_GUI_EXEC__':   '',  # foo_gui.py (for .desktop file)
    # '__CN_GUI_ICON__':   ''   # foo.png (for .desktop file)
}

dict_files = {
    'common': [
        'misc',
        '.gitignore',
        'LICENSE.txt',
        'metadata.py',
        'README.md',
    ],
    'module': [

    ],
    'package': [

    ],
    'cli': [

    ],
    'gui': [
        'gui',
    ]
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
    # recurse_rename(dict_proj['proj_dir'])
    rename(dict_proj['proj_dir'])
    # recurse_replace(dict_proj['proj_dir'])
    # add_git_venv()


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

    # no file, create it using defaults
    if not os.path.exists(conf_path):
        with open(conf_path, 'w') as file:
            file.write(json.dumps(dict_conf, indent=4))

            # warn user about fresh default file and exit
            print('Edit the pymaker.json file before running. See README.md')
            exit()

    # there is a file
    else:

        # read conf dir
        with open(conf_path) as file:
            dict_conf = json.load(file)

        # apply default value if key is empty
        # NB: this is here in case the user edits the file manually and enters
        # an empty value for one of the REQUIRED keys
        # sure would be great if we had a function that could merge user and
        # default dictionaries... -)
        if dict_conf['conf_base'] == '':
            dict_conf['conf_base'] = BASE_DIR
        if dict_conf['conf_date'] == '':
            dict_conf['conf_date'] = DATE_FMT

        # write the file back (in case we changed something above)
        with open(conf_path, 'w') as file:
            file.write(json.dumps(dict_conf, indent=4))


# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_dict_proj():

    """
        Get project info

        Asks the user for project info, such as type, name, etc.
    """

    global dict_conf
    global dict_reps

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
    if dict_proj['proj_type'] in 'm':
        prj_sub_dir = dict_conf['conf_mods']
    elif dict_proj['proj_type'] in 'p':
        prj_sub_dir = dict_conf['conf_pkgs']
    elif dict_proj['proj_type'] in 'c':
        prj_sub_dir = dict_conf['conf_clis']
    if dict_proj['proj_type'] in 'g':
        prj_sub_dir = dict_conf['conf_guis']

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
    # NB: need a var here b/c brackets [] don't work inside f-string {}
    tmp_path = dict_proj['proj_dir']
    if os.path.exists(tmp_path):
        print(f'Project {tmp_path} already exists')
        exit()

    # calculate small name
    # NB: prj_name_small will be used later, so easier to set it to a var
    prj_name_small = prj_name_big.lower()
    dict_reps['__CN_SMALL_NAME__'] = prj_name_small

    # calculate current date
    dict_reps['__CN_DATE__'] = \
        datetime.now().strftime(dict_conf['conf_date'])

    # get author straight from conf
    dict_reps['__CN_AUTHOR__'] = dict_conf['conf_auth']

    # get email straight from conf
    dict_reps['__CN_MAIL__'] = dict_conf['conf_mail']

    # get license straight from conf
    dict_reps['__CN_LICENSE__'] = dict_conf['conf_lcns']

    # this starts the extension process
    # we pass the conf dict read from pymaker.json and the reps dict that is
    # hard coded here, to an external py file. there, new conf k/v pairs and new
    # rep k/v pairs can be assesed and added to the reps k/v set.
    dict_conf, dict_reps = add_reps(dict_conf, dict_reps)

    print(json.dumps(dict_reps, indent=4))
    exit()
    # FIXME: what to do with these
#     # calculate/make install dir
#     conf_inst = dict_conf['conf_inst']
#     small_name = dict_prj['proj_small_name']
#     if conf_inst == '':
#         conf_inst = f'{USER_DIR}/.{conf_auth}/{small_name}'

#     dict_conf['conf_inst'] = os.path.abspath(conf_inst)
#     os.makedirs(dict_conf['conf_inst'], exist_ok=True)
#     dict_proj['proj_reps']['__CN_INST_DIR__'] = conf_inst

#     # calculate/make config dir
#     dict_conf['conf_conf'] = os.path.abspath(f'{conf_conf}/{prj_name_small}')
#     os.makedirs(dict_conf['conf_conf'], exist_ok=True)
#     dict_proj['proj_reps']['__CN_CONF_DIR__'] = dict_conf['conf_conf']

#     # calculate gui location
#     dict_proj['proj_reps']['__CN_GUI_EXEC__'] = \
#         f'{USER_DIR}/.{conf_auth}/{prj_name_small}/gui/{prj_name_small}_gui.py'

#     # calculuate icon location
#     dict_proj['proj_reps']['__CN_GUI_ICON__'] = \
#         f'{USER_DIR}/.local/share/icons/{conf_auth}/{prj_name_small}.png'


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
# def recurse_rename(path):

#     """
#         Recursive function for renaming files/folders

#         Paramaters:
#             path [string]: the folder to start recursively renaming from

#         This is a recursive function to rename files under a given folder. It
#         iterates over the contents of the folder, renaming files as it goes. If
#         it encounters a folder, it calls itself recursively, passing that folder
#         as the parameter. Once all files are renamed, it will then bubble up to
#         rename all folders.
#     """

#     # don't rename these dirs or contents
#     skip_dirs = ['misc']

#     # the replacement dict
#     reps = dict_proj['proj_reps']

#     # returns only final path part for each entry
#     lst = os.listdir(path)

#     # for each file/folder
#     for item in lst:

#         # put path back together
#         item_path = os.path.join(path, item)

#         # if it's a dir
#         if os.path.isdir(item_path):

#             # always skip misc folder (never replace/rename)
#             if item not in skip_dirs:


#                 print('before dir:', item_path)

#                 # recurse itself to find more files
#                 recurse_rename(item_path)

#                 print('after dir:', item_path)

#         else:
#             #TODO: put replace code here

#         # called for each file and dir

#         new_item = item
#         # for each replacement key
#         for key in reps.keys():

#             # TODO: this prevents problems where we rename a file in a folder that
#             # we (will) also renamed (not sure but it works?)
#             # if key in item:

#         # print('item:', item)
#         # print('item_path:', item_path)

#             # # do the string replace
#             new_item = new_item.replace(key, reps[key])
#         print('item:', new_item)
#             # # remove trailing identifiers
#             # new_item = new_item.replace('_app', '')
#             # new_item = new_item.replace('_mod', '')

#             # # create new path
#         new_path = os.path.join(path, new_item)

#             # do the actual rename
#         os.rename(item_path, new_path)

def rename(path):

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

    # don't rename these dirs or files, or change file contents
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

                print('before dir:', item_path)

                # recurse itself to find more files
                rename(item_path)

                print('after dir:', item_path)

        else:
            replace(item_path)

        # called for each file and dir

        new_item = item
        # for each replacement key
        for key in reps.keys():

            # TODO: this prevents problems where we rename a file in a folder that
            # we (will) also renamed (not sure but it works?)
            # if key in item:

            # print('item:', item)
            # print('item_path:', item_path)

            # # do the string replace
            new_item = new_item.replace(key, reps[key])
        print('item:', new_item)
        # # remove trailing identifiers
        # new_item = new_item.replace('_app', '')
        # new_item = new_item.replace('_mod', '')

        # # create new path
        new_path = os.path.join(path, new_item)

        # do the actual rename
        os.rename(item_path, new_path)
# ------------------------------------------------------------------------------
# Recursive function for replacing text inside files
# ------------------------------------------------------------------------------
# def recurse_replace(path):

#     """
#         Recursive function for replacing text inside files

#         Paramaters:
#             path [string]: the file to replace text in

#         This is a recursive function to replace text inside a file. Given a
#         specific file, it iterates the file line by line, replacing text as it
#         goes. When it is done, it saves the file to disk. This replaces the
#         __CN_... stuff from the settings inside the file, as headers are
#         delegated to the next function (recurse_replace_headers).
#     """

#     # don't rename these dirs or contents
#     skip_dirs = ['misc']

#     # the replacement dict
#     reps = dict_proj['proj_reps']

#     # returns only final path part for each entry
#     lst = os.listdir(path)

#     # for each file/folder
#     for item in lst:

#         # put path back together
#         item_path = os.path.join(path, item)

#         # if it's a dir
#         if os.path.isdir(item_path):

#             # always skip misc folder (never replace/rename)
#             if item not in skip_dirs:

#                 # recurse itself to find more files
#                 recurse_replace(item_path)

#         # if it's a file
#         else:

#             # replace headers in file
#             recurse_replace_headers(item_path, reps)

#             # open file as text line array
#             with open(item_path) as file:
#                 data = file.readlines()

#             # for each line in array
#             for i in range(0, len(data)):

#                 # replace text in line
#                 for key in reps.keys():
#                     data[i] = data[i].replace(key, reps[key])

#             # NB: i think file.read() strips the string, so we lose the
#             # last blank line, which is part of my styling
#             # so add it back in before saving
#             data.append('\n')

#             # save file with replacements
#             with open(item_path, 'w') as file:
#                 file.writelines(data)

#             # readme needs extra handling
#             if item == 'README.md':
#                 fix_readme(item_path)


def replace(path):

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

    # the replacement dict
    reps = dict_proj['proj_reps']

    # open file as text line array
    with open(path) as file:
        data = file.readlines()

    # replace headers in file
    data = replace_headers(data, reps)

    # for each line in array
    for i in range(0, len(data)):

        # replace text in line
        for key in reps.keys():
            data[i] = data[i].replace(key, reps[key])

    # NB: i think file.read() strips the string, so we lose the
    # last blank line, which is part of my styling
    # so add it back in before saving
    data.append('\n')

    # save file with replacements
    with open(path, 'w') as file:
        file.writelines(data)

    # readme needs extra handling
    if item == 'README.md':
        fix_readme(path)


# ------------------------------------------------------------------------------
# Cleans out the unneccessry parts of the README file
# ------------------------------------------------------------------------------
def fix_readme(path):

    """
        Cleans out the unneccesary parts of the README file

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as Module/Package or
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
