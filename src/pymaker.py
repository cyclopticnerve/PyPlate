#! /usr/bin/env python
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
from datetime import datetime
import json
import os
import re
import shlex
import shutil
import subprocess

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_FILE = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

# this is the dir above where the script is being run from
# (e.g. ~/Documents/Projects/Python/PyPlate/)
dir_pyplate = os.path.join(DIR_FILE, '..')
DIR_PYPLATE = os.path.abspath(dir_pyplate)

# this is the dir where the template files are located relative to this script
# (e.g. ~/Documents/Projects/Python/PyPlate/template/)
DIR_TEMPLATE = os.path.join(DIR_PYPLATE, 'template')

# this is the location where the project's subdir will be (above PyPlate)
# (e.g. ~/Documents/Projects/Python/)
dir_base = os.path.join(DIR_PYPLATE, '..')
DIR_BASE = os.path.abspath(dir_base)

# the dict of user info to be replaced in the headers and text of a new project
# they are placed here to be easily modified by subsequent users
# they are then copied to g_dict_settings to be used here and copied to the
# project folder for use by pybaker.py
DICT_USER = {

    # the author name, used in headers and pyproject.toml
    '__PP_AUTHOR__':        'cyclopticnerve',

    # the author's email, used in headers and pyproject.toml
    '__PP_EMAIL__':         'cyclopticnerve@gmail.com',

    # the license name, used in headers, README.md, and pyproject.toml
    '__PP_LICENSE__':       'WTFPLv2',

    # NB: the struggle here is that using the fixed format results in a
    # four-digit year, but using the locale format ('%x') results in a two-digit
    # year (at least for my locale, which in 'en_US'). so what to do? what i
    # really want is a locale format that uses four-digit years everywhere. so i
    # am faced with a 'cake and eat it too' situation. not sure how to proceed
    # but i think for now i will leave this as a user-editable string and place
    # it in the realm of 'edit it before you run' along with
    # author/email/license...
    '__PP_DATE_FMT__':      '%m/%d/%Y'
}

# the types of projects this script can create
# key is the short type name
# val[0] is the long type name
# val[1] is the subdir name under DIR_BASE where the project will be created
# val[2] is the dir under 'template' to get the files from
DICT_TYPES = {
    'c': ['CLI',        'CLIs',     'cli'],
    'g': ['GUI',        'GUIs',     'gui'],
    'm': ['Module',     'Modules',  'mod'],
    'p': ['Package',    'Packages', 'pkg']
}

# the list of keys to replace in the header of each file
# these values are used to find matching lines in the file that are assumed to
# be header lines, if they match the pattern used in _fix_header()
# the file header line should contain lines that match the pattern:
# '# <Key>: <val> ...'
# or
# '<!-- <key>: <val> ...'
# where <key> is one of the items here, and <val> is one of the keys from
# g_dict_settings. if <key> does not match one of these items or <val> does
# not match one of the keys from g_dict_settings, it is left untouched.
# see template/common/README.md for an example
LIST_HEADER = [
    'Project',      # PyPlate
    'Filename',     # pyplate.py
    'Date',         # 12/08/2022
    'Author',       # cyclopticnerve
    'License'       # WTFPLv2
]

# the dict of sections to remove in the README file
# key is the project type we are making (may contain multiple project types)
# RM_DELETE_START is the tag at the start of the section to remove
# RM_DELETE_END is the tag at the end of the section to remove
# NB: these keys start with 'RM' instead of 'PP' because most keys will remain
# in the file, and we don't want pybaker to report their presence as an error
DICT_README = {
    'mp': {
        'RM_DELETE_START':  '<!-- __RM_APP_START__ -->',
        'RM_DELETE_END':    '<!-- __RM_APP_END__ -->'
    },
    'cg': {
        'RM_DELETE_START':  '<!-- __RM_MOD_START__ -->',
        'RM_DELETE_END':    '<!-- __RM_MOD_END__ -->'
    }
}

