# config = {
#     'DICT_USER': {
#         '__PP_AUTHOR__': 'cyclopticnerve'
#     }
# }

# g_dict_settings = {
#     '__PP_AUTHOR__':            config['DICT_USER']['__PP_AUTHOR__'],
#     # '__PP_EMAIL__':             DICT_USER['__PP_EMAIL__'],
#     # '__PP_LICENSE_NAME__':      DICT_USER['__PP_LICENSE_NAME__'],
#     # '__PP_DATE_FMT__':          DICT_USER['__PP_DATE_FMT__'],
#     # '__PP_TYPE_PRJ__':          '', # 'c'
#     # '__PP_DIR_PRJ__':           '', # '~/Documents/Projects/Python/CLIs/PyPlate'
#     # '__PP_NAME_BIG__':          '', # PyPlate
#     # '__PP_NAME_SMALL__':        '', # pyplate
#     # '__PP_DATE__':              '', # 12/08/2022
#     # '__PP_TREE_IGNORE__':       LIST_TREE_IGNORE,
# }
"""docstring"""
import config

g_dict_settings = {
    '__PP_AUTHOR__':            config.DICT_USER['__PP_AUTHOR__'],
}

print(g_dict_settings)
