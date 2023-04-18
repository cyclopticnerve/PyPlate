#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: __PP_NAME_SMALL__.py                                  |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: flesh this out more once we use it for a gui app
# this is a hot mess
# what level indenting???

# TODO: init controls in window
# TODO: set handler to class?

# TODO: move handler class to seperate file
#     how to avoid circular imports?

# TODO: check for gtk version 3/4
#   does gi.rtepository have a >= ?
#   load ui file based on installed GTK version

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import argparse
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk  # noqa: E402 (module import not at top of file)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------


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

    class __PP_NAME_BIG__App(Gtk.Application):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.connect('activate', self.on_activate)

        def on_activate(self, app):

            # load file from abs path
            builder = Gtk.Builder()
            builder.add_from_file('__PP_NAME_SMALL__-gtk3.ui')
            builder.connect_signals(self)

            # show window
            winMain = builder.get_object('__PP_NAME_SMALL__.winMain')
            self.add_window(winMain)
            winMain.present()

        # def clicked(self, obj):
        #     print('click')

    # show the window
    __PP_NAME_SMALL__App = __PP_NAME_BIG__App()
    __PP_NAME_SMALL__App.run()

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

    # convert agrs to dict
    arg_dict = vars(args)

    # return the object for inspection
    return arg_dict


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
