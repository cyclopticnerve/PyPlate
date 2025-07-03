#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pybaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pyplate: replace=False

"""
A program to change the metadata of a PyPlate project and create a dist

This module sets the project metadata in each of the files, according to the
data present in the conf files. It then sets up the dist folder with all
necessary files to create a complete distribution of the project.

Run pybaker -h for more options.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import locale
from pathlib import Path
import shutil
import sys

# local imports
import cnlib.cnfunctions as F
from pyplate import PyPlate

# ------------------------------------------------------------------------------
# local imports

# pylint: disable=wrong-import-position

# fudge the path to import conf stuff
P_DIR_PRJ = Path(__file__).parents[1].resolve()
sys.path.append(str(P_DIR_PRJ))

import conf.conf as C

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./pybaker.py

# path to project dir
T_DIR_PRJ = Path(__file__).parents[1].resolve()

# init gettext
T_DOMAIN = "pyplate"
T_DIR_LOCALE = T_DIR_PRJ / "i18n/locale"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class PyBaker(PyPlate):
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class implements all the needed functionality of PyBaker, to create a
    distribution from a PyPlate project.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # # pyplate: replace=True

    # I18N: short description
    S_PP_SHORT_DESC = _(
        "A program for building CLI/Gui/Package projects in Python from a "
        "template"
    )

    # version string
    S_PP_VERSION = "Version 0.0.1+20250507.9"

    # pyplate: replace=False

    # ide option strings
    S_ARG_IDE_OPTION = "-i"
    S_ARG_IDE_ACTION = "store_true"
    S_ARG_IDE_DEST = "IDE_DEST"
    # I18N help string for ide cmd line option
    S_ARG_IDE_HELP = _("ask for project folder when running in IDE")

    # about string
    S_ABOUT = (
        "\n"
        f"{'PyPlate/PyBaker'}\n"
        f"{S_PP_SHORT_DESC}\n"
        f"{S_PP_VERSION}\n"
        f"https://github.com/cyclopticnerve/PyPlate\n"
    )

    # I18N cmd line instructions string
    S_EPILOG = _(
        "Run this program from the parent directory of the project you want "
        "to build."
    )

    # --------------------------------------------------------------------------
    # Instance methods
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

        # do super init
        super().__init__()

        # set the initial values of properties
        self._ide = False

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

        # do super main
        super().main()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_fix()

        # do replacements in final project location
        self._do_fix()

        # do extra stuff to final dir after fix
        self._do_after_fix()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_dist()

        # copy project files into dist folder
        self._do_dist()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_after_dist()

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

        Perform some mundane stuff like setting properties.
        """

        # do setup
        super()._setup()

        # add ide option
        self._parser.add_argument(
            self.S_ARG_IDE_OPTION,
            dest=self.S_ARG_IDE_DEST,
            help=self.S_ARG_IDE_HELP,
            action=self.S_ARG_IDE_ACTION,
        )

        # parse command line
        self._do_cmd_line()
        if self._debug:
            self._dict_debug = C.D_DBG_PB

        # get ide flag from cmd line
        self._ide = self._dict_args.get(self.S_ARG_IDE_DEST, False)

        # if ide=yes, ask for prj name
        if self._ide:

            # ask for prj name rel to cwd
            in_str = C.S_ASK_IDE.format(self._dir_prj)
            while True:
                prj_name = input(in_str)
                if prj_name == "":
                    continue

                # if running in ide, cwd is pyplate prj dir, so move up and down
                tmp_dir = Path(self._dir_prj / prj_name).resolve()

                # check if project exists
                if not tmp_dir.exists():
                    e_str = C.S_ERR_NOT_EXIST.format(tmp_dir)
                    print(e_str)
                    continue

                # set project dir and exit loop
                self._dir_prj = tmp_dir
                print()
                break

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Check that the PyPlate data is present and correct, so we don't crash
        looking for non-existent files.
        """

        # check if dir_prj has pyplate folder for a valid prj
        path_pyplate = self._dir_prj / C.S_PRJ_PP_DIR
        if not path_pyplate.exists():
            print(C.S_ERR_NOT_PRJ)
            sys.exit()

        # check if data files exist
        path_prv = self._dir_prj / C.S_PRJ_PRV_CFG
        path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
        if not path_prv.exists() or not path_pub.exists():
            print(C.S_ERR_PP_MISSING)
            sys.exit()

        # check if files are valid json
        try:
            # get global and calculated settings dicts in private.json
            self._dict_prv = F.load_dicts([path_prv], {})

            # get individual dicts in project.json
            self._dict_pub = F.load_dicts([path_pub], {})

            # reload dict pointers after dict change
            self._reload_dicts()
        except OSError:
            print(C.S_ERR_PP_INVALID)
            sys.exit()

    # --------------------------------------------------------------------------
    # Do any work before making dist
    # --------------------------------------------------------------------------
    def _do_before_dist(self):
        """
        Do any work before making dist

        Do any work on the dist folder before it is created. This method is
        called after _do_after_fix, and before _do_dist.
        """

        C.do_before_dist(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_debug
        )

    # --------------------------------------------------------------------------
    # Copy fixed files to final location
    # --------------------------------------------------------------------------
    def _do_dist(self):
        """
        Copy fixed files to final location

        Gets dirs/files from project and copies them to the dist/assets dir.
        """

        # print info
        print(C.S_ACTION_DIST, end="", flush=True)

        # ----------------------------------------------------------------------
        # do common dist stuff

        # find old dist? nuke it from orbit! it's the only way to be sure!
        a_dist = self._dir_prj / C.S_DIR_DIST
        if a_dist.is_dir():
            shutil.rmtree(a_dist)

        # make child dir in case we nuked
        name_fmt = self._dict_prv_prj["__PP_DIST_DIR__"]
        p_dist = a_dist / name_fmt
        p_dist.mkdir(parents=True)

        # for each key, val (type, dict)
        for key, val in self._dict_pub_dist.items():

            # get src/dst rel to prj dir/dist dir
            src = self._dir_prj / key
            dst = p_dist / val
            if not dst.exists():
                dst.mkdir(parents=True)
            dst = dst / src.name

            # do the copy
            if src.exists() and src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif src.exists() and src.is_file():
                shutil.copy2(src, dst)

        # done copying project files
        print(C.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # Do any work after making dist
    # --------------------------------------------------------------------------
    def _do_after_dist(self):
        """
        Do any work after making dist

        Do any work on the dist folder after it is created. This method is
        called after _do_dist. Currently, this method purges any "ABOUT" file
        used as placeholders for github syncing. It also tars the source folder
        if it is a package, making for one (or two) less steps in the user's
        install process.
        """

        C.do_after_dist(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_debug
        )


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create object
    pb = PyBaker()

    # run main method with args
    pb.main()

# -)
