#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: metadata.py                                           |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENCE__                                         \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import datetime
import json
import os
import re
import shlex
import subprocess

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_FILE = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

# this is the project dir
dir_prj = os.path.join(DIR_FILE, '..')
DIR_PRJ = os.path.abspath(dir_prj)

# load blacklist file
DICT_BLACKLIST = {}
path_blacklist = os.path.join(DIR_PRJ, 'conf', 'blacklist.json')
if os.path.exists(path_blacklist):
    with open(path_blacklist, 'r') as f:
        try:
            DICT_BLACKLIST = json.load(f)
        except (Exception):
            print(f'{f} is not a valid JSON file')
            exit()

# load settings file
DICT_SETTINGS = {}
path_settings = os.path.join(DIR_PRJ, 'conf', 'settings.json')
if os.path.exists(path_settings):
    with open(path_settings, 'r') as f:
        try:
            DICT_SETTINGS = json.load(f)
        except (Exception):
            print(f'{f} is not a valid JSON file')
            exit()

# load strings file
DICT_STRINGS = {}
path_strings = os.path.join(DIR_PRJ, 'conf', 'strings.json')
if os.path.exists(path_strings):
    with open(path_strings, 'r') as f:
        try:
            DICT_STRINGS = json.load(f)
        except (Exception):
            print(f'{f} is not a valid JSON file')
            exit()

# get list of approved categories
# https://specifications.freedesktop.org/menu-spec/latest/apa.html
LIST_CATEGORIES = [
    'AudioVideo',
    'Audio',
    'Video',
    'Development',
    'Education',
    'Game',
    'Graphics',
    'Network',
    'Office',
    'Science',
    'Settings',
    'System',
    'Utility',
    'Building',
    'Debugger',
    'IDE',
    'GUIDesigner',
    'Profiling',
    'RevisionControl',
    'Translation',
    'Calendar',
    'ContactManagement',
    'Database',
    'Dictionary',
    'Chart',
    'Email',
    'Finance',
    'FlowChart',
    'PDA',
    'ProjectManagement',
    'Presentation',
    'Spreadsheet',
    'WordProcessor',
    '2DGraphics',
    'VectorGraphics',
    'RasterGraphics',
    '3DGraphics',
    'Scanning',
    'OCR',
    'Photography',
    'Publishing',
    'Viewer',
    'TextTools',
    'DesktopSettings',
    'HardwareSettings',
    'Printing',
    'PackageManager',
    'Dialup',
    'InstantMessaging',
    'Chat',
    'IRCClient',
    'Feed',
    'FileTransfer',
    'HamRadio',
    'News',
    'P2P',
    'RemoteAccess',
    'Telephony',
    'TelephonyTools',
    'VideoConference',
    'WebBrowser',
    'WebDevelopment',
    'Midi',
    'Mixer',
    'Sequencer',
    'Tuner',
    'TV',
    'AudioVideoEditing',
    'Player',
    'Recorder',
    'DiscBurning',
    'ActionGame',
    'AdventureGame',
    'ArcadeGame',
    'BoardGame',
    'BlocksGame',
    'CardGame',
    'KidsGame',
    'LogicGame',
    'RolePlaying',
    'Shooter',
    'Simulation',
    'SportsGame',
    'StrategyGame',
    'Art',
    'Construction',
    'Music',
    'Languages',
    'ArtificialIntelligence',
    'Astronomy',
    'Biology',
    'Chemistry',
    'ComputerScience',
    'DataVisualization',
    'Economy',
    'Electricity',
    'Geography',
    'Geology',
    'Geoscience',
    'History',
    'Humanities',
    'ImageProcessing',
    'Literature',
    'Maps',
    'Math',
    'NumericalAnalysis',
    'MedicalSoftware',
    'Physics',
    'Robotics',
    'Spirituality',
    'Sports',
    'ParallelComputing',
    'Amusement',
    'Archiving',
    'Compression',
    'Electronics',
    'Emulator',
    'Engineering',
    'FileTools',
    'FileManager',
    'TerminalEmulator',
    'Filesystem',
    'Monitor',
    'Security',
    'Accessibility',
    'Calculator',
    'Clock',
    'TextEditor',
    'Documentation',
    'Adult',
    'Core',
    'KDE',
    'GNOME',
    'XFCE',
    'DDE',
    'GTK',
    'Qt',
    'Motif',
    'Java',
    'ConsoleOnly',
    'Screensaver',
    'TrayIcon',
    'Applet',
    'Shell',
]

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
    fix_blacklist()
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
    fix_gtk3()

    # # check for __PP_ /PP_ stuff left over or we missed
    recurse_and_check(DIR_PRJ)

    # do housekeeping
    do_extras()

    # do gettext stuff
    do_gettext()

    # # print error count (__PP_/PP_ stuff found)
    print(f'Errors: {g_err_cnt}')


