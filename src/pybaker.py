#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A program to set the metadata of a PyPlate project and create a dist

This module sets the project metadata in each of the files, according to the
data present in the conf files. It then sets up the dist folder with all
necessary files to create a complete distribution of the project.
"""

# TODO: for each file in proj, use blacklist and D_CFG/D_ADD/etc to find and
# dunder that is not in comment
# report that as error

# TODO: replace all PB_VERSION with new version, across all files in prj dir
# TODO: fix every metadata using choice menu for new value
# gonna need a lot of regex in pybaker.conf
# TODO: do we need D_PRJ_DEF/D_PRJ_DIST_DIRS?
# TODO: what do we need from D_PRJ_CFG? just __PP_DEV_PP__?

# DONE ask for meta
# DONE update meta in conf file
# replace (or just report) any dunders
# replace metadata using prj pybaker (context is prj or dev specific)
# make install.py
# make dist (list of prj stuff into assets folder, install and README.md alongside)

# TODO: pybaker not rely so much on regex, more on context start/end

# ------------------------------------------------------------------------------

# TODO: pull in a fresh copy of libs on every run and put it in dist
# we need to get the location of PyPlate from settings (src)
# we need the name of the "lib" folder from settings (dst)
# TODO: any time pybaker encounters a file with __PP_DATE__ still in the
# header, make sure to use today's date, not the one stored in a config dict
# TODO: install script must install libs, src, etc. into proper folders
# TODO: installer for pkg should move pkg to __PP_USER_LIB__

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# path to this project
# parent is src, parents[1] is PyPlate
# NB: needed to get imports from conf (bootstrap)
P_DIR_PYPLATE = Path(__file__).parents[1].resolve()
P_DIR_PP_LIB = P_DIR_PYPLATE / "lib"
sys.path.append(str(P_DIR_PYPLATE))
sys.path.append(str(P_DIR_PP_LIB))

# local imports
from conf import pybaker_conf as B  # type:ignore
from cnlib import cnfunctions as F  # type: ignore
from cnlib.cnformatter import CNFormatter  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# this is our metadata bootstrap

# get names
S_PP_NAME_BIG = "PyBaker"
S_PP_NAME_SMALL = "pybaker"
S_PP_SHORT_DESC = (
    "A program to set the metadata of a PyPlate project and create a dist"
)

# formatted version
S_PP_VER_FMT = f"Version {B.S_VERSION}"

# about string
S_PP_ABOUT = (
    f"{S_PP_NAME_SMALL}\n"
    f"{S_PP_SHORT_DESC}\n"
    f"{S_PP_VER_FMT}\n"
    f"https://www.github.com/cyclopticnerve/PyPlate"
)

# debug option strings
S_DBG_OPTION = "-d"
S_DBG_ACTION = "store_true"
S_DBG_DEST = "DBG_DEST"
S_DBG_HELP = "enable debugging option"

# folder option strings
S_PRJ_OPTION = "-f"
S_PRJ_METAVAR = "PROJECT DIR"
S_PRJ_DEST = "PRJ_DEST"
S_PRJ_HELP = "the project directory to bake"

# path to prj pyplate files
S_PP_PRV = "pyplate/conf/private.json"
S_PP_PRJ = "pyplate/conf/project.json"

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class PyBaker:
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class implements all the needed functionality of PyBaker, to create a
    distribution of a project from a settings file.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initialize the new object

        Initializes a new instance of the class, setting the default values
        of its properties, and any other code that needs to run to create a
        new object.
        """

        # set the initial values of properties
        self._d_args = {}
        self._debug = False
        self._dict_rep = {}
        self._dir_prj = Path()
        self._version = ""
        self._d_blacklist = {}  # project.json
        self._d_i18n = {}  # project.json
        self._d_metadata = {}  # project.json
        self._d_settings = {}  # private.json
        self._error_count = 0

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main method of the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        The main method of the program

        This method is the main entry point for the program, initializing the
        program, and performing its steps.
        """

        # ----------------------------------------------------------------------
        #  do the work

        # call boilerplate code
        self._setup()

        # load the config files
        if not self._debug:
            self.load_config_files()

        # ask for version number
        # self._get_version()

        # replace all dunders ala pymaker
        # self._fix_version()
        # self._fix_toml()

        # self._fix_src()
        # self.fix_metadata()
        # fix_blacklist()
        # fix_readme()

        # # pkg
        # fix_pyproject()
        # # fix_init()

        # # cli/gui
        # fix_argparse()
        # fix_install()

        # # gui
        # fix_desktop()
        # fix_gtk3()

        # # check for dunders left over or we missed
        # recurse_and_check(_DIR_PRJ)

        # # do housekeeping
        # do_extras()

        # # do gettext stuff
        # # do_gettext()

        # # # print error count (dunder stuff found)
        # s = G_STRINGS["S_ERR_COUNT"]
        # print(s.format(G_ERROR_COUNT))

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # NB: these are the main steps, called in order from main

    # --------------------------------------------------------------------------
    # Boilerplate to use at the start of main
    # --------------------------------------------------------------------------
    def _setup(self):
        """
        Boilerplate to use at the start of main

        Perform some mundane stuff like running the arg parser and loading
        config files.
        """

        # ----------------------------------------------------------------------
        # set pp cmd line stuff

        # get cmd line args
        dict_args = self._run_parser()

        # check for flags
        self._debug = dict_args[S_DBG_DEST]

        # # check for folder
        # if not self._debug:
        #     self._dir_prj = Path(dict_args[S_PRJ_DEST])

    # # --------------------------------------------------------------------------
    # # Load the required config files
    # # --------------------------------------------------------------------------
    # def load_config_files(self):
    #     """Y
    #     Load the required config files

    #     Get required config files and load them into the dictionaries required
    #     by the program. These files may sometimes be edited by users, so we
    #     need to check that they:
    #     (1. exist)
    #     and
    #     (2. are valid JSON).
    #     Both of these are handled by F.load_dicts.
    #     """

    #     # TODO use dunders here
    #     # get individual dicts in the project file
    #     path_to_conf = self._dir_prj / "pyplate" / "conf" / "project.json"
    #     dict_all = F.load_dicts([path_to_conf], {})
    #     self._d_blacklist = dict_all["BLACKLIST"]
    #     self._d_i18n = dict_all["I18N"]
    #     self._d_metadata = dict_all["META"]

    #     # get main dict in private.json
    #     path_to_conf = self._dir_prj / "pyplate" / "conf" / "private.json"
    #     self._d_settings = F.load_dicts([path_to_conf], {})

    # # --------------------------------------------------------------------------
    # # Get new version number
    # # --------------------------------------------------------------------------
    # def _get_version(self):
    #     """
    #     Get new version number

    #     Asks the user for the version number of this distribution.
    #     """

    #     # NEXT: enforce semantic versioning (_check_version)
    #     # first get old version from metadata
    #     # NB: if no version key, use default of "0.0.1"
    #     old_version = self._d_metadata.get("__PP_VERSION__", "")
    #     if old_version == "":
    #         old_version = "0.0.0"

    #     # now ask user for new number or default
    #     fmt_str = B.S_ASK_VER.format(old_version)
    #     new_version = input(fmt_str)
    #     if new_version == "":
    #         new_version = old_version

    #     # save new version to metadata
    #     self._d_metadata["__PP_VERSION__"] = new_version
    #     self._version = new_version
    #     # TODO: save new version to file

    # def fix_metadata(self):
    #     """docstring"""

    # --------------------------------------------------------------------------
    # NB: these are minor steps called from the main steps

    # --------------------------------------------------------------------------
    # Set up and run the command line parser
    # --------------------------------------------------------------------------
    def _run_parser(self):
        """
        Set up and run the command line parser

        Returns: A dictionary of command line arguments

        This method sets up and runs the command line parser to minimize code
        in the main method.
        """

        # create the command line parser
        parser = argparse.ArgumentParser(formatter_class=CNFormatter)

        # add args
        self._add_args(parser)

        # get namespace object
        args = parser.parse_args()

        # convert namespace to dict
        self._d_args = vars(args)

        return self._d_args

    # --------------------------------------------------------------------------
    # Add arguments to argparse parser
    # --------------------------------------------------------------------------
    def _add_args(self, parser):
        """
        Add arguments to argparse parser

        Arguments:
            parser: The parser for which to add arguments

        This method is teased out for better code maintenance.
        """

        # set help string
        parser.description = S_PP_ABOUT

        # add debug option
        parser.add_argument(
            S_DBG_OPTION,
            action=S_DBG_ACTION,
            dest=S_DBG_DEST,
            help=S_DBG_HELP,
        )

        # add project dir
        parser.add_argument(
            S_PRJ_OPTION,
            metavar=S_PRJ_METAVAR,
            dest=S_PRJ_DEST,
            help=S_PRJ_HELP,
        )

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main method
    pb = PyBaker()
    pb.main()

