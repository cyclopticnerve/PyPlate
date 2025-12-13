# --------------------------------------------------------------------------
# Make reps, save public, fix public dunders, reload sub dicts
# --------------------------------------------------------------------------
def _fix_dicts(self):
    """
    Make reps, save/fix public dunders, reload sub dicts

    Make reps, save/fix public dunders, reload sub dicts
    """

    # ----------------------------------------------------------------------
    # get prv subs
    self._dict_prv_all = self._dict_prv[C.S_KEY_PRV_ALL]
    self._dict_prv_prj = self._dict_prv[C.S_KEY_PRV_PRJ]

    # ----------------------------------------------------------------------
    # get prv subs
    self._dict_rep = self._dict_prv_all | self._dict_prv_prj

    # ----------------------------------------------------------------------
    # save/fix/load public

    try:
        # save public settings
        path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
        F.save_dict_into_paths(self._dict_pub, [path_pub])
    except OSError as e:  # from save_dict
        F.printd(self.S_ERR_ERR, str(e))

    # fix dunders in dict_pub
    self._fix_contents(path_pub)

    try:
        # load public settings
        path_pub = self._dir_prj / C.S_PRJ_PUB_CFG
        self._dict_pub = F.load_paths_into_dict([path_pub])
    except OSError as e:  # from load dict
        F.printd(self.S_ERR_ERR, str(e))

    # ----------------------------------------------------------------------
    # get pub subs
    self._dict_pub_bl = self._dict_pub[C.S_KEY_PUB_BL]
    self._dict_pub_dbg = self._dict_pub[C.S_KEY_PUB_DBG]
    self._dict_pub_dist = self._dict_pub[C.S_KEY_PUB_DIST]
    self._dict_pub_docs = self._dict_pub[C.S_KEY_PUB_DOCS]
    self._dict_pub_i18n = self._dict_pub[C.S_KEY_PUB_I18N]
    self._dict_pub_meta = self._dict_pub[C.S_KEY_PUB_META]

