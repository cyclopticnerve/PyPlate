"""
docstring
"""

# from pathlib import Path
import glob

# PATH = "/home/dana/Documents/Projects/Python/Packages/Pkg_Test/"
GLOB = str("**/glob_test_folder*")

# lst = list(PATH.glob(GLOB))
lst = glob.glob(GLOB)
print(lst)
