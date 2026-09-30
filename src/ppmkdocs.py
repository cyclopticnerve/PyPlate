# ------------------------------------------------------------------------------
# Package :PyPlate                                                /          \
# Filename: pp_mkdocs.py                                          |     ()     |
# Date    : 09/04/2026                                            |            |
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
from pathlib import Path
import shutil

# lib imports
from cnlib import cnfunctions

# local imports
import conf

# --------------------------------------------------------------------------
# Public functions
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Make docs using mkdocs
# --------------------------------------------------------------------------
def make_docs(
    dir_prj,
    dir_docs,
    use_rm=False,
    use_api=False,
    lst_api_in=None,
    file_rm=None,
    dir_api_out=None,
    dir_img=None,
):
    """
    Docstring for make_docs

    :param self: Description
    :param dir_prj: Description
    :param use_rm: Description
    :param use_api: Description
    :param lst_api_in: Description
    :param file_rm: Description
    :param dir_api_out: Description
    :param dir_img: Description
    """

    # NB: mutable lists are only set once, passing an empty list does
    # NUSSING!!!
    # so we pass None to make sure the internal list gets reset
    if not lst_api_in:
        lst_api_in = []

    # ----------------------------------------------------------------------
    # check docs dir for exist

    # find docs dir
    dir_docs = Path(dir_prj) / dir_docs

    # no docs folder in template
    if not dir_docs.exists():

        # make dir
        dir_docs.mkdir(parents=True)

        # make img dir
        # NB: the name of this dir is hard-coded in mkdocs (AFAIK)
        # it is used exclusively to serve the favicon.ico
        # paths to readme images, etc, can use a different dir
        img_dir = dir_docs / conf.S_MK_DIR_IMG
        img_dir.mkdir(parents=True)

    # ----------------------------------------------------------------------
    # make index

    # make empty or from readme or don't touch
    _make_index(dir_prj, use_rm, file_rm, dir_docs)

    # ----------------------------------------------------------------------
    # make api

    # make new api or delete old
    _make_api(dir_prj, use_api, lst_api_in, dir_api_out, dir_docs)

    # ----------------------------------------------------------------------
    # make img dir

    # dir_img is source (from project main)
    if dir_img:
        # make new img dir or combine
        dir_img_src = Path(dir_prj) / dir_img
        if dir_img_src.exists():
            dir_img_dst = dir_docs / dir_img
            shutil.copytree(dir_img_src, dir_img_dst, dirs_exist_ok=True)


# --------------------------------------------------------------------------
# Bake docs using mkdocs
# --------------------------------------------------------------------------
def bake_docs(p_dir_prj):
    """
    Bake docs using mkdocs

    Raises:
        cnlib.cnfunctions.CNRunError if bake fails

    Updates and deploys docs using mkdocs.
    """

    # ----------------------------------------------------------------------
    # build docs

    # format cmd using pdoc template dir, output dir, and start dir
    cmd = conf.S_CMD_DOC_BUILD.format(p_dir_prj)

    # the command to run mkdocs
    try:
        cp = cnfunctions.run(cmd, shell=True, capture_output=True)
        return cp
    except cnfunctions.CNRunError as e:
        raise e


# --------------------------------------------------------------------------
# Deploy docs using mkdocs
# --------------------------------------------------------------------------
def deploy_docs(p_dir_prj):
    """
    Bake docs using mkdocs

    Raises:
        cnlib.cnfunctions.CNRunError if bake fails

    Updates and deploys docs using mkdocs.
    """

    # ----------------------------------------------------------------------
    # deploy docs

    # format cmd using pdoc template dir, output dir, and start dir
    cmd = conf.S_CMD_DOC_DEPLOY.format(p_dir_prj)

    # the command to run mkdocs
    try:
        cp = cnfunctions.run(cmd, shell=True, capture_output=True)
        return cp
    except cnfunctions.CNRunError as e:
        raise e


# --------------------------------------------------------------------------
# Private functions
# --------------------------------------------------------------------------


