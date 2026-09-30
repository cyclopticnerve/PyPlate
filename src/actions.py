# ------------------------------------------------------------------------------
# Package :PyPlate                                                /          \
# Filename: actions.py                                            |     ()     |
# Date    : 09/03/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module contains the actions to run as we make or bake a project.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path
import shutil
from typing import Any, Callable

# cnlib imports
from cnlib import cnfunctions
from cnlib.cnpot import CNPotPy
from cnlib.cntree import CNTree
from cnlib.cnvenv import CNVenv
# from cnlib.decorators import cnspinner

# local imports
import conf
import meta
import ppglobals
import ppmkdocs
import spinner

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Run an action
# ------------------------------------------------------------------------------
def action_run(
    dict_act: dict[str, Any],
    key: str,
    msg: str,
    action_func: Callable,
    dir_prj: Path,
    dict_prv: dict[str, Any],
    dict_pub: dict[str, Any],
):
    """
    Run an action

    Arguments:
        dict_act: the dict of acts and whether to perform them
        key: name of action i.e. conf.S_KEY_ACT_VENV to make venv
        msg: what to print while doing the action, or when skipped
        action_func: the real function to be decorated
        dir_prj: project directory (arg to action_func)
        dict_prv: private.json (arg to action_func)
        dict_pub: project.json (arg to action_func)

    This is just a convenience function to handle skipping or handling an
    action. Skipping should be pretty self-explanatory. An error message will
    only be shown after all steps are completed.
    """

    # handle skip
    if not dict_act[key]:
        spinner.skip(msg)
        return

    # any action_func may throw an error, which will be returned by cnspinner.
    # to be clear, cnspinner handles printing the "fail" message (and possibly
    # printing the error message, if cnfunctions.B_PP_DEBUG is True). the
    # cnspinner function will then return the error here, so we can set
    # B_PP_RESULT.
    err = action_func(dir_prj, dict_prv, dict_pub)
    if err:
        ppglobals.B_PP_RESULT = False


# ------------------------------------------------------------------------------
# Make a venv in the project directory
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_VENV)
def action_venv(
    dir_prj: Path, dict_prv: dict[str, Any], _dict_pub: dict[str, Any]
):
    """
    Make a venv in the project directory

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        _dict_pub: The PyPlate public dict (not used)

    This function makes a venv in the project directory.
    """

    # get name of venv folder and reqs file
    dir_venv = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]

    # create a cnvenv object
    cv = CNVenv(dir_prj, dir_venv)

    # create venv
    cv.create()

# ------------------------------------------------------------------------------
# Install reqs in venv
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_REQS)
def action_reqs(
    dir_prj: Path, dict_prv: dict[str, Any], _dict_pub: dict[str, Any]
):
    """
    Install reqs in venv

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        _dict_pub: The PyPlate public dict (not used)

    This function installs the requirements from the requirements.txt file.
    """

    # get name of venv folder and reqs file
    dir_venv = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]

    # create a cnvenv object
    cv = CNVenv(dir_prj, dir_venv)

    # get name of venv folder and reqs file
    file_reqs = dir_prj / conf.S_FILE_REQS

    # install requirements
    cv.install_reqs(file_reqs)


# ------------------------------------------------------------------------------
# Make git repo for new project
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_GIT)
def action_git(
    dir_prj: Path, _dict_prv: dict[str, Any], _dict_pub: dict[str, Any]
):
    """
    Make git repo for new project

    Args:
        dir_prj: The project directory
        _dict_prv: The PyPlate private dict (not used)
        _dict_pub: The PyPlate public dict (not used)

    This function creates a new .git folder in the project.
    """

    # add git dir
    cmd = conf.S_CMD_GIT_CREATE.format(dir_prj)
    # NB: we use capture_output=True to hide the terminal output
    cnfunctions.run(cmd, shell=True, capture_output=True)


