# from pprint import pp
from cnlib import cnfunctions as F

# ------------------------------------------------------------------------------

dict_def = {
    "__PP_PRJ_TYPE__": "c",
    "foo": {
        "__NEW_KEY__": "",
    },
}

dict_prj = {
    "__PP_PRJ_TYPE__": "c",
}

# ------------------------------------------------------------------------------

dict_new = F.combine_dicts(dict_def, dict_prj)
F.pp(dict_new)

print("-----------------------------------------------------------------------")

dict_new = F.combine_dicts(dict_prj, dict_def)
F.pp(dict_new)
