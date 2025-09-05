# dict_state = {
#     "name_win": {  # name_win/state_win
#         KEY_CLASS: "windowmain.WindowMain",  # mod_name.Class_Name
#         KEY_SIZE: {
#             KEY_SIZE_W: 0,  # int
#             KEY_SIZE_H: 0,  # int
#             KEY_SIZE_M: False,  # bool
#         },
#         KEY_CTLS: {
#             "entry_test": "a",  # str/int/bool
#         },
#         KEY_TITLE = "",  # use value from .ui file
#         KEY_VISIBLE = True,  # whether the window is restored at next launch
#     },
# }

# keys for state dict
# class name as string
KEY_CLASS = "KEY_CLASS"
# size sub-dict
KEY_SIZE = "KEY_SIZE"
KEY_SIZE_W = "KEY_SIZE_W"
KEY_SIZE_H = "KEY_SIZE_H"
KEY_SIZE_M = "KEY_SIZE_M"
# controls sub-dict
KEY_CTLS = "KEY_CTLS"
# last set title
KEY_TITLE = "KEY_TITLE"
# is window visible at launch
KEY_VISIBLE = "KEY_VISIBLE"
