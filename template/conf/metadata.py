#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: metadata.py                                           |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import json
import os
import re

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# this is the project dir
curr_dir = os.path.dirname(__file__)
prj_dir = os.path.join(curr_dir, '..')
DIR_PROJ = os.path.abspath(prj_dir)

# load settings file
DICT_SETTINGS = []
file_settings = os.path.join(DIR_PROJ, 'conf', 'settings.json')
if os.path.exists(file_settings):
    with open(file_settings, 'r', encoding='utf-8') as f:
        DICT_SETTINGS = json.load(f)

# load metadata file
DICT_METADATA = []
file_metadata = os.path.join(DIR_PROJ, 'conf', 'metadata.json')
if os.path.exists(file_metadata):
    with open(file_metadata, 'r', encoding='utf-8') as f:
        DICT_METADATA = json.load(f)

# load blacklist file
DICT_BLACKLIST = []
file_blacklist = os.path.join(DIR_PROJ, 'conf', 'blacklist.json')
if os.path.exists(file_blacklist):
    with open(file_blacklist, 'r', encoding='utf-8') as f:
        DICT_BLACKLIST = json.load(f)

# TODO: what to do about descs? toml? or help file?
# 'metadata' will be edited by the user through 'conf/metadata.json'

# the following caveats apply to 'metadata':

# PP_VERSION
# this is the canonical (only and absolute) version number string for this
# project
# this should provide the absolute version number string (in semantic notation)
# of this project, and all other version numbers should be superceded by this
# string

# PP_SHORT_DESC
# this is the short description of the project, used in README.md and
# # pyproject.toml

# PP_KEYWORDS
# these are the keywords for the project, for use in pyproject.toml for the PyPI
# listing, and should also be used in the GitHub project page
# delimiters for all entries MUST be comman

# PP_PY_DEPS
# these are the python dependencies for the project
# they are stored here for install.py, pyproject.toml, and README.md
# it is a dictionary where the key is the dep name, and the value is a link to
# the download page (for README)
# when used in pyproject.toml or install.py, it will be automatically downloaded
# from PyPI by pip using just the name

# PP_SYS_DEPS
# these are the sytem dependencies for the project
# they are stored here for install.py
# delimiters for all entries MUST be comma

# PP_GUI_CATEGORIES = ''
# PP_GUI_EXEC = ''
# PP_GUI_ICON = ''
# this is mostly for desktops that use a windows-stylew menu/submenu, not for
# Ubuntu-style overviews, and will be used in the __PP_NAME_BIG__.desktop file
# gui categories MUST be seperated by a comma
# if exec/icon paths are not absolute, they will be found in standard paths
# these paths vary, but I will add them here in the comments when I figure them
# out

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# keep track of error count
g_err_cnt = 0


# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# The main function of the module
# ------------------------------------------------------------------------------
def main():
    """
        The main function of the module

        This function is the main entry point for the module, initializing the
        module, and performing its steps.
    """

    # do proactive replacements in specific files (replaces needed text)
    fix_pyproject()
    fix_install()
    fix_desktop()
    fix_init()
    fix_readme()
    fix_argparse()

    # find __PP_ /PP_ stuff
    recurse(DIR_PROJ)

    # print error count (__PP_/PP_ stuff found)
    print(f'Errors: {g_err_cnt}')


