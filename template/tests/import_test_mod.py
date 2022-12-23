
# ------------------------------------------------------------------------------
# this part is only for internal package test without venv install
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# up_one = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, up_one)

# ------------------------------------------------------------------------------

import __CN_SMALL_NAME__                                        # 1 one
print(__CN_SMALL_NAME__.func())

# import __CN_SMALL_NAME__ as mod                                 # 2 one as
# print(mod.func())

# from __CN_SMALL_NAME__ import func                              # 3 from one
# print(func())

# from __CN_SMALL_NAME__ import func as afunc                     # 4 from one as
# print(afunc())

# # THIS ONE IS NOT USED!!!
# import __CN_SMALL_NAME__.func                                   # 5 two
# print(__CN_SMALL_NAME__.func())                                 # (same as #1)

# # THIS ONE IS NOT USED!!!
# import __CN_SMALL_NAME__.func as afunc                          # 6 two as
# print(afunc())                                                  # (same as #4)

# # THIS ONE DOES NOT EXIST!!!
# from __CN_SMALL_NAME__.__CN_SMALL_NAME__ import func            # 7 from two
# print(func())

# # THIS ONE DOES NOT EXIST!!!
# from __CN_SMALL_NAME__.__CN_SMALL_NAME__ import func as afunc   # 8 from two as
# print(afunc())

# # WORKS, BUT NOT RECOMMENDED!!!
# from __CN_SMALL_NAME__ import *
# print(func())                                                   # (same as #3)
