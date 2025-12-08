"""
Docstring for tests.glob
"""

# ------------------------------------------------------------------------------

from pathlib import Path
from pprint import pp

# ------------------------------------------------------------------------------

dir_prj = Path(__file__).parents[1].resolve()
list_src = ["install", "src", "bin", "develop.py"]  # globs ok

# NB: NO GLOBS!!!
dict_clangs = {
    "Python": [
        ".py",
    ],
    "Glade": [".ui", ".glade"],
    "Desktop": [".desktop"],
}

dict_res = {}

# ------------------------------------------------------------------------------

for place in list_src:

    p_place = dir_prj / place
    if p_place.is_dir():

        for lang, exts in dict_clangs.items():  # Python, [".py"]
            list_clang = []
            for ext in exts:

                res = list(p_place.glob("**/*" + ext))

                list_clang.extend(res)

            list_clang = [str(item) for item in list_clang]
            list_old = dict_res.get(lang, [])
            list_old.extend(list_clang)
            dict_res[lang] = list_old

    else:

        ext_place = p_place.suffix

        # find lang from suffix
        for lang, exts in dict_clangs.items():  # Python, [".py"]
            if ext_place in exts:

                list_old = dict_res.get(lang, [])
                list_old.extend([str(p_place)])
                dict_res[lang] = list_old

                break

pp(dict_res)
