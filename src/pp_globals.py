# ------------------------------------------------------------------------------
# Project : PyPlate                                                /          \
# Filename: pp_globals.py                                         |     ()     |
# Date    : 09/03/2026                                            |            |
# Author  : cyclopticnerve                                        |   \____/   |
# License : WTFPLv2                                                \          /
# ------------------------------------------------------------------------------

"""
A module containing functions and variables that need to be accessed by every
other module in the program.
"""

# ------------------------------------------------------------------------------
# Imports
# ------------------------------------------------------------------------------

# system imports
from pathlib import Path

# local imports
from cnlib import cnpot

# ------------------------------------------------------------------------------
# Paths
# ------------------------------------------------------------------------------

# get PyPlate path
P_DIR_PRJ = Path(__file__).parents[1].resolve()

# ------------------------------------------------------------------------------
# I18N
# ------------------------------------------------------------------------------

T_DOMAIN = "pyplate"
T_DIR_LOCALE = P_DIR_PRJ / "i18n/locale"
_ = cnpot.underscore(T_DOMAIN, T_DIR_LOCALE)

# ------------------------------------------------------------------------------

"""
man i went down a fucking rabbit hole today looking at globals in python. so
many different opinions, citing source code, official (and unofficial) docs,
best practices, etc.
so i would like to LOUDLY tell you why i use these global variables.

this is pretty much the START code of this program. this is where it all
begins. if you run pymaker, this is the first local import. same with pybaker.
so it makes sense to start here.

i want EVERY part of my code to know what the debug state is, or what the final
outcome is (or the outcome of the current step, if we fail on first).
the most "pythonic" (shudder) way to do this is to have a class with an
instance variable or instance methods to read/write that variable. aint nobody
got time for that.

i need to know, right now, the state of something. at the absolute highest
level, as soon as the user runs the program.

also, the chances of having a name collision here are VERY LOW.

people argue that using globals "affects the whole program." well, yeah,
sometimes thats the point.

/r /s
"""

# ------------------------------------------------------------------------------
# Bools
# ------------------------------------------------------------------------------

# global debug value (does NOT apply to cnlib/cnfunctions)
B_PP_DEBUG = False
# global result flag
B_PP_RESULT = True

# -)