# # ------------------------------------------------------------------------------
# # Public functions
# # ------------------------------------------------------------------------------

# # --------------------------------------------------------------------------
# # Replace text in the pyproject file
# # --------------------------------------------------------------------------
# def _fix_readme(self, item):
#     """
#     Replace text in the README file

#     Replace short description, dependencies, and version number in the
#     README file.
#     """

#     # check if the file exists
#     # path_readme = self._dir_prj / "README.md"
#     # if not path_readme.exists():
#     #     return

#     # default text if we can't open file
#     text = ""

#     # open file and get contents
#     with open(item, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # # replace short description
#     # str_pattern = (
#     #     r"(<!--[\t ]*__RM_SHORT_DESC_START__[\t ]*-->)"
#     #     r"(.*?)"
#     #     r"(<!--[\t ]*__RM_SHORT_DESC_END__[\t ]*-->)"
#     # )

#     # # replace short_desc
#     # pp_short_desc = self._d_metadata["__PP_SHORT_DESC__"]

#     # # replace text
#     # str_rep = rf"\g<1>\n{pp_short_desc}\n\g<3>"
#     # text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # # replace dependencies array
#     # str_pattern = (
#     #     r"(<!--[\t ]*__RM_PY_DEPS_START__[\t ]*-->)"
#     #     r"(.*?)"
#     #     r"(<!--[\t ]*__RM_PY_DEPS_END__[\t ]*-->)"
#     # )