# ------------------------------------------------------------------------------
# Replace text in the blacklist.json file
# ------------------------------------------------------------------------------
def fix_blacklist():
    """
        Replace text in the blacklist.json file

        Replace any __PP_ stuff in blacklist file.
        This is here as a convenience, since you have all the dunders in
        settings.json by the time the blacklist.json file is created.
    """

    # check if the file exists
    path_blacklist = os.path.join(DIR_PRJ, 'conf', 'blacklist.json')
    if not os.path.exists(path_blacklist):
        return

    # open file and get contents
    with open(path_blacklist, 'r') as f:
        text = f.read()

        # replace text
        settings = DICT_SETTINGS['info']
        for key, val in settings.items():
            text = text.replace(key, val)

    # save file
    with open(path_blacklist, 'w') as f:
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
    path_readme = os.path.join(DIR_PRJ, 'README.md')
    if not os.path.exists(path_readme):
        return

    # open file and get contents
    with open(path_readme, 'r') as f:
        text = f.read()

        # replace short description
        str_pattern = (
            r'(<!--[\t ]*__RM_SHORT_DESC_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__RM_SHORT_DESC_END__[\t ]*-->)'
        )

        # replace text
        pp_short_desc = DICT_STRINGS['PP_SHORT_DESC']
        str_rep = rf'\g<1>\n{pp_short_desc}\n\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace dependencies array
        str_pattern = (
            r'(<!--[\t ]*__RM_PY_DEPS_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__RM_PY_DEPS_END__[\t ]*-->)'
        )

        # build a string from the dict (markdown links)
        # only format links if value is not empty
        pp_py_deps = DICT_STRINGS['PP_PY_DEPS']
        kv_py_deps = []
        for key, val in pp_py_deps.items():
            if val == '':
                kv_py_deps.append(key)
            else:
                kv_py_deps.append(f'[{key}]({val})')

        # build a string (or none) for the deps
        if len(kv_py_deps) == 0:
            str_py_deps = 'None'
        else:
            str_py_deps = '<br>\n'.join(kv_py_deps)

        # replace text
        str_rep = rf'\g<1>\n{str_py_deps}\n\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        pp_version = DICT_STRINGS['PP_VERSION']

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
    with open(path_readme, 'w') as f:
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
    with open(path_toml, 'r') as f:
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
        pp_name_small = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
        str_rep = rf'\g<1>\g<2>\g<3>"{pp_name_small}"'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*version[\t ]*=[\t ]*)'
            r'(.*?$)'
        )
        pp_version = DICT_STRINGS['PP_VERSION']
        if pp_version == '':
            pp_version = '0.0.0'
        str_rep = rf'\g<1>\g<2>\g<3>"{pp_version}"'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace short description
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*description[\t ]*=[\t ]*)'
            r'(.*?$)'
        )
        pp_short_desc = DICT_STRINGS['PP_SHORT_DESC']
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
        pp_keywords = DICT_STRINGS['PP_KEYWORDS']
        str_pp_keywords = [f'"{item}"' for item in pp_keywords]
        str_pp_keywords = ', '.join(str_pp_keywords)

        # replace string
        str_rep = rf'\g<1>\g<2>\g<3>[{str_pp_keywords}]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace dependencies array
        str_pattern = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*dependencies[\t ]*=[\t ]*)'
            r'(.*?\])'
        )

        # convert dict to string (only using keys)
        pp_py_deps = DICT_STRINGS['PP_PY_DEPS']

        # NB: this is not conducive to a dict (we don't need links, only names)
        # so don't do what we did in README, keep it simple
        list_py_deps = [item for item in pp_py_deps.keys()]
        str_pp_py_deps = [f'"{item}"' for item in list_py_deps]
        str_pp_py_deps = ', '.join(str_pp_py_deps)

        # replace text
        str_rep = rf'\g<1>\g<2>\g<3>[{str_pp_py_deps}]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_toml, 'w') as f:
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
    pp_name_small = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
    dir_pkg = os.path.join(DIR_PRJ, 'src', pp_name_small)
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
    with open(path_init, 'r') as f:
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
    with open(path_init, 'w') as f:
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
        with open(path_item, 'r') as f:
            text = f.read()

            # replace short description
            str_pattern = (
                r'(import argparse.*def _parse_args\(\):.*)'
                r'(argparse.ArgumentParser\(\s*description=\')'
                r'(.*?)'
                r'(\'.*)'
            )
            pp_short_desc = DICT_STRINGS['PP_SHORT_DESC']
            str_rep = rf'\g<1>\g<2>{pp_short_desc}\g<4>'
            text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

            # replace version
            str_pattern = (
                r'(import argparse.*def _parse_args\(\):.*)'
                r'(print\(\'.* version )'
                r'(.*?)'
                r'(\'.*)'
            )
            pp_version = DICT_STRINGS['PP_VERSION']
            str_rep = rf'\g<1>\g<2>{pp_version}\g<4>'
            text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # save file
        with open(path_item, 'w') as f:
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
    with open(path_install, 'r') as f:
        text = f.read()

        # replace python dependencies array
        str_pattern = (
            r'(^\s*dict_install[\t ]*=\s*{)'
            r'(.*?)'
            r'(^\s*\'py_deps\'[\t ]*:)'
            r'(.*?\])'
        )

        # convert dict keys to string
        pp_py_deps = DICT_STRINGS['PP_PY_DEPS']
        str_pp_py_deps = ','.join(pp_py_deps.keys())

        # replace text
        str_rep = rf'\g<1>\g<2>\g<3> [\n\t\t{str_pp_py_deps}\n\t]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace system dependencies array
        str_pattern = (
            r'(^\s*dict_install[\t ]*=)'
            r'(.*?)'
            r'(^\s*\'sys_deps\'[\t ]*:)'
            r'(.*?\])'
        )

        # convert dict to string
        pp_sys_deps = DICT_STRINGS['PP_SYS_DEPS']
        str_pp_sys_deps = ','.join(pp_sys_deps)

        # replace string
        str_rep = rf'\g<1>\g<2>\g<3> [\n\t\t{str_pp_sys_deps}\n\t]'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_install, 'w') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the desktop file
