
# ------------------------------------------------------------------------------
# this part is only for internal package test without venv install
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# up_one = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, up_one)

# ------------------------------------------------------------------------------

import module_name                                     # 1 one
print(module_name.func())

# import module_name as mod                            # 2 one as
# print(mod.func())

# from module_name import func                         # 3 from one
# print(func())

# from module_name import func as afunc                # 4 from one as
# print(afunc())

# THIS ONE IS NOT USED!!!
# import module_name.func                              # 5 two (same as #1)
# print(module_name.func())

# THIS ONE IS NOT USED!!!
# import module_name.func as afunc                     # 6 two as (same as #4)
# print(afunc())

# THIS ONE IS NOT USED!!!
# from module_name.module_name import func             # 7 from two
# print(func())

# THIS ONE IS NOT USED!!!
# from module_name.module_name import func as afunc    # 8 from two as
# print(afunc())

# WORKS, BUT NOT RECOMMENDED!!!
# from module_name import *
# print(func())