#     # # build a string from the dict (markdown links)
#     # # only format links if value is not empty
#     # pp_py_deps = self._d_metadata["__PP_PY_DEPS__"]
#     # kv_py_deps = []
#     # for key, val in pp_py_deps.items():
#     #     if val == "":
#     #         kv_py_deps.append(key)
#     #     else:
#     #         kv_py_deps.append(f"[{key}]({val})")

#     # # build a string (or none) for the deps
#     # if len(kv_py_deps) == 0:
#     #     str_py_deps = "None"
#     # else:
#     #     str_py_deps = "<br>\n".join(kv_py_deps)

#     # # replace text
#     # str_rep = rf"\g<1>\n{str_py_deps}\n\g<3>"
#     # text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace version
#     pp_version = self._d_metadata["__PP_VERSION__"]

#     str_pattern = (
#         r"(\s*foo@bar:~/Downloads\$ python -m pip install )"
#         r"(.*-)"
#         r"(.*?)"
#         r"(\.tar\.gz)"
#     )
#     str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
#     text = re.sub(str_pattern, str_rep, text)

#     str_pattern = (
#         r"(\s*foo@bar:~/Downloads/)"
#         r"(.*?)"
#         r"(\$ python -m pip install ./dist/)"
#         r"(.*-)"
#         r"(.*?)"
#         r"(\.tar\.gz)"
#     )
#     str_rep = rf"\g<1>\g<2>\g<3>\g<4>{pp_version}\g<6>"
#     text = re.sub(str_pattern, str_rep, text)

#     str_pattern = r"(foo@bar:~\$ cd ~/Downloads/)(.*-)(.*)"
#     str_rep = rf"\g<1>\g<2>{pp_version}"
#     text = re.sub(str_pattern, str_rep, text)

#     str_pattern = (
#         r"(\s*foo@bar:~/Downloads/)(.*-)(.*)(\$ \./install.py)"
#     )
#     str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
#     text = re.sub(str_pattern, str_rep, text)

#     # save file
#     with open(item, "w", encoding="UTF8") as a_file:
#         a_file.write(text)

# # --------------------------------------------------------------------------
# #
# # --------------------------------------------------------------------------
# def _fix_version(self):
#     """
#     docstring
#     """

#     self._dict_rep = {
#         "__PP_VERSION__": self._d_metadata["__PP_VERSION__"],
#     }

#     # fix up blacklist and convert relative or glob paths to absolute Path
#     # objects
#     dict_paths = self._d_metadata["BLACKLIST"]

#     # just shorten the names
#     skip_all = dict_paths[M.S_KEY_SKIP_ALL]
#     skip_contents = dict_paths[M.S_KEY_SKIP_CONTENTS]
#     skip_header = dict_paths[M.S_KEY_SKIP_HEADER]
#     skip_code = dict_paths[M.S_KEY_SKIP_CODE]
#     # skip_path = dict_paths[M.S_KEY_SKIP_PATH]

#     # ----------------------------------------------------------------------
#     # do the fixes bottom up
#     # NB: topdown=False is required for the renaming, as we don't want to
#     # rename (and thus clobber) a directory name before we rename all its
#     # child dirs/files
#     # note that root is a full path, dirs and files are relative to root
#     for root, root_dirs, root_files in os.walk(
#         self._dir_prj, topdown=False
#     ):

#         # convert root into Path object
#         root = Path(root)

#         # skip dir if in skip_all
#         if root in skip_all:
#             root_dirs.clear()
#             continue

#         # convert files into Paths
#         files = [root / f for f in root_files]

#         # for each file item
#         for item in files:

#             # skip file if in skip_all
#             if item in skip_all:
#                 continue

#             # fix README if it is the top-level README.md
#             # NB: need to do before any other stuff, requires special
#             # treatment
#             # if (
#             #     item
#             #     == self._dir_prj / self._d_settings["__PP_README_FILE__"]
#             # ):
#             #     self._fix_readme(item)

#             # if we shouldn't skip contents
#             if root not in skip_contents and item not in skip_contents:

#                 # check for header bl
#                 bl_hdr = True
#                 if root not in skip_header and item not in skip_header:
#                     bl_hdr = False

#                 # check for code blacklist
#                 bl_code = True
#                 if root not in skip_code and item not in skip_code:
#                     bl_code = False

#                 # fix text
#                 self._fix_content(item, bl_hdr, bl_code)

#         #     # fix path
#         #     if root not in skip_path and item not in skip_path:
#         #         self._fix_path(item)

#         # # fix current dir path
#         # if root not in skip_path:
#         #     self._fix_path(root)

# # ------------------------------------------------------------------------------
# # Replace text in the pyproject file
# # ------------------------------------------------------------------------------
# def fix_pyproject():
#     """
#     Replace text in the pyproject file

#     Replaces things like the keywords, requirements, etc. in the toml file.
#     """

#     # check if the file exists
#     path_toml = _DIR_PRJ / "pyproject.toml"
#     if not path_toml.exists():
#         return

#     # default text if we can't open file
#     text = ""

#     # open file and get contents
#     with open(path_toml, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # NB: we do a dunder replace here because putting a dunder as the
#     # default name in the toml file causes the linter to choke, so we use a
#     # dummy name

