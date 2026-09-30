# ------------------------------------------------------------------------------
# Package :PyPlate                                                /          \
# Filename: hooks.py                                              |     ()     |
# Date    : 09/03/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
This module separates out the pre/post functions, such as do_before_template,
do_after_fix, etc.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# local imports
from datetime import datetime
from pathlib import Path
import shutil

# local imports
import conf
import actions

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Do any work before template copy
# ------------------------------------------------------------------------------
def do_before_template(_dir_prj, _dict_prv, _dict_pub, _dict_act):
    """
    Do any work before template copy

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_act: The dictionary containing the current session's action
        settings

    Do any work before copying the template. This method is called just before
    _do_template, before any files have been copied.\n
    It is mostly used to make final adjustments to the 'dict_prv' and
    'dict_pub' dicts before any copying occurs.
    """


# ------------------------------------------------------------------------------
# Do any work after template copy
# ------------------------------------------------------------------------------
def do_after_template(
    dict_act,
    dir_prj,
    dict_prv,
    dict_pub,
):
    """
    Do any work after template copy

    Args:
        dict_act: The dictionary containing the current session's debug
        settings
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data

    Do any work after copying the template. This function is called after
    _do_template, and before _do_before_fix.\n Use this function to create any
    files that your project needs to be created dynamically. You can also run
    code that is only called by PyMaker before fixing, like chopping
    the readme file sections.
    """
    # get project type
    prj_type = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # --------------------------------------------------------------------------
    # create venv

    # call the spinner-wrapped function
    actions.action_run(
        # check for key presence or skip
        dict_act,  # ok
        conf.S_KEY_ACT_VENV,  # ok
        conf.S_ACTION_VENV,  # ok
        # run action and check for error
        actions.action_venv,  # ok
        dir_prj,  # ok
        dict_prv,  # ok
        dict_pub,  # ok
    )

    # --------------------------------------------------------------------------
    # install reqs

    # call the spinner-wrapped function
    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_REQS,
        conf.S_ACTION_REQS,
        # run action and check for error
        actions.action_reqs,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # --------------------------------------------------------------------------
    # git

    # call the spinner-wrapped function
    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_GIT,
        conf.S_ACTION_GIT,
        # run action and check for error
        actions.action_git,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # --------------------------------------------------------------------------
    # inst/uninst dict inj project.json

    # fix dict_pub
    if prj_type in conf.D_TYPE_INST:
        dict_pub[conf.S_KEY_PUB_INST] = dict(conf.D_TYPE_INST[prj_type])

        # call the spinner-wrapped function
        actions.action_run(
            # check for key presence or skip
            dict_act,
            conf.S_KEY_ACT_INST,
            conf.S_ACTION_INST,
            # run action and check for error
            actions.action_inst,
            dir_prj,
            dict_prv,
            dict_pub,
        )

    # --------------------------------------------------------------------------
    # purge package dirs
    if prj_type in conf.D_PURGE_MAKE:
        # call the spinner-wrapped function
        actions.action_run(
            # test if action should be run
            dict_act,
            conf.S_KEY_ACT_PURGE,
            conf.S_ACTION_PURGE,  # string to print in spinner
            #
            actions.action_purge,  # real function
            dir_prj,  # func params
            dict_prv,
            dict_pub,
        )

    # --------------------------------------------------------------------------
    # do i18n stuff

    if prj_type in conf.D_TYPE_I18N:

        # get dst/src dict
        dict_dst = dict_pub[conf.S_KEY_PUB_I18N]
        dict_src = conf.D_TYPE_I18N[prj_type]

        # fix i18n dict in project.json
        dict_dst[conf.S_KEY_PUB_I18N_SRC] = list(
            dict_src[conf.S_KEY_PUB_I18N_SRC]
        )

    # --------------------------------------------------------------------------
    # set dist dict to default

    dict_pub[conf.S_KEY_PUB_DIST] = dict(conf.D_TYPE_DIST[prj_type])

    # --------------------------------------------------------------------------
    # set DOCS_DIR_API

    if prj_type in conf.D_DOCS_DIR_API:
        dict_pub[conf.S_KEY_PUB_DOCS][conf.S_KEY_DOCS_DIR_API] = (
            conf.D_DOCS_DIR_API[prj_type]
        )


