
# this part is only for internal package test without venv install
# import os
# import sys

# curr_dir = os.path.abspath(os.path.dirname(__file__))
# up_one = os.path.abspath(os.path.join(curr_dir, '..'))
# sys.path.insert(1, up_one)

# without init, 5 does not work

# from package_name import module_name                  # 1
# print(module_name.joke())                             # 1

# from package_name import module_name as dhmt          # 2
# print(dhmt.joke())                                    # 2

# import package_name.module_name                       # 3
# print(package_name.module_name.joke())                # 3

# import package_name.module_name as dhmt               # 4
# print(dhmt.joke())                                    # 4

# import package_name                                   # 5
# print(package_name.module_name.joke())                # 5

from package_name.module_name import joke             # 6
print(joke())                                         # 6