#     # replace name
#     str_pattern = (
#         r"(^\s*\[project\]\s*$)" r"(.*?)" r"(^\s*name[\t ]*=[\t ]*)" r"(.*?$)"
#     )
#     pp_name_small = DICT_SETTINGS["info"]["__PP_NAME_SMALL__"]
#     str_rep = rf'\g<1>\g<2>\g<3>"{pp_name_small}"'
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace version
#     str_pattern = (
#         r"(^\s*\[project\]\s*$)"
#         r"(.*?)"
#         r"(^\s*version[\t ]*=[\t ]*)"
#         r"(.*?$)"
#     )
#     pp_version = DICT_METADATA["__PP_VERSION__"]
#     if pp_version == "":
#         pp_version = S.DEF_VERSION
#     str_rep = rf'\g<1>\g<2>\g<3>"{pp_version}"'
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace short description
#     str_pattern = (
#         r"(^\s*\[project\]\s*$)"
#         r"(.*?)"
#         r"(^\s*description[\t ]*=[\t ]*)"
#         r"(.*?$)"
#     )
#     pp_short_desc = DICT_METADATA["__PP_SHORT_DESC__"]
#     str_rep = rf'\g<1>\g<2>\g<3>"{pp_short_desc}"'
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # # replace keywords array
#     str_pattern = (
#         r"(^\s*\[project\]\s*$)"
#         r"(.*?)"
#         r"(^\s*keywords[\t ]*=[\t ]*)"
#         r"(.*?\])"
#     )

#     # convert dict to string
#     pp_keywords = DICT_METADATA["__PP_KEYWORDS__"]
#     str_pp_keywords = [f'"{item}"' for item in pp_keywords]
#     str_pp_keywords = ", ".join(str_pp_keywords)

#     # replace string
#     str_rep = rf"\g<1>\g<2>\g<3>[{str_pp_keywords}]"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace dependencies array
#     str_pattern = (
#         r"(^\s*\[project\]\s*$)"
#         r"(.*?)"
#         r"(^\s*dependencies[\t ]*=[\t ]*)"
#         r"(.*?\])"
#     )

#     # convert dict to string (only using keys)
#     pp_py_deps = DICT_METADATA["__PP_PY_DEPS__"]

#     # NB: this is not conducive to a dict (we don't need links, only names)
#     # so don't do what we did in README, keep it simple
#     list_py_deps = [item for item in pp_py_deps.keys()]
#     str_pp_py_deps = [f'"{item}"' for item in list_py_deps]
#     str_pp_py_deps = ", ".join(str_pp_py_deps)

#     # replace text
#     str_rep = rf"\g<1>\g<2>\g<3>[{str_pp_py_deps}]"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # save file
#     with open(path_toml, "w", encoding="UTF8") as a_file:
#         a_file.write(text)

# # ------------------------------------------------------------------------------
# # Replace text in the install file
# # ------------------------------------------------------------------------------
# def fix_install():
#     """
#     Replace text in the install file

#     Replaces the system and Python dependencies in the install file.
#     """

#     # check if the file exists
#     path_install = _DIR_PRJ / "install.py"
#     if not path_install.exists():
#         return

#     # default text if we can't open file
#     text = ""

#     # open file and get content
#     with open(path_install, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # replace python dependencies array
#     str_pattern = (
#         r"(^\s*dict_install[\t ]*=\s*{)"
#         r"(.*?)"
#         r"(^\s*\'py_deps\'[\t ]*:)"
#         r"(.*?\])"
#     )

#     # convert dict keys to string
#     pp_py_deps = DICT_METADATA["__PP_PY_DEPS__"]
#     str_pp_py_deps = ",".join(pp_py_deps.keys())

#     # replace text
#     str_rep = rf"\g<1>\g<2>\g<3> [\n\t\t{str_pp_py_deps}\n\t]"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace system dependencies array
#     str_pattern = (
#         r"(^\s*dict_install[\t ]*=)"
#         r"(.*?)"
#         r"(^\s*\'sys_deps\'[\t ]*:)"
#         r"(.*?\])"
#     )

#     # convert dict to string
#     pp_sys_deps = DICT_METADATA["__PP_SYS_DEPS__"]
#     str_pp_sys_deps = ",".join(pp_sys_deps)

#     # replace string
#     str_rep = rf"\g<1>\g<2>\g<3> [\n\t\t{str_pp_sys_deps}\n\t]"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # save file
#     with open(path_install, "w", encoding="UTF8") as a_file:
#         a_file.write(text)


# # ------------------------------------------------------------------------------
# # Replace text in the desktop file
# # ------------------------------------------------------------------------------
# def fix_desktop():
#     """
#     Replace text in the desktop file

#     Replaces the desc, exec, icon, path, and category text in a .desktop
#     file for programs that use this.
#     """

#     # global error count
#     global G_ERROR_COUNT

#     # check if the file exists
#     pp_name_small = DICT_SETTINGS["info"]["__PP_NAME_SMALL__"]
#     path_desk = os.path.join(_DIR_PRJ, "src", f"{pp_name_small}.desktop")
#     if not os.path.exists(path_desk):
#         return

