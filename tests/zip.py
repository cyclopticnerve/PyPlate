"""docstring"""

# from pathlib import Path
import shutil
# import tarfile

# ------------------------------------------------------------------------------

# PATH_IN = "/home/dana/Projects/Python/PyPlate"
# FMT = "w:gz"
# PATH_OUT = "/home/dana/Projects/Python/PyPlate/dist/PyPlate.tar.gz"

# with tarfile.open(PATH_OUT, mode=FMT) as compressed:
#     compressed.add(PATH_IN, arcname="PyPlate")

# ------------------------------------------------------------------------------

PATH_OUT = "/home/dana/Projects/Python/PyPlate_archive"
FMT = "zip"
PATH_IN = "/home/dana/Projects/Python/PyPlate/dist/pyplate-1.0.0"

print(shutil.make_archive(PATH_OUT, FMT, PATH_IN))
