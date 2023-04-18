# ------------------------------------------------------------------------------
# this part is only for internal package test without venv install
# import os
# import sys

# DIR_CURR = os.path.abspath(os.path.dirname(__file__))
# src_dir = os.path.abspath(os.path.join(DIR_CURR, '../src'))
# sys.path.insert(1, src_dir)

# ------------------------------------------------------------------------------

# without __init__.py imports, #1 and #2 don't work

# ------------------------------------------------------------------------------

# import __PP_NAME_SMALL__                                      # 1 one
# print(__PP_NAME_SMALL__.mod_name_1.func_1())

# import __PP_NAME_SMALL__ as pkg                               # 2 one as
# print(pkg.mod_name_1.func_1())

# from __PP_NAME_SMALL__ import mod_name_1                      # 3 from one
# print(mod_name_1.func_1())

# from __PP_NAME_SMALL__ import mod_name_1 as mod               # 4 from one as
# print(mod.func_1())

# import __PP_NAME_SMALL__.mod_name_1                           # 5 two
# print(__PP_NAME_SMALL__.mod_name_1.func_1())                  # (same as #1)

# import __PP_NAME_SMALL__.mod_name_1 as mod                    # 6 two as
# print(mod.func_1())                                           # (same as #4)

# from __PP_NAME_SMALL__.mod_name_1 import func_1               # 7 from two
# print(func_1())

# from __PP_NAME_SMALL__.mod_name_1 import func_1 as func1      # 8 from two as
# print(func1())

# # WORKS, BUT NOT RECOMMENDED!!!
# from __PP_NAME_SMALL__ import *
# print(mod_name_1.func_1())                                    # 9 (same as #3)