#     # validate wanted categories into approved categories
#     pp_gui_categories = []
#     wanted_cats = DICT_METADATA["__PP_GUI_CATS__"]
#     for cat in wanted_cats:
#         # category is valid
#         if cat in LIST_CATEGORIES:
#             # add to final list
#             pp_gui_categories.append(cat)
#         else:
#             # category is not valid, print error and increase error count
#             print(
#                 f'In PP_GUI_CATEGORIES, "{cat}" is not valid, see \n'
#                 "https://specifications.freedesktop.org/menu-spec/latest/apa.html"
#             )
#             G_ERROR_COUNT += 1

#     # default text if we can't open file
#     text = ""

#     # open file and get contents
#     with open(path_desk, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # replace categories
#     str_pattern = (
#         r"(^\s*\[Desktop Entry\]\s*$)"
#         r"(.*?)"
#         r"(^\s*Categories[\t ]*=)"
#         r"(.*?$)"
#     )

#     # convert dict to string
#     str_cat = ";".join(pp_gui_categories)
#     str_cat += ";"

#     # replace text
#     str_rep = rf"\g<1>\g<2>\g<3>{str_cat}"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace short description
#     str_pattern = (
#         r"(^\s*\[Desktop Entry\]\s*$)"
#         r"(.*?)"
#         r"(^\s*Comment[\t ]*=)"
#         r"(.*?$)"
#     )
#     pp_short_desc = DICT_METADATA["__PP_SHORT_DESC__"]
#     str_rep = rf"\g<1>\g<2>\g<3>{pp_short_desc}"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # get path to install dir
#     path_home = os.path.expanduser("~")
#     author = DICT_SETTINGS["info"]["__PP_AUTHOR__"]
#     pp_name_big = DICT_SETTINGS["info"]["__PP_NAME_BIG__"]
#     path_inst = os.path.join(path_home, f".{author}", pp_name_big, "src")

#     # replace exec
#     str_pattern = (
#         r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Exec[\t ]*=)" r"(.*?$)"
#     )
#     path_exec = os.path.join(path_inst, f"{pp_name_small}.py")
#     str_rep = rf"\g<1>\g<2>\g<3>{path_exec}"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace icon
#     str_pattern = (
#         r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Icon[\t ]*=)" r"(.*?$)"
#     )
#     path_icon = os.path.join(path_inst, f"{pp_name_small}.png")
#     str_rep = rf"\g<1>\g<2>\g<3>{path_icon}"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace path
#     str_pattern = (
#         r"(^\s*\[Desktop Entry\]\s*$)" r"(.*?)" r"(^\s*Path[\t ]*=)" r"(.*?$)"
#     )
#     str_rep = rf"\g<1>\g<2>\g<3>{path_inst}"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # save file
#     with open(path_desk, "w", encoding="UTF8") as a_file:
#         a_file.write(text)


# # ------------------------------------------------------------------------------
# # Replace text in the UI file
# # ------------------------------------------------------------------------------
# def fix_gtk3():
#     """
#     Replace text in the UI file

#     Replace description and version number in the UI file.
#     """

#     # check if there is a .ui file
#     pp_name_small = DICT_SETTINGS["info"]["__PP_NAME_SMALL__"]
#     path_ui = os.path.join(_DIR_PRJ, "src", f"{pp_name_small}_gtk3.ui")
#     if not os.path.exists(path_ui):
#         return

#     # default text if we can't open file
#     text = ""

#     # open file and get contents
#     with open(path_ui, "r", encoding="UTF8") as a_file:
#         text = a_file.read()

#     # replace short description
#     str_pattern = (
#         r"(<object class=\"GtkAboutDialog\".*?)"
#         r"(<property name=\"comments\".*?\>)"
#         r"(.*?)"
#         r"(</property>)"
#     )
#     pp_short_desc = DICT_METADATA["__PP_SHORT_DESC__"]
#     str_rep = rf"\g<1>\g<2>{pp_short_desc}\g<4>"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # replace version
#     str_pattern = (
#         r"(<object class=\"GtkAboutDialog\".*?)"
#         r"(<property name=\"version\">)"
#         r"(.*?)"
#         r"(</property>.*)"
#     )
#     pp_version = DICT_METADATA["__PP_VERSION__"]
#     str_rep = rf"\g<1>\g<2>{pp_version}\g<4>"
#     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

#     # save file
#     with open(path_ui, "w", encoding="UTF8") as a_file:
#         a_file.write(text)


# # ------------------------------------------------------------------------------
# # Recurse through the folder structure looking for errors
# # ------------------------------------------------------------------------------
# def recurse_and_check(path):
#     """
#     Recurses through the folder structure looking for errors

#     Arguments:
#         dir: The directory to start looking for errors

#     This function recurses through the project directory, checking for
#     errors in each file's headers, and content for strings that do not match
#     their intended contents. It checks a header's project, filename, and
#     date values as well as looking for dunder values that should have been
#     replaced.
#     """

#     # blacklist
#     # don't check everything/contents/headers/text/path names for these items
#     # strip trailing slashes to match path component
#     skip_all = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_all"]]
#     skip_file = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_file"]]
#     skip_header = [
#         item.strip(os.sep) for item in DICT_BLACKLIST["skip_header"]
#     ]
#     skip_text = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_text"]]
#     skip_path = [item.strip(os.sep) for item in DICT_BLACKLIST["skip_path"]]

