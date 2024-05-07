# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module modifies the current project to replace metadata in each of the
files, according to the data present in the conf files.
"""

# TODO: pybaker ask for ver or default, update meta, check for dunders, make
# install.py, make dist
# TODO: pybaker not rely so much on regex, more on context start/end

# TODO: this prog should:
# show current version number
# ask for new version number
# read a dict of what to put in dist
# TODO: when run, ask for new version str (default: old version str
# put that new version str in metadata file)

# ------------------------------------------------------------------------------

# TODO: pull in a fresh copy of libs on every run and put it in dist
# we need to get the location of PyPlate from settings (src)
# we need the name of the "lib" folder from settings (dst)
# TODO: any time pybaker encounters a file with __PC_DATE__ still in the
# header, make sure to use today's date, not the one stored in a config dict
# TODO: install script must install libs, src, etc. into proper folders
# TODO: installer for pkg should move pkg to __PC_USER_LIB__

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from datetime import date
import json

# TODO: get rid of this
import os
from pathlib import Path
import re
import shlex
import subprocess

# local imports
from cnlib.cnpot import CNPotPy  # type: ignore
from EVERYTHING.cntree import CNTree

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = True

# some useful constants
_DIR_SELF = Path(__file__).parent

# this is the project dir
_DIR_PRJ = _DIR_SELF.parent

# default blacklist dict
DICT_BLACKLIST = {}

# default metadata dict
DICT_METADATA = {}

# default settings dict
DICT_SETTINGS = {}

# get list of approved categories
# https://specifications.freedesktop.org/menu-spec/latest/apa.html
LIST_CATEGORIES = [
    "AudioVideo",
    "Audio",
    "Video",
    "Development",
    "Education",
    "Game",
    "Graphics",
    "Network",
    "Office",
    "Science",
    "Settings",
    "System",
    "Utility",
    "Building",
    "Debugger",
    "IDE",
    "GUIDesigner",
    "Profiling",
    "RevisionControl",
    "Translation",
    "Calendar",
    "ContactManagement",
    "Database",
    "Dictionary",
    "Chart",
    "Email",
    "Finance",
    "FlowChart",
    "PDA",
    "ProjectManagement",
    "Presentation",
    "Spreadsheet",
    "WordProcessor",
    "2DGraphics",
    "VectorGraphics",
    "RasterGraphics",
    "3DGraphics",
    "Scanning",
    "OCR",
    "Photography",
    "Publishing",
    "Viewer",
    "TextTools",
    "DesktopSettings",
    "HardwareSettings",
    "Printing",
    "PackageManager",
    "Dialup",
    "InstantMessaging",
    "Chat",
    "IRCClient",
    "Feed",
    "FileTransfer",
    "HamRadio",
    "News",
    "P2P",
    "RemoteAccess",
    "Telephony",
    "TelephonyTools",
    "VideoConference",
    "WebBrowser",
    "WebDevelopment",
    "Midi",
    "Mixer",
    "Sequencer",
    "Tuner",
    "TV",
    "AudioVideoEditing",
    "Player",
    "Recorder",
    "DiscBurning",
    "ActionGame",
    "AdventureGame",
    "ArcadeGame",
    "BoardGame",
    "BlocksGame",
    "CardGame",
    "KidsGame",
    "LogicGame",
    "RolePlaying",
    "Shooter",
    "Simulation",
    "SportsGame",
    "StrategyGame",
    "Art",
    "Construction",
    "Music",
    "Languages",
    "ArtificialIntelligence",
    "Astronomy",
    "Biology",
    "Chemistry",
    "ComputerScience",
    "DataVisualization",
    "Economy",
    "Electricity",
    "Geography",
    "Geology",
    "Geoscience",
    "History",
    "Humanities",
    "ImageProcessing",
    "Literature",
    "Maps",
    "Math",
    "NumericalAnalysis",
    "MedicalSoftware",
    "Physics",
    "Robotics",
    "Spirituality",
    "Sports",
    "ParallelComputing",
    "Amusement",
    "Archiving",
    "Compression",
    "Electronics",
    "Emulator",
    "Engineering",
    "FileTools",
    "FileManager",
    "TerminalEmulator",
    "Filesystem",
    "Monitor",
    "Security",
    "Accessibility",
    "Calculator",
    "Clock",
    "TextEditor",
    "Documentation",
    "Adult",
    "Core",
    "KDE",
    "GNOME",
    "XFCE",
    "DDE",
    "GTK",
    "Qt",
    "Motif",
    "Java",
    "ConsoleOnly",
    "Screensaver",
    "TrayIcon",
    "Applet",
    "Shell",
]

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# keep track of error count
G_ERROR_COUNT = 0

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

G_STRINGS = {
    "S_ERR_COUNT": "Errors: {}",
    "S_ERR_UFNF": "ERROR: File {} could not be found, trying default",
    "S_ERR_UJSON": "ERROR: FIle {} is not a valid JSON file, trying default",
    "S_ERR_DFNF": "ERROR: Default file {} could not be found",
    "S_ERR_DJSON": "ERROR: Default file {} is not a valid JSON file",
}

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Main function of the program
# ------------------------------------------------------------------------------
def main():
    """
    Main function of the program

    Main entry point for the program, initializing the program, and performing
    its steps.
    """

    # common
    load_config_files()
    fix_blacklist()
    fix_readme()

    # pkg
    fix_pyproject()
    # fix_init()

    # cli/gui
    fix_argparse()
    fix_install()

    # gui
    fix_desktop()
    fix_gtk3()

    # check for dunders left over or we missed
    recurse_and_check(_DIR_PRJ)

    # do housekeeping
    do_extras()

    # do gettext stuff
    # do_gettext()

    # # print error count (dunder stuff found)
    s = G_STRINGS["S_ERR_COUNT"]
    print(s.format(G_ERROR_COUNT))


# ------------------------------------------------------------------------------
# Load the required config files
# ------------------------------------------------------------------------------
def load_config_files():
    """
    Load the required config files

    Get required config files and load them into the dictionaries required
    by the program. These files may sometimes be edited by users, so we need to
    check that they:
    (1. exist)
    or
    (2. get backup)
    and
    (3. are valid JSON).
    """

    try:
        a_dict = DICT_BLACKLIST
        a_user = _DIR_PRJ / "conf" / "blacklist.json"
        a_default = _DIR_PRJ / "conf" / "default" / "blacklist_default.json"
        _load_user_or_default(a_dict, a_user, a_default)
    except:
        # if we can't load user or default, exit the program
        exit()

    try:
        a_dict = DICT_METADATA
        a_user = _DIR_PRJ / "conf" / "metadata.json"
        a_default = _DIR_PRJ / "conf" / "default" / "metadata_default.json"
        _load_user_or_default(a_dict, a_user, a_default)
    except:
        # if we can't load user or default, exit the program
        exit()

    try:
        a_dict = DICT_SETTINGS
        a_user = _DIR_PRJ / "conf" / "metadata.json"
        a_default = _DIR_PRJ / "conf" / "default" / "settings_default.json"
        _load_user_or_default(a_dict, a_user, a_default)
    except:
        # if we can't load user or default, exit the program
        exit()

    # # default blacklist dict
    # global DICT_BLACKLIST

    # # get user file or default
    # path_blacklist = _DIR_PRJ / "conf" / "blacklist.json"
    # if not path_blacklist.exists():
    #     path_blacklist = (
    #         _DIR_PRJ / "conf" / "defaults" / "blacklist_default.json"
    #     )
    #     if not path_blacklist.exists():
    #         raise Exception(G_STRINGS["S_ERR_FNF"].format(path_blacklist))

    # # load file
    # with open(path_blacklist, "r", encoding="UTF8") as a_file:
    #     DICT_BLACKLIST = json.load(a_file)
    #     try:
    #         DICT_BLACKLIST = json.load(a_file)
    #     except json.JSONDecodeError:
    #         raise Exception(G_STRINGS["S_ERR_JSON"].format(a_file))

    # # default settings dict
    # global DICT_SETTINGS
    # path_settings = _DIR_PRJ / "conf" / "settings.json"
    # if path_settings.exists():
    #     with open(path_settings, "r", encoding="UTF8") as a_file:
    #         try:
    #             DICT_SETTINGS = json.load(a_file)
    #         except json.JSONDecodeError:
    #             print(G_STRINGS["S_ERR_JSON"].format(a_file))
    #             return

    # # default strings dict
    # global DICT_METADATA
    # path_strings = _DIR_PRJ / "conf" / "strings.json"
    # if path_strings.exists():
    #     with open(path_strings, "r", encoding="UTF8") as a_file:
    #         try:
    #             DICT_METADATA = json.load(a_file)
    #         except json.JSONDecodeError:
    #             print(G_STRINGS["S_ERR_JSON"].format(a_file))
    #             return


# ------------------------------------------------------------------------------
# Replace values in the blacklist file
# ------------------------------------------------------------------------------
def fix_blacklist():
    """
    Replace values in the blacklist file

    Replace any dunders in blacklist file. This allows you to use file
    names/paths in blacklist.json that have dunders in their value. This is
    really only useful if you use dunders in the user blacklist, since
    they get replaced each time you run pybaker.py, and at that time you
    know what the replacement values will be.
    """

    # get path to blacklist file
    path_blacklist = _DIR_PRJ / "conf" / "blacklist.json"

    # open file and get contents
    with open(path_blacklist, "r", encoding="UTF8") as a_file:
        text = a_file.read()

        # replace text
        for key, val in DICT_BLACKLIST.items():
            text = text.replace(key, val)

    # save file
    with open(path_blacklist, "w", encoding="UTF8") as a_file:
        a_file.write(text)

    # now that the blacklist file is fixed, reload it
    global DICT_BLACKLIST
    path_blacklist = _DIR_PRJ / "conf" / "blacklist.json"
    if path_blacklist.exists():
        with open(path_blacklist, "r", encoding="UTF8") as a_file:
            try:
                DICT_BLACKLIST = json.load(a_file)
            except json.JSONDecodeError:
                print(G_STRINGS["S_ERR_JSON"].format(a_file))
                return


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
    path_readme = _DIR_PRJ / "README.md"
    if not path_readme.exists():
        return

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path_readme, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # replace short description
    str_pattern = (
        r"(<!--[\t ]*__RM_SHORT_DESC_START__[\t ]*-->)"
        r"(.*?)"
        r"(<!--[\t ]*__RM_SHORT_DESC_END__[\t ]*-->)"
    )

    # replace short_desc
    pp_short_desc = DICT_METADATA["__PM_SHORT_DESC__"]

    # replace text
    str_rep = rf"\g<1>\n{pp_short_desc}\n\g<3>"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace dependencies array
    str_pattern = (
        r"(<!--[\t ]*__RM_PY_DEPS_START__[\t ]*-->)"
        r"(.*?)"
        r"(<!--[\t ]*__RM_PY_DEPS_END__[\t ]*-->)"
    )

    # build a string from the dict (markdown links)
    # only format links if value is not empty
    pp_py_deps = DICT_METADATA["__PM_PY_DEPS__"]
    kv_py_deps = []
    for key, val in pp_py_deps.items():
        if val == "":
            kv_py_deps.append(key)
        else:
            kv_py_deps.append(f"[{key}]({val})")

    # build a string (or none) for the deps
    if len(kv_py_deps) == 0:
        str_py_deps = "None"
    else:
        str_py_deps = "<br>\n".join(kv_py_deps)

    # replace text
    str_rep = rf"\g<1>\n{str_py_deps}\n\g<3>"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace version
    pp_version = DICT_METADATA["__PM_VERSION__"]

    str_pattern = (
        r"(\s*foo@bar:~/Downloads\$ python -m pip install )"
        r"(.*-)"
        r"(.*?)"
        r"(\.tar\.gz)"
    )
    str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
    text = re.sub(str_pattern, str_rep, text)

    str_pattern = (
        r"(\s*foo@bar:~/Downloads/)"
        r"(.*?)"
        r"(\$ python -m pip install ./dist/)"
        r"(.*-)"
        r"(.*?)"
        r"(\.tar\.gz)"
    )
    str_rep = rf"\g<1>\g<2>\g<3>\g<4>{pp_version}\g<6>"
    text = re.sub(str_pattern, str_rep, text)

    str_pattern = r"(\s*foo@bar:~\$ cd ~/Downloads/)" r"(.*-)" r"(.*)"
    str_rep = rf"\g<1>\g<2>{pp_version}"
    text = re.sub(str_pattern, str_rep, text)

    str_pattern = (
        r"(\s*foo@bar:~/Downloads/)" r"(.*-)" r"(.*)" r"(\$ \./install.py)"
    )
    str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
    text = re.sub(str_pattern, str_rep, text)

    # save file
    with open(path_readme, "w", encoding="UTF8") as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the pyproject file
# ------------------------------------------------------------------------------
def fix_pyproject():
    """
    Replace text in the pyproject file

    Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # check if the file exists
    path_toml = _DIR_PRJ / "pyproject.toml"
    if not path_toml.exists():
        return

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path_toml, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # NB: we do a dunder replace here because putting a dunder as the
    # default name in the toml file causes the linter to choke, so we use a
    # dummy name

    # replace name
    str_pattern = (
        r"(^\s*\[project\]\s*$)" r"(.*?)" r"(^\s*name[\t ]*=[\t ]*)" r"(.*?$)"
    )
    pp_name_small = DICT_SETTINGS["info"]["__PC_NAME_SMALL__"]
    str_rep = rf'\g<1>\g<2>\g<3>"{pp_name_small}"'
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace version
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*version[\t ]*=[\t ]*)"
        r"(.*?$)"
    )
    pp_version = DICT_METADATA["__PM_VERSION__"]
    if pp_version == "":
        pp_version = S.DEF_VERSION
    str_rep = rf'\g<1>\g<2>\g<3>"{pp_version}"'
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*description[\t ]*=[\t ]*)"
        r"(.*?$)"
    )
    pp_short_desc = DICT_METADATA["__PM_SHORT_DESC__"]
    str_rep = rf'\g<1>\g<2>\g<3>"{pp_short_desc}"'
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # # replace keywords array
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*keywords[\t ]*=[\t ]*)"
        r"(.*?\])"
    )

    # convert dict to string
    pp_keywords = DICT_METADATA["__PM_KEYWORDS__"]
    str_pp_keywords = [f'"{item}"' for item in pp_keywords]
    str_pp_keywords = ", ".join(str_pp_keywords)

    # replace string
    str_rep = rf"\g<1>\g<2>\g<3>[{str_pp_keywords}]"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace dependencies array
    str_pattern = (
        r"(^\s*\[project\]\s*$)"
        r"(.*?)"
        r"(^\s*dependencies[\t ]*=[\t ]*)"
        r"(.*?\])"
    )

    # convert dict to string (only using keys)
    pp_py_deps = DICT_METADATA["__PM_PY_DEPS__"]

    # NB: this is not conducive to a dict (we don't need links, only names)
    # so don't do what we did in README, keep it simple
    list_py_deps = [item for item in pp_py_deps.keys()]
    str_pp_py_deps = [f'"{item}"' for item in list_py_deps]
    str_pp_py_deps = ", ".join(str_pp_py_deps)

    # replace text
    str_rep = rf"\g<1>\g<2>\g<3>[{str_pp_py_deps}]"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_toml, "w", encoding="UTF8") as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the __init__.py file
