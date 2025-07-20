# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: mkdocs.py                                             |     ()     |
# Date    : 07/11/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module makes documentation for a project using MkDocs. It uses the
project's source files and the config file "mkdocs.yml" to create MarkDown
files in the "docs" folder. It then builds the html file structure in the
"site" folder. It uses the "gh-deploy" program to publish the site to a
remote-only branch. It then instructs GitHub Pages to auto-publish your docs at
<username>.github.io/<repo_name> from that branch.
As much code/settings/constants as can be are reused from conf.py.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
import gettext
import locale
from pathlib import Path
import shutil
import subprocess

# local imports
# pylint: disable=no-name-in-module
from . import conf

# ------------------------------------------------------------------------------
# Globals
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# gettext stuff for CLI
# NB: keep global
# to test translations, run as foo@bar:$ LANGUAGE=xx ./__PP_NAME_PRJ_SMALL__.py

# path to project dir
T_DIR_PRJ = Path(__file__).parents[1].resolve()

# init gettext
T_DOMAIN = "pyplate"
T_DIR_LOCALE = T_DIR_PRJ / "i18n/locale"
T_TRANSLATION = gettext.translation(T_DOMAIN, T_DIR_LOCALE, fallback=True)
_ = T_TRANSLATION.gettext

# fix locale (different than gettext stuff, mostly fixes GUI issues, but ok to
# use for CLI in the interest of common code)
locale.bindtextdomain(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# cmd for mkdocs
# NB: format params are path to pp, path to pp venv, and path to project
S_CMD_DOC_BUILD = "cd {};. {}/bin/activate;cd {};mkdocs build"

# cmd for mkdocs
# NB: format params are path to pp, path to pp venv, and path to project
S_CMD_DOC_DEPLOY = "cd {};. {}/bin/activate;cd {};mkdocs gh-deploy"

# file ext for in/out
S_EXT_IN = ".py"
S_EXT_OUT = ".md"

# more out dirs
S_DIR_API = "docs/API"

# default to include mkdocstrings content in .md file
# NB: format params are file name, pkg (parent dir) name, and module name
S_DEF_FILE = "# {}\n::: {}.{}"

# config file name (will be made abs to prj dir)
S_YML_NAME = "mkdocs.yml"

# config file content
# NB: format params are prj dir name (same as __PP_NAME_PRJ_BIG__),
# conf.S_MKDOCS_THEME
S_YML_TEXT = (
    "site_name: {}\n"
    "theme: {}\n"
    "plugins:\n"
    "- search\n"
    "- mkdocstrings\n"
)

# name of home page file (DO NOT CHANGE!!!)
S_INDEX_NAME = "index.md"
# I18N: name of home link in nav
S_HOME_NAME = _("Home")

# err message if no remote repo
S_ERR_NO_REPO = _(
    "MkDocs failed to deploy. Make sure you have published your repo and run\n"
    "'pybaker' from your project directory to publish your docs using MkDocs."
)


# ------------------------------------------------------------------------------
# Make docs using mkdocs
# ------------------------------------------------------------------------------
def make_docs(dir_prj, dict_prv, dict_pub, p_dir_pp, p_dir_pp_venv):
    """
    Make docs using mkdocs

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        p_dir_pp: Path to PyPlate program
        p_dir_pp_env: Path to PyPlate's venv (to activate pdoc3)

    Make the documents using the specified parameters.
    """

    # where to put the .md files
    dir_docs_out = dir_prj / conf.S_DIR_DOCS

    # --------------------------------------------------------------------------
    # make yaml

    # path to file
    yaml_file = dir_prj / S_YML_NAME
    if not yaml_file.exists():

        # file text
        theme = ""
        if conf.S_MKDOCS_THEME == conf.S_THEME_RTD:
            theme = conf.S_THEME_RTD
        text = S_YML_TEXT.format(dir_prj.name, theme)

        # write file
        with open(yaml_file, "w", encoding=conf.S_ENCODING) as a_file:
            a_file.write(text)

    # --------------------------------------------------------------------------
    # make home page
    # NB: just copy readme.md to index.md

    # path to files
    readme_file = dir_prj / conf.S_FILE_README
    index_file = dir_docs_out / S_INDEX_NAME
    if not index_file.exists():
        # read input file
        text = ""
        with open(readme_file, "r", encoding=conf.S_ENCODING) as a_file:
            text = a_file.read()

        # write file
        with open(index_file, "w", encoding=conf.S_ENCODING) as a_file:
            a_file.write(text)

    # copy image for index.md as README.md
    prj_name = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_NAME_PRJ_SMALL__"]
    prj_img = prj_name + ".png"
    img_src = dir_prj / conf.S_DIR_IMAGES / prj_img
    dir_img_dest = dir_docs_out / conf.S_DIR_IMAGES
    dir_img_dest.mkdir(parents=True, exist_ok=True)

    shutil.copy(img_src, dir_img_dest)

    # --------------------------------------------------------------------------
    # run mkdocstrings

    # NB: this function uses the blacklist to filter files at the very end of
    # the fix process. at this point you can assume ALL dunders in ALL eligible
    # files have been fixed, as well as paths/filenames. also dict_pub and
    # dict_prv have been undunderized
    dict_bl = dict_pub[conf.S_KEY_PUB_BL]

    # just shorten the names
    skip_all = dict_bl[conf.S_KEY_SKIP_ALL]
    skip_contents = dict_bl[conf.S_KEY_SKIP_CONTENTS]

    # --------------------------------------------------------------------------
    # do the fixes

    files_out = []

    # NB: root is a full path, dirs and files are relative to root
    for root, root_dirs, root_files in dir_prj.walk():

        # handle dirs in skip_all
        if root in skip_all:
            # NB: don't recurse into subfolders
            root_dirs.clear()
            continue

        # convert files into Paths
        files = [root / f for f in root_files]
        files = [f for f in files if f.suffix.lower() == S_EXT_IN]

        # for each file item
        for item in files:

            # handle files in skip_all
            if item in skip_all:
                continue

            # handle dirs/files in skip_contents
            if not root in skip_contents and not item in skip_contents:

                # add the python file to the list
                files_out.append(item)

    # --------------------------------------------------------------------------
    # make structure

    # for each py file
    for f in files_out:

        # make the api folder
        dir_docs_api = dir_prj / S_DIR_API
        dir_docs_api.mkdir(parents=True, exist_ok=True)

        # make a parent folder in docs (goes in nav bar)
        # NB: basically we find every .py file and get its path relative to
        # project dir
        # then we make a folder with the same relative path, but rel to docs
        # dir
        path_rel = f.relative_to(dir_prj)
        path_doc = dir_docs_api / path_rel.parent
        path_doc.mkdir(parents=True, exist_ok=True)

        # create a default file
        # NB: just swap ".py" ext for ".md"
        file_md = path_doc / Path(str(f.stem) + S_EXT_OUT)

        # format contents of file
        file_fmt = S_DEF_FILE.format(f.name, f.parent.name, f.stem)
        with open(file_md, "w", encoding=conf.S_ENCODING) as a_file:
            a_file.write(file_fmt)

    # --------------------------------------------------------------------------
    # make docs

    # format cmd using pdoc template dir, output dir, and start dir
    cmd_docs = S_CMD_DOC_BUILD.format(
        p_dir_pp,
        p_dir_pp_venv,
        dir_prj,
    )

    # the command to run pdoc
    try:
        subprocess.run(
            cmd_docs,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
    except Exception as e:
        raise e


# ------------------------------------------------------------------------------
# Deploy docs using mkdocs
# ------------------------------------------------------------------------------
def deploy_docs(dir_prj, _dict_prv, _dict_pub, p_dir_pp, p_dir_pp_venv):
    """
    Deploy docs using mkdocs

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        p_dir_pp: Path to PyPlate program
        p_dir_pp_env: Path to PyPlate's venv (to activate pdoc3)

    Deploy the documents using the specified parameters.
    """

    # format cmd using pdoc template dir, output dir, and start dir
    cmd_docs = S_CMD_DOC_DEPLOY.format(
        p_dir_pp,
        p_dir_pp_venv,
        dir_prj,
    )

    # the command to run mkdocs
    try:
        subprocess.run(
            cmd_docs,
            shell=True,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
    except Exception as e:
        print(S_ERR_NO_REPO)
        raise e


# -)
