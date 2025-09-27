from pathlib import Path

p_dist = Path(__file__).parent.resolve()


L_DIST_REMOVE_EXT = [
    "bin/__PP_NAME_PRJ_SMALL__.py",
    "install/install.py",
    "install/uninstall.py",
]

# for each file name to purge
for item in L_DIST_REMOVE_EXT:

    # glob it
    lst = list(p_dist.rglob(item))

    # for each item in glob, remove dir or file
    for item2 in lst:
        if item2.is_file():
            item2.rename(Path(item2.parent, item2.stem))
            # print(item2, item2.stem)
