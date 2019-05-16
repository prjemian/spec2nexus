'''
unit tests for the writer module
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2019, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import os
import shutil
import sys
import tempfile
import unittest

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

from spec2nexus import nexus

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class TestExampleData_to_Nexus(unittest.TestCase):

    def setUp(self):
        self._owd = os.getcwd()
        self.data_path = os.path.join(os.path.dirname(nexus.__file__), "data")
        self.sys_argv0 = sys.argv[0]
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

        noise = "verbose"   # for developer
        # noise = "quiet"     # for travis-ci
        self.test_files = {
            "02_03_setup.dat":          f"-f --{noise}   -s 46",
            "33id_spec.dat":            f"-f --{noise}   -s 1,3-5,8",
            "spec_from_spock.spc":      f"-f --{noise}   -s 116",
            "mca_spectra_example.dat":  f"-f --{noise}   -s 1",
            "xpcs_plugin_sample.spec":  f"-f --{noise}   -s 1",
            }

    def tearDown(self):
        sys.argv = [self.sys_argv0,]
        if os.path.exists(self._owd):
            os.chdir(self._owd)
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_example_data(self):
        self.assertTrue(True, "trivial assertion - always True")
        
        for fn, args in self.test_files.items():
            shutil.copy2(os.path.join(self.data_path, fn), self.tempdir)
            cmd = fn + "  " + args
            _argv = sys.argv = [self.sys_argv0,] + [c for c in cmd.split()]

            nexus.main()
            # reading SPEC data file: xpcs_plugin_sample.spec
            #   discovered 878 scans
            #   converting scan number(s): 1
            # E
            # ======================================================================
            # ERROR: test_example_data (__main__.TestExampleData_to_Nexus)
            # ----------------------------------------------------------------------
            # Traceback (most recent call last):
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/eznx.py", line 175, in write_dataset
            #     dset = parent[name]
            #   File "h5py/_objects.pyx", line 54, in h5py._objects.with_phil.wrapper
            #   File "h5py/_objects.pyx", line 55, in h5py._objects.with_phil.wrapper
            #   File "/home/oxygen/JEMIAN/Apps/BlueSky/lib/python3.6/site-packages/h5py/_hl/group.py", line 177, in __getitem__
            #     oid = h5o.open(self.id, self._e(name), lapl=self._lapl)
            #   File "h5py/_objects.pyx", line 54, in h5py._objects.with_phil.wrapper
            #   File "h5py/_objects.pyx", line 55, in h5py._objects.with_phil.wrapper
            #   File "h5py/h5o.pyx", line 190, in h5py.h5o.open
            # KeyError: "Unable to open object (object 'VA0' doesn't exist)"
            # 
            # During handling of the above exception, another exception occurred:
            # 
            # Traceback (most recent call last):
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/tests/test_nexus.py", line 67, in test_example_data
            #     nexus.main()
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/nexus.py", line 190, in main
            #     out.save(nexus_output_file_name, scan_list)
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/writer.py", line 90, in save
            #     self.save_scan(nxentry, self.spec.getScan(key))
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/writer.py", line 151, in save_scan
            #     func(nxentry, self, scan.header, nxclass=CONTAINER_CLASS)
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/plugins/XPCS_spec2nexus.py", line 38, in writer
            #     writer.save_dict(group, dd)
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/writer.py", line 159, in save_dict
            #     self.write_ds(group, k, v)
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/writer.py", line 306, in write_ds
            #     eznx.write_dataset(group, clean_name, data, spec_name=label, **attr)
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/eznx.py", line 179, in write_dataset
            #     dset = makeDataset(parent, name, data, **attr)
            #   File "/home/oxygen18/JEMIAN/Documents/eclipse/spec2nexus/src/spec2nexus/eznx.py", line 162, in makeDataset
            #     obj = parent.create_dataset(name, data=list(map(encoder, data)))
            #   File "/home/oxygen/JEMIAN/Apps/BlueSky/lib/python3.6/site-packages/h5py/_hl/group.py", line 116, in create_dataset
            #     dsid = dataset.make_new_dset(self, shape, dtype, data, **kwds)
            #   File "/home/oxygen/JEMIAN/Apps/BlueSky/lib/python3.6/site-packages/h5py/_hl/dataset.py", line 100, in make_new_dset
            #     tid = h5t.py_create(dtype, logical=1)
            #   File "h5py/h5t.pyx", line 1611, in h5py.h5t.py_create
            #   File "h5py/h5t.pyx", line 1633, in h5py.h5t.py_create
            #   File "h5py/h5t.pyx", line 1688, in h5py.h5t.py_create
            # TypeError: Object dtype dtype('O') has no native HDF5 equivalent
            # 
            # ----------------------------------------------------------------------
            # Ran 1 test in 6.949s
            # 
            # FAILED (errors=1)
            
            hn = os.path.splitext(fn)[0] + ".hdf5"
            self.assertTrue(os.path.exists(hn))


def suite(*args, **kw):
    test_list = [
        TestExampleData_to_Nexus,
        ]

    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
