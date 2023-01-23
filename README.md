<!----------------------------------------------------------------------------->
<!-- Project : PyPlate                                         /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    : 12/19/2022                                     |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# PyPlate

## "It mostly works™"
[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

A template for creating modules/packages/CLI apps/GTK3 apps in Python

## Requirements
None

## Installing
You should first run:
```bash
foo@bar:~$ sudo apt update && sudo apt upgrade
```
to make sure you have the lastest software installed.

You can download the (hopefully stable)
[latest release](https://github.com/cyclopticnerve/PyPlate/releases/latest) 
from the main branch.<br>
Download either the 'tar.gz' or '.zip' file and extract it.

Or you can clone the git repo to get the latest (and often broken) code 
from the dev branch:
```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
```
Next, cut/copy/paste/cp/mv the 'PyPlate' directory wherever you want. For all 
examples below, we will use '~/Documents/Projects/Python/'.
```bash
foo@bar:~/Downloads$ cp PyPlate ~/Documents/Projects/Python
```

Lastly, you can delete the downloaded folder, if you copied it.

## Uninstalling
Just delete the 'PyPlate' folder from wherever you put it in the install step.

## Usage
To create a project, cd into the 'PyPlate/src/' directory, and run 'pymaker.py':
``` bash
foo@bar:~$ cd Documents/Projects/Python/PyPlate/src
foo@bar:~/Documents/Projects/Python/PyPlate/src$ ./pymaker.py
```

Enter the required information, and 'pymaker.py' will create the required files 
and folders in a subdirectory of 'BASE_DIR/SUB_DIR'.

From there you are free to modify the projects in your favorite IDE.

## Notes

If you make any changes to this template to better suit your own style/setup, 
please let me know or send a pull request. I will take a look and see if I can 
incorporate your changes to make them user-agnostic. This way the template can 
hopefully become more customizable to suit everyone's needs.

## -)
<!-- -) -->
