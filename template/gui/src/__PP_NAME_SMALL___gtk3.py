# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL___gtk3.py                             |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: load controls - called from here or owner py?
# TODO: save controls - called from here or owner py?
# TODO: pass file path to constructor to use in load/save controls

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import os
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402 (import not at top of file)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# this is the dir where the script is being run from
# # (e.g. ~/Documents/Projects/Python/Apps/__PP_NAME_BIG__)
DIR_CURR = os.path.dirname(__file__)

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# The main class of the program
# ------------------------------------------------------------------------------
class App(Gtk.Application):
    """
        The main class of the program

        A class that extends Gtk.Application to provide a GUI for the calling
        python script.
    """

    # --------------------------------------------------------------------------
    # Public variables
    # --------------------------------------------------------------------------
    builder = None

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Load the state of all gui objects when the main window is shown
    # --------------------------------------------------------------------------
    def winMain_load(self, obj):
        """
            Load the state of all gui objects when the main window is shown

            Parameters:
                self [Class]: the class object
                obj [object]: the Gtk object to init

            Load the state of all gui objects when the main window is shown
        """

        pass

    # --------------------------------------------------------------------------
    # Save the state of all gui objects when the main window is closed
    # --------------------------------------------------------------------------
    def winMain_save(self, obj):
        """
            Save the state of all gui objects when the main window is closed

            Parameters:
                self [Class]: the class object
                obj [object]: the Gtk object to save

            Save the state of all gui objects when the main window is closed
        """

        pass

    # --------------------------------------------------------------------------
    # Called to get a button's text
    # --------------------------------------------------------------------------
    def winMain_bntAbout_get_label(self, obj):
        """
            Called to get an object's property

            Parameters:
                self [Class]: the class object
                obj [object]: the Gtk object to get a property from

            Get a GTK object's property (such as its text).
        """

        if obj is None:

            # using builder to get obj (useful for common methods)
            btnAbout = self.builder.get_object('winMain_btnAbout')
            print(btnAbout.get_label())
        else:

            # using specific object
            print(obj.get_label())

    # --------------------------------------------------------------------------
    # Called to set a button's text
    # --------------------------------------------------------------------------
    def winMain_bntAbout_set_label(self, obj):
        """
            Called to set an object's property

            Parameters:
                self [Class]: the class object
                obj [object]: the Gtk object to set a property on

            Set a GTK object's property (such as its text).
        """

        if obj is None:

            # using builder to get obj (useful for common methods)
            btnAbout = self.builder.get_object('winMain_btnAbout')
            btnAbout.set_label('foobar')
        else:

            # using specific object
            obj.set_label('foobar')

    # --------------------------------------------------------------------------
    # Called when a button is clicked
    # --------------------------------------------------------------------------
    def winMain_btnAbout_evt_clicked(self, obj):
        """
            Called when an event happens on a GTK object

            Parameters:
                self [Class]: the class object
                obj [object]: the Gtk object that the event was generated for

            The GTK object had an event happen.
        """

        # get/set the object's properties
        btnAbout = self.builder.get_object('winMain_btnAbout')
        self.winMain_bntAbout_get_label(btnAbout)
        # self.winMain_bntAbout_set_label(btnAbout)

        # get about dialog, run, hide (standrad for reusable dialogs)
        dlgAbout = self.builder.get_object('dlgAbout')
        dlgAbout.run()
        dlgAbout.hide()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class to an object/instance
    # --------------------------------------------------------------------------
    def __init__(self, **kwargs):
        """
            Initialize the class to an object/instance

            Parameters:
                self [Class]: the class object
                **kwargs [dict]: the dict of parameters passes to the __init__
                function

            This method is called when a new instance of the class is created.
            NB: You want to do AS LITTLE coding in the init method because the
            whole class my not exist at this point! This is especially important
            for connections.
        """

        # always call super
        super().__init__(**kwargs)

        # connect default operations for a window
        self.connect('activate', self._activate)

    # --------------------------------------------------------------------------
    # Called when the main window is shown
    # --------------------------------------------------------------------------
    def _activate(self, app):
        """
            Called when the main window is shown

            Parameters:
                self [Class]: the class object
                app [Gtk.Application]: the Application object

            The Application is about to show the Window.
        """

        # the builder for this instance (all gui objects referenced from here)
        self.builder = Gtk.Builder()

        # get path to ui file
        path_gui = os.path.join(DIR_CURR, 'guitest_gtk3.ui')

        # load file from path
        self.builder.add_from_file(path_gui)
        self.builder.connect_signals(self)

        # show window
        winMain = self.builder.get_object('winMain')
        self.add_window(winMain)
        winMain.present()

# -)
