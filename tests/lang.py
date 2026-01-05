from pathlib import Path
import re

CUR = Path(__file__).parent.resolve()
SIS = CUR  / "spaceoddity.po"

R_FIND = r"\"Language: (.*)(\\n)"

with open(SIS, "r", encoding="UTF8") as a_file:
    # lines = a_file.readlines()
    string = a_file.read()

    # for line in lines:
    res = re.search(R_FIND, string)
    if res:
        print(res.group(1))
            # print(res)
            # for group in res.groups():
            #     print(group)

    # print(lines)