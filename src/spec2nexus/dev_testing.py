#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Process specific data file(s)'''


import h5toText
import os
import spec
import writer


if __name__ == '__main__':
    pwd = os.path.abspath(os.getcwd())
    # 03_06_JanTest.dat has ...
    prefix = os.path.abspath(os.path.join(pwd, 'data', '03_06_JanTest'))
    file1 = prefix + '.dat'
    hfile = prefix + '.hdf5'

    # writer interface has changed, must use new spec module to proceed
    specfile = spec.SpecDataFile(file1)
    writer = writer.Writer(specfile)
    writer.save(hfile, sorted(specfile.getScanNumbers()))
    h5toText.do_filelist([hfile, ], None)
