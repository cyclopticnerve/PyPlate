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

A template for creating packages/modules/CLI apps/GTK3 apps in Python

## Requirements

None

## Installing

You should first run:

```bash
foo@bar:~$ sudo apt update && sudo apt upgrade
```

to make sure you have the lastest software installed.

1. You can download the (hopefully stable)
[latest release](https://github.com/cyclopticnerve/PyPlate/releases/latest) 
from the main branch.<br>
Download either the 'tar.gz' or '.zip' file and extract it.<br>

2. Or you can clone the git repo to get the latest (and often broken) code 
from the dev branch:

```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
```


3. Then copy/paste the PyPlate directory wherever you want it. A good suggestion is 
~/Documents/Projects/Python/Tools.

Then you can delete the downloaded folder.

## Uninstalling

Just delete the PyPlate folder from wherever you put it in install.

## Usage

First, cd into the PyPlate folder, then run pymaker.py:

``` bash
foo@bar:~$ cd Documents/Projects/Python/Tools/PyPlate
foo@bar:~/Documents/Projects/Python/Tools/PyPlate$ ./pymaker.py
```

Enter the required information, and PyMaker will create the required files and 
folders in a subdirectory of ~/Documents/Projects/Python based on your entries.<br>

Note that this path is one above the install dir, and one down based on the type
of template you create.
Modules and packages will be placed in a 'Libs' folder, and CLI/GUI projects 
will be placed in an 'Apps' folder, RELATIVE to the PyPlate folder.<br>
From there you are free to modify the projects in your favorite IDE.

## Notes

## -)
<!-- -) -->
