
'''
spec2nexus issue #216: Index error reading a single scan SPEC file

The output file gets created but only contains /S1/definition, 
running spec2nexus-2021.1.7.
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

import spec2nexus.extractSpecScan
import spec2nexus.spec
import spec2nexus.writer

import tests.common


class Issue216(unittest.TestCase):
   
    def setUp(self):
        _path = os.path.abspath(os.path.dirname(__file__))
        self.testfile = os.path.join(_path, 'data', 'issue216_scan1.spec')

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
        nexus_output_file_name = os.path.join(
            self.tempdir, 
            os.path.basename(os.path.splitext(self.testfile)[0])
            ) + ".h5"
        self.assertFalse(os.path.exists(nexus_output_file_name))

        out = spec2nexus.writer.Writer(sdf)
        out.save(nexus_output_file_name, [scanNum,])

        self.assertTrue(os.path.exists(nexus_output_file_name))
        with h5py.File(nexus_output_file_name) as h5:
            # check the NXentry/positioners:NXnote group
            self.assertIn("/S1/definition", h5)
            # TODO: test for other content
            # 7 data columns (#N 7) but (#L EPOCH Phi CESR IC1 IC2 DIODE)
            # 9 data points
            # TODO: should supply default labels when len(#L) < int(#N[0])


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue216,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
