# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: functions.py                                          |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : __PP_AUTHOR__                                         |   \____/   |
# License : __PP_LICENSE_NAME__                                    \          /
# ------------------------------------------------------------------------------

"""
A file to hold common functions for the rest of the application

Functions:
    doo_bool: A function to convert bools from other values, like integers or
    strings
    get_ctl_type: A convenience method to return the type of a control, parsed
    from the class control set
    sanitize_gui(): Called when a gui dict is passed in, to ensure all values
    are of the correct type.
    pretty: A convenience method to pretty print a dict
    combine_dicts: Updates a dictionary with new values and missing key/value
    pairs from a second dictionary
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# local imports
from . import constants as C  # pylint: disable=import-error

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Strings
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A function to convert bools from other values, like integers or strings
# ------------------------------------------------------------------------------
def do_bool(val):
    """
    A function to convert bools from other values, like integers or strings

    Arguments:
        val: the value to convert to a bool

    Returns:
        A boolean value converted from the argument

    Converts integers and strings to boolean values based on the rules.
    """

    # if it is an integer, these values == True
    rules_true = [
        "true",
        "1",
        "yes",
        "y",
    ]

    # find val in dict
    val = str(val).lower() in rules_true

    # return bool
    return val


# --------------------------------------------------------------------------
# A convenience method to return the type of a control, parsed from the
# class control set
# --------------------------------------------------------------------------
def get_ctl_type(class_dict, ctl_name):
    """
    A convenience method to return the type of a control, parsed from the
    class control set

    Arguments:
        class_dict: the dict of common class properties
        ctl_name: the control whose type we want to know

    Returns the control type for a specified control in a specified class,
    so that we can determine setter/getter methods as well as the value
    type. The result is one of constants.CTL_TYPE_...
    """

    # get controls for class
    class_ctls = class_dict.get(C.KEY_CLS_CTLS, {})

    # get control type
    dict_ctl = class_ctls.get(ctl_name, {})
    ctl_type = dict_ctl.get(C.KEY_CTL_TYPE, C.CTL_TYPE_TEXT)

    # return the type
    return ctl_type

# ------------------------------------------------------------------------------
# Called when the gui dict is passed in, to ensure all values are of the
# correct type
# ------------------------------------------------------------------------------
def sanitize_gui(dict_class, dict_gui):
    """
    Called when a gui dict is passed in, to ensure all values are of
    the correct type

    Arguments:
        dict_class: The dict_app entry for this window's class
        dict_gui: The dict to sanitize

    Returns:
        The sanitized dict
    """

    # do visibility
    # NB: do not use get, if it's empty, skip and leave it empty
    if C.KEY_WIN_VISIBLE in dict_gui:
        val = dict_gui[C.KEY_WIN_VISIBLE]
        val = do_bool(val)
        dict_gui[C.KEY_WIN_VISIBLE] = val

    # check if size dict exists
    # NB: do not use get, if it's empty, skip and leave it empty
    if C.KEY_WIN_SIZE in dict_gui:
        # get the size dict
        dict_size = dict_gui[C.KEY_WIN_SIZE]

        # fix width
        w = dict_size[C.KEY_SIZE_W]
        dict_size[C.KEY_SIZE_W] = int(w)

        # fix height
        h = dict_size[C.KEY_SIZE_H]
        dict_size[C.KEY_SIZE_H] = int(h)

        # fix max
        m = dict_size[C.KEY_SIZE_M]
        dict_size[C.KEY_SIZE_M] = do_bool(m)

        # put it back
        dict_gui[C.KEY_WIN_SIZE] = dict_size

    # check if controls dict exists
    # NB: do not use get, if it's empty, skip and leave it empty
    if C.KEY_WIN_CTLS in dict_gui:
        # get the window's controls dict
        dict_ctls = dict_gui[C.KEY_WIN_CTLS]

        # for each control
        for k, v in dict_ctls.items():
            # get value type from control type
            ctl_type = get_ctl_type(dict_class, k)
            val_type = ctl_type.get(C.KEY_CTL_VAL_TYPE, None)

            # get the val from the user dict
            val = v.get(C.KEY_CTL_VAL, "")

            # convert int
            if val_type == C.CTL_VAL_TYPE_INT:
                val = int(val)

            # convert bool
            elif val_type == C.CTL_VAL_TYPE_BOOL:
                val = do_bool(val)

            # update controls dict
            dict_ctls[k][C.KEY_CTL_VAL] = val

        # update window dict
        dict_gui[C.KEY_WIN_CTLS] = dict_ctls

    # return updated dict
    return dict_gui

# ------------------------------------------------------------------------------
# Convenience function to pretty print a dict
# ------------------------------------------------------------------------------
def pretty(dict_print, indent_size=4, indent_level=0):
    """
    Convenience function to pretty print a dict

    Arguments:
        dict_print: The dictionary to print
        indent_size: The number of spaces to use for each indent level
        indent_level: The number of indent levels to use for this part of the
        print process

    Returns:
        The formatted string to print

    Formats a dictionary nicely so it can be printed to the console. Note that
    this method includes magic commas in the output, and therefore cannot be
    used to create true JSON-compatible strings. It should only be used for
    debugging.
    """

    # sanity check
    if not isinstance(dict_print, dict):
        raise OSError("dict_print param is not a dict")

    # convert indent_size to string and multiply by indent_level
    # NB: add 1 so the first indent is actually indented (assuming default
    # level is 0)
    indent_str = (" " * indent_size) * (indent_level + 1)

    # lists will need an extra indent, since they don't recurse
    indent_str_list = (" " * indent_size) * (indent_level + 2)

    # default result opening brace (no indent in case it is nested and is
    # preceded by a key)
    out = "{\n"

    # for each entry
    for k, v in dict_print.items():

        # if the value is a dict
        if isinstance(v, dict):

            # concat the key and opening brace
            out += indent_str + f'"{k}": '

            # recurse the value and increase indent level
            out += pretty(v, indent_level=indent_level + 1) + "\n"

        # if the value is a list
        elif isinstance(v, list):

            # print the key and opening bracket
            out += indent_str + f'"{k}": [\n'

            # print the values
            for item in v:
                if isinstance(item, str):
                    out += indent_str_list + f'"{item}",\n'
                else:
                    out += indent_str_list + f"{item},\n"

        # if it is a single entry (str, int, bool)
        else:
            # print the key
            out += indent_str + f'"{k}": '

            # print the value, quoting it if it is a string
            if isinstance(v, str):
                out += f'"{v},"\n'
            else:
                out += f"{v},\n"

    # get original indent
    indent_str = (" " * indent_size) * indent_level

    # # add closing bracket
    out += indent_str + "},"

    # return result
    return out


# ------------------------------------------------------------------------------
# Updates a dictionary with new values and missing key/value pairs from a
# second dictionary
# ------------------------------------------------------------------------------
def combine_dicts(dict_old, dict_new):
    """
    Updates a dictionary with new values and missing key/value pairs from a
    second dictionary

    Arguments:
        dict_old: The dictionary defined as the one to receive updates
        dict_new: The dictionary containing new keys/values to be updated
        in the old dictionary

    Returns:
        The updated dict_old, filled with updates from dict_new

    This function takes keys/values from dict_new and adds/overwrites these
    keys and values in dict_old, preserving any values that are blank or
    None in dict_new.
    """

    # sanity check
    if dict_new is None:
        return dict_old

    # for each k,v pair in dict_new
    for k, v in dict_new.items():
        # copy whole value if key is missing
        if not k in dict_old:
            dict_old[k] = v

        # if the key is present in both
        else:
            # if the value is a dict
            if isinstance(v, dict):
                # start recursing
                # recurse using the current key and value
                dict_old[k] = combine_dicts(dict_old[k], v)

            # if the value is not a dict
            else:
                # just copy value from one dict to the other
                dict_old[k] = v

    # return the updated dict_old
    return dict_old


# -)