#     # get list of replaceable file names
#     items = [item for item in os.listdir(path) if item not in skip_all]
#     for item in items:
#         # put path back together
#         path_item = os.path.join(path, item)

#         # if it's a dir
#         if os.path.isdir(path_item):
#             # recurse itself to find more files
#             recurse_and_check(path_item)

#         else:
#             # only open files we should be mucking in
#             if item not in skip_file:
#                 # default lines if we can't open file
#                 lines = []

#                 # open file and get lines
#                 with open(path_item, "r", encoding="UTF8") as a_file:
#                     lines = a_file.readlines()

#                 # check headers of most files
#                 if item not in skip_header:
#                     _check_header(path_item, lines)

#                 # check contents of most files
#                 if item not in skip_text:
#                     _check_text(path_item, lines)

#         # check file paths (subdirs and such)
#         if item not in skip_path:
#             _check_path(path_item)


# # ------------------------------------------------------------------------------
# # Do extra functions to update project dir after recurse
# # ------------------------------------------------------------------------------
# def do_extras():
#     """
#     Do extras functions to update project dir after recurse

#     Do some extra functions like add requirements, update docs, and update
#     the CHANGELOG file for the current project.
#     """

#     # get current dir
#     dir_curr = os.getcwd()

#     # make sure we are in project path
#     os.chdir(_DIR_PRJ)

#     # add requirements
#     path_req = os.path.join(_DIR_PRJ, "requirements.txt")
#     with open(path_req, "w", encoding="UTF8") as a_file:
#         cmd = "python -m pip freeze -l --exclude-editable --require-virtualenv"
#         cmd_array = shlex.split(cmd)
#         subprocess.run(cmd_array, stdout=a_file, check=False)

#     # update CHANGELOG
#     path_chg = os.path.join(_DIR_PRJ, "CHANGELOG.md")
#     with open(path_chg, "w", encoding="UTF8") as a_file:
#         cmd = 'git log --pretty="%ad - %s"'
#         cmd_array = shlex.split(cmd)
#         subprocess.run(cmd_array, stdout=a_file, check=False)

#     # get tree path
#     path_tree = os.path.join(_DIR_PRJ, "misc", "tree.txt")

#     # if not exist
#     # if not os.path.exists(path_tree):

#     # # create tree object and call
#     # p_t = pytree.PyTree()
#     # TODO: make this use blacklist
#     # tree = p_t.build_tree(_DIR_PRJ, DICT_SETTINGS['__PP_TREE_IGNORE__'])

#     # # write tree to file
#     # with open(path_tree, 'w', encoding='UTF8') as a_file:
#     #     a_file.write(tree)

#     # update docs
#     # NB: this is ugly and stupid, but it's the only way to get pdoc3 to work

#     # move into src dir
#     # dir_src = os.path.join(_DIR_PRJ, 'src')
#     # os.chdir(dir_src)

#     # # get docs dir
#     # path_docs = os.path.join('..', 'docs')
#     # path_docs = os.path.abspath(path_docs)

#     # # # update docs
#     # cmd = f'python -m pdoc --html -f -o {path_docs} .'
#     # cmd_array = shlex.split(cmd)
#     # subprocess.run(cmd_array, check=False)

#     # # go back to old dir
#     # os.chdir(dir_curr)


# # ------------------------------------------------------------------------------
# # Run xgettext over files to produce a locale template
# # ------------------------------------------------------------------------------
# # def do_gettext():
# #     """
# #     Run xgettext over files to produce a locale template

# #     Use xgettext to scan .py and .ui files for I18N strings and collect them
# #     int a .pot file in the locale folder. Only applies to gui projects at
# #     the moment.
# #     """

# #     # check if we are a gui project
# #     is_gui = DICT_SETTINGS["project"]["type"] == "g"
# #     if not is_gui:
# #         return

# #     # get locale folder and pot filename
# #     dir_locale = os.path.join(_DIR_PRJ, "src", "locale")
# #     pp_name_small = DICT_SETTINGS["info"]["__PP_NAME_SMALL__"]
# #     path_pot = os.path.join(dir_locale, f"{pp_name_small}.pot")
# #     pp_version = DICT_METADATA["__PP_VERSION__"]

# #     # remove old pot and recreate empty file
# #     if os.path.exists(path_pot):
# #         os.remove(path_pot)
# #     with open(path_pot, "w", encoding="UTF8") as a_file:
# #         a_file.write("")

# #     # build a list of files
# #     res = []
# #     exts = [".py", ".ui", ".glade"]

# #     # scan for files in src directory
# #     dir_src = os.path.join(_DIR_PRJ, "src")
# #     list_files = os.listdir(dir_src)

# #     # for each file in dir
# #     for file in list_files:
# #         # check for ext
# #         for ext in exts:
# #             if file.endswith(ext):
# #                 # rebuild complete path and add to list
# #                 path = os.path.join(dir_src, file)
# #                 res.append(path)

