from pathlib import Path
import sys
# ------------------------------------------------------------------------------
# local imports

import conf as C

# fudge the path to import pyplate stuff
P_DIR_PRJ = Path(__file__).parents[1].resolve()
sys.path.append(str(P_DIR_PRJ))

import src.pyplate_base as PP

# get version number from base
C.D_PRV_PRJ["__PP_VERSION_PP__"] = PP.PyPlateBase.S_PP_VERSION

# ------------------------------------------------------------------------------
# Public functions
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Do any work before template copy
# ------------------------------------------------------------------------------
def do_before_template(_dir_prj, _dict_prv, _dict_pub, _dict_dbg):
    """
    Do any work before template copy

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Do any work before copying the template. This method is called just before
    _do_template, before any files have been copied.\n
    It is mostly used to make final adjustments to the 'dict_prv' and
    'dict_pub' dicts before any copying occurs.
    """


# ------------------------------------------------------------------------------
# Do any work after template copy
# ------------------------------------------------------------------------------
def do_after_template(dir_prj, dict_prv, dict_pub, dict_dbg):
    """
    Do any work after template copy

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Raises:
        cnlib.cnfunctions.CNRunError if git create fails

    Do any work after copying the template. This function is called after
    _do_template, and before _do_before_fix.\n
    Use this function to create any files that your project needs to be created
    dynamically. You can also run code that is only called by PyMaker before
    fixing, like chopping the readme file sections.
    """

    # get project type
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # --------------------------------------------------------------------------
    # create venv

    # if venv flag is set
    if dict_dbg[S_KEY_DBG_VENV]:
        _res, cv = _action_venv(dir_prj, dict_prv)
        _action_reqs(dir_prj, cv)

    # --------------------------------------------------------------------------
    # git

    # if git flag
    if dict_dbg[S_KEY_DBG_GIT]:
        _action_git(dir_prj)

    # --------------------------------------------------------------------------
    # inst/uninst

    # make sure we use the right settings
    if prj_type in D_TYPE_INST:
        dict_pub[S_KEY_PUB_INST] = dict(D_TYPE_INST[prj_type])
        _action_inst(dir_prj, dict_pub)

    # --------------------------------------------------------------------------
    # purge package dirs

    if prj_type in D_PURGE:
        _action_purge(prj_type, dir_prj)


    # --------------------------------------------------------------------------
    # do i18n stuff

    if prj_type in D_TYPE_I18N:

        # get dst/src dict
        dict_dst = dict_pub[S_KEY_PUB_I18N]
        dict_src = D_TYPE_I18N[prj_type]

        # fix sources
        dict_dst[S_KEY_PUB_I18N_SRC] = list(dict_src[S_KEY_PUB_I18N_SRC])

    # --------------------------------------------------------------------------
    # set dist dict to default

    dict_pub[S_KEY_PUB_DIST] = dict(D_TYPE_DIST[prj_type])

    # --------------------------------------------------------------------------
    # set DOCS_DIR_API

    if prj_type in D_DOCS_DIR_API:
        dict_pub[S_KEY_PUB_DOCS][S_KEY_DOCS_DIR_API] = D_DOCS_DIR_API[prj_type]

