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

# find path to lib
P_DIR_PRJ = Path(__file__).parents[1].resolve()
P_DIR_LIB = P_DIR_PRJ / "lib"

# add lib path to import search
sys.path.append(str(P_DIR_LIB))

from cnlib import cnfunctions as F  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# ------------------------------------------------------------------------------

d = {"foo": "bar,"}
F.pp(d, label="test")
