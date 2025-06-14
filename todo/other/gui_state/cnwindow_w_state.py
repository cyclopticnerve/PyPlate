# # ------------------------------------------------------------------------------
# # Project : CNAppLib                                               /          \
# # Filename: cnwindow.py                                           |     ()     |
# # Date    : 03/14/2024                                            |            |
# # Author  : cyclopticnerve                                        |   \____/   |
# # License : WTFPLv2                                                \          /
# # ------------------------------------------------------------------------------

# """
# A class to manage a GTK Window

# This class handles common stuff like setting/getting the window state,
# resizing, handling the close event (ie. the 'X' button) and changing the title
# if any controls are modified.
# Remember to connect all the appropriate window events in your ui file to the
# private methods declared here.
# """

# # ------------------------------------------------------------------------------
# # Imports
# # ------------------------------------------------------------------------------

# # system imports
# from pathlib import Path
# import sys

# # cnlib imports
# from .cnapp import CNApp as A
# from cnlib import cnfunctions as CF  # type: ignore
# import gi  # type: ignore
# gi.require_version("Gtk", "3.0")
# from gi.repository import Gtk  # type: ignore

# # find paths to lib
# # NB: this assumes cnlib is a "sister" folder to cnapplib
# DIR_CNLIB = Path(__file__).parents[1].resolve()

# # add paths to import search
# sys.path.append(str(DIR_CNLIB))

# # ------------------------------------------------------------------------------
# # Public classes
# # ------------------------------------------------------------------------------


# # ------------------------------------------------------------------------------
# # A class to wrap Gtk.(Application)Window objects in the ui file
# # ------------------------------------------------------------------------------
# class CNWindow:
#     """
#     A class to wrap Gtk.(Application)Window objects in the ui file

#     Properties:
#         name: The name of the window in the app's instance list
#         window: The window object from the UI file

#     Methods:
#         set_state: Sets the values for the window's controls
#         get_state: Returns a dictionary of the window's controls' values
#         set_title: Sets the new title of the window (used to adjust for
#         modified indicator)
#         get_title: Gets the current title of the window (used to adjust for the
#         modified indicator)
#         is_modified: Returns whether any controls have been modified since the
#         last save
#         show_dialog: Shows a dialog by name from the UI file and returns its
#         result

#     This class contains all the handler code for a typical window.
#     """

#     # --------------------------------------------------------------------------
#     # Instance methods
#     # --------------------------------------------------------------------------

#     # --------------------------------------------------------------------------
#     # Initialize the new object
#     # --------------------------------------------------------------------------
#     def __init__(
#         self,
#         app,        # not stored
#         name_win,   # public
#         ui_file,    # not stored
#         ui_name,    # not stored
#         dict_state  # private
#     ):
#         """
#         Initialize the new object

#         Args:
#             app: The calling Application object
#             name_win: The name of the window in the app's instance list
#             ui_file: The ui file that contains the window for this class
#             ui_name: The name of the window object in the ui_file
#             dict_state: The dict of user props for this Window from the calling
#             Application

#         Initializes a new instance of the class, setting the default values of
#         its properties, and any other code needed to create a new object.
#         """

#         # ----------------------------------------------------------------------
#         # props

#         # private props
#         # NB: used for i18n in _show_dialog, and _evt_win_delete
#         self._app = app

#         # public props
#         self.name = name_win

#         # set def props
#         self._close_action = A.CLOSE_ACTION_SAVE
#         self._show_mod = False
#         self._mod_char = "\u29BF"
#         self._mod_fmt = "${MOD} ${TITLE}"

#         # ----------------------------------------------------------------------
#         # ui_file/ui_name

#         # create the builder
#         # NEXT: remove for templates
#         self._builder = Gtk.Builder()

#         # I18N: set the builder to point to domain
#         self._builder.set_translation_domain(self._app.app_id)

#         # get class's ui file and add to builder
#         # NB: cast in case it is a Path object
#         self._builder.add_from_file(str(ui_file))

#         # get the main window object from the ui file
#         # NB: public because we need it in app._app_evt_activate
#         self.window = self._builder.get_object(ui_name)

#         # ----------------------------------------------------------------------
#         # title

#         # get initial ui file title for use in formatting mod indicator
#         self._def_title = self.window.get_title()

#         # ----------------------------------------------------------------------
#         # dict_state

