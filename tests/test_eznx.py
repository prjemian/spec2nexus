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
import numpy
import os
import shutil
import sys
import tempfile
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import eznx

import tests.common


class TestEznx(unittest.TestCase):

    def setUp(self):
        self._owd = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

    def tearDown(self):
        if os.path.exists(self._owd):
            os.chdir(self._owd)
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_example(self):
        root = eznx.makeFile('test.h5', creator='eznx', default='entry')
        nxentry = eznx.makeGroup(root, 'entry', 'NXentry', default='data')
        ds = eznx.write_dataset(nxentry, 'title', 'simple test data')
        nxdata = eznx.makeGroup(nxentry, 'data', 'NXdata', signal='counts', axes='tth', tth_indices=0)
        ds = eznx.write_dataset(nxdata, 'tth', [10.0, 10.1, 10.2, 10.3], units='degrees')
        ds = eznx.write_dataset(nxdata, 'counts', [1, 50, 1000, 5], units='counts', axes="tth")
        root.close()
        
        """
        Test the data file for this structure::
        
            test.h5:NeXus data file
              @creator = eznx
              @default = 'entry'
              entry:NXentry
                @NX_class = NXentry
                @default = 'data'
                title:NX_CHAR = simple test data
                data:NXdata
                  @NX_class = NXdata
                  @signal = 'counts'
                  @axes = 'tth'
                  @axes_indices = 0
                  counts:NX_INT64[4] = [1, 50, 1000, 5]
                    @units = counts
                    @axes = tth
                  tth:NX_FLOAT64[4] = [10.0, 10.1, 10.199999999999999, 10.300000000000001]
                    @units = degrees
        """
        self.assertTrue(os.path.exists("test.h5"))
        with h5py.File("test.h5", "r") as hp:
            root = hp["/"]
            self.assertEqual(root.attrs.get("creator"), "eznx")
            self.assertEqual(root.attrs.get("default"), "entry")

            nxentry = root["entry"]
            self.assertEqual(nxentry.attrs.get("NX_class"), "NXentry")
            self.assertEqual(nxentry.attrs.get("default"), "data")
            self.assertEqual(
                eznx.read_nexus_field(nxentry, "title").decode('utf8'),
                "simple test data")

            nxdata = nxentry["data"]
            self.assertEqual(nxdata.attrs.get("NX_class"), "NXdata")
            self.assertEqual(nxdata.attrs.get("signal"), "counts")
            self.assertEqual(nxdata.attrs.get("axes"), "tth")
            self.assertEqual(nxdata.attrs.get("tth_indices"), 0)
            
            # test the HDF5 structure
            counts = nxdata["counts"]
            self.assertEqual(counts.attrs.get("units"), "counts")
            self.assertEqual(counts.attrs.get("axes"), "tth")
            tth = nxdata["tth"]
            self.assertEqual(tth.attrs.get("units"), "degrees")

            # test the data
            fields = eznx.read_nexus_group_fields(nxentry, "data", "counts tth".split())
            counts = fields["counts"]
            self.assertEqual(len(counts), 4)
            self.assertEqual(counts[2], [1, 50, 1000, 5][2])
            tth = fields["tth"]
            self.assertEqual(len(tth), 4)
            self.assertEqual(tth[2], [10.0, 10.1, 10.2, 10.3][2])

    def test_create_dataset_None(self):
        root = eznx.makeFile('test.h5', creator='eznx', default='entry')
        nxentry = eznx.makeGroup(root, 'entry', 'NXentry', default='data')
        ds = eznx.makeDataset(nxentry, "data_is_None", None)

        with h5py.File("test.h5", "r") as hp:
            root = hp["/"]
            nxentry = root["entry"]
            self.assertTrue("data_is_None" in nxentry)

            ds = nxentry["data_is_None"]
            value = ds[()]        # ds.value deprecated in h5py
            self.assertEqual(len(value), 0)
            self.assertEqual(value, "")
            self.assertTrue("NOTE" in ds.attrs)
            note =  "no data supplied, value set to empty string"
            self.assertEqual(ds.attrs["NOTE"],  note)

    def test_write_dataset_existing(self):
        root = eznx.makeFile('test.h5', creator='eznx', default='entry')
        nxentry = eznx.makeGroup(root, 'entry', 'NXentry', default='data')
        eznx.write_dataset(nxentry, "text", "some text")
        eznx.write_dataset(nxentry, "text", "replacement text")

        with h5py.File("test.h5", "r") as hp:
            root = hp["/"]
            nxentry = root["entry"]
            self.assertTrue("text" in nxentry)
            value = eznx.read_nexus_field(nxentry, "text", astype=str)
            self.assertEqual(value, "replacement text")

    def test_makeExternalLink(self):
        external = eznx.makeFile('external.h5', creator='eznx', default='entry')
        eznx.write_dataset(external, "text", "some text")

        root = eznx.makeFile('test.h5', creator='eznx', default='entry')
        nxentry = eznx.makeGroup(root, 'entry', 'NXentry', default='data')
        eznx.makeExternalLink(root, 'external.h5', "/text", nxentry.name + "/external_text")

        # check the external file first
        with h5py.File("external.h5", "r") as hp:
            root = hp["/"]
            self.assertTrue("text" in root)
            ds = root["text"]
            value = ds[()]        # ds.value deprecated in h5py
            self.assertEqual(value, [b"some text"])

        # check the file with the external link
        with h5py.File("test.h5", "r") as hp:
            root = hp["/"]
            nxentry = root["entry"]
            self.assertTrue("external_text" in nxentry)
            value = eznx.read_nexus_field(nxentry, "external_text")
            self.assertEqual(value, b"some text")
            value = eznx.read_nexus_field(nxentry, "external_text", astype=str)
            self.assertEqual(value, "some text")

    def test_read_nexus_field_alternatives(self):
        root = eznx.makeFile('test.h5', creator='eznx', default='entry')
        nxentry = eznx.makeGroup(root, 'entry', 'NXentry', default='data')
        eznx.write_dataset(nxentry, "text", "some text")
        eznx.write_dataset(nxentry, "number", 42)
        eznx.write_dataset(nxentry, "array", [[1,2,3], [4,5,6]])

        # check the file with the external link
        with h5py.File("test.h5", "r") as hp:
            root = hp["/"]
            nxentry = root["entry"]
            
            value = eznx.read_nexus_field(nxentry, "key_error")
            self.assertEqual(value, None)
            
            value = eznx.read_nexus_field(nxentry, "text")
            self.assertEqual(value, b"some text")
            value = eznx.read_nexus_field(nxentry, "text", astype=str)
            self.assertEqual(value, "some text")
            
            value = eznx.read_nexus_field(nxentry, "number")
            self.assertEqual(value, 42)
            value = eznx.read_nexus_field(nxentry, "number", astype=float)
            self.assertEqual(value, 42)
            value = eznx.read_nexus_field(nxentry, "number", astype=str)
            self.assertEqual(value, "42")
            
            ds = nxentry["array"]
            value = ds[()]        # ds.value deprecated in h5py
            expected = numpy.array([[1,2,3], [4,5,6]])
            self.assertTrue((value == expected).any())

            with self.assertRaises(RuntimeError) as context:
                value = eznx.read_nexus_field(nxentry, "array")
            received = str(context.exception)
            expected = "unexpected 2-D data"
            self.assertTrue(received.startswith(expected))


def suite(*args, **kw):
    test_list = [
        TestEznx,
        ]

    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