# ------------------------------------------------------------------------------
# Do any work before fix
# ------------------------------------------------------------------------------
def do_before_fix(_dir_prj, dict_prv, dict_pub, _dict_dbg):
    """
    Do any work before fix

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
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
    dict_prv_all = dict_prv[S_KEY_PRV_ALL]
    dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]
    dict_pub_meta = dict_pub[S_KEY_PUB_META]

    # --------------------------------------------------------------------------
    # calculate current date
    # NB: this is the initial create date for all files in the template
    # new files added to the project will have their dates set to the date
    # when pybaker was last run

    # get current date and format it according to dev fmt
    now = datetime.now()
    fmt_date = S_DATE_FMT
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
    dict_prv_prj["__PP_FILE_APP__"] = S_APP_FILE_FMT.format(name_prj_small)
    dict_prv_prj["__PP_CLASS_APP__"] = S_APP_CLASS_FMT.format(name_prj_pascal)
    dict_prv_prj["__PP_FILE_WIN__"] = S_WIN_FILE_FMT.format(name_sec_small)
    dict_prv_prj["__PP_CLASS_WIN__"] = S_WIN_CLASS_FMT.format(name_sec_pascal)

    # app id for gui
    author = dict_prv_all["__PP_AUTHOR__"]
    dict_prv_prj["__PP_APP_ID__"] = S_APP_ID_FMT.format(author, name_prj_small)

    # --------------------------------------------------------------------------
    # folders

    # path to the program's install dir (/home/user/.local/share/app_name)
    usr_inst = f"{S_USR_SHARE}/{name_prj_small}"
    dict_prv_prj["__PP_USR_INST__"] = usr_inst

    # --------------------------------------------------------------------------
    # files

    # k/v to fix desktop
    name_prj_big = dict_prv_prj["__PP_NAME_PRJ_BIG__"]
    dict_prv_prj["__PP_FILE_DESK__"] = (
        f"{S_DIR_SRC}/{S_DIR_GUI}/{S_DIR_DESKTOP}/{name_prj_big}.desktop"
    )

    # --------------------------------------------------------------------------
    # various image files
    img_name = S_IMG_FMT.format(name_prj_small)

    dict_prv_prj["__PP_IMG_README__"] = f"{S_DIR_IMAGES}/{img_name}"
    # NB: .desktop needs abs path to img
    dict_prv_prj["__PP_IMG_DESK__"] = f"{usr_inst}/{S_DIR_IMAGES}/{img_name}"
    # NB: .ui files need rel path to img
    dict_prv_prj["__PP_IMG_DASH__"] = f"{"../../.."}/{S_DIR_IMAGES}/{img_name}"
    dict_prv_prj["__PP_IMG_ABOUT__"] = (
        f"{"../../.."}/{S_DIR_IMAGES}/{img_name}"
    )

    # --------------------------------------------------------------------------
    # version stuff

    # get base version
    ver_base = dict_pub_meta[S_KEY_META_VERSION]
    dict_prv_prj["__PP_VER_MMR__"] = ver_base

    # set display of version
    ver_disp = S_VER_DISP_FMT.format(ver_base)
    dict_prv_prj["__PP_VER_DISP__"] = ver_disp

    # format dist dir name with prj and ver
    ver_dist = S_VER_DIST_FMT.format(name_prj_small, ver_base)
    dict_prv_prj["__PP_FMT_DIST__"] = ver_dist

    # --------------------------------------------------------------------------
    # develop.py stuff
    prj_type = dict_prv_prj["__PP_TYPE_PRJ__"]
    if prj_type in L_INST_SELF:
        dict_prv_prj["__PP_DEV_INST__"] = S_CMD_VENV_INST_SELF
    else:
        dict_prv_prj["__PP_DEV_INST__"] = S_CMD_VENV_INST_REQS


# ------------------------------------------------------------------------------
# Do any work after fix
# ------------------------------------------------------------------------------
def do_after_fix(dir_prj, dict_prv, dict_pub, dict_dbg):
    """
    Do any work after fix

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings
        pymaker: True if called by PyMaker, False if called by PyBaker

    Do any work after fix.\n
    This function is called by both PyMaker and PyBaker.\n
    This method is called just after _do_fix, after all files have been
    modified.\n
    It is mostly used to update metadata once all the normal fixes have been
    applied.
    """

    # get project type
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # i18n
    # NB: needs to be callable from pybaker for -l option
    # if i18n flag is set
    if dict_dbg[S_KEY_DBG_I18N]:
        _action_i18n(dir_prj, dict_prv, dict_pub)

    # meta
    _action_meta(dir_prj, dict_prv, dict_pub)

    # add/remove placeholders
    _action_placeholders(dir_prj)

    # --------------------------------------------------------------------------
    # install package in itself
    # if venv flag is set and it is the right type (package)
    if dict_dbg[S_KEY_DBG_VENV] and prj_type in L_INST_SELF:
        _action_edit(dir_prj, dict_prv)


    # --------------------------------------------------------------------------
    # docs

    # if docs flag is set
    if dict_dbg[S_KEY_DBG_DOCS]:
        _action_docs(dir_prj, dict_pub)

    # --------------------------------------------------------------------------
    # tree
    # NB: run last so it includes .git and .venv folders
    # NB: this will wipe out all previous checks (maybe good?)

    # if tree flag is set
    if dict_dbg[S_KEY_DBG_TREE]:
        _action_tree(dir_prj, dict_pub)

# ------------------------------------------------------------------------------
# Do any work before making dist
# ------------------------------------------------------------------------------
def do_before_dist(dir_prj, dict_prv, _dict_pub, dict_dbg):
    """
    Do any work before making dist

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Do any work on the dist folder before it is created. This method is called
    after _do_after_fix, and before _do_dist.
    """

    # --------------------------------------------------------------------------
    # freeze venv

    # if venv flag is set
    if dict_dbg[S_KEY_DBG_VENV]:

        prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

        if prj_type in L_APP_INSTALL:
            # print info
            print(S_ACTION_FREEZE, end="", flush=True)

            # get name ov venv folder and reqs file
            dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]
            file_reqs = dir_prj / S_FILE_REQS

            # do the thing with the thing
            cv = CNVenv(dir_prj, dir_venv)
            try:
                cv.freeze(file_reqs)
                F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
            except F.CNRunError as e:
                # exit gracefully
                F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
                F.printd(S_ERR_ERR, str(e))

    # --------------------------------------------------------------------------
    # docs

    # if docs flag is set
    if dict_dbg[S_KEY_DBG_DOCS]:

        # "I expect the BEST!" - Debbie Hunt
        deploy = True

        # ----------------------------------------------------------------------

        # print info
        print(S_ACTION_BAKE_DOCS, end="", flush=True)

        # get docs object
        cm = CNMkDocs()

        # the command to make or bake docs
        try:
            cm.build_docs(P_DIR_PP_VENV, dir_prj)
            F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
        except F.CNRunError as e:
            deploy = False
            # fail gracefully
            F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
            F.printd(S_ERR_ERR, str(e))

        # ----------------------------------------------------------------------

        if deploy:

            # print info
            print(S_ACTION_DEPLOY_DOCS, end="", flush=True)

            # the command to make or bake docs
            try:
                cm.deploy_docs(P_DIR_PP_VENV, dir_prj)
                F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
            except F.CNRunError as e:
                # fail gracefully
                F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
                F.printc(
                    S_ERR_NO_REPO, fg=F.C_FG_WHITE, bg=F.C_BG_RED, bold=True
                )
                F.printd(S_ERR_ERR, str(e))


# ------------------------------------------------------------------------------
# Do any work after making dist
# ------------------------------------------------------------------------------
def do_after_dist(dir_prj, dict_prv, _dict_pub, dict_dbg):
    """
    Do any work after making dist

    Args:
        dir_prj: The root of the new project
        dict_prv: The dictionary containing private pyplate data
        dict_pub: The dictionary containing public project data
        dict_dbg: The dictionary containing the current session's debug
        settings

    Do any work on the dist folder after it is created. This method is called
    after _do_dist. Currently, this method purges any "ABOUT" file used as
    placeholders for github syncing. It also tars the source folder if it is a
    package, making for one (or two) less steps in the user's install process.
    """

    # get project type
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # get dist dir for all operations
    dist = Path(dir_prj) / S_DIR_DIST
    name_fmt = str(dict_prv[S_KEY_PRV_PRJ]["__PP_FMT_DIST__"])
    p_dist = dist / name_fmt

    # --------------------------------------------------------------------------
    # move some files around between end of dist and start of install

    if prj_type in L_APP_INSTALL:
        # move install.py to above assets
        file_inst = p_dist / S_DIR_ASSETS / S_DIR_INSTALL / S_FILE_INST_PY
        if file_inst.exists():
            shutil.move(file_inst, p_dist)

        # move uninstall.py to top of assets
        file_uninst = p_dist / S_DIR_ASSETS / S_DIR_INSTALL / S_FILE_UNINST_PY
        if file_uninst.exists():
            dest = p_dist / S_DIR_ASSETS
            shutil.move(file_uninst, dest)

    # --------------------------------------------------------------------------
    # remove extensions of some files

    # glob L_DIST_REMOVE_EXT
    list_del = []
    for item in L_DIST_REMOVE_EXT:
        res = list(p_dist.glob(item))
        list_del.extend(res)

    # rename stuff
    for item in list_del:
        if item.is_file():
            item.rename(Path(item.parent, item.stem))

    # --------------------------------------------------------------------------
    # remove unnecessary files from dist

    lst_del = []
    for item in L_PURGE_FILES:
        res = list(p_dist.glob(item))
        lst_del.extend(res)

    for item in lst_del:
        if item.is_dir():
            shutil.rmtree(item)
        elif item.is_file():
            item.unlink()

    # --------------------------------------------------------------------------
    # compress dist

    # print info
    print(S_ACTION_COMPRESS, end="", flush=True)

    # get out file (dist/prj-<version>.xxx) and in dir (dist/prj-<version>)
    path_out = path_in = str(p_dist)

    # make archive type(s)
    # shutil.make_archive(path_out, "gztar", path_in)
    shutil.make_archive(path_out, "zip", path_in)

    # print info
    F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)

    # --------------------------------------------------------------------------
    # delete the origin dir, if key set

    # if debug key set
    if dict_dbg[S_KEY_DBG_DIST]:

        # print info
        print(S_ACTION_REM_DIST, end="", flush=True)

        # get dist dir for all operations
        dist = Path(dir_prj) / S_DIR_DIST
        name_fmt = dict_prv[S_KEY_PRV_PRJ]["__PP_FMT_DIST__"]
        p_dist = dist / name_fmt

        # delete folder
        shutil.rmtree(p_dist)

        # show info
        F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)


# ------------------------------------------------------------------------------
# Private functions
# ------------------------------------------------------------------------------


# FIXME: clean up
@S.spin(S_ACTION_VENV)
def _action_venv(dir_prj, dict_prv):
    # print info
    # print(S_ACTION_VENV, end="", flush=True)

    # get name ov venv folder and reqs file
    dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]

    # create a cnvenv object
    cv = CNVenv(dir_prj, dir_venv)

    # create venv
    try:
        cv.create()
        # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
        return (True, cv)
    except F.CNRunError as e:
        # exit gracefully
        return (False, e)
        # F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
        # F.printd(S_ERR_ERR, str(e))


@S.spin(S_ACTION_REQS)
def _action_reqs(dir_prj, cv):
    # print info
    # print(S_ACTION_REQS, end="", flush=True)

    # get name of venv folder and reqs file
    file_reqs = dir_prj / S_FILE_REQS

    # install requirements
    try:
        cv.install_reqs(file_reqs)
        # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
        return (True, None)
    except F.CNRunError as e:
        # exit gracefully
        # F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
        # F.printd(S_ERR_ERR, str(e))
        return (False, e)
        # sys.exit(-1)


@S.spin(S_ACTION_GIT)
def _action_git(dir_prj):
    # show info
    # print(S_ACTION_GIT, end="", flush=True)

    # add git dir
    cmd = S_CMD_GIT_CREATE.format(dir_prj)
    try:
        F.run(cmd, shell=True)
        # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
        return (True, None)
    except F.CNRunError as e:
        # exit gracefully
        # F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
        # F.printd(S_ERR_ERR, str(e))
        # sys.exit(-1)
        return (False, e)

@S.spin(S_ACTION_INST)
def _action_inst(dir_prj, dict_pub):

    # show info
    # print(S_ACTION_INST, end="", flush=True)

    # create a template and save cfg file
    dict_inst = dict_pub[S_KEY_PUB_INST]

    # dict_inst_cont = dict_inst[S_KEY_INST_CONT]
    path_inst = dir_prj / S_DIR_INSTALL / S_FILE_INST_CFG

    # # create a template uninstall cfg file
    # dict_uninst_cont = dict_inst[S_KEY_UNINST_CONT]
    # path_uninst = dir_prj / S_DIR_INSTALL / S_FILE_UNINST_CFG

    try:
        F.save_dict_into_paths(dict_inst, [path_inst])
        # F.save_dict_into_paths(dict_inst, [path_uninst])

        # show info
        return (True, None)
        # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)

    except OSError as e:  # from save_dict
        # F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
        # F.printd(S_ERR_ERR, str(e))
        return (False, e)


@S.spin(S_ACTION_PURGE)
def _action_purge(prj_type, dir_prj):
    # print(S_ACTION_PURGE, end="", flush=True)

    lst_purge = D_PURGE[prj_type]
    lst_purge = [
        (
            Path(dir_prj) / item
            if not Path(item).is_absolute()
            else Path(item)
        )
        for item in lst_purge
    ]
    for item in lst_purge:
        if item.exists():
            if item.is_dir():
                shutil.rmtree(item)
            elif item.is_file():
                item.unlink()

    # print done
    # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
    return (True, None)

@S.spin(S_ACTION_I18N)
def _action_i18n(dir_prj, dict_prv, dict_pub):
    # print info
    # print(S_ACTION_I18N, end="", flush=True)

    # --------------------------------------------------------------------------
    # do bulk of i18n

    # create CNPotPy object
    potpy = CNPotPy(
        # header
        str_domain=dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_PRJ_SMALL__"],
        str_version=dict_prv[S_KEY_PRV_PRJ]["__PP_VER_MMR__"],
        str_author=dict_prv[S_KEY_PRV_ALL]["__PP_AUTHOR__"],
        str_email=dict_prv[S_KEY_PRV_ALL]["__PP_EMAIL__"],
        # base prj dir
        dir_prj=dir_prj,
        # in
        list_src=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_SRC],
        # out
        dir_pot=S_PATH_POT,
        dir_po=S_PATH_PO,
        dir_locale=S_PATH_LOCALE,
        # optional in
        str_tag=S_I18N_TAG,
        dict_clangs=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_CLANGS],
        list_wlangs=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_WLANGS],
        charset=dict_pub[S_KEY_PUB_I18N][S_KEY_PUB_I18N_CHAR],
    )

    # make .pot, .po, and .mo files
    try:
        potpy.main()
        # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
    except F.CNRunError as e:
        # fail gracefully
        # F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
        # F.printd(S_ERR_ERR, str(e))
        return (False, e)

    # ----------------------------------------------------------------------
    # do .desktop i18n/version

    # check if we want template
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]
    if prj_type in L_MAKE_DESK:

        # path to desktop template
        path_dsk_tmp = dir_prj / S_PATH_DSK_TMP
        # path to desktop output
        path_dsk_out = (
            dir_prj / dict_prv[S_KEY_PRV_PRJ]["__PP_FILE_DESK__"]
        )

        # do the thing
        try:
            potpy.make_desktop(path_dsk_tmp, path_dsk_out)
        except F.CNRunError as e:
            # fail gracefully
            # F.printd(S_ERR_ERR, str(e))
            return (False, e)

    return (True, None)

@S.spin(S_ACTION_META)
def _action_meta(dir_prj, dict_prv, dict_pub):

    # --------------------------------------------------------------------------
    # filter using blacklist

    # NB: this is an example of how to use the blacklist filter in your own
    # customized fix routine

    # print info
    # print(S_ACTION_META, end="", flush=True)

    # NB: this function uses the blacklist to filter files at the very end of
    # the fix process. At this point you can assume ALL dunders in ALL eligible
    # files have been fixed, as well as paths/filenames. also dict_pub has been
    # undunderized

    # fix up blacklist and convert relative or glob paths to absolute Path
    # objects

    dict_bl = dict(dict_pub[S_KEY_PUB_BL])

    # for each section of blacklist
    for key, val in dict_bl.items():

        # convert all items in list to Path objects
        list_res = []
        for item in val:
            res = list(dir_prj.glob(item))
            list_res.extend(res)

        dict_bl[key] = list_res

    # just shorten the names
    skip_all = dict_bl[S_KEY_SKIP_ALL]
    skip_contents = dict_bl[S_KEY_SKIP_CONTENTS]

    # --------------------------------------------------------------------------
    # fix meta

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
            if item.suffix in L_EXT_PO:
                _fix_po(item, dict_prv[S_KEY_PRV_PRJ], dict_pub)
                continue

            # handle files in skip_all
            if item in skip_all:
                continue

            # handle dirs/files in skip_contents
            if not root in skip_contents and not item in skip_contents:
                # fix content with appropriate dict
                _fix_files(item, dict_prv, dict_pub)


    # print done
    # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
    return (True, None)

@S.spin(S_ACTION_PLACE)
def _action_placeholders(dir_prj):

    # print info
    # print(S_ACTION_PLACE, end="", flush=True)

    list_skip = []
    for item in L_PH_SKIP:
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
            with open(root / S_PH_NAME, "w", encoding=S_ENCODING) as a_file:
                a_file.write(S_PH_TEXT)

        # if dir has files/folders and placeholder
        if len(root_dirs) > 0 or len(root_files) > 1:
            for a_file in root_files:
                if a_file == S_PH_NAME:
                    a_path = root / a_file
                    a_path.unlink()

    # print info
    # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
    return (True, None)

@S.spin(S_ACTION_EDIT)
def _action_edit(dir_prj, dict_prv):

    # print(S_ACTION_EDIT, end="", flush=True)

    # get venv name
    dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]

    # install
    try:
        F.run(
            S_CMD_VENV_INST_SELF.format(dir_prj, dir_venv),
            shell=True,
            capture_output=True,
        )
        # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
        return (True, None)
    except F.CNRunError as e:
        return (False, e)
        # F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
        # F.printd(S_ERR_ERR, str(e))

@S.spin(S_ACTION_MAKE_DOCS)
def _action_docs(dir_prj, dict_pub):

    # print info
    # print(S_ACTION_MAKE_DOCS, end="", flush=True)

    # get some props
    dict_docs = dict_pub[S_KEY_PUB_DOCS]
    use_rm = dict_docs[S_KEY_DOCS_USE_RM]
    use_api = dict_docs[S_KEY_DOCS_MAKE_API]
    lst_api_in = dict_docs[S_KEY_DOCS_DIR_API]

    # check if first run
    index_path = dir_prj / S_DIR_DOCS / S_FILE_INDEX
    exist = index_path.exists()

    # if use_rm = true, use rm on every run
    # if use_rm = false, use rm only only on first run
    if use_rm or not exist:
        use_rm = True

    # the command to make docs
    try:

        # make docs
        mkdocs = CNMkDocs()
        mkdocs.make_docs(
            dir_prj,
            S_DIR_DOCS,
            use_rm,
            use_api,
            lst_api_in,
            S_FILE_README,
            S_DIR_API,
            S_DIR_IMAGES,
        )

        # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
        return (True, None)
    except F.CNRunError as e:
        # fail gracefully
        # F.printc(S_ACTION_FAIL, fg=F.C_FG_RED, bold=True)
        # F.printd(S_ERR_ERR, str(e))
        return (False, e)

@S.spin(S_ACTION_TREE)
def _action_tree(dir_prj, dict_pub):

    # print info
    # print(S_ACTION_TREE, end="", flush=True)

    # get path to tree
    file_tree_text = dir_prj / S_TREE_TEXT_FILE
    file_tree_html = dir_prj / S_TREE_HTML_FILE

    # create the file so it includes itself
    with open(file_tree_text, "w", encoding=S_ENCODING) as a_file:
        a_file.write("")

    # create the file so it includes itself
    with open(file_tree_html, "w", encoding=S_ENCODING) as a_file:
        a_file.write("")

    # create tree object and call
    tree_obj = CNTree(
        str(dir_prj),
        filter_list=dict_pub[S_KEY_PUB_BL][S_KEY_SKIP_TREE],
        dir_format=S_TREE_DIR_FORMAT,
        file_format=S_TREE_FILE_FORMAT,
        ignore_case=False,
    )
    tree_obj.make_tree()

    # write to file
    with open(file_tree_text, "w", encoding=S_ENCODING) as a_file:
        a_file.write(tree_obj.text)
    with open(file_tree_html, "w", encoding=S_ENCODING) as a_file:
        a_file.write(tree_obj.html)

    # ----------------------------------------------------------------------
    # we are done
    # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)
    return (True, None)


# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------

def _fix_po(path, dict_prv_prj, _dict_pub):

    # ----------------------------------------------------------------------
    # fix po files outside blacklist to hide file paths

    # print info
    # print(S_ACTION_PO, end="", flush=True)

    # replace version
    pp_version = dict_prv_prj["__PP_VER_MMR__"]
    str_pattern = S_PO_VER_SCH
    str_rep = S_PO_VER_REP.format(pp_version)

    # # get po/pot exts
    # l_ext =
    # list_files = []
    # for item in l_ext:
    #     res = list(dir_prj.glob(item))
    #     list_files.extend(res)

    # # for each file
    # for item in list_files:

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # delete path from .pot/.po files (in case of debug)
    # NB: also no regex or rules, just nuke it everywhere
    text = text.replace(str(Path.home()), "")

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)

    # print done
    # F.printc(S_ACTION_DONE, fg=F.C_FG_GREEN, bold=True)

# ------------------------------------------------------------------------------
# Fix stuff in individual files
# ------------------------------------------------------------------------------
def _fix_files(path, dict_prv, dict_pub):
    """
    Fix stuff in individual files

    Args:
        path: Path object for file to be fixed
        dict_prv_prj: Private project dict
        dict_pub_prj: Public project dict

    Fixes stuff in individual files. Note that this function is only called
    for files that make it through the BL filter. Switches are your problem.
    """

    # get sub-dicts we need
    dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]
    dict_pub_meta = dict_pub[S_KEY_PUB_META]

    # fix readme
    if path.name == S_FILE_README:
        _fix_readme(path, dict_prv_prj, dict_pub_meta)

    # fix pyproject
    if path.name == S_FILE_TOML:
        _fix_pyproject(path, dict_prv_prj, dict_pub_meta)

    # fix desktop
    if path.suffix in L_EXT_DESK:
        _fix_desktop(path, dict_prv_prj, dict_pub_meta)

    # fix ui files
    if path in L_EXT_GUI:
        _fix_ui(path, dict_prv_prj, dict_pub_meta)

    # fix src files
    if path.suffix in L_EXT_PY:
        _fix_src(path, dict_prv_prj, dict_pub_meta)

    # fix install.json
    if path.name == S_FILE_INST_CFG:
        _fix_install(path, dict_prv_prj, dict_pub_meta)

    # fix mkdocs.yml
    if path.name == S_FILE_MKDOCS_YML:
        _fix_mkdocs(path, dict_prv_prj, dict_pub)

# ------------------------------------------------------------------------------
# Remove/replace parts of the main README file
# ------------------------------------------------------------------------------
def _fix_readme(path, dict_prv_prj, dict_pub_meta):
    """
    Remove/replace parts of the main README file

    Args:
        path: Path for the README to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Removes parts of the file not applicable to the current project type. Also
    fixes metadata in the file when dict_meta is present.
    """

    # print(S_ACTION_README, end="", flush=True)

    # --------------------------------------------------------------------------
    # readme chop section

    # the whole text of the file
    text = ""

    # open and read whole file
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # find the remove blocks (opposite of prj type)
    prj_type = dict_prv_prj["__PP_TYPE_PRJ__"]
    if prj_type in L_APP_INSTALL:
        str_pattern = S_RM_PKG
    else:
        str_pattern = S_RM_APP

    # replace block with empty string (equiv to deleting it)
    # NB: need S flag to make dot match newline
    text = re.sub(str_pattern, "", text, flags=re.S)

    # ------------------------------------------------------------------------------

    # replace short description
    str_pattern = S_RM_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_RM_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # replace version
    str_pattern = S_RM_VER_SCH
    pp_ver_disp = dict_prv_prj["__PP_VER_DISP__"]
    str_rep = S_RM_VER_REP.format(pp_ver_disp)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # --------------------------------------------------------------------------

    # not technically metadata, but other stuff we gotta fix anyway

    # fix readme screenshot

    # get project type
    prj_type = dict_prv_prj["__PP_TYPE_PRJ__"]

    # should we futz with the readme?
    if prj_type in L_SCREENSHOT:

        # format the alt text
        s_alt = S_ERR_NO_SCREENSHOT.format(S_PATH_SCREENSHOT)
        s_img = S_RM_SCREENSHOT.format(s_alt, S_PATH_SCREENSHOT)

        # replace screenshot
        str_pattern = S_RM_SS_SCH
        str_rep = S_RM_SS_REP.format(s_img)
        text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # --------------------------------------------------------------------------
    # fix deps in readme

    # get deps as links
    d_py_deps = dict_pub_meta[S_KEY_META_DEPS]
    l_rm_deps = [
        f"[{key}]({val})" if val != "" else key
        for key, val in d_py_deps.items()
    ]

    # make a pretty string
    s_rm_deps = "<br>\n".join(l_rm_deps)
    if len(s_rm_deps) == 0:
        s_rm_deps = S_DEPS_NONE

    # replace dependencies array
    str_pattern = S_RM_DEPS_SCH
    str_rep = S_RM_DEPS_REP.format(s_rm_deps)
    text = re.sub(str_pattern, str_rep, text, flags=re.S)

    # --------------------------------------------------------------------------

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)

# ------------------------------------------------------------------------------
# Replace text in the pyproject file
# ------------------------------------------------------------------------------
def _fix_pyproject(path: Path, dict_prv_prj, dict_pub_meta):
    """
    Replace text in the pyproject file

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: the dict of metadata to replace in the file

    Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # convert long ver to mmr
    str_pattern = S_SEM_VER_VALID
    str_rep = dict_prv_prj["__PP_VER_MMR__"]
    str_rep = re.sub(str_pattern, S_SEM_VER_PYPRJ, str_rep)

    # --------------------------------------------------------------------------

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = S_TOML_VER_SCH
    str_rep = S_TOML_VER_REP.format(str_rep)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = S_TOML_DESC_SCH
    str_rep = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_TOML_DESC_REP.format(str_rep)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # fix keywords for pyproject.toml
    l_keywords = dict_pub_meta[S_KEY_META_KEYWORDS]
    q_keywords = [f'"{item}"' for item in l_keywords]
    s_keywords = ", ".join(q_keywords)

    # replace keywords array
    str_pattern = S_TOML_KW_SCH
    str_rep = S_TOML_KW_REP.format(s_keywords)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # --------------------------------------------------------------------------
    # fix packages list

    # get src or pkg name as start_dir
    prj_type = dict_prv_prj["__PP_TYPE_PRJ__"]
    prj_name = dict_prv_prj["__PP_NAME_PRJ_SMALL__"]
    start_dir = ""

    # use appropriate start dir
    if prj_type in L_TOML_USE_SRC:
        start_dir = S_DIR_SRC
    else:
        start_dir = prj_name

    # get full start path
    path_src = path.parent.resolve()
    path_src = path_src / start_dir

    # init list
    pkgs = [start_dir]
    path_prj = path_src.parent.resolve()

    # walk all subdirs of 'path_src'
    for parent_dir, child_dirs, _child_files in path_src.walk():

        # only care about dirs
        for child_dir in child_dirs:

            # get full path, then relative to project path to get relative path
            abs_path = parent_dir / child_dir
            rel_path = abs_path.relative_to(path_prj)

            # swap characters
            str_rel_path = str(rel_path).replace("/", ".")

            # add to list
            pkgs.append(str_rel_path)

    # format list
    pkgs = [f'"{item}"' for item in pkgs]
    s_pkgs = ", ".join(pkgs)
    s_pkgs = f"[{s_pkgs}]"

    # replace package list
    str_pattern = S_TOML_PKGS_SCH
    str_rep = S_TOML_PKGS_REP.format(s_pkgs)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # --------------------------------------------------------------------------

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the desktop file
# ------------------------------------------------------------------------------
def _fix_desktop(path, _dict_prv_prj, dict_pub_meta):
    """
    Replace text in the desktop file

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: the dict of metadata to replace in the file

    Replaces the description (comment) and category text in a .desktop file for
    programs that use this.
    """

    # the result cat list
    new_cats = []

    # check cats now
    cats = dict_pub_meta[S_KEY_META_CATS]
    for cat in cats:
        # category is not valid
        if not cat in L_CATS:
            # category is not valid, print error
            print("\n", path, ":")
            print(S_ERR_DESK_CAT.format(cat))
        else:
            new_cats.append(cat)

    # convert list to string
    str_cat = "".join(new_cats)

    # --------------------------------------------------------------------------

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace categories
    str_pattern = S_DESK_CAT_SCH
    str_rep = S_DESK_CAT_REP.format(str_cat)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description (comment)
    str_pattern = S_DESK_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_DESK_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the UI files
