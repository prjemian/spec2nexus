#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''developer test for nexus'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2016, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


import sys
import nexus

args = 'data/02_03_setup.dat  -f --verbose   -s 46'
args = 'data/33id_spec.dat  -f --verbose   -s 1'
args = 'data/spectra_example.dat  -f --verbose   -s 1'
args = 'data/mca_spectra_example.dat  -f --verbose   -s 1'
args = 'data/xpcs_plugin_sample.spec -f --verbose  -s 1'
for _ in args.split():
    sys.argv.append(_)

nexus.main()
