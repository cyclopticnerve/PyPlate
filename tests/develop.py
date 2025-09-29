#!/usr/bin/env python

"""fuck off"""

import json
from pathlib import Path
import subprocess

# ------------------------------------------------------------------------------

dir_prj = Path(__file__).parents[1].resolve()
p_file_prv = dir_prj / "pyplate/private/private.json"

# get dict prv prj
with open(p_file_prv, encoding="UTF8") as a_file:
    dict_prv = json.load(a_file)

# get inner dicts
dict_prv_all = dict_prv["PRV_ALL"]
dict_prv_prj = dict_prv["PRV_PRJ"]

# get dict values
name_venv = dict_prv_prj["__PP_NAME_VENV__"]
reqs_file = dict_prv_all["__PP_REQS_FILE__"]

is_pkg = dict_prv_prj["__PP_TYPE_PRJ__"] == "p"

# ------------------------------------------------------------------------------

MSG_FAILED = "Failed"
MSG_DONE = "Done"
MSG_MAKE_VENV = "Making venv... "
MSG_INST_REQS = "Installing requirements... "

CMD_MAKE_VENV = f"cd {dir_prj};python -m venv {name_venv}"
CMD_REQS_CLI = f"cd {dir_prj};. {name_venv}/bin/activate;python -m pip install -r {reqs_file}"
CMD_REQS_PKG = (
    f"cd {dir_prj};. {name_venv}/bin/activate;python -m pip install -e ."
)

# ------------------------------------------------------------------------------

# 1. make venv
# 2. get inst cmd
# 3: do inst cmd

# ------------------------------------------------------------------------------
# 1. make venv

print(MSG_MAKE_VENV, end="", flush=True)

try:
    # subprocess.run(MAKE_CMD_VENV, shell=True, check=True)
    print(CMD_MAKE_VENV)
except (FileNotFoundError, subprocess.CalledProcessError) as e:
    print(MSG_FAILED)

print(MSG_DONE)

# ------------------------------------------------------------------------------
# 2: get inst cmd

CMD_INST_REQS = CMD_REQS_CLI
if is_pkg:
    CMD_INST_REQS = CMD_REQS_PKG

# ------------------------------------------------------------------------------

# 3. do inst cmd
print(MSG_INST_REQS, end="", flush=True)

try:
    # subprocess.run(CMD, shell=True, check=True)
    print(CMD_INST_REQS)
except (FileNotFoundError, subprocess.CalledProcessError) as _e:
    print(MSG_FAILED)

print(MSG_DONE)
