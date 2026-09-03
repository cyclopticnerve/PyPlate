

# ------------------------------------------------------------------------------
# Fix po files outside blacklist to hide file paths
# ------------------------------------------------------------------------------
# def fix_po(path, _dir_prj, dict_prv, _dict_pub):

# #     # replace version
# #     # NB: done in cnpot
# #     # dict_prv_prj = dict_prv[S_KEY_PRV_PRJ]
# #     # pp_version = dict_prv_prj["__PP_VER_MMR__"]
# #     # str_pattern = S_PO_VER_SCH
# #     # str_rep = S_PO_VER_REP.format(pp_version)

# #     # open file and get contents
# #     with open(path, "r", encoding=S_ENCODING) as a_file:
# #         text = a_file.read()

# #     # replace version
# #     # text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

#     # save file
#     with open(path, "w", encoding=S_ENCODING) as a_file:
#         a_file.write(text)


# ------------------------------------------------------------------------------
# Fix stuff in individual files
# ------------------------------------------------------------------------------
def _fix_files(path, dict_prv, dict_pub):
    """
    Fix stuff in individual files

    Args:
        path: G.Path object for file to be fixed
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
        path: G.Path for the README to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Removes parts of the file not applicable to the current project type. Also
    fixes metadata in the file when dict_meta is present.
    """

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
    text = G.re.sub(str_pattern, "", text, flags=G.re.S)

    # --------------------------------------------------------------------------

    # replace short description
    str_pattern = S_RM_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_RM_DESC_REP.format(pp_short_desc)
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.S)

    # replace version
    str_pattern = S_RM_VER_SCH
    pp_ver_disp = dict_prv_prj["__PP_VER_DISP__"]
    str_rep = S_RM_VER_REP.format(pp_ver_disp)
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.S)

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
        text = G.re.sub(str_pattern, str_rep, text, flags=G.re.S)

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
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.S)

    # --------------------------------------------------------------------------

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)


# ------------------------------------------------------------------------------
# Replace text in the pyproject file
# ------------------------------------------------------------------------------
def _fix_pyproject(path: G.Path, dict_prv_prj, dict_pub_meta):
    """
    Replace text in the pyproject file

    Args:
        path: G.Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: the dict of metadata to replace in the file

    Replaces things like the keywords, requirements, etc. in the toml file.
    """

    # convert long ver to mmr
    str_pattern = S_SEM_VER_VALID
    str_rep = dict_prv_prj["__PP_VER_MMR__"]
    str_rep = G.re.sub(str_pattern, S_SEM_VER_PYPRJ, str_rep)

    # --------------------------------------------------------------------------

    # default text if we can't open file
    text = ""

    # open file and get contents
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

    # replace version
    str_pattern = S_TOML_VER_SCH
    str_rep = S_TOML_VER_REP.format(str_rep)
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

    # replace short description
    str_pattern = S_TOML_DESC_SCH
    str_rep = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_TOML_DESC_REP.format(str_rep)
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

    # fix keywords for pyproject.toml
    l_keywords = dict_pub_meta[S_KEY_META_KEYWORDS]
    q_keywords = [f'"{item}"' for item in l_keywords]
    s_keywords = ", ".join(q_keywords)

    # replace keywords array
    str_pattern = S_TOML_KW_SCH
    str_rep = S_TOML_KW_REP.format(s_keywords)
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

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

            # ignore __pycache__
            if child_dir == "__pycache__":
                continue

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
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

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
        path: G.Path for the file to modify text
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
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

    # replace short description (comment)
    str_pattern = S_DESK_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_DESK_DESC_REP.format(pp_short_desc)
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

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
        path: G.Path for the file to modify text
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
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

    # replace short description
    str_pattern = S_UI_DESC_SCH
    pp_short_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
    str_rep = S_UI_DESC_REP.format(pp_short_desc)
    text = G.re.sub(str_pattern, str_rep, text, flags=G.re.M | G.re.S)

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
        path: G.Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Returns:
        The new line of code

    Fixes the version number and short description in any file whose extension
    is in L_EXT_PY. These two variables are special in that they can be changed
    between bakes (and indeed the version SHOULD BE CHANGED), so they fall
    outside the usual "replace dunder" paradigm. It also handles strings that
    are i18n'd.
    """

    # open and read whole file
    with open(path, "r", encoding=S_ENCODING) as a_file:
        text = a_file.read()

        # replace version in file
        str_ver = dict_prv_prj["__PP_VER_DISP__"]
        str_sch = S_SRC_VER_SCH
        str_rep = S_SRC_VER_REP.format(str_ver)
        text = G.re.sub(str_sch, str_rep, text, flags=G.re.S)

        # replace short desc in file
        str_desc = dict_pub_meta[S_KEY_META_SHORT_DESC]
        str_sch = S_SRC_DESC_SCH
        str_rep = S_SRC_DESC_REP.format(str_desc)
        text = G.re.sub(str_sch, str_rep, text, flags=G.re.S)

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
        path: G.Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Fixes the version number in install.json.
    """

    # open file and get contents
    a_dict = G.F.load_paths_into_dict(path)

    # replace version
    ver = dict_prv_prj["__PP_VER_MMR__"]
    a_dict[S_KEY_INST_VER] = ver

    # save file
    G.F.save_dict_into_paths(a_dict, path)


# ------------------------------------------------------------------------------
# Fix the theme name in mkdocs.yml
# ------------------------------------------------------------------------------
def _fix_mkdocs(path, _dict_prv_prj, dict_pub):
    """
    Fix the theme name in mkdocs.yml

    Args:
        path: G.Path for the file to modify text
        dict_prv_prj: Private calculated proj dict
        dict_pub_meta: Dict of metadata to replace in the file

    Fixes the theme name in mkdocs.yml.
    """

    # get theme name
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
    text = G.re.sub(str_pattern, str_rep, text)

    # save file
    with open(path, "w", encoding=S_ENCODING) as a_file:
        a_file.write(text)