# this is the set of files/folders we don't mess with in the final project
# each item can be a filename or a folder
# NB: you can use dunders here since the path is the last thing to get fixed
# these file/folder names should match what's in the template folder (before any
# modifications, hence using dunder keys)
DICT_BLACKLIST = {

    # skip header, skip text, skip path
    'PP_SKIP_ALL': [
        '.git',
        '.venv',
        '.vscode',
        'docs',
        'misc',
        'README',
        'tests',
        'locale',
        'CHANGELOG.md',
        'LICENSE.txt',
        'requirements.txt'
    ],

    # skip header, skip text, fix path
    'PP_SKIP_FILE': [
        '__PP_NAME_SMALL__.png'
    ],

    # skip header, fix text, fix path
    'PP_SKIP_HEADER': [],

    # fix header, skip text, fix path
    'PP_SKIP_TEXT': [
        'conf',
        'MANIFEST.in',
        '.gitignore'
    ],

    # fix header, fix text, skip path
    'PP_SKIP_PATH': []
}

# the metadata that the final project will use for pybaker.py
DICT_METADATA = {

    # the version number to use in README.md and pyproject.toml
    '__PP_VERSION__':           '',

    # the short description to use in README.md and pyproject.toml
    '__PP_SHORT_DESC__':        '',

    # the keywords to use in pyproject.toml and github
    '__PP_KEYWORDS__':          [],

    # the dependencies to use in README.md, pyproject.toml, github, and
    # install.py`
    '__PP_PY_DEPS__':           {},

    # the dependencies to use in README.md, github.com, and install.py
    '__PP_SYS_DEPS__':          [],

    # the categories to use in .desktop
    '__PP_GUI_CATEGORIES__':    []
}

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# the default settings to use to create the project
# these can be used later by pybaker.py (from misc/settings.json)
# NB: these are one-time settings created by pymaker and should not be edited
# dunders will be used for string replacement here, and checking in pybaker
# also, some entries are moved from DICT_USER for convenience
g_dict_settings = {
    '__PP_NAME_BIG__':   '',    # PyPlate
    '__PP_NAME_SMALL__': '',    # pyplate
    '__PP_DATE__':       '',    # 12/08/2022
    '__PP_AUTHOR__':     DICT_USER['__PP_AUTHOR__'],
    '__PP_EMAIL__':      DICT_USER['__PP_EMAIL__'],
    '__PP_LICENSE__':    DICT_USER['__PP_LICENSE__'],
    '__PP_DATE_FMT__':   DICT_USER['__PP_DATE_FMT__']
}

# this dict is only used internally by pymaker.py
# NB: the project type is the lower-cased single char from get_project_info()
# the project dir is only used to figure where the project will get created
g_dict_project = {
    'PP_TYPE_PRJ': '',     # 'c'
    'PP_DIR_PRJ':  ''      # '~/Documents/Projects/Python/CLIs/PyPlate'
}

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

    # get info and copy template
    get_project_info()
    copy_template()

    # call walk to do replacements in final project location, starting at the
    # top level folder of the project
    dir_prj = g_dict_project['PP_DIR_PRJ']
    walk_and_fix(dir_prj)

    # do extra stuff to final dir after recurse
    do_extras()

# ------------------------------------------------------------------------------
# Get project info
# ------------------------------------------------------------------------------
def get_project_info():
    """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        g_dict_settings and g_dict_project.
    """

    # the settings dict (global b/c we will modify here)
    global g_dict_settings

    # the project dict (global b/c we will modify here)
    global g_dict_project

    # first get question
    str_prj = 'Project type'

    # then get types
    list_types = [f'{key} ({val[0]})' for (key, val) in DICT_TYPES.items()]
    str_types = ' | '.join(list_types)
    str_in = f'{str_prj} [{str_types}]: '

    # sanity check
    type_prj_lower = ''

    # loop forever until we get a valid type (or user presses Ctrl+C)
    while True:

        # ask what type of project
        type_prj = input(str_in)

        # check project type
        # first, is there an entry?
        if len(type_prj) == 0:
            continue

        # get first (or only) char and lowercase it
        type_prj = type_prj[0]
        type_prj_lower = type_prj.lower()

        # get array of acceptable lowercase types
        list_type_lower = [item.lower() for item in DICT_TYPES.keys()]

        # we got a valid type
        if type_prj_lower in list_type_lower:
            g_dict_project['PP_TYPE_PRJ'] = type_prj_lower
            break

    # get output subdir
    dir_type = DICT_TYPES[type_prj_lower][1]

    # get question
    str_name = 'Project name: '

    # sanity check
    info_name_big = ''

    # loop forever until we get a valid name and dir (or user presses Ctrl+C)
    while True:

        # ask for project name
        info_name_big = input(str_name)

        # check for valid name
        if not _check_name(info_name_big):
            continue

        # calculate final project location
        dir_prj = os.path.join(DIR_BASE, dir_type, info_name_big)

        # check if project already exists
        if os.path.exists(dir_prj):
            print(f'Project {dir_prj} already exists')
            continue

        # at this point, both name and dir are valid (both valid to continue)
        # so store both and exit loop
        g_dict_settings['__PP_NAME_BIG__'] = info_name_big
        g_dict_project['PP_DIR_PRJ'] = dir_prj
        break

    # calculate small name
    info_name_small = info_name_big.lower()
    g_dict_settings['__PP_NAME_SMALL__'] = info_name_small

    # calculate current date (format assumed from constants above)
    # NB: this gives us a create date that we cannot get reliably from Linux
    # later this may be changed to modified date
    now = datetime.now()
    fmt_date = DICT_USER['__PP_DATE_FMT__']
    info_date = now.strftime(fmt_date)
    g_dict_settings['__PP_DATE__'] = info_date

