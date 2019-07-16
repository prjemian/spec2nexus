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

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import spec, writer

import tests.common


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.join(_path, 'spec2nexus')
        self.datapath = os.path.join(self.basepath, 'data')
        self.fname = os.path.join(self.datapath, '33id_spec.dat')
        basename = os.path.splitext(self.fname)[0]
        self.hname = tests.common.create_test_file()

    def tearDown(self):
        for tname in (self.hname,):
            if os.path.exists(tname):
                os.remove(tname)
                #print "removed test file:", tname
                pass

    def testWriter(self):
        '''test the writer.Writer class'''
        spec_data = spec.SpecDataFile(self.fname)
        out = writer.Writer(spec_data)
        scan_list = [1, 5, 7]
        out.save(self.hname, scan_list)

        dd = out.root_attributes()
        self.assertTrue(isinstance(dd, dict))
        
        # TODO: test writer's various functions and methods

        # test file written by Writer
        with h5py.File(self.hname, "r") as hp:
            root = hp["/"]
            default = root.attrs.get("default")
            self.assertNotEqual(default, None)
            self.assertTrue(default in root)
            nxentry = root[default]

            default = nxentry.attrs.get("default")
            self.assertNotEqual(default, None)
            self.assertTrue(default in nxentry)
            nxdata = nxentry[default]

            signal = nxdata.attrs.get("signal")
            self.assertNotEqual(signal, None)
            self.assertTrue(signal in nxdata)


class TestMeshes(unittest.TestCase):

    def setUp(self):
        self._owd = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

    def tearDown(self):
        if os.path.exists(self._owd):
            os.chdir(self._owd)
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_save_data_mesh(self):
        #S 22  mesh  eta 57 57.1 10  chi 90.9 91 10  1
        fname = os.path.join(_path, "spec2nexus", 'data', '33id_spec.dat')
        hname = "test.h5"
        spec_data = spec.SpecDataFile(fname)
        out = writer.Writer(spec_data)
        out.save(hname, [22])
  
        with h5py.File(hname, "r") as hp:
            root = hp["/"]
            nxdata = root["/S22/data"]
            signal = nxdata.attrs["signal"]
            self.assertEqual(nxdata[signal][()].shape, (11, 11))

            ds = nxdata["_mca_"]
            self.assertEqual(ds[()].shape, (11, 11, 91))
            self.assertEqual(ds.attrs["axes"], "eta:chi:_mca_channel_")
            self.assertEqual(ds.attrs["spec_name"], "_mca_")
            self.assertEqual(ds.attrs["units"], "counts")

    def test_save_data_hklmesh(self):
        #S 17  hklmesh  H 1.9 2.1 100  K 1.9 2.1 100  -800000
        fname = os.path.join(_path, "spec2nexus", 'data', '33bm_spec.dat')
        hname = "test.h5"
        spec_data = spec.SpecDataFile(fname)
        out = writer.Writer(spec_data)
        out.save(hname, [17])
  
        with h5py.File(hname, "r") as hp:
            root = hp["/"]
            nxdata = root["/S17/data"]
            signal = nxdata.attrs["signal"]
            axes = nxdata.attrs["axes"]
            self.assertEqual(axes[0], b"H")
            self.assertEqual(axes[1], b"K")

    def test_save_data_hscan(self):
        # hklscan moving H
        test_file = 'lmn40.spe'
        scan_number = 74
        
        fname = os.path.join(_path, "spec2nexus", 'data', test_file)
        hname = "test.h5"
        spec_data = spec.SpecDataFile(fname)
        out = writer.Writer(spec_data)
        out.save(hname, [scan_number])
        
        with h5py.File(hname, "r") as hp:
            root = hp["/"]
            nxdata = root["/S%d/data" % scan_number]
            signal = nxdata.attrs["signal"]
            axes = nxdata.attrs["axes"]
            self.assertEqual(signal, "NaI")
            self.assertEqual(axes, "H")

    def test_save_data_kscan(self):
        # hklscan moving K
        test_file = '33id_spec.dat'
        scan_number = 104
        
        fname = os.path.join(_path, "spec2nexus", 'data', test_file)
        hname = "test.h5"
        spec_data = spec.SpecDataFile(fname)
        out = writer.Writer(spec_data)
        out.save(hname, [scan_number])
        
        with h5py.File(hname, "r") as hp:
            root = hp["/"]
            nxdata = root["/S%d/data" % scan_number]
            signal = nxdata.attrs["signal"]
            axes = nxdata.attrs["axes"]
            self.assertEqual(signal, "I0")
            self.assertEqual(axes, "K")

    def test_save_data_lscan(self):
        # hklscan moving L
        test_file = '33bm_spec.dat'
        scan_number = 14
        
        fname = os.path.join(_path, "spec2nexus", 'data', test_file)
        hname = "test.h5"
        spec_data = spec.SpecDataFile(fname)
        out = writer.Writer(spec_data)
        out.save(hname, [scan_number])
        
        with h5py.File(hname, "r") as hp:
            root = hp["/"]
            nxdata = root["/S%d/data" % scan_number]
            signal = nxdata.attrs["signal"]
            axes = nxdata.attrs["axes"]
            self.assertEqual(signal, "signal")
            self.assertEqual(axes, "L")


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        TestWriter,
        TestMeshes,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
