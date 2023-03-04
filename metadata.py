#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: metadata.py                                           |     ()     |
# Date    : 12/22/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import os
import re

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# this is the dir where the script is being run from
DIR_CURR = os.path.abspath(os.path.dirname(__file__))

# this is the canonical (only and absolute) version number string for this
# project
# this should provide the absolute version number string (in semantic notation)
# of this project, and all other version numbers should be superceded by this
# string
# format is N.N.N
CN_VERSION = '0.1.0'

# these are the short description, keywords, and dependencies for the project
# they are stored here for projects that don't use pyproject.toml
# these will be used in the GitHub repo
# delimiters for CN_KEYWORDS and CN_XXX_DEPS MUST be comma
CN_SHORT_DESC = (
    'A template for creating packages/modules/CLI apps/GTK3 apps in Python'
)
CN_KEYWORDS = (
    'python,python3,template,project,module,package,cli,gui,linux,ubuntu,gtk,'
    'gtk3,gtk4'
)
CN_SYS_DEPS = ''
CN_PY_DEPS = ''

# gui categories MUST be seperated by semicolon and MUST end with semicolon
# this is mostly for desktops that use a windows-stylew menu/submenu, not for
# Ubuntu-style overviews
CN_GUI_CATEGORIES = ''

# if exec/icon paths are not absolute, they will be found in standard paths
# these paths vary, but I will add them here in the comments when I figure them
# out
CN_GUI_EXEC = ''
CN_GUI_ICON = ''

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main function of the module
# ------------------------------------------------------------------------------
def main():
    """
        The main function of the module

        This function is the main entry point for the module, initializing the
        module, and performing it's steps.
    """

    # do proactive replacements (replaces needed text)
    do_toml()
    do_install()
    do_desktop()
    do_readme()

    # do preventative checks (does not replace anything, just prints/warns)
    recurse(DIR_CURR)


