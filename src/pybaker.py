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

# local imports
from cnlib import cnfunctions as F  # type: ignore
import pyplate as P
from pyplate import _
from pyplate import PyPlate

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

    # ide option strings
    S_ARG_IDE_OPTION = "-i"
    S_ARG_IDE_ACTION = "store_true"
    S_ARG_IDE_DEST = "IDE_DEST"
    # I18N help string for ide cmd line option
    S_ARG_IDE_HELP = _("ask for project folder when running in IDE")

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
    S_ARG_VER_HELP = _(
        "set the new version of the project\n(if used, -l is ignored)"
    )
    # I18N: config file dest
    S_ARG_VER_METAVAR = _("VERSION")

    # about string
    S_ABOUT = (
        "\n"
        f"{'PyPlate/PyBaker'}\n"
        f"{PyPlate.S_PP_SHORT_DESC}\n"
        f"{PyPlate.S_PP_VERSION}\n"
        f"https://github.com/cyclopticnerve/PyPlate\n"
    )

    # I18N cmd line instructions string
    S_EPILOG = _(
        "Run this program from the directory of the project you want to build."
    )

    # error strings

    # I18N: language already exists in project.json and i18n folder
    S_ERR_LANG_EXIST = _("Language file {} already exists")
    S_ERR_NO_LANG = _("Could not get language code from {}")

    # messages

    # bake msg
    # NB: param is name of project folder
    S_MSG_BAKE = _("Baking {}")
    # NB: format param is file name
    # I18N: add language at cmd line
    S_MSG_LANG_ADD = _("Adding language file {}...")

    # questions

    # I18N: answer yes
    S_ASK_YES = _("y")
    # I18N: answer no
    S_ASK_NO = _("N")
    # NB: format param is file name
    # I18N: ask to overwrite
    S_ASK_OVER = _("The file {} already exists. Do you want to overwrite it?")

    # --------------------------------------------------------------------------
    # Instance methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    # def __init__(self):
    #     """
    #     Initialize the new object

    #     Initializes a new instance of the class, setting the default values
    #     of its properties, and any other code that needs to run to create a
    #     new object.
    #     """

    #     # do super init
    #     super().__init__()

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

        # ----------------------------------------------------------------------
        # teardown

        # call boilerplate code
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

        # add ide option
        self._parser.add_argument(
            self.S_ARG_IDE_OPTION,
            dest=self.S_ARG_IDE_DEST,
            help=self.S_ARG_IDE_HELP,
            action=self.S_ARG_IDE_ACTION,
        )

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

    # --------------------------------------------------------------------------
    # Get project info
    # --------------------------------------------------------------------------
    def _get_project_info(self):
        """
        Get project info

        Raises:
            OSError if anything goes wrong

        Check that the PyPlate data is present and correct, so we don't crash
        looking for non-existent files. Also handles command line settings.
        """

        # ----------------------------------------------------------------------

        # handle -i
        self._handle_i()

        # ----------------------------------------------------------------------
        # sanity checks

        # check if dir_prj has pyplate folder for a valid prj
        path_pyplate = self._dir_prj / P.C.S_PRJ_PP_DIR
        if not path_pyplate.exists():
            print(P.C.S_ERR_NOT_PRJ)
            P.sys.exit(-1)

        # check if data files exist
        path_prv = self._dir_prj / P.C.S_PRJ_PRV_CFG
        path_pub = self._dir_prj / P.C.S_PRJ_PUB_CFG
        if not path_prv.exists() or not path_pub.exists():
            print(P.C.S_ERR_PP_MISSING)
            P.sys.exit(-1)

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
            print(self.S_ERR_ERR, e)
            P.sys.exit(-1)

        # ----------------------------------------------------------------------
        # fix dicts
        self._fix_dicts()

        # ----------------------------------------------------------------------
        # handle -d
        # NB: do after _fix_dicts
        if self._cmd_debug:
            self._dict_dbg = dict(P.C.D_DBG_PB)

        # ----------------------------------------------------------------------
        # handle -v
        self._handle_v()

        # ----------------------------------------------------------------------
        # handle -l
        self._handle_l()

        # ----------------------------------------------------------------------
        # print some info
        print()
        print(self.S_MSG_BAKE.format(self._dir_prj.name))

        # blank line before printing progress
        print()

    # --------------------------------------------------------------------------
    # Do any work before making dist
    # --------------------------------------------------------------------------
    def _do_before_dist(self):
        """
        Do any work before making dist

        Do any work on the dist folder before it is created. This method is
        called after _do_after_fix, and before _do_dist.
        """

        P.C.do_before_dist(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_dbg
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
        print(P.C.S_ACTION_DIST, end="", flush=True)

        # ----------------------------------------------------------------------
        # do common dist stuff

        # find old dist? nuke it from orbit! it's the only way to be sure!
        a_dist = self._dir_prj / P.C.S_DIR_DIST
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
        # done copying project files
        F.printc(P.C.S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)

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

        P.C.do_after_dist(
            self._dir_prj, self._dict_prv, self._dict_pub, self._dict_dbg
        )

    # --------------------------------------------------------------------------
    # Handle the -i option
    # --------------------------------------------------------------------------
    def _handle_i(self):
        """
        Docstring for _handle_i

        :param self: Description
        """

        ide = self._dict_args.get(self.S_ARG_IDE_DEST, False)
        if not ide:
            return

        # ask for prj name rel to cwd
        in_str = P.C.S_ASK_IDE.format(self._dir_prj)
        while True:
            prj_name = input(in_str)
            if prj_name == "":
                continue

            # if running in ide, cwd is pyplate prj dir, so move up + down
            tmp_dir = P.Path(self._dir_prj / prj_name).resolve()

            # check if project exists
            if not tmp_dir.exists():
                e_str = P.C.S_ERR_NOT_EXIST.format(tmp_dir)
                print(e_str)
                continue

            # set project dir and exit loop
            self._dir_prj = tmp_dir
            # print()
            break

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
            pattern = P.C.S_SEM_VER_VALID
            version = ver
            ver_ok = P.re.search(pattern, version) is not None

            # ask if user wants to keep invalid version or quit
            if not ver_ok:
                res = F.dialog(
                    P.C.S_ERR_SEM_VER,
                    [P.C.S_ERR_SEM_VER_Y, P.C.S_ERR_SEM_VER_N],
                    default=P.C.S_ERR_SEM_VER_N,
                    loop=True,
                )
                if res == P.C.S_ERR_SEM_VER_N:
                    P.sys.exit(-1)

        # not passed, ask question
        else:

            # format and ask question
            old_ver = self._dict_pub_meta[P.C.S_KEY_META_VERSION]
            ask_ver = P.C.S_ASK_VER.format(old_ver)

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
                pattern = P.C.S_SEM_VER_VALID
                version = new_ver
                ver_ok = P.re.search(pattern, version) is not None

                # ask if user wants to keep invalid version or quit
                if ver_ok:

                    # set the new version, and we are done
                    ver = new_ver
                    break

                # print version error
                print(P.C.S_ERR_SEM_VER)

        # change in project.json
        self._dict_pub_meta[P.C.S_KEY_META_VERSION] = ver

        # set version in install dict
        prj_type = self._dict_prv_prj["__PP_TYPE_PRJ__"]
        if prj_type in P.C.L_APP_INSTALL:
            self._dict_pub_inst[P.C.S_KEY_INST_VER] = ver

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

        print(self.S_MSG_LANG_ADD.format(lang_file), flush=True, end="")

        # default lang code
        lang_code = ""

        # get code from file
        p_lang = self._dir_prj / lang_file

        # in case of typo -)
        if not p_lang.exists():
            F.printc(P.C.S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
            return

        # find the line
        with open(p_lang, "r", encoding=P.C.S_ENCODING) as a_file:
            string = a_file.read()

        # find the lang
        res = re.search(P.C.S_PO_LANG_SCH, string)
        if res:
            lang_code = res.group(2)

        # make sure it worked before doing api
        if lang_code == "":
            F.printc(P.C.S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
            return

        # get lang dict from props
        dict_lang = self._dict_pub_i18n[P.C.S_KEY_PUB_I18N_WLANGS]

        # only add once (might be old)
        if not lang_code in dict_lang:
            dict_lang.append(lang_code)

        # check file exists
        dst = self._dir_prj / P.C.S_DIR_I18N / P.C.S_DIR_PO / lang_code
        dst_file = dst / lang_file
        if dst_file.exists():
            print()

            # ask to overwrite
            msg = self.S_ASK_OVER.format(lang_file)
            ask = F.dialog(
                msg, [self.S_ASK_YES, self.S_ASK_NO], default=self.S_ASK_NO
            )
            if ask != self.S_ASK_YES:
                F.printc(P.C.S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
                return

        # copy file to dest
        dst.mkdir(parents=True, exist_ok=True)
        shutil.copy(p_lang, dst_file)

        F.printc(P.C.S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)

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