# ------------------------------------------------------------------------------
# Copy template files to final location
# ------------------------------------------------------------------------------
def copy_template():
    """
        Copy template files to final location

        Get files/folders from template and copy them to the project folder.
    """

    # create target folder
    dir_prj = g_dict_project['PP_DIR_PRJ']
    os.makedirs(dir_prj)

    # NB: I tried this both ways:

    # 1. template/src/type/file
    # this made a cleaner tree, but an uglier code base
    # also i had to add an 'extras' folder for MANIFEST/pyproject to avoid
    # recursion/manually adding them
    # this also negated the option of combining them into a single loop

    # 2. template/type/src/file
    # this made the tree a little uglier, but made a cleaner code base
    # also the tree ends up reflecting the final project tree better, as
    # everything under the common folder ends up at the root level of the
    # project, and everything under the type dir also ends up at the root level
    # of the project
    # this was also able to add everything into a single loop

    # create list of source dirs
    # add common
    list_src = ['common']

    # add project type source
    type_prj = g_dict_project['PP_TYPE_PRJ']
    dir_src = DICT_TYPES[type_prj][2]
    list_src.append(dir_src)

    # list_src is now ['common', project type src]
    for item in list_src:

        # list each item in each folder in list_src
        dir_in = os.path.join(DIR_TEMPLATE, item)
        items = os.listdir(dir_in)

        # for each item in each folder
        for item in items:

            # build old item/new item
            item_from = os.path.join(dir_in, item)
            item_to = os.path.join(dir_prj, item)

            # if it's a dir
            if os.path.isdir(item_from):

                # copy dir
                shutil.copytree(item_from, item_to)

            # if its not a dir
            else:

                # then copy file
                shutil.copy2(item_from, item_to)

    # NB: the following commands are included in copy_template because their
    # resulting files are part of the project, they are just empty to start
    # whereas the stuff in do_extras MUST be initialized AFTER the project
    # exists
    # also we may want to modify them during _walk_and_fix()

    # write DICT_BLACKLIST to conf file
    path_to = os.path.join(dir_prj, 'conf', 'blacklist.json')
    with open(path_to, 'w') as f:
        dict_blacklist = json.dumps(DICT_BLACKLIST, indent=4)
        f.write(dict_blacklist)

    # write DICT_METADATA to conf file
    path_to = os.path.join(dir_prj, 'conf', 'metadata.json')
    with open(path_to, 'w') as f:
        dict_metadata = json.dumps(DICT_METADATA, indent=4)
        f.write(dict_metadata)

    # write g_dict_settings to conf file
    path_to = os.path.join(dir_prj, 'conf', 'settings.json')
    with open(path_to, 'w') as f:
        dict_settings = json.dumps(g_dict_settings, indent=4)
        f.write(dict_settings)

