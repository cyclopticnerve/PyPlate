from pathlib import Path
import re

path = str(Path(__file__))
print(path)

home = str(Path.home())

with open(path, "r", encoding="UTF8") as a_file:
    text = a_file.read()

# delete path from .pot/.po files (in case of debug)
# NB: also no regex or rules, just nuke it everywhere
text = text.replace(home, "")

# save file
with open(path, "w", encoding="UTF8") as a_file:
    a_file.write(text)