# ------------------------------------------------------------------------------
# TODO: remove this (init files are always empty now)
# def fix_init():
#     """
#     Replace text in the __init__.py file

#     Replaces the 'from __PC_NAME_SMALL__ import filename' text in the
#     __init__.py file.
#     """

#     # first check if there is a pkg dir
#     pp_name_small = DICT_SETTINGS["info"]["__PC_NAME_SMALL__"]
#     dir_pkg = _DIR_PRJ / "src" / pp_name_small
#     if not dir_pkg.exists() or not dir_pkg.is_dir():
#         return

#     # the file name of the init
#     file_init = "__init__.py"

#     # check if there is an __init__.py file
#     path_init = dir_pkg / file_init
#     if not path_init.exists():
#         return

#     # check if there are any .py files in package dir that are not init file
#     lst_modules = [
#         item for item in os.listdir(dir_pkg) if item != file_init and item.suffix == "py"
#     ]
#     if len(lst_modules) == 0:
#         return

#     # strip ext and add to list
#     lst_files = [item.with_suffix("") for item in lst_modules]

#     # sort file list to look pretty (listdir is not sorted)
#     lst_files.sort()

#     # format list for imports section
#     lst_imports = ["from {pp_small} import {item}" "for item in lst_files"]
#     str_imports = "\n".join(lst_imports)

