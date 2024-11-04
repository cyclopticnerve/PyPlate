# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnpot.py                                              |     ()     |
# Date    : 03/14/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
Run GNU gettext tools to create i18n files for a project

This class converts all marked strings in source files to i18n versions using
xgettext, and creates .pot files in the locale directory. It also uses msgfmt
to convert .po files to .mo files.

The class can handle all xgettext's supported file types by using each language
name as the key for a list of file extensions in a dictionary.

Note that the word "language" here can refer either to the computer language of
the input file (ie. "Python", "Glade") or the written language of the output
file (ie. "English", "Spanish"). I have tried to disambiguate this by using
"clang(s)" to refer to the former, and "wlang(s)" to refer to the latter.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from datetime import date
from pathlib import Path
import re
import shutil

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
from . import cnfunctions as F

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to handle making the different I18N files needed for a Python project
# ------------------------------------------------------------------------------
class CNPotPy:
    """
    A class to handle making the different I18N files needed for a Python
    project

    Public methods:
        main: Run the program
        make_desktop: Make a desktop file

    This class provides methods to create .pot, .po, .mo, and .desktop files
    for internationalizing a Python or PyGObject project.
    """

    # default locale dir under src
    DEF_DIR_LOCALE = "locale"
    # default po dir under src
    DEF_DIR_PO = "po"
    # default encoding for .pot and .po files
    DEF_CHARSET = "UTF-8"

    # this is the default subdir for GNU
    # NB: DO NOT CHANGE THIS! i only put it here because it is a string
    DIR_MESSAGES = "LC_MESSAGES"
    # the file to store all wlangs for bulk operations
    # NB: DO NOT CHANGE THIS! i only put it here because it is a string
    FILE_LINGUAS = "LINGUAS"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(
        self,
        dir_src,
        str_appname,
        str_version,
        str_author,
        str_email,
        dir_locale=None,
        dir_po=None,
        str_domain="messages",
        dict_clangs=None,
        dict_no_ext=None,
        list_wlangs=None,
        charset=None,
    ):
        """
        Initialize the new object

        Arguments:
            dir_src: Where to start looking for input files
            str_appname: Name to use in .pot/.po header
            str_version: Version info to use in .pot/.po header
            str_email: Email to use in .pot/.po header
            dir_locale: Where to put output locale files (default:
            dir_src/"locale")
            dir_po: Where to put new .po files that are waiting to be merged
            (default: dir_src/"po")
            str_domain: THe name of the domain (base name) for output files
            (default: "messages")
                This creates files like "<str_domain>.pot", "<str_domain>.po",
                and "<str_domain>.mo", and is used in the .py scripts to bind a
                domain to a locale folder
            dict_clangs: The dictionary of file extensions to scan for each
            clang
            dict_no_ext: An optional dict mapping files with no extension
            to their clang value
            list_wlangs: A list of supported languages to ensure a complete
            file structure in the project dir
            charset: the charset to use as the default in the .pot file, and
            any initial .po files created (default: UTF-8)

        An example format for the dict_clangs arg is:

        {
            "Python": [
                ".py",
            ],
            "Glade": [
                ".ui",
                ".glade",
            ],
            "Desktop": [
                ".desktop"
            ],
        }

        An example format for the dict_no_ext arg is:

        {
            "Markdown": [
                "README",
            ],
            "Text": [
                "INSTALL",
                "LICENSE",
            ],
        }

        An example format for list_wlangs is:
        [
            "en_US",
            "de_DE.ISO_88591",
            "es",
        ]

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # set private props from params
        self._dir_src = Path(dir_src)

        # header info
        self._str_appname = str_appname
        self._str_version = str_version
        self._str_author = str_author
        self._str_email = str_email

        # fix up dir_locale
        if dir_locale is None:
            dir_locale = self._dir_src / self.DEF_DIR_LOCALE
        elif not dir_locale.is_absolute():
            dir_locale = self._dir_src / dir_locale
        self._dir_locale = dir_locale

        # fix up dir_po
        if dir_po is None:
            dir_po = self._dir_src / self.DEF_DIR_PO
        elif not dir_po.is_absolute():
            dir_po = self._dir_src / dir_po
        self._dir_po = dir_po

        # set str_domain
        self._str_domain = str_domain

        # fix up dict_clangs
        if dict_clangs is None:
            dict_clangs = {}
        self._dict_clangs = dict_clangs

        # set no ext
        if dict_no_ext is None:
            dict_no_ext = {}
        self._dict_no_ext = dict_no_ext

        # fix up list_wlangs
        if list_wlangs is None:
            list_wlangs = []
        self._list_wlangs = list_wlangs

        # fix up charset
        if charset is None:
            charset = self.DEF_CHARSET
        self._charset = charset

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Main method of the class
    # --------------------------------------------------------------------------
    def main(self):
        """
        Main method of the class

        Main method of the class, performing its steps.
        """

        # ----------------------------------------------------------------------
        # do the steps

        self.make_pot()
        self.make_pos()
        self.make_mos()

    # --------------------------------------------------------------------------
    # Localize the desktop file using all available wlangs
    # --------------------------------------------------------------------------
    def make_desktop(self, dt_template, dt_out):
        """
        Localize the desktop file using all available wlangs

        Arguments:
            dt_template: File containing the default information to include in
            the desktop file
            dt_out: Location of the i18n'ed desktop file

        Takes a template desktop file and applies all i18n'ed info from all .po
        files in the po folder and creates a final .desktop file.
        """

        # build the command as a string
        cmd = (
            f"msgfmt --desktop --template={dt_template} -d {self._dir_po} "
            f"-o {dt_out}"
        )

        # run the command
        F.sh(cmd)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Create a .pot file in the locale folder
    # --------------------------------------------------------------------------
    def make_pot(self):
        """
        Create a .pot file in the locale folder

        Parses the files for each clang, creating a unified .pot file, which is
        placed in "<dir_locale>/<str_domain>.pot". This method can (and should)
        be run, in Mayor Tweed's words, "early and often". You should run it
        every time a source file that contains i18n strings is added, edited,
        or deleted. The ideal scenario is to run it just before the repo is
        synced, so that the .pot file is synced.
        """

        # ok so this is a tricky situation. here are the possible scenarios:
        # 1. create a new, fresh .pot that has never existed before
        # 2. add / edit / remove files to / from a .pot file we have already
        #    created
        # 3. add / edit / remove strings to / from a .pot file we have already
        #    created
        # 4. add / edit / remove clang types to / from a .pot file we have
        #    already created
        # 6. etc., etc., etc
        # how do we do all this (at least in the context of a .pot file)?
        # the simplest answer would seem to be:
        # delete the .pot (if it exists) and start over fresh every time
        # BUT! we need to use the -j (join) flag in order to allow multiple
        # clangs to be combined into one .pot file
        # the solution i have found is:
        # delete the existing .pot file (if it exists)
        # create a new, empty .pot file (if it does not exist, which it
        # shouldn't, race conditions be damned... Python file operations are
        # atomic, right? RIGHT???)
        # run every clang through xgettext, joining it with the previous file
        # until we have a .pot file that contains every string (and only the
        # strings) in dict_clangs
        # step 3: PROFIT! (hahaha that joke never gets old...)

        # make sure all necessary dirs exist
        self._make_wlang_dirs()

        # get path to pot file
        pot_file = self._dir_po / f"{self._str_domain}.pot"

        # delete the existing .pot file (if it exists)
        Path.unlink(pot_file, missing_ok=True)

        # create a new, empty .pot file if it does not exist
        # NB: this allow us to use the -j flag without error (which would
        # happen if the current file to join does not exist)
        Path.touch(pot_file, exist_ok=True)

        # get all files for all clangs
        files_dict = self._get_paths_for_exts(self._dict_clangs)

        # for each clang name / list of clang files
        for clang_name, clang_files in files_dict.items():

            # check if there are any files (avoids any unnecessary errors for
            # empty lists)
            if len(clang_files) == 0:
                continue

            # get initial cmd
            cmd = (
                "xgettext "
                # add any comments above string (or msgctxt in ui files)
                # NB: check that all files have appropriate contexts/comments
                "-c "
                # fix some header values (the rest should be fixed in
                # _fix_header)
                # NB: if blank, file is public domain
                # if not included, file is under same license as
                # self._str_appname.
                # "--copyright-holder "" "
                # Project-Id-Version
                # | name | version | out
                # -----------------------------------
                # |    0 |       0 | PACKAGE VERSION
                # |    0 |       1 | PACKAGE VERSION
                # |    1 |       0 | self._str_appname
                # |    1 |       1 | self._str_appname self._str_version
                f"--package-name {self._str_appname} "
                f"--package-version {self._str_version} "
                # author email
                f"--msgid-bugs-address {self._str_email} "
                # sort entries by file
                "-F "
                # append existing file
                # NB: this is the key to running xgettext once for each clang
                # this allows us to set the -L option for different file types
                # and still end up with one unified .pot file
                "-j "
                # final name of output file
                # NB: note that you can fiddle with the -o, -d, and -p options
                # here, but i find it's just better to use an abs path to the
                # output file
                f"-o {pot_file} "
                # input clang
                f"-L {clang_name} "
            )

            # add all input files
            for item in clang_files:
                cmd += f"{item} "

            # do the final command
            F.sh(cmd)

        # fix CHARSET in pot
        self._fix_pot_header(pot_file)

    # --------------------------------------------------------------------------
    # Merge any .po files in the pos folder with existing .po files
    # --------------------------------------------------------------------------
    def make_pos(self):
        """
        Merge any .po files in the pos folder with existing .po files

        Whenever a new .pot file is generated using make_pot, it should be sent
        to the translator for each wlang. Then when the translator sends back
        the translated .po file, place it in the appropriate pos/<wlang>
        folder. Then run pybaker to merge the new .po file with any existing
        .po file, and then pybaker will create a new .mo file.
        """
        # make sure all necessary dirs exist
        self._make_wlang_dirs()

        # get the pot file we made in the last step
        pot_file = self._dir_po / f"{self._str_domain}.pot"

        # for each wlang in the po folder
        for wlang in self._list_wlangs:

            # create or update the .po file
            po_file = self._dir_po / f"{wlang}.po"
            if not po_file.exists():

                # no po file, copy pot
                shutil.copy(pot_file, po_file)
            else:

                # update existing po file using latest pot
                cmd = f"msgmerge --update {po_file} {pot_file}"
                F.sh(cmd)

    # --------------------------------------------------------------------------
    # Create .mo files for all .po files in the locale folder
    # --------------------------------------------------------------------------
    def make_mos(self):
        """
        Create .mo files for all .po files in the locale folder

        Makes all the required .mo files for all the .po files in the locale
        dir
        """

        # make sure all necessary dirs exist
        self._make_wlang_dirs()

        # get all wlangs to output
        wlangs_pos = list(self._dir_po.glob("*.po"))

        # for each wlang
        for wlang_po in wlangs_pos:

            # get wlang name
            wlang_name = wlang_po.stem  # es

            # get .mo file (output)
            mo_dir = self._dir_locale / wlang_name / self.DIR_MESSAGES
            mo_file = mo_dir / f"{self._str_domain}.mo"

            # do the command
            cmd = f"msgfmt -o {mo_file} {wlang_po}"
            F.sh(cmd)

    # --------------------------------------------------------------------------
    # Private functions
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Scan the source dir for files with certain extensions
    # --------------------------------------------------------------------------
    def _get_paths_for_exts(self, dict_clangs):
        """
        Scan the source dir for files with certain extensions

        Arguments:
            dict_clangs: The dictionary of clang names / clang extensions to
            scan for
            dict_no_ext: An optional dictionary mapping files with no extension
            to their clang value

        Returns:
            A dictionary containing file paths to source files

        This method converts the dict_clangs dictionary:
            {
                "Python": [".py"],
                "Glade": [".ui", ".glade"],
                "Desktop": [".desktop"],
            }
        into a dictionary of file paths for each clang:
            {
                "Python": [<Path>, ...],
                "Glade": [<Path>, ...],
                "Desktop": [<path>, ...],
            }
        so they can be passed to xgettext.
        """

        # get default result
        dict_res = {}

        # get all paths to all files in source dir, recursively
        # NB: very important to convert generator to list here
        # this is because generators use yield to return every result
        # individually, while lists are monolithic (and rglob is a generator)
        # you cannot iterate over a generator's yield result, because it is
        # generally only one item, while a list contains all results
        # calling list() on a generator causes the generator to give ALL it's
        # generated results to the final list
        paths = list(self._dir_src.rglob("*"))

        # for each clang name / list of exts
        for clang, ext_list in dict_clangs.items():

            # sanity check to add dots for exts that don't start with dot
            # (dots needed for path.suffix matching)
            exts = [
                f".{item}" if not item.startswith(".") else item
                for item in ext_list
            ]

            # get all paths that match file ext
            files = [f for f in paths if f.suffix in exts]

            # make sure the key exists
            if not clang in dict_res:
                dict_res[clang] = []

            # add results to langs that have extensions
            dict_res[clang].extend(files)

        # now time to handle files with no ext
        for clang, name_list in self._dict_no_ext.items():

            # get all paths that match file ext
            # NB: the is_file() check here is to make sure we only add files
            # that have no ext, not dirs (which have no ext, obvs)
            files = [f for f in paths if f.name in name_list if f.is_file()]

            # make sure the key exists
            if not clang in dict_res:
                dict_res[clang] = []

            # add results to langs that have extensions
            dict_res[clang].extend(files)

        # return result
        return dict_res

    # --------------------------------------------------------------------------
    # Make a list of all supported written language directories
    # --------------------------------------------------------------------------
    def _get_wlang_names(self):
        """
        Make a list of all supported written language directories

        Finds all known written languages just before calling a function.

        The idea is to get all *existing* languages on disk, then
        add all the languages passed in to the constructor.

        The logic here is a little fuzzy, so try to keep the removal of
        languages in sync between disk and the list passed to the constructor.
        Adding languages should be as easy as adding a .po file to the correct
        po/wlang dir.
        """

        # make sure there is a locale dir
        Path.mkdir(self._dir_locale, parents=True, exist_ok=True)

        # make sure there is a po dir
        Path.mkdir(self._dir_po, parents=True, exist_ok=True)

        # sweep locale dir for wlangs and reduce to ISO name
        locale_wlangs_glob = self._dir_locale.glob("*")
        # convert generator to list
        locale_wlangs = list(locale_wlangs_glob)
        # only dirs
        locale_wlangs = [item for item in locale_wlangs if item.is_dir()]
        # only names (last path component)
        locale_wlangs = [item.name for item in locale_wlangs]

        # sweep po folder for wlangs and reduce to ISO name
        po_wlangs_glob = self._dir_po.glob("*")
        # convert generator to list
        po_wlangs = list(po_wlangs_glob)
        # only dirs
        po_wlangs = [item for item in po_wlangs if item.is_dir()]
        # only names (last path component)
        po_wlangs = [item.name for item in po_wlangs]

        # combine locale and po wlangs (whatever we found on disk)
        list_on_dir = locale_wlangs + po_wlangs
        # remove duplicates
        set_on_dir = set(list_on_dir)
        # convert back to list
        list_on_dir = list(set_on_dir)

        # add any names passed in via list_wlangs (should be ISO names)
        list_comb = list_on_dir + self._list_wlangs
        # remove duplicates
        set_comb = set(list_comb)
        # convert back to list
        list_comb = list(set_comb)

        # assign all found/new langs
        self._list_wlangs = list_comb

    # --------------------------------------------------------------------------
    # Make a list of all supported written language directories
    # --------------------------------------------------------------------------
    def _make_wlang_dirs(self):

        # get names of all wlangs present in po/locale/property
        self._get_wlang_names()

        # empty linguas contents
        linguas = ""

        # make the po dir where we will put updated files to be merged
        d = self._dir_po
        Path.mkdir(d, parents=True, exist_ok=True)

        # go through the wlang list
        for wlang in self._list_wlangs:

            # make the locale/lang/LC_MESSAGES dir
            d = self._dir_locale / wlang / self.DIR_MESSAGES
            Path.mkdir(d, parents=True, exist_ok=True)

            # add each wlang to LINGUAS file
            linguas += wlang + " "

        # write the LINGUAS file
        linguas_path = self._dir_po / self.FILE_LINGUAS
        with open(linguas_path, "w", encoding="UTF8") as f:
            f.write(linguas)

    # --------------------------------------------------------------------------
    # Set the charset for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self, file_pot):
        """
        Set the charset for the pot which will carry over to each po

        Arguments:
            file_pot: the path object representing the pot file to fix

        Fix the charset in the pot file to a known value so that msgfmt does
        not complain. The charset for an individual file can be set by the
        translator. This is just to keep the compiler from complaining, and
        also aids in testing when no editing is done.
        """

        # open file and get contents
        with open(file_pot, "r", encoding="UTF8") as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = r"# SOME DESCRIPTIVE TITLE."
        str_rep = f"# {self._str_appname} translation template"
        text = re.sub(str_pattern, str_rep, text)

        # replace copyright
        str_pattern = r"(# Copyright \(C\) )(YEAR)( )(THE PACKAGE'S COPYRIGHT HOLDER)"
        year = date.today().year
        str_rep = rf"\g<1>{year}\g<3>{self._str_author}"
        text = re.sub(str_pattern, str_rep, text)

        # replace author's email
        str_pattern = r"(# FIRST AUTHOR )(<EMAIL@ADDRESS>)(, )(YEAR)"
        email = self._str_email
        year = date.today().year
        str_rep = rf"\g<1>{email}\g<3>{year}"
        text = re.sub(str_pattern, str_rep, text)

        # NB: if the specific phrase "CHARSET" is not found, nothing will be
        # changed
        str_pattern = r"(\"Content-Type: text/plain; charset=)(CHARSET)(.*)"
        str_rep = rf"\g<1>{self._charset}\g<3>"
        text = re.sub(str_pattern, str_rep, text, flags=re.M)

        # save file
        with open(file_pot, "w", encoding="UTF8") as a_file:
            a_file.write(text)


# -)
