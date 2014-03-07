#!/usr/bin/env python

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
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
       download_url=spec2nexus.__download_url__,
       keywords=spec2nexus.__keywords__,
       platforms='any',
       requires = ('numpy', 'h5py'),   # intend to drop nexpy requirement
       package_dir = {'': 'src'},
       packages = ['spec2nexus', ],
       #packages=find_packages(),
       package_data = {
                       'spec2nexus': ['data/*'],
                       },
        classifiers= ['Development Status :: 5 - Production/Stable',
                      'Environment :: Console',
                      'Intended Audience :: Science/Research',
                      'License :: Freely Distributable',
                      'License :: Public Domain',
                      'Programming Language :: Python',
                      'Programming Language :: Python :: 2',
                      'Programming Language :: Python :: 2.7',
                      'Topic :: Scientific/Engineering',
                      'Topic :: Scientific/Engineering :: Astronomy',
                      'Topic :: Scientific/Engineering :: Bio-Informatics',
                      'Topic :: Scientific/Engineering :: Chemistry',
                      'Topic :: Scientific/Engineering :: Information Analysis',
                      'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
                      'Topic :: Scientific/Engineering :: Mathematics',
                      'Topic :: Scientific/Engineering :: Physics',
                      'Topic :: Scientific/Engineering :: Visualization',
                      'Topic :: Software Development',
                      'Topic :: Utilities',
                      ],
       entry_points={
            # create & install scripts in <python>/bin
            'console_scripts': [
                'spec2nexus=spec2nexus.cli:main',
                'h5toText=spec2nexus.h5toText:main',
			],
            #'gui_scripts': [],
       },
      )
