#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2015, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE, distributed with this software.
#-----------------------------------------------------------------------------

from setuptools import setup, find_packages
import os
import re
import sys

# pull in some definitions from the package's __init__.py file
sys.path.insert(0, os.path.join('src', ))
import spec2nexus


verbose=1
long_description = open('README.rst', 'r').read()


setup (name =  spec2nexus.__package_name__,        # spec2nexus
       version = spec2nexus.__version__,
       license = spec2nexus.__license__,
       description = spec2nexus.__description__,
       long_description = long_description,
       author=spec2nexus.__author_name__,
       author_email=spec2nexus.__author_email__,
       url=spec2nexus.__url__,
       #download_url=spec2nexus.__download_url__,
       keywords=spec2nexus.__keywords__,
       platforms='any',
       install_requires = spec2nexus.__install_requires__,
       package_dir = {'': 'src'},
       packages = ['spec2nexus', 'spec2nexus.plugins', ],
       #packages=find_packages(),
       package_data = {
                       'spec2nexus': ['data/*'],
                       },
       classifiers = spec2nexus.__classifiers__,
       entry_points={
            # create & install scripts in <python>/bin
            'console_scripts': [
                'spec2nexus=spec2nexus.nexus:main',
                'h5toText=spec2nexus.h5toText:main',
                'extractSpecScan=spec2nexus.extractSpecScan:main',
                'specplot=spec2nexus.specplot:main',
                'specplot_gallery=spec2nexus.specplot_gallery:main',
			],
            #'gui_scripts': [],
       },
      )
