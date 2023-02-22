# ------------------------------------------------------------------------------
# Project : __CN_NAME_BIG__                                        /          \
# Filename: metadata.py                                           |     ()     |
# Date    : __CN_DATE__                                           |            |
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
# gui categories MUST be seperated by semicolon and MUST end with semicolon
CN_SHORT_DESC = ''
CN_KEYWORDS = ''
CN_SYS_DEPS = ''
CN_PY_DEPS = ''

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------
curr_dir = os.path.abspath(os.path.dirname(__file__))


# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------
def main():
    
    do_toml()
    do_inst()
    do_desk()
    do_readme()
    recurse(curr_dir)


def do_toml():

    # TODO: deps must have version?

    # NB: this function will ALWAYS create a multi-line array, e.g.:
    # keywords = [
    #     "foo",
    #     "bar"
    # ]
    # even if the input file's array was a single line or multiline
    # also if the input file's array was empty or not

    prj_toml = os.path.join(curr_dir, 'pyproject2.toml')
    if os.path.exists(prj_toml):

        with open(prj_toml) as file:
            text = file.read()

        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*version[\t ]*=)'
            r'(.*?$)'
        )
        rep_str = rf'\g<1>\g<2>\g<3> "{CN_VERSION}"'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*description[\t ]*=)'
            r'(.*?$)'
        )
        rep_str = rf'\g<1>\g<2>\g<3> "{CN_SHORT_DESC}"'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*keywords[\t ]*=)'
            r'(.*?\])'
        )
        split_str = split_quote(CN_KEYWORDS)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        pattern_str = (
            r'(^\s*\[project\]\s*$)'
            r'(.*?)'
            r'(^\s*dependencies[\t ]*=)'
            r'(.*?\])'
        )
        split_str = split_quote(CN_PY_DEPS)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}]'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        with open(prj_toml, 'w') as file:
            file.write(text)


def do_inst():

    prj_inst = os.path.join(curr_dir, 'install2')
    if os.path.exists(prj_inst):

        with open(prj_inst) as file:
            text = file.read()

        pattern_str = (
            r'(^\s*dict_install[\t ]*=)'
            r'(.*?)'
            r'(^\s*\'sys_deps\'[\t ]*:)'
            r'(.*?\])'
        )
        split_str = split_quote(CN_SYS_DEPS, tabs=2)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\t\g<5>'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        pattern_str = (
            r'(^\s*dict_install[\t ]*=\s*{)'
            r'(.*?)'
            r'(^\s*\'py_deps\'[\t ]*:)'
            r'(.*?\])'
        )
        split_str = split_quote(CN_PY_DEPS, tabs=2)
        rep_str = rf'\g<1>\g<2>\g<3> [\n{split_str}\t\g<5>'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        with open(prj_inst, 'w') as file:
            file.write(text)


def do_desk():

    prj_desk = os.path.join(curr_dir, 'gui/__CN_NAME_SMALL__2.desktop')
    if os.path.exists(prj_desk):

        with open(prj_desk) as file:
            text = file.read()

        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Comment[\t ]*=)'
            r'(.*?$)'
        )
        rep_str = rf'\g<1>\g<2>\g<3>{CN_SHORT_DESC}'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        pattern_str = (
            r'(^\s*\[Desktop Entry\]\s*$)'
            r'(.*?)'
            r'(^\s*Categories[\t ]*=)'
            r'(.*?$)'
        )
        # TODO: ensure categories seperated by ; and end with ; (not split)
        # set up a func to split, remove ',', join, add ';'
        rep_str = rf'\g<1>\g<2>\g<3>{CN_GUI_CATEGORIES}'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        with open(prj_desk, 'w') as file:
            file.write(text)


def do_readme():

    prj_read = os.path.join(curr_dir, 'README2.md')
    if os.path.exists(prj_read):

        with open(prj_read) as file:
            text = file.read()

        pattern_str = (
            r'(<!--[\t ]*__CN_SHORT_DESC_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__CN_SHORT_DESC_END__[\t ]*-->)'
        )
        rep_str = rf'\g<1>\n{CN_SHORT_DESC}\n\g<3>'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

        pattern_str = (
            r'(<!--[\t ]*__CN_PY_DEPS_START__[\t ]*-->)'
            r'(.*?)'
            r'(<!--[\t ]*__CN_PY_DEPS_END__[\t ]*-->)'
        )
        split_str = split_quote(CN_PY_DEPS, tabs=0, quote='', join='')
        rep_str = rf'\g<1>\n{split_str}\g<3>'
        text = re.sub(pattern_str, rep_str, text, 1, re.I | re.M | re.S)

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

        with open(prj_read, 'w') as file:
            file.write(text)


def recurse(path):

    # don't rename these dirs or files, or change file contents
    # NB: must not end in '/'!!!
    skip_dirs = [
        'misc',
        'metadata.py'
    ]

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

            check_headers(path_item, text)
            check_dunders(path_item, text)

    check_path(path_item)


def check_headers(path_item, text):

    # check project name
    proj_name = os.path.basename(curr_dir)
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
    def_date = "__CN_DATE__"
    pattern = (
        r'(^\s*(<!--|#) Date    : )'
        r'(.*?)'
        r'(\s)'
    )
    res = re.search(pattern, text, re.I | re.M)
    if res and def_date == res.group(3):
        print(f'{path_item}: Header Date is not set')


def check_dunders(path_item, text):

    # NB: this doesn't check folder names but that seems like a lot of extra
    # work so we don't really care -)

    dunders = [
        "__CN_NAME_BIG__",
        "__CN_NAME_SMALL__"
    ]
    for item in dunders:
        if item in text:
            print(f'{path_item} contains {item}')


def check_path(path_item):

    dunders = [
        "__CN_NAME_BIG__",
        "__CN_NAME_SMALL__"
    ]
    for item in dunders:
        if item in path_item:
            print(f'{path_item} has {item} in path')


def split_quote(str_in, tabs=1, split=',', quote='"', join=','):

    # str_in = str_in.strip()
    split_lst = str_in.split(split)

    # NB: blank strings, when split w/param, still contain 1 entry
    # https://stackoverflow.com/questions/16645083/when-splitting-an-empty-string-in-python-why-does-split-return-an-empty-list
    split_lst = [f'{quote}{item}{quote}' for item in split_lst if item != '']

    if len(split_lst) == 0:
        return ''

    # {item}{,}\n
    # {tabs}(item){,}\n
    # {tabs}{item}
    tab_str = '\t' * tabs
    split_lst_str = f'{join}\n{tab_str}'.join(split_lst)

    # {tabs}{item}{,}\n
    # {tabs}(item){,}\n
    # {tabs}{item}\n
    #
    split_lst_str = f'{tab_str}{split_lst_str}\n'

    return split_lst_str


if __name__ == '__main__':
    main()

# -)