# #     # for each file that can be I18N'd, run xgettext
# #     author = DICT_SETTINGS["info"]["__PP_AUTHOR__"]
# #     email = DICT_SETTINGS["info"]["__PP_EMAIL__"]
# #     for file in res:
# #         cmd = (
# #             "xgettext "  # the xgettext cmd
# #             f"{file} "  # the file name
# #             "-j "  # append to current file
# #             '-c"I18N:" '  # look for tags in .py files
# #             "--no-location "  # don't print filename/line number
# #             f"-o {path_pot} "  # location of output file
# #             "-F "  # sort output by input file
# #             f"--copyright-holder={author} "
# #             f"--package-name={pp_name_small} "
# #             f"--package-version={pp_version} "
# #             f"--msgid-bugs-address={email}"
# #         )
# #         cmd_array = shlex.split(cmd)
# #         subprocess.run(cmd_array, check=False)

# #     # now lets do some text replacements to make it look nice

# #     # default text if we can't open file
# #     text = ""

# #     # open file and get contents
# #     with open(path_pot, "r", encoding="UTF8") as a_file:
# #         text = a_file.read()

# #     # replace short description
# #     str_pattern = r"(# SOME DESCRIPTIVE TITLE.)"
# #     pp_name_big = DICT_SETTINGS["info"]["__PP_NAME_BIG__"]
# #     str_rep = f"# {pp_name_big} translation template"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # replace copyright
# #     author = DICT_SETTINGS["info"]["__PP_AUTHOR__"]
# #     str_pattern = r"(# Copyright \(C\) )" r"(.*?)" rf"( {author})"
# #     year = date.today().year
# #     str_rep = rf"\g<1>{year}\g<3>"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # replace author's email
# #     str_pattern = r"(# FIRST AUTHOR )" r"(<EMAIL@ADDRESS>)" r"(, )" r"(YEAR)"
# #     email = DICT_SETTINGS["info"]["__PP_EMAIL__"]
# #     year = date.today().year
# #     str_rep = rf"\g<1>{email}\g<3>{year}"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # replace charset
# #     str_pattern = (
# #         r'("Content-Type: text/plain; charset=)' r"(CHARSET)" r'(\\n")'
# #     )
# #     charset = "UTF-8"
# #     str_rep = rf"\g<1>{charset}\g<3>"
# #     text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

# #     # save file
# #     with open(path_pot, "w", encoding="UTF8") as a_file:
# #         a_file.write(text)


# # ------------------------------------------------------------------------------
# # Private functions
# # ------------------------------------------------------------------------------


# # ------------------------------------------------------------------------------
# # Opens the user or default config file, whichever is found first
# # ------------------------------------------------------------------------------
# def _load_user_or_default(a_dict, a_user, a_default):
#     """
#     Opens the user or default config file, whichever is found first

#     Arguments:
#         a_dict: Dictionary to load JSON file into
#         a_user: User Path to load dict from
#         a_default: Path to default file if user file is not found

#     Raises:
#         Exception: if neither file can be found or if both files are invalid
#         JSON

#     This is a convenience function to load a JSON file into a dict. If the user
#     file is not found, it tries to load the default file. If neither file is
#     found or they are both invalid JSON files, an Exception is raised.
#     """

#     # check if user file exists
#     if a_user.exists():

#         # try to load user file
#         try:
#             a_dict = json.load(a_user)
#             return

#         # we can't load it
#         except json.JSONDecodeError:
#             print(G_STRINGS["S_ERR_UJSON"].format(a_user))

#     # we can't find it
#     else:
#         print(G_STRINGS["S_ERR_UFNF"].format(a_user))

#     # check if default file exists
#     if a_default.exists():

#         # try to load default file
#         try:
#             a_dict = json.load(a_default)

#             # save default as user
#             with open(a_user, "w", encoding="UTF-8") as f:
#                 f.write(a_dict)

#             # done
#             return

#         # we can't load it
#         except json.JSONDecodeError:
#             print(G_STRINGS["S_ERR_DJSON"].format(a_default))

#     # we can't find it
#     else:
#         print(G_STRINGS["S_ERR_DFNF"].format(a_default))

#     # we can't find it or load it
#     raise Exception


# # ------------------------------------------------------------------------------
# # Checks header values for dunders
# # ------------------------------------------------------------------------------
# def _check_header(path_item, lines):
#     """
#     Checks header values for dunders

#     Arguments:
#         path_item: The full path to file to be checked for header
#         lines: The contents of the file to be checked

#     This function checks the files headers for values that either do not
#     match the file's project/file name, or do not have a date set.
#     This method is private because it is only called from inside
#     recurse_and_check().
#     """

#     # global error count
#     global G_ERROR_COUNT

#     # for each line in file
#     for i, line in enumerate(lines):
#         # check project name
#         prj_name = os.path.basename(_DIR_PRJ)
#         str_pattern = (
#             r"(^\s*(<!--|#)\s*)" r"(Project)" r"(\s*:\s*)" r"(.*?)" r"(\s)"
#         )
#         str_res = re.search(str_pattern, line, flags=re.M | re.S)
#         if str_res and str_res.group(5) != prj_name:
#             print(
#                 f"{path_item}:{i + 1}: Header Project name should be "
#                 f"'{prj_name}'"
#             )

