#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Process specific data file(s)"""

# TODO: fold into the unit test suite


import os
from spec2nexus import writer
from spec2nexus import spec


if __name__ == '__main__':
    pwd = os.path.abspath(os.getcwd())
    prefix = os.path.abspath(os.path.join(pwd, 'data', 'APS_spec_data'))
    file1 = prefix + '.dat'
    hfile = prefix + '.hdf5'
    # lmn40.spe has two header sections, 2nd is just before "#S 8"
    prefix = os.path.abspath(os.path.join(pwd, 'data', 'lmn40'))
    file1 = prefix + '.spe'

    # CdOsO has four header sections and two #S 1 scans
    prefix = os.path.abspath(os.path.join(pwd, 'data', 'CdOsO'))
    file1 = prefix

    # writer interface has changed, must use new spec module to proceed
    specfile = spec.SpecDataFile(file1)
    writer = writer.Writer(specfile)
    writer.save(hfile, sorted(specfile.getScanNumbers()))
