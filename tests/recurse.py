import os

# ------------------------------------------------------------------------------

DIR_PRJ = '/home/dana/Documents/Projects/Python/Modules/ModTest'

DICT_BLACKLIST = {

    # no header, no text, no path
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
        'requirements.txt',
    ],

    # no header, no text, yes path
    'PP_SKIP_FILE': [
        '__PP_NAME_SMALL__.png',
    ],

    # no header, yes text, yes path
    'PP_SKIP_HEADER': [],

    # yes header, no text, yes path
    'PP_SKIP_TEXT': [
        'conf',
        'MANIFEST.in',
        '.gitignore',
    ],

    # yes header, yes text, no path
    'PP_SKIP_PATH': [],

}

# ------------------------------------------------------------------------------

# def recurse_and_fix(dir):
#     """
#         Recursively scan folders/files in the project for replace/rename

#         Parameters:
#             dir: The directory to start recursively scanning from

#         This is a recursive function to scan for folders/files under a given
#         folder. It iterates over the contents of the 'dir' folder, starting at
#         the project's location. It checks if each item is a file or a folder. If
#         it encounters a folder, it calls itself recursively, passing that folder
#         as the parameter. If it encounters a file, it calls methods to do text
#         replacement of headers, then other text. Finally it renames the file if
#         the path contains a replacement key. Once all files are fixed, it will
#         then bubble up to fix all folders.
#     """

#     # blacklist
#     # remove all leading/trailing slashes
#     # NB: these lists are explained in detail in the README file
#     skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_ALL']]
#     skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_FILE']]
#     skip_header = [item.strip(os.sep)
#                    for item in DICT_BLACKLIST['PP_SKIP_HEADER']]
#     skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_TEXT']]
#     skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_PATH']]

#     # get list of file names in dest dir (excluding skip_all)
#     items = [item for item in os.listdir(dir) if item not in skip_all]
#     for item in items:

#         # put path back together
#         abs_item = os.path.join(dir, item)

#         # if it's a dir
#         if os.path.isdir(abs_item):

#             # TODO check if this dir is in blacklist
#             # if is is, continue
#             # recurse itself to find more files
#             print('doing folder:\t', abs_item)
#             recurse_and_fix(abs_item)

#         else:
#             if item not in skip_file:

#                 abs_file = os.path.join(dir, item)

#                 # replace headers from lines
#                 if item not in skip_header:
#                     print('fix_headers:\t', abs_file)

#                 # replace text from lines
#                 if item not in skip_text:
#                     print('fix_text:\t', abs_file)

#                 # readme needs extra handling
#                 if item == 'README.md':
#                     print('fix_readme:\t', abs_file)

#             # fix path
#             if item not in skip_path:
#                 print('fix_path:\t', abs_file)

# ------------------------------------------------------------------------------


def walk(dir):

    # get the lists of excluded files/folders
    skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_ALL']]
    skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_FILE']]
    skip_header = [item.strip(os.sep)
                   for item in DICT_BLACKLIST['PP_SKIP_HEADER']]
    skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_TEXT']]
    skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST['PP_SKIP_PATH']]

    # walk from project dir
    for root, dirs, files in os.walk(dir):

        # readme (fix before any path changes)
        for f in files:
            if f == 'README.md':
                path = os.path.join(root, file)
                _fix_readme(path)

        # remove any dirs/files in skip_all for next iteration
        dirs[:] = [d for d in dirs if d not in skip_all]
        files[:] = [f for f in files if f not in skip_all]

        # header
        exclude = skip_all + skip_file + skip_header
        _filter_header(root, files, exclude)
        print('')

        # text
        exclude = skip_all + skip_file + skip_text
        _filter_text(root, files, exclude)
        print('')

        # path
        exclude = skip_all + skip_path
        _filter_path(root, files, exclude)
        print('')


# ------------------------------------------------------------------------------


def _filter_header(root, files, exclude):
    root_name = os.path.basename(root)
    if root_name not in exclude:
        for file_name in files:
            if file_name not in exclude:
                path = os.path.join(root, file_name)
                _fix_header(path)


def _filter_text(root, files, exclude):
    root_name = os.path.basename(root)
    if root_name not in exclude:
        for file_name in files:
            if file_name not in exclude:
                path = os.path.join(root, file_name)
                _fix_text(path)


def _filter_path(root, files, exclude):
    root_name = os.path.basename(root)
    if root_name not in exclude:
        for file_name in files:
            if file_name not in exclude:
                path = os.path.join(root, file_name)
                _fix_path(path)
        _fix_path(root)


# ------------------------------------------------------------------------------


def _fix_readme(path):
    print('_fix_readme:', path)


def _fix_header(path):
    print('_fix_header: ', path)


def _fix_text(path):
    print('_fix_text:', path)


def _fix_path(path):
    print('_fix_path:', path)


# ------------------------------------------------------------------------------


walk(DIR_PRJ)
