#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""developer test for extractSpecScan"""

# TODO: fold into the unit test suite

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2019, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


import sys
from spec2nexus import extractSpecScan

#args = 'data/APS_spec_data.dat -s 1 6   -c mr USAXS_PD I0 seconds'
#args = 'data/33id_spec.dat     -s 1 6   -c H K L signal elastic I0 seconds'
#args = 'data/CdOsO     -s 1 1.1 48   -c HerixE H K L T_control_LS340  T_sample_LS340 ICO-C  PIN-D  PIN-C Seconds'
args = 'data/02_03_setup.dat     -s 46  1-3   -c ar  ay  dy  Epoch  seconds  I0  USAXS_PD'
# args = 'data/02_03_setup.dat     -s 47   -c mr seconds  I0  USAXS_PD'
args = 'data/xpcs_plugin_sample.spec  -s 7   -c img_n  Epoch  ccdc'

for _ in args.split():
    sys.argv.append(_)

sys.argv.append('-G')
sys.argv.append('-V')
sys.argv.append('-Q')
sys.argv.append('-P')
extractSpecScan.main()
