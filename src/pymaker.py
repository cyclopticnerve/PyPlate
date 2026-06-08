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
import shutil

# venv imports
from cnlib import cnfunctions as F  # type: ignore

# local imports
import pyplate_base as B
from pyplate_base import _

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ALTERNATE dict in pymaker to control pm processing
# NB: this is what controls the steps in making TEST projects
# it does NOT affect the project's 'pyplate/*' files
D_PM_ACT = {
    B.C.S_KEY_ACT_VENV: True,
    B.C.S_KEY_ACT_REQS: True,
    B.C.S_KEY_ACT_GIT: True,
    B.C.S_KEY_ACT_INST: True,
    B.C.S_KEY_ACT_PURGE: True,
    B.C.S_KEY_ACT_I18N: True,
    B.C.S_KEY_ACT_META: True,
    B.C.S_KEY_ACT_PLACE: True,
    B.C.S_KEY_ACT_EDIT: True,
    B.C.S_KEY_ACT_MAKE_DOCS: True,
    B.C.S_KEY_ACT_TREE: True,
    B.C.S_KEY_ACT_FREEZE: True,
    B.C.S_KEY_ACT_BAKE_DOCS: True,
    B.C.S_KEY_ACT_DEPLOY_DOCS: True,
    B.C.S_KEY_ACT_COMPRESS: True,
    B.C.S_KEY_ACT_REM_DIST: True,
}

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class PyMaker(B.PyPlateBase):
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
        f"{'PyPlate/PyMaker'}\n"
        f"{B.PyPlateBase.S_PP_SHORT_DESC}\n"
        f"{B.PyPlateBase.S_PP_VERSION}\n"
        f"https://github.com/cyclopticnerve/PyPlate"
    )

    # I18N: cmd line instructions string
    S_EPILOG = _(
        "Run this program from the directory where you want to create "
        "a project."
    )

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

        # call boilerplate code
        self._setup()

        # ----------------------------------------------------------------------
        # main stuff

        # get project info
        self._get_project_info()  # here

        # do before template
        self._do_before_template()  # here/conf

        # copy template
        self._do_template()  # here

        # do before template
        self._do_after_template()  # here/conf

        # do any fixing up of dicts (like meta keywords, etc)
        self._do_before_fix()  # super

        # do replacements in final project location
        self._do_fix()  # super

        # do extra stuff to final dir after fix
        self._do_after_fix()  # super

        # done with project
        print()

        # NB: easier to parse path than get dunder
        if B.C.B_ERROR:
            print(self.S_ERR_MAKE.format(self._dir_prj.name))
            if not B.C.B_DEBUG:
                print(self.S_ERR_USE_D)
        else:
            print(B.C.S_MSG_MAKE_DONE.format(self._dir_prj.name))

        # ----------------------------------------------------------------------
        # teardown

        # call boilerplate code
        self._save_config()
        self._teardown()

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

        # name to use for the usage string (defaults to pyplate)
        self._parser.prog = "pymaker"

        # do parent setup
        super()._setup()

        # do not run pymaker in pyplate dir
        # NB: expensive, but needs to be done after testing for -h and
        # --uninstall
        if self._dir_prj.is_relative_to(B.P_DIR_PRJ):
            F.printc(B.C.S_ERR_PRJ_DIR_IS_PP, fg=F.C_FG_RED, bold=True)
            self._teardown(-1)

    # --------------------------------------------------------------------------
    # Handle the -t option
    # --------------------------------------------------------------------------
    def _handle_t(self):
        """
        Docstring for _handle_t
        """

        # super for warning
        super()._handle_t()

        # local
        self._dict_act = dict(D_PM_ACT)

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Asks the user for project info, such as type and name, to be saved to
        self._dict_prv_prj.
        """

        # check version from conf
        pattern = B.C.S_SEM_VER_VALID
        version = B.C.D_PUB_META[B.C.S_KEY_META_VERSION]
        ver_ok = B.re.search(pattern, version) is not None

        # ask if user wants to keep invalid version or quit
        if not ver_ok:
            res = F.dialog(
                B.C.S_ERR_SEM_VER,
                [F.S_ASK_YES, F.S_ASK_NO],
                default=F.S_ASK_NO,
                # loop=True
            )
            if res != F.S_ASK_YES:
                self._teardown(-1)

        # ----------------------------------------------------------------------
        # first question is type
        # NB: this makes the string to display in terminal

        # sanity check
        prj_type = ""

        # build the input question
        types = []
        for item in B.C.L_TYPES:
            s = B.C.S_ASK_TYPE_FMT.format(item[0], item[1])
            types.append(s)
        str_types = B.C.S_ASK_TYPE_JOIN.join(types)

        # format the question
        in_type = B.C.S_ASK_TYPE.format(str_types)

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

        # if in test mode
        if self._arg_test:

            # get long name
            name_prj = "DEBUG"
            for item in B.C.L_TYPES:
                if item[0] == prj_type:
                    # get debug name of project
                    name_prj = f"{item[1]} DEBUG"
                    break

            # dir name, no spaces
            name_prj_big = name_prj.replace(" ", "_")

            # set up for existence check
            tmp_dir = self._dir_prj / name_prj_big

            # check if project already exists
            if tmp_dir.exists():

                # if it does exist, "nuke it from orbit! it's the only way to
                # be sure!"
                # NB: yes i know ive used this joke more than once... FUCK YOU
                # ITS FUNNY
                shutil.rmtree(tmp_dir)

        # not test mode
        else:

            # loop forever until we get a valid name that does not exist
            while True:

                # ask for name of project
                name_prj = input(B.C.S_ASK_NAME)
                name_prj = name_prj.strip(" ")

                # check for valid name
                if self._check_name(name_prj):

                    # dir name, no spaces
                    name_prj_big = name_prj.replace(" ", "_")

                    # set up for existence check
                    tmp_dir = self._dir_prj / name_prj_big

                    # check if project already exists
                    if tmp_dir.exists():

                        # tell the user that the old name exists
                        print(B.C.S_ERR_EXIST.format(name_prj_big))
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
        if prj_type in B.C.D_NAME_SEC:

            # dup prj names if test mode
            if self._arg_test:
                name_sec = name_prj
                name_sec_big = name_prj_big
                name_sec_small = name_prj_small
                name_sec_pascal = name_prj_pascal

            # if not test mode, if need second name, ask for it
            else:

                # format question for second name
                s_sec_ask = B.C.D_NAME_SEC[prj_type]
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
        # make dicts from conf defaults

        # create global settings dicts in private.json
        self._dict_prv = {
            B.C.S_KEY_PRV_ALL: dict(B.C.D_PRV_ALL),
            B.C.S_KEY_PRV_PRJ: dict(B.C.D_PRV_PRJ),
        }

        # create individual dicts in project.json
        self._dict_pub = {
            B.C.S_KEY_PUB_META: dict(B.C.D_PUB_META),
            B.C.S_KEY_PUB_BL: dict(B.C.D_PUB_BL),
            B.C.S_KEY_PUB_ACT: dict(B.C.D_PUB_ACT),
            B.C.S_KEY_PUB_DIST: dict(B.C.D_PUB_DIST),
            B.C.S_KEY_PUB_DOCS: dict(B.C.D_PUB_DOCS),
            B.C.S_KEY_PUB_I18N: dict(B.C.D_PUB_I18N),
            B.C.S_KEY_PUB_INST: dict(B.C.D_PUB_INST),
        }

        # ----------------------------------------------------------------------
        # fill dicts

        # get prv subs
        self._dict_prv_all = self._dict_prv[B.C.S_KEY_PRV_ALL]
        self._dict_prv_prj = self._dict_prv[B.C.S_KEY_PRV_PRJ]

        # save project stuff
        self._dict_prv_prj["__PP_TYPE_PRJ__"] = prj_type
        self._dict_prv_prj["__PP_NAME_PRJ__"] = name_prj
        self._dict_prv_prj["__PP_NAME_PRJ_BIG__"] = name_prj_big
        self._dict_prv_prj["__PP_NAME_PRJ_SMALL__"] = name_prj_small
        self._dict_prv_prj["__PP_NAME_PRJ_PASCAL__"] = name_prj_pascal
        self._dict_prv_prj["__PP_NAME_SEC_BIG__"] = name_sec_big
        self._dict_prv_prj["__PP_NAME_SEC_SMALL__"] = name_sec_small
        self._dict_prv_prj["__PP_NAME_SEC_PASCAL__"] = name_sec_pascal
        self._dict_prv_prj["__PP_NAME_VENV__"] = B.C.S_VENV_FMT_NAME.format(
            name_prj_small
        )
        self._dict_prv_prj["__PP_FILE_APP__"] = B.C.S_APP_FILE_FMT.format(
            name_prj_small
        )
        self._dict_prv_prj["__PP_CLASS_APP__"] = name_prj_pascal
        self._dict_prv_prj["__PP_FILE_WIN__"] = B.C.S_WIN_FILE_FMT.format(
            name_sec_small
        )
        self._dict_prv_prj["__PP_CLASS_WIN__"] = name_sec_pascal

        # ----------------------------------------------------------------------
        # get reps to fix public
        self._fix_dicts()

        # ----------------------------------------------------------------------

        # print some info
        print()
        print(B.C.S_MSG_MAKE.format(name_prj_big))
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

        B.C.do_before_template(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_act
        )

    # --------------------------------------------------------------------------
    # Copy template files to final location
    # --------------------------------------------------------------------------
    @B.C.S.spin(B.C.S_ACTION_COPY)
    def _do_template(self):
        """
        Copy template files to final location

        Gets dirs/files from template and copies them to the project dir.
        """

        # ----------------------------------------------------------------------
        # do template/all

        # copy template/all
        src = B.P_DIR_PRJ / B.C.S_DIR_TEMPLATE / B.C.S_DIR_ALL
        dst = self._dir_prj
        shutil.copytree(src, dst, dirs_exist_ok=True)

        # ----------------------------------------------------------------------
        # copy template/type

        # get some paths
        prj_type_short = self._dict_prv_prj["__PP_TYPE_PRJ__"]
        prj_type_long = ""

        # get long type of project
        for item in B.C.L_TYPES:
            if item[0] == prj_type_short:
                prj_type_long = item[2]
                break

        # get the src dir in the template dir
        src = B.P_DIR_PRJ / B.C.S_DIR_TEMPLATE / prj_type_long
        dst = self._dir_prj
        shutil.copytree(src, dst, dirs_exist_ok=True)

        # ----------------------------------------------------------------------
        # do stuff outside template all/type

        # copy linked files
        for key, val in B.C.D_COPY.items():

            # get src/dst
            src = B.P_DIR_PRJ / key
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
        # NB: None = pass, Exception = fail
        return None

    # --------------------------------------------------------------------------
    # Do any work after template copy
    # --------------------------------------------------------------------------
    def _do_after_template(self):
        """
        Do any work after template copy

        Do any work after copying the template. This method is called after
        _do_template, and before _do_before_fix.
        """

        B.C.do_after_template(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_act
        )

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # create a new instance of the main class
    pm = PyMaker()

    # run the new object
    pm.main()

# -)
