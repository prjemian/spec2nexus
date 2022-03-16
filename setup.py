#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
import pathlib
import sys

import versioneer

# pull in some definitions from the package's __init__.py file
basedir = pathlib.Path(__file__).absolute().parent
sys.path.insert(0, str(basedir / "src"))
import spec2nexus as package


verbose = 1
readme = open(str(basedir / "README.md"), "r").read()


setup(
    name=package.__package_name__,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license=package.__license__,
    description=package.__description__,
    long_description=readme,

    # allowed values:
    # https://packaging.python.org/en/latest/specifications/core-metadata/#description-content-type
    long_description_content_type="text/markdown",

    author=package.__author_name__,
    author_email=package.__author_email__,
    url=package.__url__,
    # download_url=package.__download_url__,
    keywords=package.__keywords__,
    platforms="any",
    install_requires=package.__install_requires__,
    package_dir={"": "src"},
    packages=["spec2nexus", "spec2nexus.plugins"],
    package_data={
        "spec2nexus": [
            "data/02_03_setup_fly/*",
            "data/*.*",
            "data/Cd*",
            "plugins/*.xsd",
            "LICENSE.txt",
            "diffractometer-geometries.dict",
        ],
    },
    classifiers=package.__classifiers__,
    entry_points={
        # create & install scripts in <python>/bin
        "console_scripts": [
            "spec2nexus=spec2nexus.nexus:main",
            "extractSpecScan=spec2nexus.extractSpecScan:main",
            "specplot=spec2nexus.specplot:main",
            "specplot_gallery=spec2nexus.specplot_gallery:main",
        ],
        # 'gui_scripts': [],
    },
)


# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2022, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE, distributed with this software.
# -----------------------------------------------------------------------------