# ------------------------------------------------------------------------------
# Do any work before fix
# ------------------------------------------------------------------------------
def do_before_fix(_dir_prj, dict_prv, dict_pub, _dict_act):
    """
    Do any work before fix

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_act: The dictionary containing the current session's action
        settings
        pymaker: True if called by PyMaker, False if called by PyBaker

    Do any work before fix.\n
    This function is called by both PyMaker and PyBaker.\n
    This method is called just before_do_fix, after all dunders have been
    configured, but before any files have been modified.\n
    It is mostly used to make final adjustments to the 'dict_prv' and
    'dict_pub' dicts before any replacement occurs.
    """

    # --------------------------------------------------------------------------
    # get sub dicts we need
    dict_prv_all = dict_prv[conf.S_KEY_PRV_ALL]
    dict_prv_prj = dict_prv[conf.S_KEY_PRV_PRJ]
    dict_pub_meta = dict_pub[conf.S_KEY_PUB_META]

    # --------------------------------------------------------------------------
    # calculate current date
    # NB: this is the initial create date for all files in the template
    # new files added to the project will have their dates set to the date
    # when pybaker was last run

    # get current date and format it according to dev fmt
    now = datetime.now()
    fmt_date = conf.S_DATE_FMT
    info_date = now.strftime(fmt_date)
    dict_prv_prj["__PP_DATE__"] = info_date

    # --------------------------------------------------------------------------
    # get project names
    name_prj_small = dict_prv_prj["__PP_NAME_PRJ_SMALL__"]
    name_prj_pascal = dict_prv_prj["__PP_NAME_PRJ_PASCAL__"]
    name_sec_small = dict_prv_prj["__PP_NAME_SEC_SMALL__"]
    name_sec_pascal = dict_prv_prj["__PP_NAME_SEC_PASCAL__"]

    # --------------------------------------------------------------------------
    # gui app/win replacements
    dict_prv_prj["__PP_FILE_APP__"] = conf.S_APP_FILE_FMT.format(
        name_prj_small
    )
    dict_prv_prj["__PP_CLASS_APP__"] = conf.S_APP_CLASS_FMT.format(
        name_prj_pascal
    )
    dict_prv_prj["__PP_FILE_WIN__"] = conf.S_WIN_FILE_FMT.format(
        name_sec_small
    )
    dict_prv_prj["__PP_CLASS_WIN__"] = conf.S_WIN_CLASS_FMT.format(
        name_sec_pascal
    )

    # app id for gui
    author = dict_prv_all["__PP_AUTHOR__"]
    dict_prv_prj["__PP_APP_ID__"] = conf.S_APP_ID_FMT.format(
        author, name_prj_small
    )

    # --------------------------------------------------------------------------
    # folders

    # path to the program's install dir (/home/user/.local/share/app_name)
    usr_inst = f"{conf.S_USR_SHARE}/{name_prj_small}"
    dict_prv_prj["__PP_USR_INST__"] = usr_inst

    # --------------------------------------------------------------------------
    # files

    # k/v to fix desktop
    name_prj_big = dict_prv_prj["__PP_NAME_PRJ_BIG__"]
    dict_prv_prj["__PP_FILE_DESK__"] = (
        f"{conf.S_DIR_SRC}/{conf.S_DIR_GUI}/{conf.S_DIR_DESKTOP}/{name_prj_big}.desktop"
    )

    # --------------------------------------------------------------------------
    # various image files
    img_name = conf.S_IMG_FMT.format(name_prj_small)

    dict_prv_prj["__PP_IMG_README__"] = f"{conf.S_DIR_IMAGES}/{img_name}"
    # NB: .desktop needs abs path to img
    dict_prv_prj["__PP_IMG_DESK__"] = (
        f"{usr_inst}/{conf.S_DIR_IMAGES}/{img_name}"
    )
    # NB: .ui files need rel path to img
    dict_prv_prj["__PP_IMG_DASH__"] = (
        f"{"../../.."}/{conf.S_DIR_IMAGES}/{img_name}"
    )
    dict_prv_prj["__PP_IMG_ABOUT__"] = (
        f"{"../../.."}/{conf.S_DIR_IMAGES}/{img_name}"
    )

    # --------------------------------------------------------------------------
    # version stuff

    # get base version
    ver_base = dict_pub_meta[conf.S_KEY_META_VERSION]
    dict_prv_prj["__PP_VER_MMR__"] = ver_base

    # set display of version
    ver_disp = conf.S_VER_DISP_FMT.format(ver_base)
    dict_prv_prj["__PP_VER_DISP__"] = ver_disp

    # format dist dir name with prj and ver
    ver_dist = conf.S_VER_DIST_FMT.format(name_prj_small, ver_base)
    dict_prv_prj["__PP_FMT_DIST__"] = ver_dist

    # --------------------------------------------------------------------------
    # develop.py stuff
    prj_type = dict_prv_prj["__PP_TYPE_PRJ__"]
    if prj_type in conf.L_INST_SELF:
        dict_prv_prj["__PP_DEV_INST__"] = (
            conf.S_CMD_VENV_INST_REQS + ";" + conf.S_CMD_VENV_INST_SELF
        )
    else:
        dict_prv_prj["__PP_DEV_INST__"] = conf.S_CMD_VENV_INST_REQS


