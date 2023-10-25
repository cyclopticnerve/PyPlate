"""
docstring
"""

import os

DICT_BLACKLIST = {
    # skip header, skip text, skip path (0 0 0)
    # NB: this is mostly to speed up processing by not even looking at them
    "PP_SKIP_ALL": [
        ".git",
        ".venv",
        ".vscode",
        "docs",
        "misc",
        "README",
        "tests",
        "**/locale",
        "CHANGELOG.md",
        "LICENSE.txt",
        "requirements.txt",
        "__pycache__",
        "ABOUT",
    ],
}


for root, dirs, files in os.walk("."):
    # dirs[:] = [item for item in dirs if item not in DICT_BLACKLIST["PP_SKIP_ALL"]]
    # files[:] = [item for item in files if item not in DICT_BLACKLIST["PP_SKIP_ALL"]]
    print("root:", root)
    print("dirs:", dirs)
    print("files:", files)
    print("----------")
