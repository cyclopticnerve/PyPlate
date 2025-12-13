# # ------------------------------------------------------------------------------
# # Project : CNAppLib                                               /          \
# # Filename: cnapp.py                                              |     ()     |
# # Date    : 03/14/2024                                            |            |
# # Author  : cyclopticnerve                                        |   \____/   |
# # License : WTFPLv2                                                \          /
# # ------------------------------------------------------------------------------

# """
# A class to manage a GTK Application with at least one window and possible
# configuration parameters

# This class manages the basic functions of an application, such as activation
# and (possibly) setting/getting the backing dictionary of all window
# sizes/controls.
# """

# # TODO: quit from dock does not close all windows when one or more show
# # modified dialog
# # TODO: dock icon works in debugger, but not .desktop or terminal
# # this is a wayland thing, see here:
# # https://stackoverflow.com/questions/45162862/how-do-i-set-an-icon-for-the-whole-application-using-pygobject

# # ------------------------------------------------------------------------------
# # Imports
# # ------------------------------------------------------------------------------

# # system imports
# import copy
# import importlib
# from pathlib import Path
# import sys

# # cnlib imports
# from cnlib import cnfunctions as CF  # type: ignore
# import gi  # type: ignore

# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk, GLib  # type: ignore

# # find paths to lib
# # NB: this assumes cnlib is a "sister" folder to cnapplib
# DIR_CNLIB = Path(__file__).parents[1].resolve()

# # add paths to import search

# # ------------------------------------------------------------------------------
# # Public classes
# # ------------------------------------------------------------------------------


# # ------------------------------------------------------------------------------
# # A subclass of Gtk.Application to suit our needs
# # ------------------------------------------------------------------------------
# class CNApp(Gtk.Application):
#     """
#     A subclass of Gtk.Application to suit our needs

#     Properties:
#         app_id: The reverse dot notation id of the app (ie.
#             "org.cyclopticnerve.foobar")

#     Methods:
#         add_window: Add a new window instance
#         remove_window: Remove a window instance from the internal list
#         get_windows: Return the read-only list of currently visible windows
#         get_active_window: Return the CNWindow subclass instance for the active
#             window (the currently focused window)

#     A class that extends Gtk.Application to manage the GUI for the calling
#     Python script.
#     """

#     # --------------------------------------------------------------------------
#     # Class constants
#     # --------------------------------------------------------------------------

#     # values for CLOSE_ACTION
#     # don't save values, just close
#     CLOSE_ACTION_CANCEL = "CLOSE_ACTION_CANCEL"
#     # always save values and close
#     CLOSE_ACTION_SAVE = "CLOSE_ACTION_SAVE"
#     # show dialog
#     CLOSE_ACTION_ASK = "CLOSE_ACTION_ASK"

#     # --------------------------------------------------------------------------
#     # Instance methods
#     # --------------------------------------------------------------------------

#     # --------------------------------------------------------------------------
#     # Initialize the new object
#     # --------------------------------------------------------------------------
#     def __init__(self, app_id, path_state, dict_def_state):
#         """
#         Initialize the new object

#         Args:
#             app_id: The reverse-notation id of the app (ie.
#             "org.cyclopticnerve.foobar")
#             path_state: The path to the state file for loading/saving
#             dit_def_state: The dict that describes the startup state of the app
#             if path_state does not exist or is empty

#         Initializes a new instance of the class, setting the default values of
#         its properties, and any other code needed to create a new object.\n
#         The path_state property can be either a string or a Path, and can be
#         relative to the subclass's location.\n
#         See 'template/g/src/support/appmain.py' for an example.
#         """

#         # ----------------------------------------------------------------------
#         # app_id

#         # NB: this is prop'd and public for window classes to use as i18n domain
#         # (window subclasses are where the i18n stuff is done)
#         # self.app_id = app_id
#         self.app_id = app_id

#         # ----------------------------------------------------------------------
#         # path_state

#         # get absolute path of state file
#         self._path_state = Path(path_state).resolve()

#         # ----------------------------------------------------------------------
#         # dict_state

#         # flag to tell if we are using state file or default
#         use_file = False

#         # assume dict_def_state as current state
#         self._dict_state = dict_def_state

#         # set all windows in def state to be visible
#         for _k, v in self._dict_state.items():
#             v[self.KEY_VISIBLE] = True

#         # get state from file
#         # NB: both path_state and dict_def_state should contain one or more
#         # windows to be shown at launch
#         # load_dicts goes through each file in the array, combining dicts with
#         # the previous result (starting with an empty dict) as it goes
#         dict_file_state = CF.load_paths_into_dict([self._path_state])