#     # format __all__ for completeness
#     lst_all = [f"'{item}'" for item in lst_files]
#     str_all_join = ", ".join(lst_all)
#     str_all = f"__all__ = [{str_all_join}]"

#     # default text if we can't open file
#     text = ""

#     # open file and get contents
#     with open(path_init, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # replace imports block
#     str_pattern = (
#         r"(^#[\t ]*__PD_IMPORTS_START__[\t ]*)"
#         r"(.*?)"
#         r"(^#[\t ]*__PD_IMPORTS_END__[\t ]*)"
#     )
#     str_rep = rf"\g<1>\n{str_imports}\n{str_all}\n\g<3>"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # save file
#     with open(path_init, "w", encoding="UTF8") as a_file:
#         a_file.write(text)


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

    # get all paths
    lst_paths = [dir_src / item for item in os.listdir(dir_src)]
    if len(lst_paths) == 0:
        return

    # get all files
    lst_files = [
        item for item in lst_paths if item.is_file() and item.suffix == ".py"
    ]

    # for each file
    for item in lst_files:
        # get the whole path
        path_item = dir_src / item

        # check if file exists
        if not path_item.exists() or path_item.is_dir():
            continue

        # default text if we can't open file
        text = ""

        # open file and get contents
        with open(path_item, "r", encoding="UTF8") as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = (
            r"(import argparse.*def _parse_args\(\):.*)"
            r"(argparse.ArgumentParser\(\s*description=\')"
            r"(.*?)"
            r"(\'.*)"
        )
        pp_short_desc = DICT_METADATA["__PM_SHORT_DESC__"]
        str_rep = rf"\g<1>\g<2>{pp_short_desc}\g<4>"
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # replace version
        str_pattern = (
            r"(import argparse.*def _parse_args\(\):.*)"
            r"(print\(\'.* version )"
            r"(.*?)"
            r"(\'.*)"
        )
        pp_version = DICT_METADATA["__PM_VERSION__"]
        str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
        text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

        # save file
        with open(path_item, "w", encoding="UTF8") as a_file:
            a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the install file
