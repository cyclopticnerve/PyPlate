#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__-gtk4.py                             |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

""" 
This is a module to present a GUI interface using GTK4

This is a file to present a GTK4 window in a GUI program. It is not ready for
primetime yet. It should be closely coupled to any gtk3 files that are known to
work.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import argparse
import os

# PyGObject imports
# import gi

# gi.require_version("Adw", "1")
# gi.require_version("Gtk", "4.0")
# from gi.repository import Adw, Gtk

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# The main function of the program
# ------------------------------------------------------------------------------
def main():
    """
    The main function of the program

    This function is the main entry point for the program, initializing the
    GUI and attaching it to the underlying Python program.
    """

    # NB: uncomment this line and add args to _add_args()
    # args = _parse_args()

    # ------------------------------------------------------------------------------

    curr_dir = os.path.dirname(__file__)
    gui_path = os.path.join(curr_dir, "gui", "__PP_NAME_SMALL__-gtk4.ui")

    class MyApp(Adw.Application):
        """
        class docstring
        """

        def __init__(self, **kwargs):
            """
            func docstring
            """

            super().__init__(**kwargs)
            self.connect("activate", self.on_activate)

        def on_activate(self, _app):
            """
            func docstring
            """

            # load file from abs path
            builder = Gtk.Builder(self)
            builder.add_from_file(gui_path)

            # show window
            win = builder.get_object("window1")
            self.add_window(win)
            win.present()

        def clicked(self, _obj):
            """
            func docstring
            """

            print("click")

    # show the window
    my_app = MyApp()
    my_app.run()


# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Add command line args to the parser
# ------------------------------------------------------------------------------
def add_args(_argparser):
    """
    Adds command line args to the parser

    Args:
        argparser: The argparse object to add args to

    This function adds arguments to the parser. It is teased out to make
    editing command line arguments easier.
    """

    # https://docs.python.org/3/library/argparse.html

    # _argparser.add_argument('-f')


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Parse command line args and return the dict
# ------------------------------------------------------------------------------
def _parse_args():
    """
    Parses command line args and return the dict

    Returns:
        The dict of commands passed on the command line

    This function gets the command line passed to the program, parses it,
    and returns the command line options as a list.
    """

    # create the parser
    argparser = argparse.ArgumentParser(description="A short description")

    # always print prog name/version
    print("GUITest version 0.1.0")

    # add arguments here
    add_args(argparser)

    # parse the arg list into a Namespace object (similar to dict)
    # NB: if there is an error in the command line, this function will:
    # 1. print usage
    # 2. print the error
    # 3. exit
    args = argparser.parse_args()

    # if we made it this far, cmd line is ok so print usage
    argparser.print_usage()

    # convert args to dict
    dict_args = vars(args)

    # return the object for inspection
    return dict_args


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":

    # run the main function
    main()

# -)
