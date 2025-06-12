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

# my imports
import cnfunctions as F

# ------------------------------------------------------------------------------
# Classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to handle making the different I18N files needed for a Python project
# ------------------------------------------------------------------------------
class CNPotPy:
    """
    A class to handle making the different I18N files needed for a Python
    project

    Methods:
        main: Run the program and make or update the files
        make_desktop: Localize the desktop file using all available wlangs

    This class provides methods to create .pot, .po, .mo, and .desktop files
    for internationalizing a Python or PyGObject project.
    """

    # --------------------------------------------------------------------------
    # Class constants
    # --------------------------------------------------------------------------

    # default encoding for .pot and .po files
    S_CHARSET = "UTF-8"
    # this is the default subdir for GNU
    S_DIR_LC = "LC_MESSAGES"
    # the file to store all wlang/domain names for .desktop files
    S_FILE_LINGUAS = "LINGUAS"

    # default file extensions
    S_EXT_POT = ".pot"
    S_EXT_PO = ".po"
    S_EXT_MO = ".mo"

    # shell commands to make po/mo
    # NB: format params are file_po and pot_file
    S_CMD_MERGE_POS = "msgmerge --update {} {} --backup=none"
    # NB: format params are mo_file and wlang_po
    S_CMD_MAKE_MOS = "msgfmt -o {} {}"
    # NB: format params are po dir, template file, and output file
    S_CMD_DSK = "msgfmt --desktop -d {} --template={} -o {} "

    # NB: format param is dir_prj
    S_ERR_NOT_ABS = "path {} is not absolute"
    # NB: format param is dir_prj
    S_ERR_NOT_DIR = "path {} is not a directory"

    # header regexes
    R_TITLE_SCH = r"# SOME DESCRIPTIVE TITLE."
    R_TITLE_REP = r"# {} translation template"

    R_COPY_SCH = (
        r"(# Copyright \(C\) )(YEAR)( )(THE PACKAGE'S COPYRIGHT HOLDER)"
    )
    R_COPY_REP = r"\g<1>{}\g<3>{}"

    R_EMAIL_SCH = r"(# FIRST AUTHOR )(<EMAIL@ADDRESS>)(, )(YEAR)"
    R_EMAIL_REP = r"\g<1>{}\g<3>{}"

    R_CHAR_SCH = r"(\"Content-Type: text/plain; charset=)(CHARSET)(.*)"
    R_CHAR_REP = r"\g<1>{}\g<3>"

    R_VER_SCH = r"^(\"Project-Id-Version: .*? )([^\n]*)(\\n\")$"
    R_VER_REP = r"\g<1>{}\g<3>"

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(
        self,
        # header
        str_domain,
        str_version,
        str_author,
        str_email,
        # base prj dir
        dir_prj,
        # in
        list_src,
        # out
        dir_pot,
        dir_po,
        dir_locale,
        # optional in
        str_tag=None,
        dict_clangs=None,
        dict_no_ext=None,
        list_wlangs=None,
        charset=S_CHARSET,
        location=True,
    ):
        """
        Initialize the new object

        Args:
            str_domain: The name of the domain (base name) for output files
                This creates files like "<str_domain>.pot", "<str_domain>.po",
                and "<str_domain>.mo", and is used in the .py scripts to bind a
                domain to a locale folder
            str_version: Version info to use in .pot/.po header
            str_author: Author name to use in .pot/.po header
            str_email: Email to use in .pot/.po header

            dir_prj: The main project dir, used for relative paths

            list_src: Where to look for input files

            dir_pot: Directory to place master .pot file
            dir_po: Directory to place .po file
            dir_locale: Directory to place .mo files

            str_tag: Tag that starts a context comment (default: None)
                If this string is empty or None, all comments above an entry
                are included as context.
            dict_clangs: The dictionary of file extensions to scan for each
            clang (default: None)
                If ths dict is empty or None, all files will be scanned
                (this is generally considered a "Very Bad Thing").
            dict_no_ext: An optional dict mapping files with no extension
            to their clang value (default: None)
            list_wlangs: A list of supported languages to ensure a complete
            file structure in the project dir (default: None)
            charset: the charset to use as the default in the .pot file, and
            any initial .po files created (default: "UTF-8")

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

        # set header info
        self._str_domain = str_domain
        self._str_version = str_version
        self._str_author = str_author
        self._str_email = str_email

        # set base props
        self._dir_prj = Path(dir_prj)
        if not self._dir_prj.is_absolute():
            raise OSError(self.S_ERR_NOT_ABS.format(self._dir_prj))
        if not self._dir_prj.is_dir():
            raise OSError(self.S_ERR_NOT_DIR.format(self._dir_prj))

        # fix up in props
        if list_src is None:
            list_src = []
        self._list_src = list_src

        # set out props
        self._dir_pot = Path(dir_pot)
        if not self._dir_pot.is_absolute():
            self._dir_pot = self._dir_prj / dir_pot
        self._dir_po = Path(dir_po)
        if not self._dir_po.is_absolute():
            self._dir_po = self._dir_prj / dir_po
        self._dir_locale = Path(dir_locale)
        if not self._dir_locale.is_absolute():
            self._dir_locale = self._dir_prj / dir_locale

        # set optional in props

        # set comment tag
        if str_tag is None:
            str_tag = ""
        self._str_tag = str_tag

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
            charset = self.S_CHARSET
        self._charset = charset

        # set location prop
        self._location = location

        # make sure all necessary dirs exist
        self._make_wlang_dirs()

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the program and make or update the files
    # --------------------------------------------------------------------------
    def main(self):
        """
        Run the program and make or update the files

        Main method of the class, performing its steps. This method can (and
        should) be run, in Mayor Tweed's words, "early and often". You should
        run it every time a source file that contains i18n strings is added,
        edited, or deleted. The ideal scenario is to run it just before the
        repo is synced, so that the .pot file is synced.
        """

        # ----------------------------------------------------------------------
        # do the steps

        self._make_pot()
        self._make_pos()
        self._make_mos()

    # --------------------------------------------------------------------------
    # Localize the desktop file using all available wlangs
    # --------------------------------------------------------------------------
    def make_desktop(self, dt_template, dt_out):
        """
        Localize the desktop file using all available wlangs

        Args:
            dt_template: File containing the default information to include in
            the desktop file
                This is the file that pymaker/pybaker modifies using metadata.
            dt_out: Location of the i18n'ed desktop file
                This is the file that will be distributed with your app.

        Takes a template desktop file and applies all i18n'ed info from all .po
        files in the po folder and creates a final .desktop file.
        """

        # fix params to abs paths
        dt_template = Path(dt_template)
        if not dt_template.is_absolute():
            dt_template = self._dir_prj / dt_template
        dt_out = Path(dt_out)
        if not dt_out.is_absolute():
            dt_out = self._dir_prj / dt_out

        # check if template exists
        if dt_template.exists():

            # build the command as a string
            cmd = self.S_CMD_DSK.format(self._dir_po, dt_template, dt_out)

            # run the command
            F.sh(cmd)

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Create a .pot file in the locale folder
    # --------------------------------------------------------------------------
    def _make_pot(self):
        """
        Create a .pot file in the pot folder

        Parses the files for each clang, creating a unified .pot file, which is
        placed in "<dir_pot>/<str_domain>.pot".
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

        # get path to pot file
        file_pot = self._dir_pot / f"{self._str_domain}{self.S_EXT_POT}"

        # delete the existing .pot file (if it exists)
        file_pot.unlink(missing_ok=True)

        # create a new, empty .pot file if it does not exist
        # NB: this allow us to use the -j flag without error (which would
        # happen if the current file to join does not exist)
        file_pot.parent.mkdir(parents=True, exist_ok=True)
        file_pot.touch(exist_ok=True)

        # get all paths for this domain
        # NB: or if no src list specified, scan ALL files
        clangs_paths = self._get_paths_for_clangs()

        # for each clang name / list of clang files
        for clang_name, clang_files in clangs_paths.items():

            # sanity check
            if len(clang_files) == 0:
                continue

            # get initial cmd
            cmd = (
                f"cd {self._dir_prj}; "
                "xgettext "
                # add any comments above string (or msgctxt in ui files)
                # NB: check that all files have appropriate contexts/comments
                # NB: also, no space after -c? weird right?
                f"-c{self._str_tag} "
                # fix some header values (the rest should be fixed in
                # _fix_pot_header)
                # copyright
                # NB: if blank, file is public domain
                # if not included, file is under same license as _str_appname
                # "--copyright-holder "" "
                # version
                # | name | version | Project-Id-Version
                # -----------------------------------
                # |    0 |       0 | PACKAGE VERSION
                # |    0 |       1 | PACKAGE VERSION
                # |    1 |       0 | self._str_domain
                # |    1 |       1 | self._str_domain self._str_version
                f"--package-name {self._str_domain} "
                f"--package-version {self._str_version} "
                # author email
                f"--msgid-bugs-address {self._str_email} "
                # sort entries by file
                "-F "
                # don't add location info (hide path to source)
                # "--no-location "
                # append existing file
                # NB: this is the key to running xgettext multiple times for
                # one domain
                # this allows us to set the -L option for different file types
                # and still end up with one unified .pot file
                "-j "
                # final name of output file
                # NB: note that you can fiddle with the -o, -d, and -p options
                # here, but i find it's just better to use an abs path to the
                # output file
                f"-o {file_pot} "
                # add -L for specific exts
                f"-L {clang_name} "
            )

            if not self._location:
                cmd += "--no-location "

            # add all input files
            paths = [f'"{item}" ' for item in clang_files]
            j_paths = "".join(paths)
            cmd += j_paths

            # do the final command
            F.sh(cmd, shell=True)

            # fix CHARSET in pot
            self._fix_pot_header(file_pot)

    # --------------------------------------------------------------------------
    # Merge any .po files in the pos folder with existing .po files
    # --------------------------------------------------------------------------
    def _make_pos(self):
        """
        Create .po files in the po folder or merge any updated .pot files with
        existing .po files

        Whenever a new .pot file is generated using make_pot, this method will
        produce a new .po file for each wlang that contains the difference
        between the new .pot file and the existing .po file.

        This new .po file should be sent to the translator for each wlang. Then
        when the translator sends back the translated .po file, place it in the
        appropriate <dir_po>/<wlang> dir. Then run pybaker to create a new .mo
        file.
        """

        # for each wlang in the po folder
        for wlang in self._list_wlangs:

            # get the pot file we made in the last step
            file_pot = self._dir_pot / f"{self._str_domain}{self.S_EXT_POT}"

            # create or update the .po file
            file_po = (
                self._dir_po / f"{wlang}/{self._str_domain}{self.S_EXT_PO}"
            )
            file_po.parent.mkdir(parents=True, exist_ok=True)
            if not file_po.exists():

                # no po file, copy pot
                shutil.copy(file_pot, file_po)
                continue

            # update existing po file using latest pot
            cmd = self.S_CMD_MERGE_POS.format(file_po, file_pot)
            F.sh(cmd)

    # --------------------------------------------------------------------------
    # Create .mo files for all .po files in the locale folder
    # --------------------------------------------------------------------------
    def _make_mos(self):
        """
        Create .mo files for all .po files in the locale folder

        Makes all the required .mo files for all the .po files in the locale
        dir
        """

        # get all wlangs to output
        list_pos = list(self._dir_po.glob(f"*/*{self.S_EXT_PO}"))

        # for each wlang
        for file_po in list_pos:

            # get wlang name
            wlang = file_po.parent.name  # en, etc

            # get .mo file (output)
            mo_dir = self._dir_locale / wlang / self.S_DIR_LC
            mo_dir.mkdir(parents=True, exist_ok=True)
            mo_file = mo_dir / f"{self._str_domain}{self.S_EXT_MO}"

            # do the command
            cmd = self.S_CMD_MAKE_MOS.format(mo_file, file_po)
            F.sh(cmd)

    # --------------------------------------------------------------------------
    # Make a list of all supported written language directories
    # --------------------------------------------------------------------------
    def _make_wlang_dirs(self):
        """
        Make a list of all supported written language directories

        This writes the LINGUAS file, which is used for i18n'ing a .desktop
        file.
        """

        # ----------------------------------------------------------------------

        # make the main dirs
        self._dir_pot.mkdir(parents=True, exist_ok=True)
        self._dir_po.mkdir(parents=True, exist_ok=True)
        self._dir_locale.mkdir(parents=True, exist_ok=True)

        # make the LC dirs
        for wlang in self._list_wlangs:

            # make the locale/lang/LC_MESSAGES dir
            mo_dir = self._dir_locale / wlang / self.S_DIR_LC
            mo_dir.mkdir(parents=True, exist_ok=True)

        # make LINGUAS file
        linguas = ""
        for wlang in self._list_wlangs:
            # add each wlang to LINGUAS file
            linguas += f"{wlang}/{self._str_domain} "

        # write the LINGUAS file
        linguas_path = self._dir_po / self.S_FILE_LINGUAS
        with open(linguas_path, "w", encoding="UTF8") as f:
            f.write(linguas)

    # --------------------------------------------------------------------------
    # Scan the source dirs for files with certain extensions
    # --------------------------------------------------------------------------
    def _get_paths_for_clangs(self):
        """
        Scan the source dirs for files with certain extensions

        Returns:
            A dictionary containing file paths to source files

        This method converts the dict_clangs dictionary:
            {
                "Python": [".py"],
                "Glade": [".ui", ".glade"],
                "Desktop": [".desktop"],
            }
        into a dictionary of file paths to scan for each clang:
            {
                "Python": [<Path>, ...],
                "Glade": [<Path>, ...],
                "Desktop": [<Path>, ...],
            }
        so they can be passed to xgettext.
        """

        # return value
        scan_all = {}

        # make src paths abs to prj dir
        abs_srcs = [
            self._dir_prj / src if not Path(src).is_absolute() else Path(src)
            for src in self._list_src
        ]

        # for each full src
        for abs_src in abs_srcs:

            # get default result
            dict_res_src = {}

            # get all files for all clangs (or all files if no clangs)

            # get all paths to all files in source dir, recursively
            # NB: very important to convert generator to list here
            # this is because generators use yield to return every result
            # individually, while lists are monolithic (rglob is a generator)
            # you cannot iterate over a generator's yield result, because it is
            # generally only one item, while a list contains all results
            # calling list() on a generator causes the generator to give ALL
            # it's generated results to the final list

            # assume file, or glob if dir
            paths = [abs_src]
            if abs_src.is_dir():
                paths = list(abs_src.rglob("*"))

            # for each clang name / list of exts
            for clang, ext_list in self._dict_clangs.items():

                # sanity check to add dots for exts that don't start with dot
                # (dots needed for path.suffix matching)
                exts = [
                    f".{item}" if not item.startswith(".") else item
                    for item in ext_list
                ]
                exts = [item.lower() for item in exts]

                # get all paths that match file ext
                files = [f for f in paths if f.suffix.lower() in exts]

                # make sure the key exists
                if not clang in dict_res_src:
                    dict_res_src[clang] = []

                # add results to langs that have extensions
                dict_res_src[clang].extend(files)

            # now time to handle files with no ext
            for clang, name_list in self._dict_no_ext.items():

                # get all paths that match file name
                # NB: the is_file() check here is to make sure we only add
                # files that have no ext, not dirs (which have no ext, obvs)
                files = [
                    f for f in paths if f.name in name_list if f.is_file()
                ]

                # make sure the key exists
                if not clang in dict_res_src:
                    dict_res_src[clang] = []

                # add results to langs that have extensions
                dict_res_src[clang].extend(files)

            # add them all up
            scan_all = F.combine_dicts(dict_res_src, scan_all)

        # return result
        return scan_all

    # --------------------------------------------------------------------------
    # Set the header values for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self, file_pot):
        """
        Set the header values for the pot which will carry over to each po

        Args:
            file_pot: the path object representing the pot file to fix

        Fix the charset in the pot file to a known value so that msgfmt does
        not complain. The charset for an individual file can be set by the
        translator. This is just to keep the compiler from complaining, and
        also aids in testing when no editing is done.
        """

        # open file and get contents
        with open(file_pot, "r", encoding="UTF-8") as a_file:
            text = a_file.read()

        # replace short description
        str_pattern = self.R_TITLE_SCH
        str_rep = self.R_TITLE_REP.format(self._str_domain)
        text = re.sub(str_pattern, str_rep, text)

        # replace copyright
        str_pattern = self.R_COPY_SCH
        year = date.today().year
        str_rep = self.R_COPY_REP.format(year, self._str_author)
        text = re.sub(str_pattern, str_rep, text)

        # replace author's email
        str_pattern = self.R_EMAIL_SCH
        email = self._str_email
        year = date.today().year
        str_rep = self.R_EMAIL_REP.format(email, year)
        text = re.sub(str_pattern, str_rep, text)

        # NB: if the specific phrase "CHARSET" is not found, nothing will be
        # changed
        str_pattern = self.R_CHAR_SCH
        str_rep = self.R_CHAR_REP.format(self._charset)
        text = re.sub(str_pattern, str_rep, text, flags=re.M)

        # save file
        with open(file_pot, "w", encoding="UTF-8") as a_file:
            a_file.write(text)


# -)
