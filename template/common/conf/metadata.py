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
from glob import glob
import json
import os
import re
import shlex
import subprocess

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# this is the project dir
dir = os.path.dirname(__file__)
dir_prj = os.path.join(dir, '..')
DIR_PRJ = os.path.abspath(dir_prj)

# load blacklist file
DICT_BLACKLIST = []
path_blacklist = os.path.join(DIR_PRJ, 'conf', 'blacklist.json')
if os.path.exists(path_blacklist):
    with open(path_blacklist, 'r', encoding='utf-8') as f:
        try:
            DICT_BLACKLIST = json.load(f)
        except (Exception):
            print(f'{f} is not a valid JSON file')
            exit()

# load metadata file
DICT_METADATA = []
path_metadata = os.path.join(DIR_PRJ, 'conf', 'metadata.json')
if os.path.exists(path_metadata):
    with open(path_metadata, 'r', encoding='utf-8') as f:
        try:
            DICT_METADATA = json.load(f)
        except (Exception):
            print(f'{f} is not a valid JSON file')
            exit()

# load settings file
DICT_SETTINGS = []
path_settings = os.path.join(DIR_PRJ, 'conf', 'settings.json')
if os.path.exists(path_settings):
    with open(path_settings, 'r', encoding='utf-8') as f:
        try:
            DICT_SETTINGS = json.load(f)
        except (Exception):
            print(f'{f} is not a valid JSON file')
            exit()

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# keep track of error count
g_err_cnt = 0


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

    # do proactive replacements in specific files (replaces needed text)

    # common
    fix_readme()

    # mod/pkg
    fix_pyproject()

    # pkg
    fix_init()

    # cli/gui
    fix_argparse()
    fix_install()

    # gui
    fix_desktop()
    fix_ui()

    # check for __PP_ /PP_ stuff left over or we missed
    recurse(DIR_PRJ)

    # do housekeeping
    do_extras()

    # print error count (__PP_/PP_ stuff found)
    print(f'Errors: {g_err_cnt}')


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
    path_readme = os.path.join(DIR_PRJ, 'README.md')
    if not os.path.exists(path_readme):
        return

    # open file and get contents
    with open(path_readme, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace short description
        str_pattern = (
            r'(<!--[\t ]*__RM_SHORT_DESC_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__RM_SHORT_DESC_END__[\t ]*-->)'
        )

        # get short description
        pp_short_desc = DICT_METADATA['PP_SHORT_DESC']

        # replace text
        str_rep = rf'\g<1>\n{pp_short_desc}\n\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace dependencies array
        str_pattern = (
            r'(<!--[\t ]*__RM_PY_DEPS_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__RM_PY_DEPS_END__[\t ]*-->)'
        )

        # build a string from the dict (markdown link)
        pp_py_deps = DICT_METADATA['PP_PY_DEPS']
        lst_py_deps = [f'[{key}]({val})' for (key, val) in pp_py_deps.items()]
        str_py_deps = ','.join(lst_py_deps)

        # split the string for README
        str_split = _split_quote(str_py_deps, join='<br>\n', tail='\n')
        if str_split == '':
            str_split = 'None\n'

        # replace text
        str_rep = rf'\g<1>\n{str_split}\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        pp_version = DICT_METADATA['PP_VERSION']

        str_pattern = (
            r'(\s*foo@bar:~/Downloads\$ python -m pip install )'
            r'(.*-)'
            r'(.*?)'
            r'(\.tar\.gz)'
        )
        str_rep = rf'\g<1>\g<2>{pp_version}\g<4>'
        text = re.sub(str_pattern, str_rep, text)

        str_pattern = (
            r'(\s*foo@bar:~/Downloads/)'
            r'(.*?)'
            r'(\$ python -m pip install ./dist/)'
            r'(.*-)'
            r'(.*?)'
            r'(\.tar\.gz)'
        )
        str_rep = rf'\g<1>\g<2>\g<3>\g<4>{pp_version}\g<6>'
        text = re.sub(str_pattern, str_rep, text)

        str_pattern = (
            r'(\s*foo@bar:~\$ cd ~/Downloads/)'
            r'(.*-)'
            r'(.*)'
        )
        str_rep = rf'\g<1>\g<2>{pp_version}'
        text = re.sub(str_pattern, str_rep, text)

        str_pattern = (
            r'(\s*foo@bar:~/Downloads/)'
            r'(.*-)'
            r'(.*)'
            r'(\$ \./install.py)'
        )
        str_rep = rf'\g<1>\g<2>{pp_version}\g<4>'
        text = re.sub(str_pattern, str_rep, text)

    # save file
    with open(path_readme, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the pyproject file
# ------------------------------------------------------------------------------
def fix_pyproject():
    """
        Replace text in the pyproject file

        Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # check if the file exists
    path_toml = os.path.join(DIR_PRJ, 'pyproject.toml')
    if not os.path.exists(path_toml):
        return

    # open file and get contents
    with open(path_toml, 'r', encoding='utf-8') as f:
        text = f.read()

        # NB: we do a dunder replace here because putting a dunder as the
        # default name in the toml file causes the linter to choke, so we use a
        # dummy name

        # replace name
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*name[\t ]*=[\t ]*)'
            r'(.*?$)'
        )
        pp_name = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
        str_rep = rf'\g<1>\g<2>\g<3>"{pp_name}"'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*version[\t ]*=[\t ]*)'
            r'(.*?$)'
        )
        pp_version = DICT_METADATA['PP_VERSION']
        str_rep = rf'\g<1>\g<2>\g<3>"{pp_version}"'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace short description
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*description[\t ]*=[\t ]*)'
            r'(.*?$)'
        )
        pp_short_desc = DICT_METADATA['PP_SHORT_DESC']
        str_rep = rf'\g<1>\g<2>\g<3>"{pp_short_desc}"'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # # replace keywords array
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*keywords[\t ]*=[\t ]*)'
            r'(.*?\])'
        )

        # convert dict to string
        pp_keywords = DICT_METADATA['PP_KEYWORDS']
        str_split = _split_quote(pp_keywords, quote='"', lead='\t',
                                 join=',\n\t', tail='\n')

        # replace string
        str_rep = rf'\g<1>\g<2>\g<3>[\n{str_split}]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace dependencies array
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*dependencies[\t ]*=[\t ]*)'
            r'(.*?\])'
        )

        # convert dict to string (only using keys)
        pp_py_deps = DICT_METADATA['PP_PY_DEPS']

        # NB: this is not conducive to a dict (we don't need links, only names)
        # so don't do what we did in README, keep it simple
        str_py_deps = ','.join(pp_py_deps.keys())

        # split the string for pyproject
        str_split = _split_quote(str_py_deps, quote='"', lead='\t',
                                 join=',\n\t', tail='\n')

        # replace text
        str_rep = rf'\g<1>\g<2>\g<3>[\n{str_split}]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_toml, 'w', encoding='utf-8') as f:
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

    # first check if there is a pkg dir
    dir_pkg = os.path.join(DIR_PRJ, 'src', '__PP_NAME_SMALL__')
    if not os.path.exists(dir_pkg) or not os.path.isdir(dir_pkg):
        return

    # the file name of the init
    file_init = '__init__.py'

    # check if there is an __init__.py file
    path_init = os.path.join(dir_pkg, file_init)
    if not os.path.exists(path_init):
        return

    # check if there are any .py files in package dir that are not init file
    lst_modules = [item for item in os.listdir(dir_pkg)
                   if item != file_init and os.path.splitext(item)[1] == 'py']
    if len(lst_modules) == 0:
        return

    # strip ext and add to list
    lst_files = [os.path.splitext(item)[0] for item in lst_modules]

    # sort file list to look pretty (listdir is not sorted)
    lst_files.sort()

    # format list for imports section
    lst_imports = [
        f'from {pp_small} import {item}  # noqa: W0611 (unused import)'
        for item in lst_files
    ]
    str_imports = '\n'.join(lst_imports)

    # format __all__ for completeness
    lst_all = [f'\'{item}\'' for item in lst_files]
    str_all_join = ', '.join(lst_all)
    str_all = f'__all__ = [{str_all_join}]'

    # open file and get contents
    with open(path_init, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace imports block
        str_pattern = (
            r'(^#[\t ]*__PP_IMPORTS_START__[\t ]*)'
            r'(.*?)'
            r'(^#[\t ]*__PP_IMPORTS_END__[\t ]*)'
        )
        str_rep = rf'\g<1>\n{str_imports}\n{str_all}\n\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_init, 'w', encoding='utf-8') as f:
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
    dir_src = os.path.join(DIR_PRJ, 'src')

    # get all paths
    lst_paths = [os.path.join(dir_src, item) for item in os.listdir(dir_src)]
    if len(lst_paths) == 0:
        return

    # get all files
    lst_files = [item for item in lst_paths if os.path.isfile(item) and
                 os.path.splitext(item)[1] == '.py']

    # for each file
    for item in lst_files:

        # get the whole path
        path_item = os.path.join(dir_src, item)

        # check if file exists
        if not os.path.exists(path_item) or os.path.isdir(path_item):
            continue

        # open file and get contents
        with open(path_item, 'r', encoding='utf-8') as f:
            text = f.read()

            # replace short description
            str_pattern = (
                r'(import argparse.*def _parse_args\(\):.*)'
                r'(argparse.ArgumentParser\(\s*description=\')'
                r'(.*?)'
                r'(\'.*)'
            )
            PP_SHORT_DESC = DICT_METADATA['PP_SHORT_DESC']
            str_rep = rf'\g<1>\g<2>{PP_SHORT_DESC}\g<4>'
            text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

            # replace version
            str_pattern = (
                r'(import argparse.*def _parse_args\(\):.*)'
                r'(print\(\'.* version )'
                r'(.*?)'
                r'(\'.*)'
            )
            PP_VERSION = DICT_METADATA['PP_VERSION']
            str_rep = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
            text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # save file
        with open(path_item, 'w', encoding='utf-8') as f:
            f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the install file
# ------------------------------------------------------------------------------
def fix_install():
    """
        Replace text in the install file

        Replaces the system and Python dependencies in the install file.
    """

    # check if the file exists
    path_install = os.path.join(DIR_PRJ, 'install.py')
    if not os.path.exists(path_install):
        return

    # open file and get content
    with open(path_install, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace python dependencies array
        str_pattern = (
            r'(^\s*dict_install[\t ]*=\s*{)'
            r'(.*?)'
            r'(^\s*\'py_deps\'[\t ]*:)'
            r'(.*?\])'
        )

        # convert dict keys to string
        PP_PY_DEPS = DICT_METADATA['PP_PY_DEPS']
        str_py_deps = ','.join(PP_PY_DEPS.keys())
        str_split = _split_quote(str_py_deps, quote='"', lead='\t\t',
                                 join=',\n\t\t')

        # replace text
        str_rep = rf'\g<1>\g<2>\g<3> [\n{str_split}\n\t]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace system dependencies array
        str_pattern = (
            r'(^\s*dict_install[\t ]*=)'
            r'(.*?)'
            r'(^\s*\'sys_deps\'[\t ]*:)'
            r'(.*?\])'
        )

        # convert dict to string
        PP_SYS_DEPS = DICT_METADATA['PP_SYS_DEPS']
        str_split = _split_quote(PP_SYS_DEPS, quote='"', lead='\t\t',
                                 join=',\n\t\t')

        # replace string
        str_rep = rf'\g<1>\g<2>\g<3> [\n{str_split}\n\t]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_install, 'w', encoding='utf-8') as f:
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

    # check if the file exists
    path_desk = os.path.join(DIR_PRJ, 'src', 'gui', '__PP_NAME_BIG__.desktop')
    if not os.path.exists(path_desk):
        return

    # open file and get contents
    with open(path_desk, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace short description
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Comment[\t ]*=)'
            r'(.*?$)'
        )
        PP_SHORT_DESC = DICT_METADATA['PP_SHORT_DESC']
        str_rep = rf'\g<1>\g<2>\g<3>{PP_SHORT_DESC}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace categories
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Categories[\t ]*=)'
            r'(.*?$)'
        )

        # convert dict to string
        PP_GUI_CATEGORIES = DICT_METADATA['PP_GUI_CATEGORIES']
        str_split = _split_quote(PP_GUI_CATEGORIES, join=';', tail=';')

        # replace text
        str_rep = rf'\g<1>\g<2>\g<3>{str_split}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace exec
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Exec[\t ]*=)'
            r'(.*?$)'
        )
        # TODO: look in $PATH
        PP_GUI_EXEC = DICT_METADATA['PP_GUI_EXEC']
        str_rep = rf'\g<1>\g<2>\g<3>{PP_GUI_EXEC}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace icon
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Icon[\t ]*=)'
            r'(.*?$)'
        )
        # TODO: look in $PATH
        PP_GUI_ICON = DICT_METADATA['PP_GUI_ICON']
        str_rep = rf'\g<1>\g<2>\g<3>{PP_GUI_ICON}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_desk, 'w', encoding='utf-8') as f:
        f.write(text)

# TODO: set desktop path entry to prog dir???


# ------------------------------------------------------------------------------
# Replace text in the UI file
# ------------------------------------------------------------------------------
def fix_ui():
    """
        Replace text in the UI file

        Replace short description, program name, and version number in the
        UI file.
    """

    # first get gui dir
    dir_gui = os.path.join(DIR_PRJ, 'src', 'gui')
    if not os.path.exists(dir_gui) or not os.path.isdir(dir_gui):
        return

    # check if there is a .ui file
    path_ui = os.path.join(dir_gui, '__PP_NAME_SMALL_-gtk3.ui')
    if not os.path.exists(path_ui):
        return

    # open file and get contents
    with open(path_ui, 'r', encoding='utf-8') as f:
        text = f.read()

        # replace version
        str_pattern = (
            r'(<object class=\"GtkAboutDialog\".*?)'
            r'(<property name=\"version\">)'
            r'(.*?)'
            r'(</property>.*)'
        )
        PP_VERSION = DICT_METADATA['PP_VERSION']
        str_rep = rf'\g<1>\g<2>{PP_VERSION}\g<4>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace short description
        str_pattern = (
            r'(<object class=\"GtkAboutDialog\".*?)'
            r'(<property name=\"comments\".*?\>)'
            r'(.*?)'
            r'(</property>)'
        )
        PP_SHORT_DESC = DICT_METADATA['PP_SHORT_DESC']
        str_rep = rf'\g<1>\g<2>{PP_SHORT_DESC}\g<4>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_ui, 'w', encoding='utf-8') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Recurse through the folder structure looking for errors
# ------------------------------------------------------------------------------
def recurse(dir):
    """
        Recurse through the folder structure looking for errors

        Parameters:
            dir [string]: the directory to start looking for errors

        This function recurses through the project directory, looking for errors
        in each file's headers and content for strings that do not match their
        intended contents. It checks a header's project, filename, and date
        values as well as looking for dunder values that should have been
        replaced.
    """

    # blacklist
    # don't check everything/contents/headers/text/path names for these items
    # strip trailing slashes to match path component
    skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_all']]
    skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_file']]
    skip_header = [item.strip(os.sep)
                   for item in DICT_BLACKLIST['skip_header']]
    skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_text']]
    skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST['skip_path']]

    # get list of replaceable file names
    items = [item for item in os.listdir(dir) if item not in skip_all]
    for item in items:

        # put path back together
        path_item = os.path.join(dir, item)

        # if it's a dir
        if os.path.isdir(path_item):

            # recurse itself to find more files
            recurse(path_item)

        else:

            # only open files we should be mucking in
            if item not in skip_file:

                # open file and get lines
                with open(path_item, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                    # check headers of most files
                    if item not in skip_header:
                        _check_header(path_item, lines)

                    # check contents of most files
                    if item not in skip_text:
                        _check_text(path_item, lines)

        # check file paths (subdirs and such)
        if item not in skip_path:
            _check_path(path_item)


# ------------------------------------------------------------------------------
# Do extra functions to update project dir after recurse
# ------------------------------------------------------------------------------

def do_extras():
    """
        Do extras functions to update project dir after recurse

        Do some extra functions like add requirements, update docs, and update
        the CHANGELOG file for the current project.
    """

    # get pyplate/src dir
    dir_curr = os.getcwd()

    # make sure we are in project path
    os.chdir(DIR_PRJ)

    # add requirements
    path_req = os.path.join(DIR_PRJ, 'requirements.txt')
    with open(path_req, 'w', encoding='utf-8') as f:

        cmd = 'python -m pip freeze -l --exclude-editable --require-virtualenv'
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=f)

    # update CHANGELOG
    path_chg = os.path.join(DIR_PRJ, 'CHANGELOG.md')
    with open(path_chg, 'w', encoding='utf-8') as f:

        cmd = 'git log --pretty="%ad - %s"'
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=f)

    # go back to old dir
    os.chdir(dir_curr)

# ------------------------------------------------------------------------------

    type_prj = DICT_SETTINGS['project']['type']

    # update docs
    cmd = 'python -m pdoc --html -f -o docs'
    cmd_array = shlex.split(cmd)

    # docs for module/cli
    if type_prj in 'mc':
        glob_py = glob(f'src{os.sep}*.py')
        cmd_array += glob_py

    # docs for package
    elif type_prj == 'p':
        prj_small = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
        cmd_array += [f'src{os.sep}{prj_small}']

    subprocess.run(cmd_array)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Checks header values for dunders
# ------------------------------------------------------------------------------
def _check_header(path_item, lines):
    """
        Checks header values for dunders

        Parameters:
            path_item [string]: the full path to file to be checked for header
            lines [array]: the contents of the file to be checked

        This function checks the files headers for values that either do not
        match the file's project/file name, or do not have a date set.
    """

    # global error count
    global g_err_cnt

    # for each line in file
    for i in range(0, len(lines)):
        line = lines[i]

        # check project name
        prj_name = os.path.basename(DIR_PRJ)
        str_pattern = (
            r'(^\s*(<!--|#)\s*)'
            r'(Project)'
            r'(\s*:\s*)'
            r'(.*?)'
            r'(\s)'
        )
        str_res = re.search(str_pattern, line, flags=re.M | re.S)
        if str_res and str_res.group(5) != prj_name:
            print(
                f'{path_item}:{i + 1}: Header Project name should be '
                f'\'{prj_name}\''
            )

            # inc error count
            g_err_cnt += 1

        # check file name
        file_name = os.path.basename(path_item)
        str_pattern = (
            r'(^\s*(<!--|#)\s*)'
            r'(Filename)'
            r'(\s*:\s*)'
            r'(.*?)'
            r'(\s)'
        )
        str_res = re.search(str_pattern, line, flags=re.M | re.S)
        if str_res and str_res.group(5) != file_name:
            print(
                f'{path_item}:{i + 1}: Header Filename should be '
                f'\'{file_name}\''
            )

            # inc error count
            g_err_cnt += 1

        # check date
        str_pattern = (
            r'(^\s*(<!--|#)\s*)'
            r'(Date)'
            r'(\s*:\s*)'
            r'(.*?)'
            r'(\s)'
        )
        str_res = re.search(str_pattern, line, flags=re.M | re.S)
        if str_res:

            # there is *something* in the date field
            if str_res.group(5) != '':

                # check for valid date
                str_pattern2 = r'\d*/\d*/\d*'
                str_res2 = re.search(str_pattern2, str_res.group(5))
                if not str_res2:
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

        Parameters:
            path_item [string]: the full path to file to be checked for text
            lines [array]: the contents of the file to be checked

        This function checks that none of the files contains an unreplaced
        replacement variable from the initial project info.
    """

    # global error count
    global g_err_cnt

    # for each line in file
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

        Parameters:
            path_item [string]: the full path to file to be checked for path

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

        Parameters:
            str_in [string]: the string to split
            split [string]: the character to split on
            quote [string]: the character to use to quote each entry (or empty)
            lead [string]: the string to precede the formatted string (or empty)
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
    lst_split = [item.strip() for item in str_in.split(split)]

    # blank strings, when split w/param, still contain 1 entry
    # https://stackoverflow.com/questions/16645083/when-splitting-an-empty-string-in-python-why-does-split-return-an-empty-list
    # so we do the list comprehension BEFORE testing the list length
    # quote items and put into new list
    lst_split = [f'{quote}{item}{quote}' for item in lst_split if item != '']

    # if the list is empty, return empty result
    if len(lst_split) == 0:
        return ''

    # join list using join string
    str_split = f'{join}'.join(lst_split)

    # surround list with lead and tail
    str_split = f'{lead}{str_split}{tail}'

    # return the final string
    return str_split


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
