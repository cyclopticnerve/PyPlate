# ------------------------------------------------------------------------------
# Project : __PP_NAME_BIG__                                        /          \
# Filename: metadata.py                                           |     ()     |
# Date    : __PP_DATE__                                           |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

import os
import re

path = os.path.abspath(__file__)
rep = "03/03/0303"


def check():
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines:

            # pattern
            pattern = (
                r'(# )'
                r'(Project)'
                r'( *: )'
                r'([\w./]*)'
                r'( *)'
                r'(.*)'
            )
            res = re.search(pattern, line)

            print(len(line))

            if res:
                key_cnt = (
                    len(res.group(1)) +
                    len(res.group(2)) +
                    len(res.group(3)) +
                    len(rep) +
                    # len(res.group(5)) +
                    len(res.group(6))
                )

                spaces = (
                    len(line) - 1 - key_cnt
                )
                spaces_str = ' ' * spaces

                rep_str = rf'\g<1>\g<2>\g<3>{rep}{spaces_str}\g<6>'
                line = re.sub(pattern, rep_str, line)

            print(line, end='')


if __name__ == '__main__':
    check()