#         # if there is a state in the file, try using that
#         if len(dict_file_state) > 0:
#             # file must have at least one window marked visible
#             for _k, v in dict_file_state.items():
#                 if v[self.KEY_VISIBLE]:
#                     use_file = True

#         # we found a usable state file, go with that
#         if use_file:
#             self._dict_state = dict_file_state

#         # ----------------------------------------------------------------------
#         # _dict_inst

#         # create the default list of known windows (keys are window names,
#         # values are window instances)
#         self._dict_inst = {}

#         # ----------------------------------------------------------------------
#         # setup

#         # call super init to initialize the base class
#         super().__init__(application_id=self.app_id)

#         # NB: some useless shit i found on the interwebs (doesn't do anything)
#         # maybe for dbus?
#         GLib.set_prgname("__PP_NAME_PRJ_BIG__")
#         GLib.set_application_name("__PP_NAME_PRJ_BIG__")

#         # ----------------------------------------------------------------------
#         # connections

#         # connect default operations for a new application
#         self.connect("activate", self._evt_app_activate)
#         self.connect("shutdown", self._evt_app_shutdown)

#     # --------------------------------------------------------------------------
#     # Public methods
#     # --------------------------------------------------------------------------

#     # --------------------------------------------------------------------------
#     # Add a new window instance with the specified name and class
#     # --------------------------------------------------------------------------
#     def add_window(
#         self, class_win, name_win, state_win
#     ):  # pylint: disable=arguments-differ
#         """
#         Add a new window instance with the specified name, class, and state

#         Args:
#             class_win: The subclass of CNWindow to create, passed as a string
#             in the form of "module_name.Class_Name"
#             name_win: The unique name to store in the backing dict
#             state_win: The dict of properties, such as size and control values,
#             for the new window

#         Adds a new instance of the specified class with the specified name and
#         state and puts it in the instance list.
#         """

#         # sanity check
#         if name_win in self._dict_inst:
#             print("window name exists")
#             return

#         # this was a really hard piece of code to write, and it is U.G.L.Y. it
#         # ain't got no alibi. it's UGLY. i'm still not sure if it is the right
#         # way to do this... basically what's going on here is: to create a
#         # window, we need a "handler" class. something to handle the clicks and
#         # clacks of the gui, which is stored in a module. which is just a text
#         # file, stored on some medium (disk drive, etc.) that text file is
#         # "tangible", that is we can see and interact directly with the code.
#         # we can use that text file to create an "intangible" object (oh hey
#         # OOP!) but if we want to load/save state, we need to know the class of
#         # the object, and it's props, so we can recreate it on the next run.
#         # but here's the kicker: since we are using json to save/load the
#         # state, we can only use simple scalar types like integers, booleans,
#         # and strings (yes i know about pickle files, but that is beyond
#         # complicated, and i'm too old/stupid/lazy to get into that, uh, jar of
#         # pickles? LOL see what i did there? look ma i made a pun!) so if we
#         # can only read/write simple scalar types, the best one to use for
#         # complicated expressions is a string. so i thought the best way to
#         # refer to this intangible object in a tangible way was to store the
#         # module name and class name in a fixed way, and do it the same way
#         # Python does for imports - a filename-dot-classname.
#         # you will need to provide the path to the module, but that should
#         # already be handled by the template code, so a simple DIR_SELF /
#         # "module_name.Class_Name" should suffice.

#         # split the class name into module name / internal class name
#         mod_class_name = class_win.split(".", 1)
#         mod_name = mod_class_name[0]
#         class_name = mod_class_name[1]

#         # this is probably the part i like LEAST about this code
#         # mucking around in the Python import system gives me angina

#         # first we load the module (this is like the import statements at the
#         # top of this file, but done dynamically, so we don't need to know the
#         # module name beforehand)
#         mod = importlib.import_module(mod_name)

#         # here we use introspection (i know that's what it's called in c/c++,
#         # is that what python people call it too?) to find the class inside the
#         # module (this also feels ugly to me. i feel like you should know an
#         # object without having to say, "hey, give me all the names of your
#         # properties and methods, and i'll try to use the right one")
#         class_win_real = getattr(mod, class_name)

#         # create the window instance
#         inst_win = class_win_real(self, name_win, state_win)

#         # add the window to the app
#         super().add_window(inst_win.window)
#         self._dict_inst[name_win] = inst_win

#         # show the window
#         inst_win.window.present()

