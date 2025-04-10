# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_FILE_WIN__.py                                    |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
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
from pathlib import Path

# ------------------------------------------------------------------------------
# 3rd party imports

import gi

gi.require_version("Gtk", "3.0")

# pylint: disable=wrong-import-position

from gi.repository import Gtk  # type: ignore

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to wrap a specific window object in the ui file
# ------------------------------------------------------------------------------
class __PP_CLASS_WIN__(Gtk.ApplicationWindow):
    """
    A class to wrap a specific window object in the ui file

    This class contains all the handler code for a specific window and it's
    controls.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # find path to self
    P_DIR_PRJ = Path(__file__).parents[3].resolve()

    # get paths to ui files
    P_FILE_WIN = P_DIR_PRJ / "__PP_DIR_UI__/__PP_FILE_WIN__.ui"
    P_FILE_DLG = P_DIR_PRJ / "__PP_DIR_UI__/__PP_DLG_FILE__.ui"

    # the name of the window in the ui file
    S_UI_WIN_NAME = "__PP_CLASS_WIN__"
    S_UI_ABT_NAME = "__PP_DLG_ABOUT__"

    # window actions
    S_ACTION_DELETE_EVENT = "delete-event"
    S_ACTION_DESTROY = "destroy"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, app):
        """
        Initialize the new object

        Args:
            app: The calling Application object

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # set props
        self._app = app

        # props necessary tro create a basic window
        ui_file = self.P_DIR_PRJ / "__PP_DIR_UI__/__PP_FILE_WIN__.ui"
        ui_path = Path(ui_file).resolve()

        # create a builder and set i18n domain
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self._app._i18n_domain)

        # load file and get window
        self.builder.add_from_file(str(ui_path))
        self.window = self.builder.get_object("__PP_CLASS_WIN__")

        # connect all control signals
        self.builder.connect_signals(self)  # pylint: disable=no-member

        # connect window signals
        self.window.connect(self.S_ACTION_DELETE_EVENT, self._evt_win_delete)
        self.window.connect(self.S_ACTION_DESTROY, self._evt_win_destroy)

    # --------------------------------------------------------------------------
    # Control signal methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the About button is clicked
    # --------------------------------------------------------------------------
    def _btn_about_clicked(self, _obj):
        """
        Called when the About button is clicked

        Args:
            _obj: Not used

        The About button was clicked, show the About dialog.
        """

        # get dialog, run, hide (standard for reusable modal dialogs)
        # NB: no ext (will find .ui, .glade, .xml...)
        dlg_file = self.P_DIR_PRJ / "__PP_DIR_UI__" / "__PP_DLG_FILE__.ui"
        dlg_path = Path(dlg_file).resolve()
        self._app.show_dialog(dlg_path, "__PP_DLG_ABOUT__")

    # --------------------------------------------------------------------------
    # Called when the New button is clicked
    # --------------------------------------------------------------------------
    def _btn_new_clicked(self, _obj):
        """
        Called when the New button is clicked

        Args:
            _obj: Not used

        The New button was clicked, add the new window.
        """

        print("btn_new: not implemented")

    # --------------------------------------------------------------------------
    # Called when the Title button is clicked
    # --------------------------------------------------------------------------
    def _btn_title_clicked(self, _obj):
        """
        Called when the Title button is clicked

        Args:
            _obj: Not used

        The Title button was clicked, change the window title.
        """

        print("btn_title: not implemented")

    # --------------------------------------------------------------------------
    # Called when the Save button is clicked
    # --------------------------------------------------------------------------
    def _btn_save_clicked(self, _obj):
        """
        Called when the Save button is clicked

        Args:
            _obj: Not used

        The Save button was clicked.
        """

        print("btn_save: not implemented")

    # --------------------------------------------------------------------------
    # Called when the Cancel button is clicked
    # --------------------------------------------------------------------------
    def _btn_cancel_clicked(self, _obj):
        """
        Called when the Cancel button is clicked

        Args:
            _obj: Not used

        The Cancel button was clicked.
        """

        print("btn_cancel: not implemented")

    # --------------------------------------------------------------------------
    # Called when the OK button is clicked
    # --------------------------------------------------------------------------
    def _btn_ok_clicked(self, _obj):
        """
        Called when the OK button is clicked

        Args:
            _obj: Not used

        The OK button was clicked.
        """

        print("btn_ok: not implemented")

    # --------------------------------------------------------------------------
    # Called when the Close button is clicked
    # --------------------------------------------------------------------------
    def _btn_close_clicked(self, _obj):
        """
        Called when the Close button is clicked

        Args:
            _obj: Not used

        The Close button was clicked.
        """

        # close the window as if by the 'X' button
        self.window.close()

    # --------------------------------------------------------------------------
    # Window signal methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the main window is closed by the 'X' button
    # --------------------------------------------------------------------------
    def _evt_win_delete(self, _obj, _event):
        """
        Called when the main window is closed by the 'X' button

        Args:
            _obj: Not used
            _event: Not used

        Returns:
            False to allow the window to close
            True to keep the window open

        The Window is about to close via the 'X' button (or some other system
        event, like closing from the overview or the dock). Note that this
        handler expects to return THE OPPOSITE of the _can_close method's
        result. That is, returning False here lets the window close, while
        returning True means the window will not close. This is easy to work
        around since _can_close returns a boolean value.
        """

        print("_evt_win_delete")

        # close window
        return False

    # --------------------------------------------------------------------------
    # Called after the window is destroyed
    # --------------------------------------------------------------------------
    def _evt_win_destroy(self, _obj):
        """
        Called after the window is destroyed

        Args:
            _obj: Not used

        This method is called after the window is destroyed. It is used to
        remove the window from the app's internal list.
        """

        print("_evt_win_destroy")


# -)