# ------------------------------------------------------------------------------
# Scan folders/files in the project for replace/rename
# ------------------------------------------------------------------------------
def walk_and_fix(path):
    """
        Scan folders/files in the project for replace/rename

        Parameters:
            dir: The directory to start recursively scanning from

        This function scans for folders/files under a given folder. It iterates
        over the contents of the 'dir' folder, starting at the project's
        location. For each file/folder it encounters, it passes the path to a
        filter to determine if the file needs fixing based on its appearance in
        the blacklist.
    """

    # get the lists of excluded files/folders
    skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_ALL']]
    skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_FILE']]
    skip_header = [item.strip(os.sep)
                   for item in DICT_BLACKLIST['PP_SKIP_HEADER']]
    skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_TEXT']]
    skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_PATH']]

    # walk from project dir
    for root, dirs, files in os.walk(path):

        # readme (fix before any path changes)
        for f in files:
            if f == 'README.md':
                path_rm = os.path.join(root, f)
                _fix_readme(path_rm)

        # remove any dirs/files in skip_all for next iteration
        dirs[:] = [d for d in dirs if d not in skip_all]
        files[:] = [f for f in files if f not in skip_all]

        # header
        exclude = skip_all + skip_file + skip_header
        _filter_header(root, files, exclude)

        # text
        exclude = skip_all + skip_file + skip_text
        _filter_text(root, files, exclude)

        # path
        exclude = skip_all + skip_path
        _filter_path(root, files, exclude)

# ------------------------------------------------------------------------------
# Add extra folders/files to new project after recurse
# ------------------------------------------------------------------------------
def do_extras():
    """
        Add extra folders/files to new project after recurse

        Adds a .git folder (repository) and a .venv (virtual environment) folder
        to the project, and sets them up as necessary. These files do NOT need
        to be modified by recurse_and_fix, so we do them last.
    """

    # get project dir
    dir_prj = g_dict_project['PP_DIR_PRJ']

    # copy the 'starter kit' of requirements
    # NB: this is the current set of requirements used to build/run PyPlate
    # also note that these are the requirements for the venv, NOT the
    # requirements for running the resulting project (that's a task for another
    # day...)
    # also note that the output directory is the project location, but we do NOT
    # change the current directory yet (to use the PyPlate dir as the starting
    # point for pip freeze)
    # also note that we use stdout=f in the subprocess because '>' isn't
    # supported in subprocess (even when using 'shell=True)
    # FIXME: no longer works
    # path_reqs = os.path.join(dir_prj, 'requirements.txt')
    # with open(path_reqs, 'w') as f:
    #     cmd = 'python -m pip freeze'
    #     cmd_array = shlex.split(cmd)
    #     subprocess.run(cmd_array, stdout=f)

    # now change working dir
    # save old working dir (PyPlate/src)
    dir_curr = os.getcwd()

    # change to project path
    os.chdir(dir_prj)

    # add git folder
    cmd = 'git init'
    cmd_array = shlex.split(cmd)
    subprocess.run(cmd_array)

    # create tree
    # NB: use 'stdout=f' to replace '>'
    path_tree = os.path.join(dir_prj, 'misc', 'tree.txt')
    with open(path_tree, 'w') as f:
        cmd = 'tree --dirsfirst --noreport'
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=f)

    # FIXME: no longer works
    # add venv dir
    # NB: use '.venv' to be compatible with VSCodium
    # cmd = 'python -m venv .venv'
    # cmd_array = shlex.split(cmd)
    # subprocess.run(cmd_array)
    # TODO: activate venv and install reqs

    # go back to old dir
    os.chdir(dir_curr)

# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Filter files that need header replacement
# ------------------------------------------------------------------------------
def _filter_header(root, files, exclude):
    """
        Filter files that need header replacement

        Parameters:
            root:the directory to check
            files: the list of files to check
            exclude: the list of files/folders to skip

    """

    # get current folder name
    root_name = os.path.basename(root)

    # if not excluded
    if root_name not in exclude:

        # get each file name
        for file_name in files:

            # if not excluded
            if file_name not in exclude:

                # rebuild full path
                path = os.path.join(root, file_name)

                # do fix header
                _fix_header(path)

# ------------------------------------------------------------------------------
# Filter files that need text replacement
# ------------------------------------------------------------------------------
def _filter_text(root, files, exclude):
    """
        Filter files that need text replacement

        Parameters:
            root:the directory to check
            files: the list of files to check
            exclude: the list of files/folders to skip
    """

    # get current folder name
    root_name = os.path.basename(root)

    # if not excluded
    if root_name not in exclude:

        # get each file name
        for file_name in files:

            # if not excluded
            if file_name not in exclude:

                # rebuild full path
                path = os.path.join(root, file_name)

                # do fix text
                _fix_text(path)

