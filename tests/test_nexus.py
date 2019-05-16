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

import h5py
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

        self.noise = "verbose"   # for developer
        self.noise = "quiet"     # for travis-ci
        self.test_files = {
            "02_03_setup.dat":          "-f --%s   -s 46",
            "33id_spec.dat":            "-f --%s   -s 1,3-5,8",
            "spec_from_spock.spc":      "-f --%s   -s 116",
            "mca_spectra_example.dat":  "-f --%s   -s 1",
            "xpcs_plugin_sample.spec":  "-f --%s   -s 1",
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
            cmd = fn + "  " + args % self.noise
            _argv = sys.argv = [self.sys_argv0,] + [c for c in cmd.split()]

            nexus.main()
            
            hn = os.path.splitext(fn)[0] + ".hdf5"
            self.assertTrue(os.path.exists(hn))
            with h5py.File(hn, "r") as nx:
                self.assertTrue(isinstance(nx, h5py.File), "is HDF5 file")

                root = nx.get("/")
                self.assertNotEqual(root, None, "HDF5 file has root element")
                comments = root.attrs.get("SPEC_comments")
                self.assertNotEqual(comments, None, "HDF5 file has SPEC comments")
                default = root.attrs.get("default")
                self.assertNotEqual(default, None, "HDF5 file has default attribute")

                nxentry = root[default]
                self.assertNotEqual(nxentry, None, "HDF5 file has NXentry group")
                self.assertTrue(isinstance(nxentry, h5py.Group), default + " is HDF5 Group")

                default = nxentry.attrs.get("default")
                self.assertNotEqual(default, None, default + " group has default attribute")
                nxdata = nxentry[default]
                self.assertNotEqual(nxdata, None, "NXentry group has NXdata group")
                self.assertTrue(isinstance(nxdata, h5py.Group), default + " is HDF5 Group")


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
