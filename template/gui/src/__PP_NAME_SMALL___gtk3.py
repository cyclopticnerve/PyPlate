# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL___gtk3.py                             |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: Set up a dictionary of control names to config entries This will be used
# to load json into gui, compare current gui to original json, and save gui to
# json
# User data for each control in Glade could be the dictionary key for that
# value
# TODO: there's a lot of strings in here for control names and settings keys?


"""
1. run metadata.py to do xgettext and make .pot file
2. copy .pot file to locale/<lang>/LC_MESSAGES and rename .po
3. edit .po file
4. run msgfmt -o __PP_NAME_SMALL__.mo __PP_NAME_SMALL__.po in
    locale/<lang>/LC_MESSAGES dir

"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import gi
import locale
import os

# complicated imports
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa E402 - import not at top of file

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# the application id to use for GTK
APPLICATION_ID = 'org.cyclopticnerve.__PP_NAME_SMALL__'

# some useful constants
DIR_HOME = os.path.expanduser('~')
DIR_SELF = os.path.dirname(__file__)

# the path to the locale dir
DIR_LOCALE = os.path.join(DIR_SELF, 'locale')

# the path to ui file (even if it is in same dir)
PATH_GUI = os.path.join(DIR_SELF, '__PP_NAME_SMALL___gtk3.ui')

# whether to auto-save gui state on close, or abandon all changes (or ask, like
# through a 'Save' dialog)
SAVE_ON_EXIT = False

# constant for 'Close without saving' dialog button
CLOSE_WITHOUT_SAVING = -69  # Nice

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# get gettext class object and set macro
translator = gettext.translation(
    '__PP_NAME_SMALL__', DIR_LOCALE, fallback=True)
_ = translator.gettext

# ------------------------------------------------------------------------------
# Class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# The main class of the program
# -----------------------------------------------------------------------------


class App(Gtk.Application):
    """
        The main class of the program

        A class that extends Gtk.Application to provide a GUI for the calling
        python script.
    """

    # --------------------------------------------------------------------------
    # Private variables
    # --------------------------------------------------------------------------

    # the _builder to get gtk objects from
    _builder = None

    # the one and only window instance
    _winMain = None

    # the default wndow title (changes on modified)
    _str_default_title = ''

    # the dict of gui control values
    # order of precedence is:
    # 1. values in .ui file
    # 2. this dict
    # 3. dict passed to set_gui()
    _dict_gui = {}

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Sets the property value of _dict_gui
    # --------------------------------------------------------------------------
    def set_gui(self, a_dict):
        """
            Sets the property value of _dict_gui

            Parameters:
                self [GTK.Class]: the class object
                a_dict [dict]: the new property dictionary

            This method sets the _dict_gui property. Must be called before
            run().
        """

        # add new keys/overwrite existing
        # NB: self._dict_gui(): defaults from class def
        #     a_dict:           param passed in above
        # The idea here is to move k/v pairs sent into this method into the
        # self._dict_gui dict. To do that, we assign k/v pairs from the
        # passed-in dict (a_dict) to the existing dict (self._dict_gui). If the
        # keys overlap, precedence is given to the passed-in dict. Otherwise no
        # action is taken and the self._dict_gui k/v remains.

        # for each valid key
        for key in a_dict.keys():

            # add/overwrite key/value
            self._dict_gui[key] = a_dict[key]

    # --------------------------------------------------------------------------
    # Gets the property value of _dict_gui
    # --------------------------------------------------------------------------

    def get_gui(self):
        """
            Gets the property value of _dict_gui

            Parameters:
                self [GTK.Class]: the class object

            Returns:
                [dict]: the current property dictionary

            This method gets the _dict_gui property. Must be called after run().
        """

        # get the instance property
        return self._dict_gui

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the main window is closed by the 'X' button
    # --------------------------------------------------------------------------
    def _winMain_evt_delete_event(self, obj, event):
        """
            Called when the main window is closed by the 'X' button

            Parameters:
                self [Gtk.Class]: the class object
                obj [Gtk.Object]: the calling object
                event [Gtk.Event]: not used

            Returns:
                [bool]: opposite of whether we allow the window to close or not
                    Return True to say we handled it (don't close)
                    Return False to say we didn't handle it (close)

            The Window is about to close via the 'X' button (or some other
            system event, like closing from the overview).

            NB: This method is public so you can do something like an 'Are you
            sure you want to close' or 'Values modified - Save/Close/Cancel'
            dialog.
        """

        # if not modified
        if not self._is_modified():

            # can't save state before _is_modified
            self._save_state()

            # no save, just close
            return False

        # if auto-save, no ask, just save and close
        if SAVE_ON_EXIT:

            # save gui to dict and then save state
            self._dict_gui = self._get_gui()
            self._save_state()

            # and close
            return False

        # create a message dialog
        msgBox = self._get_dialog()

        # show message box and get result
        response = msgBox.run()
        msgBox.hide()

        # if user chooses close, just close
        if response == CLOSE_WITHOUT_SAVING:
            self._save_state()
            return False

        # if user chooses cancel, don't close
        elif response == Gtk.ResponseType.CANCEL:
            return True

        # if user chooses yes, save and close
        else:  # response == Gtk.ResponseType.OK:

            # save gui to dict and then save state
            self._dict_gui = self._get_gui()
            self._save_state()

            # and close
            return False

    # --------------------------------------------------------------------------
    # Called when the About button is clicked
    # --------------------------------------------------------------------------
    def _winMain_btnAbout_evt_clicked(self, obj):
        """
            Called when the About button is clicked

            Parameters:
                self [Gtk.Class]: the class object
                obj [GTK.Object]: the calling object

            The About button was clicked. Show the About dialog.
        """

        # get about dialog, run, hide (standard for reusable modal dialogs)
        dlgAbout = self._builder.get_object('dlgAbout')
        dlgAbout.run()
        dlgAbout.hide()

    # --------------------------------------------------------------------------
    # Called when the Save button is clicked
    # --------------------------------------------------------------------------
    def _winMain_btnSave_evt_clicked(self, obj):
        """
            Called when the Save button is clicked

            Parameters:
                self [Gtk.Class]: the class object
                obj [GTK.Object]: the calling object

            The Save button was clicked.
        """

        # save gui to dict
        self._dict_gui = self._get_gui()

        # update modified status (ignore return)
        self._is_modified()

    # --------------------------------------------------------------------------
    # Called when the Cancel button is clicked
    # --------------------------------------------------------------------------
    def _winMain_btnCancel_evt_clicked(self, obj):
        """
            Called when the Cancel button is clicked

            Parameters:
                self [Gtk.Class]: the class object
                obj [GTK.Object]: the calling object

            The Cancel button was clicked.
        """

        # save state before destroy
        self._save_state()

        # close main wndow
        self._winMain.destroy()

    # --------------------------------------------------------------------------
    # Called when the OK button is clicked
    # --------------------------------------------------------------------------
    def _winMain_btnOK_evt_clicked(self, obj):
        """
            Called when the OK button is clicked

            Parameters:
                self [Gtk.Class]: the class object
                obj [GTK.Object]: the calling object

            The OK button was clicked.
        """

        # save gui to dict
        self._dict_gui = self._get_gui()

        # save state before destroy
        self._save_state()

        # close main window
        self._winMain.destroy()

    # --------------------------------------------------------------------------
    # Called when any control in the window is modified
    # --------------------------------------------------------------------------
    def _winMain_evt_modified(self, obj):
        """
            Called when any control in the window is modified

            Parameters:
                self [Gtk.Class]: the class object
                obj [GTK.Object]: the calling object

            Use this method to update the modified status of a cntrol and change
            the modified status of the window.
        """

        # get modified state and change window title (ignore return value)
        self._is_modified()

    # --------------------------------------------------------------------------
    # Set the state of all gui objects
    # --------------------------------------------------------------------------
    def _set_gui(self):
        """
            Set the state of all gui objects

            Parameters:
                self [Gtk.Class]: the class object

            Set the state of all gui objects from self._dict_gui when this
            method is called. This method is only called once, from _activate().
        """

        # add any missing gui keys (useful when loading empty gui config)
        # NB: doing it this way means we can be assured that we will have all
        # keys present in self._.dict_gui, saving a sanity check line for each
        # control key (which could add up fast!) as well as having a stable
        # starting point for _is_modified().

        # first get the current gui (actual current control values)
        # this gives us a set of needed keys in dict_gui
        dict_gui = self._get_gui()

        # for each key in the current needed gui
        for key in dict_gui.keys():

            # check if key is in wanted gui
            if key in self._dict_gui.keys():

                # if key is present, move it to current ui
                dict_gui[key] = self._dict_gui[key]

        # clear needed/wanted ui
        self._dict_gui = {}

        # move required back to property
        for key in dict_gui.keys():
            self._dict_gui[key] = dict_gui[key]

        # ----------------------------------------------------------------------

        entTest = self._builder.get_object('winMain_entTest')
        entTest.set_text(self._dict_gui['entry'])
        chkTest = self._builder.get_object('winMain_chkTest')
        chkTest.set_active(self._dict_gui['check'] == 'True')

        # ----------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Get the state of all gui objects
    # --------------------------------------------------------------------------
    def _get_gui(self):
        """
            Get the state of all gui objects

            Parameters:
                self [Gtk.Class]: the class object

            Returns:
                [dict]: A dictionary containing the current state of the gui

            Get the state of all gui objects and return it whenever this method
            is called. This method is called from several places, both for
            saving the actual GUI values and also for checking the existance of
            keys.
        """

        dict_gui = {}

        # ----------------------------------------------------------------------

        # NB: here you should set a key/value pair for each control you wish to
        # save/restore
        # this will become the 'template' which will be checked whenever the gui
        # is loaded from a dict, to ensure keys exist for each control
        # values are only important when saving/closing

        # set the property value
        entTest = self._builder.get_object('winMain_entTest')
        dict_gui['entry'] = entTest.get_text()
        chkTest = self._builder.get_object('winMain_chkTest')
        dict_gui['check'] = str(chkTest.get_active())

        # ----------------------------------------------------------------------

        return dict_gui

    # --------------------------------------------------------------------------
    # Create a save dialog for when the window is closed by the 'X' button
    # --------------------------------------------------------------------------
    def _get_dialog(self):
        """
            Create a save dialog for when the window is closed by the 'X' button

            Parameters:
                self [Gtk.Class]: the class object

            Returns:
                [Gtk.MessageDialog]: The dialog to show when the user presses
                the 'X' button

            Create a dialog that has 3 buttons, set their labels/colors, and
            various text labels.
        """

        # before (does not appear in pot)
        # I18N: the main message of the save dialog
        # after
        str_main = _('Save changes before closing?')
        # I18N: the submessage of the save dialog
        str_sec = _('If you don\'t save, changes will be permanently lost.')
        # I18N: the destructive button label (to close without saving)
        str_close = _('Close without saving')
        # I18N: the cancel button label (to do nothing)
        str_cancel = _('Cancel')
        # I18N: the save button label (to save and close)
        str_save = _('Save')

        # create a new message box
        msgBox = Gtk.MessageDialog(text=str_main, secondary_text=str_sec,
                                   message_type=Gtk.MessageType.QUESTION)

        # add buttons to message box
        msgBox.add_buttons(
            str_close, CLOSE_WITHOUT_SAVING,
            str_cancel, Gtk.ResponseType.CANCEL,
            str_save, Gtk.ResponseType.OK
        )

        # make all buttons stretch
        msgBox.action_area.set_homogeneous(True)

        # set the bad-nono button as red
        btnRed = msgBox.get_widget_for_response(
            response_id=CLOSE_WITHOUT_SAVING)
        btnRed_style_context = btnRed.get_style_context()
        btnRed_style_context.add_class('destructive-action')

        # set default button and spacing (neither work)
        msgBox.set_default_response(Gtk.ResponseType.OK)

        # return the dialog
        return msgBox

    # --------------------------------------------------------------------------
    # Saves the window size/state whenever it is closed
    # --------------------------------------------------------------------------
    def _save_state(self):
        """
            Saves the window size/state whenever it is closed

            Parameters:
                self [Gtk.Class]: the class object

            Saves the window size/state to _dict_gui whenever it is closed.
        """

        # get the window
        winMain = self._builder.get_object('winMain')

        # get size from ui file (not actual window, in case we are maximized)
        size = winMain.get_default_size()

        # check if we are maximized
        max = winMain.is_maximized()

        # if not maximized, use current size
        if not max:
            size = winMain.get_size()

        # create a dictionary to hold the size/state
        dict_win_props = {
            'width': f'{size.width}',
            'height': f'{size.height}',
            'max': f'{max}'
        }

        # set the state dict into the gui dict
        self._dict_gui['state'] = dict_win_props

    # --------------------------------------------------------------------------
    # Loads the window size/state whenever it is shown
    # --------------------------------------------------------------------------
    def _load_state(self):
        """
            Loads the window size/state whenever it is shown

            Parameters:
                self [Gtk.Class]: the class object

            Sets the window size/state to _dict_gui whenever it is opened.
        """

        # check for key/sub-dict
        if 'state' in self._dict_gui.keys():

            # get window state if it present
            dict_state = self._dict_gui['state']

            #  get props from dict
            w = dict_state['width']
            h = dict_state['height']
            m = dict_state['max']

            # get the window
            winMain = self._builder.get_object('winMain')

            # set size
            winMain.set_default_size(int(w), int(h))

            # set state
            if m == 'True':
                winMain.maximize()

    # --------------------------------------------------------------------------
    # Called when the Application needs to set if it has been modified
    # --------------------------------------------------------------------------

    def _is_modified(self):
        """
            Called when the Application needs to set if it has been modified

            Parameters:
                self [GtkClass]: the class object

            The Application needs to know if it has been modified. So we create
            a hypothetical save dict, and compare it to the load dict. If there
            are any differences, we have been modified. This method is called
            frequently and is not stored in a variable to prevent caching.
        """

        # defult result
        result = False

        # the new save dict (the current state of the gui)
        dict_gui = self._get_gui()

        # enumerate the keys we will save
        for key in dict_gui.keys():

            # compare current value to load value
            val_new = dict_gui[key]
            val_old = self._dict_gui[key]

            # if they are different, we are modified
            if val_new != val_old:
                result = True

        # get the new window title
        str_title = (f'*{self._str_default_title}' if result
                     else self._str_default_title)

        # change window title
        self._winMain.set_title(str_title)

        # now return result for internal stuff
        return result

    # --------------------------------------------------------------------------
    # Called when the Application is activated (ie first window is shown)
    # --------------------------------------------------------------------------
    def _activate(self, obj):
        """
            Called when the Application is activated (ie first window is shown)

            Parameters:
                self [GTK.Class]: the class object
                obj [GTK.Object]: the calling object

            The Application is about to show the main Window.
        """

        # set the locale to point to the dir
        locale.bindtextdomain('guitest', DIR_LOCALE)

        # the builder for this instance (all gui objects referenced from here)
        self._builder = Gtk.Builder()

        # set the builder to point to domain
        self._builder.set_translation_domain('guitest')

        # load ui file from path and connect signals
        self._builder.add_from_file(PATH_GUI)
        self._builder.connect_signals(self)

        # create the main window and add to app's window list
        self._winMain = self._builder.get_object('winMain')
        self.add_window(self._winMain)

        # get the initial window title (for modified indicator)
        self._str_default_title = self._winMain.get_title()

        # load size/state
        self._load_state()

        # set the config into the controls
        # NB: do set here because controls now defenitely exist
        self._set_gui()

        # show window
        self._winMain.present()

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class to an object/instance
    # --------------------------------------------------------------------------
    def __init__(self):
        """
            Initialize the class to an object/instance

            Parameters:
                self [GTK.Class]: the class object

            This method is called when a new instance of the class is created,
            i.e 'app = App()'
            NB: You want to do AS LITTLE coding in the init method because the
            whole class my not exist at this point! This is especially important
            for connections and loading the gui. That is why they are deferred
            to _activate().
        """

        # always call super
        super().__init__(application_id=APPLICATION_ID)

        # connect default operations for a window
        self.connect('activate', self._activate)


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.

        NB: this is only here so the gui can be run standalone in the debugger
        DO NOT call this file directly
    """

    # run main function
    app = App()
    app.run()

# -)
