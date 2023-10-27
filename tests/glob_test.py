"""
docstring
"""

from pathlib import Path

PATH = Path.home() / "Documents/Projects/Python/PyPlate/tests/"
GLOB = str("glob_test.py")

lst = list(PATH.glob(GLOB))
print(lst)
