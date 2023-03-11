#! /usr/bin/env python
# ------------------------------------------------------------------------------
# Project : __CN_NAME_BIG__                                        /          \
# Filename: __CN_NAME_SMALL__-gtk.py                              |     ()     |
# Date    : __CN_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# TODO: flesh this out more once we use it for a gui app
# this is a hot mess
# what level indenting???

# TODO: check for gtk version 3/4
#    does gi.rtepository have a >= ?
#   load ui file based on installed GTK version

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------
import argparse
import os
import sys

from gi.repository import Adw, Gtk
import gi
# TODO: test if v4 exitst, if not use v3
gi.require_version('Adw', '1')
gi.require_version('Gtk', '4.0')

# import main py file
DIR_CURR = os.path.abspath(os.path.dirname(__file__))
up_one = os.path.abspath(os.path.join(DIR_CURR, '..'))
sys.path.insert(1, up_one)
import __CN_NAME_SMALL__.py  # noqa E402 (import not at top of file)

# ------------------------------------------------------------------------------
# Functions
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

    gi.require_version('Adw', '1')
    gi.require_version('Gtk', '4.0')

    # TODO: this will be path to v3 or v4 ui file
    gui_path = 'test.ui'

    # NB: use this if you need to
    # parse args
    # args = _parse_args()

    class MyApp(Adw.Application):

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.connect('activate', self.on_activate)

        def on_activate(self, app):
            builder = Gtk.Builder()
            builder.add_from_file(gui_path)

            win = builder.get_object('window1')
            self.add_window(win)
            win.present()

    MyApp().run()


# ------------------------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Parses the command line
# ------------------------------------------------------------------------------
def _parse_args():
    """
        Parses the command line

        Returns:
            [dict]: A dict of command line options and their values

        This function parses the command line and collates required/optional
        values.
    """

    # always print prog name/version
    print('__CN_NAME_BIG__ version CN_VERSION')

    # create the pasrser
    parser = argparse.ArgumentParser(
        description='CN_SHORT_DESC'
    )

    # add default cmd-line args
    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='CN_VERSION'
    )

    # add any position/optional args\
    _add_args()

    # parse the cmd-line args
    args = parser.parse_args()

    # convert args to dict
    ret_args = vars(args)

    # if no args, print usage
    if len(ret_args) == 0:
        parser.print_usage()

    # return the parsed args
    return ret_args


# ------------------------------------------------------------------------------
# Add arguments to command-line parser
# ------------------------------------------------------------------------------
def _add_args(parser):

    # NB: add args here
    # https://docs.python.org/3/library/argparse.html
    # parser.add_argument(
    #     '--bar'
    # )

    # used in case above code is commented (like pass)
    return


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
