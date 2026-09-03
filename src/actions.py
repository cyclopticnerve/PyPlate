# ------------------------------------------------------------------------------
# Run an action
# ------------------------------------------------------------------------------
def _action_run(dict_act, key, msg, action_func, dir_prj, dict_prv, dict_pub):
    """
    Run an action

    Arguments:

    dict_act: the dict of acts and whether to perform them
    key: name of action i.e. S_KEY_ACT_VENV to make venv
    msg: what to print while doing the action, or when skipped

    action_func: the real function to be decorated

    dir_prj: project directory (arg to action_func)
    dict_prv: private.json (arg to action_func)
    dict_pub: project.json (arg to action_func)

    This is just a convenience method to handle skipping or handling an error.
    Skipping should be pretty self-explanatory. Handling an error in a step
    depends on the value of B_STOP_ON_ERROR. If True, the first error that
    occurs will stop the program. If False, the next steps will continue, and
    an error message will only be shown after all steps are completed.
    """

    # handle skip
    if not dict_act[key]:
        G.S.skip(msg)
        return

    # any action_func may throw an error, which will be returned by cnspinner.
    # to be clear, cnspinner handles printing the "fail" message (and possibly
    # printing the error message, if G.F.B_PP_DEBUG is True). the cnspinner function
    # will then return the error here, so we can set B_PP_RESULT.
    err = action_func(dir_prj, dict_prv, dict_pub)
    if err:
        # TODO: do we need this? (the global)
        # global G.B_PP_RESULT  # pylint:disable=global-statement
        G.B_PP_RESULT = False


# ------------------------------------------------------------------------------
# Make a venv in the project directory
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_VENV)
def _action_venv(dir_prj, dict_prv, _dict_pub):
    """
    Make a venv in the project directory

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        _dict_pub: The PyPlate public dict (not used)

    Returns:
        A tuple consisting of:
            bool: Whether the action passed or failed
            obj: An object returned from the function
    """

    # get name of venv folder and reqs file
    dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]

    # create a cnvenv object
    cv = G.CNVenv(dir_prj, dir_venv)

    # create venv
    cv.create()


# ------------------------------------------------------------------------------
# Install reqs in venv
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_REQS)
def _action_reqs(dir_prj, dict_prv, _dict_pub):
    """
    Install reqs in venv

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    Returns:
        A tuple consisting of:
            bool: Whether the action passed or failed
            obj: An object returned from the function
    """

    # get name of venv folder and reqs file
    dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]

    # create a cnvenv object
    cv = G.CNVenv(dir_prj, dir_venv)

    # get name of venv folder and reqs file
    file_reqs = dir_prj / S_FILE_REQS

    # install requirements
    cv.install_reqs(file_reqs)


# ------------------------------------------------------------------------------
# Make git repo for new project
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_GIT)
def _action_git(dir_prj, _dict_prv, _dict_pub):
    """
    Make git repo for new project

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    Returns:
        A tuple consisting of:
            bool: Whether the action passed or failed
            obj: An object returned from the function
    """

    # add git dir
    cmd = S_CMD_GIT_CREATE.format(dir_prj)
    G.F.run(cmd, shell=True, capture_output=True)


# ------------------------------------------------------------------------------
# Install lib in project
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_INST)
def _action_inst(dir_prj, dict_prv, dict_pub):
    """
    Install lib in project

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    Returns:
        A tuple consisting of:
            bool: Whether the action passed or failed
            obj: An object returned from the function
    """

    # make the project.json inst dict
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]
    dict_pub[S_KEY_PUB_INST] = dict(D_TYPE_INST[prj_type])

    # create a template and save cfg file
    dict_inst = dict_pub[S_KEY_PUB_INST]

    # dict_inst_cont = dict_inst[S_KEY_INST_CONT]
    path_inst = dir_prj / S_DIR_INSTALL / S_FILE_INST_CFG

    G.F.save_dict_into_paths(dict_inst, [path_inst])


