"""
docstring
"""

import json

DICT_SETTINGS = {
    "a1": "aa1",
    # "a2": "aa2",
    "b1": "3",
    # "b2": "4",
}

DICT_BLACKLIST = {
    "a": [
        "a1",
        "a2",
    ],
    "b": [
        "b1",
        "b2",
    ],
}

for key_set, val_set in DICT_SETTINGS.items():
    for key_bl in DICT_BLACKLIST:
        DICT_BLACKLIST[key_bl] = [
            item.replace(key_set, val_set) for item in DICT_BLACKLIST[key_bl]
        ]

print(json.dumps(DICT_BLACKLIST, indent=4))
