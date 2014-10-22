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
    # FIXME: writer interface has changed
    specfile = spec.SpecDataFile(file1)
    writer = writer.Writer(specfile)
    # FIXME: exception at writing scan labels into h5py
    '''
Traceback (most recent call last):
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\dev_datafile.py", line 27, in <module>
    writer.save(hfile, sorted(specfile.getScanNumbers()))
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\writer.py", line 78, in save
    self.save_scan(nxentry, self.spec.getScan(key))
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\writer.py", line 113, in save_scan
    func(nxentry, self, scan, nxclass=CONTAINER_CLASS)
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\control_lines\spec_common_spec2nexus.py", line 510, in data_lines_writer
    writer.save_data(nxdata, scan)
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\writer.py", line 127, in save_data
    signal, axes = self.mesh(nxdata, scan)
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\writer.py", line 204, in mesh
    self.write_ds(nxdata, label, utils.reshape_data(axis, data_shape))
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\writer.py", line 223, in write_ds
    eznx.write_dataset(group, clean_name, data, spec_name=label, **attr)
  File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\eznx.py", line 164, in write_dataset
    dset[:] = data
  File "C:\Users\Pete\Apps\epd\lib\site-packages\h5py\_hl\dataset.py", line 577, in __setitem__
    for fspace in selection.broadcast(mshape):
  File "C:\Users\Pete\Apps\epd\lib\site-packages\h5py\_hl\selections.py", line 296, in broadcast
    raise TypeError("Can't broadcast %s -> %s" % (target_shape, count))
TypeError: Can't broadcast (16, 16) -> (1,)
    '''
    writer.save(hfile, sorted(specfile.getScanNumbers()))
#     h5toText.do_filelist([hfile, ], None)