#         # make a def state dict
#         # def_state = self.get_state()
#         def_state = {}
#         def_state[A.KEY_SIZE] = self._get_size()
#         def_state[A.KEY_CTLS] = self._get_ctls()
#         def_state[A.KEY_TITLE] = self.get_title()

#         # combine state dicts
#         # order of precedence is:
#         # 1. values from ui file (def_state)
#         # 2. values passed in from user (param dict_state)
#         self._dict_state = CF.combine_dicts(def_state, dict_state)

#         # apply final state to size/ctls
#         # self.set_state()
#         self._set_size()
#         self._set_ctls()
#         self.set_title(self._dict_state[A.KEY_TITLE])

#         # ----------------------------------------------------------------------
#         # connections

#         # connect default operations for a new window
#         self.window.connect("delete-event", self._evt_win_delete)
#         self.window.connect("destroy", self._evt_win_destroy)

#         # connect all subInstance methods
#         self._builder.connect_signals(self)

#     # --------------------------------------------------------------------------
#     # Public methods
#     # --------------------------------------------------------------------------

#     # --------------------------------------------------------------------------
#     # A convenience method to set window size/ctls from state
#     # --------------------------------------------------------------------------
#     # def set_state(self):
#     #     """
#     #     A convenience method to set size/ctls from state
#     #     """

#     #     self._set_size()
#     #     self._set_ctls()

#     # --------------------------------------------------------------------------
#     # A convenience method to get size/ctls from window
#     # --------------------------------------------------------------------------
#     def get_state(self):
#         """
#         A convenience method to get size/ctls from window
#         """

#         # # the default result is an empty dict
#         # result = {}

#         # # state = size/ctls
#         # result[A.KEY_SIZE] = self._get_size()
#         # result[A.KEY_CTLS] = self._get_ctls()

#         # # return result
#         # return result
#         return self._dict_state

#     # --------------------------------------------------------------------------
#     # Sets the window title without borking modified indicator
#     # --------------------------------------------------------------------------
#     def set_title(self, new_title):
#         """
#         Sets the window title without borking modified indicator

#         Args:
#             new_title: The new title of the window

#         Set the new window title and apply the modified indicator (if needed).
#         Useful for document windows where the title should reflect the document
#         name, or instances of a class where the title may be different than
#         what is in the ui file.
#         """

#         # set the new title without mod indicator
#         self._def_title = new_title

#         # apply the modified indicator and then apply title to window
#         self.is_modified()

#     # --------------------------------------------------------------------------
#     # Gets the title of the window without mod indicator
#     # --------------------------------------------------------------------------
#     def get_title(self):
#         """
#         Gets the title of the window without mod indicator

#         Returns:
#             The title of the window without modified indicator. This is useful
#             if you need to save or compare the title to some other value,
#             regardless of the modified state of the window.
#         """

#         # return last set title without mod indicator
#         return self._def_title

#     # --------------------------------------------------------------------------
#     # Called when the window needs to set if it has been modified
#     # --------------------------------------------------------------------------
#     def is_modified(self):
#         """
#         Called when the window needs to set if it has been modified

#         Returns:
#             True if any control has been modified since last save
#             False otherwise

#         The window needs to know if it has been modified. So we create a
#         hypothetical current dict, and compare it to the last saved dict. If
#         there are any differences, we have been modified. This method is called
#         frequently and is not stored in a variable to prevent caching. It also
#         modifies the title of the window if AC.KEY_WIN_MOD is True. The return
#         is ignored when all we care about is modifying the title, but may be
#         used to determine whether to show the close dialog. Note that this
#         property is not saved between sessions, since it is always False when
#         the window closes (either by saving the changes or discarding them).
#         """

#         # default result
#         result = False

#         # get the old and new values of the gui
#         old_ctls = self._dict_state[A.KEY_CTLS]
#         new_ctls = self._get_ctls()

#         # enumerate the keys we will save
#         for new_key, new_val in new_ctls.items():
#             # get previous value
#             old_val = old_ctls[new_key]

#             # if they are different, we are modified
#             if new_val != old_val:
#                 result = True

#                 # at least one value has changed, GTFO
#                 break

#         # update the window title
#         self._format_title(result)

#         # now return result for internal stuff
#         return result

#     # --------------------------------------------------------------------------
#     # A convenience method for subclasses to show a dialog
#     # --------------------------------------------------------------------------
#     def show_dialog(self, ui_file, dlg_name):
#         """
#         A convenience method for subclasses to show a dialog

