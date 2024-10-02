# ------------------------------------------------------------------------------
# Project : Installerator                                          /          \
# Filename: uninstallerator.py                                    |     ()     |
# Date    : 09/29/2022                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# global imports
import os
import shutil

# local imports
from installerator.base_installerator import Base_Installerator

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

DEBUG = 0


# ------------------------------------------------------------------------------
# Define the main class
# ------------------------------------------------------------------------------

class Uninstallerator(Base_Installerator):

    """
        The class to use for uninstalling. You should override dict_user in
        run().
    """

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the class
    # --------------------------------------------------------------------------
    def __init__(self):

        """
            The default initialization of the class

            This method calls the __init__ method of the base class.
            The base method does nothing. It is provided only as a convention.
        """

        # base installer init
        super().__init__()

    # --------------------------------------------------------------------------
    # Run the script
    # --------------------------------------------------------------------------
    def run(self, dict_user):

        """
            Runs the setup using the supplied user dictionary

            Paramaters:
                dict_user [dict]: the user dict to get options from

            This method is the main function of the class. It performs the
            various steps required to uninstall a python program, and should be
            the only method called by your uninstall.py file.
        """

        # base installer run
        super()._run(dict_user)

        # show some text
        prog_name = self.dict_conf['general']['name']
        print(f'Uninstalling {prog_name}')

        super()._do_preflight()
        self._do_dirs()
        self._do_files()
        super()._do_postflight()

        # done uninstalling
        print(f'{prog_name} uninstalled')

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Delete any unnecessary directories
    # --------------------------------------------------------------------------
    def _do_dirs(self):

        """
            Delete any specified folders

            Raises:
                Exception(str): if deleting the folder fails

            This method deletes any system folders where your program no longer
            requires read-write acces. If the folder contains any files, those
            files will also be deleted. Therefore make sure you only delete
            folders that are not used by any other programs.
        """

        # check for empty/no list
        if not super()._needs_step('dirs'):
            return

        # show some text
        print('Deleting directories')

        # for each folder we need to delete
        for item in self.dict_conf['dirs']:

            # show that we are doing something
            print(f'Deleting directory {item}... ', end='')

            # delete the folder
            try:
                if not DEBUG:
                    shutil.rmtree(item)
                print('Done')
            except Exception as error:
                print('Fail')
                raise Exception(f'Could not delete directory {item}: {error}')

    # --------------------------------------------------------------------------
    # Delete any necessary files (outside above directiories)
    # --------------------------------------------------------------------------
    def _do_files(self):

        """
            Delete any specified files

            Raises:
                Exception(str): if deleting the file fails

            This method deletes any files used by your program. Note that these
            files may have been intrinsically deleted using _do_dirs, so this
            method is only necessary if you store any files outside those
            folders.
        """

        # check for empty/no list
        if not super()._needs_step('files'):
            return

        # show some text
        print('Deleting files')

        # for each file we need to delete
        for src, dst in self.dict_conf['files'].items():

            # show that we are doing something
            print(f'Deleting file {src}... ', end='')

            # NB: removed because all paths should be absolute
            # convert relative path to absolute path
            # abs_src = os.path.join(dst, src)

            # delete the file (if it'wasn't in a folder above)
            if os.path.exists(src):
                try:
                    if not DEBUG:
                        os.remove(src)
                    print('Done')
                except Exception as error:
                    print('Fail')
                    raise Exception(f'Could not delete file {src}: {error}')

# -)
