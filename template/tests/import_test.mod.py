
# ------------------------------------------------------------------------------
# this part is only for internal package test without venv install
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# src_dir = os.path.abspath(os.path.join(curr_dir, '../src'))
# sys.path.insert(1, src_dir)

# ------------------------------------------------------------------------------

# import __CN_NAME_SMALL__                                   # 1 one
# print(__CN_NAME_SMALL__.func())

# import __CN_NAME_SMALL__ as mod                            # 2 one as
# print(mod.func())

# from __CN_NAME_SMALL__ import func                         # 3 from one
# print(func())

# from __CN_NAME_SMALL__ import func as afunc                # 4 from one as
# print(afunc())

# # THIS ONE IS NOT USED!!!
# import __CN_NAME_SMALL__.func                              # 5 two
# print(__CN_NAME_SMALL__.func())                            # (same as #1)

# # THIS ONE IS NOT USED!!!
# import __CN_NAME_SMALL__.func as afunc                     # 6 two as
# print(afunc())                                             # (same as #4)

# # THIS ONE DOES NOT EXIST!!!
# from __CN_NAME_SMALL__.__CN_NAME_SMALL__ import func       # 7 from two
# print(func())

# # THIS ONE DOES NOT EXIST!!!
# from __CN_NAME_SMALL__.__CN_NAME_SMALL__ import func as afunc   # 8 from two as
# print(afunc())

# # WORKS, BUT NOT RECOMMENDED!!!
# from __CN_NAME_SMALL__ import *
# print(func())                                                   # (same as #3)
