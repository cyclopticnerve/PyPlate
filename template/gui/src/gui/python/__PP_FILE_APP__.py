# ------------------------------------------------------------------------------
# Project : __PP_NAME_PRJ_BIG__                                    /          \
# Filename: __PP_FILE_APP__.py                                    |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
A class to manage a GTK Application with at least one window and possible
configuration parameters

This class manages the basic functions of an application, such as activation
and (possibly) setting/getting the backing dictionary of all window
sizes/controls.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path

# ------------------------------------------------------------------------------
# venv imports
import gi
gi.require_version("Gtk", "3.0")

# pylint: disable=wrong-import-position
# pylint: disable=no-name-in-module

from gi.repository import Gtk  # type: ignore

# pylint: enable=no-name-in-module

# ------------------------------------------------------------------------------
# local imports
from __PP_FILE_WIN__ import __PP_CLASS_WIN__

# pylint: enable=wrong-import-position

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A subclass of Gtk.Application to suit our needs
# ------------------------------------------------------------------------------
class __PP_CLASS_APP__(Gtk.Application):
    """
    A subclass of Gtk.Application to suit our needs

    Methods:
        show_dialog: Show a dialog relative to the App (no parent) or a
        specified window

    A class that extends Gtk.Application to manage the GUI for the calling
    Python script.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # find path to self
    P_DIR_PRJ = Path(__file__).parents[3].resolve()
    P_FILE_DLG = P_DIR_PRJ / "__PP_DIR_UI__/__PP_FILE_DLG__.ui"

    # gui stuff
    S_APP_ID = "org.__PP_AUTHOR__.__PP_NAME_PRJ_SMALL__"
    S_I18N_DOMAIN = "__PP_NAME_PRJ_SMALL__"
    S_UI_ABT_NAME = "__PP_DLG_ABOUT__"

    # app actions
    S_ACTION_ACTIVATE = "activate"
    S_ACTION_SHUTDOWN = "shutdown"

    # --------------------------------------------------------------------------
    # Instance methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, dict_args=None, dict_cfg=None):
        """
        Initialize the new object

        Args:
            dict_args: A dictionary of command line arguments passed to the
            application (default: None)
            dict_cfg: A json dict containing all the config for the current
            instance (default: None)

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # ----------------------------------------------------------------------
        # call super init to initialize the base class
        super().__init__(application_id=self.S_APP_ID)

        # ----------------------------------------------------------------------
        # set properties

        # set domain as prop instead of class const (win needs no ref to App)
        self._i18n_domain = self.S_I18N_DOMAIN

        # set args
        if dict_args is None:
            dict_args = {}
        self._dict_args = dict_args

        # set config
        if dict_cfg is None:
            dict_cfg = {}
        self._dict_cfg = dict_cfg

        # ----------------------------------------------------------------------
        # connections

        # connect default operations for a new application
        self.connect(self.S_ACTION_ACTIVATE, self._evt_app_activate)
        self.connect(self.S_ACTION_SHUTDOWN, self._evt_app_shutdown)

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # A convenience method for subclasses to show a dialog
    # --------------------------------------------------------------------------
    def show_dialog(self, dlg_file, dlg_name, parent=None):
        """
        A convenience method for subclasses to show a dialog

        Args:
            dlg_file: The .ui file containing the dialog
            dlg_name: The name of the dialog in the ui file
            parent: The owner of the dialog, or None if it is a global dialog
            (default: None)

        Returns:
            The result of calling run() on the dialog

        Show the named dialog and returns after it is closed. This is mostly to
        show the About dialog, but it can be used to show any modal dialog and
        return its result.
        """

        # NB: note that the dialog is only hidden after run, not destroyed.
        # this means you can call this method on the same dialog and it will
        # not go all !@#$%^& on you. (i never could work out the difference
        # between hide/close/destroy/remove/etc)

        # get a builder to load the dialog ui file
        dlg_builder = Gtk.Builder()

        # set the builder to point to domain
        dlg_builder.set_translation_domain(self.S_I18N_DOMAIN)

        # get class's ui file and add to builder
        # NB: cast in case it is a Path object
        dlg_path = Path(dlg_file).resolve()
        dlg_builder.add_from_file(str(dlg_path))

        # get dialog
        dialog = dlg_builder.get_object(dlg_name)

        # check for parent (none = global, some = that)
        if not parent is None:
            dialog.set_transient_for(parent)

        # run, destroy (standard for reusable modal dialogs)
        result = dialog.run()
        dialog.destroy()

        # return dialog end result
        return result

    # --------------------------------------------------------------------------
    # A convenience method for subclasses to show a dialog
    # --------------------------------------------------------------------------
    def show_about_dialog(self):
        """
        A convenience method for subclasses to show an about dialog

        Returns:
            The result of calling run() on the dialog

        Show the About dialog and returns after it is closed. The dialog should
        be named the same as self.S_UI_ABT_NAME.
        """

        # show about dialog
        dlg_file = self.P_FILE_DLG
        dlg_path = Path(dlg_file).resolve()
        self.show_dialog(dlg_path, self.S_UI_ABT_NAME)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the Application is activated
    # --------------------------------------------------------------------------
    def _evt_app_activate(self, _obj):
        """
        Called when the Application is activated

        Args:
            _obj: Not used

        The Application is about to start. Add your window instances here.
        """

        # create a python window class
        win = __PP_CLASS_WIN__(self)

        # get the gtk window instance
        gwin = win.window

        # add the gtk window instance to the app
        self.add_window(gwin)

        # show the gtk window instance
        gwin.present()

    # --------------------------------------------------------------------------
    # Called when the Application is stopped (ie. last window is closed, dock
    # menu quit, top bar quit, etc.)
    # --------------------------------------------------------------------------
    def _evt_app_shutdown(self, _obj):
        """
        Called when the Application is stopped (ie. last window is closed, dock
        menu quit, top bar quit, etc.)

        Args:
            _obj: Not used

        This method is called after all windows have been closed. It is used to
        clean up the application by saving anything app-specific.
        """

        # don't do anything special at quit, windows should handle that


# -)
