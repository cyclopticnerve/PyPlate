# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnfunctions.py                                        |     ()     |
# Date    : 02/21/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A collection of common functions used by CN software

Functions:
    do_bool: Convert other values, like integers or strings, to bools
    dpretty: Pretty print a dict
    lpretty: Pretty print a list
    pp: Pretty print a dictionary or list
    combine_dicts: Update a dictionary with a second dictionary
    sh: Run a command string in the shell
    load_dicts: Combines dictionaries from all found paths
    save_dict: Save a dictionary to all paths
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import json
import gettext
import shlex
import subprocess

# pylint: disable=import-error

# my imports
from . import cnconstants as C

# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Macros
# ------------------------------------------------------------------------------

_ = gettext.gettext

# ------------------------------------------------------------------------------
# A function to convert bools from other values, like integers or strings
# ------------------------------------------------------------------------------
def do_bool(val):
    """
    Convert other values, like integers or strings, to bools

    Arguments:
        val: The value to convert to a bool

    Returns:
        A boolean value converted from the argument

    Converts integers and strings to boolean values based on the rules.
    """

    # the default result
    res = False

    # if it is in this list, it is True, else false
    # NB: strings here should be all lowercase
    rules_true = [
        "true",
        "1",
        "yes",
        "y",
    ]

    # first convert it to a string (if it isn't already)
    val = str(val)

    # then lowercase it for easier matching
    val = val.lower()

    # find val in dict
    res = val in rules_true

    # return result
    return res


