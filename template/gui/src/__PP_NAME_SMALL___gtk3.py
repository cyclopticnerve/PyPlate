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

# TODO: save window size/pos/state

# TODO: single instance https://python-gtk-3-tutorial.readthedocs.io/en/latest/application.html

# TODO: there's a lot of strings in here for control names and settings keys?

# the options here are:
# make dict global
# use cli global
# make deep copy of dict

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import os

# complicated imports
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa E402 - import not at top of file

# local imports
# import __PP_NAME_SMALL__ as cli  # noqa E402 - import not at top of file
# from cli import g_dict_config  # noqa E402 - import not at top of file

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_SELF = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

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
    # Public variables
    # --------------------------------------------------------------------------

    # the builder to get gtk objects from
    builder = None

    # the one and only window instance
    winMain = None

    dict_config = None

    # the default wndow title (changes on modified)
    str_default_title = None

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when the main window is closed by the 'X' button
    # --------------------------------------------------------------------------
    def winMain_evt_delete_event(self, obj, event):
        """
            Called when the main window is closed by the 'X' button

            Parameters:
                self [Class]: the class object
                obj [Gtk.Object]: the calling object
                event [Gtk.Event]: not used

            Returns:
                [bool]: opposite of whether we allow the window to close or not
                    Return True to say we handled it (don't close)
                    Return False to say we didn't hadle it (close)

            The Window is about to close via the 'X' button (or some other
            system event, like closing from the overview).
            NB: This method is public so you can do something like an 'Are you
            sure you want to close' or 'Values modified - Save/Close/Cancel'
            dialog.
        """

        # if not modified, no save, just close
        if not self._is_modified():
            return False

        # if auto-save, no ask, just save and close
        if SAVE_ON_EXIT:
            # dict_gui = self.save_gui()
            # cli._save_gui(dict_gui)
            return False

        # I18N: translate these strings
        str_main = 'Save changes before closing?'
        str_sec = 'If you don\'t save, changes will be permanently lost.'
        str_close = 'Close without saving'
        str_cancel = 'Cancel'
        str_save = 'Save'

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
        msgBox.action_area.set_spacing(0)

        # show message box and get result
        response = msgBox.run()
        msgBox.hide()

        # if user chooses close, just close
        if response == CLOSE_WITHOUT_SAVING:
            return False

        # if user chooses cancel, don't close
        elif response == Gtk.ResponseType.CANCEL:
            return True

        # if user chooses yes, save and close
        elif response == Gtk.ResponseType.YES:
            # dict_gui = self.save_gui()
            # cli._save_gui(dict_gui)
            return False

    # --------------------------------------------------------------------------
    # Called when the About button is clicked
    # --------------------------------------------------------------------------
    def winMain_btnAbout_evt_clicked(self, obj):
        """
            Called when the About button is clicked

            Parameters:
                self [Class]: the class object
                obj [GTK.Object]: the calling object

            The About button was clicked. Show the About dialog.
        """

        # get about dialog, run, hide (standrad for reusable modal dialogs)
        dlgAbout = self.builder.get_object('dlgAbout')
        dlgAbout.run()
        dlgAbout.hide()

    # --------------------------------------------------------------------------
    # Called when the Cancel button is clicked
    # --------------------------------------------------------------------------
    def winMain_btnCancel_evt_clicked(self, obj):
        """
            Called when the Cancel button is clicked

            Parameters:
                self [Class]: the class object
                obj [GTK.Object]: the calling object

            The Cancel button was clicked.
        """

        # close main wndow
        self.winMain.destroy()

    # --------------------------------------------------------------------------
    # Called when the OK button is clicked
    # --------------------------------------------------------------------------
    def winMain_btnOK_evt_clicked(self, obj):
        """
            Called when the OK button is clicked

            Parameters:
                self [Class]: the class object
                obj [GTK.Object]: the calling object

            The OK button was clicked.
        """

        # save gui state on close
        if self._is_modified():
            # dict_gui = self.save_gui()
            # cli._save_gui(dict_gui)
            pass

        # close main window
        self.winMain.destroy()

    # --------------------------------------------------------------------------
    # Load the state of all gui objects
    # --------------------------------------------------------------------------

    def load_gui(self):
        """
            Load the state of all gui objects

            Parameters:
                self [Class]: the class object

            Load the state of all gui objects when this method is called.
        """

        # ----------------------------------------------------------------------

        if 'entry' in self.dict_config.keys():
            entTest = self.builder.get_object('winMain_entTest')
            entTest.set_text(self.dict_config['entry'])
        if 'check' in self.dict_config.keys():
            chkTest = self.builder.get_object('winMain_chkTest')
            chkTest.set_active(self.dict_config['check'] == 'True')

        # ----------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Save the state of all gui objects
    # --------------------------------------------------------------------------
    def save_gui(self):
        """
            Save the state of all gui objects

            Parameters:
                self [Class]: the class object

            Return:
                a dict containing the current state of the gui

            Save the state of all gui objects whenever this method is called.
        """

        # create a new, empty dict for control values
        dict_gui = {}

        # ----------------------------------------------------------------------

        # set the property value
        entTest = self.builder.get_object('winMain_entTest')
        dict_gui['entry'] = entTest.get_text()
        chkTest = self.builder.get_object('winMain_chkTest')
        dict_gui['check'] = str(chkTest.get_active())

        # ----------------------------------------------------------------------

        # return the new gui state
        print('-- saved --')
        print(dict_gui)

        return dict_gui

    def tmp_save_gui(self, obj):
        pass

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Called when any control in the window is modified
    # --------------------------------------------------------------------------

    def _winMain_evt_modified(self, obj):
        """
            Called when any control in the window is modified

            Parameters:
                self [Class]: the class object
                obj [GTK.Object]: the calling object

            Use this method to update the modified status of a cntrol and change
            the modified status of the window.
        """

        # get modified state and change window title
        # self._is_modified()
        pass

    # --------------------------------------------------------------------------
    # Called when the Application needs to set if it has been modified
    # --------------------------------------------------------------------------
    def _is_modified(self):
        """
            Called when the Application needs to set if it has been modified

            Parameters:
                self [Class]: the class object

            The Application needs to know if it has been modified. So we create
            a hypothetical save dict, and compare it to the load dict. If there
            are any differences, we have been modified. This method is called
            frequently and is not stored in a variable to prevent caching.
        """

        # defult result
        result = False

        # the new save dict (the current state of the gui)
        dict_gui = self.save_gui()

        # enumerate the keys we will save
        for key in dict_gui.keys():

            # if key is also in load dict
            if key in self.dict_config.keys():

                # compare current value to load value
                val_new = dict_gui[key]
                val_old = self.dict_config[key]

                # if they are different, we are modified
                if val_new != val_old:
                    result = True

        # get the new window title
        str_title = ('*' + self.str_default_title if result
                     else self.str_default_title)

        # change window title
        self.winMain.set_title(str_title)

        # now return result for internal stuff
        return result

    # --------------------------------------------------------------------------
    # Called to set up gui loading in the background
    # --------------------------------------------------------------------------
    def _load_gui(self):

        # global ref to dict
        # global g_dict_config

        # create default dict_config
        # NB: this checks if param passed to constructor is missing or None
        if self.dict_config is None:
            self.dict_config = {}

        # add any missing gui keys (useful when loading empty gui config)
        # NB: doing it this way rather than in the real load means we can be
        # assured that in the real load, we will have all keys present, saving a
        # sanity check line for each control key (which could add up fast!)

        # first get the current gui (just what's set in the ui file)
        dict_gui = self.save_gui()

        # add any missing keys to the incoming dict (using ui vals)
        for key in dict_gui.keys():
            if key not in self.dict_config.keys():
                self.dict_config[key] = dict_gui[key]

    # --------------------------------------------------------------------------
    # Called to set up gui loading in the background
    # --------------------------------------------------------------------------
    # def _save_gui(self, obj):

    #     # # get the current ui status
    #     dict_gui = self.save_gui()

    #     # save that as our new comparison
    #     global g_dict_config
    #     g_dict_config = dict_gui

    #     # check if modified (should always return false)
    #     self._is_modified()
    # #     pass

    # --------------------------------------------------------------------------
    # Called when the Application is activated
    # --------------------------------------------------------------------------
    def _activate(self, obj):
        """
            Called when the Application is activated

            Parameters:
                self [GTK.Class]: the class object
                obj [GTK.Object]: the calling object

            The Application is about to show the Window.
        """

        # I18N: do locale stuff here (see gdrive/projects/common)

        # the builder for this instance (all gui objects referenced from here)
        self.builder = Gtk.Builder()

        # load ui file from path and connect signals
        self.builder.add_from_file(PATH_GUI)
        self.builder.connect_signals(self)

        # create the main window and add to app's window list
        self.winMain = self.builder.get_object('winMain')
        self.add_window(self.winMain)

        # get the initial window title (for modified indicator)
        self.str_default_title = self.winMain.get_title()

        # NB: do load stuff here because controls now defenitely exist

        # this checks if param passed to constructor is missing or None
        # create default dict_config
        if self.dict_config is None:
            self.dict_config = self.save_gui()

        # do private load
        self._load_gui()

        # load the config into the gui
        self.load_gui()

        # show window
        self.winMain.present()

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class to an object/instance
    # --------------------------------------------------------------------------
    def __init__(self, dict_config=None):
        """
            Initialize the class to an object/instance

            Parameters:
                self [GTK.Class]: the class object
                dict_config [dict]: the config dict that holds the current gui
                state (default: None)

            This method is called when a new instance of the class is created,
            i.e 'app = App()'
            NB: You want to do AS LITTLE coding in the init method because the
            whole class my not exist at this point! This is especially important
            for connections. That is why they are deferred to _activate().
        """

        # always call super
        super().__init__(application_id='org.cyclopticnerve.__PP_NAME_SMALL__')

        # save param to class variable
        self.dict_config = dict_config

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
    """

    a_dict = {
        'entry': 'no',
        'check': 'True'
    }

    # run main function
    # app = App()
    # app = App(None)
    # app = App({})
    app = App(a_dict)
    app.run()
    app.save_gui()

# -)
