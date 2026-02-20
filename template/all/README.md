<!----------------------------------------------------------------------------->
<!-- Project : __PP_NAME_PRJ_BIG__                             /          \  -->
<!-- Filename: __PP_README_FILE__                             |     ()     | -->
<!-- Date    : __PP_DATE__                                    |            | -->
<!-- Author  : __PP_AUTHOR__                                  |   \____/   | -->
<!-- License : __PP_LICENSE_NAME__                             \          /  -->
<!----------------------------------------------------------------------------->

# ![Logo](__PP_DIR_IMAGES__/__PP_NAME_PRJ_SMALL__.png) __PP_NAME_PRJ_BIG__

## "It mostly works" ™©®

__PP_RM_LICENSE__

<!-- __RM_SHORT_DESC__ -->
<!-- __RM_SHORT_DESC__ -->

<!-- __RM_VERSION__ -->
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
- [Developing](#developing)
- [Notes](#notes)

## Requirements
<!-- __RM_DEPS__ -->
[Python 3.10+](https://python.org)
<!-- __RM_DEPS__ -->

## Downloading

There are two ways to get the code:

1. Download the [latest
release](https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__/releases/latest)
(the **'__PP_NAME_PRJ_SMALL__-\<version\>.zip'** file should work on all platforms).

2. Or you can clone the git repo to get the latest (and often broken) code from
   the main branch:
```bash
$ git clone https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__
```

## Installing
<!-- __RM_PKG__ -->
There are also two ways to get __PP_NAME_PRJ_BIG__ into your project.<br>
Run these commands from your project directory.

First make sure you have a venv and it is active:
```bash
$  python -m venv .venv
$ . .venv/bin/activate
```

### Manually

If you downloaded the zip file:
```bash
$ python -m pip install /path/to/__PP_NAME_PRJ_SMALL__-<version>.zip
```

Or if you cloned the repo:
```bash
$ python -m pip install /path/to/__PP_NAME_PRJ_BIG__
```

### Automagically
Add this line to your project's 'requirements.txt' file:
```bash
__PP_NAME_PRJ_BIG__ @ git+https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__@<tag>
```
where \<tag\> is the tag you want, such as 'v0.0.1', etc.

Then run:
```
$ python -m pip install -r requirements.txt
```
<!-- __RM_PKG__ -->
<!-- __RM_APP__ -->
If you downloaded the zip file, extract it and go to the main directory:
```bash
$ cd ~/Downloads/__PP_NAME_PRJ_SMALL__-<version>
```
where \<version\> is the version number of the file you downloaded.

If you cloned the repo, just go to the 'install' directory:
```bash
$ cd ~/Downloads/__PP_NAME_PRJ_BIG__/install
```

Either way, run the install script:
```bash
$ ./install.py
```
<!-- __RM_APP__ -->

## Usage
Read the full [documentation](https://__PP_AUTHOR__.github.io/__PP_NAME_PRJ_BIG__).

## Uninstalling
<!-- __RM_PKG__ -->
In your project folder:
```bash
$ . .venv/bin/activate
$ python -m pip uninstall __PP_NAME_PRJ_SMALL__
```
<!-- __RM_PKG__ -->
<!-- __RM_APP__ -->
Just type the program name and use the '--uninstall' option:
```bash
$ __PP_NAME_PRJ_SMALL__ --uninstall
```
<!-- __RM_APP__ -->

## Documentation
See the full [documentation](https://__PP_AUTHOR__.github.io/__PP_NAME_PRJ_BIG__).

## Developing
If you are developing this project, make sure you run the "develop.py" script
first to create the proper virtual environment and install the requirements (if
any). 

## Notes
10/10, no notes.

-)
<!-- -) -->
