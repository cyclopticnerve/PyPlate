<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# PyPlate

## "It mostly works™"

[![License: WTFPLv2](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

A program for creating CLI/Package/GUI projects in Python from a template

## Requirements
[Python 3.10+](https://www.python.org/)

## Installing
1. Download the (hopefully stable) [latest
release](https://github.com/cyclopticnerve/PyPlate/releases/latest) from the
main branch. Select  either the 'tar.gz' or 'zip' file
2. Extract/unzip the file.
3. Go into the extracted folder and run the installer:
```bash
foo@bar:~/Documents/Downloads/PyPlate-<version>$ ./install.sh
```

Or you can clone the git repo to get the latest (and often broken) code from
the dev branch:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
foo@bar:~/Downloads$ cd ~/Documents/Downloads/PyPlate-<version>
foo@bar:~/Documents/Downloads/PyPlate-<version>$ ./install.sh
```

## Uninstalling
Go to the config folder for PyPlate and run the uninstaller:
```bash
foo@bar:~$ cd ~/.config/pyplate/conf
foo@bar:~/.config/pyplate/conf$ ./uninstall.sh
```

## Usage
PyPlate consists of two main scripts, 'pymaker.py' and 'pybaker.py'. The first
is used to create the project, and the second is used to update an existing
project as its development continues.

Let us start with 'pymaker.py'.

## PyMaker.py
Before you do anything, you should take a look at the 'pyplate_conf.py' file in
'~/.config/pyplate/conf'. This file contains A LOT of information that is used
when creating/building a project. Most of these are string values and
file/folder names used in the program, which you are free to change. PyPlate
does not yet support i18n/l10n, but that may be included at a later date.  
In the future, the installer will ask you for this information, so you only
have to enter it at install time.

### One important thing to note:  
By default, PyPlate will create it's projects in '~/Documents/Projects/Python'.
To change this, edit this value in ~/.conf/pyplate/conf/pyplate_conf.py:

```python
S_BASE_DIR = "~/Documents/Projects/Python"
```
Again, this is a feature which should be handled by the installer, and I am
working on it.

This file also contains some functions that are run at various times during
creating/building the project, such as before copying files, after copying
files, etc.
These functions have been extended to the config file so you don't have to do a
lot of mucking around in the source code, so be sure to take a look at those too.

Now run the script from the command line:
```bash
foo@bar:~$ pymaker.py
```

Enter the required information, and 'pymaker.py' will create the required files
and folders in a subdirectory of 'S_BASE_DIR'. The project will eventually be
created in 'S_BASE_DIR/TYPE/PRJ_NAME', where:
1. 'S_BASE_DIR' is the base directory (as explained above)
2. 'TYPE' is the type of project 
   * 'CLIs' for a command line program
   * 'PKGs' for a package
   * 'GUIs' for a GTK3/4 application
3. 'PRJ_NAME' as the project name entered when creating the project

So, from all of our assumptions above, if the project type is 'c', and the
project name is 'CLI_Test', then the project will be created in
'~/Documents/Projects/Python/CLIs/CLI_Test'.

That's it! From there you are free to modify the projects in your favorite IDE.

## PyBaker.py / Updating the project
Once you have created a project, you can use 'pybaker.sh' in the project's
'pyplate' directory to update metadata in the project's files and create a
'dist' folder.
If you are using VSCode, you can select 'Terminal/Run Build Task...' from the
menu bar or press 'Ctrl+Shift+B'.

'pybaker.py' is a script which will replace certain values in the project
directory. These values are placed in the 'project.json' file in your
project's 'pyplate/project.json' file. Things like version number, short
description, and other values that might change during a project's lifecycle
are placed here.

The values in the ''pyplate/project.json' file can be edited at any time,
followed by re-running 'pybaker.py'.

Note that pybaer.py has one required parameter: the directory of the project
you wish to bake:
```bash
foo@bar:~$ pybaker.py ~/Documents/Projects/Python/MyApp
```
but this should be easy to do with any tool you use.  
When using VSCode, this is done for you.,

## Notes
If you make any changes to this template to better suit your own style/setup,
please let me know or send a pull request. I will take a look and see if I can
incorporate your changes to make them user-agnostic. This way the template can
hopefully become more customizable to suit everyone's needs.

## -)
<!-- -) -->
