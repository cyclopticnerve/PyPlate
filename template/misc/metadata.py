#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PkgTest                                                /          \
# Filename: metadata.py                                           |     ()     |
# Date    : 03/23/2023                                            |            |
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
file_settings = os.path.join(DIR_PROJ, 'misc', 'settings.json')
if os.path.exists(file_settings):
    with open(file_settings, 'r', encoding='utf-8') as f:
        DICT_SETTINGS = json.load(f)

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# keep track of error count
err_cnt = 0


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
    do_toml()
    do_install()
    do_desktop()
    do_init()
    do_readme()

    # do replacements for PP_ stuff
    # also print found __PP_ stuff
    recurse(DIR_PROJ)

    # print error count (__PP_ stuff found)
    print(f'Errors: {err_cnt}')


# ------------------------------------------------------------------------------
# Replace text in the pyproject.toml file
# ------------------------------------------------------------------------------
def do_toml():
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

        # replace version
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*version[\t ]*=)'
            r'(.*?$)'
        )
        PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
        rep_str = rf'\g<1>\g<2>\g<3> "{PP_VERSION}"'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace short description
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*description[\t ]*=)'
            r'(.*?$)'
        )
        PP_SHORT_DESC = DICT_SETTINGS['metadata']['PP_SHORT_DESC']
        rep_str = rf'\g<1>\g<2>\g<3> "{PP_SHORT_DESC}"'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # # replace keywords array
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*keywords[\t ]*=)'
            r'(.*?\])'
        )
        PP_KEYWORDS = DICT_SETTINGS['metadata']['PP_KEYWORDS']
        split_str = _split_quote(PP_KEYWORDS)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace dependencies array
        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*dependencies[\t ]*=)'
            r'(.*?\])'
        )
        PP_PY_DEPS = DICT_SETTINGS['metadata']['PP_PY_DEPS']
        split_str = _split_quote(PP_PY_DEPS)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

    # save file
    with open(prj_toml, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the install file
# ------------------------------------------------------------------------------
def do_install():
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
        PP_PY_DEPS = DICT_SETTINGS['metadata']['PP_PY_DEPS']
        split_str = _split_quote(PP_PY_DEPS, tabs=2)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\t\]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace system dependencies array
        pattern_str = (
            r'(^\s*dict_install[\t ]*=)'
            r'(.*?)'
            r'(^\s*\'sys_deps\'[\t ]*:)'
            r'(.*?\])'
        )
        PP_SYS_DEPS = DICT_SETTINGS['metadata']['PP_SYS_DEPS']
        split_str = _split_quote(PP_SYS_DEPS, tabs=2)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\t\]'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

    # save file
    with open(prj_inst, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the desktop file
# ------------------------------------------------------------------------------
def do_desktop():
    """
        Replace text in the desktop file

        Replaces the icon, executable, and category text in a .desktop file for
        programs that use this.
    """

    # first get the gui dir
    gui_dir = os.path.join(DIR_PROJ, 'gui')
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

    # open file and get contents
    with open(prj_desk[0], 'r', encoding='utf-8') as f:
        text = f.read()

        # replace short description
        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Comment[\t ]*=)'
            r'(.*?$)'
        )
        PP_SHORT_DESC = DICT_SETTINGS['metadata']['PP_SHORT_DESC']
        rep_str = rf'\g<1>\g<2>\g<3>{PP_SHORT_DESC}'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace categories
        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Categories[\t ]*=)'
            r'(.*?$)'
        )
        PP_GUI_CATEGORIES = DICT_SETTINGS['metadata']['PP_GUI_CATEGORIES']
        if not PP_GUI_CATEGORIES.endswith(';'):
            PP_GUI_CATEGORIES += ';'
        rep_str = rf'\g<1>\g<2>\g<3>{PP_GUI_CATEGORIES}'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace exec
        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Exec[\t ]*=)'
            r'(.*?$)'
        )
        # TODO: look in $PATH
        PP_GUI_EXEC = DICT_SETTINGS['metadata']['PP_GUI_EXEC']
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
        PP_GUI_ICON = DICT_SETTINGS['metadata']['PP_GUI_ICON']
        rep_str = rf'\g<1>\g<2>\g<3>{PP_GUI_ICON}'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

    # save file
    with open(prj_desk, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the __init__.py file
# ------------------------------------------------------------------------------
def do_init():
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

def do_readme():
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
            r'(<!--[\t ]*__PP_SHORT_DESC_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__PP_SHORT_DESC_END__[\t ]*-->)'
        )
        PP_SHORT_DESC = DICT_SETTINGS['metadata']['PP_SHORT_DESC']
        rep_str = rf'\g<1>\n{PP_SHORT_DESC}\n\g<3>'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace dependencies array
        pattern_str = (
            r'(<!--[\t ]*__PP_PY_DEPS_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__PP_PY_DEPS_END__[\t ]*-->)'
        )
        PP_PY_DEPS = DICT_SETTINGS['metadata']['PP_PY_DEPS']
        split_str = _split_quote(PP_PY_DEPS, tabs=0, quote='', join='<br>')
        rep_str = rf'\g<1>\n{split_str}\g<3>'
        text = re.sub(pattern_str, rep_str, text, flags=re.M | re.S)

        # replace version
        pattern_vers = (
            r'(\s*foo@bar:~/Downloads\$ python -m pip install )'
            r'(.*-)'   # __PP_NAME_BIG__
            r'(.*?)'   # PP_VERSION
            r'(\.tar\.gz)'
        )
        PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
        rep_str = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
        text = re.sub(pattern_vers, rep_str, text)

        pattern_vers = (
            r'(\s*foo@bar:~/Downloads/)'
            r'(.*?)'   # __PP_NAME_BIG__
            r'(\$ python -m pip install ./dist/)'
            r'(.*-)'   # __PP_NAME_SMALL__
            r'(.*?)'   # PP_VERSION
            r'(\.tar\.gz)'
        )
        PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
        rep_str = rf'\g<1>\g<2>\g<3>\g<4>{PP_VERSION}\g<6>'
        text = re.sub(pattern_vers, rep_str, text)

        pattern_vers = (
            r'(\s*foo@bar:~\$ cd Downloads/)'
            r'(.*-)'   # __PP_NAME_BIG__
            r'(.*)'    # PP_VERSION
        )
        PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
        rep_str = rf'\g<1>\g<2>{PP_VERSION}'
        text = re.sub(pattern_vers, rep_str, text)

        pattern_vers = (
            r'(\s*foo@bar:~/Downloads/)'
            r'(.*-)'   # __PP_NAME_BIG__
            r'(.*)'    # PP_VERSION
            r'(\$ \./install.py)'
        )
        PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
        rep_str = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
        text = re.sub(pattern_vers, rep_str, text)

    # save file
    with open(prj_read, 'w', encoding='utf-8') as f:
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
    skip_all = [
        '.venv',
        '.git',
        'dist',
        'docs',
        'checklist.txt',
        'settings.json',
        'snippets.txt',
        'todo.txt',
        'tests',
        '__pycache__',
        'PKG-INFO',
    ]
    skip_headers = [
    ]
    skip_dunders = [
        'metadata.py',
        'README.md',
    ]
    skip_rename = [
    ]

    # strip trailing slashes to match path component
    skip_all = [item.strip('/') for item in skip_all]
    skip_headers = [item.strip('/') for item in skip_headers]
    skip_dunders = [item.strip('/') for item in skip_dunders]
    skip_rename = [item.strip('/') for item in skip_rename]

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

                # check headers of every file
                if item not in skip_headers:
                    _check_headers(path_item, lines)

                # don't check contents of metadata.py
                if item not in skip_dunders:
                    _check_dunders(path_item, lines)

        # check file paths (subdirs and such)
        if item not in skip_rename:
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
        '__PP_NAME_SMALL__.egg-info',
            path_item [string]: the full path to file to be checked
            lines [array]: the contents of the file to be checked

        This function checks the files headers for values that either do not
        match the file's project/file name, or do not have a date set.
    """

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
            global err_cnt
            err_cnt += 1

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
            global err_Cnt
            err_cnt += 1

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
                    global err_Cnt
                    err_cnt += 1

            else:
                print(f'{path_item}:{i + 1}: Header Date is not set')

                # inc error count
                global err_Cnt
                err_cnt += 1


# ------------------------------------------------------------------------------
# Checks file contents for dunders
# ------------------------------------------------------------------------------
def _check_dunders(path_item, lines):
    """
        Checks file contents for dunders

        Paramaters:
            path_item [string]: the full path to file to be checked for text
            lines [array]: the contents of the file to be checked

        This function checks that none of the files contains an unreplaced
        dunder variable from the initial project info.
    """

    for i in range(0, len(lines)):
        line = lines[i]

        # the dunders to look for
        reps = [rep for rep in DICT_SETTINGS['info'] and
                DICT_SETTINGS['metadata']]

        # check for dunders in text
        for rep in reps:
            if rep in line:
                print(f'{path_item}:{i + 1}: Text contains {rep}')

                # inc error count
                global err_cnt
                err_cnt += 1


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

    # check for dunders in path
    if '__PP_' in path_item:
        print(f'{path_item}: Path contains __PP_')

        # inc error count
        global err_cnt
        err_cnt += 1


# ------------------------------------------------------------------------------
# A helper function to split keywords and dependencies
# ------------------------------------------------------------------------------
def _split_quote(str_in, tabs=1, split=',', quote='"', join=','):
    """
        A helper function to split keywords and dependencies

        Paramaters:
            str_in [string]: the string to split tabs [string]: number of tabs
            at the beginning of every line split [string]: the character to
            split on quote [string]: the character to use to quote each entry
            (or empty) join [string]: the character to join each line in the
            output

        Returns:
            [string]: a new string which is split, quoted, joined, and tabbed

        This function takes a string and splits it using the splt param, then
        rejoins it using the quote param, the join param, and the number of tabs
        to create a nice-looking list.

        For example, the input string 'foo,bar' using the default parameters
        will produce the following output:

        \t"foo",
        \t"bar"\n

    """

    # first split the list using the split char
    split_lst = str_in.split(split)

    # blank strings, when split w/param, still contain 1 entry
    # https://stackoverflow.com/questions/16645083/when-splitting-an-empty-string-in-python-why-does-split-return-an-empty-list
    # so we do the list comprehension BEFORE testing the list length
    # quote items and put into new list
    split_lst = [f'{quote}{item}{quote}' for item in split_lst if item != '']

    # if the list is empty, return empty result
    if len(split_lst) == 0:
        return ''

    # create tab_str and join items using tabs and join char
    # "foo",
    #     "bar"
    tab_str = '\t' * tabs
    split_lst_str = f'{join}\n{tab_str}'.join(split_lst)

    # put tabs at start of string and newline at end
    #     "foo",
    #     "bar"
    #
    split_lst_str = f'{tab_str}{split_lst_str}\n'

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
