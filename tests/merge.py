# from pprint import pp
from cnlib import cnfunctions as F

# ------------------------------------------------------------------------------

def combine_dicts(dict_a, dict_b):

    # check for def pram gotcha
    if not dict_b:
        dict_b = {}

    if not isinstance(dict_a, list):
        dict_a = [dict_a]

    for item in dict_a:

        # for each k,v pair in dict_new
        for k, v in item.items():

            # if the value is a dict
            if isinstance(v, dict):
                # recurse using the current key and value
                dict_b[k] = combine_dicts(v, dict_b.get(k, None))
                continue

            # if the value is not a dict, just copy value from one dict to the other
            dict_b[k] = v

    return dict_b

# ------------------------------------------------------------------------------

a_dict_a = {
    "__PP_PRJ_TYPE__": "c",
    "foo": {
        "__NEW_KEY__": "",
    },
}

a_dict_b = {
    "__PP_PRJ_TYPE__": "c",
}

# ------------------------------------------------------------------------------

dict_new = combine_dicts([a_dict_a], a_dict_b)
F.pp(dict_new)

print("-----------------------------------------------------------------------")

dict_new = combine_dicts(a_dict_b, a_dict_a)
F.pp(dict_new)
