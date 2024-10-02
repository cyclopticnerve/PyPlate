
# global imports
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# src = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, src)

# local imports

# 1
# from package.module import class
from installerator.installerator import Uninstallerator # noqa E402 (ignore import order)

# 2
# import installerator # noqa E402 (ignore import order)

dict_user = {
    "general": {
        "name": "SpaceOddity"
    },
    "preflight": [
        "${HOME}/.spaceoddity/cron_uninstall.py"
    ],
    "dirs": [
        "${HOME}/.spaceoddity",
        "${HOME}/.config/spaceoddity"
    ]
}
# ------------------------------------------------------------------------------
# Run the main class if we are not an import
# ------------------------------------------------------------------------------
if __name__ == '__main__':

    # create an instance of the class
    uninst = Uninstallerator()

    # # run the instance
    uninst.run(dict_user)