# ------------------------------------------------------------------------------
def _fix_ui(path, dict_prv_prj, dict_pub_meta):
    """
    Replace text in the UI files

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: the dict of metadata to replace in the file

    Replace description and version number in the UI file.
    """

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = S_UI_VER_SCH
    pp_version = dict_prv_prj["__PP_VER_MMR__"]
    str_rep = S_UI_VER_REP.format(pp_version)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # replace short description
    str_pattern = S_UI_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_UI_DESC_REP.format(pp_short_desc)
    text = re.sub(str_pattern, str_rep, text, flags=re.M | re.S)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Fix the version number and short description in source files
# ------------------------------------------------------------------------------
def _fix_src(path, dict_prv_prj, dict_pub_meta):
    """
    Fix the version number and short description in source files

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Returns:
        The new line of code

    Fixes the version number and short description in any file whose extension
    is in L_EXT_PY.
    """

    # the switch statuses
    # NB: this is an example of using switches to control line replacement
    dict_sw_block = dict(D_SWITCH_DEF)
    dict_sw_line = dict(D_SWITCH_DEF)

    # do md/html/xml separately (needs special handling)
    dict_type_rules = PP.get_type_rules(path)

    # the whole text of the file
    lines = []

    # open and read whole file
    with open(path, "r", encoding=S_ENCODING) as a_file:
        lines = a_file.readlines()

    # for each line in array
    for index, line in enumerate(lines):

        # ------------------------------------------------------------------
        # skip blank lines
        if line.strip() == "":
            continue

        # ------------------------------------------------------------------
        # split the line into code and comm

        # we will split the line into two parts
        # NB: assume code is whole line (i.e. no trailing comment)
        split_pos = 0
        code = line
        comm = ""

        # find split sequence
        split_sch = dict_type_rules[S_KEY_SPLIT]
        split_grp = dict_type_rules[S_KEY_SPLIT_COMM]

        # there may be multiple matches per line (ignore quoted markers)
        matches = re.finditer(split_sch, line)

        # only use matches that have the right group
        matches = [match for match in matches if match.group(split_grp)]
        for match in matches:

            # split the line into code and comment (including delimiter)
            split_pos = match.start(split_grp)
            code = line[:split_pos]
            comm = line[split_pos:]

        # ------------------------------------------------------------------
        # check for switches

        # reset line switch values to block switch values
        dict_sw_line = dict(dict_sw_block)

        # check switches
        PP.check_switches(
            code,
            comm,
            dict_type_rules,
            dict_sw_block,
            dict_sw_line,
        )

        # check for block or line replace switch
        repl = False
        if (
            dict_sw_block[S_SW_REPLACE] is True
            and dict_sw_line[S_SW_REPLACE] is True
        ) or dict_sw_line[S_SW_REPLACE] is True:
            repl = True

        # switch says no, gtfo
        if not repl:
            continue

        # ----------------------------------------------------------------------

        # replace version in line
        str_ver = dict_prv_prj["__PP_VER_DISP__"]
        str_sch = S_SRC_VER_SCH
        str_rep = S_SRC_VER_REP.format(str_ver)
        line = re.sub(str_sch, str_rep, line)

        # replace line in lines
        lines[index] = line

    # save lines back to file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.writelines(lines)

    # --------------------------------------------------------------------------
    # S_PP_SHORT_DESC needs special handling for _() and () if Black wraps it
    # FIXME: does not respect current state of replace flag b/c multiline

    # open and read whole file
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

        # replace short desc in multi line
        str_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
        str_sch = S_SRC_DESC_SCH
        str_rep = S_SRC_DESC_REP.format(str_desc)
        text = re.sub(str_sch, str_rep, text, flags=re.S)

    # save lines back to file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Fix version number in install.json
# ------------------------------------------------------------------------------
def _fix_install(path, dict_prv_prj, _dict_pub_meta):
    """
    Fix version number in install.json

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Fixes the version number in install.json.
    """

    # open file and get contents
    a_dict = F.load_paths_into_dict(path)

    # replace version
    ver = dict_prv_prj["__PP_VER_MMR__"]
    a_dict[S_KEY_INST_VER] = ver

    # save file
    F.save_dict_into_paths(a_dict, path)


# ------------------------------------------------------------------------------
# Fix the theme name in mkdocs.yml
# ------------------------------------------------------------------------------
def _fix_mkdocs(path, _dict_prv_prj, dict_pub):
    """
    Fix the theme name in mkdocs.yml

    Args:
        path: Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Fixes the theme name in mkdocs.yml.
    """

    dict_pub_docs = dict_pub[S_KEY_PUB_DOCS]
    theme = dict_pub_docs[S_KEY_DOCS_THEME]

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace theme
    str_pattern = S_THEME_SCH
    str_rep = S_THEME_REP.format(theme)
    text = re.sub(str_pattern, str_rep, text)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)
