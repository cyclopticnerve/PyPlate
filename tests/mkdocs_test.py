from pathlib import Path

PRJ_DIR = Path(__file__).resolve().parents[1]
FILE_TO_TEST = Path(__file__).resolve()

PATH_REL = FILE_TO_TEST.relative_to(PRJ_DIR)

STR_1 = ".".join(PATH_REL.parts)
if STR_1.endswith(".py"):
    STR_1 = STR_1.removesuffix(".py")
print(STR_1)