#             # inc error count
#             G_ERROR_COUNT += 1

#         # check file name
#         file_name = os.path.basename(path_item)
#         str_pattern = (
#             r"(^\s*(<!--|#)\s*)" r"(Filename)" r"(\s*:\s*)" r"(.*?)" r"(\s)"
#         )
#         str_res = re.search(str_pattern, line, flags=re.M | re.S)
#         if str_res and str_res.group(5) != file_name:
#             print(
#                 f"{path_item}:{i + 1}: Header Filename should be "
#                 f"'{file_name}'"
#             )

#             # inc error count
#             G_ERROR_COUNT += 1

#         # check date
#         str_pattern = (
#             r"(^\s*(<!--|#)\s*)" r"(Date)" r"(\s*:\s*)" r"(.*?)" r"(\s)"
#         )
#         str_res = re.search(str_pattern, line, flags=re.M | re.S)
#         if str_res:
#             # there is *something* in the date field
#             if str_res.group(5) != "":
#                 # check for valid date
#                 str_pattern2 = r"\d*/\d*/\d*"
#                 str_res2 = re.search(str_pattern2, str_res.group(5))
#                 if not str_res2:
#                     print(f"{path_item}:{i + 1}: Header Date is not set")

#                     # inc error count
#                     G_ERROR_COUNT += 1

#             else:
#                 print(f"{path_item}:{i + 1}: Header Date is not set")

#                 # inc error count
#                 G_ERROR_COUNT += 1


# # ------------------------------------------------------------------------------
# # Checks file contents for replacements
# # ------------------------------------------------------------------------------
# def _check_text(path_item, lines):
#     """
#     Checks file contents for replacements

#     Arguments:
#         path_item: The full path to file to be checked for text
#         lines: The contents of the file to be checked

#     This function checks that none of the files contains an unreplaced
#     replacement variable from the initial project info.
#     This method is private because it is only called from inside
#     recurse_and_check().
#     """

#     # global error count
#     global G_ERROR_COUNT

#     # for each line in file
#     for i, line in enumerate(lines):
#         # the dunders to look for
#         reps = [rep for rep in DICT_SETTINGS["info"] and DICT_METADATA]

#         # check for dunders in text
#         for rep in reps:
#             if rep in line:
#                 print(f"{path_item}:{i + 1}: Text contains {rep}")

#                 # inc error count
#                 G_ERROR_COUNT += 1


# # ------------------------------------------------------------------------------
# # Checks file paths for dunders
# # ------------------------------------------------------------------------------
# def _check_path(path_item):
#     """
#     Checks file paths for dunders

#     Arguments:
#         path_item: The full path to file to be checked for path

#     This function checks that none of the files paths contains an unreplaced
#     dunder variable from the initial project info.
#     This method is private because it is only called from inside
#     recurse_and_check().
#     """

#     # global error count
#     global G_ERROR_COUNT

#     # TODO make this use __PP, __PP, __PP
#     # check for dunders in path
#     if "__PP_" in path_item:
#         print(f"{path_item}: Path contains __PP_")

#         # inc error count
#         G_ERROR_COUNT += 1


# # ------------------------------------------------------------------------------
# # Code to run when called from command line
# # ------------------------------------------------------------------------------
# if __name__ == "__main__":
#     # Code to run when called from command line

#     # This is the top level code of the program, called when the Python file
#     # is invoked from the command line.

#     # run main function
#     main()

# # def do_pot():
# #     """docstring"""

# #     # # dict of clangs and exts
# #     dict_in = {
# #         "Python": [
# #             "py",
# #         ],
# #         "Glade": [
# #             ".ui",
# #             ".glade",
# #         ],
# #         "Desktop": [".desktop"],
# #     }

# #     # dict of clangs and no exts (ie file names)
# #     dict_blank = {
# #         "Python": [
# #             "__PP_NAME_SMALL__",
# #         ],
# #     }

# #     # the list of languages your program has been translated into (can grow
# #     # over time, adding languages as they become available)
# #     list_wlang = [
# #         "es",
# #         "xo",
# #         "pq",
# #     ]

# #     # path to src dir
# #     dir_src = Path(__file__).parent.resolve()

# #     pp = CNPotPy(
# #         dir_src,
# #         str_appname="foo",
# #         str_version="0",
# #         str_email="foo@bar.com",
# #         str_domain=f"{C_DOMAIN}",
# #         dict_clangs=dict_in,
# #         dict_no_ext=dict_blank,
# #         list_wlangs=list_wlang,
# #     )

# #     # I18N: run cnpotpy
# #     pp.make_pot()
# #     pp.make_pos()
# #     pp.make_mos()
# #     pp.make_desktop(
# #         C_GUI_DIR / "template.desktop",
# #         C_GUI_DIR / "__PP_NAME_SMALL__.desktop",
# #     )

# #     # TODO: this is for testing purposes only
# #     t = gettext.translation(
# #         C.DOMAIN, localedir=C.POT_DEF_DIR_LOCALE, languages=["es"]
# #     )
# #     t.install()
# #     _ = t.gettext

# #     # get path to config file
# #     C_PATH_GUI = C_PATH_SRC / "cfg/__PP_NAME_SMALL__.json"


# # -)
