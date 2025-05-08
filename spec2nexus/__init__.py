# -*- coding: iso-8859-1 -*-

"""Configuration of spec2nexus package."""

__package__ = "spec2nexus"

try:
    from setuptools_scm import get_version

    __version__ = get_version(root="..", relative_to=__file__)
    del get_version

except (LookupError, ModuleNotFoundError):
    from importlib.metadata import version

    __version__ = version(__package__)

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2025, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
