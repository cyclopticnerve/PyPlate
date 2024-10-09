#! /usr bin/env python
"""
docstring
"""

import json
from pathlib import Path
import shutil

src = Path(__file__).parent.resolve()
conf = src / "inst_conf.json"
dict_install = {}

with open(conf, "r", encoding="UTF-8") as a_file:
    dict_install = json.load(a_file)

for key, val in dict_install.items():

    new_src = src / key
    new_dst = Path.home() / val / new_src.name

    if new_src.is_dir():
        shutil.copytree(new_src, new_dst)
    elif new_src.is_file():
        shutil.copy2(new_src, new_dst)
