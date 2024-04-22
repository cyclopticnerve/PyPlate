"""docstring"""
from pathlib import Path
import re

# the list of keywords to search in headers
L_HEADER = [
    "Project",  # PyPlate
    "Filename",  # pyplate.py
    "Date",  # 12/08/2022
    "Author",  # cyclopticnerve
    "License",  # WTFPLv2
]

D_PRJ_CFG = {
    "__PD_AUTHOR__": "cyclopticnerve",
    "__PD_LICENSE_NAME__": "WTFPLv2",
    # --------------------------------------------------------------------------
    "__PC_NAME_BIG__": "BigNameProject",  # PyPlate
    "__PC_DATE__": "04/21/2024",  # the date pymaker was run
    "__PC_FILENAME__": Path(__file__).name,
}

D_PRJ_PRJ = {
    "__PP_DUMMY__": "",
}

R_HEADER = (
    # format is keyword from L_HEADER
    r"^(\s*(#|<!--)\s*{}\s*:)"  # 1/2 key
    r"(\s*)(\S*)"  # 3 space / 4 dunder
    r"(\s*)(.*)"  # 5 pad / 6 rat
)

# header replacement string
# format dunder repl, rat
R_HEADER_REP = r"\g<1>\g<3>{}{}\g<6>"

SRC1 = [
    "# ------------------------------------------------------------------------------\n",
    "# Project : __PC_NAME_BIG__                                        /          \\\n",
    "# Filename: test.py                                               |     ()     |\n",
    "# Date    : __PC_DATE__                                           |            |\n",
    "# Author  : __PD_AUTHOR__                                         |   \\____/   |\n",
    "# License : __PD_LICENSE_NAME__                                    \\          /\n",
    "# ------------------------------------------------------------------------------\n",
]
SRC2 = [
    "# ------------------------------------------------------------------------------\n",
    "# Filename: __PP_DUMMY__                                          |     ()     |\n",
    "# ------------------------------------------------------------------------------\n",
]
SRC3 = [
    "# ------------------------------------------------------------------------------\n",
    "# Filename: __PC_FILENAME__                                       |     ()     |\n",
    "# ------------------------------------------------------------------------------\n",
]

def fix_header(src_str):
    """
    docstring
    """

    dict_repls = {}
    for key, val in D_PRJ_CFG.items():
        dict_repls[key] = val
    for key, val in D_PRJ_PRJ.items():
        dict_repls[key] = val

    # default lines
    lines = "".join(src_str)
    print(lines)

    # for each header key
    for item in L_HEADER: # "Project"

        # put keyword in regex pattern
        str_pattern = R_HEADER.format(item)

        # find first instance of header pattern
        # search for regex with "# Project : xxx...\n"
        # NB: need M for caret match
        res = re.search(str_pattern, lines, flags=re.M)

        # no res, keep going
        if not res:
            continue

        # replace bits
        repl = res.group(4)

        # save old len for padding
        old_len = len(repl)

        # do string replacement
        for key_set, val_set in dict_repls.items():
            repl = repl.replace(key_set, val_set)

        # get the new len and the difference
        new_len = len(repl)
        len_diff = new_len - old_len
        abs_diff = abs(len_diff)

        # add or remove spaces from pad
        pad = res.group(5)

        # string got longer, remove leading spaces
        if len_diff > 0:
            pad = pad[abs_diff:]
        else:
            # string got shorter, insert leading spaces
            s_pad = " " * abs_diff
            pad = s_pad + pad

        # replace text in the line
        str_rep = R_HEADER_REP.format(repl, pad)
        lines = re.sub(str_pattern, str_rep, lines, flags=re.M)

    print(lines)

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # Code to run when called from command line

    # This is the top level code of the program, called when the Python file is
    # invoked from the command line.

    # run main method
    fix_header(SRC1)
    fix_header(SRC2)
    fix_header(SRC3)

# -)
