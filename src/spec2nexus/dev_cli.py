#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''developer test items'''

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
import cli

if __name__ == '__main__':
    # developer test items
    #sys.argv.append('--help')
    #sys.argv.append('-V')
    #sys.argv.append('-q')
    sys.argv.append('-v')
    #sys.argv.append('-f')
    #sys.argv.append('-s 19,5-9,19')
    #sys.argv.append('-s 2')
    sys.argv.append(os.path.join('data', 'APS_spec_data.dat'))
    sys.argv.append(os.path.join('data', '33id_spec.dat'))
    sys.argv.append(os.path.join('data', '33bm_spec.dat'))
    sys.argv.append(os.path.join('data', 'lmn40.spe'))
    cli.main()
