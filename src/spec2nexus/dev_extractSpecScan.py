#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''developer test for extractSpecScan'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


import os
import sys
import extractSpecScan

testpath = os.path.abspath(os.path.split(__file__)[0])
testfile = os.path.join(testpath, 'data', 'CdSe')
if not os.path.exists(testfile):
    raise IOError, 'file does not exist: ' + testfile

sys.argv = [sys.argv[0], ]
sys.argv.append(testfile)
sys.argv.append('-s')
sys.argv.append('92')
sys.argv.append('95')
sys.argv.append('-c')
sys.argv.append('HerixE')
sys.argv.append('T_sample_LS340')
sys.argv.append('HRMpzt1')
#sys.argv.append('-v')

# Show how to get the help/usage text
# sys.argv = [sys.argv[0], ]
# sys.argv.append('-h')

extractSpecScan.main()
