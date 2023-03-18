#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : ModTest                                                /          \
# Filename: metadata.py                                           |     ()     |
# Date    : 03/17/2023                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import json
import os
import re

# TODO: text in pp_argparse
# TODO: text in empty_main
# TODO: text in README

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# this is the dir where the script is being run from
this_dir = os.path.dirname(__file__)
DIR_CURR = os.path.abspath(this_dir)

# this is the project dir
prj_dir = os.path.join(this_dir, '..')
DIR_PROJ = os.path.abspath(prj_dir)

# load settings file
file_settings = os.path.join(DIR_CURR, 'settings.json')
path_settings = os.path.abspath(file_settings)
if os.path.exists(path_settings):
    with open(file_settings, 'r', encoding='utf-8') as f:
        DICT_SETTINGS = json.load(f)


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
    do_readme()

    # do preventative checks (does not replace anything, just prints/warns)
    # NOT ENTIRELY TRUE - it DOES do version/desc replacement in .py files that
    # have a parse_args() function
    recurse(DIR_PROJ)


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
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # replace short description
    pattern_str = (
        r'(^\s*\[project\]\s*$)'
        r'(.*?)'
        r'(^\s*description[\t ]*=)'
        r'(.*?$)'
    )
    PP_SHORT_DESC = DICT_SETTINGS['metadata']['PP_SHORT_DESC']
    rep_str = rf'\g<1>\g<2>\g<3> "{PP_SHORT_DESC}"'
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # replace keywords array
    pattern_str = (
        r'(^\s*\[project\]\s*$)'
        r'(.*?)'
        r'(^\s*keywords[\t ]*=)'
        r'(.*?\])'
    )
    PP_KEYWORDS = DICT_SETTINGS['metadata']['PP_KEYWORDS']
    split_str = _split_quote(PP_KEYWORDS)
    rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

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
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

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
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

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
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

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

    # since we don't do replacements in this file, we need to get the path to
    # the desktop file without knowing the project's PP_NAME_SMALL value

    # first get the gui dir
    gui_dir = os.path.join(DIR_PROJ, 'gui')
    if not os.path.exists(gui_dir):
        return

    # next list all files in gui dir
    gui_files = os.listdir(gui_dir)
    if len(gui_files) == 0:
        return

    # then get a list of all the files ending in .desktop
    desk = [item for item in gui_files if
            os.path.splitext(item)[1] == '.desktop']
    if len(desk) == 0:
        return

    # check if the file exists
    prj_desk = os.path.join(gui_dir, desk[0])
    if not os.path.exists(prj_desk):
        return

    # open file and get contents
    with open(prj_desk, 'r', encoding='utf-8') as f:
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
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # replace categories
    pattern_str = (
        r'(^\s*\[Desktop Entry\]\s*$)'
        r'(.*?)'
        r'(^\s*Categories[\t ]*=)'
        r'(.*?$)'
    )
    PP_GUI_CATEGORIES = DICT_SETTINGS['metadata']['PP_GUI_CATEGORIES']
    if not PP_GUI_CATEGORIES.endswith(';'):
        PP_GUI_CATEGORIES = PP_GUI_CATEGORIES + ';'
    rep_str = rf'\g<1>\g<2>\g<3>{PP_GUI_CATEGORIES}'
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # replace exec
    pattern_str = (
        r'(^\s*\[Desktop Entry\]\s*$)'
        r'(.*?)'
        r'(^\s*Exec[\t ]*=)'
        r'(.*?$)'
    )
    PP_GUI_EXEC = DICT_SETTINGS['metadata']['PP_GUI_EXEC']
    rep_str = rf'\g<1>\g<2>\g<3>{PP_GUI_EXEC}'
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # replace icon
    pattern_str = (
        r'(^\s*\[Desktop Entry\]\s*$)'
        r'(.*?)'
        r'(^\s*Icon[\t ]*=)'
        r'(.*?$)'
    )
    PP_GUI_ICON = DICT_SETTINGS['metadata']['PP_GUI_ICON']
    rep_str = rf'\g<1>\g<2>\g<3>{PP_GUI_ICON}'
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # save file
    with open(prj_desk, 'w', encoding='utf-8') as f:
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
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # replace dependencies array
    pattern_str = (
        r'(<!--[\t ]*__PP_PY_DEPS_START__[\t ]*-->)'
        r'(.*?)'
        r'(<!--[\t ]*__PP_PY_DEPS_END__[\t ]*-->)'
    )
    PP_PY_DEPS = DICT_SETTINGS['metadata']['PP_PY_DEPS']
    split_str = _split_quote(PP_PY_DEPS, tabs=0, quote='', join='<br>')
    rep_str = rf'\g<1>\n{split_str}\g<3>'
    text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

    # replace version
    pattern_vers = (
        r'(^\s*foo@bar:~/Downloads\$ python -m pip install )'
        r'(.*-)'   # __PP_NAME_BIG__
        r'(.*?)'   # PP_VERSION
        r'(\.tar\.gz$)'
    )
    PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
    rep_str = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
    text = re.sub(pattern_vers, rep_str, text, re.I | re.M)

    pattern_vers = (
        r'(^\s*foo@bar:~/Downloads/)'
        r'(.*?)'   # __PP_NAME_BIG__
        r'(\$ python -m pip install ./dist/)'
        r'(.*-)'   # __PP_NAME_SMALL__
        r'(.*?)'   # PP_VERSION
        r'(\.tar\.gz$)'
    )
    PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
    rep_str = rf'\g<1>\g<2>\g<3>\g<4>{PP_VERSION}\g<6>'
    text = re.sub(pattern_vers, rep_str, text, re.I | re.M)

    pattern_vers = (
        r'(^\s*foo@bar:~\$ cd Downloads/)'
        r'(.*-)'   # __PP_NAME_BIG__
        r'(.*$)'   # PP_VERSION
    )
    PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
    rep_str = rf'\g<1>\g<2>{PP_VERSION}'
    text = re.sub(pattern_vers, rep_str, text, re.I | re.M)

    pattern_vers = (
        r'(^\s*foo@bar:~/Downloads/)'
        r'(.*-)'   # __PP_NAME_BIG__
        r'(.*)'    # PP_VERSION
        r'(\$ \./install.py$)'
    )
    PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
    rep_str = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
    text = re.sub(pattern_vers, rep_str, text, re.I | re.M)

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

    # don't replace headers, text, or names for these folders/files
    skip_dirs = [
        '.venv',
        '.git'
    ]
    # skip_headers = [
    # ]
    # skip_text = [
    #     'metadata.py'
    # ]
    # skip_rename = [
    # ]

    # strip trailing slashes to match path component
    skip_dirs = [item.rstrip('/') for item in skip_dirs]
    # skip_headers = [item.rstrip('/') for item in skip_headers]
    # skip_text = [item.rstrip('/') for item in skip_text]
    # skip_rename = [item.rstrip('/') for item in skip_rename]

    # get list of replaceable file names
    items = [item for item in os.listdir(path) if item not in skip_dirs]
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
            # if item not in skip_headers:
            _check_headers(path_item, lines)

            # don't check contents of metadata.py
            # if item not in skip_text:
            if (
                item != 'metadata.py' and
                item != 'settings.json'
            ):
                _check_dunders(path_item, lines)

            # check fo parse_args method
            _check_parse_args(path_item, lines)

        # check file paths (subdirs and such)
        # if item not in skip_rename:
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
            text [string]: the contents of the file to be checked

        This function checks the files headers for values that either do not
        match the file's project/file name, or do not have a date set.
    """

    # check project name
    proj_name = os.path.basename(DIR_PROJ)
    pattern = (
        r'(^\s*(<!--|#)\s*)'
        r'(Project)'
        r'(\s*:\s*)'
        r'(.*?)'
        r'(\s)'
    )
    for i in range(0, len(lines)):
        res = re.search(pattern, lines[i], re.I | re.M)
        if res and res.group(5) != proj_name:
            print(f'{path_item}:{i + 1}: Header Project name should be \'{proj_name}\'')

    # check file name
    file_name = os.path.basename(path_item)
    pattern = (
        r'(^\s*(<!--|#)\s*)'
        r'(Filename)'
        r'(\s*:\s*)'
        r'(.*?)'
        r'(\s)'
    )
    for i in range(0, len(lines)):
        res = re.search(pattern, lines[i], re.I | re.M)
        if res and res.group(5) != file_name:
            print(f'{path_item}:{i + 1}: Header Filename should be \'{file_name}\'')

    # check date
    pattern = (
        r'(^\s*(<!--|#)\s*)'
        r'(Date)'
        r'(\s*:\s*)'
        r'(.*?)'
        r'(\s)'
    )
    for i in range(0, len(lines)):
        res = re.search(pattern, lines[i], re.I | re.M)
        if res:

            # there is *something* in the date field
            if res.group(5) != '':

                # check for valid date
                pattern2 = r'\d*/\d*/\d*'
                res2 = re.search(pattern2, res.group(5), re.I | re.M)
                if not res2:
                    print(f'{path_item}:{i + 1}: Header Date is not set')
            else:
                print(f'{path_item}:{i + 1}: Header Date is not set')


# ------------------------------------------------------------------------------
# Checks file contents for dunders
# ------------------------------------------------------------------------------
def _check_dunders(path_item, lines):
    """
        Checks file contents for dunders

        Paramaters:
            path_item [string]: the full path to file to be checked for text
            text [string]: the contents of the file to be checked

        This function checks that none of the files contains an unreplaced
        dunder variable from the initial project info.
    """

    # TODO get these from dict_settings['info'], dict_settings['metadata']
    # the dunders to look for
    reps = [rep for rep in DICT_SETTINGS['info'] and DICT_SETTINGS['metadata']]
    # reps = [
    #     '__PP_NAME_BIG__',
    #     '__PP_NAME_SMALL__',
    #     '__PP_DATE__',
    #     'PP_VERSION',
    #     'PP_SHORT_DESC',
    #     'pp_KEYWORDS',
    #     'PP_PY_DEPS',
    #     'PP_SYS_DEPS',
    # ]

    # check for dunders in text
    for rep in reps:
        pattern = rf'{rep}'
        for i in range(0, len(lines)):
            res = re.findall(pattern, lines[i], re.I | re.M)
            if res:
                for item in res:
                    print(f'{path_item}:{i + 1}: Text contains {item}')


# ------------------------------------------------------------------------------
# Checks file contents for parse_args
# ------------------------------------------------------------------------------
def _check_parse_args(path_item, lines):
    """
        Checks file contents for parse_args

        Paramaters:
            path_item [string]: the full path to file to be checked for text
            text [string]: the contents of the file to be checked

        This function checks that none of the files paths contains an unreplaced
        dunder variable from the initial project info.
    """

# TODO: this should be done with replace and then checked again after

    # first check if path ends in .py
    if os.path.splitext(path_item) == 'py':

        # check for regex
        pattern_str = (
            r'(^def _parse_args\(\):.*?print\(\'.*?version )'
            r'(.*?)'
            r'(\'\))'
        )
        PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
        rep_str = rf'\g<1>{PP_VERSION}\g<3>'
        text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)

        pattern_str = (
            r'(^def _parse_args\(\):.*?parser.add_argument.*version=\')'
            r'(.*?)'
            r'(\')'
        )
        PP_VERSION = DICT_SETTINGS['metadata']['PP_VERSION']
        rep_str = rf'\g<1>{PP_VERSION}\g<3>'
        text = re.sub(pattern_str, rep_str, text, e.I | re.M | re.S)

        pattern_str = (
            r'(^def _parse_args\(\):.*?description=\')'
            r'(.*?)'
            r'(\')'
        )
        PP_SHORT_DESC = DICT_SETTINGS['metadata']['PP_SHORT_DESC']
        rep_str = rf'\g<1>{PP_SHORT_DESC}\g<3>'
        text = re.sub(pattern_str, rep_str, text, re.I | re.M | re.S)


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
    pattern = r'__PP_.*?__'
    res = re.search(pattern, path_item, re.I | re.M)
    if res:
        print(f'{path_item}: Path contains {res.group(0)}')


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
        \t"bar"

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

