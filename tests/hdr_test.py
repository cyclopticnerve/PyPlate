"""docstring"""

from pathlib import Path
import re

D_HEADER = {
    "sch_hdr": (
        r"^((#|<!--) \S* *: )"  # 1/2 keyword
        r"(\S+( \S+)*)"  # 3/4 value (multi word)
        r"( *)"  # 5 padding (if any)
        r"(.*)"  # 6 rat (if any)
    ),
    # format param is fmt_val_pad result
    "rep_hdr": r"\g<1>{}\g<6>",
    "grp_val": 3,
    "grp_pad": 5,
    # format params are grp_val and grp_pad result
    "fmt_val_pad": "{}{}",
}

D_PRJ_REQ = {
    "__PD_AUTHOR__": "cyclopticnerve",
    "__PD_LICENSE_NAME__": "WTFPLv2",
    "__PA_DUMMY__": "",
    "__PC_NAME_BIG__": "PyPlate",
    "__PC_NAME_SMALL__": "pyplate",
    "__PC_DATE__": "04/21/2024",
}

# ------------------------------------------------------------------------------

def _fix_content(lines, bl_hdr=False, bl_code=False):

    # for each line in array
    for index, line in enumerate(lines):

        # skip blank lines, obv
        if line.strip() == "":
            continue

        # should we even look for headers?
        if not bl_hdr:

            # check if it matches header pattern
            str_pattern = D_HEADER["sch_hdr"]
            res = re.search(str_pattern, line)
            if res:

                # fix it
                lines[index] = _fix_header(line)

                # stop on first match
                continue

        if not bl_code:
            lines[index] = _fix_code(line)

# ------------------------------------------------------------------------------

def _fix_header(line):

    # break apart header line
    # NB: gotta do this again, can't pass res param
    str_pattern = D_HEADER["sch_hdr"]
    res = re.search(str_pattern, line)

    # pull out val and pad
    val = res.group(D_HEADER["grp_val"])
    pad = res.group(D_HEADER["grp_pad"])

    # do all string replacements and measurements
    old_len_val = len(val)
    val = _fix_code(val)
    new_len_val = len(val)

    # set default padding
    old_len_pad = len(pad)

    # only recalculate padding if val len changed
    # there is padding, must be rat
    if old_len_val != new_len_val and old_len_pad > 1:

        # get length change (+/-)
        val_diff = new_len_val - old_len_val

        # check if the amount to change is less than we've got
        # NB: invert the sign
        new_len_pad = old_len_pad + (0 - val_diff)

        # we need some padding
        if new_len_pad > 0:
            pad = " " * new_len_pad
        else:

            # always have at least one space in padding
            pad = " "

    # put the parts back together
    repl = D_HEADER["fmt_val_pad"].format(val, pad)

    # format replacement regex
    str_rep = D_HEADER["rep_hdr"].format(repl)
    line = re.sub(str_pattern, str_rep, line)

    # return replacement result
    return line

# ------------------------------------------------------------------------------

def _fix_code(line):

    # find all dunders in line
    for key, val in D_PRJ_REQ.items():
        line = line.replace(key, val)

    # return fixed code
    return line

# ------------------------------------------------------------------------------
# Code to run when called from command line
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    a_path = (
        Path.home()
        / "Documents/Projects/Python/PyPlate/template/all/tests/hdr_test.py"
    )

    a_lines = []

    with open(a_path, "r", encoding="UTF-8") as a_file:
        a_lines = a_file.readlines()

    _fix_content(a_lines)

    for a_line in a_lines:
        print(a_line)
