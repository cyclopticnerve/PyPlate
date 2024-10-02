"""
docstring
"""

# system imports
from pathlib import Path
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

DIR_SELF = Path(__file__).parent.resolve()
DIR_ASSETS = DIR_SELF / "assets"

P_DIR_LIB = Path(__file__).parents[2].resolve()
sys.path.append(str(P_DIR_LIB))

# local imports
from cninstall.cninstaller import CNInstaller # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

# the user dict
dict_user = {
    "meta": {
        "name": "SpaceOddity",
        "version": "0.0.1"
    },
    # "preflight": [],
    # "sys_reqs": [],
    # "py_reqs": [],
    "content": {
        "conf": ".conf/spaceoddity",
        "spaceoddity.py": ".spaceoddity",
        "LICENSE": ".spaceoddity",
        "VERSION": ".spaceoddity",
        "uninstall.py": ".spaceoddity",
        "uninstall.json": ".spaceoddity",
        "cron_uninstall.py": ".config/.spaceoddity",
    },
    # "postflight":[]
}

# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # create an instance of the class
    inst = CNInstaller(DIR_ASSETS, debug=True)

    # # run the instance
    inst.run_dict(dict_user)
