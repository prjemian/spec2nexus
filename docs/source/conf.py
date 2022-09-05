# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

import pathlib
import sys
sys.path.insert(0, str(pathlib.Path().absolute().parent.parent / "src"))
import spec2nexus

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = spec2nexus.__package_name__
copyright = spec2nexus.__copyright__
author = spec2nexus.__author__
description = spec2nexus.__description__

# version: The short X.Y version
# release: The full version, including alpha/beta/rc tags
from spec2nexus._version import get_versions
versioneer_version = get_versions()['version']
del get_versions
versioneer_version = versioneer_version.split('+')
version = versioneer_version[0]
# The full version, including alpha/beta/rc tags.
#release = punx.__release__
#release = version
if len(versioneer_version) == 2:
    release = versioneer_version[1]
else:
    release = ''

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    'sphinx.ext.inheritance_diagram',
]

templates_path = ['_templates']
# source_suffix = ['.rst', '.md']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_theme = "furo"
html_static_path = ['_static']
