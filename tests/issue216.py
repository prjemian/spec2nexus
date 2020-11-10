
'''
spec2nexus issue #216: Index error reading a single scan SPEC file

The output file gets created but only contains /S1/definition,
running spec2nexus-2021.1.7.

This data file has problems which were not identified clearly
until this issue.  All problems are related to incorrect formatting
of the `#L` line.  The number of columns specified in #N matches
the number of values on each data line (7).

1. The number of columns specified in #N does not match the number
   of columns described in #L
2. The labels given on #L are only delimited by single spaces.
   This results in only one label defined.
3. The number of separate labels given in #L (6) does not equal the
   number of data columns.
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2020, Pete R. Jemian
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
        with self.assertRaises(ValueError):
            scan.interpret()


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
