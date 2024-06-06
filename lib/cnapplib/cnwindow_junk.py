# store properties
# self._app = app
# self._name_win = name_win
# self._dict_state = dict_state
# self._close_dlg_file = close_dlg_file
# self._close_dlg_name = close_dlg_name


# minimum dict_win must contain:
# AC.KEY_WIN_CLASS,
# class_win = dict_win.get(AC.KEY_WIN_CLASS, None)
# if class_win is None:
#     # I18N: the specified class is None
#     raise IOError(AC.ERR_CLASS_NONE)

# # get the app dict for the class
# dict_classes = self._app._dict_app[AC.KEY_APP_CLASSES]
# self._dict_class = dict_classes[class_win]

# save size/objects
# self._dict_state[A.KEY_WIN_SIZE] = self._get_size()
# # self._dict_state[A.KEY_WIN_CTLS] = self.get_state()

# # save backing store to app
# # self._app.set_dict_state(self._name_win, self._dict_state)

# # update modified status (ignore return)
# self._is_modified()

# return self._dict_state