# ------------------------------------------------------------------------------
def fix_install():
    """
    Replace text in the install file

    Replaces the system and Python dependencies in the install file.
    """

    # check if the file exists
    path_install = _DIR_PRJ / "install.py"
    if not path_install.exists():
        return

    # default text if we can't open file
    text = ""

    # open file and get content
    with open(path_install, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # replace python dependencies array
    str_pattern = (
        r"(^\s*dict_install[\t ]*=\s*{)"
        r"(.*?)"
        r"(^\s*\'py_deps\'[\t ]*:)"
        r"(.*?\])"
    )

    # convert dict keys to string
    pp_py_deps = DICT_METADATA["__PM_PY_DEPS__"]
    str_pp_py_deps = ",".join(pp_py_deps.keys())

    # replace text
    str_rep = rf"\g<1>\g<2>\g<3> [\n\t\t{str_pp_py_deps}\n\t]"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace system dependencies array
    str_pattern = (
        r"(^\s*dict_install[\t ]*=)"
        r"(.*?)"
        r"(^\s*\'sys_deps\'[\t ]*:)"
        r"(.*?\])"
    )

    # convert dict to string
    pp_sys_deps = DICT_METADATA["__PM_SYS_DEPS__"]
    str_pp_sys_deps = ",".join(pp_sys_deps)

    # replace string
    str_rep = rf"\g<1>\g<2>\g<3> [\n\t\t{str_pp_sys_deps}\n\t]"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_install, "w", encoding="UTF8") as a_file:
        a_file.write(text)


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
    global G_ERROR_COUNT

    # check if the file exists
    pp_name_small = DICT_SETTINGS["info"]["__PC_NAME_SMALL__"]
    path_desk = os.path.join(_DIR_PRJ, "src", f"{pp_name_small}.desktop")
    if not os.path.exists(path_desk):
        return

    # validate wanted categories into approved categories
    pp_gui_categories = []
    wanted_cats = DICT_METADATA["__PM_GUI_CATS__"]
    for cat in wanted_cats:
        # category is valid
        if cat in LIST_CATEGORIES:
            # add to final list
            pp_gui_categories.append(cat)
        else:
            # category is not valid, print error and increase error count
            print(
                f'In PP_GUI_CATEGORIES, "{cat}" is not valid, see \n'
                "https://specifications.freedesktop.org/menu-spec/latest/apa.html"
            )
            G_ERROR_COUNT += 1

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path_desk, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # replace categories
    str_pattern = (
        r"(^\s*\[Desktop Entry\]\s*$)"
        r"(.*?)"
        r"(^\s*Categories[\t ]*=)"
        r"(.*?$)"
    )

    # convert dict to string
    str_cat = ";".join(pp_gui_categories)
    str_cat += ";"

    # replace text
    str_rep = rf"\g<1>\g<2>\g<3>{str_cat}"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = (
        r"(^\s*\[Desktop Entry\]\s*$)"
        r"(.*?)"
        r"(^\s*Comment[\t ]*=)"
        r"(.*?$)"
    )
    pp_short_desc = DICT_METADATA["__PM_SHORT_DESC__"]
    str_rep = rf"\g<1>\g<2>\g<3>{pp_short_desc}"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # get path to install dir
    path_home = os.path.expanduser("~")
    author = DICT_SETTINGS["info"]["__PD_AUTHOR__"]
    pp_name_big = DICT_SETTINGS["info"]["__PC_NAME_BIG__"]
    path_inst = os.path.join(path_home, f".{author}", pp_name_big, "src")

    # replace exec
    str_pattern = (
        r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Exec[\t ]*=)" r"(.*?$)"
    )
    path_exec = os.path.join(path_inst, f"{pp_name_small}.py")
    str_rep = rf"\g<1>\g<2>\g<3>{path_exec}"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace icon
    str_pattern = (
        r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Icon[\t ]*=)" r"(.*?$)"
    )
    path_icon = os.path.join(path_inst, f"{pp_name_small}.png")
    str_rep = rf"\g<1>\g<2>\g<3>{path_icon}"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace path
    str_pattern = (
        r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Path[\t ]*=)" r"(.*?$)"
    )
    str_rep = rf"\g<1>\g<2>\g<3>{path_inst}"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_desk, "w", encoding="UTF8") as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the UI file
