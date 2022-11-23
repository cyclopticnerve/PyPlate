<!----------------------------------------------------------------------------->
<!-- Project :                                                 /          \  -->
<!-- Filename: README.md                                      |     ()     | -->
<!-- Date    :                                                |            | -->
<!-- Author  : cyclopticnerve                                 |   \____/   | -->
<!-- License : WTFPLv2                                         \          /  -->
<!----------------------------------------------------------------------------->

# Project_Name

## "It mostly works™"

[![License: WTFPL](https://img.shields.io/badge/License-WTFPL-brightgreen.svg)](http://www.wtfpl.net/about/)

<Description>

![](readme/readme_ss.jpg)

## Requirements

## Installing

You should first run:

```bash
foo@bar:~$ sudo apt update && sudo apt upgrade
```

to make sure you have the lastest software installed.

<-- pacakge/module -->
You can download the (hopefully stable) 
[latest release](https://github.com/cyclopticnerve/<Project_Name>/releases/latest) 
from the main branch. <br>
Download the Source Code (tar.gz) file. <br>
Then install it using:

```bash
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ python -m pip install <Project_Name>-X.X.X.tar.gz
```

Or you can clone the git repo to get the latest (and often broken) code 
from the dev branch:

```bash
foo@bar:~$ python -m pip install build
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/<Project_Name>
foo@bar:~/Downloads$ cd <Project_Name>
foo@bar:~/Downloads/<Project_Name>$ python -m build
foo@bar:~/Downloads/<Project_Name>$ python -m pip install ./dist/<Project_Name>-X.X.X.tar.gz -r ./requirements.txt
```

<-- application -->
You can download the (hopefully stable)
[latest release](https://github.com/cyclopticnerve/<Program_Name>/releases/latest) 
from the main branch, unzip it, and run the *install.py* file from there:

```bash
foo@bar:~$ cd Downloads/<Program_Name>-X.X.X
foo@bar:~/Downloads/<Program_Name>-X.X.X$ ./install.py
```

Or you can clone the git repo to get the latest (and often broken) code 
from the dev branch:

```bash
foo@bar:~$ python -m pip install build
foo@bar:~$ cd Downloads
foo@bar:~/Downloads$ git clone https://github.com/cyclopticnerve/<Program_Name>
foo@bar:~/Downloads$ cd <Program_Name>
foo@bar:~/Downloads/Program_Name$ ./install.py

## Uninstalling

<-- package/module -->
```python
python -m pip uninstall <project_name>
```

<-- application -->
```bash
foo@bar:~$ cd .<program_name>
foo@bar:~/.<program_name>$ ./uninstall.py
## Usage

## Notes

## -)

