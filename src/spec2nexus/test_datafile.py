#!/usr/bin/env python

'''Process specific data file(s)'''


import h5toText
import os
import prjPySpec
import prjPySpec2eznx


if __name__ == '__main__':
    pwd = os.path.abspath(os.getcwd())
    prefix = os.path.abspath(os.path.join(pwd, 'data', 'APS_spec_data'))
    file1 = prefix + '.dat'
    prefix = os.path.abspath(os.path.join(pwd, 'data', 'lmn40'))
    file1 = prefix + '.spe'
    hfile = prefix + '.hdf5'
    specfile = prjPySpec.SpecDataFile(file1)
    writer = prjPySpec2eznx.Writer(specfile)
    writer.save(hfile, [5,6])
    h5toText.do_filelist([hfile, ], None)