# ------------------------------------------------------------------------------
# Whether to create an install dict in project.json
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_INST)
def action_inst(
    dir_prj: Path, dict_prv: dict[str, Any], dict_pub: dict[str, Any]
):
    """
    Whether to create an install dict in project.json

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    This function creates an install dict in project.json (public) for CLI/GUI
    projects.
    """

    # make the project.json inst dict
    prj_type = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]
    dict_pub[conf.S_KEY_PUB_INST] = dict(conf.D_TYPE_INST[prj_type])

    # create a template and save cfg file
    dict_inst = dict_pub[conf.S_KEY_PUB_INST]

    # dict_inst_cont = dict_inst[conf.S_KEY_INST_CONT]
    path_inst = dir_prj / conf.S_DIR_INSTALL / conf.S_FILE_INST_CFG

    # combine dicts
    cnfunctions.save_dict_into_paths(dict_inst, [path_inst])


# ------------------------------------------------------------------------------
# Purge some files
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_PURGE)
def action_purge(
    dir_prj: Path, dict_prv: dict[str, Any], _dict_pub: dict[str, Any]
):
    """
    Purge some files

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        _dict_pub: The PyPlate public dict (not used)

    This function purges some files/folders not needed for certain project
    types.
    """

    prj_type = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # get list of purges for this prj type
    lst_purge = conf.D_PURGE_MAKE[prj_type]

    # make sure all paths are absolute
    lst_purge = [
        (
            ppglobals.Path(dir_prj) / item
            if not ppglobals.Path(item).is_absolute()
            else ppglobals.Path(item)
        )
        for item in lst_purge
    ]

    # nuke any files/folders
    for item in lst_purge:
        if item.exists():
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()


# ------------------------------------------------------------------------------
# Make i18n stuff
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_I18N)
def action_i18n(
    dir_prj: Path, dict_prv: dict[str, Any], dict_pub: dict[str, Any]
):
    """
    Make i18n stuff

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    This function makes (or updates) the i18n folder in the project.
    """

    # --------------------------------------------------------------------------
    # do bulk of i18n

    # check if we want i18n
    prj_type = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]
    if prj_type in conf.L_MAKE_I18N:

        # get settings from project.json
        dict_i18n = dict_pub[conf.S_KEY_PUB_I18N]
        dict_prv_all = dict_prv[conf.S_KEY_PRV_ALL]
        dict_prv_prj = dict_prv[conf.S_KEY_PRV_PRJ]

        # create CNPotPy object
        potpy = CNPotPy(
            dir_prj,  # base dir prj
            dir_prj / dict_i18n[conf.S_KEY_PUB_I18N_DIR],  # out
            list_src=dict_i18n[conf.S_KEY_PUB_I18N_SRC],  # in
            str_domain=dict_prv_prj["__PP_NAME_PRJ_SMALL__"],
            # str_domain=dict_i18n[conf.S_KEY_PUB_I18N_DOM],
            str_version=dict_prv_prj["__PP_VER_MMR__"],
            # str_version=dict_i18n[conf.S_KEY_PUB_I18N_VER],
            str_author=dict_prv_all["__PP_AUTHOR__"],
            # str_author=dict_i18n[conf.S_KEY_PUB_I18N_AUTH],
            str_email=dict_prv_all["__PP_EMAIL__"],
            # str_email=dict_i18n[conf.S_KEY_PUB_I18N_EMAIL],
            str_tag=dict_i18n[conf.S_KEY_PUB_I18N_TAG],
            str_encoding=dict_i18n[conf.S_KEY_PUB_I18N_CHAR],
            dict_clangs=dict_i18n[conf.S_KEY_PUB_I18N_CLANGS],
        )

        # make .pot, .po, and .mo files
        potpy.main()

        # ----------------------------------------------------------------------
        # do .desktop i18n/version

        # path to desktop template
        path_desk_tmp = dir_prj / conf.S_PATH_DSK_TMP
        # path to desktop output
        path_desk_out = (
            dir_prj / dict_prv[conf.S_KEY_PRV_PRJ]["__PP_FILE_DESK__"]
        )

        # check for template.desktop (or rule out using dict)
        if path_desk_tmp.exists():

            # do the thing
            potpy.make_desktop(path_desk_tmp, path_desk_out)


