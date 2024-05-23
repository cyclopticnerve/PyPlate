# ------------------------------------------------------------------------------
# Project : __PC_NAME_BIG__                                        /          \
# Filename: windowmain.py                                         |     ()     |
# Date    : __PC_DATE__                                           |            |
# Author  : __PD_AUTHOR__                                         |   \____/   |
# License : __PD_LICENSE_NAME__                                    \          /
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
from datetime import datetime
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# add lib path to import search
DIR_LIB = "__PC_USR_LIB__"
sys.path.append(str(DIR_LIB))

import guiconstants as GC
from cnapplib.cnwindow import CNWindow  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to wrap a specific window object in the ui file
# ------------------------------------------------------------------------------
class WindowMain(CNWindow):
    """
    A class to wrap a specific window object in the ui file

    This class contains all the handler code for a specific window.
    """

    # --------------------------------------------------------------------------
    # Window control events
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
        self.show_dialog(GC.DLG_ABOUT)

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

        # create a new window
        n = str(datetime.now())

        # add the window to the app
        self._app.add_instance(f"win-{n}", self._dict_gui)

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

        # get entry text
        entry = self.get_control(GC.WIN_MAIN_ENTRY_TEST)

        # set entry text to title
        self.set_title(entry)

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

        # save size/controls
        self._update_gui()

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

        # close this window
        self.window.destroy()

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

        # save size/controls
        self._update_gui()

        # close this window
        self.window.destroy()

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

        # get the default result
        result = self._can_close()

        # maybe close window based on dialog result
        if result:

            # close this window
            self.window.destroy()


# -)
