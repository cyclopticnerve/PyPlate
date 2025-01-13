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

# ------------------------------------------------------------------------------
# A convenience method to return the type of a control, parsed from the
# class control set
# ------------------------------------------------------------------------------
# def _get_ctl_type(self, ctl_name):
#     """
#     A convenience method to return the type of a control, parsed from the
#     class control set

#     Args:
#         class_dict: the dict of common class properties
#         ctl_name: the control whose type we want to know

#     Returns the control type for a specified control in a specified class,
#     so that we can determine setter/getter methods as well as the value
#     type. The result is one of constants.CTL_TYPE_...
#     """

#     # get controls for class
# Args:
#     ui_file: The file containing the dialog description in xml
#     dlg_name: The name of the dialog in the ui file
#     class_ctls = class_dict.get(AC.KEY_CLS_CTLS, {})

#     # get control type
#     dict_ctl = class_ctls.get(ctl_name, {})
#     ctl_type = dict_ctl.get(AC.KEY_CTL_TYPE, AC.CTL_TYPE_TEXT)

#     # return the type
#     return ctl_type

# ------------------------------------------------------------------------------
# Called when the gui dict is passed in, to ensure all values are of the
# correct type
# ------------------------------------------------------------------------------
# def _sanitize_gui(self, dict_gui):
#     """
#     Called when a gui dict is passed in, to ensure all values are of
#     the correct type

#     Args:
#         dict_class: The dict_app entry for this window's class
#         dict_gui: The dict to sanitize

#     Returns:
#         The sanitized dict
#     """

#     # do visibility
#     # NB: do not use get, if it's empty, skip and leave it empty
#     # if AC.KEY_WIN_VISIBLE in dict_gui:
#     #     val = dict_gui[AC.KEY_WIN_VISIBLE]
#     #     val = CF.do_bool(val)
#     #     dict_gui[AC.KEY_WIN_VISIBLE] = val

#     # check if size dict exists
#     # NB: do not use get, if it's empty, skip and leave it empty
#     if A.KEY_WIN_SIZE in dict_gui:
#         # get the size dict
#         dict_size = dict_gui[A.KEY_WIN_SIZE]

#         # fix width
#         w = dict_size[A.KEY_WIN_SIZE_W]
#         dict_size[A.KEY_WIN_SIZE_W] = int(w)

#         # fix height
#         h = dict_size[A.KEY_WIN_SIZE_H]
#         dict_size[A.KEY_WIN_SIZE_H] = int(h)

#         # fix max
#         m = dict_size[A.KEY_WIN_SIZE_M]
#         dict_size[A.KEY_WIN_SIZE_M] = CF.do_bool(m)

#         # put it back
#         dict_gui[A.KEY_WIN_SIZE] = dict_size

#     # check if controls dict exists
#     # NB: do not use get, if it's empty, skip and leave it empty
#     if A.KEY_WIN_CTLS in dict_gui:
#         # get the window's controls dict
#         dict_ctls = dict_gui[A.KEY_WIN_CTLS]

#         # for each control
#         for k, v in dict_ctls.items():
#             # get value type from control type
#             ctl_type = get_ctl_type(k)
#             val_type = ctl_type.get(AC.KEY_CTL_VAL_TYPE, None)

#             # get the val from the user dict
#             val = v.get(AC.KEY_CTL_VAL, "")

#             # convert int
#             if val_type == AC.CTL_VAL_TYPE_INT:
#                 val = int(val)

#             # convert bool
#             elif val_type == AC.CTL_VAL_TYPE_BOOL:
#                 val = CF.do_bool(val)

#             # update controls dict
#             dict_ctls[k][AC.KEY_CTL_VAL] = val

#         # update window dict
#         dict_gui[AC.KEY_WIN_CTLS] = dict_ctls

#     # return updated dict
#     return dict_gui

# # --------------------------------------------------------------------------
# # A convenience method to set the value of the specified control
# # --------------------------------------------------------------------------
# def set_control(self, ctl_name, value):
#     """
#     A convenience method to set the value of the specified control

#     Args:
#         ctl_name: The name of the control in the UI file
#         value: The new value for the control

#     Returns the value of a window control as named in the UI file.
#     """

#     # get the control
#     obj = self._builder.get_object(ctl_name)

#     # get control's type
#     type_ = AF.get_ctl_type(self._dict_class, ctl_name)

