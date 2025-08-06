#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pymaker.py                                            |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# pylint: disable=too-many-lines
# pyplate: replace=False

"""
A program to create a PyPlate project from a few variables

This module gets the project type, the project's destination dir, copies the
required dirs/files for the project type from the template to the specified
destination, and performs some initial fixes/replacements of text and path
names in the resulting files.

Run pymaker -h for more options.
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
from cnlib import cnfunctions as F  # type: ignore
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
class PyMaker(PyPlate):
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main method of the program

    This class implements all the needed functionality of PyMaker, to create a
    PyPlate project from a template.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # about string
    S_ABOUT = (
        "\n"
        f"{'PyPlate/PyMaker'}\n"
        f"{PyPlate.S_PP_SHORT_DESC}\n"
        f"{PyPlate.S_PP_VERSION}\n"
        f"https://github.com/cyclopticnerve/PyPlate\n"
    )

    # I18N cmd line instructions string
    S_EPILOG = _("Run this program from the directory where you want to create \
a project.")

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

        # do before template
        self._do_before_template()

        # copy template
        self._do_template()

        # do before template
        self._do_after_template()

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_fix()

        # do replacements in final project location
        self._do_fix()

        # do extra stuff to final dir after fix
        self._do_after_fix()

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

        # do parent setup
        super()._setup()

        # parse command line
        self._do_cmd_line()
        if self._debug:
            self._dict_debug = C.D_DBG_PM

        # do not run pymaker in pyplate dir
        if self._dir_prj.is_relative_to(self.P_DIR_PP):
            print(C.S_ERR_PRJ_DIR_IS_PP)
            sys.exit()

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        self._dict_prv_prj.
        """

        # ----------------------------------------------------------------------
        # first question is type
        # NB: this makes the string to display in terminal

        # sanity check
        prj_type = ""

        # build the input question
        types = []
        for item in C.L_TYPES:
            s = C.S_ASK_TYPE_FMT.format(item[0], item[1])
            types.append(s)
        str_types = C.S_ASK_TYPE_JOIN.join(types)

        # format the question
        in_type = C.S_ASK_TYPE.format(str_types)

        # loop forever until we get a valid type
        while True:

            # ask for type of project (single letter)
            prj_type = input(in_type)

            # check for valid type
            if self._check_type(prj_type):
                prj_type = prj_type[0].lower()

                # at this point, type is valid so exit loop
                break

        # ----------------------------------------------------------------------
        # next question is name

        # sanity check
        cwd = Path.cwd()

        # if in debug mode
        if self._debug:

            # get long name
            for item in C.L_TYPES:
                if item[0] == prj_type:
                    # get debug name of project
                    name_prj = f"{item[1]} DEBUG"
                    break

            # dir name, no spaces
            name_prj_big = name_prj.replace(" ", "_")

            # set up for existence check
            tmp_dir = cwd / name_prj_big

            # check if project already exists
            if tmp_dir.exists():

                # if it does exist, "nuke it from orbit! it's the only way to
                # be sure!"
                # NB: yes i know ive used this joke more than once... FUCK YOU
                # ITS FUNNY
                shutil.rmtree(tmp_dir)

        # not debug
        else:

            # loop forever until we get a valid name that does not exist
            while True:

                # ask for name of project
                name_prj = input(C.S_ASK_NAME)
                name_prj = name_prj.strip(" ")

                # check for valid name
                if self._check_name(name_prj):

                    # dir name, no spaces
                    name_prj_big = name_prj.replace(" ", "_")

                    # set up for existence check
                    tmp_dir = cwd / name_prj_big

                    # check if project already exists
                    if tmp_dir.exists():

                        # tell the user that the old name exists
                        print(C.S_ERR_EXIST.format(name_prj_big))
                    else:
                        break

        # save global property
        self._dir_prj = tmp_dir

        # save other names
        name_prj_small = name_prj_big.lower()
        name_prj_pascal = F.pascal_case(name_prj_small)

        # ----------------------------------------------------------------------
        # here we figure out the binary/package/window name for a project

        # NB: for a cli, the binary name is the project name lowercased
        # for a gui we should ask for the main window class name
        # for a package we should ask for the module name

        name_sec = ""
        name_sec_big = ""
        name_sec_small = ""
        name_sec_pascal = ""

        # do we need a second name?
        if prj_type in C.D_NAME_SEC:

            # dup prj names if debug
            if self._debug:
                name_sec = name_prj
                name_sec_big = name_prj_big
                name_sec_small = name_prj_small
                name_sec_pascal = name_prj_pascal

            # if not debug, if need second name, ask for it
            else:

                # format question for second name
                s_sec_ask = C.D_NAME_SEC[prj_type]
                s_sec_ask_fmt = s_sec_ask.format(name_prj_small)

                # loop forever until we get a valid name or empty string
                while True:

                    # ask for second name
                    name_sec = input(s_sec_ask_fmt)
                    name_sec = name_sec.strip(" ")

                    # empty, keep default
                    if name_sec == "":
                        name_sec = name_prj_small

                    # check for valid name
                    if self._check_name(name_sec):
                        name_sec_big = name_sec.replace(" ", "_")
                        break

                # save other names
                name_sec_small = name_sec_big.lower()
                name_sec_pascal = F.pascal_case(name_sec_small)

        # ----------------------------------------------------------------------

        # create global and calculated settings dicts in private.json
        self._dict_prv = {
            C.S_KEY_PRV_ALL: C.D_PRV_ALL,
            C.S_KEY_PRV_PRJ: C.D_PRV_PRJ,
        }

        # create individual dicts in pyplate.py
        self._dict_pub = {
            C.S_KEY_PUB_BL: C.D_PUB_BL,
            C.S_KEY_PUB_DBG: C.D_PUB_DBG,
            C.S_KEY_PUB_DOCS: C.D_PUB_DOCS[prj_type],
            # NB: placeholder until we get prj type
            C.S_KEY_PUB_DIST: {},
            C.S_KEY_PUB_I18N: C.D_PUB_I18N,
            C.S_KEY_PUB_META: C.D_PUB_META,
        }

        # reload dicts after modify
        # NB: VERY IMPORTANT!!!
        self._reload_dicts()

        # ----------------------------------------------------------------------
        # calculate dunder values now that we have project info

        # save project stuff
        self._dict_prv_prj["__PP_TYPE_PRJ__"] = prj_type
        self._dict_prv_prj["__PP_NAME_PRJ__"] = name_prj
        self._dict_prv_prj["__PP_NAME_PRJ_BIG__"] = name_prj_big
        self._dict_prv_prj["__PP_NAME_PRJ_SMALL__"] = name_prj_small
        self._dict_prv_prj["__PP_NAME_PRJ_PASCAL__"] = name_prj_pascal
        self._dict_prv_prj["__PP_NAME_SEC_BIG__"] = name_sec_big
        self._dict_prv_prj["__PP_NAME_SEC_SMALL__"] = name_sec_small
        self._dict_prv_prj["__PP_NAME_SEC_PASCAL__"] = name_sec_pascal
        self._dict_prv_prj["__PP_NAME_VENV__"] = C.S_VENV_FMT_NAME.format(
            name_prj_small
        )
        self._dict_prv_prj["__PP_FILE_APP__"] = C.S_APP_FILE_FMT.format(
            name_prj_small
        )
        self._dict_prv_prj["__PP_CLASS_APP__"] = name_prj_pascal
        self._dict_prv_prj["__PP_FILE_WIN__"] = C.S_WIN_FILE_FMT.format(
            name_sec_small
        )
        self._dict_prv_prj["__PP_CLASS_WIN__"] = name_sec_pascal

        # add dist stuff
        self._dict_pub[C.S_KEY_PUB_DIST] = C.D_PUB_DIST[prj_type].copy()

        # ----------------------------------------------------------------------

        # remove home dir from PyPlate path
        h = str(Path.home())
        p = str(self.P_DIR_PP)
        p = p.lstrip(h).strip("/")
        p = p.lstrip(h).strip("\\")
        # NB: change global val
        self._dict_prv_prj["__PP_DEV_PP__"] = p

        # reload dicts after modify
        self._reload_dicts()

        # blank line before printing progress
        print()

    # --------------------------------------------------------------------------
    # Do any work before template copy
    # --------------------------------------------------------------------------
    def _do_before_template(self):
        """
        Do any work before template copy

        Do any work before copying the template. This method is called just
        before _do_template, before any files have been copied.\n
        It is mostly used to make final adjustments to the 'dict_prv' and
        'dict_pub' dicts before any copying occurs.
        """

        C.do_before_template(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_debug
        )

    # --------------------------------------------------------------------------
    # Copy template files to final location
    # --------------------------------------------------------------------------
    def _do_template(self):
        """
        Copy template files to final location

        Gets dirs/files from template and copies them to the project dir.
        """

        # show info
        print(C.S_ACTION_COPY, end="", flush=True)

        # ----------------------------------------------------------------------
        # do template/all

        # copy template/all
        src = self.P_DIR_PP / C.S_DIR_TEMPLATE / C.S_DIR_ALL
        dst = self._dir_prj
        shutil.copytree(src, dst, dirs_exist_ok=True)

        # ----------------------------------------------------------------------
        # copy template/type

        # get some paths
        prj_type_short = self._dict_prv_prj["__PP_TYPE_PRJ__"]
        prj_type_long = ""

        # get long type of project
        for item in C.L_TYPES:
            if item[0] == prj_type_short:
                prj_type_long = item[2]
                break

        # get the src dir in the template dir
        src = self.P_DIR_PP / C.S_DIR_TEMPLATE / prj_type_long
        dst = self._dir_prj
        shutil.copytree(src, dst, dirs_exist_ok=True)

        # ----------------------------------------------------------------------
        # do stuff outside template all/type

        # copy linked files
        for key, val in C.D_COPY.items():

            # get src/dst
            src = self.P_DIR_PP / key
            dst = self._dir_prj / val

            # copy dir/file
            if src.is_dir():
                shutil.copytree(src, dst)
            elif src.is_file():
                shutil.copy2(src, dst)

        # ----------------------------------------------------------------------
        # merge reqs

        # merge reqs files from all and prj
        self._merge_reqs(prj_type_long)

        # ----------------------------------------------------------------------
        # done
        print(C.S_ACTION_DONE)

    # --------------------------------------------------------------------------
    # Do any work after template copy
    # --------------------------------------------------------------------------
    def _do_after_template(self):
        """
        Do any work after template copy

        Do any work after copying the template. This method is called after
        _do_template, and before _do_before_fix.
        """

        C.do_after_template(
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
    pm = PyMaker()

    # run main method with args
    pm.main()

# -)
