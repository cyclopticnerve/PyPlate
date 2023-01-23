import json

with open('./template/misc/empty_class.py') as file:
    lines = file.readlines()

header_start = \
    '# ------------------------------------------------------------------------------'
header_end = header_start
header_sep = ':'

header_parts = [

]

in_it = False

for line in lines:

    if line.strip() == header_start and not in_it:
        in_it = True
        continue

    if in_it:
        if line.strip() == header_end and in_it:
            in_it = False
            break

        # print(line.strip())

        parts_a = line.split(header_sep)
        after = parts_a[1]
        after = after.replace('\n', '')
        parts_b = after.split(maxsplit=1)
        for pa in parts_b:
            print('x' + pa + 'x\n')
        header_parts.append([parts_a[0], parts_b[0], parts_b[1]])

print(json.dumps(header_parts, indent=4))


for item in header_parts:

    spaces = 80 - (len(item[0]) + len(item[1]) + len(item[2]))
    spaces_str = ' ' * spaces

    # create replacement string (with newline!!!)
    rep_str = f'{item[0]}:{item[1]}{spaces_str}{item[2]}'
    print(rep_str)

# head    | repl                 | blank                         | tail        |
# Project : __CN_BIG_NAME__                                        /          \
# Filename: __CN_SMALL_NAME__.py                                  |     ()     |
# Date    : __CN_DATE__                                           |            |
# Author  : __CN_AUTHOR__                                         |   \____/   |
# License : __CN_LICENSE__                                         \          /

"""
    head starts at 0
    repl starts at 12
    blank starts at 29
    more starts at 68

    head starts at 0
    repl starts at 12
    blank starts at 34
    more starts at 67

    head starts at 0
    repl starts at 12
    blank starts at 25
    more starts at 67

    head starts at 0
    repl starts at 12
    blank starts at 27
    more starts at 67

    head starts at 0
    repl starts at 12
    blank starts at 28
    more starts at 68

    regex 101
    (# [a-zA-Z]*:)\\s(__[A-Z_]*__)(\\s*)(.*)
    # Project: __CN_PRJ_NAME__          /      \\

"""
