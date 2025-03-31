# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename:                                                       |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
A class to manage a specific window (or type of window).

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

# my imports
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # pylint: disable=wrong-import-position # type: ignore

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

    # find path to self and ui file
    P_DIR_PRJ = Path(__file__).parents[3].resolve()

    # get paths to ui files
    P_FILE_WIN = P_DIR_PRJ / "__PP_DIR_UI__/__PP_FILE_WIN__.ui"
    P_FILE_DLG = P_DIR_PRJ / "__PP_DIR_UI__/__PP_DLG_FILE__.ui"

    # the name of the window in the ui file
    S_UI_WIN_NAME = "__PP_CLASS_WIN__"
    S_UI_ABT_NAME = "__PP_DLG_ABOUT__"

    # window actions
    S_ACTION_DELETE_EVENT = "delete-event"

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

        # create a builder and set i18n domain
        self.builder = Gtk.Builder()
        self.builder.set_translation_domain(self._app._i18n_domain)

        # load file and get window
        self.builder.add_from_file(str(self.P_FILE_WIN))
        self.window = self.builder.get_object(self.S_UI_WIN_NAME)

        # connect all control signals
        self.builder.connect_signals(self)  # pylint: disable=no-member

        # connect window signals
        self.window.connect(self.S_ACTION_DELETE_EVENT, self._evt_win_delete)

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

        # use app object to show dialog
        self._app.show_dialog(self.P_FILE_DLG, self.S_UI_ABT_NAME)

    # --------------------------------------------------------------------------
    # Called when the Close button is clicked
    # --------------------------------------------------------------------------
    def _btn_close_clicked(self, _obj):
        """
        Called when the Close button is clicked

        Args:
            _obj: Not used

        The Close button was clicked, close the window.
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
            False to allow the window to close\n
            True to keep the window open

        The Window is about to close via the 'X' button (or some other system
        event, like closing from the overview or the dock, or the window's
        close() method).\n
        Note that this handler should return THE OPPOSITE of what you might
        expect. That is, returning False here lets the window close, while
        returning True means the window will not close.\n
        You can use this method to do any cleanup before the window closes.
        """

        # close window
        return False


# -)
