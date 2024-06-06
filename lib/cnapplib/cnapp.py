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

# TODO: quit from dock does not close all windows when one or more show
# modified dialog
# TODO: dock icon works in debugger, but not .desktop or terminal
# this is a wayland thing, see here:
# https://stackoverflow.com/questions/45162862/how-do-i-set-an-icon-for-the-whole-application-using-pygobject

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import copy
import importlib
from pathlib import Path
import sys

# find paths to lib
# NB: this assumes cnlib is a "sister" folder to cnapplib
DIR_LIB = Path(__file__).parents[1].resolve()

# add paths to import search
sys.path.append(str(DIR_LIB))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
from cnlib import cnfunctions as CF  # type: ignore
import gi  # type: ignore

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error


# dict_state = {
#     "name_win": { <== name_win/state_win
#         KEY_CLASS: "windowmain.WindowMain",  # mod_name.class_name
#         KEY_SIZE: {
#             KEY_SIZE_W: 0,
#             KEY_SIZE_H: 0,
#             KEY_SIZE_M: False,
#         },
#         KEY_CTLS: {
#             "entry_test": "a"
#         },
#     },
# }


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
        app_id: The reverse-notation id of the app (ie.
        "org.cyclopticnerve.foobar")

    Methods:
        add_window: Add a new window instance
        remove_window: Remove the window instance from the internal list
        get_windows: Return the read-only list of currently visible windows
        get_active_window: Return the CNWindow subclass instance for the active
        window (the currently focused window)

    A class that extends Gtk.Application to manage the GUI for the calling
    Python script.
    """

    # --------------------------------------------------------------------------
    # Constants
    # --------------------------------------------------------------------------

    # keys for state dict
    # size sub dict
    KEY_SIZE = "KEY_SIZE"
    KEY_SIZE_W = "KEY_SIZE_W"
    KEY_SIZE_H = "KEY_SIZE_H"
    KEY_SIZE_M = "KEY_SIZE_M"
    # class name as string
    KEY_CLASS = "KEY_CLASS"
    # controls sub dict
    KEY_CTLS = "KEY_CTLS"

    # values for CLOSE_ACTION
    # don't save values, just close
    CLOSE_ACTION_CANCEL = "CLOSE_ACTION_CANCEL"
    # always save values and close
    CLOSE_ACTION_SAVE = "CLOSE_ACTION_SAVE"
    # show dialog
    CLOSE_ACTION_ASK = "CLOSE_ACTION_ASK"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, app_id, path_state, dict_def_state):
        """
        Initialize the new object

        Arguments:
            app_id: The reverse-notation id of the app (ie.
            "org.cyclopticnerve.foobar")
            path_state: The path to the state file for loading/saving
            dit_def_state: The dict that describes the startup state of the app
            if path_state does not exist or is empty

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.\n
        The path_state property can be either a string or a Path, and can be
        relative to the subclass's location.\n
        See 'template/g/src/support/appmain.py' for an example.
        """

        # ----------------------------------------------------------------------
        # app_id

        # NB: this is prop'd and public for window classes to use as i18n domain
        # (window subclasses are where the i18n stuff is done)
        # self.app_id = app_id
        self.app_id = app_id

        # ----------------------------------------------------------------------
        # path_state

        # get absolute path of state file
        self._path_state = Path(path_state).resolve()

        # ----------------------------------------------------------------------
        # dict_state

        # save dict_def_state as current state (will be checked in _activate)
        self._dict_state = dict_def_state

        # ----------------------------------------------------------------------
        # _dict_inst

        # create the default list of known windows (items are window instances)
        self._dict_inst = {}

        # ----------------------------------------------------------------------
        # setup

        # call super init to initialize the base class
        super().__init__(application_id=self.app_id)

        # NB: some useless shit i found on the interwebs (doesn't do anything)
        GLib.set_prgname("__PC_NAME_BIG__")
        GLib.set_application_name("__PC_NAME_BIG__")

        # ----------------------------------------------------------------------
        # connections

        # connect default operations for a new application
        self.connect("activate", self._evt_app_activate)
        self.connect("shutdown", self._evt_app_shutdown)

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Add a new window instance with the specified name and class
    # --------------------------------------------------------------------------
    def add_window(
        self, class_win, name_win, state_win
    ):  # pylint: disable=arguments-differ
        """
        Add a new window instance with the specified name and class

        Arguments:
            class_win: The subclass of CNWindow to create
            name_win: The unique name to store in the backing dict
            state_win: The dict of properties, such as size and control values,
            for the new window

        Adds a new instance of the specified class with the specified name and
        state dict and puts it in the backing store.
        """

        # sanity check
        if name_win in self._dict_inst:
            print("window name exists")
            return

        # create the window instance
        inst_win = class_win(self, name_win, state_win)

        # add the window to the app
        super().add_window(inst_win.window)
        self._dict_inst[name_win] = inst_win

        # show the window
        inst_win.window.present()

    # --------------------------------------------------------------------------
    # Remove the specified window instance from the internal list
    # --------------------------------------------------------------------------
    def remove_window(self, name_win):  # pylint: disable=arguments-differ
        """
        Remove the specified window instance from the internal list

        Arguments:
            name_win: The name of the window instance to remove

        Removes a window instance from the internal list. Note that this does
        not destroy the Gtk.window, and this method should in fact be called
        from the actual Gtk.Window object's destroy method handler.
        """

        # check if name in list
        if name_win in self._dict_inst:

            # get handler
            inst = self._dict_inst[name_win]

            # call super to remove window object from Gtk.Application
            super().remove_window(inst.window)

            # and finally, remove handler from our list
            # (yes i know its a dict not a list)
            self._dict_inst.pop(name_win)

    # --------------------------------------------------------------------------
    # Return the list of currently displayed windows
    # --------------------------------------------------------------------------
    def get_windows(self):
        """
        Return the list of currently displayed windows

        Returns the list of currently displayed windows. This method makes the
        list internal and thus read-only.
        """

        # return the (read-only?) dict
        return copy.deepcopy(self._dict_inst)

    # --------------------------------------------------------------------------
    # Return the window name and handler instance for the active window (the
    # currently focused window)
    # --------------------------------------------------------------------------
    def get_active_window(self):
        """
        Return the CNWindow subclass instance for the active window (the
        currently focused window)

        Returns:
            The CNWindow subclass instance for the active window

        Finds and returns the CNWindow subclass instance for the currently
        focused Gtk.(Application)Window, or None if there is no active window
        or it is not in the internal list.
        """

        # ask GTK.Application for active window
        active_obj = super().get_active_window()

        # loop until we find handler for active window
        for _name, handler in self._dict_inst.items():
            if handler.window == active_obj:
                return handler

        # cant find window, return none
        return None

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the Application is activated (ie. first window is shown)
    # --------------------------------------------------------------------------
    def _evt_app_activate(self, _obj):
        """
        Called when the Application is activated (ie. first window is shown)

        Arguments:
            _obj: Not used

        The Application is about to start. Show default window(s) or possibly
        all windows that were open during the last session.
        """

        # get state from file
        # NB: at this point, self._dict_state is def state in init
        tmp_state = CF.load_dicts([self._path_state], {})

        # if there is a state in the file, use that
        if len(tmp_state) > 0:
            self._dict_state = tmp_state

        # loop through each window that needs to be shown
        for name_win, state_win in self._dict_state.items():

            # get class
            mod_class_name = state_win[self.KEY_CLASS].split(".")
            mod_name = mod_class_name[0]
            class_name = mod_class_name[1]
            mod = importlib.import_module(mod_name)
            class_win = getattr(mod, class_name)

            # add class instance using info from self._dict_state
            self.add_window(class_win, name_win, state_win)

    # --------------------------------------------------------------------------
    # Called when the Application is stopped (ie. last window is closed, dock
    # menu quit, top bar quit, etc.)
    # --------------------------------------------------------------------------
    def _evt_app_shutdown(self, _obj):
        """
        Called when the Application is stopped (ie. last window is closed, dock
        menu quit, top bar quit, etc.)

        Arguments:
            _obj: Not used

        This method removes any windows left in the list when tha application
        quits.
        """

        # TODO: is this called before or after windows are destroyed?
        # if before, can just call get_state on all remaining windows
        # if after, get_state must be called in each window's destroy method
        print("shutdown: ", len(self._dict_inst))

        # save _dict_state to _path_state
        CF.save_dict([self._path_state], self._dict_state)

        # TODO: is any of this needed?

        # start with a fresh dict
        # dict_state = {}

        # # loop through all existing windows
        # for k, v in self._dict_inst.items():
        #     # dict_state[k] = v.get_state()
        #     # simulate the 'X' button in window's title bar
        #     v.window.destroy()

        # CF.save_dict([self._path_state], dict_state)
        # destroy any windows left in the list
        # for key, value in self._dict_inst.items():

        #     # remove it from the list
        #     # del self._dict_inst[key]

        #     # send it the destroy message
        #     value.delete()


# -)
