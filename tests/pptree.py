# ------------------------------------------------------------------------------
# Project : PyPlate                                               /          \
# Filename: pptree.py                                            |     ()     |
# Date    : 08/06/2023                                           |            |
# Author  : cyclopticnerve                                       |   \____/   |
# License : WTFPLv2                                               \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import os
import pathlib

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# some useful constants
DIR_FILE = os.path.dirname(__file__)
DIR_HOME = os.path.expanduser('~')

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Class
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# A class to generate a file tree in text format with checkboxes next to each
# folder/file
# ------------------------------------------------------------------------------
class PPTree(object):
    """
        A class to generate a file tree in text format with checkboxes next to
        each folder/file

        Methods:
            build_tree(): Creates the new tree and returns it's items as a
            string.

       This class builds the tree as a complete string, ready to be printed to
       stdout or a file.
    """

    # --------------------------------------------------------------------------
    # Internal constants
    # --------------------------------------------------------------------------

    # these are the console/terminal values for the individual
    # prefix/connector chars
    VRT = '\u2502'  # the vertical join (pipe)
    HRZ = '\u2500'  # the horizontal join (dash)
    TEE = '\u251C'  # the tee join (not last item)
    ELL = '\u2514'  # the elbow join (last item)
    IND = '   '     # the minimum space between prefix and connector     
    BNK = ' '       # the space between connector and name

    # these are the preset char sequences for the prefix/connector char sets
    # NB: these must always add to 7
    PFX_VRT = f'{IND}{VRT}{IND}'            # pfx for next level     ('   |   ')
    PFX_NUN = f'{IND}{BNK}{IND}'            # pfx to skip a level    ('       ')
    CON_TEE = f'{IND}{TEE}{HRZ}{HRZ}{BNK}'  # conn for a sub level   ('   T-- ')
    CON_ELL = f'{IND}{ELL}{HRZ}{HRZ}{BNK}'  # conn for last sub level('   L-- ')
    
    # the checkbox stuff
    FMT_CHK = '[]'                          # the checkbox format
    FMT_FNL = f'{FMT_CHK}{BNK}'             # the checkbox/name format

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
        # not exist at this point! you should definitely not call get/set
        # methods to init controls. these methods/controls may not exist at the
        # time you call them. so to initialize scalar properties, set them
        # empirically rather than using setter methods.

        # set the initial value of class
        self._root = ''
        self._ignore = []
        self._tree = []
        self._str = ''

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Creates a tree from the given root dir and ignore list
    # --------------------------------------------------------------------------
    def build_tree(self, root, ignore=None):
        """
            Creates a tree from the given root dir and ignore list

            Parameters:
                root: The complete path to the root directory of the tree
                ignore: A list of folder/file names to ignore

            Returns:
                The current tree as a newline-separated string

            Create a tree from the given root dir and ignore list, as a
            newline-separated string.
        """

        # create a Path object from the root dir
        self._root = pathlib.Path(root)

        # check root
        if not self._root.is_dir():
            raise Exception('root is not a directory')
            return

        # initialize the ignore list
        # NB: https://docs.python-guide.org/writing/gotchas/
        if ignore == None:

            # create the ignore list if it does not already exist
            self._ignore = []
        else:

            # replace existing ignore list
            # NB: since all private functions are called from this one, ignore
            # remains in scope so we only need a reference, not a deep copy
            self._ignore = ignore

        # initialize the tree
        self._tree = []

        # initialize the result
        self._str = ''

        # add the main root folder name
        self._tree.append(f'{self.FMT_FNL}{self._root.name}{os.sep}')

        # create the rest of the dirs/files recursively
        self._tree_body(self._root)

        # turn the tree array into a string
        for item in self._tree:
            self._str += item + '\n'

        # return tree
        return self._str
    
    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Creates the current section of the tree
    # --------------------------------------------------------------------------
    def _tree_body(self, dir, prefix=''):
        """
            Creates the current section of the tree

            Parameters:
                dir: The current directory we are recursing
                prefix: the current prefix (combination of pipes/blanks) to show
                    the level of indentation

            This method is called recursively to build up the visual level of
            indentation, as well as add folders recursively to the tree.
        """ 

        # NB: we list folders and files separately so that we can do folders
        # fist, sorted alphabetically, then files sorted alphabetically

        # # list all folders in path, sorted by lower name
        items = dir.iterdir()
        items_dirs = [item for item in items if item.is_dir()]
        items_dirs.sort(key=lambda path: str(path).lower())
   
        # list all files in path, sorted by lower name
        # NB: we have to do an iter again for files
        items = dir.iterdir()
        items_files = [item for item in items if item.is_file()]
        items_files.sort(key=lambda path: str(path).lower())

        # combine lists (folders first)
        items = items_dirs + items_files

        # get number of files/folders
        count = len(items)

        # for each entry (assuming folders first)
        for index, item in enumerate(items):

            # get the type of connector based on position in enum
            connector = self.CON_TEE if index < (count - 1) else self.CON_ELL

            # call the sub def based on item type
            if item.is_dir():
                self._add_dir(prefix, connector, item, index, count)
            else:
                self._add_file(prefix, connector, item)

    # --------------------------------------------------------------------------
    # Adds a directory to the tree
    # --------------------------------------------------------------------------
    def _add_dir(self, prefix, connector, item, index, count):
        """
            Adds a directory to the tree

            Parameters:
                prefix: The prefix of pipes determined by this function or
                    _add_file()
                connector: The char to show before the dir name, either a tee
                    or an ell
                item: The dir name to print
                index: The index of the current dir in its parent
                count: The count of dirs in the parent

            Returns:
                None if dir is in the skip array
                Otherwise, continue (recurse)

            When recursing, add a directory to to output listing. Files in this
            directory will be added by another function.
        """

        # filter out any skipped dirs
        if item.name in self._ignore:
            return

        # append the display name of the dir
        self._tree.append(
            f'{prefix}{connector}{self.FMT_FNL}{item.name}{os.sep}'
        )

        # figure out prefix for next level (cumulative for recursion)
        prefix += self.PFX_VRT if index < (count - 1) else self.PFX_NUN

        # recurse with next level of dir
        self._tree_body(item, prefix)

    # --------------------------------------------------------------------------
    # Adds a file to the tree
    # --------------------------------------------------------------------------
    def _add_file(self, prefix, connector, item):
        """
            Adds a file to the tree

            Parameters:
                prefix: The prefix of pipes determined by this function or
                    _add_folder()
                connector: the char to show before the file name, either a tee
                    or an ell
                item: the file name to print

            Returns:
                None if file is in the skip array

            When recursing, add a file to to output listing. Dirs in this
            directory will be added by another function.
        """

        # filter out any skipped files
        if item.name in self._ignore:
            return
            
        # append the display name of the file
        self._tree.append(
            f'{prefix}{connector}{self.FMT_FNL}{item.name}'
        )

# -)
