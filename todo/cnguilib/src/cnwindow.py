# ------------------------------------------------------------------------------
# Project : CNGuiLib                                               /          \
# Filename: cnwindow.py                                           |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to manage a GTK Window

This class handles common stuff like setting/getting the window state,
resizing, handling the close event (ie. the 'X' button) and changing the title
if any controls are modified.
Remember to connect all the appropriate window events in your ui file to the
private methods declared here.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path
import sys

# find paths to lib
# NB: this assumes cnlib is a "sister" folder to cnapplib
DIR_CNLIB = Path(__file__).parents[1].resolve()

# add paths to import search
# sys.path.append(str(DIR_CNLIB))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
import gi  # type: ignore
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to wrap Gtk.(Application)Window objects in the ui file
# ------------------------------------------------------------------------------
class CNWindow:
    """
    A class to wrap Gtk.(Application)Window objects in the ui file

    Properties:
        name: The name of the window in the CNApp's instance list
        window: The window object from the UI file

    This class contains all the handler code for a typical window.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    S_ACTION_DELETE_EVENT = "delete-event"
    S_ACTION_DESTROY = "destroy"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, app, name_win, ui_file, ui_name):
        """
        Initialize the new object

        Args:
            app: The calling Application object
            name_win: The name of the window in the CNApp's instance list
            ui_file: The ui file that contains the window for this class
            ui_name: The name of the window object in the ui_file

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # ----------------------------------------------------------------------
        # props

        # private props
        # NB: used for i18n in show_dialog, and _evt_win_destroy
        self._app = app

        # public props
        self.name_win = name_win

        # ----------------------------------------------------------------------
        # ui_file/ui_name

        # create the builder
        self._builder = Gtk.Builder()

        # set the builder to point to domain
        self._builder.set_translation_domain(self._app.i18n_domain)

        # get class's ui file and add to builder
        # NB: cast in case it is a Path object
        ui_path = Path(ui_file).resolve()
        self._builder.add_from_file(str(ui_path))

        # get the main window object from the ui file
        # NB: public because we need it in app._app_evt_activate
        self.window = self._builder.get_object(ui_name)

        # ----------------------------------------------------------------------
        # connections

        # connect default operations for a new window
        # NB: NOT STRINGS!!! DO NOT DUMB!!!
        self.window.connect(self.S_ACTION_DELETE_EVENT, self._evt_win_delete)
        self.window.connect(self.S_ACTION_DESTROY, self._evt_win_destroy)

        # connect all subclass methods
        self._builder.connect_signals(self)  # pylint: disable=no-member

    # --------------------------------------------------------------------------
    # Window events
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

        print(f"{self.name_win}: _evt_win_delete")

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

        print(f"{self.name_win}: _evt_win_destroy")

        # remove the window from app list
        self._app.remove_window(self.name_win)


# -)
