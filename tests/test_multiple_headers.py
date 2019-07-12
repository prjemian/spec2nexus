
'''
test punx tests/common module (supports unit testing)
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
import sys
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

import spec2nexus.extractSpecScan
import spec2nexus.spec

import tests.common


class Issue143(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(_path, 'spec2nexus', 'data', '05_02_test.dat')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        duplicate_fails = False
        try:
            specData = spec2nexus.spec.SpecDataFile(self.testfile)
        except spec2nexus.spec.DuplicateSpecScanNumber:
            duplicate_fails = True
        self.assertFalse(duplicate_fails, "should not raise DuplicateSpecScanNumber now")
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))

        scanNum = 110
        scan = specData.getScan(scanNum)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))

        scanNum = 1.17
        scan = specData.getScan(scanNum)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))


def suite(*args, **kw):
    test_list = [
        Issue143,
        ]
    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
