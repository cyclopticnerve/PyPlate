"""
docstring
"""

# from cnlib import cnfunctions as F  # type: ignore

# F.printc("plain", "string")
# F.printc("red", "ok", color="91;1", end="", sep=";", flush=True)
# print("red", "ok")


B_DEBUG = False

def printd(string, error=""):
    print(string)
    if B_DEBUG:
        print(error)


printd("Normal", "error")
