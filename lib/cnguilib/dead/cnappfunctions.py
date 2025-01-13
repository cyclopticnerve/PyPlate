# # ------------------------------------------------------------------------------
# # Project : CNAppLib                                               /          \
# # Filename: cnappfunctions.py                                     |     ()     |
# # Date    : 03/14/2024                                            |            |
# # Author  : cyclopticnerve                                        |   \____/   |
# # License : WTFPLv2                                                \          /
# # ------------------------------------------------------------------------------

# """
# A collection of common functions used by different classes in the library

# Functions:
#     get_ctl_type: A convenience method to return the type of a control, parsed
#     from the class control set
#     sanitize_gui(): Called when a gui dict is passed in, to ensure all values
#     are of the correct type
# """

# # ------------------------------------------------------------------------------
# # Imports
# # ------------------------------------------------------------------------------

# # pylint: disable=import-error

# # my imports
# from cnlib import cnfunctions as CF
# from . import cnapp as AC

# # pylint: enable=import-error


# # ------------------------------------------------------------------------------
# # A convenience method to return the type of a control, parsed from the
# # class control set
# # ------------------------------------------------------------------------------
# def get_ctl_type(class_dict, ctl_name):
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
#     class_ctls = class_dict.get(AC.KEY_CLS_CTLS, {})

#     # get control type
#     dict_ctl = class_ctls.get(ctl_name, {})
#     ctl_type = dict_ctl.get(AC.KEY_CTL_TYPE, AC.CTL_TYPE_TEXT)

#     # return the type
#     return ctl_type


# # ------------------------------------------------------------------------------
# # Called when the gui dict is passed in, to ensure all values are of the
# # correct type
# # ------------------------------------------------------------------------------
# def sanitize_gui(dict_class, dict_gui):
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
#     if AC.KEY_WIN_VISIBLE in dict_gui:
#         val = dict_gui[AC.KEY_WIN_VISIBLE]
#         val = CF.do_bool(val)
#         dict_gui[AC.KEY_WIN_VISIBLE] = val

#     # check if size dict exists
#     # NB: do not use get, if it's empty, skip and leave it empty
#     if AC.KEY_WIN_SIZE in dict_gui:
#         # get the size dict
#         dict_size = dict_gui[AC.KEY_WIN_SIZE]

#         # fix width
#         w = dict_size[AC.KEY_SIZE_W]
#         dict_size[AC.KEY_SIZE_W] = int(w)

#         # fix height
#         h = dict_size[AC.KEY_SIZE_H]
#         dict_size[AC.KEY_SIZE_H] = int(h)

#         # fix max
#         m = dict_size[AC.KEY_SIZE_M]
#         dict_size[AC.KEY_SIZE_M] = CF.do_bool(m)

#         # put it back
#         dict_gui[AC.KEY_WIN_SIZE] = dict_size

#     # check if controls dict exists
#     # NB: do not use get, if it's empty, skip and leave it empty
#     if AC.KEY_WIN_CTLS in dict_gui:
#         # get the window's controls dict
#         dict_ctls = dict_gui[AC.KEY_WIN_CTLS]

#         # for each control
#         for k, v in dict_ctls.items():
#             # get value type from control type
#             ctl_type = get_ctl_type(dict_class, k)
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


# # -)
