"""doc"""

from pathlib import Path
import re
from typing import Dict, Any

path = Path(__file__).parent.resolve()
path = path / "strs2.py"

# ------------------------------------------------------------------------------

S_SW_ENABLE = "enable"
S_SW_DISABLE = "disable"
S_SW_REPLACE = "replace"

R_SW_SPLIT = r"(\'|\")([^\'\"\n]+)(\'|\")|(\#.*)"
R_SW_SWITCH = r"^\s*#\s*pyplate\s*:\s*(\S*)\s*=\s*(\S*)\s*$"

D_BLOCK = {
    S_SW_REPLACE: True,
}
D_LINE: Dict[str, Any] = {
    S_SW_REPLACE: None,
}

# ------------------------------------------------------------------------------

def do_lines():
    """doc"""

    with open(path, "r", encoding="UTF8") as a_file:
        lines = a_file.readlines()

    for line in lines:

        code = line
        comm = ""

        matches = re.finditer(R_SW_SPLIT, line)
        for match in matches:
            if match.group(4):
                split = match.start(4)
                code = line[:split]
                comm = line[split:]

        handle_switch(code, comm)

        print("code :", code.rstrip())
        print("comm :", comm.rstrip())

        if (
            D_BLOCK[S_SW_REPLACE]
            and D_LINE[S_SW_REPLACE] != 0
            or D_LINE[S_SW_REPLACE] == 1
        ):
            print("repl")
        else:
            print("no repl")

        print("----")

# ------------------------------------------------------------------------------

def handle_switch(code, comm):
    """doc"""

    switch = re.search(R_SW_SWITCH, comm)
    if not switch:
        return

    key = switch.group(2)
    val = switch.group(1)

    if code.strip() == "":

        if key in D_BLOCK:
            if val == S_SW_ENABLE:
                D_BLOCK[key] = True
            elif val == S_SW_DISABLE:
                D_BLOCK[key] = False

    else:

        D_LINE[key] = None
        if key in D_LINE:
            if val == S_SW_ENABLE:
                D_LINE[key] = True
            elif val == S_SW_DISABLE:
                D_LINE[key] = False


do_lines()