# ------------------------------------------------------------------------------
# Fix placeholders
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_PLACE)
def action_placeholders(
    dir_prj: Path, _dict_prv: dict[str, Any], _dict_pub: dict[str, Any]
):
    """
    Fix placeholders

    Args:
        dir_prj: The project directory
        _dict_prv: The PyPlate private dict (not used)
        _dict_pub: The PyPlate public dict (not used)

    This function adds or removes placeholder files, based on whether or not
    the folder has files in it or not.
    """

    # do not fuck with placeholders in these dirs
    list_skip = []
    for item in conf.L_PH_SKIP:
        res = list(dir_prj.glob(item))
        list_skip.extend(res)

    # for all dirs/subdirs
    for root, root_dirs, root_files in dir_prj.walk():

        # skip .git, etc
        if root in list_skip:
            root_dirs.clear()
            continue

        # if dir is empty
        if len(root_dirs) == 0 and len(root_files) == 0:

            # make a dummy file
            with open(
                root / conf.S_PH_NAME, "w", encoding=conf.S_ENCODING
            ) as a_file:
                a_file.write(conf.S_PH_TEXT)

        # if dir has files/folders and placeholder
        if len(root_dirs) > 0 or len(root_files) > 1:
            for a_file in root_files:
                if a_file == conf.S_PH_NAME:
                    a_path = root / a_file
                    a_path.unlink()


# ------------------------------------------------------------------------------
# Install package in itself
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_EDIT)
def action_edit(dir_prj: Path, dict_prv: dict[str, Any], _dict_pub: dict[str, Any]):
    """
    Install package in itself

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        _dict_pub: The PyPlate public dict (not used)

    This function installs a package project in its own venv as editable. This
    is useful for testing a package in a real-world scenario.
    """

    # get venv name
    dir_venv = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]

    # install
    cmd = conf.S_CMD_VENV_INST_SELF.format(dir_prj, dir_venv)
    cnfunctions.run(cmd, shell=True, capture_output=True)


# ------------------------------------------------------------------------------
# Make tree files
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_TREE)
def action_tree(dir_prj, _dict_prv, dict_pub):
    """
    docstring
    """

    # get path to tree
    file_tree_text = dir_prj / conf.S_TREE_TEXT_FILE
    file_tree_html = dir_prj / conf.S_TREE_HTML_FILE

    file_tree_text.parent.mkdir(exist_ok=True)
    file_tree_html.parent.mkdir(exist_ok=True)

    # create the file so it includes itself
    with open(file_tree_text, "w", encoding=conf.S_ENCODING) as a_file:
        a_file.write("")

    # create the file so it includes itself
    with open(file_tree_html, "w", encoding=conf.S_ENCODING) as a_file:
        a_file.write("")

    # create tree object and call
    tree_obj = CNTree(
        str(dir_prj),
        filter_list=dict_pub[conf.S_KEY_PUB_BL][conf.S_KEY_SKIP_TREE],
        dir_format=conf.S_TREE_DIR_FORMAT,
        file_format=conf.S_TREE_FILE_FORMAT,
        ignore_case=False,
    )
    tree_obj.make_tree()

    # write to file
    with open(file_tree_text, "w", encoding=conf.S_ENCODING) as a_file:
        a_file.write(tree_obj.text)
    with open(file_tree_html, "w", encoding=conf.S_ENCODING) as a_file:
        a_file.write(tree_obj.html)


# ------------------------------------------------------------------------------
# Freeze venv dir
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_FREEZE)
def action_freeze(dir_prj, dict_prv, _dict_pub):
    """docstring"""
    # get name ov venv folder and reqs file
    dir_venv = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]
    file_reqs = dir_prj / conf.S_FILE_REQS

    # do the thing with the thing
    cv = CNVenv(dir_prj, dir_venv)
    cv.freeze(file_reqs)