# --------------------------------------------------------------------------
# Make the home file (index.md)
# --------------------------------------------------------------------------
def _make_index(dir_prj, use_rm, file_rm, dir_docs):
    """
    Make the home file (index.md)

    Make the index.md file from the README.
    """

    # first check if index exists
    dir_docs_out = Path(dir_prj) / dir_docs
    path_index = dir_docs_out / conf.S_MK_INDEX

    # if not exist
    if not path_index.exists():

        # create empty file
        if not use_rm:
            # create a dummy file
            # NB: i dont like this... what if dev deletes file to reset?
            # we lose the instructions file
            with open(path_index, "w", encoding=conf.S_ENCODING) as a_file:
                a_file.write("Coming soon...")
            return

    # if exist
    else:

        # leave alone
        if not use_rm:
            return

    # ----------------------------------------------------------------------
    # make home page
    # NB: just copy readme.md to index.md
    if use_rm:

        # path to files
        readme_file = Path(dir_prj) / file_rm

        # read input file
        text = ""
        with open(readme_file, "r", encoding=conf.S_ENCODING) as a_file:
            text = a_file.read()

        # write file
        with open(path_index, "w", encoding=conf.S_ENCODING) as a_file:
            a_file.write(text)


# --------------------------------------------------------------------------
# Make the api files
# --------------------------------------------------------------------------
def _make_api(dir_prj, use_api, lst_api_in, dir_api_out, dir_docs):
    """
    Make the api files

    Make the documents using the specified parameters.
    """

    # sanity check
    if not dir_api_out:
        return

    # find api dir
    dir_prj = Path(dir_prj)
    dir_docs_out = dir_prj / dir_docs
    dir_api_out = dir_docs_out / dir_api_out

    # nuke it if it exists and we changed our mind
    if not use_api and dir_api_out.exists():
        shutil.rmtree(dir_api_out)
        return

    # ----------------------------------------------------------------------

    # gather list of full paths to .py files
    files_out = []

    for item in lst_api_in:

        dir_api = dir_prj / item

        # NB: root is a full path, dirs and files are relative to root
        for root, _root_dirs, root_files in dir_api.walk():

            # convert files into Paths
            files = [root / f for f in root_files]
            files = [
                f
                for f in files
                if f.suffix.lower() == conf.S_MK_EXT_IN.lower()
            ]

            # for each file item
            for item in files:
                files_out.append(item)

    # ----------------------------------------------------------------------
    # make structure

    # nuke / remake the api folder
    if dir_api_out.exists():

        # delete and recreate dir
        shutil.rmtree(dir_api_out)
        dir_api_out.mkdir(parents=True)

    # for each py file
    for f in files_out:

        # make a parent folder in docs (goes in nav bar)
        # NB: basically we find every .py file and get its path relative to
        # project dir
        # then we make a folder with the same relative path, but rel to docs
        # dir
        path_rel = f.relative_to(dir_prj)
        path_doc = dir_api_out / path_rel.parent
        path_doc.mkdir(parents=True, exist_ok=True)

        # create a default file
        # NB: just swap ".py" ext for ".md"
        file_md = path_doc / Path(str(f.stem) + conf.S_MK_EXT_OUT)

        # fix rel path into package dot notation
        s_parts = ".".join(path_rel.parts)
        if s_parts.endswith(conf.S_MK_EXT_IN):
            s_parts = s_parts.removesuffix(conf.S_MK_EXT_IN)

        # format contents of file
        file_fmt = conf.S_MK_DEF_FILE.format(f.name, s_parts)
        with open(file_md, "w", encoding=conf.S_ENCODING) as a_file:
            a_file.write(file_fmt)


#  ________________________________________________________________
# < <Diziet> Fuck, I can't compile the damn thing and I wrote it ! >
#  ----------------------------------------------------------------
#         \   ^__^
#          \  (oo)\_______
#             (__)\       )\/\
#                 ||----w |
#                 ||     ||

# -)
