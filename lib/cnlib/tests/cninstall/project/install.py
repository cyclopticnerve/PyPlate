"""
docstring
"""

from pathlib import Path
import sys

PATH_LIB = Path(__file__).parents[1].resolve()
sys.path.append(str(PATH_LIB))

# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=no-name-in-module
# pylint: disable=import-error

from cninstall import cnbaseinstall # type: ignore

# pylint: enable=wrong-import-position
# pylint: enable=wrong-import-order
# pylint: enable=no-name-in-module
# pylint: enable=import-error
