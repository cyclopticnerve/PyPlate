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

# system imports
import argparse
import json
import os

# local imports
import __PP_NAME_SMALL___gtk3 as gui

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_SELF = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

# the key in args for the config file (shown in help)
PATH_CONFIG_ARG = 'PATH_CONFIG'

# the path to the default config file
PATH_CONFIG_DEF = os.path.join(DIR_HOME, '.config', '__PP_NAME_BIG__',
                               'config.json')

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# args are global so we can read them from any function
# they are only set once, in __name__()
g_dict_args = {}

# the global config dict (built-in or loaded from config file)
# they are set twice (once in load_config(), and again in _save_gui()
# order of precedence is:
# 1. this definition
# 2. file at PATH_CONFIG_DEF
# 3. command line flag -c
g_dict_config = {}


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
        program, and performing its steps.
    """

    # call the steps in order
    print(func())

    # show the window (with config dict)
    # NB: app.run() blocks so only put code after this that you want to run
    # AFTER the window is closed
    # check if there is a 'gui' sub-dict
    # if 'gui' in g_dict_config.keys():
    #     app = gui.App(g_dict_config['gui'])
    # else:
    #     app = gui.App()
    # app.run()

    app = gui.App()
    app.laod_gui(a_dict)
    app.run()
    new_dict = app.save_gui()


# ------------------------------------------------------------------------------
# Short description
# ------------------------------------------------------------------------------
def func():
    """
        Short description

        Parameters:
            var_name [type]: description

        Returns:
            [type]: description

        Raises:
            exception_type(vars): description

        Long description (including HTML).
    """

    return ('this is func')


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

    # argparser.add_argument('-c', dest=PATH_CONFIG_ARG)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Parse command line args and set the global dict
# ------------------------------------------------------------------------------
def _parse_args():
    """
        Parse command line args and set the global dict

        This function gets the command line passed to the program, parses it,
        and sets the command line options as a global dict.
    """

    global g_dict_args

    # create the parser
    argparser = argparse.ArgumentParser(
        description='PP_SHORT_DESC'
    )

    # always print prog name/version
    print('__PP_NAME_BIG__ version PP_VERSION')

    # add arguments from the function above
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
    g_dict_args = vars(args)


# ------------------------------------------------------------------------------
# Load config file from specified path
# ------------------------------------------------------------------------------
def _load_config(path):
    """
        Load config file from specified path

        Parameters:
            path [string]: the path to the config file to load from

        Raises:
            Exception(str): if the file is not valid JSON

        Load the global config from a file at the specified location.
    """

    # the dictionary to load to
    global g_dict_config

    # sanity check
    if path is None or not os.path.isfile(path):
        return

    # open the file for reading
    try:
        with open(path, 'r', encoding='utf8') as f:
            g_dict_config = json.load(f)
    except (Exception):
        raise Exception(f'_load_config: "{path}" is not a valid JSON file')


# ------------------------------------------------------------------------------
# Save config file to specified path
# ------------------------------------------------------------------------------
def _save_config(path):
    """
        Save config file to specified path

        Parameters:
            path [string]: the path to the config file to save to

        Raises:
            Exception(str): if the file does not exist and can't be created

        Save the global config to a file at the specified location.
    """

    # sanity check
    if path is None or path == '':
        return

    # open the file for writing (and create if it doesn't exist)
    try:

        # first make dirs
        dir_config = os.path.dirname(path)
        if dir_config != '':
            os.makedirs(dir_config, exist_ok=True)

        # then write to file
        with open(path, 'w', encoding='utf8') as f:
            json.dump(g_dict_config, f)
    except (Exception):
        raise Exception(f'_save_config: "{path}" cannot be created')


# ------------------------------------------------------------------------------
# Callback from gui to save state
# ------------------------------------------------------------------------------
def _save_gui(a_dict):
    """
        Callback from gui to save state

        Parameters:
            a_dict [dict]: the dictionary of gui settings to save

        This function gets the gui state as a dictionary, and saves it to a
        file.
    """

    # save gui config to section
    global g_dict_config
    g_dict_config['gui'] = a_dict

    # NB: the actual file save is done after app.run() ends


# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    """
        Code to run when called from command line

        This is the top level code of the program, called when the Python file
        is invoked from the command line.
    """

    # create our one set of args
    _parse_args()

    # TODO: we could try to make a rock-solid path (or None) here

    # set defualt path
    path = PATH_CONFIG_DEF

    # check if there is an arg for config path
    if PATH_CONFIG_ARG in g_dict_args.keys():

        arg_path = g_dict_args[PATH_CONFIG_ARG]
        if arg_path is not None and arg_path != '':

            # load from the arg path
            path = g_dict_args[PATH_CONFIG_ARG]

    # load config dict from file (or just keep built-in)
    _load_config(path)

    # run main function
    main()

    # save config dict to file
    _save_config(path)

# -)
