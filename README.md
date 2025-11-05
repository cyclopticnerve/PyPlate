<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

![Logo](images/pyplate.png)
# PyPlate

## "It mostly works" ™©®

[![License: WTFPLv2](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net)

<!-- __RM_SHORT_DESC__ -->
A program for creating and building CLI/GUI/Packages in Python from a template
<!-- __RM_SHORT_DESC__ -->

<!-- __RM_VERSION__ -->
Version 0.0.6
<!-- __RM_VERSION__ -->

<!-- __RM_SCREENSHOT__ -->
<!-- __RM_SCREENSHOT__ -->

## Table of Contents
- [Requirements](#requirements)
- [Downloading](#downloading)
- [Installing](#installing)
- [Usage](#usage)
- [Uninstalling](#uninstalling)
- [Documentation](#documentation)
- [Notes](#notes)

## Requirements
<!-- __RM_DEPS__ -->
[Python 3.10+](https://python.org)
<!-- __RM_DEPS__ -->

## Downloading

There are two ways to get the code:

1. Download the [latest
release](https://github.com/cyclopticnerve/PyPlate/releases/latest) (the
**'Source code (zip)'** file should work an all platforms).

2. Or you can clone the git repo to get the latest (and often broken) code from
   the main branch:
```bash
$ git clone https://github.com/cyclopticnerve/PyPlate
```

## Installing
<!-- __RM_APP__ -->
If you downloaded the zip file, extract it and go to the 'install' directory:
```bash
$ cd ~/Downloads/PyPlate-<version>/install
```
where \<version\> is the version number of the file you downloaded.

If you cloned the repo, just go to the 'install' directory:
```bash
$ cd ~/Downloads/PyPlate/install
```

Either way, run the install script:
```bash
$ ./install.py
```
<!-- __RM_APP__ -->

## Usage
PyPlate consists of two main programs, 'pymaker' and 'pybaker'. The first
is used to create the project, and the second is used to build an existing
project as its development continues.

Let us start with 'pymaker'.

## PyMaker - Create the project
Before you do anything, you should take a look at the 'conf.py' file in
'~/.local/share/pyplate/conf'. This file contains A **LOT** of information that
is used when creating/building a project. Most of these are string values and
file/folder names used in the program, which you are free to change. PyPlate
does not yet support i18n/l10n for itself (meaning any strings in this file
will not be i18n'ed), but that may be included at a later date.  

This file also contains some functions that are run at various times during
creating/building the project, such as before/after creating a project,
before/after building a project, etc.
These functions have been extended to the config file so you don't have to do a
lot of mucking around in the source code, but be sure to take a look at those
too.

Now run the script from the command line, in the directory where you want to
create the project:
```bash
$ cd ~/Projects/Python
$ pymaker
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

## Documenting you project
You can document your project using either pdoc3 or MkDocs.

Step 1:
- Create your project using pymaker
- Publish your repo to GitHub

Step 2:
   - To use pdoc3, you have to:
      - Open you GitHub repo in a browser
      - Go to the repo's Settings/Pages
      - Set the source to your main branch / docs folder

   - To use MkDocs, you have to:
      - run 'pybaker' from your project directory

Wait a minute or two, and your docs should appear at
      https://\<username\>.github.io/\<repo_name\>

## Uninstalling
<!-- __RM_APP__ -->
Go to the source folder for PyPlate and run the uninstaller:
```bash
$ cd ~/.local/share/pyplate/uninstall
$ ./uninstall.py
```
<!-- __RM_APP__ -->

## Documentation
See the [documentation](https://cyclopticnerve.github.io/PyPlate)

## Notes
If you have any sort of spellchecker in your IDE, *FOR GOD'S SAKE TURN IT OFF!*
It would brick a fucking quantum computer. On the other hand, I'm about to use
an Oxford comma, so \\/ jog on.

If you make any changes to this template to better suit your own style/setup,
please let me know or send a pull request. I will take a look and see if I can
incorporate your changes to make them user, system, and/or IDE agnostic. This
way the template can hopefully become more customizable to suit everyone's
needs.

PyPlate currently uses [MkDocs](https://https://www.mkdocs.org/) for
documentation, because pdoc3 is TOO SIMPLE and sphinx is TOO COMPLEX!

-)
<!-- -) -->
