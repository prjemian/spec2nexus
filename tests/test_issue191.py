"""Test issue 191."""

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2020, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------

import h5py
import os
import shutil
import sys
import tempfile
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_path = os.path.abspath(os.path.join(_test_path, "src"))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

import spec2nexus.extractSpecScan
import spec2nexus.spec
import spec2nexus.writer


class Issue191(unittest.TestCase):
    def setUp(self):
        _path = os.path.abspath(os.path.dirname(__file__))
        self.testfile = os.path.join(_path, "data", "JL124_1.spc")

        self._owd = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

    def tearDown(self):
        if os.path.exists(self._owd):
            os.chdir(self._owd)
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_nexus_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        sdf = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(sdf, spec2nexus.spec.SpecDataFile))

        scanNum = 1
        scan = sdf.getScan(scanNum)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))

        # force plugins to process
        scan.interpret()

        self.assertTrue(os.path.exists(self.tempdir))
        nexus_output_file_name = (
            os.path.join(
                self.tempdir,
                os.path.basename(os.path.splitext(self.testfile)[0]),
            )
            + ".h5"
        )
        self.assertFalse(os.path.exists(nexus_output_file_name))

        out = spec2nexus.writer.Writer(sdf)
        out.save(nexus_output_file_name, [scanNum,])

        self.assertTrue(os.path.exists(nexus_output_file_name))
        with h5py.File(nexus_output_file_name, "r") as h5:
            # check the NXentry/positioners:NXnote group
            self.assertIn("/S1/positioners", h5)
            pg = h5["/S1/positioners"]
            self.assertIsInstance(pg, h5py.Group)
            self.assertTrue(hasattr(pg, "attrs"))
            self.assertEqual(pg.attrs.get("NX_class"), "NXnote")
            self.assertEqual(pg.attrs.get("target"), pg.name)

            for var in "Chi DCM_theta Delta GammaScrew Motor_10".split():
                self.assertIn(var, pg)
                child = pg[var]
                self.assertIsInstance(child, h5py.Group)
                self.assertTrue(hasattr(child, "attrs"))
                self.assertIn("NX_class", child.attrs)
                self.assertEqual(child.attrs["NX_class"], "NXpositioner")
                self.assertIn("name", child)
                self.assertEqual(child["name"][()], var.encode())
                self.assertIn("value", child)
                self.assertEqual(child["value"][()].shape, (1,))

            # check the NXentry/NXinstrument/positioners link
            self.assertIn("/S1/instrument/positioners", h5)
            ipg = h5["/S1/instrument/positioners"]
            self.assertIsInstance(ipg, h5py.Group)
            self.assertTrue(hasattr(ipg, "attrs"))
            self.assertEqual(pg.attrs.get("NX_class"), "NXnote")
            self.assertNotEqual(ipg.attrs.get("target"), ipg.name)
            self.assertEqual(ipg.attrs.get("target"), pg.name)


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue191,
    ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
