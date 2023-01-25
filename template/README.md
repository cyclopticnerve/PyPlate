<!----------------------------------------------------------------------------->
<!-- Project : __CN_BIG_NAME__                                 /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : __CN_DATE__                                    |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# __CN_BIG_NAME__

<!-- Tagline, common to all projects-->
## "It mostly works™"

<!-- License badge, common to all projects -->
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

<!-- __CN_SHORT_DESC_START__ -->
__CN_SHORT_DESC__
<!-- __CN_SHORT_DESC_END__ -->

<!-- Screenshot, common to all projects -->
<!-- ![Screenshot](misc/screenshot.jpg) -->

## Requirements
<!-- __CN_MOD_START__ -->
<!-- __CN_PY_DEPS__ -->
<!-- __CN_MOD_END__ -->
<!-- __CN_APP_START__ -->
This application requires:

[Configurator](https://github.com/cyclopticnerve/Configurator)<br>
[Installerator](https://github.com/cyclopticnerve/Installerator)<br>
<!-- __CN_PY_DEPS__ -->
<!-- __CN_APP_END__ -->

## Installing
You should first run:
```bash
foo@bar:~$ sudo apt update && sudo apt upgrade
```
to make sure you have the lastest software installed.

<!-- __CN_MOD_START__ -->
You can download the (hopefully stable)
[latest release](https://github.com/__CN_AUTHOR__/__CN_BIG_NAME__/releases/latest)
from the main branch.<br>
Download the 'Source Code (tar.gz)' file.

Then install it using:
```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ python -m pip install __CN_BIG_NAME__-__CN_VERSION__.tar.gz
```
Or you can clone the git repo to get the latest (and often broken) code from the 
dev branch:
```bash
foo@bar:~$ python -m pip install build
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/__CN_AUTHOR__/__CN_BIG_NAME__
foo@bar:~/Downloads$ cd __CN_BIG_NAME__
foo@bar:~/Downloads/__CN_BIG_NAME__$ python -m build
foo@bar:~/Downloads/__CN_BIG_NAME__$ python -m pip install ./dist/__CN_SMALL_NAME__-__CN_VERSION__.tar.gz -r ./requirements.txt
```
<!-- __CN_MOD_END__ -->
<!-- __CN_APP_START__ -->
Make sure you've installed
[Configurator](https://github.com/cyclopticnerve/Configurator)
and
[Installerator](https://github.com/cyclopticnerve/Installerator).<br>
You can download the (hopefully stable)
[latest release](https://github.com/__CN_AUTHOR__/__CN_BIG_NAME__/releases/latest)
from the main branch.<br>
Download either the 'tar.gz' or '.zip' file and extract it.<br>
Then run the 'install.py' file from there:
```bash
foo@bar:~$ cd Downloads/__CN_BIG_NAME__-__CN_VERSION__
foo@bar:~/Downloads/__CN_BIG_NAME__-__CN_VERSION__$ ./install.py
```
Or you can clone the git repo to get the latest (and often broken) code from the
dev branch:
```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/__CN_AUTHOR__/__CN_BIG_NAME__
foo@bar:~/Downloads$ cd __CN_BIG_NAME__
foo@bar:~/Downloads/__CN_BIG_NAME__$ ./install.py
```
<!-- __CN_APP_END__ -->

## Uninstalling
<!-- __CN_MOD_START__ -->
```bash
foo@bar:~$ python -m pip uninstall __CN_SMALL_NAME__
```
<!-- __CN_MOD_END__ -->
<!-- __CN_APP_START__ -->
```bash
foo@bar:~$ cd .__CN_AUTHOR__/__CN_SMALL_NAME__
foo@bar:~/.__CN_AUTHOR__/__CN_SMALL_NAME__$ ./uninstall.py
```
<!-- __CN_APP_END__ -->

## Usage
blah blah blah

## Notes
blah blah blah

## -)
<!-- -) -->
