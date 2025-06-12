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
    pascal_case: Convert a class name to it's Pascal equivalent
    do_bool: Convert other values, like integers or strings, to bools
    dpretty: Pretty print a dict
    lpretty: Pretty print a list
    pp: Pretty print a dictionary or list
    combine_dicts: Update a dictionary with one or more dictionaries
    sh: Run a command string in the shell
    load_dicts: Combines dictionaries from all found paths
    save_dict: Save a dictionary to all paths
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import json
from pathlib import Path
import shlex
import subprocess

# ------------------------------------------------------------------------------
# Constant strings
# ------------------------------------------------------------------------------

S_ERR_NOT_DICT = "dpretty object is not a dict"
S_ERR_NOT_LIST = "lpretty object is not a list"
S_ERR_NOT_DICT_OR_LIST = "pp object is not a dict or list"
S_ERR_SHELL = "shell process failed"
# NB: format param is dict file path
S_ERR_NOT_EXIST = "dict file '{}' does not exist"
# NB: format param is dict file path
S_ERR_NOT_VALID = "dict file '{}' is not a valid JSON file"
# NB: format param is dict file path
S_ERR_NOT_CREATE = "dict file '{}' could not be created"

# if it is in this list, it is True, else false
# NB: strings here should be all lowercase
L_RULES_TRUE = [
    "true",
    "1",
    "yes",
    "y",
]

# ------------------------------------------------------------------------------
# Public methods
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Format a string in Pascal case
# ------------------------------------------------------------------------------
def pascal_case(a_str):
    """
    Format a string in Pascal case

    Args:
        a_str: A string to convert to Pascal case

    Returns;
        The Pascal cased string

    Formats the given string to a Pascal case equivalent, ie. "my_class"
    becomes "MyClass".
    """

    # do formatting
    name_pascal = a_str
    name_pascal = name_pascal.replace("_", " ")
    name_pascal = name_pascal.replace("-", " ")
    name_pascal = name_pascal.title()
    name_pascal = name_pascal.replace(" ", "")

    # return result
    return name_pascal


# ------------------------------------------------------------------------------
# Convert other values, like integers or strings, to bools
# ------------------------------------------------------------------------------
def do_bool(val):
    """
    Convert other values, like integers or strings, to bools

    Args:
        val: The value to convert to a bool

    Returns:
        A boolean value converted from the argument

    Converts integers and strings to boolean values based on the rules.
    """

    # lower all test vals
    rules_true = [item.lower() for item in L_RULES_TRUE]

    # return result
    return str(val).lower() in rules_true


# ------------------------------------------------------------------------------
# Pretty print a dict
# ------------------------------------------------------------------------------
def dpretty(dict_print, indent_size=4, indent_level=0, label=None):
    """
    Pretty print a dict

    Args:
        dict_print: The dictionary to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        indent_level: The number of indent levels to use for this part of the
        print process (default: 0)
        label: The string to use as a label (default: None)

    Returns:
        The formatted string to print

    Raises:
        OSError if the first param is not a dict

    Formats a dictionary nicely so it can be printed to the console.
    """

    # sanity check
    if not isinstance(dict_print, dict):
        raise OSError(S_ERR_NOT_DICT)

    # default out
    out = ""

    # print label
    if label is not None:
        out += label + ": "

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
    out += indent_str + "}"

    # return result
    return out


# ------------------------------------------------------------------------------
# Pretty print a list
# ------------------------------------------------------------------------------
def lpretty(list_print, indent_size=4, indent_level=0, label=None):
    """
    Pretty print a list

    Args:
        list_print: The list to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        indent_level: The number of indent levels to use for this part of the
        print process (default: 0)
        label: The string to use as a label (default: None)

    Returns:
        The formatted string to print

    Raises:
        OSError if the first param is not a list

    Formats a list nicely so it can be printed to the console.
    """

    # sanity check
    if not isinstance(list_print, list):
        raise OSError(S_ERR_NOT_LIST)

    # default out
    out = ""

    # print label
    if label is not None:
        out += label + ": "

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
    out += indent_str + "]"

    # return result
    return out


