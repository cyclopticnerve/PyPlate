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
import gettext
import locale
from pathlib import Path
import re
import shutil

# my imports
import cnfunctions as F

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./pybaker.py

T_DOMAIN = "cnlib"
T_DIR_PRJ = Path(__file__).parents[1].resolve()
T_DIR_LOCALE = f"{T_DIR_PRJ}/i18n/locale"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

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
    S_DEF_CHARSET = "UTF-8"

    # NB: DO NOT CHANGE THESE! i only put them here because they are strings
    # default locale folder under i18n
    S_DIR_LOCALE = "locale"
    # default po folder under i18n
    S_DIR_PO = "po"
    # default pot folder under i18n
    S_DIR_POT = "pot"
    # this is the default subdir for GNU
    S_DIR_MESSAGES = "LC_MESSAGES"
    # the file to store all wlangs for bulk operations
    S_FILE_LINGUAS = "LINGUAS"
    # default file extensions
    S_POT_EXT = ".pot"
    S_PO_EXT = ".po"
    S_MO_EXT = ".mo"

    # shell commands to make po/mo
    # NB: format params are po_file and pot_file
    S_CMD_MERGE_POS = "msgmerge --update {} {} --backup=none"
    # NB: format params are mo_file and wlang_po
    S_CMD_MAKE_MOS = "msgfmt -o {} {}"
    # NB: format params are po dir, template dir, and output file
    S_CMD_DSK = "msgfmt --desktop -d {} --template={} -o {}"

    # error messages
    # I18N: path {} is not absolute
    # NB: format param is dir_prj
    S_ERR_NOT_ABS = _("path {} is not absolute")
    # I18N: path {} is not a directory
    # NB: format param is dir_prj
    S_ERR_NOT_DIR = _("path {} is not a directory")

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
        str_version,  # pub
        str_author,  # prv
        str_email,  # prv
        # base prj dir
        dir_prj,
        # in
        dict_domains,
        # out
        dir_i18n,
        # optional in
        str_tag=None,
        dict_clangs=None,  # pub
        dict_no_ext=None,  # pub
        list_wlangs=None,  # pub
        charset=None,  # pub
    ):
        """
        Initialize the new object

        Args:

            str_domain: Name to use in .pot/.po header
            str_version: Version info to use in .pot/.po header
            str_author: Author name to use in .pot/.po header
            str_email: Email to use in .pot/.po header

            dir_prj: Used for relative paths

            dir_src: Where to start looking for input files

            dir_pot: Directory to place master .pot file

            dir_locale: Where to put output locale files (default:
            dir_src/"locale")
            dir_po: Where to put new .po files that are waiting to be merged
            (default: dir_src/dir_locale/"po")
            str_domain: The name of the domain (base name) for output files
            (default: "messages")
                This creates files like "<str_domain>.pot", "<str_domain>.po",
                and "<str_domain>.mo", and is used in the .py scripts to bind a
                domain to a locale folder

            str_tag: Tag that starts a context comment (default: "")
                If this string is empty, all comments above an entry are
                included as context
            dict_clangs: The dictionary of file extensions to scan for each
            clang\n
            Note that if ths dict is empty or None, all files will be scanned
            (this is generally considered * A Very Bad Thing *)
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

        # set header info
        self._str_version = str_version
        self._str_author = str_author
        self._str_email = str_email

        # set base props
        self._dir_prj = Path(dir_prj)
        if not self._dir_prj.is_absolute():
            raise OSError(self.S_ERR_NOT_ABS.format(self._dir_prj))
        if not self._dir_prj.is_dir():
            raise OSError(self.S_ERR_NOT_DIR.format(self._dir_prj))

        # fix up dict_domains
        if dict_domains is None:
            dict_domains = {}
        self._dict_domains = dict_domains

        # set out props
        self._dir_i18n = Path(dir_i18n)
        if not self._dir_i18n.is_absolute():
            self._dir_i18n = self._dir_prj / dir_i18n

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
            charset = self.S_DEF_CHARSET
        self._charset = charset

        # set up folder props
        self._dir_locale = self._dir_i18n / self.S_DIR_LOCALE
        self._dir_po = self._dir_i18n / self.S_DIR_PO
        self._dir_pot = self._dir_i18n / self.S_DIR_POT

    # --------------------------------------------------------------------------
    # Public methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Run the program and make or update the files
    # --------------------------------------------------------------------------
    def main(self):
        """
        Run the program and make or update the files

        Main method of the class, performing its steps.
        """

        # ----------------------------------------------------------------------
        # do the steps

        self._make_pot()
        self._merge_pos()
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

        # sanity check
        dt_template = Path(dt_template)
        if not dt_template.is_absolute():
            dt_template = self._dir_prj / dt_template
        dt_out = Path(dt_out)
        if not dt_out.is_absolute():
            dt_out = self._dir_prj / dt_out

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

        # for each src folder in each domain
        for domain, srcs in self._dict_domains.items():

            # get path to pot file
            pot_file = self._dir_pot / f"{domain}{self.S_POT_EXT}"

            # delete the existing .pot file (if it exists)
            pot_file.unlink(missing_ok=True)

            # create a new, empty .pot file if it does not exist
            # NB: this allow us to use the -j flag without error (which would
            # happen if the current file to join does not exist)
            pot_file.parent.mkdir(parents=True, exist_ok=True)
            pot_file.touch(exist_ok=True)

            # get all paths for this domain
            files_dict = self._get_paths_for_domain(srcs, self._dict_clangs)

            # for each clang name / list of clang files
            for clang_name, clang_files in files_dict.items():

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
                    f"--package-name {domain} "
                    f"--package-version {self._str_version} "
                    # author email
                    f"--msgid-bugs-address {self._str_email} "
                    # sort entries by file
                    "-F "
                    # don't add location info (hide path to source)
                    "--no-location "
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
                )

                # add -L for specific exts
                if clang_name != "*":
                    cmd += f"-L {clang_name} "

                # add all input files
                paths = [f"\"{item}\" " for item in clang_files]
                j_paths = "".join(paths)
                cmd += j_paths

                # do the final command
                F.sh(cmd, shell=True)

            # fix CHARSET in pot
            self._fix_pot_header(domain, pot_file)

    # --------------------------------------------------------------------------
    # Merge any .po files in the pos folder with existing .po files
    # --------------------------------------------------------------------------
    def _merge_pos(self):
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

        # for each domain
        for domain in self._dict_domains:

            # for each wlang in the po folder
            for wlang in self._list_wlangs:

                # get the pot file we made in the last step
                pot_file = self._dir_pot / f"{domain}{self.S_POT_EXT}"

                # create or update the .po file
                po_file = self._dir_po / f"{wlang}/{domain}{self.S_PO_EXT}"
                po_file.parent.mkdir(parents=True, exist_ok=True)
                if not po_file.exists():

                    # no po file, copy pot
                    shutil.copy(pot_file, po_file)
                    continue

                # update existing po file using latest pot
                cmd = self.S_CMD_MERGE_POS.format(po_file, pot_file)
                F.sh(cmd)

                # fix po version
                with open(po_file, "r", encoding="UTF-8") as a_file:
                    text = a_file.read()

                rep = self.R_VER_REP.format(self._str_version)
                text = re.sub(self.R_VER_SCH, rep, text, flags=re.M)

                # write fixed text back to file
                with open(po_file, "w", encoding="UTF-8") as a_file:
                    a_file.write(text)

    # --------------------------------------------------------------------------
    # Create .mo files for all .po files in the locale folder
    # --------------------------------------------------------------------------
    def _make_mos(self):
        """
        Create .mo files for all .po files in the locale folder

        Makes all the required .mo files for all the .po files in the locale
        dir
        """

        # make sure all necessary dirs exist
        self._make_wlang_dirs()

        # get all wlangs to output
        wlangs_pos = list(self._dir_po.glob(f"*/*{self.S_PO_EXT}"))

        # for each wlang
        for wlang_po in wlangs_pos:

            # get wlang name
            wlang_name = wlang_po.parent.name  # en, etc
            domain = wlang_po.stem

            # get .mo file (output)
            mo_dir = self._dir_locale / wlang_name / self.S_DIR_MESSAGES
            mo_dir.mkdir(parents=True, exist_ok=True)
            mo_file = mo_dir / f"{domain}{self.S_MO_EXT}"

            # do the command
            cmd = self.S_CMD_MAKE_MOS.format(mo_file, wlang_po)
            F.sh(cmd)

    # --------------------------------------------------------------------------
    # Scan the source dir for files with certain extensions
    # --------------------------------------------------------------------------
    def _get_paths_for_domain(self, srcs, dict_clangs):
        """
        Scan the source dir for files with certain extensions

        Args:
            srcs: An array of dirs to search, relative to _dir_pj
            dict_clangs: The dictionary of clang names / clang extensions to
            scan for

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
                "Desktop": [<Path>, ...],
            }
        so they can be passed to xgettext.
        """

        # return value
        scan_all = {}

        # make src paths abs to prj dir
        abs_srcs = [self._dir_prj / src for src in srcs]

        # for each full src
        for abs_src in abs_srcs:

            # get default result
            dict_res = {}

            # get all files for all clangs (or all files if no clangs)

            # get all paths to all files in source dir, recursively
            # NB: very important to convert generator to list here
            # this is because generators use yield to return every result
            # individually, while lists are monolithic (and rglob is a generator)
            # you cannot iterate over a generator's yield result, because it is
            # generally only one item, while a list contains all results
            # calling list() on a generator causes the generator to give ALL it's
            # generated results to the final list
            paths = list(abs_src.rglob("*"))

            # sanity check
            if not dict_clangs or len(dict_clangs) == 0:
                scan_all["*"] = paths.copy()
                return scan_all

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

            # add them all up
            scan_all = F.combine_dicts(dict_res, scan_all)

        # return result
        return scan_all

    # --------------------------------------------------------------------------
    # Make a list of all supported written language directories
    # --------------------------------------------------------------------------
    def _get_wlang_names(self):
        """
        Make a list of all supported written language directories

        Finds all known written languages just before calling a function.

        The idea is to get all *existing* languages on disk, then
        add all the languages passed in to the constructor.

        This method is used to get a list of all languages installed, which is
        in turn used to write the LINGUAS file. That file is in turn used to do
        i18n on the .desktop file. The logic here is a little fuzzy, so try to
        keep the removal of languages in sync between disk and the list passed
        to the constructor. Adding languages should be as easy as adding a
        wlang identifier to pyplate/project.json.
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
        locale_wlangs = [item.stem for item in locale_wlangs]

        # sweep po folder for wlangs and reduce to ISO name
        po_wlangs_glob = self._dir_po.glob(f"*{self.S_PO_EXT}")
        # convert generator to list
        po_wlangs = list(po_wlangs_glob)
        # only dirs
        po_wlangs = [item for item in po_wlangs if item.is_file()]
        # only names (last path component)
        po_wlangs = [item.stem for item in po_wlangs]

        # combine locale and po wlangs (whatever we found on disk)
        list_on_disk = locale_wlangs + po_wlangs
        # remove duplicates
        set_on_disk = set(list_on_disk)
        # convert back to list
        list_on_disk.extend(set_on_disk)

        # add any names passed in via list_wlangs (should be ISO names)
        list_comb = list_on_disk + self._list_wlangs
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
        """
        Make a list of all supported written language directories

        This writes the LINGUAS file, which is used for i18n'ing a .desktop
        file.
        """

        # get names of all wlangs present in po/locale/property
        self._get_wlang_names()

        # empty linguas contents
        linguas = ""

        # make the po dir where we will put updated files to be merged
        Path.mkdir(self._dir_po, parents=True, exist_ok=True)
        Path.mkdir(self._dir_pot, parents=True, exist_ok=True)

        # go through the wlang list
        for wlang in self._list_wlangs:

            # make the locale/lang/LC_MESSAGES dir
            d = self._dir_locale / wlang / self.S_DIR_MESSAGES
            Path.mkdir(d, parents=True, exist_ok=True)

            # add each wlang to LINGUAS file
            linguas += wlang + " "

        # write the LINGUAS file
        linguas_path = self._dir_po / self.S_FILE_LINGUAS
        with open(linguas_path, "w", encoding="UTF8") as f:
            f.write(linguas)

    # --------------------------------------------------------------------------
    # Set the charset for the pot which will carry over to each po
    # --------------------------------------------------------------------------
    def _fix_pot_header(self, domain, file_pot):
        """
        Set the charset for the pot which will carry over to each po

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
        str_rep = self.R_TITLE_REP.format(domain)
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
