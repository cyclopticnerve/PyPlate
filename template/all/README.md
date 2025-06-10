<!----------------------------------------------------------------------------->
<!-- Project : __PP_NAME_PRJ_BIG__                             /          \  -->
<!-- Filename: __PP_README_FILE__                             |     ()     | -->
<!-- Date    : __PP_DATE__                                    |            | -->
<!-- Author  : __PP_AUTHOR__                                  |   \____/   | -->
<!-- License : __PP_LICENSE_NAME__                             \          /  -->
<!----------------------------------------------------------------------------->

!(images/__PP_NAME_PRJ_SMALL__.png)
# __PP_NAME_PRJ_BIG__

## "It mostly works" ™©®

__PP_RM_LICENSE__

<!-- __RM_SHORT_DESC__ -->
__PP_SHORT_DESC__
<!-- __RM_SHORT_DESC__ -->

<!-- __RM_VERSION__ -->
__PP_VER_DISP__
<!-- __RM_VERSION__ -->

<!-- ![alt-text](readme/screenshot.png) -->

## Table of Contents
- [Requirements](#requirements)
- [Installing](#installing)
- [Uninstalling](#uninstalling)
- [Usage](#usage)
- [Notes](#notes)

## Requirements
<!-- __RM_DEPS__ -->
__PP_PY_DEPS__
<!-- __RM_DEPS__ -->

## Installing
<!-- __RM_PKG__ -->
First, download the [latest release](https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__/releases/latest).
Download the 'tar.gz' file.

Then install it:
```bash
foo@bar:~$ cd ~/Downloads/__PP_NAME_PRJ_BIG__-<version>/dist
foo@bar:~/Downloads$ python -m pip install __PP_NAME_PRJ_BIG__-<version>.tar.gz
```
Or you can clone the git repo to get the latest (and often broken) code:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__
foo@bar:~/Downloads$ cd __PP_NAME_PRJ_BIG__-<version>
```
Then build and install it:
```bash
foo@bar:~/Downloads/__PP_NAME_PRJ_BIG__-<version>$ python -m pip install build
foo@bar:~/Downloads/__PP_NAME_PRJ_BIG__-<version>$ python -m build
foo@bar:~/Downloads/__PP_NAME_PRJ_BIG__-<version>$ python -m pip install ./dist/__PP_NAME_PRJ_SMALL__-<version>.tar.gz
```
<!-- __RM_PKG__ -->
<!-- __RM_APP__ -->
First, download the [latest release](https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__/releases/latest).
Download either the 'tar.gz' or '.zip' file and extract it.

Then install it:
```bash
foo@bar:~$ cd ~/Downloads/__PP_NAME_PRJ_BIG__-<version>/dist
foo@bar:~/Downloads/__PP_NAME_PRJ_BIG__-<version>/dist$ ./install.py
```

Or you can clone the git repo to get the latest (and often broken) code:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__
foo@bar:~/Downloads$ cd __PP_NAME_PRJ_BIG__-<version>/dist
foo@bar:~/Downloads/__PP_NAME_PRJ_BIG__-<version>$ ./install.py
```
<!-- __RM_APP__ -->

## Usage
blah blah blah

## Uninstalling
<!-- __RM_PKG__ -->
```bash
foo@bar:~$ python -m pip uninstall __PP_NAME_PRJ_SMALL__
```
<!-- __RM_PKG__ -->
<!-- __RM_APP__ -->
Go to the source folder for __PP_NAME_PRJ__ and run the uninstaller:
```bash
foo@bar:~$ cd ~/.local/share/__PP_NAME_PRJ_SMALL__/uninstall
foo@bar:~/.local/share/__PP_NAME_PRJ_SMALL__/uninstall$ ./uninstall.py
```
<!-- __RM_APP__ -->

## Notes
blah blah blah

-)
<!-- -) -->
