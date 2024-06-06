# ------------------------------------------------------------------------------
# Project : CNAppLib                                               /          \
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

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
from .cnapp import CNApp as A
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
        window: The window object from the UI file

    Methods:
        # TODO: which are public/private?
        set_title: Sets the new title of the window (used to adjust for
        modified indicator)
        get_title:Get the current title of the window (used to adjust for the
        modified indicator)
        set_control: Sets the value of a single control by name
        get_control: Gets the value of a single control by name
        set_controls: Sets the value of all controls from a dictionary
        get_controls: Gets the value of all controls into a dictionary
        is_modified: Returns whether any controls have been modified since the
        last save
        show_dialog: Shoes a dialog by name from the UI file and returns its
        result

    This class contains all the handler code for a typical window.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(
        self,
        app,        # not stored
        name_win,   # public
        ui_file,    # not stored
        ui_name,    # not stored
        dict_state  # private
    ):
        """
        Initialize the new object

        Arguments:
            app: The calling Application object
            name_win: The name of the window in the app's instance list
            ui_file: The ui file that contains the window for this class
            ui_name: The name of the window object in the ui_file
            dict_state: The dict of user props for this Window from the calling
            Application

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # ----------------------------------------------------------------------
        # props

        # private props
        # NB: used for i18n in _show_dialog and _evt_win_delete
        self._app = app

        # public props
        self.name_win = name_win

        # set def props
        self._close_action = A.CLOSE_ACTION_SAVE
        self._show_mod = False
        self._mod_char = "\u29BF"
        self._mod_fmt = "${MOD} ${TITLE}"

        # ----------------------------------------------------------------------
        # ui_file/ui_name

        # create the builder
        # NEXT: remove for templates
        self._builder = Gtk.Builder()

        # I18N: set the builder to point to domain
        self._builder.set_translation_domain(self._app.app_id)

        # get class's ui file and add to builder
        # NB: cast in case it is a Path object
        self._builder.add_from_file(str(ui_file))

        # get the main window object from the ui file
        # NB: public because we need it in app._app_evt_activate
        self.window = self._builder.get_object(ui_name)

        # ----------------------------------------------------------------------
        # title

        # get initial ui file title for use in formatting mod indicator
        self._def_title = self.window.get_title()

        # ----------------------------------------------------------------------
        # dict_state

        self._dict_state = dict_state

        # start with a clean dict
        # self._dict_state = {}
        # TODO: get_state should return a dict of size/gui
        # self._dict_state = self._get_state()

        # get current (default) size/controls from ui file
        # self._dict_state[A.KEY_WIN_SIZE] = self._get_size()
        # self._dict_state[A.KEY_WIN_SIZE] = self.get_state()[A.KEY_WIN_SIZE]
        # self._dict_state[A.KEY_WIN_CTLS] = self.get_state()[A.KEY_WIN_CTLS]

        # combine user_dict values
        # order of precedence is:
        # 1. values from ui file
        # 2. values passed in from user (param dict_gui)

        # combine ui settings and user settings
        # TODO: wtf is dict_win?
        # need to get def size/gui from ui file, combine with param,
        # set_state with that combined dict

        # dict_win = dict_state[self._name_win]
        # self._dict_state = CF.combine_dicts(self._dict_state, [dict_win])

        # fix ints/bools in dict_gui
        # FIXME: how to sanitize gui for bool/int/str without ctl type?
        # self._dict_state = self._sanitize_gui(self._dict_state)

        # once we have the final dict_gui, apply backing store to window
        # self._set_size()

        # get the list of window controls
        # dict_ctls = self._dict_state[A.KEY_WIN_CTLS]
        # self.set_controls(dict_ctls)
        # NB: use sanitized state
        # self._set_state(self._dict_state)

        # save backing store to app
        # self._app.set_dict_state(self._name_win, self._dict_state)

        # ----------------------------------------------------------------------
        # connections

        # connect default operations for a new window
        self.window.connect("delete-event", self._evt_win_delete)
        self.window.connect("destroy", self._evt_win_destroy)

        # TODO: for each control, connect its modified action to
        # _ctl_evt_modified

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # A convenience method to set window size/ctls from state
    # --------------------------------------------------------------------------
    def set_state(self):
        """
        A convenience method to set size/ctls from state
        """

        self._set_size()
        self._set_ctls()

    # --------------------------------------------------------------------------
    # A convenience method to get state size/ctls from window
    # --------------------------------------------------------------------------
    def get_state(self):
        """
        A convenience method to get size/ctls from window
        """

        self._get_size()
        self._get_ctls()

    # --------------------------------------------------------------------------
    # Sets the window title without borking modified indicator
    # --------------------------------------------------------------------------
    def set_title(self, new_title):
        """
        Sets the window title without borking modified indicator

        Arguments:
            new_title: The new title of the window

        Set the new window title and apply the modified indicator (if needed).
        Useful for document windows where the title should reflect the document
        name, or instances of a class where the title may be different than
        what is in the ui file.
        """

        # set the new title without mod indicator
        self._def_title = new_title

        # apply the modified indicator and then apply title to window
        self.is_modified()

    # --------------------------------------------------------------------------
    # Gets the title of the window without mod indicator
    # --------------------------------------------------------------------------
    def get_title(self):
        """
        Gets the title of the window without mod indicator

        Returns:
            The title of the window without modified indicator. This is useful
            if you need to save or compare the title to some other value,
            regardless of the modified state of the window.
        """

        # return last set title without mod indicator
        return self._def_title

    # --------------------------------------------------------------------------
    # Called when the window needs to set if it has been modified
    # --------------------------------------------------------------------------
    def is_modified(self):
        """
        Called when the window needs to set if it has been modified

        Returns:
            True if any control has been modified since last save
            False otherwise

        The window needs to know if it has been modified. So we create a
        hypothetical current dict, and compare it to the last saved dict. If
        there are any differences, we have been modified. This method is called
        frequently and is not stored in a variable to prevent caching. It also
        modifies the title of the window if AC.KEY_WIN_MOD is True. The return
        is ignored when all we care about is modifying the title, but may be
        used to determine whether to show the close dialog. Note that this
        property is not saved between sessions, since it is always False when
        the window closes (either by saving the changes or discarding them).
        """

        # default result
        result = False

        # get the old and new values of the gui
        old_ctls = self._dict_state[A.KEY_CTLS]
        new_ctls = self._get_ctls()[A.KEY_CTLS]

        # enumerate the keys we will save
        for new_key, new_val in new_ctls.items():
            # get previous value
            old_val = old_ctls[new_key]

            # if they are different, we are modified
            if new_val != old_val:
                result = True

                # at least one value has changed, GTFO
                break

        # update the window title
        self._format_title(result)

        # now return result for internal stuff
        return result

    # --------------------------------------------------------------------------
    # A convenience method for subclasses to show a dialog
    # --------------------------------------------------------------------------
    def show_dialog(self, ui_file, dlg_name):
        """
        A convenience method for subclasses to show a dialog

        Arguments:
            ui_file: The file containing the dialog description in xml
            dlg_name: The name of the dialog in the ui file

        Returns:
            The result of calling run() on the dialog

        Show the named dialog and returns after it is closed. This is mostly to
        show the About dialog, but it can be used to show any modal dialog and
        return its run value.
        """

        # get a builder to load the dialog ui file
        dlg_builder = Gtk.Builder()

        # I18N
        # set the builder to point to domain
        dlg_builder.set_translation_domain(self._app.app_id)

        # get class's ui file and add to builder
        # NB: cast in case it is a Path object
        dlg_builder.add_from_file(str(ui_file))

        # get dialog, run, hide (standard for reusable modal dialogs)
        dialog = dlg_builder.get_object(dlg_name)
        result = dialog.run()
        dialog.hide()

        # return dialog end result
        return result

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # A convenience method to format and set the title when the modified status
    # changes
    # --------------------------------------------------------------------------
    def _format_title(self, is_modified):
        """
        A convenience method to format and set the title when the modified
        status changes

        Arguments:
            is_modified: Whether to the window controls have been modified

        Change the window title when the window title changes, and incorporate
        the modified indicator. Note that we pass the modified flag as an
        argument, since calling is_modified here would cause an endless loop.
        """

        # by default, just use the regular title
        str_title = self._def_title

        # if we are modified and we want to show it
        # NB: we use a param instead of the result of is_modified to prevent an
        # infinite loop (is_modified calls this method)
        if is_modified and self._show_mod:

            # replace each part
            str_title = self._mod_fmt.replace("${MOD}", self._mod_char)
            str_title = str_title.replace("${TITLE}", self._def_title)

        # change window title
        self.window.set_title(str_title)

    # --------------------------------------------------------------------------
    # Sets the window size before it is shown
    # --------------------------------------------------------------------------
    def _set_size(self):
        """
        Sets the window size before it is shown

        Set the window size from _dict_gui before it is shown.
        """

        # get new size
        dict_size = self._dict_state[A.KEY_SIZE]

        # convert from string to int
        w = dict_size[A.KEY_SIZE_W]
        h = dict_size[A.KEY_SIZE_H]
        m = dict_size[A.KEY_SIZE_M]

        # set size
        self.window.set_default_size(w, h)

        # set max
        if m:
            self.window.maximize()

    # --------------------------------------------------------------------------
    # Gets the current window size to a dictionary
    # --------------------------------------------------------------------------
    def _get_size(self):
        """
        Gets the current window size to a dictionary

        Returns:
            A dictionary containing the size info

        Gets the current window max state/size to a dictionary. Creating a temp
        dict and returning it ensures that no keys are missing and no values
        are empty, similar to _get_controls.
        """

        # get current state/size
        is_max = self.window.is_maximized()
        size = self.window.get_size()

        # create a dict based on determined state/size
        result = {
            A.KEY_SIZE_M: is_max,
            A.KEY_SIZE_W: size.width,
            A.KEY_SIZE_H: size.height,
        }

        # set result to internal state dict
        self._dict_state[A.KEY_SIZE] = result

    # --------------------------------------------------------------------------
    # Sets the current window control values
    # --------------------------------------------------------------------------
    def _set_ctls(self):
        """
        Sets the current window control values

        A dummy method that will be overridden in the subclass. This method
        sets the values of the controls in the window using self._dict_state.
        """

        # show a message in case we forgot to override this in the subclass
        print("not implemented")

    # --------------------------------------------------------------------------
    # Gets the current window control values
    # --------------------------------------------------------------------------
    def _get_ctls(self):
        """
        Gets the current window control values

        Returns:
            The state of the current window

        A dummy method that will be overridden in the subclass. This method
        returns the values of the controls in the window.
        """

        # show a message in case we forgot to override this in the subclass
        print("not implemented")
        return {}

    # --------------------------------------------------------------------------
    # A convenience method for when the window wants to close
    # --------------------------------------------------------------------------
    def _can_close(self):
        """
        A convenience method for when the window wants to close

        Arguments:
            ui_file: The file containing the dialog description in xml
            dlg_name: The name of the dialog in the ui file

        Returns:
            True if we allow the window to close
            False if we do not want the window to close

        This method returns a boolean value which determines whether the window
        closes or not, and possibly saves the current state of the gui to the
        backing store.

        Depending on the window's CLOSE_ACTION, one of three things happens:
        - If CLOSE_ACTION is CLOSE_ACTION_CANCEL, the gui is not saved and the
        method returns False, meaning the window should not close.
        - If CLOSE_ACTION is CLOSE_ACTION_SAVE, the gui is saved and the method
        returns True, allowing the window to close.
        - If CLOSE_ACTION is ACLOSE_ACTION_ASK, another decision is made:
            - If the window is not modified, this method returns True, allowing
            the window to close
            - If the window is modified, a dialog is shown to ask the
            user what they want to do.

        When shown, the dialog has 3 buttons: 'Close without saving', 'Cancel',
        or 'Save/Save As...' (Strings are localized).\n
        If the user chooses the first button, this method will return True,
        allowing the window to close, but losing all changes.\n
        If the user chooses the second button, the method returns False and the
        window stays open, with all changes intact.\n
        If the third button is chosen, the gui is saved to the backing store
        and the method returns True, in which case the window will close.
        """

        # always save size, don't care about ctls
        self._get_size()

        # not modified, allow close
        if not self.is_modified():
            return True

        # don't allow close
        if self._close_action == A.CLOSE_ACTION_CANCEL:
            return False

        # save size/controls and allow close
        if self._close_action == A.CLOSE_ACTION_SAVE:
            self._get_ctls()
            return True

        # get result from dialog
        # NB: close_action == AC.CLOSE_ACTION_ASK
        dlg_res = self._show_close_dialog()

        if dlg_res == Gtk.ResponseType.CLOSE:
            # close window without saving
            return True
        if dlg_res == Gtk.ResponseType.CANCEL:
            # do not close window
            return False
        if dlg_res == Gtk.ResponseType.OK:
            # save size/controls and close
            self._get_ctls()
            return True

        # default response
        return True

    # --------------------------------------------------------------------------
    # A convenience method to show the close dialog
    # --------------------------------------------------------------------------
    def _show_close_dialog(self):
        """
        A convenience method to show the close dialog

        This method should be overridden in a subclass to show the dialog and
        return the result.
        """

        # return default result
        return True

    # --------------------------------------------------------------------------
    # Window events
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when any control in the window is modified
    # --------------------------------------------------------------------------
    def _evt_ctl_modified(self, _obj):
        """
        Called when any control in the window is modified

        Arguments:
            _obj: Not used

        Use this method to update the modified status of the window. Controls
        can have multiple handlers, so always connect your controls to this
        handler, as well as window-specific handlers for a particular control.
        """

        # get modified value and change window title (ignore return value)
        self.is_modified()

    # --------------------------------------------------------------------------
    # Called when the main window is closed by the 'X' button
    # --------------------------------------------------------------------------
    def _evt_win_delete(self, _obj, _event):
        """
        Called when the main window is closed by the 'X' button

        Arguments:
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

        # maybe close window
        return not self._can_close()

    # --------------------------------------------------------------------------
    # Called after the window is destroyed
    # --------------------------------------------------------------------------
    def _evt_win_destroy(self, _obj):
        """
        Called after the window is destroyed

        Arguments:
            _obj: Not used

        This method is called after the window is destroyed. It is used to
        remove the window from the app's internal list.
        """

        print("_evt_win_destroy")

        # remove the window from app list
        self._app.remove_window(self.name_win)

    # ------------------------------------------------------------------------------
    # A convenience method to return the type of a control, parsed from the
    # class control set
    # ------------------------------------------------------------------------------
    # def _get_ctl_type(self, ctl_name):
    #     """
    #     A convenience method to return the type of a control, parsed from the
    #     class control set

    #     Arguments:
    #         class_dict: the dict of common class properties
    #         ctl_name: the control whose type we want to know

    #     Returns the control type for a specified control in a specified class,
    #     so that we can determine setter/getter methods as well as the value
    #     type. The result is one of constants.CTL_TYPE_...
    #     """

    #     # get controls for class
    # Arguments:
    #     ui_file: The file containing the dialog description in xml
    #     dlg_name: The name of the dialog in the ui file
    #     class_ctls = class_dict.get(AC.KEY_CLS_CTLS, {})

    #     # get control type
    #     dict_ctl = class_ctls.get(ctl_name, {})
    #     ctl_type = dict_ctl.get(AC.KEY_CTL_TYPE, AC.CTL_TYPE_TEXT)

    #     # return the type
    #     return ctl_type

    # ------------------------------------------------------------------------------
    # Called when the gui dict is passed in, to ensure all values are of the
    # correct type
    # ------------------------------------------------------------------------------
    # def _sanitize_gui(self, dict_gui):
    #     """
    #     Called when a gui dict is passed in, to ensure all values are of
    #     the correct type

    #     Arguments:
    #         dict_class: The dict_app entry for this window's class
    #         dict_gui: The dict to sanitize

    #     Returns:
    #         The sanitized dict
    #     """

    #     # do visibility
    #     # NB: do not use get, if it's empty, skip and leave it empty
    #     # if AC.KEY_WIN_VISIBLE in dict_gui:
    #     #     val = dict_gui[AC.KEY_WIN_VISIBLE]
    #     #     val = CF.do_bool(val)
    #     #     dict_gui[AC.KEY_WIN_VISIBLE] = val

    #     # check if size dict exists
    #     # NB: do not use get, if it's empty, skip and leave it empty
    #     if A.KEY_WIN_SIZE in dict_gui:
    #         # get the size dict
    #         dict_size = dict_gui[A.KEY_WIN_SIZE]

    #         # fix width
    #         w = dict_size[A.KEY_WIN_SIZE_W]
    #         dict_size[A.KEY_WIN_SIZE_W] = int(w)

    #         # fix height
    #         h = dict_size[A.KEY_WIN_SIZE_H]
    #         dict_size[A.KEY_WIN_SIZE_H] = int(h)

    #         # fix max
    #         m = dict_size[A.KEY_WIN_SIZE_M]
    #         dict_size[A.KEY_WIN_SIZE_M] = CF.do_bool(m)

    #         # put it back
    #         dict_gui[A.KEY_WIN_SIZE] = dict_size

    #     # check if controls dict exists
    #     # NB: do not use get, if it's empty, skip and leave it empty
    #     if A.KEY_WIN_CTLS in dict_gui:
    #         # get the window's controls dict
    #         dict_ctls = dict_gui[A.KEY_WIN_CTLS]

    #         # for each control
    #         for k, v in dict_ctls.items():
    #             # get value type from control type
    #             ctl_type = get_ctl_type(k)
    #             val_type = ctl_type.get(AC.KEY_CTL_VAL_TYPE, None)

    #             # get the val from the user dict
    #             val = v.get(AC.KEY_CTL_VAL, "")

    #             # convert int
    #             if val_type == AC.CTL_VAL_TYPE_INT:
    #                 val = int(val)

    #             # convert bool
    #             elif val_type == AC.CTL_VAL_TYPE_BOOL:
    #                 val = CF.do_bool(val)

    #             # update controls dict
    #             dict_ctls[k][AC.KEY_CTL_VAL] = val

    #         # update window dict
    #         dict_gui[AC.KEY_WIN_CTLS] = dict_ctls

    #     # return updated dict
    #     return dict_gui

    # # --------------------------------------------------------------------------
    # # A convenience method to set the value of the specified control
    # # --------------------------------------------------------------------------
    # def set_control(self, ctl_name, value):
    #     """
    #     A convenience method to set the value of the specified control

    #     Arguments:
    #         ctl_name: The name of the control in the UI file
    #         value: The new value for the control

    #     Returns the value of a window control as named in the UI file.
    #     """

    #     # get the control
    #     obj = self._builder.get_object(ctl_name)

    #     # get control's type
    #     type_ = AF.get_ctl_type(self._dict_class, ctl_name)

    #     # get control's setter method
    #     set_ = type_[A.KEY_CTL_SET]

    #     # call method to set value
    #     fnc = getattr(obj, set_)
    #     fnc(value)

    # # --------------------------------------------------------------------------
    # # A convenience method to return the value of the specified control
    # # --------------------------------------------------------------------------
    # def get_control(self, ctl_name):
    #     """
    #     A convenience method to return the value of the specified control

    #     Arguments:
    #         ctl_name: The name of the control in the UI file

    #     Returns the value of a window control as named in the UI file.
    #     """

    #     # get the control
    #     obj = self._builder.get_object(ctl_name)

    #     # get control's type
    #     type_ = AF.get_ctl_type(self._dict_class, ctl_name)

    #     # get control's getter method
    #     get = type_[A.KEY_CTL_GET]

    #     # call method to get value
    #     fnc = getattr(obj, get)
    #     val = fnc()

    #     # return value
    #     return val

    # # --------------------------------------------------------------------------
    # # Sets the values of all controls before window is shown
    # # --------------------------------------------------------------------------
    # def set_controls(self, dict_ctls):
    #     """
    #     Sets the values of all controls before window is shown

    #     Arguments:
    #         dict_ctls: The dict containing the values for each control

    #     Set the values of all controls from the specified dict when this
    #     method is called.
    #     """

    #     # now put the new gui values into the controls
    #     for k, v in dict_ctls.items():

    #         # get the value
    #         val = v[A.KEY_CTL_VAL]

    #         # do the method for each control
    #         self.set_control(k, val)

    # # --------------------------------------------------------------------------
    # # Gets the current values of all controls to a dictionary
    # # --------------------------------------------------------------------------
    # def get_controls(self):
    #     """
    #     Gets the current values of all controls to a dictionary

    #     Returns:
    #         A dictionary containing the current values of the controls

    #     Gets the values of all gui objects and return it whenever this method
    #     is called. This method is called from several places, both for
    #     saving the actual gui values and also for checking the existence of
    #     keys. Creating a temp dict and returning it ensures that no keys are
    #     missing and no values are empty, similar to _get_size.
    #     """

    #     # create a tmp dict
    #     result = {}

    #     # get the controls we want to save
    #     dict_ctls = self._dict_class[A.KEY_CLS_CTLS]

    #     # now get the new values from the controls
    #     for k, _v in dict_ctls.items():

    #         # get the value in the control
    #         val = self.get_control(k)

    #         # save val to dict
    #         result[k] = {
    #             A.KEY_CTL_VAL: val,
    #         }

    #     # return the tmp dict
    #     return result

    # # --------------------------------------------------------------------------
    # # Update the backing dict of a particular window, setting its size and
    # # control values
    # # --------------------------------------------------------------------------
    # def set_dict_state(self, name_win, dict_state):
    #     """
    #     Update the backing dict of a particular window, saving its size and
    #     control values

    #     Arguments:
    #         name_win: The name of the window to save the GUI for
    #         dict_state: The current state of the window's GUI, to be saved in
    #         the global backing store

    #     This method updates the backing store for a particular window whenever
    #     that window's values change (such as size or control values).

    #     This method should NOT be called by any outside script. It is public
    #     only so it can be used by Window and its subclasses.

    #     The contents of this dict are a reflection of the CURRENT VALUES of the
    #     GUI, after any changes have been made. This method is called by the
    #     window's _do_update method.
    #     """

    #     # set the gui dict for the window name
    #     self._dict_state[name_win] = dict_state
    #     # FIXME: for each window in dict_app, if has entry in dict_state, apply
    #     # dict_state to window

    # # --------------------------------------------------------------------------
    # # Return the backing dict of all windows, containing their size and
    # # control values
    # # --------------------------------------------------------------------------
    # def get_dict_state(self, name_win):
    #     """
    #     Return the backing dict of all windows, containing their size and
    #     control values

    #     Returns:
    #         The current backing dictionary

    #     This method should be called after run(), so that the dict is updated
    #     after any save actions have been completed.

    #     The contents of this dict are a reflection of the CURRENT VALUES of the
    #     GUI, after any changes have been made. The dict is updated by
    #     set_dict_state.

    #     The dictionary does NOT contain settings like window class, close
    #     action, etc. since these do not need to be saved between sessions.
    #     """

    #     # return the backing gui dict
    #     if name_win in self._dict_state:
    #         return self._dict_state[name_win]

    #     return None

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # # --------------------------------------------------------------------------
    # # Creates a dialog for when the window is closed by some means and is
    # # modified, and returns the result of that dialog
    # # --------------------------------------------------------------------------
    # def _show_close_dialog(self):
    #     """
    #     Creates a dialog for when the window is closed by some means and is
    #     modified, and returns the result of that dialog

    #     Returns:
    #         The result of the dialog as one of:
    #         - Gtk.ResponseType.CLOSE
    #         - Gtk.ResponseType.CANCEL
    #         - Gtk.ResponseType.OK

    #     Create a dialog that has 3 buttons, set their labels/colors, and return
    #     which button was clicked.
    #     """

    #     # create a new message box
    #     msg_box = Gtk.MessageDialog(
    #         parent=self.window,
    #         text=self._app.STR_CLOSE_DLG_MAIN,
    #         secondary_text=self._app.STR_CLOSE_DLG_SEC,
    #         message_type=Gtk.MessageType.QUESTION,
    #     )

    #     # add buttons to message box
    #     # I18N
    #     msg_box.add_buttons(
    #         self._app.STR_CLOSE_DLG_CLOSE,
    #         Gtk.ResponseType.CLOSE,
    #         self._app.STR_CLOSE_DLG_CANCEL,
    #         Gtk.ResponseType.CANCEL,
    #         # NEXT: if doc-based and untitled, this should be "Save As..."
    #         self._app.STR_CLOSE_DLG_SAVE,
    #         Gtk.ResponseType.OK,
    #     )

    #     # make all buttons stretch
    #     msg_box.action_area.set_homogeneous(True)  # pylint: disable=no-member

    #     # set the bad/none button as red
    #     btn_red = msg_box.get_widget_for_response(
    #         response_id=Gtk.ResponseType.CLOSE
    #     )
    #     btn_red_style_context = btn_red.get_style_context()
    #     btn_red_style_context.add_class("destructive-action")

    #     # set focus to save button
    #     btn_def = msg_box.get_widget_for_response(
    #         response_id=Gtk.ResponseType.OK
    #     )
    #     msg_box.set_focus(btn_def)

    #     # center dialog on parent
    #     msg_box.set_position(  # pylint: disable=no-member
    #         Gtk.WindowPosition.CENTER
    #     )

    #     # show message box and get result
    #     result = msg_box.run()  # pylint: disable=no-member
    #     msg_box.hide()

    #     # return the button that was clicked
    #     return result

    # --------------------------------------------------------------------------
    # A convenience method for subclasses to update their control values in the
    # backing store
    # --------------------------------------------------------------------------
    # def _update_gui(self):
    #     """
    #     A convenience method for subclasses to update their control values in
    #     the backing store

    #     This method just hides some implementation details when a window wants
    #     to update its gui values in the backing store.
    #     """

    #     # save size/objects
    #     self._dict_state[A.KEY_WIN_SIZE] = self._get_size()
    #     self._dict_state[A.KEY_WIN_CTLS] = self.get_state()

    #     # save backing store to app
    #     self._app.set_dict_state(self._name_win, self._dict_state)

    #     # update modified status (ignore return)
    #     self.is_modified()

# -)
