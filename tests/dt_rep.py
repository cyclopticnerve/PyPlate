"""docstring"""

from pathlib import Path
import re

IN_FILE = (
    "/home/dana/Documents/Projects/Python/PyPlate/template/gui/src/gui/"
    "desktop/template.desktop"
)
R_ICON_SCH = r"^(Icon=)(.*)$"
R_ICON_REP = r"\g<1>{}/\g<2>"

STR_ICON = ".local/share/gui_test/src/gui/desktop/GUI_Test.png"
PATH_ICON = Path(STR_ICON).resolve()
print(PATH_ICON)

HOME = Path.home()
R_ICON_REP = R_ICON_REP.format(HOME)

with open(IN_FILE, "r", encoding="UTF-8") as a_file:
    text = a_file.read()

res = re.search(R_ICON_SCH, text, flags=re.M)
if res:
    path_icon = res.group(2)
    print(path_icon)
    text = re.sub(R_ICON_SCH, R_ICON_REP, text, flags=re.M)

# print(res)
print(text)
