"""
An example of how to add cnlibs to your script
"""

# TODO: pybaker replace paths to lib

# system imports
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# find paths to dev or user
# TODO: make sure the parent name is right
DIR_PARENT = Path(__file__).parent
if DIR_PARENT.name == "__PD_DEV_SRC__":
    DIR_LIB = Path.home() / "__PC_DEV_LIB__"
else:
    DIR_LIB = Path.home() / "__PC_USR_LIB__"

# add lib path to import search
sys.path.append(str(DIR_LIB))

from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------

d = {"foo": "bar,"}
F.pp(d, label="test")