# ------------------------------------------------------------------------------
# Filter files that need path replacement
# ------------------------------------------------------------------------------
def _filter_path(root, files, exclude):
    """
        Filter files that need path replacement

        Parameters:
            root:the directory to check
            files: the list of files to check
            exclude: the list of files/folders to skip
    """

    # get current folder name
    root_name = os.path.basename(root)

    # if not excluded
    if root_name not in exclude:

        # get each file name
        for file_name in files:

            # if not excluded
            if file_name not in exclude:

                # rebuild full path
                path = os.path.join(root, file_name)

                # do fix header
                _fix_path(path)

        # for directory, do fix path
        _fix_path(root)

# ------------------------------------------------------------------------------
# Remove unnecessary parts of the README file
# ------------------------------------------------------------------------------
def _fix_readme(path):
    """
        Remove unnecessary parts of the README file

        Parameters:
            path: The path to README for removing README text

        This function removes sections of the README file that are not
        appropriate to the specified type of project, such as Module/Package or
        CLI/GUI.
    """

    # open file
    with open(path, 'r+') as f:
        lines = f.readlines()

        # NB: the strategy here is to go through the full README and only copy
        # lines that are:
        # 1) not in any block
        # or
        # 2) in the block we want
        # the most efficient way to do this is to have an array that receives
        # wanted lines, then return that array
        # we use a new array vs. in-situ replacement here b/c we are removing A
        # LOT OF LINES, which in-situ would result in A LOT OF BLANK LINES and
        # while that would look *ok* in the resulting Markdown, looks UGLY in
        # the source code. so we opt for not copying those lines.

        # just a boolean flag to say if we are kajiggering
        # if True, we are in a block we don't want to copy
        # assume False to say we want to copy
        ignore = False

        # where to put the needed lines
        new_lines = []

        # what to ignore in the text
        # first get type of project
        type_prj = g_dict_project['PP_TYPE_PRJ']
        for key in DICT_README.keys():
            if type_prj in key:

                # get values for keys
                RM_DELETE_START = DICT_README[key]['RM_DELETE_START']
                RM_DELETE_END = DICT_README[key]['RM_DELETE_END']
                break

        # for each line
        for line in lines:

            # check if we have entered an invalid block
            if RM_DELETE_START in line:
                ignore = True

            # we're (still) in a valid block
            if not ignore:

                # iadd stuff inside valid block
                new_lines.append(line)

            # check if we have left the invalid block
            if RM_DELETE_END in line:
                ignore = False
        
        # save lines to README.md
        f.writelines(new_lines)

# ------------------------------------------------------------------------------
# Replace dunders inside headers
# ------------------------------------------------------------------------------
def _fix_header(path):
    """
        Replace dunders inside headers

        Parameters:
            path: The path for replacing header text

        This is a function to replace header text inside a file. Given a list of
        file lines, it iterates the list line by line, replacing header text as
        it goes. When it is done, it returns lhe list of lines. This replaces
        the __PP_.. stuff inside headers.
        Using this method, we preserve any right-aligned text in each header
        row. See the headers in my files for an example. Adapting this function
        to your style of header should be easy using the regex, and modifying
        DICT_HEADER to suit.
    """
    with open(path, 'r+') as f:
        lines = f.readlines()

        # for each line in array
        # NB: replace in situ so need index so use range
        for i in range(0, len(lines)):

            # for each header key
            for item in LIST_HEADER:

                # look for a header key
                pattern = (
                    r'(# |<!-- )'   # 1. opening comment char(s)
                    rf'({item})'    # 2. the key from LIST_HEADER
                    r'(\s*: )'      # 3. the following colon
                    r'([^\s\.]*)'   # 4. all chars except spaces and periods
                    r'(\S*)'        # 5. all a/n chars inc. dot (for file ext)
                    r'(\s*)'        # 6. all spaces (the padding)
                    r'(.*)'         # 7. all other chars (right-aligned text)
                )

                # find first instance of header key
                res = re.search(pattern, lines[i])

                # no res, keep going
                if not res:
                    continue

                # default value is group 4 (in case it is blank)
                val = res.group(4)

                # try to find key in dict_values
                # if blank or not dunder in g_dict_settings, leave it alone
                # and keep going
                if len(val) == 0 or val not in g_dict_settings.keys():
                    continue

                # get the value by backtracking into g_dict_settings
                val = g_dict_settings[val]

                # count what we will need without spaces
                len_res = (
                    len(res.group(1)) +
                    len(res.group(2)) +
                    len(res.group(3)) +
                    len(val) +              # group 4 is val
                    len(res.group(5)) +
                    # group 6 is str_spaces
                    len(res.group(7))
                )

                # make spaces
                # NB: this looks funky but it works:
                # 1. get the length of the old line (NOT always 80 since we
                # can't have trailing spaces)
                # 2. subtract 1 for newline
                # 3. subtract the other match lengths
                len_spaces = (
                    len(lines[i]) - 1 - len_res
                )
                str_spaces = ' ' * len_spaces

                # replace text in the line
                str_rep = rf'\g<1>\g<2>\g<3>{val}\g<5>{str_spaces}\g<7>'
                lines[i] = re.sub(pattern, str_rep, lines[i])

        # save lines to README.md
        f.writelines(lines)

