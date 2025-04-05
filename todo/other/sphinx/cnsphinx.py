# ------------------------------------------------------------------------------
# Project : CNLib                                                  /          \
# Filename: cnsphinx.py                                           |     ()     |
# Date    : 10/11/2024                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A class to make handling of docs folders easier
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path
import re

# cnlib imports
from cnlib import cnfunctions as F  # type: ignore

# ------------------------------------------------------------------------------
# Public classes
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# A class to make handling of docs files easier
# ------------------------------------------------------------------------------
class CNSphinx:
    """
    A class to make handling of docs files easier

    Public methods:
        create: Create a new docs folder
        build: Build the docs based on the provided conf.py

    This class provides methods to create, update, and build docs files in the
    project's docs folder.
    """

    # --------------------------------------------------------------------------
    # Class methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Initialize the new object
    # --------------------------------------------------------------------------
    def __init__(self, dir_prj, dir_src, dir_docs):
        """
        Initialize the new object

        Args:
            dir_prj: Path to the project's root dir (can be a string or a Path
            object)
            dir_src: Path or name of the dir where your source files are
            located (can be a strings or a Path object, absolute or relative to
            dir_prj)
            dir_docs: Path or name of the resulting docs folder (can be a
            string or a Path object, absolute or relative to dir_prj)

        Initializes a new instance of the class, setting the default values of
        its properties, and any other code needed to create a new object.
        """

        # save prj dir
        self._dir_prj = Path(dir_prj)

        # if param is not abs, make abs rel to prj dir
        self._dir_src = Path(dir_src)
        # if not self._dir_src.is_absolute():
        #     self._dir_src = self._dir_prj / dir_src

        # if param is not abs, make abs rel to prj dir
        self._dir_docs = Path(dir_docs)
        if not self._dir_docs.is_absolute():
            self._dir_docs = Path(self._dir_prj) / dir_docs

    # --------------------------------------------------------------------------
    # Create a new docs setup given the params
    # --------------------------------------------------------------------------
    def create(self, name, author, version, dirs_import=None, theme=""):
        """
        Create a new docs setup given the params

        Args:
            name: Name of the program (usually camel cased)
            author: Author of the program
            version: Version of the program as a string
            dirs_import: List of paths or names of other files to have Sphinx
            import (can be strings or Path objects, absolute or relative to
            dir_prj) (default: None)
            theme: Name of the theme to use for the docs (default: "")


        Raises:
            cnfunctions.CNShellError if an error occurs

        Creates a new docs folder with the parameters provided.
        """

        # make docs dir
        if not self._dir_docs.exists():
            Path.mkdir(self._dir_docs, parents=True)

        # sanity check
        if not dirs_import:
            dirs_import = []

        # make into Paths
        dirs_import = [Path(dir_import) for dir_import in dirs_import]

        # do imports
        dirs_import = [
            (
                dir_import
                if dir_import.is_absolute()
                else Path(self._dir_prj) / dir_import
            )
            for dir_import in dirs_import
        ]

        # the command to run sphinx-quickstart
        cmd = (
            f"cd {self._dir_docs};"
            f"sphinx-quickstart "
            "--sep "
            f"-p {name} "
            f"-a {author} "
            f"-v {version} "
            f"-r {version} "
            "-l en "
            "--ext-autodoc "
            "--extensions sphinx.ext.napoleon"
        )
        try:
            F.sh(cmd, shell=True)
            self._modify(dirs_import, theme)
        except F.CNShellError as e:
            raise e

    # --------------------------------------------------------------------------
    # Build the docs and create html files
    # --------------------------------------------------------------------------
    def build(self, dir_venv):
        """
        Build the docs and create html files

        Args:
            dir_venv: Location of the project's .venv folder, so that it uses
            the project's virtual environment version of sphinx

        Raises:
            cnfunctions.CNShellError if an error occurs

        Creates the docs/build folder and creates the output html files in the
        docs/build/html folder.
        """

        # if param is not abs, make abs rel to prj dir
        dir_venv = Path(dir_venv)
        if not dir_venv.is_absolute():
            dir_venv = self._dir_prj / dir_venv

        # the command to run sphinx-apidoc and make
        cmd = (
            f"cd {dir_venv.parent};"
            f". {dir_venv.name}/bin/activate; "
            f"cd {self._dir_docs};"
            f"sphinx-apidoc -o source {self._dir_src};"
            "make html"
        )
        try:
            res = F.sh(cmd, shell=True)
            print(res.stdout)
            print(res.stderr)
        except F.CNShellError as e:
            raise e

    # --------------------------------------------------------------------------
    # Private methods
    # --------------------------------------------------------------------------

    # --------------------------------------------------------------------------
    # Modify the conf.py file for imports and theme
    # --------------------------------------------------------------------------
    def _modify(self, dirs_import, theme):
        """
        Modify the conf.py file for imports and theme

        Modifies the newly created docs folder with information on how to find
        other source directories and the theme name. This method is called from
        create().
        """

        # these folder/file names are set in sphinx, don't change them
        path_conf = self._dir_docs / "source/conf.py"

        # block to insert for src path import
        str_imports = "from pathlib import Path\nimport sys\n\n"

        # first do src folder
        str_imports += (
            f"dir_src = Path.home() / {self._dir_src}\n"
            # "sys.path.insert(0, str(dir_src))\n"
        )

        # next do imports
        for dir_import in dirs_import:
            str_imports += (
                f"dir_src = Path.home() / {dir_import}\n"
                # "sys.path.insert(0, str(dir_src))\n"
            )
        str_imports += "\n"

        # open file to fix imports/theme
        with open(path_conf, "r", encoding="UTF-8") as a_file:

            # fix imports
            lines = a_file.readlines()
            lines.insert(0, str_imports)

            # fix theme
            if theme != "":

                # regex to fix theme
                str_pattern = r"html_theme\s*=\s*(.*)"
                str_rep = f"html_theme = '{theme}'"

                # look for theme
                for index, line in enumerate(lines):
                    if re.search(str_pattern, line):
                        line = re.sub(str_pattern, str_rep, line)
                        lines[index] = line

        # save file
        with open(path_conf, "w", encoding="UTF-8") as a_file:
            a_file.writelines(lines)


# -)