# ------------------------------------------------------------------------------
# Do any work after fix
# ------------------------------------------------------------------------------
def do_after_fix(dict_act, dir_prj, dict_prv, dict_pub):
    """
    Do any work after fix

    Args:
        dict_act: The dictionary containing the current session's debug
        settings
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data

    Do any work after fix.\n
    This function is called by both PyMaker and PyBaker.\n
    This method is called just after _do_fix, after all files have been
    modified.\n
    It is mostly used to update metadata once all the normal fixes have been
    applied.
    """

    # get project type
    prj_type = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # i18n
    if prj_type in conf.L_MAKE_I18N:
        actions.action_run(
            # check for key presence or skip
            dict_act,
            conf.S_KEY_ACT_I18N,
            conf.S_ACTION_I18N,
            # run action and check for error
            actions.action_i18n,
            dir_prj,
            dict_prv,
            dict_pub,
        )

    # meta
    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_META,
        conf.S_ACTION_META,
        # run action and check for error
        actions.action_meta,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # add/remove placeholders
    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_PLACE,
        conf.S_ACTION_PLACE,
        # run action and check for error
        actions.action_placeholders,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # --------------------------------------------------------------------------
    # install package in itself

    # if it is the right type (package)
    if prj_type in conf.L_INST_SELF:
        actions.action_run(
            # check for key presence or skip
            dict_act,
            conf.S_KEY_ACT_EDIT,
            conf.S_ACTION_EDIT,
            # run action and check for error
            actions.action_edit,
            dir_prj,
            dict_prv,
            dict_pub,
        )

    # --------------------------------------------------------------------------
    # docs

    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_DOCS_MAKE,
        conf.S_ACTION_MAKE_DOCS,
        # run action and check for error
        actions.action_make_docs,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # --------------------------------------------------------------------------
    # tree
    # NB: run last so it includes .git and .venv folders
    # NB: this will wipe out all previous checks (maybe good?)

    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_TREE,
        conf.S_ACTION_TREE,
        # run action and check for error
        actions.action_tree,
        dir_prj,
        dict_prv,
        dict_pub,
    )