# ------------------------------------------------------------------------------
def fix_gtk3():
    """
    Replace text in the UI file

    Replace description and version number in the UI file.
    """

    # check if there is a .ui file
    pp_name_small = DICT_SETTINGS["info"]["__PC_NAME_SMALL__"]
    path_ui = os.path.join(_DIR_PRJ, "src", f"{pp_name_small}_gtk3.ui")
    if not os.path.exists(path_ui):
        return

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path_ui, "r", encoding="UTF8") as a_file:
        text = a_file.read()

    # replace short description
    str_pattern = (
        r"(<object class=\"GtkAboutDialog\".*?)"
        r"(<property name=\"comments\".*?\>)"
        r"(.*?)"
        r"(</property>)"
    )
    pp_short_desc = DICT_METADATA["__PM_SHORT_DESC__"]
    str_rep = rf"\g<1>\g<2>{pp_short_desc}\g<4>"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace version
    str_pattern = (
        r"(<object class=\"GtkAboutDialog\".*?)"
        r"(<property name=\"version\">)"
        r"(.*?)"
        r"(</property>.*)"
    )
    pp_version = DICT_METADATA["__PM_VERSION__"]
    str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path_ui, "w", encoding="UTF8") as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Recurse through the folder structure looking for errors
# ------------------------------------------------------------------------------
def recurse_and_check(path):
    """
    Recurses through the folder structure looking for errors

    Arguments:
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
    skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_all"]]
    skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_file"]]
    skip_header = [
        item.strip(os.sep) for item in DICT_BLACKLIST["skip_header"]
    ]
    skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_text"]]
    skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_path"]]

    # get list of replaceable file names
    items = [item for item in os.listdir(path) if item not in skip_all]
    for item in items:
        # put path back together
        path_item = os.path.join(path, item)

        # if it's a dir
        if os.path.isdir(path_item):
            # recurse itself to find more files
            recurse_and_check(path_item)

        else:
            # only open files we should be mucking in
            if item not in skip_file:
                # default lines if we can't open file
                lines = []

                # open file and get lines
                with open(path_item, "r", encoding="UTF8") as a_file:
                    lines = a_file.readlines()

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
    os.chdir(_DIR_PRJ)

    # add requirements
    path_req = os.path.join(_DIR_PRJ, "requirements.txt")
    with open(path_req, "w", encoding="UTF8") as a_file:
        cmd = "python -m pip freeze -l --exclude-editable --require-virtualenv"
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=a_file, check=False)

    # update CHANGELOG
    path_chg = os.path.join(_DIR_PRJ, "CHANGELOG.md")
    with open(path_chg, "w", encoding="UTF8") as a_file:
        cmd = 'git log --pretty="%ad - %s"'
        cmd_array = shlex.split(cmd)
        subprocess.run(cmd_array, stdout=a_file, check=False)

    # get tree path
    path_tree = os.path.join(_DIR_PRJ, "misc", "tree.txt")

    # if not exist
    # if not os.path.exists(path_tree):

    # # create tree object and call
    # p_t = pytree.PyTree()
    # TODO: make this use blacklist
    # tree = p_t.build_tree(_DIR_PRJ, DICT_SETTINGS['__PP_TREE_IGNORE__'])

    # # write tree to file
    # with open(path_tree, 'w', encoding='UTF8') as a_file:
    #     a_file.write(tree)

    # update docs
    # NB: this is ugly and stupid, but it's the only way to get pdoc3 to work

    # move into src dir
    # dir_src = os.path.join(_DIR_PRJ, 'src')
    # os.chdir(dir_src)

    # # get docs dir
    # path_docs = os.path.join('..', 'docs')
    # path_docs = os.path.abspath(path_docs)

    # # # update docs
    # cmd = f'python -m pdoc --html -f -o {path_docs} .'
    # cmd_array = shlex.split(cmd)
    # subprocess.run(cmd_array, check=False)

    # # go back to old dir
    # os.chdir(dir_curr)


# ------------------------------------------------------------------------------
# Run xgettext over files to produce a locale template
# ------------------------------------------------------------------------------
# def do_gettext():
#     """
#     Run xgettext over files to produce a locale template

