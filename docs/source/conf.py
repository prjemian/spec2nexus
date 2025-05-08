# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# flake8: noqa

# -- Path setup --------------------------------------------------------------

import pathlib
import sys
import tomllib
from importlib.metadata import version

root_path = pathlib.Path(__file__).parent.parent.parent

with open(root_path / "pyproject.toml", "rb") as fp:
    toml = tomllib.load(fp)
metadata = toml["project"]

sys.path.insert(0, str(root_path))

# imports here for sphinx to build the documents without many WARNINGS.
import spec2nexus, spec2nexus.charts

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

author = metadata["authors"][0]["name"]
copyright = toml["tool"]["copyright"]["copyright"]
description = metadata["description"]
github_url = metadata["urls"]["source"]
project = metadata["name"]
release = spec2nexus.__version__
rst_prolog = f".. |author| replace:: {author}"
today_fmt = "%Y-%m-%d %H:%M"

# -- Special handling for version numbers ------------------------------------
# https://github.com/pypa/setuptools_scm#usage-from-sphinx

release = version(project)
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = """
    sphinx.ext.autodoc
    sphinx.ext.autosummary
    sphinx.ext.coverage
    sphinx.ext.githubpages
    sphinx.ext.inheritance_diagram
    sphinx.ext.mathjax
    sphinx.ext.todo
    sphinx.ext.viewcode
    sphinx_design
""".split()
extensions.append("sphinx_tabs.tabs")  # this must be last

templates_path = ['_templates']
# source_suffix = ['.rst', '.md']
exclude_patterns = []

# RED FLAG: This could hide real layout issues.  It quiets terms.rst for now.
# Leave the warnings for now.  Can ignore them.
# suppress_warnings = [
#     "ref.footnote",
# ]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_title = f"{project} {version}"
html_static_path = ['_static']

# -- Options for autodoc ---------------------------------------------------

autodoc_exclude_members = ",".join(
    """
    __weakref__
    _component_kinds
    _device_tuple
    _required_for_connection
    _sig_attrs
    _sub_devices
    calc_class
    component_names
    """.split()
)
autodoc_default_options = {
    "members": True,
    # 'member-order': 'bysource',
    "private-members": True,
    # "special-members": True,
    "undoc-members": True,
    "exclude-members": autodoc_exclude_members,
    "show-inheritance": True,
    "inherited-members": True,
}
autodoc_mock_imports = """
    h5py
    lxml
    numpy
""".split()