# ------------------------------------------------------------------------------
# Replace text in the pyproject.toml file
# ------------------------------------------------------------------------------
def fix_pyproject():
    """
        Replace text in the pyproject.toml file

        Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # this function will ALWAYS create a multi-line array, e.g.:
    # keywords = [
    #     "foo",
    #     "bar"
    # ]
    # even if the input file's array was a single line or multiline
    # also if the input file's array was empty or not

    # check if the file exists
    prj_toml = os.path.join(DIR_PROJ, 'pyproject.toml')
    if not os.path.exists(prj_toml):
        return

    # open file and get contents
    with open(prj_toml, 'r', encoding='utf-8') as f:
        text = f.read()

        # NB: we do a dunder replace here because putting a dunder as the
        # default name in the toml file causes the linter to choke, so we use a
        # dummy name

        # replace name
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*name[\t ]*=)'
            r'(.*?$)'
        )
        PP_NAME = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
        rep_str = rf'\g<1>\g<2>\g<3> "{PP_NAME}"'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace version
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*version[\t ]*=)'
            r'(.*?$)'
        )
        PP_VERSION = DICT_METADATA['PP_VERSION']
        rep_str = rf'\g<1>\g<2>\g<3> "{PP_VERSION}"'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace short description
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*description[\t ]*=)'
            r'(.*?$)'
        )
        PP_SHORT_DESC = DICT_METADATA['PP_SHORT_DESC']
        rep_str = rf'\g<1>\g<2>\g<3> "{PP_SHORT_DESC}"'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # # replace keywords array
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*keywords[\t ]*=)'
            r'(.*?\])'
        )

        # convert dict to string
        PP_KEYWORDS = DICT_METADATA['PP_KEYWORDS']
        split_str = _split_quote(PP_KEYWORDS, quote='"', lead='\t',
                                 join=',\n\t', tail='\n')

        # replace string
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace dependencies array
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*dependencies[\t ]*=)'
            r'(.*?\])'
        )

        # convert dict to string
        PP_PY_DEPS = DICT_METADATA['PP_PY_DEPS']
        str_py_deps = ','.join(PP_PY_DEPS.keys())
        split_str = _split_quote(str_py_deps, quote='"', lead='\t',
                                 join=',\n\t', tail='\n')

        # replace string
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

    # save file
    with open(prj_toml, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the install file_split
# ------------------------------------------------------------------------------
def fix_install():
    """
        Replace text in the install file

        Replaces the system and Python dependencies in the install file.
    """

    # check if the file exists
    prj_inst = os.path.join(DIR_PROJ, 'install.py')
    if not os.path.exists(prj_inst):
        return

    # open file and get content
    with open(prj_inst, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace python dependencies array
        pattern_str = (
            r'(^\s*dict_install[\t ]*=\s*{)'
            r'(.*?)'
            r'(^\s*\'py_deps\'[\t ]*:)'
            r'(.*?\])'
        )

        # convert dict keys to string
        PP_PY_DEPS = DICT_METADATA['PP_PY_DEPS']
        str_py_deps = ','.join(PP_PY_DEPS.keys())
        split_str = _split_quote(str_py_deps, quote='"', lead='\t\t',
                                 join=',\n\t\t')

        # replace string
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\n\t]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace system dependencies array
        pattern_str = (
            r'(^\s*dict_install[\t ]*=)'
            r'(.*?)'
            r'(^\s*\'sys_deps\'[\t ]*:)'
            r'(.*?\])'
        )

        # convert dict to string
        PP_SYS_DEPS = DICT_METADATA['PP_SYS_DEPS']
        split_str = _split_quote(PP_SYS_DEPS, quote='"', lead='\t\t',
                                 join=',\n\t\t')

        # replace string
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\n\t]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

    # save file
    with open(prj_inst, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the desktop file
# ------------------------------------------------------------------------------
def fix_desktop():
    """
        Replace text in the desktop file

        Replaces the icon, executable, and category text in a .desktop file for
        programs that use this.
    """

    # first get the gui dir
    gui_dir = os.path.join(DIR_PROJ, 'misc')
    if not os.path.exists(gui_dir):
        return

    # next list all files in gui dir
    gui_files = os.listdir(gui_dir)
    if len(gui_files) == 0:
        return

    # then get a list of all the files ending in .desktop
    prj_desk = [item for item in gui_files if
                os.path.splitext(item)[1] == '.desktop']
    if len(prj_desk) != 1:
        return

    # get path to desktop file
    path_desk = os.path.join(gui_dir, prj_desk[0])

    # open file and get contents
    with open(path_desk, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace short description
        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Comment[\t ]*=)'
            r'(.*?$)'
        )
        PP_SHORT_DESC = DICT_METADATA['PP_SHORT_DESC']
        rep_str = rf'\g<1>\g<2>\g<3>{PP_SHORT_DESC}'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace categories
        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Categories[\t ]*=)'
            r'(.*?$)'
        )

        # convert dict to string
        PP_GUI_CATEGORIES = DICT_METADATA['PP_GUI_CATEGORIES']
        split_str = _split_quote(PP_GUI_CATEGORIES, join=';', tail=';')

        # replace string
        rep_str = rf'\g<1>\g<2>\g<3>{split_str}'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace exec
        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Exec[\t ]*=)'
            r'(.*?$)'
        )
        # TODO: look in $PATH
        PP_GUI_EXEC = DICT_METADATA['PP_GUI_EXEC']
        rep_str = rf'\g<1>\g<2>\g<3>{PP_GUI_EXEC}'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace icon
        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Icon[\t ]*=)'
            r'(.*?$)'
        )
        # TODO: look in $PATH
        PP_GUI_ICON = DICT_METADATA['PP_GUI_ICON']
        rep_str = rf'\g<1>\g<2>\g<3>{PP_GUI_ICON}'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

    # save file
    with open(path_desk, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the __init__.py file
# ------------------------------------------------------------------------------
def fix_init():
    """
        Replace text in the __init__.py file

        Replaces the 'from __PP_NAME_SMALL__ import filename' text in the
        __init__.py file.
    """

    # get path to package folder inside src
    pp_small = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
    dir_pkg = os.path.join(DIR_PROJ, 'src', pp_small)
    if not os.path.exists(dir_pkg):
        return

    # initial value of path to __init__ file
    prj_init = ''

    # initial list of files that are NOT __init__
    lst_files = []

    # get all files in package dir and enumerate
    lst_names = os.listdir(dir_pkg)
    if len(lst_names) == 0:
        return
    for item in lst_names:

        # rebuild path
        path = os.path.join(dir_pkg, item)

        # if it's __init__
        if item == '__init__.py':
            prj_init = path

        else:

            # if it's a file, not a dir (__pycache__)
            if (os.path.isfile(path)):

                # strip ext and add to list
                short_item = os.path.splitext(item)[0]
                lst_files.append(short_item)

    # sort file list to look pretty (listdir is not sorted)
    lst_files.sort()

    # format list for imports section
    lst_imports = [
        f'from {pp_small} import {item}  # noqa W0611 (unused import)'
        for item in lst_files
    ]
    str_imports = '\n'.join(lst_imports)

    # format __all__ for completeness
    lst_all = [f'\'{item}\'' for item in lst_files]
    str_all_j = ', '.join(lst_all)
    str_all = f'__all__ = [{str_all_j}]'

    # open file and get contents
    with open(prj_init, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace imports block
        pattern_str = (
            r'(^#[\t ]*__PP_IMPORTS_START__[\t ]*)'
            r'(.*?)'
            r'(^#[\t ]*__PP_IMPORTS_END__[\t ]*)'
        )
        rep_str = rf'\g<1>\n{str_imports}\n{str_all}\n\g<3>'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

    # save file
    with open(prj_init, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the README file
# ------------------------------------------------------------------------------
def fix_readme():
    """
        Replace text in the README file

        Replace short description, dependencies, and version number in the
        README file.
    """

    # check if the file exists
    prj_read = os.path.join(DIR_PROJ, 'README.md')
    if not os.path.exists(prj_read):
        return

    # open file and get contents
    with open(prj_read, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace short description
        pattern_str = (
            r'(<!--[\t ]*__RM_SHORT_DESC_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__RM_SHORT_DESC_END__[\t ]*-->)'
        )
        PP_SHORT_DESC = DICT_METADATA['PP_SHORT_DESC']
        rep_str = rf'\g<1>\n{PP_SHORT_DESC}\n\g<3>'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace dependencies array
        pattern_str = (
            r'(<!--[\t ]*__RM_PY_DEPS_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__RM_PY_DEPS_END__[\t ]*-->)'
        )

        # build a string from the dict
        PP_PY_DEPS = DICT_METADATA['PP_PY_DEPS']
        str_py_deps = ''
        for key, val in PP_PY_DEPS.items():
            str_py_deps += f'[{key}]({val}),'

        # split the string for README
        split_str = _split_quote(str_py_deps, quote='', join='<br>\n',
                                 tail='\n')

        # no split str, use default
        if split_str == '':
            split_str = 'None\n'

        # replace text
        rep_str = rf'\g<1>\n{split_str}\g<3>'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # get version
        PP_VERSION = DICT_METADATA['PP_VERSION']

        # replace version
        pattern_vers = (
            r'(\s*foo@bar:~/Downloads\$ python -m pip install )'
            r'(.*-)'
            r'(.*?)'
            r'(\.tar\.gz)'
        )
        rep_str = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
        text = re.sub(pattern_vers, rep_str, text)

        pattern_vers = (
            r'(\s*foo@bar:~/Downloads/)'
            r'(.*?)'
            r'(\$ python -m pip install ./dist/)'
            r'(.*-)'
            r'(.*?)'
            r'(\.tar\.gz)'
        )
        rep_str = rf'\g<1>\g<2>\g<3>\g<4>{PP_VERSION}\g<6>'
        text = re.sub(pattern_vers, rep_str, text)

        pattern_vers = (
            r'(\s*foo@bar:~\$ cd ~/Downloads/)'
            r'(.*-)'
            r'(.*)'
        )
        rep_str = rf'\g<1>\g<2>{PP_VERSION}'
        text = re.sub(pattern_vers, rep_str, text)

        pattern_vers = (
            r'(\s*foo@bar:~/Downloads/)'
            r'(.*-)'
            r'(.*)'
            r'(\$ \./install.py)'
        )
        rep_str = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
        text = re.sub(pattern_vers, rep_str, text)

    # save file
    with open(prj_read, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text for argparse stuff
# ------------------------------------------------------------------------------
def fix_argparse():
    """
        Replace text for argparse stuff

        This function replaces PP_ variables in any file that uses
        argparse.
    """

    # get src dir
    dir_src = os.path.join(DIR_PROJ, 'src')

    # get all names in dir
    items = [item for item in os.listdir(dir_src)]

    # get all paths
    items = [os.path.join(dir_src, item) for item in items]

    # get all files
    items = [item for item in items if os.path.isfile(item)]

    # get all .py files
    items = [item for item in items if os.path.splitext(item)[1] == '.py']

    # add the template files
    # empty_main = os.path.join(DIR_PROJ, 'misc', 'empty_main.py')
    # items.append(empty_main)

    # for each file
    for path_item in items:

        # check if file exists
        if not os.path.exists(path_item):
            continue

        # open file and get contents
        with open(path_item, 'r', encoding='utf-8') as f:
            text = f.read()

            # replace short description
            pattern_str = (
                r'(import argparse.*def _parse_args\(\):.*)'
                r'(argparse.ArgumentParser\(\s*description=\')'
                r'(.*?)'
                r'(\'.*)'
            )
            PP_SHORT_DESC = DICT_METADATA['PP_SHORT_DESC']
            rep_str = rf'\g<1>\g<2>{PP_SHORT_DESC}\g<4>'
            text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

            # replace version
            pattern_str = (
                r'(import argparse.*def _parse_args\(\):.*)'
                r'(print\(\'.* version )'
                r'(.*?)'
                r'(\'.*)'
            )
            PP_VERSION = DICT_METADATA['PP_VERSION']
            rep_str = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
            text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # save file
        with open(path_item, 'w', encoding='utf-8') as f:
            f.write(text)


# ------------------------------------------------------------------------------
# Recurse through the folder structure looking for errors
# ------------------------------------------------------------------------------
def recurse(path):
    """
        Recurse through the folder structure looking for errors

        Paramaters:
            path [string]: the file path to start looking for errors

        This function recurses through the project directory, looking for errors
        in each file's headers and content for strings that do not match their
        intended contents. It checks a header's project, filename, and date
        values as well as looking for dunder values that should have been
        replaced.
    """

    # blacklist
    # don't check headers, text, or path names for these items
    skip_all = DICT_BLACKLIST['skip_all']
    skip_headers = DICT_BLACKLIST['skip_headers']
    skip_text = DICT_BLACKLIST['skip_text']
    skip_path = DICT_BLACKLIST['skip_path']

    # strip trailing slashes to match path component
    skip_all = [item.strip('/') for item in skip_all]
    skip_headers = [item.strip('/') for item in skip_headers]
    skip_text = [item.strip('/') for item in skip_text]
    skip_path = [item.strip('/') for item in skip_path]

    # get list of replaceable file names
    items = [item for item in os.listdir(path) if item not in skip_all]
    for item in items:

        # put path back together
        path_item = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(path_item):

            # recurse itself to find more files
            recurse(path_item)

        else:

            # open file and get lines
            with open(path_item, 'r', encoding='utf-8') as f:
                lines = f.readlines()

                # check headers of most files
                if item not in skip_headers:
                    _check_headers(path_item, lines)

                # check contents of most files
                if item not in skip_text:
                    _check_text(path_item, lines)

        # check file paths (subdirs and such)
        if item not in skip_path:
            _check_path(path_item)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Checks header values for dunders
# ------------------------------------------------------------------------------
def _check_headers(path_item, lines):
    """
        Checks header values for dunders

        Paramaters:
            path_item [string]: the full path to file to be checked
            lines [array]: the contents of the file to be checked

        This function checks the files headers for values that either do not
        match the file's project/file name, or do not have a date set.
    """

    # global error count
    global g_err_cnt

    for i in range(0, len(lines)):
        line = lines[i]

        # check project name
        proj_name = os.path.basename(DIR_PROJ)
        pattern = (
            r'(^\s*(<!--|#)\s*)'
            r'(Project)'
            r'(\s*:\s*)'
            r'(.*?)'
            r'(\s)'
        )
        res = re.search(pattern, line, flags=re.M | re.S)
        if res and res.group(5) != proj_name:
            print(
                f'{path_item}:{i + 1}: Header Project name should be '
                f'\'{proj_name}\''
            )

            # inc error count
            g_err_cnt += 1

        # check file name
        file_name = os.path.basename(path_item)
        pattern = (
            r'(^\s*(<!--|#)\s*)'
            r'(Filename)'
            r'(\s*:\s*)'
            r'(.*?)'
            r'(\s)'
        )
        res = re.search(pattern, line, flags=re.M | re.S)
        if res and res.group(5) != file_name:
            print(
                f'{path_item}:{i + 1}: Header Filename should be '
                f'\'{file_name}\''
            )

            # inc error count
            g_err_cnt += 1

        # check date
        pattern = (
            r'(^\s*(<!--|#)\s*)'
            r'(Date)'
            r'(\s*:\s*)'
            r'(.*?)'
            r'(\s)'
        )
        res = re.search(pattern, line, flags=re.M | re.S)
        if res:

            # there is *something* in the date field
            if res.group(5) != '':

                # check for valid date
                pattern2 = r'\d*/\d*/\d*'
                res2 = re.search(pattern2, res.group(5))
                if not res2:
                    print(f'{path_item}:{i + 1}: Header Date is not set')

                    # inc error count
                    g_err_cnt += 1

            else:
                print(f'{path_item}:{i + 1}: Header Date is not set')

                # inc error count
                g_err_cnt += 1


# ------------------------------------------------------------------------------
# Checks file contents for replacements
# ------------------------------------------------------------------------------
def _check_text(path_item, lines):
    """
        Checks file contents for replacements

        Paramaters:
            path_item [string]: the full path to file to be checked for text
            lines [array]: the contents of the file to be checked

        This function checks that none of the files contains an unreplaced
        replacement variable from the initial project info.
    """

    # global error count
    global g_err_cnt

    for i in range(0, len(lines)):
        line = lines[i]

        # the dunders to look for
        reps = [rep for rep in DICT_SETTINGS['info'] and DICT_METADATA]

        # check for dunders in text
        for rep in reps:
            if rep in line:
                print(f'{path_item}:{i + 1}: Text contains {rep}')

                # inc error count
                g_err_cnt += 1


# ------------------------------------------------------------------------------
# Checks file paths for dunders
# ------------------------------------------------------------------------------
def _check_path(path_item):
    """
        Checks file paths for dunders

        Paramaters:
            path_item [string]: the full path to file to be checked for text

        This function checks that none of the files paths contains an unreplaced
        dunder variable from the initial project info.
    """

    # global error count
    global g_err_cnt

    # check for dunders in path
    if '__PP_' in path_item:
        print(f'{path_item}: Path contains __PP_')

        # inc error count
        g_err_cnt += 1


# ------------------------------------------------------------------------------
# A helper function to split keywords and dependencies
# ------------------------------------------------------------------------------
def _split_quote(str_in, split=',', quote='', lead='', join=',', tail=''):
    """
        A helper function to split and reformat keywords and dependencies

        Paramaters:
            str_in [string]: the string to split
            split [string]: the character to split on
            quote [string]: the character to use to quote each entry (or empty)
            lead [string]: the string to preceed the formatted string (or empty)
            join [string]: the string to join each line in the output (or empty)
            tail [string]: the string to follow the formatted string (or empty)

        Returns:
            [string]: a new string which is split, quoted, joined, and
            surrounded by the lead and tail strings

        This function takes a string and splits it using the split param, then
        quotes each item using the quote param, then joins the items using the
        join param, and surrounds it using the lead and tail params to create a
        nice-looking list.
    """

    # first split the list using the split char
    split_lst = [item.strip() for item in str_in.split(split)]

    # blank strings, when split w/param, still contain 1 entry
    # https://stackoverflow.com/questions/16645083/when-splitting-an-empty-string-in-python-why-does-split-return-an-empty-list
    # so we do the list comprehension BEFORE testing the list length
    # quote items and put into new list
    split_lst = [f'{quote}{item}{quote}' for item in split_lst if item != '']

    # if the list is empty, return empty result
    if len(split_lst) == 0:
        return ''

    # join list using join string
    split_lst_str = f'{join}'.join(split_lst)

    # surround list with lead and tail
    split_lst_str = f'{lead}{split_lst_str}{tail}'

    # return the final result string
    return split_lst_str


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