# ------------------------------------------------------------------------------
# Pretty print a list or dictionary
# ------------------------------------------------------------------------------
def pp(obj, indent_size=4, label=None):
    """
    Pretty print a dictionary or list

    Args:
        obj: The dictionary or list to print
        indent_size: The number of spaces to use for each indent level
        (default: 4)
        label: The string to use as a label (default: None)

    Returns:
        The object formatted for printing

    Raises:
        OSError if the first param is not a dict or list

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
    else:
        raise OSError(S_ERR_NOT_DICT_OR_LIST)

    # print the result
    print(result)


# ------------------------------------------------------------------------------
# Update a dictionary with entries from another dict
# ------------------------------------------------------------------------------
def combine_dicts(dicts_new, dict_old=None):
    """
    Update a dictionary with entries from another dict

    Args:
        dicts_new: A dictionary or list of dictionaries containing new
        keys/values to be updated in the old dictionary
        dict_old: The dictionary defined as the one to receive updates

    Returns:
        The updated dict_old, filled with updates from dict_new

    This function takes key/value pairs from each of the new dicts and
    adds/overwrites these keys and values in dict_old, preserving any values
    that are blank or None in dict_new. It is also recursive, so a dict or list
    as a value will be handled correctly.
    """

    # default return val
    if dict_old is None:
        dict_old = {}

    # sanity check
    if isinstance(dicts_new, dict):
        dicts_new = [dicts_new]
    if len(dicts_new) == 0:
        return dict_old
    if not dict_old:
        dict_old = {}

    # go through the new dicts in order
    for dict_new in dicts_new:

        # for each k,v pair in dict_n
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
                    dict_old[k] = combine_dicts([v], dict_old[k])

                # if the value is a list
                elif isinstance(v, list):
                    list_old = dict_old[k]
                    for list_item in v:
                        list_old.append(list_item)

                # if the value is not a dict or a list
                else:
                    # just copy value from one dict to the other
                    dict_old[k] = v

    # return the updated dict_old
    return dict_old


# ------------------------------------------------------------------------------
# Run a program or command string in the shell
# ------------------------------------------------------------------------------
def sh(cmd, shell=False):
    """
    Run a program or command string in the shell

    Args:
        cmd: The command line to run
        shell: If False (the default), run the cmd as one long string. If True,
        split the cmd into separate arguments

    Returns:
        The result of running the command line, as a
        subprocess.CompletedProcess object

    This is just a dumb convenience method to use subprocess with a string
    instead of having to convert a string to an array with shlex every time I
    need to run a shell command.
    """

    # make sure it's a string (sometime pass path object)
    cmd = str(cmd)

    # split the string using shell syntax (smart split/quote)
    # NB: only split if running a file - if running a shell cmd, don't split
    if not shell:
        cmd = shlex.split(cmd)

    # get result of running the shell command or bubble up an error
    try:
        res = subprocess.run(
            # the array of commands produced by shlex.split
            cmd,
            # if check is True, an exception will be raised if the return code
            # is not 0
            # if check is False, no exception is raised but res will be None,
            # meaning you have to test for it in the calling function
            # but that also means you have no information on WHY it failed
            check=True,
            # convert stdout/stderr from bytes to text
            text=True,
            # put stdout/stderr into res
            capture_output=True,
            # whether the call is a file w/ params (False) or a direct shell
            # input (True)
            shell=shell,
        )

    # check if it failed
    except subprocess.CalledProcessError as e:
        raise OSError(S_ERR_SHELL) from e

    # return the result
    return res


# ------------------------------------------------------------------------------
# Combines dictionaries from all found paths
# ------------------------------------------------------------------------------
def load_dicts(paths, start_dict=None):
    """
    Combines dictionaries from all found paths

    Args:
        paths: The file path or list of file paths to load
        start_dict: The starting dict and final dict after combining (default:
        None)

    Returns:
        The final combined dictionary

    Raises:
        FileNotFoundError: If the file does not exist
        json.JSONDecodeError: If the file is not a valid JSON file

    Load the dictionaries from all files and use combine_dicts to combine them.
    """

    # sanity check
    if isinstance(paths, (str, Path)):
        paths = [paths]

    # set the default result
    if start_dict is None:
        start_dict = {}

    # loop through possible files
    for path in paths:

        # sanity check
        path = Path(path).resolve()

        # sanity check
        if path is None or not path.exists():
            print(S_ERR_NOT_EXIST.format(path))
            continue

        # try each option
        try:

            # open the file
            with open(path, "r", encoding="UTF-8") as a_file:
                # load dict from file
                new_dict = json.load(a_file)

                # combine new dict with previous
                start_dict = combine_dicts([new_dict], start_dict)

        # file not JSON
        except json.JSONDecodeError as e:
            raise OSError(S_ERR_NOT_VALID.format(path)) from e

    # return the final dict
    return start_dict


# ------------------------------------------------------------------------------
# Save a dictionary to all paths
# ------------------------------------------------------------------------------
def save_dict(a_dict, paths):
    """
    Save a dictionary to all paths

    Args:
        a_dict: The dictionary to save to the file
        paths: The path or list of paths to save to

    Raises:
        OSError: If the file does not exist and can't be created

    Save the dictionary to a file at all the specified locations.
    """

    # sanity check
    if isinstance(paths, (str, Path)):
        paths = [paths]

    # loop through possible files
    for path in paths:

        # sanity check
        path = Path(path).resolve()

        # try each option
        try:

            # make sure path is absolute
            if not path.is_absolute():
                print(S_ERR_NOT_CREATE.format(path))
                continue

            # first make dirs
            path.parent.mkdir(parents=True, exist_ok=True)

            # open the file
            with open(path, "w", encoding="UTF-8") as a_file:
                # save dict tp file
                json.dump(a_dict, a_file, indent=4)

        # raise an OS Error
        except OSError as e:
            raise OSError(S_ERR_NOT_CREATE.format(path)) from e


# -)
