#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__.py                                  |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

import argparse
import os

import gi
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')
from gi.repository import Adw, Gtk  # noqa: E402 (import not at top of file)


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
    gui_path = os.path.join(curr_dir, 'gui', '__PP_NAME_SMALL__-gtk4.ui')

    class MyApp(Adw.Application):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.connect('activate', self.on_activate)

        def on_activate(self, app):

            # load file from abs path
            builder = Gtk.Builder(self)
            builder.add_from_file(gui_path)

            # show window
            win = builder.get_object('window1')
            self.add_window(win)
            win.present()

        def clicked(self, obj):
            print('click')

    # show the window
    my_app = MyApp()
    my_app.run()

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Add command line args to the parser
# ------------------------------------------------------------------------------
def add_args(argparser):
    """
        Add command line args to the parser

        Parameters:
            argparser [ArgumentParser]: the argparse object to add args to

        This function adds arguments to the parser. It is teased out to make
        editing command line parameters easier.
    """

    # https://docs.python.org/3/library/argparse.html

    # argparser.add_argument('-f')


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Parse command line args and return the dict
# ------------------------------------------------------------------------------
def _parse_args():
    """
        Parse command line args and return the dict

        Returns:
            [dict]: the dict of commands passed on the command line

        This function gets the command line passed to the program, parses it,
        and returns the command line options as a list.
    """

    # create the parser
    argparser = argparse.ArgumentParser(
        description='A short description'
    )

    # always print prog name/version
    print('GUITest version 0.1.0')

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
if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.
    """

    main()

# -)
