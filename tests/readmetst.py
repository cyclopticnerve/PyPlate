
import os
import re


path = os.path.abspath(os.path.dirname(__file__))
path2 = os.path.join(path, '../template/README.md')
rep = 'ABCDEFG'


def check():
    with open(path2, 'r', encoding='utf-8') as f:
        line = f.read()

        # for line in lines:

        # pattern
        pattern = (
            r'<!-- __PP_SHORT_DESC_START__ -->[\W](.*)'  # \n<!-- __PP_SHORT_DESC_END__ -->'
        )
        res = re.search(pattern, line)

        # print(len(line))

        if res:
            # key_cnt = (
            #     len(res.group(1)) +
            #     len(res.group(2)) +
            #     len(res.group(3)) +
            #     len(rep) +
            #     # len(res.group(5)) +
            #     len(res.group(6))
            # )

            # spaces = (
            #     len(line) - 1 - key_cnt
            # )
            # spaces_str = ' ' * spaces

            # rep_str = rf'\g<1>{rep}\g<3>'
            # line = re.sub(pattern, rep_str, line)

            print(line, end='')


if __name__ == '__main__':
    check()
