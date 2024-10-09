"""
An example of how to add cnlibs to your script
"""

# system imports
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=no-name-in-module
# pylint: disable=import-error

# my imports
# add custom import paths

# find paths to dev or user
DIR_PARENT = Path(__file__).parent.resolve()
if DIR_PARENT.name == "__PP_DEV_SRC__":
    DIR_LIB = Path.home() / "__PP_DEV_PP__" / "lib"
else:
    DIR_LIB = Path.home() / "__PP_USR_LIB__"

# add lib path to import search
sys.path.append(str(DIR_LIB))

from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------

d = {"foo": "bar,"}
F.pp(d, label="test")