#         Args:
#             ui_file: The file containing the dialog description in xml
#             dlg_name: The name of the dialog in the ui file

#         Returns:
#             The result of calling run() on the dialog

#         Show the named dialog and returns after it is closed. This is mostly to
#         show the About dialog, but it can be used to show any modal dialog and
#         return its run value.
#         """

#         # get a builder to load the dialog ui file
#         dlg_builder = Gtk.Builder()

#         # I18N
#         # set the builder to point to domain
#         dlg_builder.set_translation_domain(self._app.app_id)

#         # get class's ui file and add to builder
#         # NB: cast in case it is a Path object
#         dlg_builder.add_from_file(str(ui_file))

#         # get dialog, run, hide (standard for reusable modal dialogs)
#         dialog = dlg_builder.get_object(dlg_name)
#         result = dialog.run()
#         dialog.hide()

#         # return dialog end result
#         return result

#     # --------------------------------------------------------------------------
#     # Private methods
#     # --------------------------------------------------------------------------

#     # --------------------------------------------------------------------------
#     # A convenience method to format and set the title when the modified status
#     # changes
#     # --------------------------------------------------------------------------
#     def _format_title(self, is_modified):
#         """
#         A convenience method to format and set the title when the modified
#         status changes

#         Args:
#             is_modified: Whether to the window controls have been modified

#         Change the window title when the window title changes, and incorporate
#         the modified indicator. Note that we pass the modified flag as an
#         argument, since calling is_modified here would cause an endless loop.
#         """

#         # by default, just use the regular title
#         str_title = self._def_title

#         # if we are modified and we want to show it
#         # NB: we use a param instead of the result of is_modified to prevent an
#         # infinite loop (is_modified calls this method)
#         if is_modified and self._show_mod:

#             # replace each part
#             str_title = self._mod_fmt.replace("${MOD}", self._mod_char)
#             str_title = str_title.replace("${TITLE}", self._def_title)

#         # change window title
#         self.window.set_title(str_title)

#     # --------------------------------------------------------------------------
#     # Sets the window size before it is shown
#     # --------------------------------------------------------------------------
#     def _set_size(self):
#         """
#         Sets the window size before it is shown

#         Set the window size from _dict_gui before it is shown.
#         """

#         # get new size
#         dict_size = self._dict_state[A.KEY_SIZE]

#         # convert from string to int
#         w = dict_size[A.KEY_SIZE_W]
#         h = dict_size[A.KEY_SIZE_H]
#         m = dict_size[A.KEY_SIZE_M]

#         # set size
#         self.window.set_default_size(w, h)

#         # set max
#         if m:
#             self.window.maximize()

#     # --------------------------------------------------------------------------
#     # Gets the current window size to a dictionary
#     # --------------------------------------------------------------------------
#     def _get_size(self):
#         """
#         Gets the current window size to a dictionary

#         Returns:
#             A dictionary containing the size info

#         Gets the current window max state/size to a dictionary. Creating a temp
#         dict and returning it ensures that no keys are missing and no values
#         are empty, similar to _get_controls.
#         """

#         # get current state/size
#         is_max = self.window.is_maximized()
#         size = self.window.get_size()

#         # create a dict based on determined state/size
#         result = {
#             A.KEY_SIZE_M: is_max,
#             A.KEY_SIZE_W: size.width,
#             A.KEY_SIZE_H: size.height,
#         }

#         # set result to internal state dict
#         # self._dict_state[A.KEY_SIZE] = result
#         return result

#     # --------------------------------------------------------------------------
#     # Sets the current window control values
#     # --------------------------------------------------------------------------
#     def _set_ctls(self):
#         """
#         Sets the current window control values

#         A dummy method that will be overridden in the subclass. This method
#         sets the values of the controls in the window using self._dict_state.
#         """

#         # show a message in case we forgot to override this in the subclass
#         print("_set_ctls: not implemented")

#     # --------------------------------------------------------------------------
#     # Gets the current window control values
#     # --------------------------------------------------------------------------
#     def _get_ctls(self):
#         """
#         Gets the current window control values

#         Returns:
#             The state of the current window

#         A dummy method that will be overridden in the subclass. This method
#         returns the values of the controls in the window.
#         """

#         # show a message in case we forgot to override this in the subclass
#         print("_get_ctls: not implemented")

#         # return default value
#         return {}

