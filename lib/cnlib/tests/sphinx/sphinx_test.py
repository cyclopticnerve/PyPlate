"""
docstring
"""

from pathlib import Path
import shutil
import sys

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

P_DIR_LIB = Path(__file__).parents[3].resolve()
sys.path.append(str(P_DIR_LIB))

from cnlib import cnsphinx  # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error

dir_prj = Path(__file__).parent.resolve()
dir_src = Path(dir_prj / "src")
dirs_import = [
    Path(dir_prj / "../../../../lib").resolve()
]
dir_docs = dir_prj / "docs"
if dir_docs.exists():
    shutil.rmtree(dir_docs)
Path.mkdir(dir_docs, parents=True)

NAME = "__PP_NAME_SMALL__"
AUTHOR = "__PP_AUTHOR__"
VERSION = "__PP_VERSION__"
REVISION = "0.0.0"

THEME_NAME = "sphinx_rtd_theme"

dir_venv = dir_prj / ".venv"

CS = cnsphinx.CNSphinx(dir_prj, dir_src, dir_docs)
CS.create(NAME, AUTHOR, VERSION, REVISION, dirs_import, THEME_NAME)
CS.build(dir_venv)