# ------------------------------------------------------------------------------
# Do any work before making dist
# ------------------------------------------------------------------------------
def do_before_dist(dict_act, dir_prj, dict_prv, dict_pub):
    """
    Do any work before making dist

    Args:
        dict_act: The dictionary containing the current session's debug
        settings
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data

    Do any work on the dist folder before it is created. This method is called
    after _do_after_fix, and before _do_dist.
    """

    # --------------------------------------------------------------------------
    # freeze venv

    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_FREEZE,
        conf.S_ACTION_FREEZE,
        # run action and check for error
        actions.action_freeze,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # --------------------------------------------------------------------------
    # docs bake

    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_DOCS_BAKE,
        conf.S_ACTION_BAKE_DOCS,
        # run action and check for error
        actions.action_bake_docs,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # --------------------------------------------------------------------------
    # docs deploy

    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_DOCS_DEPLOY,
        conf.S_ACTION_DEPLOY_DOCS,
        # run action and check for error
        actions.action_deploy_docs,
        dir_prj,
        dict_prv,
        dict_pub,
    )


# ------------------------------------------------------------------------------
# Do any work after making dist
# ------------------------------------------------------------------------------
def do_after_dist(
    dict_act,
    dir_prj,
    dict_prv,
    dict_pub,
):
    """
    Do any work after making dist

    Args:
        dict_act: The dictionary containing the current session's debug
        settings
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data

    Do any work on the dist folder after it is created. This method is called
    after _do_dist. Currently, this method purges any "ABOUT" file used as
    placeholders for github syncing. It also tars the source folder if it is a
    package, making for one (or two) less steps in the user's install process.
    """

    # get project type
    prj_type = dict_prv[conf.S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # get dist dir for all operations
    dist = Path(dir_prj) / conf.S_DIR_DIST
    name_fmt = str(dict_prv[conf.S_KEY_PRV_PRJ]["__PP_FMT_DIST__"])
    p_dist = dist / name_fmt

    # --------------------------------------------------------------------------
    # move some files around between end of dist and start of install

    if prj_type in conf.L_APP_INSTALL:
        # move install.py to above assets
        file_inst = (
            p_dist
            / conf.S_DIR_ASSETS
            / conf.S_DIR_INSTALL
            / conf.S_FILE_INST_PY
        )
        if file_inst.exists():
            shutil.move(file_inst, p_dist)

        # move uninstall.py to top of assets
        file_uninst = (
            p_dist
            / conf.S_DIR_ASSETS
            / conf.S_DIR_INSTALL
            / conf.S_FILE_UNINST_PY
        )
        if file_uninst.exists():
            dest = p_dist / conf.S_DIR_ASSETS
            shutil.move(file_uninst, dest)

    # --------------------------------------------------------------------------
    # remove extensions of some files

    # glob L_DIST_REMOVE_EXT
    list_del = []
    for item in conf.L_DIST_REMOVE_EXT:
        res = list(p_dist.glob(item))
        list_del.extend(res)

    # rename stuff
    for item in list_del:
        if item.is_file():
            item.rename(Path(item.parent, item.stem))

    # --------------------------------------------------------------------------
    # remove unnecessary files from dist

    lst_del = []
    for item in conf.L_PURGE_DIST:
        res = list(p_dist.glob(item))
        lst_del.extend(res)

    for item in lst_del:
        if item.is_dir():
            shutil.rmtree(item)
        elif item.is_file():
            item.unlink()

    # --------------------------------------------------------------------------
    # compress dist

    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_COMPRESS,
        conf.S_ACTION_COMPRESS,
        # run action and check for error
        actions.action_compress,
        dir_prj,
        dict_prv,
        dict_pub,
    )

    # --------------------------------------------------------------------------
    # docs bake

    actions.action_run(
        # check for key presence or skip
        dict_act,
        conf.S_KEY_ACT_REM_DIST,
        conf.S_ACTION_REM_DIST,
        # run action and check for error
        actions.action_rem_dist,
        dir_prj,
        dict_prv,
        dict_pub,
    )


# -)
