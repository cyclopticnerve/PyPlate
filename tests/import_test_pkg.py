
# ------------------------------------------------------------------------------
# this part is only for internal package test without venv install
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# up_one = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, up_one)

# ------------------------------------------------------------------------------

# without __init__.py imports, #1 and #2 don't work

import package_name                                   # 1 one
print(package_name.module_name.func())

# import package_name as pack                           # 2 one as
# print(pack.module_name.func())

# ------------------------------------------------------------------------------

# from package_name import module_name                  # 3 from one
# print(module_name.func())

# from package_name import module_name as mod           # 4 from one as
# print(mod.func())

# import package_name.module_name                       # 5 two (same as #1)
# print(package_name.module_name.func())

# import package_name.module_name as mod                # 6 two as (same as #4)
# print(mod.func())

# from package_name.module_name import func             # 7 from two
# print(func())

# from package_name.module_name import func as func2    # 8 from two as
# print(func2())

# WORKS, BUT NOT RECOMMENDED!!!
# from package_name import *
# print(module_name.func())
