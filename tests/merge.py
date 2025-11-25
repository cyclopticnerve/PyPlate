from pprint import pp

# ------------------------------------------------------------------------------

def combine_dicts(dict_a, dict_b):

    # check for def pram gotcha
    if not dict_b:
        dict_b = {}

    # for each k,v pair in dict_new
    for k, v in dict_a.items():

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
    "dict_key_1a": {
        "key_1a": "val_1a",
    },
    "dict_key_2a": {
        "key_2a": "val_2a",
    },
}

a_dict_b = {
    "dict_key_1a": {
        "key_1b": "val_1b",
    },
    "dict_key_2a": {
        "key_2a": "",
    },
    # "dict_key_2b": {
    #     "key_2b": "",
    # },
    # "dict_key_2a": {
    #     "key_2a": "",
    # },
    # "dict_key_3b": {
    #     "key_3b": "",
    # },
}

# ------------------------------------------------------------------------------

pp(combine_dicts(a_dict_a, a_dict_b), width=1)
print("-----------------------------------------------------------------------")
pp(combine_dicts(a_dict_b, a_dict_a), width=1)