#     Use xgettext to scan .py and .ui files for I18N strings and collect them
#     int a .pot file in the locale folder. Only applies to gui projects at
#     the moment.
#     """

#     # check if we are a gui project
#     is_gui = DICT_SETTINGS["project"]["type"] == "g"
#     if not is_gui:
#         return

#     # get locale folder and pot filename
#     dir_locale = os.path.join(_DIR_PRJ, "src", "locale")
#     pp_name_small = DICT_SETTINGS["info"]["__PC_NAME_SMALL__"]
#     path_pot = os.path.join(dir_locale, f"{pp_name_small}.pot")
#     pp_version = DICT_METADATA["__PM_VERSION__"]

#     # remove old pot and recreate empty file
#     if os.path.exists(path_pot):
#         os.remove(path_pot)
#     with open(path_pot, "w", encoding="UTF8") as a_file:
#         a_file.write("")

#     # build a list of files
#     res = []
#     exts = [".py", ".ui", ".glade"]

#     # scan for files in src directory
#     dir_src = os.path.join(_DIR_PRJ, "src")
#     list_files = os.listdir(dir_src)

#     # for each file in dir
#     for file in list_files:
#         # check for ext
#         for ext in exts:
#             if file.endswith(ext):
#                 # rebuild complete path and add to list
#                 path = os.path.join(dir_src, file)
#                 res.append(path)

