
# ------------------------------------------------------------------------------
# this part is only for internal package test without venv install
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# up_one = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, up_one)

# ------------------------------------------------------------------------------

# without __init__.py imports, #1 and #2 don't work

import __CN_SMALL_NAME__                                   # 1 one
print(__CN_SMALL_NAME__.mod_name_1.func_1())

# import __CN_SMALL_NAME__ as pkg                            # 2 one as
# print(pkg.mod_name_1.func_1())

# ------------------------------------------------------------------------------

# from __CN_SMALL_NAME__ import mod_name_1                    # 3 from one
# print(mod_name_1.func_1())

# from __CN_SMALL_NAME__ import mod_name_1 as mod             # 4 from one as
# print(mod.func_1())

# import __CN_SMALL_NAME__.mod_name_1                         # 5 two
# print(__CN_SMALL_NAME__.mod_name_1.func_1())                # (same as #1)

# import __CN_SMALL_NAME__.mod_name_1 as mod                  # 6 two as
# print(mod.func_1())                                         # (same as #4)

# from __CN_SMALL_NAME__.mod_name_1 import func_1             # 7 from two
# print(func_1())

# from __CN_SMALL_NAME__.mod_name_1 import func_1 as func1    # 8 from two as
# print(func1())

# # WORKS, BUT NOT RECOMMENDED!!!
# from __CN_SMALL_NAME__ import *
# print(mod_name_1.func_1())                                  # (same as #3)