#     # --------------------------------------------------------------------------
#     # Remove the specified window instance from the internal list
#     # --------------------------------------------------------------------------
#     def remove_window(self, name_win):  # pylint: disable=arguments-differ
#         """
#         Remove the specified window instance from the internal list

#         Args:
#             name_win: The name of the window instance to remove

#         Removes a window instance from the internal list. Note that this does
#         not destroy the Gtk.window, and this method should in fact be called
#         from the actual Gtk.Window object's destroy method handler.
#         """

#         # check if name in list
#         if not name_win in self._dict_inst:
#             print("window name does not exist")
#             return

#         # get handler
#         inst = self._dict_inst[name_win]

#         # find out if this is the last window
#         count = len(self._dict_inst)
#         state = self._dict_state[name_win]
#         state[self.KEY_VISIBLE] = count == 1

#         # call super to remove window object from Gtk.Application
#         super().remove_window(inst.window)

#         # and finally, remove handler from our dict
#         self._dict_inst.pop(name_win)

#     # --------------------------------------------------------------------------
#     # Return the list of currently displayed windows
#     # --------------------------------------------------------------------------
#     def get_windows(self):
#         """
#         Return the list of currently displayed windows

#         Returns:
#             The list of currently displayed windows

#         Returns the list of currently displayed windows. This method returns a
#         deep copy of the dict and thus read-only.
#         """

#         # return the (read-only?) dict
#         return copy.deepcopy(self._dict_inst)

#     # --------------------------------------------------------------------------
#     # Return the window name and handler instance for the active window (the
#     # currently focused window)
#     # --------------------------------------------------------------------------
#     def get_active_window(self):
#         """
#         Return the CNWindow subclass instance for the active window (the
#         currently focused window)

#         Returns:
#             The CNWindow subclass instance for the active window

#         Finds and returns the CNWindow subclass instance for the currently
#         focused Gtk.(Application)Window, or None if there is no active window
#         or it is not in the internal list.
#         """

#         # ask GTK.Application for active window
#         active_win = super().get_active_window()

#         # loop until we find handler for active window
#         for _name, handler in self._dict_inst.items():
#             if handler.window == active_win:
#                 return handler

#         # cant find window, return none
#         return None

#     # --------------------------------------------------------------------------
#     # Private methods
#     # --------------------------------------------------------------------------

#     # --------------------------------------------------------------------------
#     # Called when the Application is activated (ie. first window is shown)
#     # --------------------------------------------------------------------------
#     def _evt_app_activate(self, _obj):
#         """
#         Called when the Application is activated (ie. first window is shown)

#         Args:
#             _obj: Not used

#         The Application is about to start. Show default window(s) or possibly
#         all windows that were open during the last session.
#         """

#         # sanity check
#         if len(self._dict_state) == 0:
#             print("no windows visible at launch")
#             return

#         # loop through each window that needs to be shown
#         for name_win, state_win in self._dict_state.items():

#             # get the class as a string and let add_window handle the parsing
#             # and conversion to a class
#             mod_class_name = state_win[self.KEY_CLASS]

#             # add class instance using info from self._dict_state
#             self.add_window(mod_class_name, name_win, state_win)

#     # --------------------------------------------------------------------------
#     # Called when the Application is stopped (ie. last window is closed, dock
#     # menu quit, top bar quit, etc.)
#     # --------------------------------------------------------------------------
#     def _evt_app_shutdown(self, _obj):
#         """
#         Called when the Application is stopped (ie. last window is closed, dock
#         menu quit, top bar quit, etc.)

#         Args:
#             _obj: Not used

#         This method removes any windows left in the list when tha application
#         quits.
#         """

#         # TODO: is this called before or after windows are destroyed?
#         # if before, can just call get_state on all remaining windows
#         # if after, get_state must be called in each window's destroy method
#         print("shutdown: ", len(self._dict_inst))

#         # save _dict_state to _path_state
#         CF.save_dict_into_paths([self._path_state], self._dict_state)

#         # TODO: is any of this needed?

#         # start with a fresh dict
#         # dict_state = {}

#         # # loop through all existing windows
#         # for k, v in self._dict_inst.items():
#         #     # dict_state[k] = v.get_state()
#         #     # simulate the 'X' button in window's title bar
#         #     v.window.destroy()

#         # CF.save_dict_into_paths([self._path_state], dict_state)
#         # destroy any windows left in the list
#         # for key, value in self._dict_inst.items():

#         #     # remove it from the list
#         #     # del self._dict_inst[key]

#         #     # send it the destroy message
#         #     value.delete()


# # -)