#     # for each file that can be I18N'd, run xgettext
#     author = DICT_SETTINGS["info"]["__PD_AUTHOR__"]
#     email = DICT_SETTINGS["info"]["__PD_EMAIL__"]
#     for file in res:
#         cmd = (
#             "xgettext "  # the xgettext cmd
#             f"{file} "  # the file name
#             "-j "  # append to current file
#             '-c"I18N:" '  # look for tags in .py files
#             "--no-location "  # don't print filename/line number
#             f"-o {path_pot} "  # location of output file
#             "-F "  # sort output by input file
#             f"--copyright-holder={author} "
#             f"--package-name={pp_name_small} "
#             f"--package-version={pp_version} "
#             f"--msgid-bugs-address={email}"
#         )
#         cmd_array = shlex.split(cmd)
#         subprocess.run(cmd_array, check=False)

#     # now lets do some text replacements to make it look nice

#     # default text if we can't open file
#     text = ""

#     # open file and get contents
#     with open(path_pot, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # replace short description
#     str_pattern = r"(# SOME DESCRIPTIVE TITLE.)"
#     pp_name_big = DICT_SETTINGS["info"]["__PC_NAME_BIG__"]
#     str_rep = f"# {pp_name_big} translation template"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace copyright
#     author = DICT_SETTINGS["info"]["__PD_AUTHOR__"]
#     str_pattern = r"(# Copyright \(C\) )" r"(.*?)" rf"( {author})"
#     year = date.today().year
#     str_rep = rf"\g<1>{year}\g<3>"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace author's email
#     str_pattern = r"(# FIRST AUTHOR )" r"(<EMAIL@ADDRESS>)" r"(, )" r"(YEAR)"
#     email = DICT_SETTINGS["info"]["__PD_EMAIL__"]
#     year = date.today().year
#     str_rep = rf"\g<1>{email}\g<3>{year}"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace charset
#     str_pattern = (
#         r'("Content-Type: text/plain; charset=)' r"(CHARSET)" r'(\\n")'
#     )
#     charset = "UTF-8"
#     str_rep = rf"\g<1>{charset}\g<3>"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # save file
#     with open(path_pot, "w", encoding="UTF8") as a_file:
#         a_file.write(text)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Opens the user or default config file, whichever is found first
# ------------------------------------------------------------------------------
def _load_user_or_default(a_dict, a_user, a_default):
    """
    Opens the user or default config file, whichever is found first

    Arguments:
        a_dict: Dictionary to load JSON file into
        a_user: User Path to load dict from
        a_default: Path to default file if user file is not found

    Raises:
        Exception: if neither file can be found or if both files are invalid
        JSON

    This is a convenience function to load a JSON file into a dict. If the user
    file is not found, it tries to load the default file. If neither file is
    found or they are both invalid JSON files, an Exception is raised.
    """

    # check if user file exists
    if a_user.exists():

        # try to load user file
        try:
            a_dict = json.load(a_user)
            return

        # we can't load it
        except json.JSONDecodeError:
            print(G_STRINGS["S_ERR_UJSON"].format(a_user))

    # we can't find it
    else:
        print(G_STRINGS["S_ERR_UFNF"].format(a_user))

    # check if default file exists
    if a_default.exists():

        # try to load default file
        try:
            a_dict = json.load(a_default)

            # save default as user
            with open(a_user, "w", encoding="UTF-8") as f:
                f.write(a_dict)

            # done
            return

        # we can't load it
        except json.JSONDecodeError:
            print(G_STRINGS["S_ERR_DJSON"].format(a_default))

    # we can't find it
    else:
        print(G_STRINGS["S_ERR_DFNF"].format(a_default))

    # we can't find it or load it
    raise Exception


