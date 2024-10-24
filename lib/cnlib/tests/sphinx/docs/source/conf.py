from pathlib import Path
import sys

dir_src = Path('/home/dana/Documents/Projects/Python/PyPlate/lib/cnlib/tests/sphinx/src')
sys.path.insert(0, str(dir_src))
dir_src = Path('/home/dana/Documents/Projects/Python/PyPlate/lib')
sys.path.insert(0, str(dir_src))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = '__PP_NAME_SMALL__'
copyright = '2024, __PP_AUTHOR__'
author = '__PP_AUTHOR__'

version = '__PP_VERSION__'
release = '0.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'en'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
