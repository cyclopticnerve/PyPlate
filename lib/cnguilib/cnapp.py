# ------------------------------------------------------------------------------
# Project : CNAppLib                                               /          \
# Filename: cnapp.py                                              |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to manage a GTK Application with at least one window and possible
configuration parameters

This class manages the basic functions of an application, such as activation
and (possibly) setting/getting the backing dictionary of all window
sizes/controls.
"""

# FIXME: quit from dock does not close all windows when one or more show
# modified dialog
# FIXME: dock icon works in debugger, but not .desktop or terminal
# this is a wayland thing, see here:
# https://stackoverflow.com/questions/45162862/how-do-i-set-an-icon-for-the-whole-application-using-pygobject

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import copy
from pathlib import Path
import sys

# find paths to lib
# NB: this assumes cnlib is a "sister" folder to cnapplib
P_DIR_LIB = Path(__file__).parents[1].resolve()

# add paths to import search
sys.path.append(str(P_DIR_LIB))

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
# Strings
# ------------------------------------------------------------------------------

S_ERR_WIN_EXIST = "window name exists"
S_ERR_WIN_NOT_EXIST = "window name does not exist"

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A subclass of Gtk.Application to suit our needs
# ------------------------------------------------------------------------------
class CNApp(Gtk.Application):
    """
    A subclass of Gtk.Application to suit our needs

    Properties:
        i18n_domain: the domain name for i18n (usually the value of
        "__PP_NAME_SMALL__")

    Methods:
        add_window: Add a new window instance
        remove_window: Remove a window instance from the internal list
        get_windows: Return the read-only list of currently visible windows
        get_active_window: Return the CNWindow subclass instance for the active
        window (the currently focused window)
        show_dialog: Show a dialog relative to the App (no parent) or a
        specified window

    A class that extends Gtk.Application to manage the GUI for the calling
    Python script.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, app_id, i18n_domain):
        """
        Initialize the new object

        Args:
            app_id: The reverse dot notation id of the app (ie.
            "org.cyclopticnerve.foobar")
            i18n_domain: the domain name for i18n (usually the value of
            "__PP_NAME_SMALL__")

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # ----------------------------------------------------------------------
        # super

        # call super init to initialize the base class
        super().__init__(application_id=app_id)

        # ----------------------------------------------------------------------
        # set properties

        # NB: this is prop'd and public for window classes to use as i18n
        # domain (window subclasses are where the i18n stuff is done)
        self.i18n_domain = i18n_domain

        # create the default list of known windows (keys are window names,
        # values are window instances)
        self._dict_instances = {}

        # ----------------------------------------------------------------------
        # connections

        # connect default operations for a new application
        # NB: NOT STRINGS!!! DO NOT DUMB!!!
        self.connect("activate", self._evt_app_activate)
        self.connect("shutdown", self._evt_app_shutdown)

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Add a new window instance with the specified name
    # --------------------------------------------------------------------------
    def add_window(
        self, name_win, inst_win
    ):  # pylint: disable=arguments-differ
        """
        Add a new window instance with the specified name

        Args:
            name_win: The unique name to store in the instance dict
            inst_win: The CNWindow subclass instance

        Adds a new instance of the CNWindow subclass with the specified name
        and puts it in the instance list. Note that this does not automatically
        make the window visible, you must still call present() on the Gtk
        window object.
        """

        # NB: adding the actual Gtk window object to the super Application
        # object is deferred until _evt_app_activate, since that is when it
        # SHOULD happen in a real Gtk program. we do it this way so the
        # subclass only has to override __init__ and can add windows there,
        # before the app is actually activated

        # sanity check
        if name_win in self._dict_instances:
            print(S_ERR_WIN_EXIST)
            return

        # add to internal list
        self._dict_instances[name_win] = inst_win

    # --------------------------------------------------------------------------
    # Remove the specified window instance from the internal list
    # --------------------------------------------------------------------------
    def remove_window(self, name_win):  # pylint: disable=arguments-differ
        """
        Remove the specified window instance from the internal list

        Args:
            name_win: The name of the window instance to remove

        Removes a window instance from the internal list. Note that this does
        not destroy the Gtk.Window, and this method should in fact not be
        called directly, but be called from the actual Gtk.Window object's
        destroy method handler.
        """

        # sanity check
        if not name_win in self._dict_instances:
            print(S_ERR_WIN_NOT_EXIST)
            return

        # get handler
        inst_win = self._dict_instances[name_win]

        # remove from super and us
        super().remove_window(inst_win.window)
        self._dict_instances.pop(name_win)

    # --------------------------------------------------------------------------
    # Return the list of currently displayed windows
    # --------------------------------------------------------------------------
    def get_windows(self):  # pylint: disable=arguments-differ
        """
        Return the list of currently displayed windows

        Returns:
            The list of currently displayed windows

        Returns the list of currently displayed windows. This method returns a
        deep copy of the dict and thus read-only.
        """

        # return the (read-only?) dict
        return copy.deepcopy(self._dict_instances)

    # --------------------------------------------------------------------------
    # Return a tuple of the CNWindow subclass name and instance for the active
    # window (the currently focused window)
    # --------------------------------------------------------------------------
    def get_active_window(self):  # pylint: disable=arguments-differ
        """
        Return a tuple of the CNWindow subclass name and instance for the
        active window (the currently focused window)

        Returns:
            A tuple of the CNWindow subclass name and instance for the active
            window

        Finds and returns a tuple of the CNWindow subclass name and instance
        for the currently focused Gtk.(Application)Window, or None if there is
        no active window or it is not in the internal list.
        """

        # ask GTK.Application for active window
        active_win = super().get_active_window()

        # loop until we find handler for active window
        for name, handler in self._dict_instances.items():
            if handler.window == active_win:
                return (name, handler)

        # cant find window, return none
        return None

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
        dlg_builder.set_translation_domain(self.i18n_domain)

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

        The Application is about to start. Any windows in self._dict_instances will
        be added to the parent Application object and presented.
        """

        # for each window added by add_window
        for _k, v in self._dict_instances.items():

            # add it to super (must be done AFTER activation)
            super().add_window(v.window)

            # show the window
            v.window.present()

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
        # pass

# -)
