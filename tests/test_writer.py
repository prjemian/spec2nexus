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
        # TODO: make tests of other things in the Writer
        dd = out.root_attributes()
        self.assertTrue(isinstance(dd, dict))

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
        # #S 22  mesh  eta 57 57.1 10  chi 90.9 91 10  1
        fname = os.path.join(_path, "spec2nexus", 'data', '33id_spec.dat')
        hname = "test.h5"
        spec_data = spec.SpecDataFile(fname)
        out = writer.Writer(spec_data)
#         out.save(hname, [22])
#  
#         with h5py.File("test.h5", "r") as hp:
#             root = hp["/"]
#             nxentry = root["S22"]
#             self.assertTrue("text" in nxentry)
#             value = eznx.read_nexus_field(nxentry, "text", astype=str)
#             self.assertEqual(value, "replacement text")

# --------------

#     sys.argv.append(os.path.join('data', 'APS_spec_data.dat'))
#     sys.argv.append(os.path.join('data', '33id_spec.dat'))
#     sys.argv.append(os.path.join('data', '33bm_spec.dat'))
#     sys.argv.append(os.path.join('data', 'lmn40.spe'))


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
