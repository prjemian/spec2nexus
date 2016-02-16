#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''developer test for h5toText'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2015, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


import os
import sys
import h5toText

testpath = os.path.abspath(os.path.split(__file__)[0])

sys.argv = [sys.argv[0],]
# sys.argv.append('-h')
# sys.argv.append('-V')
# sys.argv.append('-a')
# sys.argv.append('-n')
# sys.argv.append('6')
# sys.argv.append(os.path.join(testpath, 'data', 'writer_1_3.h5'))
sys.argv.append(os.path.join(testpath, 'data', 'Data_Q.h5'))
# sys.argv.append(os.path.join(testpath, 'data', 'compression.h5'))
# sys.argv.append(os.path.join(testpath, 'data', 'writer_1_3.h5'))
# sys.argv.append(os.path.join(os.environ['HOMEPATH'], 'Desktop', 'thau_1.nxs.hdf'))


# Show how to get the help/usage text
# sys.argv = [sys.argv[0], ]
# sys.argv.append('-h')

h5toText.main()
