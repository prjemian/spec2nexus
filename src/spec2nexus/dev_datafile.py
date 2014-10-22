#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Process specific data file(s)'''


import h5toText
import os
import prjPySpec
import writer
import spec


if __name__ == '__main__':
    pwd = os.path.abspath(os.getcwd())
    prefix = os.path.abspath(os.path.join(pwd, 'data', 'APS_spec_data'))
    file1 = prefix + '.dat'
    # lmn40.spe has two header section, 2nd is just before "#S 8"
    prefix = os.path.abspath(os.path.join(pwd, 'data', 'lmn40'))
    file1 = prefix + '.spe'
    hfile = prefix + '.hdf5'
    specfile = prjPySpec.SpecDataFile(file1)

    # writer interface has changed, must use new spec module to proceed
    specfile = spec.SpecDataFile(file1)
    writer = writer.Writer(specfile)
    writer.save(hfile, sorted(specfile.getScanNumbers()))
    h5toText.do_filelist([hfile, ], None)
