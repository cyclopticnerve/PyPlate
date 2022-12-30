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

You can download the (hopefully stable)
[latest release](https://github.com/cyclopticnerve/PyPlate/releases/latest) 
from the main branch.<br>
Download either the 'tar.gz' or '.zip' file and extract it.<br>

Or you can clone the git repo to get the latest (and often broken) code 
from the dev branch:

```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/PyPlate
```

Next, cut/copy/paste/cp/mv the PyPlate directory wherever you want. For the 
example below, we will use "~/Documents/Projects/Python/".
```bash
foo@bar:~/Downloads$ cp PyPlate ~/Documents/Projects/Python
```

Lastly, you can delete the downloaded folder.

## Uninstalling

Just delete the PyPlate folder from wherever you put it in the install step.

## Usage

First, cd into the PyPlate folder, then run pymaker.py:

``` bash
foo@bar:~$ cd Documents/Projects/Python/PyPlate
foo@bar:~/Documents/Projects/Python/PyPlate$ ./pymaker.py
```

Enter the required information, and PyMaker will create the required files and 
folders in a subdirectory of "~/Documents/Projects/Python/" based on your 
entries.

## Notes

Note that the project path is one above the PyPlate dir, and one down based on 
the type of template you create.<br>
So, using the install path above, modules and packages will be placed in 
"~/Documents/Projects/Python/Libs/", and CLI/GUI projects will be placed 
in "~/Documents/Projects/Python/Apps".<br>
From there you are free to modify the projects in your favorite IDE.

In a future release, the base path will be configurable, so that it is 
independent of where the PyPlate directory is located.

## -)
<!-- -) -->