#     # --------------------------------------------------------------------------
#     # A convenience method for when the window wants to close
#     # --------------------------------------------------------------------------
#     def _can_close(self):
#         """
#         A convenience method for when the window wants to close

#         Returns:
#             True if we allow the window to close
#             False if we do not want the window to close

#         This method returns a boolean value which determines whether the window
#         closes or not, and possibly saves the current state of the gui to the
#         backing store.

#         Depending on the window's CLOSE_ACTION, one of three things happens:
#         - If CLOSE_ACTION is CLOSE_ACTION_CANCEL, the gui is not saved and the
#         method returns False, meaning the window should not close.
#         - If CLOSE_ACTION is CLOSE_ACTION_SAVE, the gui is saved and the method
#         returns True, allowing the window to close.
#         - If CLOSE_ACTION is ACLOSE_ACTION_ASK, another decision is made:
#             - If the window is not modified, this method returns True, allowing
#             the window to close
#             - If the window is modified, a dialog is shown to ask the
#             user what they want to do.

#         When shown, the dialog has 3 buttons: 'Close without saving', 'Cancel',
#         or 'Save/Save As...' (Strings are localized).\n
#         If the user chooses the first button, this method will return True,
#         allowing the window to close, but losing all changes.\n
#         If the user chooses the second button, the method returns False and the
#         window stays open, with all changes intact.\n
#         If the third button is chosen, the gui is saved to the backing store
#         and the method returns True, in which case the window will close.
#         """

#         # always save size, don't care about ctls
#         self._dict_state[A.KEY_SIZE] = self._get_size()
#         self._dict_state[A.KEY_TITLE] = self.get_title()

#         # don't allow close, don't need ctls
#         if self._close_action == A.CLOSE_ACTION_CANCEL:
#             return False

#         # allow close, save ctls
#         if self._close_action == A.CLOSE_ACTION_SAVE:
#             self._dict_state[A.KEY_CTLS] = self._get_ctls()
#             return True

#         # not modified, allow close, don't need ctls
#         if not self.is_modified():
#             return True

#         # if we got here, must be modified and close action = CLOSE_ACTION_ASK
#         # get result from dialog
#         dlg_res = self._show_close_dialog()

#         # based on result of dialog
#         if dlg_res == Gtk.ResponseType.CLOSE:
#             # close window without saving
#             return True
#         if dlg_res == Gtk.ResponseType.CANCEL:
#             # do not close window
#             return False
#         if dlg_res == Gtk.ResponseType.OK:
#             # save size/controls and close
#             self._dict_state[A.KEY_CTLS] = self._get_ctls()
#             return True

#     # --------------------------------------------------------------------------
#     # A convenience method to show the close dialog
#     # --------------------------------------------------------------------------
#     def _show_close_dialog(self):
#         """
#         A convenience method to show the close dialog

#         This method should be overridden in a subclass to show the dialog and
#         return the result.
#         """

#         # show a message in case we forgot to override this in the subclass
#         print("_show_close_dialog: not implemented")

#         # return default result (save ctls, close window)
#         return Gtk.ResponseType.OK

#     # --------------------------------------------------------------------------
#     # Window events
#     # --------------------------------------------------------------------------

#     # --------------------------------------------------------------------------
#     # Called when the main window is closed by the 'X' button
#     # --------------------------------------------------------------------------
#     def _evt_win_delete(self, _obj, _event):
#         """
#         Called when the main window is closed by the 'X' button

#         Args:
#             _obj: Not used
#             _event: Not used

#         Returns:
#             False to allow the window to close
#             True to keep the window open

#         The Window is about to close via the 'X' button (or some other system
#         event, like closing from the overview or the dock). Note that this
#         handler expects to return THE OPPOSITE of the _can_close method's
#         result. That is, returning False here lets the window close, while
#         returning True means the window will not close. This is easy to work
#         around since _can_close returns a boolean value.
#         """

#         # maybe close window
#         return not self._can_close()

#     # --------------------------------------------------------------------------
#     # Called after the window is destroyed
#     # --------------------------------------------------------------------------
#     def _evt_win_destroy(self, _obj):
#         """
#         Called after the window is destroyed

#         Args:
#             _obj: Not used

#         This method is called after the window is destroyed. It is used to
#         remove the window from the app's internal list.
#         """

#         # remove the window from app list
#         self._app.remove_window(self.name)

# # -)
