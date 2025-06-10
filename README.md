<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

<!-- make a pretty header -->
# ** PyPlate **
## "It mostly works" ™©®

[![License: WTFPLv2](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net)

<!-- __RM_SHORT_DESC__ -->
A program for creating and building CLI/Package/GUI projects in Python from a template
<!-- __RM_SHORT_DESC__ -->

<!-- __RM_VERSION__ -->
Version 0.0.1+20250510.11
<!-- __RM_VERSION__ -->

<!-- [![alt-text](readme/screenshot.png)]("tooltip") -->

## Table of Contents
- [Requirements](#requirements)
- [Installing](#installing)
- [Uninstalling](#uninstalling)
- [Usage](#usage)
- [Notes](#notes)

## Requirements
<!-- __RM_DEPS__ -->
[Python 3.10+](https://python.org)
<!-- __RM_DEPS__ -->

## Installing
<!-- __RM_APP__ -->
You can download the (hopefully stable)
[latest release](https://github.com/cyclopticnerve/PyPlate/releases/latest)
from the main branch.<br>
Download either the 'tar.gz' or '.zip' file and extract it.

Then install it:
```bash
foo@bar:~$ cd ~/Downloads/PyPlate-<version>/dist
foo@bar:~/Downloads/PyPlate-<version>/dist$ ./install.py
```

Or you can clone the git repo to get the latest (and often broken) code from
the dev branch:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
foo@bar:~/Downloads$ cd PyPlate-<version>/dist
foo@bar:~/Documents/Downloads/PyPlate-<version>$ ./install.py
```
<!-- __RM_APP__ -->

## Uninstalling
<!-- __RM_APP__ -->
Go to the source folder for PyPlate and run the uninstaller:
```bash
foo@bar:~$ cd ~/.local/share/pyplate/uninstall
foo@bar:~/.local/share/pyplate/uninstall$ ./uninstall.py
```
<!-- __RM_APP__ -->

## Usage
PyPlate consists of two main programs, 'pymaker' and 'pybaker'. The first
is used to create the project, and the second is used to build an existing
project as its development continues.

Let us start with 'pymaker'.

## PyMaker - create the project
Before you do anything, you should take a look at the 'pyplate.py' file in
'~/.local/share/pyplate/conf'. This file contains A LOT of information that is
used when creating/building a project. Most of these are string values and
file/folder names used in the program, which you are free to change. PyPlate
does not yet support i18n/l10n, but that may be included at a later date.  

This file also contains some functions that are run at various times during
creating/building the project, such as before/after creating a project,
before/after building a project, etc.
These functions have been extended to the config file so you don't have to do a
lot of mucking around in the source code, but be sure to take a look at those
too.

Now run the script from the command line, in the directory where you want to
create the project:
```bash
foo@bar:~$: cd Documents/Projects/Python
foo@bar:~/Documents/Projects/Python$ pymaker
```

Enter the required information, and 'pymaker' will create the required files
and folders in a subdirectory of the current directory. 

That's it! From there you are free to modify the projects in your favorite IDE.

## PyBaker - Build the project
Once you have created a project, you can use 'pybaker' in the project's
directory to update metadata in the project's files and create a
'dist' folder.
If you are using VSCode, you can select 'Terminal/Run Build Task...' from the
menu bar or press 'Ctrl+Shift+B'.

'pybaker' is a program which will replace certain values in the project
directory. These values are read/written in the 'project.json' file in your
project's 'pyplate/project.json' file. Things like version number, short
description, and other values that might change during a project's lifecycle
are placed here.

The values in the 'pyplate/project.json' file can be edited at any time,
followed by re-running 'pybaker'.

Note that if you are running pybaker from VSCode, it will ask for the name of
the project (since it may not know the current directory). Give it the name of
the project's directory as it was created by pymaker, relative to the current
dir in VSCode's terminal.

## Notes
If you make any changes to this template to better suit your own style/setup,
please let me know or send a pull request. I will take a look and see if I can
incorporate your changes to make them user, system, and/or IDE agnostic. This
way the template can hopefully become more customizable to suit everyone's
needs.

PyPlate currently uses pdoc3 for documentation, mostly because it is easy and
sphinx is HARD! I don't really want to learn RST, and the Markdown/MyST stuff
is confusing. So for now, if you create docs for your project, and you are
using an icon in said docs, you may need to adjust the path to that icon in all
your HTML files. YMMV.

-)
<!-- -) -->
