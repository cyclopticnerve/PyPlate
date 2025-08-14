# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pdoc.py                                               |     ()     |
# Date    : 07/11/2025                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module makes documentation for a project using PDoc3. It uses the
project's source files and the config files in the "pdoc3" folder to create
html files in the "docs" folder. It then tweaks the file structure to allow
GitHub Pages to auto-publish your docs at <username>.github.io/<repo_name>. It
also fixes the version number and icon for your docs.
As much code/settings/constants as can be are reused from conf.py.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path
import re
import shutil
import subprocess

# local imports
# pylint: disable=no-name-in-module
from . import conf


# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# relative path to config file
S_PATH_MAKO = "pdoc3/logo.mako"

# name of config dir
S_DIR_PDOC = "pdoc3"
# dir to put image in
S_DIR_IMG = "img"

# cmd for pdoc3
# NB: format params are path to pp, path to pp venv, path to project, path
# to project's template, path to project's docs dir, and path to project's
# input (src) dir
S_CMD_DOC = (
    "cd {};"
    ". {}/bin/activate;"
    "cd {};"
    "pdoc --html --force --template-dir {} -o {} {}"
)

# ext for fixing image
S_HTML_EXT = ".html"

# ------------------------------------------------------------------------------
# regex

# use local image in docs
S_DOC_IMG_SCH = r"(<header>.*<img src=\")(.*?)(\")"
# NB: format param is relative image path
S_DOC_IMG_REP = r"\g<1>{}\g<3>"


# ------------------------------------------------------------------------------
# Make docs using pdoc3
# ------------------------------------------------------------------------------
def make_docs(dir_prj, dict_prv, _dict_pub, p_dir_pp, p_dir_pp_venv):
    """
    Make docs using pdoc3

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        p_dir_pp: Path to PyPlate program
        p_dir_pp_env: Path to PyPlate's venv (to activate pdoc3)

    Fix version number, make the docs, move the docs, and fix the icon paths.
    """

    # --------------------------------------------------------------------------
    # nuke / remake docs dir

    dir_docs_out = dir_prj / conf.S_DIR_DOCS

    # nuke old docs
    if dir_docs_out.exists():

        # delete and recreate docs dir
        shutil.rmtree(dir_docs_out)
        dir_docs_out.mkdir(parents=True)

    # --------------------------------------------------------------------------
    # fix version

    path_mako = dir_prj / S_PATH_MAKO

    # open and read whole file
    with open(path_mako, "r", encoding=conf.S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = conf.S_RM_VER_SCH
    pp_ver_disp = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_VER_DISP__"]
    str_rep = conf.S_RM_VER_REP.format(pp_ver_disp)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # save file
    with open(path_mako, "w", encoding=conf.S_ENCODING) as a_file:
        a_file.write(text)

    # --------------------------------------------------------------------------
    # make docs

    # get template and output dirs
    dir_docs_tplt = dir_prj / S_DIR_PDOC

    # format cmd using pdoc template dir, output dir, and start dir
    cmd_docs = S_CMD_DOC.format(
        p_dir_pp,
        p_dir_pp_venv,
        dir_prj,
        dir_docs_tplt,
        dir_docs_out,
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

    # --------------------------------------------------------------------------
    # fix location

    # find the inner docs folder (named for src dir)
    dir_docs = dir_docs_out / dir_prj.name

    # get all files/dirs in inner dir
    files = list(dir_docs.iterdir())

    # move all files/dirs up one level
    for file in files:
        shutil.move(file, dir_docs_out)

    # delete empty inner dir
    dir_docs.rmdir()

    # --------------------------------------------------------------------------
    # copy image

    # make the inner img dir
    dir_docs_img = dir_docs_out / S_DIR_IMG
    dir_docs_img.mkdir(parents=True)

    # copy image to inner img dir
    img_src = dir_prj / dict_prv[conf.S_KEY_PRV_PRJ]["__PP_IMG_README__"]
    shutil.copy(img_src, dir_docs_img)

    # --------------------------------------------------------------------------
    # fix image

    # where is the image now?
    img_file = Path(S_DIR_IMG) / img_src.name

    # make sure we got a dot ext
    s_html_ext = S_HTML_EXT if S_HTML_EXT.startswith(".") else "." + S_HTML_EXT

    # walk the docs tree
    for root, _dirs, files in dir_docs_out.walk():

        # get full paths and filter for html files
        files = [root / f for f in files]
        files = [f for f in files if f.suffix.lower() == s_html_ext.lower()]

        # for eac html file
        for f in files:

            # get it's rel path to docs folder
            path_rel = f.relative_to(dir_docs_out)

            # calculate number of ups based on depth from docs
            # NB: subtract 1 for no dots if same parent
            level = len(path_rel.parents) - 1

            # build the dots, one set for each level
            dots = ""
            for _i in range(level):
                dots += "../"

            # add the image path rel to prj dir
            dots += str(img_file)

            # format the rep str
            img_rep = S_DOC_IMG_REP.format(dots)

            # open html file for read
            with open(f, "r", encoding=conf.S_ENCODING) as a_file:
                text = a_file.read()

            # replace img src with dots
            text = re.sub(S_DOC_IMG_SCH, img_rep, text, flags=re.S)

            # write text back to file
            with open(f, "w", encoding=conf.S_ENCODING) as a_file:
                a_file.write(text)


# ------------------------------------------------------------------------------
# Bake docs using pdoc3
# ------------------------------------------------------------------------------
def bake_docs(dir_prj, dict_prv, dict_pub, p_dir_pp, p_dir_pp_venv):
    """
    Bake docs using pdoc3

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        p_dir_pp: Path to PyPlate program
        p_dir_pp_env: Path to PyPlate's venv (to activate pdoc3)

    Fix version number, make the docs, move the docs, and fix the icon paths.
    """

    make_docs(dir_prj, dict_prv, dict_pub, p_dir_pp, p_dir_pp_venv)

# -)
