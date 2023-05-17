'metadata' will be edited by the user through 'conf/metadata.json'

the following caveats apply to 'metadata':

PP_VERSION

this is the canonical (only and absolute) version number string for
this project this should provide the absolute version number string (in semantic
notation) of this project, and all other version numbers should be superseded by
this string

PP_SHORT_DESC

this is the short description of the project, used in README.md
and pyproject.toml

PP_KEYWORDS

these are the keywords for the project, for use in pyproject.toml
for the PyPI listing, and should also be used in the GitHub project page
delimiters for all entries MUST be common

PP_PY_DEPS

these are the python dependencies for the project they are stored
here for install.py, pyproject.toml, and README.md it is a dictionary where the
key is the dep name, and the value is a link to the download page (for README)
when used in pyproject.toml or install.py, it will be automatically downloaded
from PyPI by pip using just the name

PP_SYS_DEPS

these are the system dependencies for the project they are stored
here for install.py delimiters for all entries MUST be comma

PP_GUI_CATEGORIES

categories must match a set of known values??? 
https://specifications.freedesktop.org/menu-spec/latest/apa.html
still working on this, for now categories are ignored

PP_GUI_EXEC
PP_GUI_ICON
this is mostly for
desktops that use a windows-style menu/submenu, not for Ubuntu-style overviews,
and will be used in the __PP_NAME_BIG__.desktop file gui categories MUST be
separated by a comma if exec/icon paths are not absolute, they will be found in
standard paths these paths vary, but I will add them here in the comments when I
figure them out