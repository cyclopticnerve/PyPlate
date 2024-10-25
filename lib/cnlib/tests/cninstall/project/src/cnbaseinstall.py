"""
docstring
"""

import shutil

class CNBaseInstall():
    """
    docstring
    """

    def __init__(self):
        """
        docstring
        """

    def create(self, list_assets, dir_assets):
        """
        docstring
        """
        # TODO: make list items into abs path objs
        # make sure dir_assets exists and is a dir and is abs or else need dir_prj
        for item in list_assets:
            if item.is_dir():
                shutil.copytree(item, dir_assets)
            elif item.is_file():
                shutil.copy(item, dir_assets)

    def install(self):
        """
        docstring
        """

    def uninstall(self):
        """
        docstring
        """

# -)
