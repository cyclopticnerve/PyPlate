# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: windowmain.py                                         |     ()     |
# Date    : 12/08/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to manage a specific Window (or type of window).

This class manages the more advanced functions of a window, such as specific
control handlers.
Remember to connect all the appropriate window events in your ui file to the
private functions declared here.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
# from datetime import datetime
from pathlib import Path
import sys

# find paths to dev or user
DIR_PARENT = Path(__file__).parent.resolve()
if DIR_PARENT.name == "src":
    DIR_PRJ = DIR_PARENT.parent
    DIR_CFG = DIR_PRJ / "src/support/conf"
    DIR_LIB = Path.home() / "Documents/Projects/Python/PyPlate" / "lib"
    DIR_SRC = DIR_PRJ / "src" / "support"
else:
    DIR_HOME = Path.home()
    DIR_CFG = DIR_HOME / ".config/pyplate"
    DIR_LIB = DIR_HOME / ".local/share/cyclopticnerve/lib"
    DIR_SRC = DIR_HOME / ".local/share/pyplate"

# add paths to import search
sys.path.append(str(DIR_LIB))
sys.path.append(str(DIR_SRC))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
from cnapplib.cnwindow import CNWindow  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=import-error
# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to wrap a specific window object in the ui file
# ------------------------------------------------------------------------------
class WindowMain(CNWindow):
    """
    A class to wrap a specific window object in the ui file

    This class contains all the handler code for a specific window and it's
    controls.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, app, name_win):
        """
        Initialize the new object

        Arguments:
            app: The calling Application object
            name_win: The name of the window in the app's instance list

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # props necessary tro create a basic window
        ui_file = (
            DIR_PARENT / "support" / "ui" / "pyplateGtk3.ui"
        )
        ui_path = Path(ui_file).resolve()
        ui_name = "win_main"

        # create a basic window
        super().__init__(app, name_win, ui_path, ui_name)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the About button is clicked
    # --------------------------------------------------------------------------
    def _btn_about_clicked(self, _obj):
        """
        Called when the About button is clicked

        Arguments:
            _obj: Not used

        The About button was clicked, show the About dialog.
        """

        # get dialog, run, hide (standard for reusable modal dialogs)
        dlg_file = DIR_PARENT / "support" / "ui" / "dialogs.ui"
        dlg_path = Path(dlg_file).resolve()
        self._app.show_dialog(dlg_path, "dlg_about")

    # --------------------------------------------------------------------------
    # Called when the New button is clicked
    # --------------------------------------------------------------------------
    def _btn_new_clicked(self, _obj):
        """
        Called when the New button is clicked

        Arguments:
            _obj: Not used

        The New button was clicked, add the new window.
        """

        print("btn_new", ": not implemented")

    # --------------------------------------------------------------------------
    # Called when the Title button is clicked
    # --------------------------------------------------------------------------
    def _btn_title_clicked(self, _obj):
        """
        Called when the Title button is clicked

        Arguments:
            _obj: Not used

        The Title button was clicked, change the window title.
        """

        print("btn_title", ": not implemented")

    # --------------------------------------------------------------------------
    # Called when the Save button is clicked
    # --------------------------------------------------------------------------
    def _btn_save_clicked(self, _obj):
        """
        Called when the Save button is clicked

        Arguments:
            _obj: Not used

        The Save button was clicked.
        """

        print("btn_save", ": not implemented")

    # --------------------------------------------------------------------------
    # Called when the Cancel button is clicked
    # --------------------------------------------------------------------------
    def _btn_cancel_clicked(self, _obj):
        """
        Called when the Cancel button is clicked

        Arguments:
            _obj: Not used

        The Cancel button was clicked.
        """

        print("btn_cancel", ": not implemented")

    # --------------------------------------------------------------------------
    # Called when the OK button is clicked
    # --------------------------------------------------------------------------
    def _btn_ok_clicked(self, _obj):
        """
        Called when the OK button is clicked

        Arguments:
            _obj: Not used

        The OK button was clicked.
        """

        print("btn_ok", ": not implemented")

    # --------------------------------------------------------------------------
    # Called when the Close button is clicked
    # --------------------------------------------------------------------------
    def _btn_close_clicked(self, _obj):
        """
        Called when the Close button is clicked

        Arguments:
            _obj: Not used

        The OK button was clicked.
        """

        # close the window as if by the 'X' button
        self.window.close()


# -)
