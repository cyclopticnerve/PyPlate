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

# NEXT: Save/load whole dict app - simpler (need to deal with wrapper class)
# NEXT: Move size to class - new win of class uses curr size of last closed of
# same class
# NEXT: save session option
# if true, on launch, restore all windows that were visible at last quit
# if false, only show window marked as main/visible
# app section in dict_gui - app saves list of visible windows at quit
# NEXT: hamburger menu in title bar or at least (i) icon for about dialog

# TODO: quit from dock does not close all windows when one or more show
# modified dialog
# TODO: dock icon works in debugger, but not .desktop or terminal
# this is a wayland thing, see here:
# https://stackoverflow.com/questions/45162862/how-do-i-set-an-icon-for-the-whole-application-using-pygobject

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import gi

# pylint: disable=wrong-import-position

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # type: ignore

# pylint: enable=wrong-import-position

# pylint: disable=import-error

# my imports
from cnlib import cnfunctions as CF
from . import cnappconstants as AC

# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Macros
# ------------------------------------------------------------------------------

_ = gettext.gettext

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A subclass of Gtk.Application to suit our needs
# -----------------------------------------------------------------------------
class CNApp(Gtk.Application):
    """
    A subclass of Gtk.Application to suit our needs

    Public properties:
        dict_cfg: the config dict passed from the main script

    Public methods:
        add_instance: Add a new window instance with the specified name and
        class
        remove_instance: Remove the specified window instance from the internal
        list
        get_instances: Return the list of existing instances
        set_dict_gui: Update the backing dict of all window, setting their size
        and control values
        get_dict_gui: Return the backing dict of all windows, containing their
        size and control values

    A class that extends Gtk.Application to manage the GUI for the calling
    Python script.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, app_id, dict_app, dict_gui=None, dict_cfg=None):
        """
        Initialize the new object

        Arguments:
            app_id: The reverse-notation id of the app (ie.
            "org.cyclopticnerve.foobar)
            dict_app: The list of app properties for the Application
                Keys and values are explained in the main file's DICT_APP
                declaration
            dict_gui: The dict of properties that were saved upon last close
            of the app, or loaded upon next open
                Keys and values are a combination of each window's size and
                control values from the defaults in the ui file and this dict
            dict_cfg: THe dictionary parsed from the command line cfg option

        Methods:
            add_instance: Add a new window instance with the specified name and
            class
            remove_instance: Remove the specified window instance from the
            internal list
            get_instance: Returns a specific window instance by name
            get_instances: Return the list of existing window instances
            get_dict_gui: Return the backing dict of all windows,
            containing their size and control values

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # ----------------------------------------------------------------------
        # app id

        if not app_id:
            # I18N: no app_id or app_id is empty
            raise IOError(_("no app_id or app_id is empty"))

        # ----------------------------------------------------------------------
        # dict_app

        # no app dict, kaboom
        if dict_app is None or len(dict_app) == 0:
            # I18N: no dict or dict is empty
            raise IOError(_("no dict_app or dict_app is empty"))

        # if no classes in dict_app
        # NB: dict_app needs to contain KEY_APP_CLASSES with at least one entry
        if (
            AC.KEY_APP_CLASSES not in dict_app
            or len(dict_app[AC.KEY_APP_CLASSES]) == 0
        ):
            # I18N: no classes in dict_app
            raise IOError(_("no classes in dict_app"))

        # if no windows in dict_app
        # NB: dict_app needs to contain KEY_APP_WINDOWS with at least one entry
        if (
            AC.KEY_APP_WINDOWS not in dict_app
            or len(dict_app[AC.KEY_APP_WINDOWS]) == 0
        ):
            # I18N: no windows in dict_app
            raise IOError(_("no windows in dict_app"))

        # set internal dict_app
        self._dict_app = dict_app

        # call super init to initialize the base class
        super().__init__(application_id=app_id)

        # TODO: what does this do? do we need it? if we do, pass app name as
        # param (don't use replacement value b/c this file doesn't get scanned
        # by pyplate)
        # some useless shit i found on the interwebs (doesn't do anything)
        # GLib.set_prgname("__PC_NAME_BIG__")
        # GLib.set_application_name("__PC_NAME_BIG__")

        # ----------------------------------------------------------------------
        # dict_gui

        # set gui dict to default so we can query it
        # NB: we need this to be SOMETHING b/c we try to combine
        dict_app_windows = self._dict_app.get(AC.KEY_APP_WINDOWS, {})

        # combine ui settings and gui settings
        self._dict_gui = CF.combine_dicts(dict_app_windows, dict_gui)

        # ----------------------------------------------------------------------
        # dict_cfg

        # set gui dict param to something
        if dict_cfg is None:
            dict_cfg = {}
        self._dict_cfg = dict_cfg

        # ----------------------------------------------------------------------
        # dict_inst

        # create the default list of known windows (items are window instances)
        # NEXT: remove for templates
        self._dict_inst = {}

        # ----------------------------------------------------------------------
        # connections

        # connect default operations for a new application
        self.connect("activate", self._activate)
        self.connect("shutdown", self._shutdown)

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Add a new window instance with the specified name and class
    # --------------------------------------------------------------------------
    def add_instance(self, name_win, dict_win):
        """
        Add a new window instance with the specified name and class

        Arguments:
            name_win: The unique name to store in the backing dict
            dict_win: The dict of properties, such as size and control values,
                for the new window

        Adds a new instance with a unique name and class type to put in the
        backing store.
        """

        # check if the name exists in the known window list
        if name_win in self._dict_inst:
            # I18N: window name already exists
            raise IOError(_("window name already exists"))

        # minimum dict_win must contain:
        # C.KEY_WIN_CLASS,
        class_win = dict_win.get(AC.KEY_WIN_CLASS, None)
        if class_win is None:
            # I18N: class is None
            raise IOError(_("class is None"))

        # # get the app dict for the class
        dict_classes = self._dict_app[AC.KEY_APP_CLASSES]
        dict_class = dict_classes[class_win]

        # get window's handler class
        handler = dict_class[AC.KEY_CLS_HANDLER]  # WindowMain

        # create the window instance
        inst = handler(self, name_win, dict_win)

        # add the Window to the app
        self.add_window(inst.window)
        self._dict_inst[name_win] = inst

        # if the window should be visible, show it
        vis_win = dict_win.get(AC.KEY_WIN_VISIBLE, AC.DEF_WIN_VISIBLE)
        if vis_win:
            inst.window.present()

    # --------------------------------------------------------------------------
    # Remove the specified window instance from the internal list
    # --------------------------------------------------------------------------
    def remove_instance(self, name_win):
        """
        Remove the specified window instance from the internal list

        Arguments:
            name_win: The name of the window instance to remove

        Removes a window instance from the internal list. Note that this does
        not destroy the window, and this method should in fact be called from
        the actual Gtk.Window object's destroy method.
        """

        # remove instance from list
        del self._dict_inst[name_win]

    # --------------------------------------------------------------------------
    # Returns a specific window instance by name
    # --------------------------------------------------------------------------
    def get_instance(self, name_win):
        """
        Returns a specific window instance by name

        Returns:
            The specific window instance

        A convenience method to return the specific window instance.

        """

        # return the instance
        return self._dict_inst[name_win]

    # --------------------------------------------------------------------------
    # Return the list of existing window instances
    # --------------------------------------------------------------------------
    def get_instances(self):
        """
        Return the list of existing window instances

        Returns:
            The list of existing window instances

        A convenience method to return the list of existing window instances.

        """

        # return the list
        return self._dict_inst

    # --------------------------------------------------------------------------
    # Update the backing dict of a particular window, setting its size and
    # control values
    # --------------------------------------------------------------------------
    def set_dict_gui(self, name_win, dict_gui):
        """
        Update the backing dict of a particular window, saving its size and
        control values

        Arguments:
            name_win: The name of the window to save the GUI for
            dict_gui: The current state of the window's GUI, to be saved in
            the global backing store

        This method updates the backing store for a particular window whenever
        that window's values change (such as size or control values).

        This method should NOT be called by any outside script. It is public
        only so it can be used by Window and its subclasses.

        The contents of this dict are a reflection of the CURRENT VALUES of the
        GUI, after any changes have been made. This method is called by the
        window's _do_update method.
        """

        # set the gui dict for the window name
        self._dict_gui[name_win] = dict_gui

    # --------------------------------------------------------------------------
    # Return the backing dict of all windows, containing their size and
    # control values
    # --------------------------------------------------------------------------
    def get_dict_gui(self):
        """
        Return the backing dict of all windows, containing their size and
        control values

        Returns:
            The current backing dictionary

        This method should be called after run(), so that the dict is updated
        after any save actions have been completed.

        The contents of this dict are a reflection of the CURRENT VALUES of the
        GUI, after any changes have been made. The dict is updated by
        set_dict_gui.

        The dictionary does NOT contain settings like window class, close
        action, etc. since these do not need to be saved between sessions.
        """

        # return the backing gui dict
        return self._dict_gui

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the Application is activated (ie. first window is shown)
    # --------------------------------------------------------------------------
    def _activate(self, _obj):
        """
        Called when the Application is activated (ie. first window is shown)

        Arguments:
            _obj: Not used

        The Application is about to start. Show all default windows and
        possibly all windows that were open during last session.
        """

        # add all known windows to app's window list
        for name_win, dict_win in self._dict_gui.items():
            self.add_instance(name_win, dict_win)

    # --------------------------------------------------------------------------
    # Called when the Application is stopped (ie. last window is closed, dock
    # menu quit, top bar quit, etc.)
    # --------------------------------------------------------------------------
    def _shutdown(self, _obj):
        """
        Called when the Application is stopped (ie. last window is closed, dock
        menu quit, top bar quit, etc.)

        Arguments:
            _obj: Not used


        This method removes any windows left in the list when tha application
        quits.
        """

        # TODO: what to do with this?
        print("shutdown")
        # destroy any windows left in the list
        # for key, value in self._dict_inst.items():

        #     # remove it from the list
        #     # del self._dict_inst[key]

        #     # send it the destroy message
        #     value.delete()


# -)