# ------------------------------------------------------------------------------
# Replace text in the pyproject.toml file
# ------------------------------------------------------------------------------
def do_toml():
    """
        Replace text in the pyproject.toml file

        Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # TODO: deps must have version?

    # this function will ALWAYS create a multi-line array, e.g.:
    # keywords = [
    #     "foo",
    #     "bar"
    # ]
    # even if the input file's array was a single line or multiline
    # also if the input file's array was empty or not

    # check if the file exists
    prj_toml = os.path.join(DIR_CURR, 'pyproject.toml')
    if not os.path.exists(prj_toml):
        return

    # open file and get contents
    with open(prj_toml) as file:
        text = file.read()

    # replace version
    pattern_str = (
        r'(^\s*\[project\]\s*$)'
        r'(.*?)'
        r'(^\s*version[\t ]*=)'
        r'(.*?$)'
    )
    rep_str = rf'\g<1>\g<2>\g<3> "{CN_VERSION}"'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # replace short description
    pattern_str = (
        r'(^\s*\[project\]\s*$)'
        r'(.*?)'
        r'(^\s*description[\t ]*=)'
        r'(.*?$)'
    )
    rep_str = rf'\g<1>\g<2>\g<3> "{CN_SHORT_DESC}"'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # replace keywords array
    pattern_str = (
        r'(^\s*\[project\]\s*$)'
        r'(.*?)'
        r'(^\s*keywords[\t ]*=)'
        r'(.*?\])'
    )
    split_str = split_quote(CN_KEYWORDS)
    rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # replace dependencies array
    pattern_str = (
        r'(^\s*\[project\]\s*$)'
        r'(.*?)'
        r'(^\s*dependencies[\t ]*=)'
        r'(.*?\])'
    )
    split_str = split_quote(CN_PY_DEPS)
    rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # save file
    with open(prj_toml, 'w') as file:
        file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the install file
# ------------------------------------------------------------------------------
def do_install():
    """
        Replace text in the install file

        Replaces the system and Python dependencies in the install file.
    """

    # check if the file exists
    prj_inst = os.path.join(DIR_CURR, 'install.py')
    if not os.path.exists(prj_inst):
        return

    # open file and get content
    with open(prj_inst) as file:
        text = file.read()

    # replace system dependencies array
    pattern_str = (
        r'(^\s*dict_install[\t ]*=)'
        r'(.*?)'
        r'(^\s*\'sys_deps\'[\t ]*:)'
        r'(.*?\])'
    )
    split_str = split_quote(CN_SYS_DEPS, tabs=2)
    rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\t\]'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # replace python dependencies array
    pattern_str = (
        r'(^\s*dict_install[\t ]*=\s*{)'
        r'(.*?)'
        r'(^\s*\'py_deps\'[\t ]*:)'
        r'(.*?\])'
    )
    split_str = split_quote(CN_PY_DEPS, tabs=2)
    rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\t\]'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # save file
    with open(prj_inst, 'w') as file:
        file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the desktop file
# ------------------------------------------------------------------------------
def do_desktop():
    """
        Replace text in the desktop file

        Replaces the icon, executable, and category text in a .desktop file for
        programs that use this.
    """

    # TODO: what about exec/icon?

    # since we don't do replacements in this file, we need to get the path to
    # the desktop file without knowing the project's CN_NAME_SMALL value

    # first get the gui dir
    gui_dir = os.path.join(DIR_CURR, 'gui')
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
    with open(prj_desk) as file:
        text = file.read()

    # replace categories
    pattern_str = (
        r'(^\s*\[Desktop Entry\]\s*$)'
        r'(.*?)'
        r'(^\s*Categories[\t ]*=)'
        r'(.*?$)'
    )
    cat_str = CN_GUI_CATEGORIES
    if not cat_str.endswith(';'):
        cat_str = cat_str + ';'
    rep_str = rf'\g<1>\g<2>\g<3>{cat_str}'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # replace short description
    pattern_str = (
        r'(^\s*\[Desktop Entry\]\s*$)'
        r'(.*?)'
        r'(^\s*Comment[\t ]*=)'
        r'(.*?$)'
    )
    rep_str = rf'\g<1>\g<2>\g<3>{CN_SHORT_DESC}'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # save file
    with open(prj_desk, 'w') as file:
        file.write(text)


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
    prj_read = os.path.join(DIR_CURR, 'README.md')
    if not os.path.exists(prj_read):
        return

    # open file and get contents
    with open(prj_read) as file:
        text = file.read()

    # replace short description
    pattern_str = (
        r'(<!--[\t ]*__CN_SHORT_DESC_START__[\t ]*-->)'
        r'(.*?)'
        r'(<!--[\t ]*__CN_SHORT_DESC_END__[\t ]*-->)'
    )
    rep_str = rf'\g<1>\n{CN_SHORT_DESC}\n\g<3>'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # replace dependencies array
    pattern_str = (
        r'(<!--[\t ]*__CN_PY_DEPS_START__[\t ]*-->)'
        r'(.*?)'
        r'(<!--[\t ]*__CN_PY_DEPS_END__[\t ]*-->)'
    )
    split_str = split_quote(CN_PY_DEPS, tabs=0, quote='', join='')
    rep_str = rf'\g<1>\n{split_str}\g<3>'
    text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

    # replace version
    pattern_py = (
        r'(^\s*foo@bar:~/Downloads\$ python -m pip install )'
        r'(.*-)'   # CN_NAME_BIG
        r'(.*?)'   # CN_VERSION
        r'(\.tar\.gz$)'
    )
    rep_str = rf'\g<1>\g<2>{CN_VERSION}\g<4>'
    text = re.sub(pattern_py, rep_str, text, 1, re.I | re.M)

    pattern_py = (
        r'(^\s*foo@bar:~/Downloads/)'
        r'(.*?)'   # CN_NAME_BIG
        r'(\$ python -m pip install ./dist/)'
        r'(.*-)'   # CN_NAME_SMALL
        r'(.*?)'   # CN_VERSION
        r'(\.tar\.gz -r ./requirements.txt$)'
    )
    rep_str = rf'\g<1>\g<2>\g<3>\g<4>{CN_VERSION}\g<6>'
    text = re.sub(pattern_py, rep_str, text, 1, re.I | re.M)

    pattern_py = (
        r'(^\s*foo@bar:~\$ cd Downloads/)'
        r'(.*-)'   # CN_NAME_BIG
        r'(.*$)'   # CN_VERSION
    )
    rep_str = rf'\g<1>\g<2>{CN_VERSION}'
    text = re.sub(pattern_py, rep_str, text, 1, re.I | re.M)

    pattern_py = (
        r'(^\s*foo@bar:~/Downloads/)'
        r'(.*-)'   # CN_NAME_BIG
        r'(.*)'   # CN_VERSION
        r'(\$ \./install.py$)'
    )
    rep_str = rf'\g<1>\g<2>{CN_VERSION}\g<4>'
    text = re.sub(pattern_py, rep_str, text, 1, re.I | re.M)

    # save file
    with open(prj_read, 'w') as file:
        file.write(text)


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

    # don't rename these dirs or files, or change file contents
    # also trim any trailing '/'
    skip_dirs = [
        'misc',
        'template'
    ]
    skip_dirs = [item.rstrip('/') for item in skip_dirs]

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
            with open(path_item) as file:
                text = file.read()

            # check headers of every file
            check_headers(path_item, text)

            # don't check contents of metadata.py
            if item != 'metadata.py':
                check_dunders(path_item, text)

        # check file paths (subdirs and such)
        check_path(path_item)


# ------------------------------------------------------------------------------
# Checks header values for dunders
# ------------------------------------------------------------------------------
def check_headers(path_item, text):
    """
        Checks header values for dunders

        Paramaters:
            path_item [string]: the full path to file to be checked
            text [string]: the contents of the file to be checked

        This function checks the files headers for values that either do not
        match the file's project/file name, or do not have a date set.
    """

    # check project name
    proj_name = os.path.basename(DIR_CURR)
    pattern = (
        r'(^\s*(<!--|#) Project : )'
        r'(.*?)'
        r'(\s)'
    )
    res = re.search(pattern, text, re.I | re.M)
    if res and proj_name != res.group(3):
        print(f'{path_item}: Header Project name should be \'{proj_name}\'')

    # check file name
    file_name = os.path.basename(path_item)
    pattern = (
        r'(^\s*(<!--|#) Filename : )'
        r'(.*?)'
        r'(\s)'
    )
    res = re.search(pattern, text, re.I | re.M)
    if res and file_name != res.group(3):
        print(f'{path_item}: Header Filename should be \'{file_name}\'')

    # check date
    pattern = (
        r'(^\s*(<!--|#) Date    : )'
        r'(__CN_DATE.*?)'
        r'(\s)'
    )
    res = re.search(pattern, text, re.I | re.M)
    if res:
        print(f'{path_item}: Header Date is not set')


# ------------------------------------------------------------------------------
# Checks file contents for dunders
# ------------------------------------------------------------------------------
def check_dunders(path_item, text):
    """
        Checks file contents for dunders

        Paramaters:
            path_item [string]: the full path to file to be checked for text
            text [string]: the contents of the file to be checked

        This function checks that none of the files contains an unreplaced
        dunder variable from the initial project info.
    """

    # check for dunders in text
    pattern = r'__CN_.*?__'
    res = re.search(pattern, text, re.I | re.M)
    if res:
        print(f'{path_item}: Text contains {res.group(0)}')


# ------------------------------------------------------------------------------
# Checks file paths for dunders
# ------------------------------------------------------------------------------
def check_path(path_item):
    """
        Checks file paths for dunders

        Paramaters:
            path_item [string]: the full path to file to be checked for text

        This function checks that none of the files paths contains an unreplaced
        dunder variable from the initial project info.
    """

    # check for dunders in path
    pattern = r'__CN_.*?__'
    res = re.search(pattern, path_item, re.I | re.M)
    if res:
        print(f'{path_item}: Path contains {res.group(0)}')


# ------------------------------------------------------------------------------
# A helper function to split keywords and dependencies
# ------------------------------------------------------------------------------
def split_quote(str_in, tabs=1, split=',', quote='"', join=','):
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