#     # get control's setter method
#     set_ = type_[A.KEY_CTL_SET]

#     # call method to set value
#     fnc = getattr(obj, set_)
#     fnc(value)

# # --------------------------------------------------------------------------
# # A convenience method to return the value of the specified control
# # --------------------------------------------------------------------------
# def get_control(self, ctl_name):
#     """
#     A convenience method to return the value of the specified control

#     Args:
#         ctl_name: The name of the control in the UI file

#     Returns the value of a window control as named in the UI file.
#     """

#     # get the control
#     obj = self._builder.get_object(ctl_name)

#     # get control's type
#     type_ = AF.get_ctl_type(self._dict_class, ctl_name)

#     # get control's getter method
#     get = type_[A.KEY_CTL_GET]

#     # call method to get value
#     fnc = getattr(obj, get)
#     val = fnc()

#     # return value
#     return val

# # --------------------------------------------------------------------------
# # Sets the values of all controls before window is shown
# # --------------------------------------------------------------------------
# def set_controls(self, dict_ctls):
#     """
#     Sets the values of all controls before window is shown

#     Args:
#         dict_ctls: The dict containing the values for each control

#     Set the values of all controls from the specified dict when this
#     method is called.
#     """

#     # now put the new gui values into the controls
#     for k, v in dict_ctls.items():

#         # get the value
#         val = v[A.KEY_CTL_VAL]

#         # do the method for each control
#         self.set_control(k, val)

# # --------------------------------------------------------------------------
# # Gets the current values of all controls to a dictionary
# # --------------------------------------------------------------------------
# def get_controls(self):
#     """
#     Gets the current values of all controls to a dictionary

#     Returns:
#         A dictionary containing the current values of the controls

#     Gets the values of all gui objects and return it whenever this method
#     is called. This method is called from several places, both for
#     saving the actual gui values and also for checking the existence of
#     keys. Creating a temp dict and returning it ensures that no keys are
#     missing and no values are empty, similar to _get_size.
#     """

#     # create a tmp dict
#     result = {}

#     # get the controls we want to save
#     dict_ctls = self._dict_class[A.KEY_CLS_CTLS]

#     # now get the new values from the controls
#     for k, _v in dict_ctls.items():

#         # get the value in the control
#         val = self.get_control(k)

#         # save val to dict
#         result[k] = {
#             A.KEY_CTL_VAL: val,
#         }

#     # return the tmp dict
#     return result

# # --------------------------------------------------------------------------
# # Update the backing dict of a particular window, setting its size and
# # control values
# # --------------------------------------------------------------------------
# def set_dict_state(self, name_win, dict_state):
#     """
#     Update the backing dict of a particular window, saving its size and
#     control values

#     Args:
#         name_win: The name of the window to save the GUI for
#         dict_state: The current state of the window's GUI, to be saved in
#         the global backing store

#     This method updates the backing store for a particular window whenever
#     that window's values change (such as size or control values).

#     This method should NOT be called by any outside script. It is public
#     only so it can be used by Window and its subclasses.

#     The contents of this dict are a reflection of the CURRENT VALUES of the
#     GUI, after any changes have been made. This method is called by the
#     window's _do_update method.
#     """

#     # set the gui dict for the window name
#     self._dict_state[name_win] = dict_state
#     # TODO: for each window in dict_app, if has entry in dict_state, apply
#     # dict_state to window

# # --------------------------------------------------------------------------
# # Return the backing dict of all windows, containing their size and
# # control values
# # --------------------------------------------------------------------------
# def get_dict_state(self, name_win):
#     """
#     Return the backing dict of all windows, containing their size and
#     control values

#     Returns:
#         The current backing dictionary

#     This method should be called after run(), so that the dict is updated
#     after any save actions have been completed.

#     The contents of this dict are a reflection of the CURRENT VALUES of the
#     GUI, after any changes have been made. The dict is updated by
#     set_dict_state.

#     The dictionary does NOT contain settings like window class, close
#     action, etc. since these do not need to be saved between sessions.
#     """

#     # return the backing gui dict
#     if name_win in self._dict_state:
#         return self._dict_state[name_win]

#     return None

# --------------------------------------------------------------------------
# Private methods
# --------------------------------------------------------------------------