# ------------------------------------------------------------------------------
def fix_desktop():
    """
        Replace text in the desktop file

        Replaces the desc, exec, icon, path, and category text in a .desktop
        file for programs that use this.
    """

    # global error count
    global g_err_cnt

    # check if the file exists
    pp_name_small = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
    path_desk = os.path.join(DIR_PRJ, 'src', f'{pp_name_small}.desktop')
    if not os.path.exists(path_desk):
        return

    # validate wanted categories into approved categories
    pp_gui_categories = []
    wanted_cats = DICT_STRINGS['PP_GUI_CATEGORIES']
    for cat in wanted_cats:

        # category is valid
        if cat in LIST_CATEGORIES:

            # add to final list
            pp_gui_categories.append(cat)
        else:

            # category is not valid, print erro and increase erro count
            print(
                f'In PP_GUI_CATEGORIES, "{cat}" is not valid, see \n'
                'https://specifications.freedesktop.org/menu-spec/latest/apa.html'
            )
            g_err_cnt += 1

    # open file and get contents
    with open(path_desk, 'r') as f:
        text = f.read()

        # replace categories
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Categories[\t ]*=)'
            r'(.*?$)'
        )

        # convert dict to string
        str_cat = ';'.join(pp_gui_categories)
        str_cat += ';'

        # replace text
        str_rep = rf'\g<1>\g<2>\g<3>{str_cat}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace short description
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Comment[\t ]*=)'
            r'(.*?$)'
        )
        pp_short_desc = DICT_STRINGS['PP_SHORT_DESC']
        str_rep = rf'\g<1>\g<2>\g<3>{pp_short_desc}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # get path to install dir
        path_home = os.path.expanduser('~')
        author = DICT_SETTINGS['info']['__PP_AUTHOR__']
        pp_name_big = DICT_SETTINGS['info']['__PP_NAME_BIG__']
        path_inst = os.path.join(path_home, f'.{author}', pp_name_big,
                                 'src')

        # replace exec
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Exec[\t ]*=)'
            r'(.*?$)'
        )
        path_exec = os.path.join(path_inst, f'{pp_name_small}.py')
        str_rep = rf'\g<1>\g<2>\g<3>{path_exec}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace icon
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Icon[\t ]*=)'
            r'(.*?$)'
        )
        path_icon = os.path.join(path_inst, f'{pp_name_small}.png')
        str_rep = rf'\g<1>\g<2>\g<3>{path_icon}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace path
        str_pattern = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Path[\t ]*=)'
            r'(.*?$)'
        )
        str_rep = rf'\g<1>\g<2>\g<3>{path_inst}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_desk, 'w') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Replace text in the UI file