# ------------------------------------------------------------------------------
# Purge some files
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_PURGE)
def _action_purge(dir_prj, dict_prv, _dict_pub):
    """
    Purge some files

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    Returns:
        A tuple consisting of:
            bool: Whether the action passed or failed
            obj: An object returned from the function
    """

    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]

    # get list of purges for this prj type
    lst_purge = D_PURGE_MAKE[prj_type]

    # make sure all paths are absolute
    lst_purge = [
        (
            G.Path(dir_prj) / item
            if not G.Path(item).is_absolute()
            else G.Path(item)
        )
        for item in lst_purge
    ]

    # nuke any files/folders
    for item in lst_purge:
        if item.exists():
            if item.is_dir():
                G.shutil.rmtree(item)
            elif item.is_file():
                item.unlink()


# ------------------------------------------------------------------------------
# Make i18n stuff
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_I18N)
def _action_i18n(dir_prj, dict_prv, dict_pub):
    """
    Make i18n stuff

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    Returns:
        A tuple consisting of:
            bool: Whether the action passed or failed
            obj: An object returned from the function
    """

    # --------------------------------------------------------------------------
    # do bulk of i18n

    # check if we want i18n
    prj_type = dict_prv[S_KEY_PRV_PRJ]["__PP_TYPE_PRJ__"]
    if prj_type in L_MAKE_I18N:

        # get settings from project.json
        dict_i18n = dict_pub[S_KEY_PUB_I18N]
        dict_prv_all = dict_prv[S_KEY_PRV_ALL]
        dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]

        # create CNPotPy object
        potpy = G.CNPotPy(
            dir_prj,  # base dir prj
            dir_prj / dict_i18n[S_KEY_PUB_I18N_DIR],  # out
            list_src=dict_i18n[S_KEY_PUB_I18N_SRC],  # in
            str_domain=dict_prv_prj["__PP_NAME_PRJ_SMALL__"],
            # str_domain=dict_i18n[S_KEY_PUB_I18N_DOM],
            str_version=dict_prv_prj["__PP_VER_MMR__"],
            # str_version=dict_i18n[S_KEY_PUB_I18N_VER],
            str_author=dict_prv_all["__PP_AUTHOR__"],
            # str_author=dict_i18n[S_KEY_PUB_I18N_AUTH],
            str_email=dict_prv_all["__PP_EMAIL__"],
            # str_email=dict_i18n[S_KEY_PUB_I18N_EMAIL],
            str_tag=dict_i18n[S_KEY_PUB_I18N_TAG],
            str_encoding=dict_i18n[S_KEY_PUB_I18N_CHAR],
            dict_clangs=dict_i18n[S_KEY_PUB_I18N_CLANGS],
        )

        # make .pot, .po, and .mo files
        potpy.main()

        # ----------------------------------------------------------------------
        # do .desktop i18n/version

        # path to desktop template
        path_desk_tmp = dir_prj / S_PATH_DSK_TMP
        # path to desktop output
        path_desk_out = dir_prj / dict_prv[S_KEY_PRV_PRJ]["__PP_FILE_DESK__"]

        # check for template.desktop (or rule out using dict)
        if path_desk_tmp.exists():

            # do the thing
            potpy.make_desktop(path_desk_tmp, path_desk_out)


# ------------------------------------------------------------------------------
# Fix metadata
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_META)
def _action_meta(dir_prj, dict_prv, dict_pub):
    """
    Fix metadata

    Args:
        dir_prj: The project directory
        dict_prv: The PyPlate private dict
        dict_pub: The PyPlate public dict

    """

    # --------------------------------------------------------------------------
    # fix version in po files
    # NB: this ignores blacklist

    # NB: root is a full path, dirs and files are relative to root
    # for root, root_dirs, root_files in dir_prj.walk():

    #     # special case for po/pot files

    #     # convert files into Paths
    #     files = [root / f for f in root_files]

    #     # for each file item
    #     for item in files:

    #         # if it is a .po or .pot file
    #         if item.suffix in L_EXT_PO:

    #             # fix it with appropriate dicts
    #             _fix_po(item, dir_prj, dict_prv, dict_pub)

    # --------------------------------------------------------------------------
    # filter using blacklist

    # NB: this is an example of how to use the blacklist filter in your own
    # customized fix routine

    # NB: this function uses the blacklist to filter files at the very end of
    # the fix process. At this point you can assume ALL dunders in ALL eligible
    # files have been fixed, as well as paths/filenames. also dict_pub has been
    # un-dunderized

    # fix up blacklist and convert relative or glob paths to absolute G.Path
    # objects
    dict_bl = dict(dict_pub[S_KEY_PUB_BL])

    # for each section of blacklist
    for key, val in dict_bl.items():

        # convert all items in list to G.Path objects
        list_res = []
        for item in val:
            res = list(dir_prj.glob(item))
            list_res.extend(res)

        # store in local bl
        dict_bl[key] = list_res

    # just shorten the names
    skip_all = dict_bl[S_KEY_SKIP_ALL]
    skip_contents = dict_bl[S_KEY_SKIP_CONTENTS]

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
                _fix_files(item, dict_prv, dict_pub)


