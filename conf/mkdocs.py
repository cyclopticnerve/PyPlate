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
# from pathlib import Path
import shutil
import subprocess

# local imports
# pylint: disable=no-name-in-module
from . import conf

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------

# cmd for mkdocs
# NB: format params are path to pp, path to pp venv, and path to project
S_CMD_DOC_BUILD = "cd {};. {}/bin/activate;cd {};mkdocs build"

# cmd for mkdocs
# NB: format params are path to pp, path to pp venv, and path to project
S_CMD_DOC_DEPLOY = "cd {};. {}/bin/activate;cd {};mkdocs gh-deploy"


# ------------------------------------------------------------------------------
# Make docs using mkdocs
# ------------------------------------------------------------------------------
def make_docs(dir_prj, _dict_prv, _dict_pub, p_dir_pp, p_dir_pp_venv):
    """
    Make docs using mkdocs

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        p_dir_pp: Path to PyPlate program
        p_dir_pp_env: Path to PyPlate's venv (to activate pdoc3)


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
    # make yaml

    yaml_file = dir_prj / "mkdocs.yml"

    text = f"site_name: {dir_prj.name}\n"
    text += "theme: readthedocs\n"
    text += "plugins:\n"
    text += "- search\n"
    text += "- mkdocstrings\n"

    with open(yaml_file, "w", encoding="UTF-8") as a_file:
        a_file.write(text)

    # --------------------------------------------------------------------------
    # make landing page

    index_file = dir_docs_out / "index.md"

    text = "## Hello World!"

    with open(index_file, "w", encoding="UTF-8") as a_file:
        a_file.write(text)

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

    # --------------------------------------------------------------------------
    # deploy

    # format cmd using pdoc template dir, output dir, and start dir
    # cmd_docs = S_CMD_DOC_DEPLOY.format(
    #     p_dir_pp,
    #     p_dir_pp_venv,
    #     dir_prj,
    # )

    # # the command to run pdoc
    # try:
    #     subprocess.run(
    #         cmd_docs,
    #         shell=True,
    #         check=True,
    #         stdout=subprocess.DEVNULL,
    #         stderr=subprocess.STDOUT,
    #     )
    # except Exception as e:
    #     raise e


# -)