# # --------------------------------------------------------------------------
# # Creates a dialog for when the window is closed by some means and is
# # modified, and returns the result of that dialog
# # --------------------------------------------------------------------------
# def _show_close_dialog(self):
#     """
#     Creates a dialog for when the window is closed by some means and is
#     modified, and returns the result of that dialog

#     Returns:
#         The result of the dialog as one of:
#         - Gtk.ResponseType.CLOSE
#         - Gtk.ResponseType.CANCEL
#         - Gtk.ResponseType.OK

#     Create a dialog that has 3 buttons, set their labels/colors, and return
#     which button was clicked.
#     """

#     # create a new message box
#     msg_box = Gtk.MessageDialog(
#         parent=self.window,
#         text=self._app.STR_CLOSE_DLG_MAIN,
#         secondary_text=self._app.STR_CLOSE_DLG_SEC,
#         message_type=Gtk.MessageType.QUESTION,
#     )

#     # add buttons to message box
#     # I18N
#     msg_box.add_buttons(
#         self._app.STR_CLOSE_DLG_CLOSE,
#         Gtk.ResponseType.CLOSE,
#         self._app.STR_CLOSE_DLG_CANCEL,
#         Gtk.ResponseType.CANCEL,
#         # NEXT: if doc-based and untitled, this should be "Save As..."
#         self._app.STR_CLOSE_DLG_SAVE,
#         Gtk.ResponseType.OK,
#     )

#     # make all buttons stretch
#     msg_box.action_area.set_homogeneous(True)  # pylint: disable=no-member

#     # set the bad/none button as red
#     btn_red = msg_box.get_widget_for_response(
#         response_id=Gtk.ResponseType.CLOSE
#     )
#     btn_red_style_context = btn_red.get_style_context()
#     btn_red_style_context.add_class("destructive-action")

#     # set focus to save button
#     btn_def = msg_box.get_widget_for_response(
#         response_id=Gtk.ResponseType.OK
#     )
#     msg_box.set_focus(btn_def)

#     # center dialog on parent
#     msg_box.set_position(  # pylint: disable=no-member
#         Gtk.WindowPosition.CENTER
#     )

#     # show message box and get result
#     result = msg_box.run()  # pylint: disable=no-member
#     msg_box.hide()

#     # return the button that was clicked
#     return result

# --------------------------------------------------------------------------
# A convenience method for subclasses to update their control values in the
# backing store
# --------------------------------------------------------------------------
# def _update_gui(self):
#     """
#     A convenience method for subclasses to update their control values in
#     the backing store

#     This method just hides some implementation details when a window wants
#     to update its gui values in the backing store.
#     """

#     # save size/objects
#     self._dict_state[A.KEY_WIN_SIZE] = self._get_size()
#     self._dict_state[A.KEY_WIN_CTLS] = self.get_state()

#     # save backing store to app
#     self._app.set_dict_state(self._name_win, self._dict_state)

#     # update modified status (ignore return)
#     self.is_modified()

# start with a clean dict
# self._dict_state = {}
# TODO: get_state should return a dict of size/gui
# self._dict_state = self._get_state()

# get current (default) size/controls from ui file
# self._dict_state[A.KEY_WIN_SIZE] = self._get_size()
# self._dict_state[A.KEY_WIN_SIZE] = self.get_state()[A.KEY_WIN_SIZE]
# self._dict_state[A.KEY_WIN_CTLS] = self.get_state()[A.KEY_WIN_CTLS]

# combine user_dict values
# order of precedence is:
# 1. values from ui file
# 2. values passed in from user (param dict_gui)

# combine ui settings and user settings
# TODO: wtf is dict_win?
# need to get def size/gui from ui file, combine with param,
# set_state with that combined dict

# dict_win = dict_state[self._name_win]
# self._dict_state = CF.combine_dicts(self._dict_state, [dict_win])

# fix ints/bools in dict_gui
# TODO: how to sanitize gui for bool/int/str without ctl type?
# self._dict_state = self._sanitize_gui(self._dict_state)

# once we have the final dict_gui, apply backing store to window
# self._set_size()

# get the list of window controls
# dict_ctls = self._dict_state[A.KEY_WIN_CTLS]
# self.set_controls(dict_ctls)
# NB: use sanitized state
# self._set_state(self._dict_state)

# save backing store to app
# self._app.set_dict_state(self._name_win, self._dict_state)
