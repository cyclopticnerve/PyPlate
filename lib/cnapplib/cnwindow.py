# ------------------------------------------------------------------------------
# Project : CNAppLib                                               /          \
# Filename: cnwindow.py                                           |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to manage a GTK Window

This class handles common stuff like setting/getting the user dict, resizing,
handling the close event (ie. the 'X' button) and changing the title if any
controls are modified.
Remember to connect all the appropriate window events in your ui file to the
private methods declared here.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import gi

# pylint: disable=wrong-import-position

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk  # type: ignore

# pylint: enable==wrong-import-position

# pylint: disable=import-error

# my imports
from cnlib import cnfunctions as CF
from . import cnappconstants as AC
from . import cnappfunctions as AF

# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Macros
# ------------------------------------------------------------------------------

_ = gettext.gettext

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to wrap Gtk.Window objects in the ui file
# ------------------------------------------------------------------------------
class CNWindow:
    """
    A class to wrap Gtk.Window objects in the ui file

    Properties:
        window: The window object from the UI file

    Methods:
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
    def __init__(self, app, name_win, dict_win):
        """
        Initialize the new object

        Arguments:
            app: The calling Application object
            name_win: The name of the window in the app's instance list
            dict_win: The dict of user props for this Window from the calling
            Application

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # store params as class variables
        self._app = app
        self._name_win = name_win

        # minimum dict_win must contain:
        # AC.KEY_WIN_CLASS,
        class_win = dict_win.get(AC.KEY_WIN_CLASS, None)
        if class_win is None:
            # I18N: the specified class is None
            raise IOError(_("class is None"))

        # # get the app dict for the class
        dict_classes = self._app._dict_app[AC.KEY_APP_CLASSES]
        self._dict_class = dict_classes[class_win]

        # create the builder
        # NEXT: remove for templates
        self._builder = Gtk.Builder()

        # I18N
        # set the builder to point to domain
        self._builder.set_translation_domain("_PP_NAME_SMALL__")

        # get class's ui file and add to builder
        # NB: cast in case it is a Path object
        ui_file = self._dict_class[AC.KEY_CLS_UI_FILE]
        self._builder.add_from_file(str(ui_file))

        # get the main window object from the ui file
        # NB: public because we need it in app._activate
        ui_name = self._dict_class[AC.KEY_CLS_UI_NAME]
        self.window = self._builder.get_object(ui_name)

        # start with a clean dict
        self._dict_gui = {}

        # get current (default) size/controls from ui file
        self._dict_gui[AC.KEY_WIN_SIZE] = self._get_size()
        self._dict_gui[AC.KEY_WIN_CTLS] = self.get_controls()

        # combine user_dict values
        # order of precedence is:
        # 1. values from ui file
        # 2. values passed in from user (param dict_gui)

        # combine ui settings and user settings
        self._dict_gui = CF.combine_dicts(self._dict_gui, [dict_win])

        # fix ints/bools in dict_gui
        self._dict_gui = AF.sanitize_gui(self._dict_class, self._dict_gui)

        # once we have the final dict_gui, apply backing store to window
        self._set_size()

        # get the list of window controls
        dict_ctls = self._dict_gui[AC.KEY_WIN_CTLS]
        self.set_controls(dict_ctls)

        # save backing store to app
        self._app.set_dict_gui(self._name_win, self._dict_gui)

        # get initial ui file title for use in formatting mod indicator
        self._def_title = self.window.get_title()

        # connect signals last to avoid triggering resize/modified events
        self._builder.connect_signals(self)  # pylint: disable=no-member

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Sets the window title without borking modified indicator
    # --------------------------------------------------------------------------
    def set_title(self, new_title):
        """
        Sets the window title without borking modified indicator

        Arguments:
            new_title: The new title of the window

        Set the new window title and apply the modified indicator (if needed).
        This method also updates the backing store with the new title. Useful
        for document windows where the title should reflect the document name,
        or instances of a class where the title may be different than what is
        in the ui file.
        """

        # set the new title without mod indicator
        self._def_title = new_title

        # apply the modified indicator and then apply title to window
        self.is_modified()

    # --------------------------------------------------------------------------
    # Gets the title from the backing store without mod indicator
    # --------------------------------------------------------------------------
    def get_title(self):
        """
        Gets the title from the backing store without mod indicator

        Returns:
            The title of the window without modified indicator. This is only
            included for completeness, since the calling app or calling script
            should keep track of what titles it is setting.
        """

        return self._def_title

    # --------------------------------------------------------------------------
    # A convenience method to set the value of the specified control
    # --------------------------------------------------------------------------
    def set_control(self, ctl_name, value):
        """
        A convenience method to set the value of the specified control

        Arguments:
            ctl_name: The name of the control in the UI file
            value: The new value for the control

        Returns the value of a window control as named in the UI file.
        """

        # get the control
        obj = self._builder.get_object(ctl_name)

        # get control's type
        type_ = AF.get_ctl_type(self._dict_class, ctl_name)

        # get control's setter method
        set_ = type_[AC.KEY_CTL_SET]

        # call method to set value
        fnc = getattr(obj, set_)
        fnc(value)

    # --------------------------------------------------------------------------
    # A convenience method to return the value of the specified control
    # --------------------------------------------------------------------------
    def get_control(self, ctl_name):
        """
        A convenience method to return the value of the specified control

        Arguments:
            ctl_name: The name of the control in the UI file

        Returns the value of a window control as named in the UI file.
        """

        # get the control
        obj = self._builder.get_object(ctl_name)

        # get control's type
        type_ = AF.get_ctl_type(self._dict_class, ctl_name)

        # get control's getter method
        get = type_[AC.KEY_CTL_GET]

        # call method to get value
        fnc = getattr(obj, get)
        val = fnc()

        # return value
        return val

    # --------------------------------------------------------------------------
    # Sets the values of all controls before window is shown
    # --------------------------------------------------------------------------
    def set_controls(self, dict_ctls):
        """
        Sets the values of all controls before window is shown

        Arguments:
            dict_ctls: The dict containing the values for each control

        Set the values of all controls from the specified dict when this
        method is called.
        """

        # now put the new gui values into the controls
        for k, v in dict_ctls.items():

            # get the value
            val = v[AC.KEY_CTL_VAL]

            # do the method for each control
            self.set_control(k, val)

    # --------------------------------------------------------------------------
    # Gets the current values of all controls to a dictionary
    # --------------------------------------------------------------------------
    def get_controls(self):
        """
        Gets the current values of all controls to a dictionary

        Returns:
            A dictionary containing the current values of the controls

        Gets the values of all gui objects and return it whenever this method
        is called. This method is called from several places, both for
        saving the actual gui values and also for checking the existence of
        keys. Creating a temp dict and returning it ensures that no keys are
        missing and no values are empty, similar to _get_size.
        """

        # create a tmp dict
        result = {}

        # get the controls we want to save
        dict_ctls = self._dict_class[AC.KEY_CLS_CTLS]

        # now get the new values from the controls
        for k, _v in dict_ctls.items():

            # get the value in the control
            val = self.get_control(k)

            # save val to dict
            result[k] = {
                AC.KEY_CTL_VAL: val,
            }

        # return the tmp dict
        return result

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
        old_gui = self._dict_gui[AC.KEY_WIN_CTLS]
        new_gui = self.get_controls()

        # enumerate the keys we will save
        for new_key, new_val in new_gui.items():
            # get previous value
            old_val = old_gui[new_key]

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
    def show_dialog(self, dlg_name):
        """
        A convenience method for subclasses to show a dialog

        Arguments:
            dlg_name: The name of the dialog in the ui file

        Returns:
            The result of calling run() on the dialog

        Show the named dialog and returns after it is closed. This is mostly to
        show the About dialog, but it can be used to show any modal dialog and
        return its run value.
        """

        # get dialog, run, hide (standard for reusable modal dialogs)
        dialog = self._builder.get_object(dlg_name)
        result = dialog.run()
        dialog.hide()

        # return dialog end result
        return result

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Sets the window size before it is shown
    # --------------------------------------------------------------------------
    def _set_size(self):
        """
        Sets the window size before it is shown

        Set the window size from _dict_gui before it is shown.
        """

        # get new size
        dict_size = self._dict_gui[AC.KEY_WIN_SIZE]

        # convert from string to int
        w = dict_size[AC.KEY_SIZE_W]
        h = dict_size[AC.KEY_SIZE_H]
        m = dict_size[AC.KEY_SIZE_M]

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
            AC.KEY_SIZE_M: is_max,
            AC.KEY_SIZE_W: size.width,
            AC.KEY_SIZE_H: size.height,
        }

        # return the temp dict
        return result

    # --------------------------------------------------------------------------
    # Creates a dialog for when the window is closed by some means and is
    # modified, and returns the result of that dialog
    # --------------------------------------------------------------------------
    def _show_close_dialog(self):
        """
        Creates a dialog for when the window is closed by some means and is
        modified, and returns the result of that dialog

        Returns:
            The result of the dialog as one of:
            - Gtk.ResponseType.CLOSE
            - Gtk.ResponseType.CANCEL
            - Gtk.ResponseType.OK

        Create a dialog that has 3 buttons, set their labels/colors, and return
        which button was clicked.
        """

        # create a new message box
        msg_box = Gtk.MessageDialog(
            parent=self.window,
            text=AC.STR_CLOSE_DLG_MAIN,
            secondary_text=AC.STR_CLOSE_DLG_SEC,
            message_type=Gtk.MessageType.QUESTION,
        )

        # add buttons to message box
        # I18N
        msg_box.add_buttons(
            AC.STR_CLOSE_DLG_CLOSE,
            Gtk.ResponseType.CLOSE,
            AC.STR_CLOSE_DLG_CANCEL,
            Gtk.ResponseType.CANCEL,
            # NEXT: if doc-based and untitled, this should be "Save As..."
            AC.STR_CLOSE_DLG_SAVE,
            Gtk.ResponseType.OK,
        )

        # make all buttons stretch
        msg_box.action_area.set_homogeneous(True)  # pylint: disable=no-member

        # set the bad/none button as red
        btn_red = msg_box.get_widget_for_response(
            response_id=Gtk.ResponseType.CLOSE
        )
        btn_red_style_context = btn_red.get_style_context()
        btn_red_style_context.add_class("destructive-action")

        # set focus to save button
        btn_def = msg_box.get_widget_for_response(
            response_id=Gtk.ResponseType.OK
        )
        msg_box.set_focus(btn_def)

        # center dialog on parent
        msg_box.set_position(  # pylint: disable=no-member
            Gtk.WindowPosition.CENTER
        )

        # show message box and get result
        result = msg_box.run()  # pylint: disable=no-member
        msg_box.hide()

        # return the button that was clicked
        return result

    # --------------------------------------------------------------------------
    # A convenience method for subclasses to update their control values in the
    # backing store
    # --------------------------------------------------------------------------
    def _update_gui(self):
        """
        A convenience method for subclasses to update their control values in
        the backing store

        This method just hides some implementation details when a window wants
        to update its gui values in the backing store.
        """

        # save size/objects
        self._dict_gui[AC.KEY_WIN_SIZE] = self._get_size()
        self._dict_gui[AC.KEY_WIN_CTLS] = self.get_controls()

        # save backing store to app
        self._app.set_dict_gui(self._name_win, self._dict_gui)

        # update modified status (ignore return)
        self.is_modified()

    # --------------------------------------------------------------------------
    # A convenience method for when the window wants to close
    # --------------------------------------------------------------------------
    def _can_close(self):
        """
        A convenience method for when the window wants to close

        Returns:
            True if we allow the window to close
            False if we do not want the window to close

        This method returns a boolean value which determines whether the window
        closes or not, and possibly saves the current state of the gui to the
        backing store.

        Depending on the window's CLOSE_ACTION, one of three things happens:
        - If CLOSE_ACTION is AC.CLOSE_ACTION_CANCEL, the gui is not saved and
        the method returns False, meaning the window should not close.
        - If CLOSE_ACTION is AC.CLOSE_ACTION_SAVE, the gui is saved and the
        method returns True, allowing the window to close.
        - If CLOSE_ACTION is AC.CLOSE_ACTION_ASK, another decision is made:
            - If the window is not modified, this method returns True, allowing
              the window to close
            - If the window is modified, a dialog is shown to ask the
        user what they want to do.

        When shown, the dialog has 3 buttons: 'Close without saving', 'Cancel',
        or 'Save/Save As...' (Strings are localized). If the user chooses the
        first button, this method will return True, allowing the window to
        close, but losing all changes. If the user chooses the second button,
        the method returns False and the window stays open, with all changes
        intact. If the third button is chosen, the gui is saved to the backing
        store and the method returns True, in which case the window will close.
        """

        # always save size, don't care about gui
        self._dict_gui[AC.KEY_WIN_SIZE] = self._get_size()
        self._app.set_dict_gui(self._name_win, self._dict_gui)

        # get close action for this window
        close_action = self._dict_class.get(
            AC.KEY_CLS_CLOSE_ACTION, AC.DEF_CLOSE_ACTION
        )

        # not modified, allow close
        if not self.is_modified():
            return True

        # don't allow close
        if close_action == AC.CLOSE_ACTION_CANCEL:
            return False

        # save size/controls and allow close
        if close_action == AC.CLOSE_ACTION_SAVE:
            self._update_gui()
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
            self._update_gui()
            return True

        # default response
        return True

    # --------------------------------------------------------------------------
    # A convenience method to format the title when the modified status changes
    # --------------------------------------------------------------------------
    def _format_title(self, is_modified):
        """
        A convenience method to format the title when the modified status
        changes

        Arguments:
            is_modified: Whether to the window controls have been modified

        Change the window title when the backing store title changes, and
        incorporate the modified indicator.
        """

        # by default, just use the regular title
        str_title = self._def_title

        # if you're modded and you know it, clap your hands (and show formatted
        # title)
        show_mod = self._dict_class.get(
            AC.KEY_CLS_SHOW_MOD, AC.DEF_CLS_SHOW_MOD
        )

        # if we are modified and we want to show it
        # NB: we use a param instead of the result of _is_modified to prevent
        # an infinite loop (_is_modified calls this method)
        if is_modified and show_mod:
            # get replacement variables
            mod = self._dict_class.get(
                AC.KEY_CLS_MOD_CHAR, AC.DEF_CLS_MOD_CHAR
            )
            title = self._def_title

            # get the fmt string to replace
            fmt_title = self._dict_class.get(
                AC.KEY_CLS_MOD_FMT, AC.DEF_CLS_MOD_FMT
            )

            # get default new title
            str_title = fmt_title

            # replace each part
            str_title = str_title.replace("${MOD}", mod)
            str_title = str_title.replace("${TITLE}", title)

        # change window title
        self.window.set_title(str_title)

    # --------------------------------------------------------------------------
    # Window events
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when any control in the window is modified
    # --------------------------------------------------------------------------
    def _ctl_event_modified(self, _obj):
        """
        Called when any control in the window is modified

        Arguments:
            _obj: Not used

        Use this method to update the modified status of a control and change
        the modified status of the window. Controls can have multiple handlers,
        so always connect your controls to this handler, as well as
        window-specific handlers for a particular control.
        """

        # get modified value and change window title (ignore return value)
        self.is_modified()

    # --------------------------------------------------------------------------
    # Called when the main window is closed by the 'X' button
    # --------------------------------------------------------------------------
    def _win_event_delete(self, _obj, _event):
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

        # maybe close window
        return not self._can_close()

    # --------------------------------------------------------------------------
    # Called after the window is destroyed
    # --------------------------------------------------------------------------
    def _win_event_destroy(self, _obj):
        """
        Called after the window is destroyed

        Arguments:
            _obj: Not used

        This method is called after the window is destroyed. It is used to
        remove the window from the app's internal list.
        """

        # remove the window from app list
        self._app.remove_instance(self._name_win)


# -)
