# ------------------------------------------------------------------------------
# Project : CNAppLib                                               /          \
# Filename: cnapp.py                                              |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to manage a GTK Application with at least one window and possible
·configuration parameters

This class manages the basic functions of an application, such as activation
and (possibly) setting/getting the backing dictionary of all window
sizes/controls.
"""

# TODO: move error strings out and get rid of gettext
# TODO: quit from dock does not close all windows when one or more show
# modified dialog
# TODO: dock icon works in debugger, but not .desktop or terminal
# this is a wayland thing, see here:
# https://stackoverflow.com/questions/45162862/how-do-i-set-an-icon-for-the-whole-application-using-pygobject

# NEXT: Save/load whole dict app - simpler (need to deal with wrapper class)
# NEXT: Move size to class - new win of class uses curr size of last closed of
# same class
# NEXT: save session option
# if true, on launch, restore all windows that were visible at last quit
# if false, only show window marked as main/visible
# app section in dict_state - app saves list of visible windows at quit
# NEXT: hamburger menu in title bar or at least (i) icon for about dialog

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from datetime import datetime
import gettext
import gi

gi.require_version("Gtk", "3.0")

# pylint: disable=wrong-import-position
# pylint: disable=import-error

# my imports
from gi.repository import Gtk  # type: ignore
from cnlib import cnfunctions as CF

# pylint: enable=wrong-import-position
# pylint: enable=import-error

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Macros
# ------------------------------------------------------------------------------

_ = gettext.gettext

# ------------------------------------------------------------------------------
# Control types
# ------------------------------------------------------------------------------

KEY_CLS_CTLS = "KEY_CLS_CTLS"
KEY_WIN_VISIBLE = "KEY_WIN_VISIBLE"
KEY_WIN_SIZE = "KEY_WIN_SIZE"
KEY_SIZE_W = "KEY_SIZE_W"
KEY_SIZE_H = "KEY_SIZE_H"
KEY_SIZE_M = "KEY_SIZE_M"
KEY_WIN_CTLS = "KEY_WIN_CTLS"

# NB: add new control types here
# used to collate set/get functions and value types
# NB: value type defaults to text, no conversion
# if value type should be int or bool, set KEY_CTL_VAL_TYPE accordingly
# this key/value is used by _sanitize_user to ensure proper type, in case
# somebody borks the entry in the config file by hand

# # window control keys
KEY_CTL_TYPE = "KEY_CTL_TYPE"
KEY_CTL_VAL = "KEY_CTL_VAL"
KEY_CTL_SET = "KEY_CTL_SET"
KEY_CTL_GET = "KEY_CTL_GET"
KEY_CTL_VAL_TYPE = "KEY_CTL_VAL_TYPE"
KEY_CTL_ACT = "KEY_CTL_ACT"

# value types to convert in _sanitize_user
CTL_VAL_TYPE_INT = "CTL_VAL_TYPE_INT"
CTL_VAL_TYPE_BOOL = "CTL_VAL_TYPE_BOOL"

# all text entries use the same set/get functions
CTL_TYPE_TEXT = {
    KEY_CTL_SET: "set_text",
    KEY_CTL_GET: "get_text",
    KEY_CTL_ACT: "do_text",
}

# all checkboxes use the same set/get functions and value type
CTL_TYPE_CHECK = {
    KEY_CTL_SET: "set_active",
    KEY_CTL_GET: "get_active",
    KEY_CTL_VAL_TYPE: CTL_VAL_TYPE_BOOL,
    KEY_CTL_ACT: "do_check",
}

# ------------------------------------------------------------------------------
# Defaults
# ------------------------------------------------------------------------------

# DEF_CLOSE_ACTION = CLOSE_ACTION_ASK
# DEF_CLS_SHOW_MOD = True
# DEF_CLS_MOD_CHAR = "\u29BF"
# DEF_CLS_MOD_FMT = "${MOD} ${TITLE}"
# DEF_WIN_VISIBLE = True
# DEF_WIN_RESTORE = False
# DEF_APP_RESTORE = False

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# strings to be localized
# I18N: the main message of the save dialog
STR_CLOSE_DLG_MAIN = _("Save changes before closing?")
# I18N: the sub message of the save dialog
STR_CLOSE_DLG_SEC = _("If you don't save, changes will be permanently lost.")
# I18N: the destructive button label (to close without saving)
STR_CLOSE_DLG_CLOSE = _("Close without saving")
# I18N: the cancel button label (to do nothing)
STR_CLOSE_DLG_CANCEL = _("Cancel")
# I18N: the save button label (to save and close)
STR_CLOSE_DLG_SAVE = _("Save")
# I18N: the save button label when the document is untitled (to save and close)
STR_CLOSE_DLG_SAVE_AS = _("Save As...")

# ------------------------------------------------------------------------------
# Error strings
# ------------------------------------------------------------------------------

ERR_DICT_APP = _("no dict_app or dict_app is empty")
ERR_NO_CLASS = _("no classes in dict_app")
ERR_NO_WIN = _("no windows in dict_app")
ERR_WIN_EXIST = _("window name already exists")
# ERR_CLASS_NONE = _("class is None")

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A subclass of Gtk.Application to suit our needs
# ------------------------------------------------------------------------------
class CNApp(Gtk.Application):
    """
    A subclass of Gtk.Application to suit our needs

    Public methods:
        add_instance: Add a new window instance with the specified name and
        class
        remove_instance: Remove the specified window instance from the internal
        list
        get_instances: Return the list of existing instances
        set_dict_state: Update the backing dict of all window, setting their size
        and control values
        get_dict_state: Return the backing dict of all windows, containing their
        size and control values
        # format unique name for window
        now = datetime.now()
        name_win = now.strftime("%d-%m-%Y_%H-%M-%S")
        # check if the name exists in the known window list
        # if name_win in self._dict_inst:
        #     # window name already exists
        #     raise IOError(AC.ERR_WIN_EXIST)


    A class that extends Gtk.Application to manage the GUI for the calling
    Python script.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, app_id, path_state=None, def_class=None):
        """
        Initialize the new object

        Arguments:
            app_id: The reverse-notation id of the app (ie.
            "org.cyclopticnerve.foobar)
            dict_app: The list of app properties for the Application
                Keys and values are explained in the main file's DICT_APP
                declaration
            dict_state: The dict of properties that were saved upon last close
            of the app, or loaded upon next open
                Keys and values are a combination of each window's size and
                control values from the defaults in the ui file and this dict
            dict_cfg: THe dictionary parsed from the command line cfg option

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # ----------------------------------------------------------------------
        # dict_app

        # no app dict, kaboom
        # if dict_app is None or len(dict_app) == 0:
        #     # no dict or dict is empty
        #     raise IOError(AC.ERR_DICT_APP)

        # if no classes in dict_app
        # NB: dict_app needs to contain KEY_APP_CLASSES with at least one entry
        # if (
        #     AC.KEY_APP_CLASSES not in dict_app
        #     or len(dict_app[AC.KEY_APP_CLASSES]) == 0
        # ):
        #     # no classes in dict_app
        #     raise IOError(AC.ERR_NO_CLASS)

        # if no windows in dict_app
        # NB: dict_app needs to contain KEY_APP_WINDOWS with at least one entry
        # if (
        #     AC.KEY_APP_WINDOWS not in dict_app
        #     or len(dict_app[AC.KEY_APP_WINDOWS]) == 0
        # ):
        #     # no windows in dict_app
        #     raise IOError(AC.ERR_NO_WIN)

        # # set internal dict_app
        # self._dict_app = dict_app

        # ----------------------------------------------------------------------
        # dict_state

        # # set gui dict to default so we can query it
        # # NB: we need this to be SOMETHING b/c we try to combine
        # dict_app_windows = self._dict_app.get(AC.KEY_APP_WINDOWS, {})
        # if dict_state is None:
        #     dict_state = {}

        # # combine ui settings and gui settings
        # self._dict_state = CF.combine_dicts(dict_app_windows, [dict_state])

        # we need this later to save session state
        self._path_state = path_state

        # set gui dict to default so we can query it
        # NB: we need this to be SOMETHING b/c we try to combine
        # dict_app_windows = self._dict_app[AC.KEY_APP_WINDOWS]
        self._dict_state = {}

        # load state
        if path_state is not None:
            self._dict_state = CF.load_dicts([self._path_state], {})

        # ----------------------------------------------------------------------
        # def_class

        # save def_class for _activate
        self._def_class = def_class

        # ----------------------------------------------------------------------
        # dict_inst

        # create the default list of known windows (items are window instances)
        # NEXT: remove for templates
        self._dict_inst = {}

        # ------------------------------------------------------------------------------

        # call super init to initialize the base class
        super().__init__(application_id=app_id)

        # TODO: what does this do? do we need it? if we do, pass app name as
        # param (don't use replacement value b/c this file doesn't get scanned
        # by pyplate)
        # some useless shit i found on the interwebs (doesn't do anything)
        # GLib.set_prgname("__PC_NAME_BIG__")
        # GLib.set_application_name("__PC_NAME_BIG__")

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
    def add_new_window(self, class_win):
        """
        Add a new window instance with the specified name and class

        Arguments:
            name_win: The unique name to store in the backing dict
            dict_win: The dict of properties, such as size and control values,
                for the new window

        Adds a new instance with a unique name and class type to put in the
        backing store.
        """

        # minimum dict_win must contain:
        # C.KEY_WIN_CLASS,
        # class_win = dict_win.get(AC.KEY_WIN_CLASS, None)
        # if class_win is None:
        #     # class is None
        #     raise IOError(ERR_CLASS_NONE)

        # format unique name for window
        now = datetime.now()
        name_win = now.strftime("%d-%m-%Y_%H-%M-%S")
        # check if the name exists in the known window list
        # if name_win in self._dict_inst:
        #     # window name already exists
        #     raise IOError(AC.ERR_WIN_EXIST)

        # # get the app dict for the class
        # dict_classes = self._dict_app[AC.KEY_APP_CLASSES]
        # dict_class = dict_classes[class_win]

        # get window's handler class
        # handler = dict_class[AC.KEY_CLS_HANDLER]  # WindowMain

        # create the window instance
        # dict_state = self._dict_state.get(name_win, {})
        inst_win = class_win(self, name_win, {})

        # add the Window to the app
        super().add_window(inst_win.window)
        self._dict_inst[name_win] = inst_win

        # return the new instance
        return inst_win

        # if the window should be visible, show it
        # vis_win = dict_state.get(KEY_WIN_VISIBLE, DEF_WIN_VISIBLE)
        # if vis_win:
        #     inst_win.window.present()

    # --------------------------------------------------------------------------
    # Add a new window instance with the specified name and class
    # --------------------------------------------------------------------------
    def add_existing_window(self, class_win, name_win):
        """
        Add a new window instance with the specified name and class

        Arguments:
            name_win: The unique name to store in the backing dict
            dict_win: The dict of properties, such as size and control values,
                for the new window

        Adds a new instance with a unique name and class type to put in the
        backing store.
        """

        # minimum dict_win must contain:
        # C.KEY_WIN_CLASS,
        # class_win = dict_win.get(AC.KEY_WIN_CLASS, None)
        # if class_win is None:
        #     # class is None
        #     raise IOError(ERR_CLASS_NONE)

        # format unique name for window
        # now = datetime.now()
        # name_win = now.strftime("%d-%m-%Y_%H-%M-%S")
        # check if the name exists in the known window list
        # if name_win in self._dict_inst:
        #     # window name already exists
        #     raise IOError(AC.ERR_WIN_EXIST)

        # # get the app dict for the class
        # dict_classes = self._dict_app[AC.KEY_APP_CLASSES]
        # dict_class = dict_classes[class_win]

        # get window's handler class
        # handler = dict_class[AC.KEY_CLS_HANDLER]  # WindowMain

        dict_state = self._dict_state[name_win]

        # create the window instance
        # dict_state = self._dict_state.get(name_win, {})
        inst_win = class_win(self, name_win, dict_state)

        # add the Window to the app
        super().add_window(inst_win.window)
        self._dict_inst[name_win] = inst_win

        # return the new instance
        return inst_win

        # if the window should be visible, show it
        # vis_win = dict_state.get(KEY_WIN_VISIBLE, DEF_WIN_VISIBLE)
        # if vis_win:
        #     inst_win.window.present()

    # --------------------------------------------------------------------------
    # Remove the specified window instance from the internal list
    # --------------------------------------------------------------------------
    def remove_window(self, name_win):  # pylint: disable=arguments-differ
        """
        Remove the specified window instance from the internal list

        Arguments:
            name_win: The name of the window instance to remove

        Removes a window instance from the internal list. Note that this does
        not destroy the window, and this method should in fact be called from
        the actual Gtk.Window object's destroy method.
        """

        # remove instance from list
        if name_win in self._dict_inst:
            inst = self._dict_inst[name_win]
            super().remove_window(inst.window)
            self._dict_inst.pop(name_win)
            # del self._dict_inst[name_win]

    # --------------------------------------------------------------------------
    # Return the list of existing window instances
    # --------------------------------------------------------------------------
    def get_windows(self, _app):  # pylint: disable=arguments-differ
        """
        Return the list of existing window instances

        Returns:
            The dict of existing window instances

        A convenience method to return the list of existing window instances.
        """

        # NB: why is app a param for this func in super? weird...

        # return the list
        return self._dict_inst

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

        # restore all windows from prev session
        print("activate")
        # print("cnapp restore session:", C_RESTORE_SESSION)
        # print("cnapp restore session:", self._restore_session)

        # no restore or no file - add default window
        if self._path_state is None or len(self._dict_state) == 0:
            self.add_new_window(self._def_class)
            return

        # add all known windows to app's window list
        # for name_win, class_win in self._dict_state.items():
        #     self.add_instance(name_win, class_win)
        # TODO: apply dict state
        for _k, v in self._dict_state.items():
            self.add_existing_window(v.class_name, v.name_win)

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
        print("cnapp save session:", self._path_state)

        # FIXME: loop through all windows and build state dict
        dict_state = {}
        for k, v in self._dict_inst.items():
            dict_state[k] = v.get_state()
            v.window.delete()

        CF.save_dict([self._path_state], dict_state)
        # destroy any windows left in the list
        # for key, value in self._dict_inst.items():

        #     # remove it from the list
        #     # del self._dict_inst[key]

        #     # send it the destroy message
        #     value.delete()


# -)
