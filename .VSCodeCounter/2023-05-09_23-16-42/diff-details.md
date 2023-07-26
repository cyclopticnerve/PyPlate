# Diff Details

Date : 2023-05-09 23:16:42

Directory /home/dana/Documents/Projects/Python/PyPlate

Total : 42 files,  47 codes, 16 comments, 33 blanks, all 96 lines

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [CHANGELOG.md](/CHANGELOG.md) | Markdown | 0 | 0 | 1 | 1 |
| [conf/metadata.py](/conf/metadata.py) | Python | 36 | -15 | 8 | 29 |
| [requirements.txt](/requirements.txt) | pip requirements | 2 | 0 | 0 | 2 |
| [src/pyplate.py](/src/pyplate.py) | Python | -23 | 2 | -3 | -24 |
| [template/README.md](/template/README.md) | Markdown | -59 | -21 | -14 | -94 |
| [template/cli/src/__PP_NAME_SMALL__.py](/template/cli/src/__PP_NAME_SMALL__.py) | Python | 18 | 100 | 30 | 148 |
| [template/common/CHANGELOG.md](/template/common/CHANGELOG.md) | Markdown | 0 | 0 | 1 | 1 |
| [template/common/README.md](/template/common/README.md) | Markdown | 59 | 21 | 14 | 94 |
| [template/common/conf/blacklist.json](/template/common/conf/blacklist.json) | JSON | 0 | 0 | 1 | 1 |
| [template/common/conf/metadata.json](/template/common/conf/metadata.json) | JSON | 10 | 0 | 0 | 10 |
| [template/common/conf/metadata.py](/template/common/conf/metadata.py) | Python | 466 | 330 | 180 | 976 |
| [template/common/conf/settings.json](/template/common/conf/settings.json) | JSON with Comments | 0 | 0 | 1 | 1 |
| [template/common/misc/empty_class.py](/template/common/misc/empty_class.py) | Python | 8 | 79 | 18 | 105 |
| [template/common/misc/empty_cli.py](/template/common/misc/empty_cli.py) | Python | 18 | 100 | 30 | 148 |
| [template/common/misc/empty_mod.py](/template/common/misc/empty_mod.py) | Python | 5 | 57 | 13 | 75 |
| [template/common/requirements.txt](/template/common/requirements.txt) | pip requirements | 0 | 0 | 1 | 1 |
| [template/conf/blacklist.json](/template/conf/blacklist.json) | JSON | 0 | 0 | -1 | -1 |
| [template/conf/metadata.json](/template/conf/metadata.json) | JSON | -10 | 0 | 0 | -10 |
| [template/conf/metadata.py](/template/conf/metadata.py) | Python | -423 | -309 | -159 | -891 |
| [template/conf/settings.json](/template/conf/settings.json) | JSON with Comments | 0 | 0 | -1 | -1 |
| [template/gui/src/__PP_NAME_BIG__.desktop](/template/gui/src/__PP_NAME_BIG__.desktop) | Desktop | 12 | 8 | 3 | 23 |
| [template/gui/src/__PP_NAME_SMALL__-handler.py](/template/gui/src/__PP_NAME_SMALL__-handler.py) | Python | 19 | 90 | 24 | 133 |
| [template/gui/src/__PP_NAME_SMALL__.py](/template/gui/src/__PP_NAME_SMALL__.py) | Python | 25 | 105 | 34 | 164 |
| [template/misc/empty_class.py](/template/misc/empty_class.py) | Python | -8 | -79 | -18 | -105 |
| [template/misc/empty_cli.py](/template/misc/empty_cli.py) | Python | -18 | -100 | -30 | -148 |
| [template/misc/empty_mod.py](/template/misc/empty_mod.py) | Python | -5 | -57 | -13 | -75 |
| [template/mod/pyproject.toml](/template/mod/pyproject.toml) | TOML | 21 | 8 | 5 | 34 |
| [template/mod/src/__PP_NAME_SMALL__.py](/template/mod/src/__PP_NAME_SMALL__.py) | Python | 5 | 57 | 13 | 75 |
| [template/pkg/pyproject.toml](/template/pkg/pyproject.toml) | TOML | 21 | 8 | 5 | 34 |
| [template/pkg/src/__PP_NAME_SMALL__/__init__.py](/template/pkg/src/__PP_NAME_SMALL__/__init__.py) | Python | 3 | 13 | 4 | 20 |
| [template/pkg/src/__PP_NAME_SMALL__/mod_name_1.py](/template/pkg/src/__PP_NAME_SMALL__/mod_name_1.py) | Python | 5 | 57 | 13 | 75 |
| [template/pkg/src/__PP_NAME_SMALL__/mod_name_2.py](/template/pkg/src/__PP_NAME_SMALL__/mod_name_2.py) | Python | 5 | 57 | 13 | 75 |
| [template/pyproject.toml](/template/pyproject.toml) | TOML | -21 | -8 | -5 | -34 |
| [template/requirements.txt](/template/requirements.txt) | pip requirements | -32 | 0 | -1 | -33 |
| [template/src/__PP_NAME_SMALL__.cli.py](/template/src/__PP_NAME_SMALL__.cli.py) | Python | -18 | -100 | -30 | -148 |
| [template/src/__PP_NAME_SMALL__.gui.py](/template/src/__PP_NAME_SMALL__.gui.py) | Python | -25 | -105 | -34 | -164 |
| [template/src/__PP_NAME_SMALL__.gui/__PP_NAME_BIG__.desktop](/template/src/__PP_NAME_SMALL__.gui/__PP_NAME_BIG__.desktop) | Desktop | -12 | -8 | -3 | -23 |
| [template/src/__PP_NAME_SMALL__.gui/__PP_NAME_BIG__Handler.py](/template/src/__PP_NAME_SMALL__.gui/__PP_NAME_BIG__Handler.py) | Python | -19 | -90 | -24 | -133 |
| [template/src/__PP_NAME_SMALL__.mod.py](/template/src/__PP_NAME_SMALL__.mod.py) | Python | -5 | -57 | -13 | -75 |
| [template/src/__PP_NAME_SMALL__.pkg/__init__.py](/template/src/__PP_NAME_SMALL__.pkg/__init__.py) | Python | -3 | -13 | -4 | -20 |
| [template/src/__PP_NAME_SMALL__.pkg/mod_name_1.py](/template/src/__PP_NAME_SMALL__.pkg/mod_name_1.py) | Python | -5 | -57 | -13 | -75 |
| [template/src/__PP_NAME_SMALL__.pkg/mod_name_2.py](/template/src/__PP_NAME_SMALL__.pkg/mod_name_2.py) | Python | -5 | -57 | -13 | -75 |

[Summary](results.md) / [Details](details.md) / [Diff Summary](diff.md) / Diff Details