# ------------------------------------------------------------------------------
def fix_gtk3():
    """
        Replace text in the UI file

        Replace description and version number in the UI file.
    """

    # check if there is a .ui file
    pp_name_small = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
    path_ui = os.path.join(DIR_PRJ, 'src', f'{pp_name_small}_gtk3.ui')
    if not os.path.exists(path_ui):
        return

    # open file and get contents
    with open(path_ui, 'r') as f:
        text = f.read()

        # replace short description
        str_pattern = (
            r'(<object class=\"GtkAboutDialog\".*?)'
            r'(<property name=\"comments\".*?\>)'
            r'(.*?)'
            r'(</property>)'
        )
        pp_short_desc = DICT_STRINGS['PP_SHORT_DESC']
        str_rep = rf'\g<1>\g<2>{pp_short_desc}\g<4>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        str_pattern = (
            r'(<object class=\"GtkAboutDialog\".*?)'
            r'(<property name=\"version\">)'
            r'(.*?)'
            r'(</property>.*)'
        )
        pp_version = DICT_STRINGS['PP_VERSION']
        str_rep = rf'\g<1>\g<2>{pp_version}\g<4>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_ui, 'w') as f:
        f.write(text)


# ------------------------------------------------------------------------------
# Recurse through the folder structure looking for errors
# ------------------------------------------------------------------------------
def recurse_and_check(dir):
    """
        Recurses through the folder structure looking for errors

        Parameters:
            dir: The directory to start looking for errors

        This function recurses through the project directory, checking for
        errors in each file's headers, and content for strings that do not match
        their intended contents. It checks a header's project, filename, and
        date values as well as looking for dunder values that should have been
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
            recurse_and_check(path_item)

        else:

            # only open files we should be mucking in
            if item not in skip_file:

                # open file and get lines
                with open(path_item, 'r') as f:
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

    # get current dir
    dir_curr = os.getcwd()

    # make sure we are in project path
    os.chdir(DIR_PRJ)

    # add requirements
    path_req = os.path.join(DIR_PRJ, 'requirements.txt')
    with open(path_req, 'w') as f:

        cmd = 'python -m pip freeze -l --exclude-editable --require-virtualenv'
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=f)

    # update CHANGELOG
    path_chg = os.path.join(DIR_PRJ, 'CHANGELOG.md')
    with open(path_chg, 'w') as f:

        cmd = 'git log --pretty="%ad - %s"'
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=f)

    # update docs
    # NB: this is ugly and stupid, but it's the only way to get pdoc3 to work

    # move into src dir
    dir_src = os.path.join(DIR_PRJ, 'src')
    os.chdir(dir_src)

    # get docs dir
    path_docs = os.path.join('..', 'docs')
    path_docs = os.path.abspath(path_docs)

    # # update docs
    cmd = f'python -m pdoc --html -f -o {path_docs} .'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # go back to old dir
    os.chdir(dir_curr)


# ------------------------------------------------------------------------------
# Run xgettext over files to produce a locale template
# ------------------------------------------------------------------------------
def do_gettext():
    """
        Run xgettext over files to produce a locale template

        Use xgettext to scan .py and .ui files for I18N strings and collect them
        int a .pot file in the locale folder. Only applies to gui projects at
        the moment.
    """

    # check if we are a gui project
    is_gui = (DICT_SETTINGS['project']['type'] == 'g')
    if not is_gui:
        return

    # get locale folder and pot filename
    dir_locale = os.path.join(DIR_PRJ, 'src', 'locale')
    pp_name_small = DICT_SETTINGS['info']['__PP_NAME_SMALL__']
    path_pot = os.path.join(dir_locale, f'{pp_name_small}.pot')
    pp_version = DICT_STRINGS['PP_VERSION']

    # remove old pot and recreate empty file
    if os.path.exists(path_pot):
        os.remove(path_pot)
    with open(path_pot, 'w') as f:
        f.write('')

    # build a list of files
    res = []
    exts = ['.py', '.ui', '.glade']

    # scan for files in src directory
    dir_src = os.path.join(DIR_PRJ, 'src')
    list_files = os.listdir(dir_src)

    # for each file in dir
    for file in list_files:

        # check for ext
        for ext in exts:
            if file.endswith(ext):

                # rebuild complete path and add to list
                path = os.path.join(dir_src, file)
                res.append(path)

    # for each file that can be I18N'd, run xgettext
    author = DICT_SETTINGS['info']['__PP_AUTHOR__']
    email = DICT_SETTINGS['info']['__PP_EMAIL__']
    for file in res:
        cmd = (
            'xgettext '         # the xgettest cmd
            f'{file} '          # the file name
            '-j '               # append to current file
            '-c"I18N:" '        # look for tags in .py files
            '--no-location '    # don't print filename/line number
            f'-o {path_pot} '   # location of output file
            '-F '               # sort output by input file
            f'--copyright-holder={author} '
            f'--package-name={pp_name_small} '
            f'--package-version={pp_version} '
            f'--msgid-bugs-address={email}'
        )
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array)

    # now lets do some text replacements to make it look nice

    # open file and get contents
    with open(path_pot, 'r') as f:
        text = f.read()

        # replace short description
        str_pattern = (
            r'(# SOME DESCRIPTIVE TITLE.)'
        )
        pp_name_big = DICT_SETTINGS['info']['__PP_NAME_BIG__']
        str_rep = f'# {pp_name_big} translation template'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace copyright
        author = DICT_SETTINGS['info']['__PP_AUTHOR__']
        str_pattern = (
            r'(# Copyright \(C\) )'
            r'(.*?)'
            rf'( {author})'
        )
        year = datetime.date.today().year
        str_rep = rf'\g<1>{year}\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace author's email
        str_pattern = (
            r'(# FIRST AUTHOR )'
            r'(<EMAIL@ADDRESS>)'
            r'(, )'
            r'(YEAR)'
        )
        email = DICT_SETTINGS['info']['__PP_EMAIL__']
        year = datetime.date.today().year
        str_rep = rf'\g<1>{email}\g<3>{year}'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace charset
        str_pattern = (
            r'("Content-Type: text/plain; charset=)'
            r'(CHARSET)'
            r'(\\n")'
        )
        charset = 'UTF-8'
        str_rep = rf'\g<1>{charset}\g<3>'
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_pot, 'w',) as f:
        f.write(text)


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
            path_item: The full path to file to be checked for header
            lines: The contents of the file to be checked

        This function checks the files headers for values that either do not
        match the file's project/file name, or do not have a date set.
        This method is private because it is only called from inside
        recurse_and_check().
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
            path_item: The full path to file to be checked for text
            lines: The contents of the file to be checked

        This function checks that none of the files contains an unreplaced
        replacement variable from the initial project info.
        This method is private because it is only called from inside
        recurse_and_check().
    """

    # global error count
    global g_err_cnt

    # for each line in file
    for i in range(0, len(lines)):
        line = lines[i]

        # the dunders to look for
        reps = [rep for rep in DICT_SETTINGS['info'] and DICT_STRINGS]

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
            path_item: The full path to file to be checked for path

        This function checks that none of the files paths contains an unreplaced
        dunder variable from the initial project info.
        This method is private because it is only called from inside
        recurse_and_check().
    """

    # global error count
    global g_err_cnt

    # check for dunders in path
    if '__PP_' in path_item:
        print(f'{path_item}: Path contains __PP_')

        # inc error count
        g_err_cnt += 1


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
