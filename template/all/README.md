<!----------------------------------------------------------------------------->
<!-- Project : __PP_NAME_PRJ_BIG__                             /          \  -->
<!-- Filename: __PP_README_FILE__                             |     ()     | -->
<!-- Date    : __PP_DATE__                                    |            | -->
<!-- Author  : __PP_AUTHOR__                                  |   \____/   | -->
<!-- License : __PP_LICENSE_NAME__                             \          /  -->
<!----------------------------------------------------------------------------->

<!-- make a pretty header -->
<table>
    <tr>
        <td>
            <img style="display:flex;" src="__PP_IMG_README__" />
        </td>
        <td>
            <span style="font-size:300%;font-weight:bold;">__PP_NAME_PRJ_BIG__</span>
        </td>
    </tr>
</table>

## "It mostly works ™©®"

__PP_RM_LICENSE__

<!-- __RM_SHORT_DESC__ -->
__PP_SHORT_DESC__
<!-- __RM_SHORT_DESC__ -->

<!-- __RM_VERSION__ -->
__PP_VER_DISP__
<!-- __RM_VERSION__ -->

<!-- ![alt-text](README/screenshot.png "screenshot") -->

## Requirements
<!-- __RM_DEPS__ -->
__PP_PY_DEPS__
<!-- __RM_DEPS__ -->

## Installing
<!-- __RM_PKG__ -->
You can download the (hopefully stable)
[latest release](https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__/releases/latest "https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__/releases/latest")
from the main branch.<br>
Download the 'tar.gz' file.

Then install it:
```bash
foo@bar:~$ cd ~/Downloads/__PP_NAME_PRJ_BIG__-<version>/dist
foo@bar:~/Downloads$ python -m pip install __PP_NAME_PRJ_BIG__-<version>.tar.gz
```
Or you can clone the git repo to get the latest (and often broken) code from the 
dev branch:
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
You can download the (hopefully stable)
[latest release](https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__/releases/latest "https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__/releases/latest")
from the main branch.<br>
Download either the 'tar.gz' or '.zip' file and extract it.

Then install it:
```bash
foo@bar:~$ cd ~/Downloads/__PP_NAME_PRJ_BIG__-<version>/dist
foo@bar:~/Downloads/__PP_NAME_PRJ_BIG__-<version>/dist$ ./install.py
```

Or you can clone the git repo to get the latest (and often broken) code from
the dev branch:
```bash
foo@bar:~$ cd ~/Downloads
foo@bar:~/Downloads$ git clone https://github.com/__PP_AUTHOR__/__PP_NAME_PRJ_BIG__
foo@bar:~/Downloads$ cd __PP_NAME_PRJ_BIG__-<version>/dist
foo@bar:~/Downloads/__PP_NAME_PRJ_BIG__-<version>$ ./install.py
```
<!-- __RM_APP__ -->

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

## Usage
blah blah blah

## Notes
blah blah blah

-)
<!-- -) -->
