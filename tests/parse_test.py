#!/usr/bin/env python3

import argparse

S_ABOUT = "name\nshort desc\nversion\nurl\n"
S_HELP = "use -h for help\n"

print(S_ABOUT)

# ------------------------------------------------------------------------------

print(S_HELP)

parser = argparse.ArgumentParser()
parser.add_argument("positional_arg", help="A positional argument")
parser.add_argument("-d", action="store_true", dest="DBG_DEST", help="debug")
parser.parse_args()

# ------------------------------------------------------------------------------