# ------------------------------------------------------------------------------
# Checks header values for dunders
# ------------------------------------------------------------------------------
def _check_header(path_item, lines):
    """
    Checks header values for dunders

    Arguments:
        path_item: The full path to file to be checked for header
        lines: The contents of the file to be checked

    This function checks the files headers for values that either do not
    match the file's project/file name, or do not have a date set.
    This method is private because it is only called from inside
    recurse_and_check().
    """

    # global error count
    global G_ERROR_COUNT

    # for each line in file
    for i, line in enumerate(lines):
        # check project name
        prj_name = os.path.basename(_DIR_PRJ)
        str_pattern = (
            r"(^\s*(<!--|#)\s*)" r"(Project)" r"(\s*:\s*)" r"(.*?)" r"(\s)"
        )
        str_res = re.search(str_pattern, line, flags=re.M | re.S)
        if str_res and str_res.group(5) != prj_name:
            print(
                f"{path_item}:{i + 1}: Header Project name should be "
                f"'{prj_name}'"
            )

            # inc error count
            G_ERROR_COUNT += 1

        # check file name
        file_name = os.path.basename(path_item)
        str_pattern = (
            r"(^\s*(<!--|#)\s*)" r"(Filename)" r"(\s*:\s*)" r"(.*?)" r"(\s)"
        )
        str_res = re.search(str_pattern, line, flags=re.M | re.S)
        if str_res and str_res.group(5) != file_name:
            print(
                f"{path_item}:{i + 1}: Header Filename should be "
                f"'{file_name}'"
            )

            # inc error count
            G_ERROR_COUNT += 1

        # check date
        str_pattern = (
            r"(^\s*(<!--|#)\s*)" r"(Date)" r"(\s*:\s*)" r"(.*?)" r"(\s)"
        )
        str_res = re.search(str_pattern, line, flags=re.M | re.S)
        if str_res:
            # there is *something* in the date field
            if str_res.group(5) != "":
                # check for valid date
                str_pattern2 = r"\d*/\d*/\d*"
                str_res2 = re.search(str_pattern2, str_res.group(5))
                if not str_res2:
                    print(f"{path_item}:{i + 1}: Header Date is not set")

                    # inc error count
                    G_ERROR_COUNT += 1

            else:
                print(f"{path_item}:{i + 1}: Header Date is not set")

                # inc error count
                G_ERROR_COUNT += 1


# ------------------------------------------------------------------------------
# Checks file contents for replacements
# ------------------------------------------------------------------------------
def _check_text(path_item, lines):
    """
    Checks file contents for replacements

    Arguments:
        path_item: The full path to file to be checked for text
        lines: The contents of the file to be checked

    This function checks that none of the files contains an unreplaced
    replacement variable from the initial project info.
    This method is private because it is only called from inside
    recurse_and_check().
    """

    # global error count
    global G_ERROR_COUNT

    # for each line in file
    for i, line in enumerate(lines):
        # the dunders to look for
        reps = [rep for rep in DICT_SETTINGS["info"] and DICT_METADATA]

        # check for dunders in text
        for rep in reps:
            if rep in line:
                print(f"{path_item}:{i + 1}: Text contains {rep}")

                # inc error count
                G_ERROR_COUNT += 1


# ------------------------------------------------------------------------------
# Checks file paths for dunders
# ------------------------------------------------------------------------------
def _check_path(path_item):
    """
    Checks file paths for dunders

    Arguments:
        path_item: The full path to file to be checked for path

    This function checks that none of the files paths contains an unreplaced
    dunder variable from the initial project info.
    This method is private because it is only called from inside
    recurse_and_check().
    """

    # global error count
    global G_ERROR_COUNT

    # TODO make this use __PD, __PC, __PM
    # check for dunders in path
    if "__PP_" in path_item:
        print(f"{path_item}: Path contains __PP_")

        # inc error count
        G_ERROR_COUNT += 1


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file
    # is invoked from the command line.

    # run main function
    main()

# -)