# ------------------------------------------------------------------------------
# Pretty print a dict
# ------------------------------------------------------------------------------
def dpretty(dict_print, indent_size=4, indent_level=0, label=None):
    """
    Pretty print a dict

    Arguments:
        dict_print: The dictionary to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        indent_level: The number of indent levels to use for this part of the
        print process (default: 0)
        label: The string to use as a label (default: None)

    Returns:
        The formatted string to print

    Formats a dictionary nicely so it can be printed to the console.
    """

    # sanity check
    if not isinstance(dict_print, dict):
        # I18N: the parameter type is not a dictionary
        raise OSError(_("dict_print param is not a dict"))

    # default out
    out = ""

    # print label
    if label is not None:
        out += label + "\n"

    # convert indent_size to string and multiply by indent_level
    indent_str = (" " * indent_size) * (indent_level)

    # items will need an extra indent, since they don't recurse
    indent_str_next = (" " * indent_size) * (indent_level + 1)

    # default result opening brace (no indent in case it is nested and is
    # preceded by a key)
    out += indent_str + "{\n"

    # for each entry
    for k, v in dict_print.items():

        # print the key
        out += indent_str_next + f'"{k}": '

        # if the value is a list
        if isinstance(v, list):

            # recurse the value and increase indent level
            ret = (
                lpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            ret = ret.lstrip()
            out += ret

        # if the value is a dict
        elif isinstance(v, dict):

            # recurse the value and increase indent level
            ret = (
                dpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            ret = ret.lstrip()
            out += ret

        # if it is a single entry (str, int, bool)
        else:

            # print the value, quoting it if it is a string
            if isinstance(v, str):
                out += f'"{v}",\n'
            else:
                out += f"{v},\n"

    # get original indent
    indent_str = (" " * indent_size) * indent_level

    # # add closing bracket
    out += indent_str + "},"

    # return result
    return out


# ------------------------------------------------------------------------------
# Pretty print a list
# ------------------------------------------------------------------------------
def lpretty(list_print, indent_size=4, indent_level=0, label=None):
    """
    Pretty print a list

    Arguments:
        list_print: The list to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        indent_level: The number of indent levels to use for this part of the
        print process (default: 0)
        label: The string to use as a label (default: None)

    Returns:
        The formatted string to print

    Formats a list nicely so it can be printed to the console.
    """

    # sanity check
    if not isinstance(list_print, list):
        # I18N: the parameter type is not a list
        raise OSError(_("list_print param is not a list"))

    # default out
    out = ""

    # print label
    if label is not None:
        out += label + "\n"

    # convert indent_size to string and multiply by indent_level
    indent_str = (" " * indent_size) * (indent_level)

    # items will need an extra indent, since they don't recurse
    indent_str_next = (" " * indent_size) * (indent_level + 1)

    # default result opening brace (no indent in case it is nested and is
    # preceded by a key)
    out += indent_str + "[\n"

    # for each entry
    for v in list_print:

        # if the value is a list
        if isinstance(v, list):

            # recurse the value and increase indent level
            ret = (
                lpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            out += ret

        # if the value is a dict
        elif isinstance(v, dict):

            # recurse the value and increase indent level
            ret = (
                dpretty(
                    v,
                    indent_size=indent_size,
                    indent_level=indent_level + 1,
                    label=None,
                )
                + "\n"
            )
            out += ret

        # if it is a single entry (str, int, bool)
        else:

            # print the value, quoting it if it is a string
            if isinstance(v, str):
                out += indent_str_next + f'"{v}",\n'
            else:
                out += indent_str_next + f"{v},\n"

    # get original indent
    indent_str = (" " * indent_size) * indent_level

    # # add closing bracket
    out += indent_str + "],"

    # return result
    return out


# ------------------------------------------------------------------------------
# Pretty print a list or dictionary
# ------------------------------------------------------------------------------
def pp(obj, indent_size=4, label=None):
    """
    Pretty print a dictionary or list

    Arguments:
        obj: The dictionary or list to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        label: The string to use as a label (default: None)

    Formats a dictionary or list nicely and prints it to the console. Note that
    this method includes magic commas in the output, and therefore cannot be
    used to create true JSON-compatible strings. It should only be used for
    debugging.
    """

    # the default result
    result = ""

    # call different pretty functions depending on the object type
    if isinstance(obj, dict):
        result = dpretty(obj, indent_size, 0, label)
    elif isinstance(obj, list):
        result = lpretty(obj, indent_size, 0, label)

    # print the result
    print(result)


# ------------------------------------------------------------------------------
# Update a dictionary with a second dictionary
# ------------------------------------------------------------------------------
def combine_dicts(dict_old, dict_new):
    """
    Update a dictionary with a second dictionary

    Arguments:
        dict_old: The dictionary defined as the one to receive updates
        dict_new: The dictionary containing new keys/values to be updated
        in the old dictionary

    Returns:
        The updated dict_old, filled with updates from dict_new

    This function takes key/value pairs from dict_new and adds/overwrites these
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


# ------------------------------------------------------------------------------
# Run a command string in the shell
# ------------------------------------------------------------------------------
def sh(string):
    """
    Run a command string in the shell

    Arguments:
        string: The string to run

    Returns:
        The result of running the string

    This is just a dumb convenience method to use subprocess with a string
    instead of having to convert a string to an array with shlex every time I
    need to run a shell command.
    """

    # split the string using shell syntax (smart split/quote)
    cmd_array = shlex.split(string)

    # get result of running the shell command
    res = subprocess.run(cmd_array, check=True)

    # return the result
    return res

# --------------------------------------------------------------------------
# Combines dictionaries from all found paths
# --------------------------------------------------------------------------
def load_dicts(paths, dict_=None):
    """
    Combines dictionaries from all found paths

    Arguments:
        paths: The list of file paths to load from
        dict_: The starting dict and final dict after combining (default: None)

    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not a valid JSON file

    Load the dictionaries from all files at all found locations, and
    combine them.
    """

    # set the default result
    if dict_ is None:
        dict_ = {}

    # loop through possible files
    for path in paths:

        # sanity check
        if path is None:
            print(C.CFG_ERR_NOT_EXIST.format(path))
            continue

        # try each option
        try:

            # make sure path is absolute
            if not path.is_absolute:
                print(C.CFG_ERR_NOT_EXIST.format(path))
                continue

            # open the file
            with open(path, "r", encoding="UTF-8") as a_file:
                # load dict from file
                temp_dict = json.load(a_file)

                # combine new dict with previous
                dict_ = combine_dicts(dict_, temp_dict)

        # file not found
        except FileNotFoundError:
            print(C.CFG_ERR_NOT_EXIST.format(path))

        # file mot JSON
        except json.JSONDecodeError:
            print(C.CFG_ERR_NOT_VALID.format(path))

    # return the final dict
    return dict_

# --------------------------------------------------------------------------
# Save a dictionary to all paths
# --------------------------------------------------------------------------
def save_dict(paths, dict_):
    """
    Save a dictionary to all paths

    Arguments:
        paths: the list of file paths to save to
        dict_: the dictionary to save to the file

    Raises:
        OSError: If the file does not exist and can't be created

    Save the dictionary to a file at all the specified locations.
    """

    # loop through possible files
    for path in paths:

        # try each option
        try:

            # make sure path is absolute
            if not path.is_absolute():
                print(C.CFG_ERR_NOT_CREATE.format(path))
                continue

            # first make dirs
            path.parent.mkdir(parents=True, exist_ok=True)

            # open the file
            with open(path, "w", encoding="UTF-8") as a_file:
                # save dict tp file
                json.dump(dict_, a_file, indent=4)

            # it worked, done here
            return

        # raise an OS Error
        except OSError:
            print(C.CFG_ERR_NOT_CREATE.format(path))

# -)
