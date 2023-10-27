# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: cntree.py                                             |     ()     |
# Date    : 08/06/2023                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module creates a tree of the specified directory, with paths being
ignored by the filter list and names being formatted according to the
specified formats.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path


# ------------------------------------------------------------------------------
# Generate a file tree in text format with the names formatted according to some
# format strings
# ------------------------------------------------------------------------------
class CNTree:
    """
    Generate a file tree in text format with the names formatted according to
    some format strings

    This class builds the tree as a complete string, ready to be printed to
    stdout or a file.

    Methods:
        build_tree(): Creates the new tree and returns its items as a string
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # NB: these all start with underscores so they don't show in docs

    # these are the console/terminal values for the individual
    # prefix/connector chars
    _CHAR_VERT = "\u2502"  # vertical join (pipe)
    _CHAR_HORZ = "\u2500"  # horizontal join (full-width dash)
    _CHAR_TEE = "\u251C"  # tee join (not last item)
    _CHAR_ELL = "\u2514"  # elbow join (last item)
    _CHAR_SPACE = " "  # single space char

    # these are the preset char sequences for the prefix/connector char sets
    # NB: these must always be equal length
    _PREFIX_VERT = f"{_CHAR_VERT}{_CHAR_SPACE}"  # next level ("| ")
    _PREFIX_NONE = f"{_CHAR_SPACE}{_CHAR_SPACE}"  # skip level ("  ")
    _CONNECTOR_TEE = f"{_CHAR_TEE}{_CHAR_HORZ}"  # next sub item ("T-")
    _CONNECTOR_ELL = f"{_CHAR_ELL}{_CHAR_HORZ}"  # last sub item ("L-")

    # the default directory/file name formats
    _FORMAT_NAME = "$NAME"
    _FORMAT_DIR = f" {_FORMAT_NAME}/"
    _FORMAT_FILE = f" {_FORMAT_NAME}"

    # custom error strings
    _ERR_NOT_A_DIR = "'{}' is not a directory"

    # custom sorting order
    _SORT_ORDER = "_."  # sort first char of name in this order (above ord)

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initializes the new object
    # --------------------------------------------------------------------------
    def __init__(self):
        """
        Initializes the new object

        Initializes a new instance of the class, setting the default values
        of its properties, and any other code that needs to run to create a
        new object.
        """

        # call super init to initialize the base class
        super().__init__()

        # NB: something i learned the hard way from c++ coding: you want to do
        # AS LITTLE coding in the constructor method because the whole class may
        # not exist at this point! you should definitely not call setter methods
        # on any attrs, as these methods may not exist at the time you call
        # them. so to initialize attrs, set them directly rather than using
        # setter methods.

        # set the initial values of properties
        # NB: probably not needed, just a sanity check
        self._start_dir = Path("")
        self._filter_list = []
        self._dir_format = CNTree._FORMAT_DIR
        self._file_format = CNTree._FORMAT_FILE
        self._dirs_only = False
        self._ignore_case = True
        self._root_lead = ""
        self._dir_lead = ""
        self._sort_order = {}
        self._tree = []

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Creates a tree from the given start directory, using filter list,
    # directory and file formats
    # --------------------------------------------------------------------------
    def build_tree(
        self,
        start_dir,
        filter_list=None,
        dir_format="",
        file_format="",
        dirs_only=False,
        ignore_case=True,
    ):
        """
        Creates a tree from the given start directory.

        The start_dir can be an absolute path, a relative path, or a Path
        object, but MUST point to a directory.

        If start_dir does not point to a directory, an OSError will be raised.

        If start_dir == None, an OSError will be raised.

        If start_dir == "", the current directory is used.

        Items in the filter list will be skipped. These items can be absolute or
        relative directory or file paths, or a glob.

        Example: 

            filter_list = ["Foo/bar.txt", "Foo"]

        An entry of "Foo/bar.txt" will skip a file with the absolute path
        "\\<start dir\\>/Foo/bar.txt".

        An entry of "Foo" (if it points to a directory) will skip a
        directory with the absolute path "\\<start dir\\>/Foo/" and
        everything under it.

        Globs are also acceptable, see 
        https://docs.python.org/3/library/pathlib.html#pathlib.Path.glob

        The format strings for directory and file names will have the value
        of "CNTree._FORMAT_NAME" replaced by the directory or file name.

        Example: (assuming CNTree._FORMAT_NAME is set to "$NAME")

            dir_format = " [] $NAME/"
            item.name = "Foo"
            result = " [] Foo/"

        Also, leading spaces in dir_format, when applied to the start_dir
        name, will be left-trimmed to make the tree start at the first
        column.

        Arguments:
            start_dir: String or Path to the root directory of the tree\
            (default: "")
            filter_list: List of directory/file names to filter out (default:\
            None)
            dir_format: Format to use for directories (default:"$NAME/")
            file_format: Format to use for files (default: "$NAME")
            dirs_only: Only list directories (default: False)
            ignore_case: Sort entries regardless of case. If False, \
            uppercase alpha characters take precedence.

        Returns:
            The current tree as a string

        Raises:
            OSError: If the start_dir parameter is None or does not contain
                a path to a valid directory
        """

        # if list is None, create it
        # https://docs.python-guide.org/writing/gotchas/
        if not filter_list:
            filter_list = []

        # reset all props every time this method is called
        # NB: most of this is not needed, since it will be set by the various
        # _sanitize* functions. just a sanity check
        self._start_dir = Path("")  # will set in sanitizer
        self._filter_list = []  # will set in sanitizer
        self._dir_format = CNTree._FORMAT_DIR
        self._file_format = CNTree._FORMAT_FILE
        self._dirs_only = dirs_only
        self._ignore_case = ignore_case
        self._root_lead = ""
        self._dir_lead = ""
        self._sort_order = {}
        self._tree = []

        # sanitize start_dir param
        try:
            self._sanitize_start_dir(start_dir)

        # this exception gets raised if start_dir is None or not a dir
        except OSError as exception:
            err_string = CNTree._ERR_NOT_A_DIR.format(start_dir)
            raise OSError(err_string) from exception

        # sanitize the filter list
        self._sanitize_filter_list(filter_list)

        # sanitize the format params
        self._sanitize_formats(dir_format, file_format)

        # get leads (extra spaces before prefix/connector)
        self._get_leads()

        # create custom sort dictionary
        self._get_sort_order()

        # add root to tree
        self._add_root()

        # enumerate the start dir and add its contents, starting recursion
        self._add_contents(self._start_dir)

        # turn the final tree array into a string and return it
        return self._get_result()

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Sanitizes the start_dir parameter
    # ---------------------------------------------------------------------------
    def _sanitize_start_dir(self, start_dir):
        """
        Sanitizes the start_dir parameter

        Arguments:
            start_dir: start_dir parameter from build_tree (Can be a string or
            Path object)

        Raises:
            OSError: If the start_dir parameter is None or does not contain a
            path to a valid directory

        Ensures the start_dir parameter is a valid path to a directory.
        """

        # check for stupid people (start_dir=None)
        if start_dir is None:
            raise OSError()

        # convert string param to Path object
        # NB: if it is already a Path, this does nothing
        self._start_dir = Path(start_dir)

        # check for param is not a dir (it happens...)
        if not self._start_dir.is_dir():
            raise OSError()

        # in case the param is relative (replace in-situ)
        self._start_dir = self._start_dir.resolve()

    # --------------------------------------------------------------------------
    # Sanitizes the filter_list parameter
    # ---------------------------------------------------------------------------
    def _sanitize_filter_list(self, filter_list):
        """
        Sanitizes the filter_list parameter

        Arguments:
            filter_list: filter_list parameter from build_tree

        Converts entries in filter_list to absolute Path objects relative
        to start_dir. Globs are acceptable, see
        https://docs.python.org/3/library/pathlib.html#pathlib.Path.globs
        """

        # convert all items in filter_list to Path objects
        filter_paths = [Path(item) for item in filter_list]

        # move absolute paths to one list
        absolute_paths = [item for item in filter_paths if item.is_absolute()]

        # move non-absolute paths (assume globs) to another list
        other_paths = [item for item in filter_paths if not item.is_absolute()]

        # convert glob/relative path objects back to strings
        other_strings = [str(item) for item in other_paths]

        # get glob results as generators
        glob_results = [self._start_dir.glob(item) for item in other_strings]

        # start with absolutes
        result = absolute_paths

        # for each generator
        for item in glob_results:
            # add results as whole shebang
            result += list(item)

        # set the filter list as the class filter list
        self._filter_list = result

    # --------------------------------------------------------------------------
    # Sanitizes the dir_format and file_format parameters
    # ---------------------------------------------------------------------------
    def _sanitize_formats(self, dir_format, file_format):
        """
        Sanitizes the dir_format and file_format parameters

        Arguments:
            dir_format: Format to use for directory names
            file_format: Format to use for file names

        Ensures that the user entered a correctly formatted format string,
        which is to say it includes the CNTree._FORMAT_NAME.
        """

        # set directory/file format
        # NB: make sure the user didn't use an incorrect format value, such as:
        # build_tree(... dir_format=None)
        # or
        # build_tree(..., dir_format="")
        # also check that the format string contains CNTree._FORMAT_NAME
        if dir_format and CNTree._FORMAT_NAME in dir_format:
            self._dir_format = dir_format
        if file_format and CNTree._FORMAT_NAME in file_format:
            self._file_format = file_format

    # --------------------------------------------------------------------------
    # Gets the leads (extra spaces) before each entry in the tree
    # ---------------------------------------------------------------------------
    def _get_leads(self):
        """
        Gets the leads (extra spaces) before each entry in the tree

        Calculates how many spaces should be presented before each entry in
        the tree. The root folder should have no spaces (left-aligned) and
        each subsequent entry should add the number of spaces in a
        directory's format name. This allows us to align the connector with
        the index of the CNTree._FORMAT_NAME variable.
        """

        # get the leads (extra indents to line up the pipes/tees/ells)
        # NB: we don't care about file leads, nothing goes under a file

        # get the root's format with no leading spaces
        root_fmt = self._dir_format.lstrip()

        # set root lead as string
        root_lead_count = root_fmt.find(CNTree._FORMAT_NAME)
        self._root_lead = " " * root_lead_count

        # set directory lead as string
        dir_lead_count = self._dir_format.find(CNTree._FORMAT_NAME)
        self._dir_lead = " " * dir_lead_count

    # --------------------------------------------------------------------------
    # Gets the sort order for custom sorting
    # ---------------------------------------------------------------------------
    def _get_sort_order(self):
        """
        Gets the sort order for custom sorting

        This just fixes a personal quirk of mine. The default sorting order
        in Python sorts names starting with a dot (.) above a name starting
        with an underscore (_) (as per string.printable), which for me is
        dependant on my locale, en_US, YMMV. This does not match my IDE,
        Codium, and I want the tree to match my File Explorer in my IDE. So
        to fix this, I created a custom sorter that reverses that. It's not
        really necessary, but it does the job.

        This function creates a dict in the form of:
        {char:index[, ...]}
        where:
        char is the character in the CNTree._SORT_ORDER string
        index is the ordinal of that char (starting at the lowest negative
        ordinal)
        so that:
        CNTree._SORT_ORDER = "_."
        results in:
        self._sort_order = {"_": -2, ".": -1}

        most of this came form:
        https://stackoverflow.com/questions/75301122/how-can-i-change-how-python-sort-deals-with-punctuation
        """

        # get length of string to count backwards
        sort_len = len(CNTree._SORT_ORDER)

        # for each char in string
        for index, char in enumerate(CNTree._SORT_ORDER):
            # make a dict entry for the char and its new ord
            self._sort_order[char] = index - sort_len

    # --------------------------------------------------------------------------
    # Adds the root to the tree
    # ---------------------------------------------------------------------------
    def _add_root(self):
        """
        Adds the root to the tree

        This function adds the root item to the tree. It just strips the
        leading blanks to make sure the root is left-aligned.
        """

        # format the root directory name to a display name and add it
        fmt_root = self._dir_format.lstrip()
        rep_name = fmt_root.replace(CNTree._FORMAT_NAME, self._start_dir.name)
        self._tree.append(rep_name)

    # --------------------------------------------------------------------------
    # Enumerates the given directory and adds its contents to the tree
    # --------------------------------------------------------------------------
    def _add_contents(self, item, prefix=""):
        """
        Enumerates the given directory and adds its contents to the tree

        Arguments:
            item: Path object we are adding
            prefix: Current prefix (combination of pipes/blanks) to show
            the level of indentation

        This method is called recursively to build up the visual level of
        indentation, as well as add directory contents to the tree. It does
        a lot of the heavy lifting to determine what gets printed, and how.
        """

        # enum all items in the dir (files and folders) and convert to list
        # NB: we need a list rather than a generator, since we want everything
        # at once (iterdir is a generator, and so yields)
        # this grabs the whole shebang at once
        items = list(item.iterdir())

        # sort everything, first by custom sort (which handles name), then
        # by type (folders first), then removes anything in the filter list
        # it also removes files if the dirs_only value is true

        # the key function's result is used to determine an item's position
        # based on a bubble sort
        # NB: the hidden params to the "key" function are self and the results
        # of an iterator of items
        items.sort(key=self._sort_by_name)

        # sort works by iterating through a list. this function passes every
        # item through the is_file() test to get its result
        # the item.is_file() might seem backwards, but sort works by placing
        # a false(0) above a true(1), so an item that is NOT a file (ie. a dir,
        # and thus a 0), will be placed above an item that IS a file (and thus a
        # 1)
        items.sort(key=lambda item: item.is_file())

        # remove the filtered paths
        items = [item for item in items if item not in self._filter_list]

        # list only dirs if flag is set
        if self._dirs_only:
            items = [item for item in items if item.is_dir()]

        # get number of files/directories (for determining connector)
        count = len(items)

        # for each entry
        for index, item in enumerate(items):
            # get the type of connector based on position in enum
            connector = (
                CNTree._CONNECTOR_TEE
                if index < (count - 1)
                else CNTree._CONNECTOR_ELL
            )

            # get format string based on whether it is a dir or file
            fmt = self._dir_format if item.is_dir() else self._file_format

            # replace name in format string
            rep_name = fmt.replace(CNTree._FORMAT_NAME, item.name)

            # add the item to the tree
            self._tree.append(f"{self._root_lead}{prefix}{connector}{rep_name}")

            # if item is a dir
            if item.is_dir():
                # adjust the prefix, and call _add_contents for the dir
                self._add_dir(item, prefix, count, index)

    # --------------------------------------------------------------------------
    # Does some extra stuff when adding a directory
    # ---------------------------------------------------------------------------
    def _add_dir(self, item, prefix, count, index):
        """
        Does some extra stuff when adding a directory

        Arguments:
            item: Path object to add
            prefix: Prefix for the last Path object added
            count: Total number of objects in the parent (for prefix)
            index: Index of this object in its parent (for prefix)

        Does some extra stuff when adding a directory. First, the prefix
        needs to be appended with another pipe or more spaces. Also the line
        needs to account for the directory lead. Then, it needs to recurse
        back to _add_contents.
        NOTE: This code CANNOT be included in _add_contents because changing the
        prefix will break recursion (IDKWTF)
        """

        # add a vert or a blank
        prefix += (
            CNTree._PREFIX_VERT if index < (count - 1) else CNTree._PREFIX_NONE
        )

        # add some spacing
        prefix += self._dir_lead

        # call _add_contents recursively with current item and new prefix
        self._add_contents(item, prefix)

    # --------------------------------------------------------------------------
    # Creates the final output string of the tree (trumpets in the distance)
    # ---------------------------------------------------------------------------
    def _get_result(self):
        """
        Creates the final output string of the tree (trumpets in the distance)

        Returns:
            The final string representation of the tree

        Gets the internal list representation of the tree, and convert it to
        a string.
        """

        # join the final tree array into a string and return it
        str_out = "\n".join(self._tree)
        return str_out

    # --------------------------------------------------------------------------
    # Sorts items in the item list according to the item name
    # --------------------------------------------------------------------------
    def _sort_by_name(self, item):
        """
        Sorts items in the item list according to the item name

        Arguments:
            item: Path object to sort

        Returns:
            The index of the sorted item

        """

        # check if we need to lowercase based on the build_tree param
        tmp_item = item.name
        if self._ignore_case:
            tmp_item = item.name.lower()

        # get the ordinal position of each char
        # NB: if the key (char) is present, the get() function returns the value
        # of the specified key. if the key is not present, it returns the second
        # (ord of char in string.printable)
        # this is why we need to know  about the ignore_case, since if it is
        # False, uppercase will always take precedence over lowercase (at least
        # in en_US str.printable, YMMV)
        return [self._sort_order.get(char, ord(char)) for char in tmp_item]


# ------------------------------------------------------------------------------
# For debugging purposes, make a tree of current folder
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    tree_obj = CNTree()
    # DIR_ROOT = Path(__file__).parent
    DIR_ROOT = ""
    print(Path(DIR_ROOT).resolve())
    # S = tree_obj.build_tree(DIR_ROOT)
    # print(S)

# -)
