# ------------------------------------------------------------------------------
# Project : __PC_NAME_BIG__                                        /          \
# Filename: appmain.py                                            |     ()     |
# Date    : __PC_DATE__                                           |            |
# Author  : __PD_AUTHOR__                                         |   \____/   |
# License : __PD_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
The main file that runs the gui application

This script is called from the main script and should not be called directly.
The purpose of this script is to offload as much GUI-specific code as possible
from the main script, so that the main script remains as close to a CLI as
possible.
"""

# TODO: command line
# run standalone (sys.argv -> argparser -> array)
# run from script (script -> argparser -> array)
# .desktop runs calling script with -g option and fixed cmd line
# (calling script -> argparser -> array)

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import json
from pathlib import Path
import sys


# add lib path to import search
C_DIR_LIB = "__PC_USR_LIB__"
sys.path.append(str(C_DIR_LIB))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
import guiconstants as GC
from windowmain import WindowMain
from cnapplib.cnapp import CNApp  # type: ignore
from cnapplib import cnappconstants as AC  # type: ignore
from cnlib import cnfunctions as CF  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# path to src dir
# TODO: use install location
# C_PATH_SRC = Path.home() / ".local/share/__PC_NAME_SMALL__"
C_PATH_SRC = Path(__file__).parent

# get path to config file
C_PATH_GUI = C_PATH_SRC / "cfg/__PC_NAME_SMALL__.json"

# get path to main ui file
C_WIN_MAIN_UI_FILE = C_PATH_SRC / "gtk/__PC_NAME_SMALL__Gtk3.ui"

# properties for whole app
# NB: THIS DICT MUST BE EDITED BY HAND!!!
C_DICT_APP = {
    # the application id to use for GTK (default: "org.foo.bar")
    # AC.KEY_APP_ID: "org.__PD_AUTHOR__.__PC_NAME_SMALL__",
    # I18N: the location of the locale files (default: "")
    # AC.KEY_APP_LOCALE: DIR_SELF / "locale",
    # list of window classes (default: None)
    # NB: this must contain one entry per class of window
    # NB: this dict holds properties common to a certain class of window so
    # that they can be referred to by multiple instances of that class
    # NB: if this value is not present or None or cannot be found, an
    # error will be thrown
    AC.KEY_APP_CLASSES: {
        # the name of the class
        GC.WIN_MAIN_CLASS: {
            # path to the class window's ui file (default: None)
            # NB: if this value is not present or None or cannot be found, an
            # error will be thrown
            AC.KEY_CLS_UI_FILE: C_WIN_MAIN_UI_FILE,
            # the name of the window object in the ui file (default: None)
            # NB: if this value is not present or None or cannot be found, an
            # error will be thrown
            AC.KEY_CLS_UI_NAME: GC.CLS_UI_NAME,
            # the name for this window's handler (default: None)
            # NB: if this value is not present or None or cannot be found, an
            # error will be thrown
            AC.KEY_CLS_HANDLER: WindowMain,
            #  what to do when the 'X'/close button is clicked or quit
            # (default: constants.DEF_CLOSE_ACTION)
            # AC.KEY_CLS_CLOSE_ACTION: AC.CLOSE_ACTION_ASK,
            # whether to show modified indicator in the window title (default:
            # constants.DEF_CLS_SHOW_MOD)
            # AC.KEY_CLS_SHOW_MOD: True,
            # the char to use as the modified indicator (default:
            # constants.DEF_CLS_MOD_CHAR)
            # AC.KEY_CLS_MOD_CHAR: "\u29BF",
            # title format for modified windows (default:
            # constants.DEF_CLS_MOD_FMT)
            # NB: ${MOD} will be replaced by the class's mod char
            # NB: ${TITLE} will be replaced by the window's title
            # AC.KEY_CLS_MOD_FMT: "${MOD} ${TITLE}",
            # the names and types of controls to save/load (default: None)
            # NB: if this key missing or the value is None or empty, no
            # controls will be saved/loaded
            AC.KEY_CLS_CTLS: {
                # the name of the control in the ui file
                GC.WIN_MAIN_ENTRY_TEST: {
                    # the type of control from constants.CTL_TYPE_... (default:
                    # constants.CTL_TYPE_TEXT)
                    # AC.KEY_CTL_TYPE: AC.CTL_TYPE_TEXT,
                },
                # the name of the control in the ui file
                GC.WIN_MAIN_CHECK_TEST: {
                    # the type of control from constants.CTL_TYPE_... (default:
                    # constants.CTL_TYPE_TEXT)
                    AC.KEY_CTL_TYPE: AC.CTL_TYPE_CHECK,
                },
            },
        },
    },
    # the list of window instances to be created at startup (default: None)
    # NB: here the properties indicate what to use when the window is first
    # created, not what is restored from a previous session (those props are
    # stored in the gui dict)
    AC.KEY_APP_WINDOWS: {
        # the name of a window instance (must be unique)
        # NB: this allows multiple instances of the same window ui with
        # separate properties, ie. document-based apps which can have more than
        # one editor window, each with the same ui class and ui file, but
        # different sizes/control values
        GC.WIN_MAIN_INST: {
            # the class of this window (must be a key in
            # DICT_APP[constants.KEY_APP_CLASSES])
            # NB: if this value is not present or None or cannot be found, an
            # error will be thrown
            AC.KEY_WIN_CLASS: GC.WIN_MAIN_CLASS,
            # whether to show this window at startup (default:
            # constants.DEF_WIN_VISIBLE)
            # NB: initially, at least one window must have this prop set to
            # true otherwise no windows will be shown
            # AC.KEY_WIN_VISIBLE: True,
            # ------------------------------------------------------------------
            # everything below this line is saved/loaded between sessions
            # ------------------------------------------------------------------
            # the initial size of the window (default: ui size)
            # AC.KEY_WIN_CLASS: "win_main_window"
            # AC.KEY_WIN_VISIBLE: <bool>,
            # AC.KEY_WIN_SIZE: {
            #     AC.KEY_SIZE_W: <int>,
            #     AC.KEY_SIZE_H: <int>,
            #     AC.KEY_SIZE_M: <bool>,
            # },
            # the initial values of the window's controls (default: ui values)
            # AC.KEY_WIN_CTLS: {
            #     # the name of the control in the ui file
            #     "entry_test": {
            #         AC.KEY_CTL_VAL: <str/int/bool>,
            #     },
            #     "check_test": {
            #         AC.KEY_CTL_VAL: <str/int/bool>,
            #     },
            # },
        },
    },
}

# the default gui dict
C_DICT_GUI = {}

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main class, responsible for the operation of the program
# ------------------------------------------------------------------------------
class AppMain:
    """
    The main class, responsible for the operation of the program

    Public methods:
        main: The main function of the program

    This object is responsible for creating and managing the GUI portion of the
    program.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, args, dict_cfg):
        """
        Initialize the new object

        Arguments:
            dict_args: The dict of the command line arguments to the main
            script
            dict_cfg: The dict loaded from the calling script, if any

        Initializes a new instance of the class, setting the default values
        of its properties, and any other code that needs to run to create a
        new object.
        """

        # call super init to initialize the base class
        super().__init__()

        # assign params to props
        self._args = args
        self._dict_cfg = dict_cfg
        self._dict_gui = C_DICT_GUI

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main function of the program
    # --------------------------------------------------------------------------
    def main(self):
        """
        The main function of the program

        This function sets up the various dictionaries and creates an App
        object to show the main window of the program.
        """

        # load gui from const file
        CF.load_dicts([C_PATH_GUI], self._dict_gui)

        # create app
        app = CNApp(
            "org.cyclopticnerve.foo",
            C_DICT_APP,
            dict_gui=self._dict_gui,
            dict_cfg=self._dict_cfg,
        )

        # run main function
        app.run()

        # get the last state of the GUI so we can save it
        self._dict_gui = app.get_dict_gui()

        # save the last state of the GUI to the const file
        CF.save_dict([C_PATH_GUI], self._dict_gui)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # The main function of the program for a debug GUI
    # --------------------------------------------------------------------------
    def _debug_main(self):
        """
        The main function of the program for a debug GUI

        This function sets up the various dictionaries and creates an App
        object to show the main window of the program in debug mode.
        """

        test = 6

        # these are all the test conditions i could think of...
        path_gui = Path()
        dict_gui = None
        app = None

        # NB: test=8 for default path
        if test == 0:
            app = CNApp()  # type: ignore # pylint: disable=no-value-for-parameter
        elif test == 1:
            app = CNApp(None)
        elif test == 2:
            app = CNApp({})
        elif test == 3:
            # test with no param
            app = CNApp(C_DICT_APP, args=self._args)
        elif test == 4:
            # test with None
            app = CNApp(C_DICT_APP, args=self._args, dict_gui=None)
        elif test == 5:
            # test with empty
            app = CNApp(C_DICT_APP, args=self._args, dict_gui={})
        elif test == 6:
            # test with setting dict manually

            # use appropriate values: strings where necessary, else ints/bools
            # integers will be converted
            # strings/bools WILL NOT
            dict_gui = {
                GC.WIN_MAIN_INST: {
                    AC.KEY_WIN_CLASS: GC.WIN_MAIN_CLASS,
                    AC.KEY_WIN_VISIBLE: "True",
                    AC.KEY_WIN_SIZE: {
                        AC.KEY_SIZE_W: "1000",
                        AC.KEY_SIZE_H: "200",
                        AC.KEY_SIZE_M: "False",
                    },
                    # TODO: make this a simple in/out file to be editable by
                    # hand or passed on cmd line (translate between cli and
                    # gui) also needs win inst name as top key
                    AC.KEY_WIN_CTLS: {
                        "entry_test": {
                            AC.KEY_CTL_VAL: "XXX",
                        },
                        "check_test": {
                            AC.KEY_CTL_VAL: "True",
                        },
                    },
                },
            }
            app = CNApp(C_DICT_APP, args=self._args, dict_gui=dict_gui)
        else:
            if test == 7:
                # test with file not exist
                path_gui = Path("not_a_path")
            elif test == 8:
                # test with invalid file
                path_gui = C_PATH_SRC / "tests/invalid.json"
            elif test == 9:
                # test with missing control type
                path_gui = C_PATH_SRC / "tests/missing_keys.json"
            elif test == 10:
                # test with valid file
                path_gui = C_PATH_SRC / "tests/valid.json"

            # try to open/validate default gui file
            with open(path_gui, "r", encoding="utf8") as f:
                dict_gui = json.loads(f.read())

            app = CNApp(C_DICT_APP, args=self._args, dict_gui=dict_gui)
        # ----------------------------------------------------------------------

        # run main function
        app.run()

        # ----------------------------------------------------------------------

        # get the last state of the GUI so we can save it
        after_dict = app.get_dict_gui()
        print(f"after:{json.dumps(after_dict, indent=4)}")


# -)