# ------------------------------------------------------------------------------
# Make docs folder
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_MAKE_DOCS)
def action_make_docs(dir_prj, _dict_prv, dict_pub):
    """
    Make docs folder

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        _dict_pub: The PyPlate public dict (not used)

    This function makes the initial files and folders for using mkdocs.
    """

    # get some props
    dict_docs = dict_pub[conf.S_KEY_PUB_DOCS]
    use_rm = dict_docs[conf.S_KEY_DOCS_USE_RM]
    use_api = dict_docs[conf.S_KEY_DOCS_MAKE_API]
    lst_api_in = dict_docs[conf.S_KEY_DOCS_DIR_API]

    # check if first run
    index_path = dir_prj / conf.S_DIR_DOCS / conf.S_FILE_INDEX
    exist = index_path.exists()

    # if use_rm = true, use rm on every run
    # if use_rm = false, use rm only only on first run
    if use_rm or not exist:
        use_rm = True

    # make docs
    ppmkdocs.make_docs(
        dir_prj,
        conf.S_DIR_DOCS,
        use_rm,
        use_api,
        lst_api_in,
        conf.S_FILE_README,
        conf.S_DIR_API,
        conf.S_DIR_IMAGES,
    )


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_BAKE_DOCS)
def action_bake_docs(dir_prj, _dict_prv, _dict_pub):
    """docstring"""
    # bake docs
    ppmkdocs.bake_docs(dir_prj)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_DEPLOY_DOCS)
def action_deploy_docs(dir_prj, _dict_prv, _dict_pub):
    """docstring"""
    # the command to deploy docs
    ppmkdocs.deploy_docs(dir_prj)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_COMPRESS)
def action_compress(dir_prj, dict_prv, _dict_pub):
    """docstring"""
    # get dist dir for all operations
    dist = ppglobals.Path(dir_prj) / conf.S_DIR_DIST
    name_fmt = str(dict_prv[conf.S_KEY_PRV_PRJ]["__PP_FMT_DIST__"])
    p_dist = dist / name_fmt

    # get out file (dist/prj-<version>.xxx) and in dir (dist/prj-<version>)
    path_out = path_in = str(p_dist)

    # make archive type
    shutil.make_archive(path_out, conf.S_DIST_MODE, path_in)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_REM_DIST)
def action_rem_dist(dir_prj, dict_prv, _dict_pub):
    """docstring"""
    # get dist dir for all operations
    dist = ppglobals.Path(dir_prj) / conf.S_DIR_DIST
    name_fmt = str(dict_prv[conf.S_KEY_PRV_PRJ]["__PP_FMT_DIST__"])
    p_dist = dist / name_fmt

    # delete folder
    shutil.rmtree(p_dist)

# ------------------------------------------------------------------------------
# Fix metadata
# ------------------------------------------------------------------------------
@spinner.spin(conf.S_ACTION_META)
def action_meta(
    dir_prj: Path, dict_prv: dict[str, Any], dict_pub: dict[str, Any]
):
    """
    Fix metadata

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    This function calls all the functions in meta.py, based on file extension.
    """

    # --------------------------------------------------------------------------
    # filter using blacklist

    # NB: this is an example of how to use the blacklist filter in your own
    # customized fix routine

    # NB: this function uses the blacklist to filter files at the very end of
    # the fix process. At this point you can assume ALL dunders in ALL eligible
    # files have been fixed, as well as paths/filenames. also dict_pub has been
    # un-dunderized

    # fix up blacklist and convert relative or glob paths to absolute
    # Path objects

    dict_bl = dict(dict_pub[conf.S_KEY_PUB_BL])

    # for each section of blacklist
    for key, val in dict_bl.items():

        # convert all items in list to pp_globals.Path objects
        list_res = []
        for item in val:
            res = list(dir_prj.glob(item))
            list_res.extend(res)

        # store in local bl
        dict_bl[key] = list_res

    # just shorten the names
    skip_all = dict_bl[conf.S_KEY_SKIP_ALL]
    skip_contents = dict_bl[conf.S_KEY_SKIP_CONTENTS]

    # --------------------------------------------------------------------------
    # fix meta in files
    # NB: this uses blacklist

    # NB: root is a full path, dirs and files are relative to root
    for root, root_dirs, root_files in dir_prj.walk():

        # handle dirs in skip_all
        if root in skip_all:
            # NB: don't recurse into subfolders
            root_dirs.clear()
            continue

        # convert files into Paths
        files = [root / f for f in root_files]

        # for each file item
        for item in files:

            # handle files in skip_all
            if item in skip_all:
                continue

            # handle dirs/files in skip_contents
            if not root in skip_contents and not item in skip_contents:

                # fix content with appropriate dicts
                meta.fix_files(item, dict_prv, dict_pub)


    # -)
