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
import re
import shutil

# venv imports
from cnlib import cnfunctions as F  # type: ignore

# local imports
import pyplate_base as B
from pyplate_base import _

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# dict in pybaker to control post processing in debug mode
D_PB_ACT = {
    B.C.S_KEY_ACT_VENV: True,
    B.C.S_KEY_ACT_REQS: True,
    B.C.S_KEY_ACT_GIT: True,
    B.C.S_KEY_ACT_INST: True,
    B.C.S_KEY_ACT_PURGE: True,
    B.C.S_KEY_ACT_I18N: True,
    B.C.S_KEY_ACT_META: True,
    B.C.S_KEY_ACT_PLACE: True,
    B.C.S_KEY_ACT_EDIT: True,
    B.C.S_KEY_ACT_DOCS_MAKE: True,
    B.C.S_KEY_ACT_TREE: True,
    B.C.S_KEY_ACT_FREEZE: True,
    B.C.S_KEY_ACT_DOCS_BAKE: True,
    B.C.S_KEY_ACT_DOCS_DEPLOY: True,
    B.C.S_KEY_ACT_COMPRESS: True,
    B.C.S_KEY_ACT_REM_DIST: True,
}

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class PyBaker(B.PyPlateBase):
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

    # lang option strings
    S_ARG_LANG_OPTION = "-l"
    S_ARG_LANG_DEST = "LANG_DEST"
    # I18N: lang option help
    S_ARG_LANG_HELP = _("add a language (*.po) file")
    # I18N: lang file source
    S_ARG_LANG_METAVAR = _("FILE")

    # ide option strings
    S_ARG_VER_OPTION = "-v"
    S_ARG_VER_DEST = "VER_DEST"
    # I18N help string for version cmd line option
    S_ARG_VER_HELP = _("set the new version of the project")
    # I18N: config file dest
    S_ARG_VER_METAVAR = _("VERSION")

    # about string
    S_ABOUT = (
        f"{'PyPlate/PyBaker'}\n"
        f"{B.PyPlateBase.S_PP_SHORT_DESC}\n"
        f"{B.PyPlateBase.S_PP_VERSION}\n"
        f"https://github.com/cyclopticnerve/PyPlate"
    )

    # I18N: cmd line instructions string
    S_EPILOG = _(
        "Run this program from the directory of the project you want to build."
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
        self._get_project_info()

        # handle -v AFTER getting current project info
        self._handle_v()

        # ----------------------------------------------------------------------
        # print some info
        print()
        print(B.C.S_MSG_BAKE.format(self._dir_prj.name))
        print()

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

        # done with project
        print()

        # NB: easier to parse path than get dunder
        if B.C.B_ERROR:
            print(self.S_ERR_BAKE.format(self._dir_prj.name))
            if not B.C.B_DEBUG:
                print(self.S_ERR_USE_D)
        else:
            print(B.C.S_MSG_BAKE_DONE.format(self._dir_prj.name))

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
        self._parser.prog = "pybaker"

        # add lang option
        self._parser.add_argument(
            self.S_ARG_LANG_OPTION,
            dest=self.S_ARG_LANG_DEST,
            help=self.S_ARG_LANG_HELP,
            metavar=self.S_ARG_LANG_METAVAR,
        )

        # add version option
        self._parser.add_argument(
            self.S_ARG_VER_OPTION,
            dest=self.S_ARG_VER_DEST,
            help=self.S_ARG_VER_HELP,
            metavar=self.S_ARG_VER_METAVAR,
        )

        # do setup
        super()._setup()

        # ----------------------------------------------------------------------
        # handle custom args
        self._handle_l()

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
        self._dict_act = dict(D_PB_ACT)

        # ----------------------------------------------------------------------

        # ask for prj name rel to cwd
        in_str = B.C.S_ASK_IDE.format(self._dir_prj)
        while True:
            prj_name = input(in_str)
            if prj_name == "":
                continue

            # if running in ide, cwd is pyplate prj dir, so move up + down
            tmp_dir = B.Path(self._dir_prj / prj_name).resolve()

            # check if project exists
            if not tmp_dir.exists():
                e_str = B.C.S_ERR_NOT_EXIST.format(tmp_dir)
                print(e_str)
                continue

            # set project dir and exit loop
            self._dir_prj = tmp_dir
            break

    # --------------------------------------------------------------------------
    # Handle the -l option
    # --------------------------------------------------------------------------
    def _handle_l(self):
        """
        Docstring for _handle_l

        :param self: Description
        """

        # if no lang, no go
        lang_file = self._dict_args.get(self.S_ARG_LANG_DEST, None)
        if not lang_file:
            return

        print(B.C.S_MSG_LANG_ADD.format(lang_file), flush=True, end="")

        # default lang code
        lang_code = ""

        # get code from file
        p_lang = self._dir_prj / lang_file

        # in case of typo -)
        if not p_lang.exists():
            F.printc(B.C.S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
            return

        # find the line
        with open(p_lang, "r", encoding=B.C.S_ENCODING) as a_file:
            string = a_file.read()

        # find the lang
        res = re.search(B.C.S_PO_LANG_SCH, string)
        if res:
            lang_code = res.group(2)

        # make sure it worked before doing api
        if lang_code == "":
            F.printc(B.C.S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
            return

        # get lang dict from props
        dict_lang = self._dict_pub_i18n[B.C.S_KEY_PUB_I18N_WLANGS]

        # only add once (might be old)
        if not lang_code in dict_lang:
            dict_lang.append(lang_code)

        # check file exists
        dst = self._dir_prj / B.C.S_DIR_I18N / B.C.S_DIR_PO / lang_code
        dst_file = dst / lang_file
        if dst_file.exists():
            print()

            # ask to overwrite
            msg = B.C.S_ASK_OVER.format(lang_file)
            ask = F.dialog(msg, [F.S_ASK_YES, F.S_ASK_NO], default=F.S_ASK_NO)
            if ask != F.S_ASK_YES:
                F.printc(B.C.S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
                return

        # copy file to dest
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy(p_lang, dst_file)

        F.printc(B.C.S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)

    # --------------------------------------------------------------------------
    # Handle the -v option
    # --------------------------------------------------------------------------

    def _handle_v(self):
        """
        Docstring for _handle_v

        :param self: Description
        """

        # first check if passed on cmd line
        ver = self._dict_args.get(self.S_ARG_VER_DEST, None)
        if ver:

            # check version before we start fixing
            pattern = B.C.S_SEM_VER_VALID
            version = ver
            ver_ok = B.re.search(pattern, version) is not None

            # ask if user wants to keep invalid version or quit
            if not ver_ok:
                res = F.dialog(
                    B.C.S_ERR_SEM_VER,
                    [F.S_ASK_YES, F.S_ASK_NO],
                    default=F.S_ASK_NO,
                    loop=True,
                )
                if res != F.S_ASK_YES:
                    self._teardown(-1)

        # not passed, ask question
        else:

            # format and ask question
            old_ver = self._dict_pub_meta[B.C.S_KEY_META_VERSION]
            ask_ver = B.C.S_ASK_VER.format(old_ver)

            # loop until condition
            while True:

                # ask for new version
                new_ver = input(ask_ver)

                # user pressed Enter, return original
                if new_ver == "":

                    # set the same version, and we are done
                    ver = old_ver
                    break

                # check version before we start fixing
                pattern = B.C.S_SEM_VER_VALID
                version = new_ver
                ver_ok = B.re.search(pattern, version) is not None

                # ask if user wants to keep invalid version or quit
                if ver_ok:

                    # set the new version, and we are done
                    ver = new_ver
                    break

                # print version error
                print(B.C.S_ERR_SEM_VER)

        # change in project.json
        self._dict_pub_meta[B.C.S_KEY_META_VERSION] = ver

        # set version in install dict
        prj_type = self._dict_prv_prj["__PP_TYPE_PRJ__"]
        if prj_type in B.C.L_APP_INSTALL:
            self._dict_pub_inst[B.C.S_KEY_INST_VER] = ver

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Check that the PyPlate data is present and correct, so we don't crash
        looking for non-existent files. Also handles command line settings.
        """

        # ----------------------------------------------------------------------
        # sanity checks

        # check if dir_prj has pyplate folder for a valid prj
        path_pyplate = self._dir_prj / B.C.S_PRJ_PP_DIR
        if not path_pyplate.exists():
            print(B.C.S_ERR_NOT_PRJ)
            self._teardown(-1)

        # check if data files exist
        path_prv = self._dir_prj / B.C.S_PRJ_PRV_CFG
        path_pub = self._dir_prj / B.C.S_PRJ_PUB_CFG
        if not path_prv.exists() or not path_pub.exists():
            print(B.C.S_ERR_PP_MISSING)
            self._teardown(-1)

        # ----------------------------------------------------------------------
        # make dicts from files

        # check if files are valid json
        try:
            # get settings dicts in private.json
            self._dict_prv = F.load_paths_into_dict(path_prv)

            # get settings dicts in project.json
            # NB: may contain dunders
            self._dict_pub = F.load_paths_into_dict(path_pub)

        # if there was a problem
        except OSError as e:  # from load_dicts
            # exit gracefully
            print(B.C.S_ERR_ERR, e)
            self._teardown(-1)

        # ----------------------------------------------------------------------
        # fix dicts
        self._fix_dicts()

        # # ----------------------------------------------------------------------
        # # print some info
        # print()
        # print(B.C.S_MSG_BAKE.format(self._dir_prj.name))
        # print()

    # --------------------------------------------------------------------------
    # Do any work before making dist
    # --------------------------------------------------------------------------
    def _do_before_dist(self):
        """
        Do any work before making dist

        Do any work on the dist folder before it is created. This method is
        called after _do_after_fix, and before _do_dist.
        """

        B.C.do_before_dist(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_act
        )

    # --------------------------------------------------------------------------
    # Copy fixed files to final location
    # --------------------------------------------------------------------------
    # NB: HOWS THIS FOR A FUCKING IMPORT CHAIN?!?!
    @B.C.S.spin(B.C.S_ACTION_DIST)
    def _do_dist(self):
        """
        Copy fixed files to final location

        Gets dirs/files from project and copies them to the dist/assets dir.
        """

        # ----------------------------------------------------------------------
        # do common dist stuff

        # find old dist? nuke it from orbit! it's the only way to be sure!
        a_dist = self._dir_prj / B.C.S_DIR_DIST
        if a_dist.is_dir():
            shutil.rmtree(a_dist)

        # make child dir in case we nuked
        name_fmt = self._dict_prv_prj["__PP_FMT_DIST__"]
        p_dist = a_dist / name_fmt
        p_dist.mkdir(parents=True)

        # for each key, val (type, dict)
        for key, val in self._dict_pub_dist.items():

            # get src/dst rel to prj dir/dist dir
            src = self._dir_prj / key
            dst = p_dist / str(val)
            if not dst.exists():
                dst.mkdir(parents=True)
            dst = dst / src.name

            # do the copy
            if src.exists() and src.is_dir():
                shutil.copytree(src, dst, dirs_exist_ok=True)
            elif src.exists() and src.is_file():
                shutil.copy2(src, dst)

        # ----------------------------------------------------------------------
        # done
        # NB: None = pass, Exception = fail
        return None

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

        B.C.do_after_dist(
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
    pb = PyBaker()

    # run the new object
    pb.main()

# -)

# "in little rooms, in buildings, "
# "in the middle of these lives "
# "which are completely meaningless..."