# ------------------------------------------------------------------------------
# Fix placeholders
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_PLACE)
def _action_placeholders(dir_prj, _dict_prv, _dict_pub):

    # do not fuck with placeholders in these dirs
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


# ------------------------------------------------------------------------------
# Install package in itself
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_EDIT)
def _action_edit(dir_prj, dict_prv, _dict_pub):

    # get venv name
    dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]
    # install
    cmd = S_CMD_VENV_INST_SELF.format(dir_prj, dir_venv)
    G.F.run(cmd, shell=True, capture_output=True)


# ------------------------------------------------------------------------------
# Make docs folderS_ERR_NO_REPO
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_MAKE_DOCS)
def _action_make_docs(dir_prj, _dict_prv, dict_pub):

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

    # make docs
    mkdocs = G.CNMkDocs()
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


# -----------------------------------------------------------------------------
# Make tree files
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_TREE)
def _action_tree(dir_prj, _dict_prv, dict_pub):

    # get path to tree
    file_tree_text = dir_prj / S_TREE_TEXT_FILE
    file_tree_html = dir_prj / S_TREE_HTML_FILE

    file_tree_text.parent.mkdir(exist_ok=True)
    file_tree_html.parent.mkdir(exist_ok=True)

    # create the file so it includes itself
    with open(file_tree_text, "w", encoding=S_ENCODING) as a_file:
        a_file.write("")

    # create the file so it includes itself
    with open(file_tree_html, "w", encoding=S_ENCODING) as a_file:
        a_file.write("")

    # create tree object and call
    tree_obj = G.CNTree(
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


# ------------------------------------------------------------------------------
# Freeze venv dir
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_FREEZE)
def _action_freeze(dir_prj, dict_prv, _dict_pub):

    # get name ov venv folder and reqs file
    dir_venv = dict_prv[S_KEY_PRV_PRJ]["__PP_NAME_VENV__"]
    file_reqs = dir_prj / S_FILE_REQS

    # do the thing with the thing
    cv = G.CNVenv(dir_prj, dir_venv)
    cv.freeze(file_reqs)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_BAKE_DOCS)
def _action_bake_docs(dir_prj, _dict_prv, _dict_pub):

    # bake docs
    mkdocs = G.CNMkDocs()
    mkdocs.bake_docs(G.P_DIR_PP_VENV, dir_prj)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_DEPLOY_DOCS)
def _action_deploy_docs(dir_prj, _dict_prv, _dict_pub):

    # the command to deploy docs
    mkdocs = G.CNMkDocs()
    mkdocs.deploy_docs(G.P_DIR_PP_VENV, dir_prj)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_COMPRESS)
def _action_compress(dir_prj, dict_prv, _dict_pub):

    # get dist dir for all operations
    dist = G.Path(dir_prj) / S_DIR_DIST
    name_fmt = str(dict_prv[S_KEY_PRV_PRJ]["__PP_FMT_DIST__"])
    p_dist = dist / name_fmt

    # get out file (dist/prj-<version>.xxx) and in dir (dist/prj-<version>)
    path_out = path_in = str(p_dist)

    # make archive type
    G.shutil.make_archive(path_out, S_DIST_MODE, path_in)


# ------------------------------------------------------------------------------
#
# ------------------------------------------------------------------------------
@G.S.spin(S_ACTION_REM_DIST)
def _action_rem_dist(dir_prj, dict_prv, _dict_pub):

    # get dist dir for all operations
    dist = G.Path(dir_prj) / S_DIR_DIST
    name_fmt = str(dict_prv[S_KEY_PRV_PRJ]["__PP_FMT_DIST__"])
    p_dist = dist / name_fmt

    # delete folder
    G.shutil.rmtree(p_dist)