# ------------------------------------------------------------------------------
# Replace dunders inside files
# ------------------------------------------------------------------------------
def _fix_text(path):
    """
        Replace dunders inside files

        Parameters: the path to the file  for replacing text

        This is a function to replace text inside a file. Given a list of file
        lines, it iterates the list line by line, replacing text as it goes.
        When it is done, it returns the list of lines. This replaces the
        __PP_...  stuff inside the file, excluding headers (which are
        already handled).
    """
    with open(path, 'r+') as f:
        lines = f.readlines()

        # for each line in array
        # NB: replace in situ so need index so use range
        for i in range(0, len(lines)):

            # replace text in line
            for key, val in g_dict_settings.items():
                if key in lines[i]:

                    # replace text with new value
                    lines[i] = lines[i].replace(key, val)

        # save lines to file
        f.writelines(lines)

# ------------------------------------------------------------------------------
# Rename folders/files in the project
# ------------------------------------------------------------------------------
def _fix_path(path):
    """
        Rename folders/files in the project

        Parameters:
            path: The path to the folder/file for renaming

        This is a function to rename folders/files. Given a path to a
        folder/file, it renames the folder/file by replacing items in the
        g_dict_settings keys with their appropriate replacements.
    """

    # first take the path apart (we only want to change the last component)
    split = os.path.split(path)
    path_dir = split[0]
    file_name = split[1]

    # replace dunders in last path component
    for key in g_dict_settings.keys():
        file_name = file_name.replace(key, g_dict_settings[key])

    # put the new path back together
    path_new = os.path.join(path_dir, file_name)

    # if it hasn't changed, skip to avoid overhead
    if path_new == path:
        return

    # do rename
    os.rename(path, path_new)

# ------------------------------------------------------------------------------
# Check project name for allowed characters
# ------------------------------------------------------------------------------
def _check_name(name):
    """
        Check project name for allowed characters

        Parameters:
            name: The name to check for allowed characters

        Returns:
            Whether the name is valid to use

        This function checks the passed name for four criteria:
        1. non-blank name
        2. starts with an alpha-numeric char
        3. ends with an alpha-numeric char
        4. contains only alpha-numeric chars or hyphen(-)/underscore (_)
    """

    # NB: there is an easier way to do this with regex:
    # ^([a-zA-Z\d]|[a-zA-Z]+[a-zA-Z\d]*[a-zA-Z\d]+)$
    # AND OMG DID IT TAKE A LONG TIME TO FIND IT!
    # in case you were looking for it. It will give you a quick yes-no answer.
    # I don't use it here because I want to give the user as much feedback as
    # possible, so I break down the regex into steps where each step explains
    # which part of the name is wrong.

    # check for blank name
    if name == '':
        return False

    # match start or return false
    pattern = r'(^[a-zA-Z\d])'
    res = re.search(pattern, name)
    if not res:
        print('Project names must start with a letter')
        return False

    # match end or return false
    pattern = r'([a-zA-Z\d]$)'
    res = re.search(pattern, name)
    if not res:
        print('Project names must end with a letter or number')
        return False

    # match middle or return false
    pattern = r'(^[a-zA-Z\d\-_]*$)'
    res = re.search(pattern, name)
    if not res:
        print('Project names must contain only letters, numbers, dashes (-), \
            or underscores (_)')
        return False

    # if we made it this far, return true
    return True

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
