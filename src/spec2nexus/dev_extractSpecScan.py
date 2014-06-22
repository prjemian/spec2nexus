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
testscans = '92 95'
testlabels = 'HerixE T_sample_LS340  HRMpzt1'
cmdLine = ' '.join((sys.argv[0], testfile, testscans, testlabels))

extractSpecScan.extractScans(cmdLine.split())
