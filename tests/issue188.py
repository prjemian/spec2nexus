
'''
test spec2nexus code
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


class Issue188(unittest.TestCase):
   
    def setUp(self):
        self.testfile = os.path.join(_path, 'spec2nexus', 'data', 'startup_1.spec')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_scan_unrecognized(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))

        scanNum = 16
        scan = specData.getScan(scanNum)
        scan.interpret()

        self.assertTrue(hasattr(scan, "data"))
        self.assertTrue(hasattr(scan, "_unrecognized"))
        self.assertEqual(len(scan._unrecognized), 112)

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))

        for scanNum in specData.getScanNumbers():
            scan = specData.getScan(scanNum)
            self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))
            self.assertTrue(hasattr(scan, "L"))
            self.assertIsInstance(scan.L, list)
            self.assertTrue(hasattr(scan, "N"))
            self.assertIsInstance(scan.N, list)
            self.assertGreaterEqual(len(scan.N), 1)
            self.assertEqual(len(scan.L), scan.N[0], "scan %s #L line" % scanNum)

            self.assertTrue(hasattr(scan, "data"))
            self.assertIsInstance(scan.data, dict)
            n = len(scan.data.keys())
            if n > 0:   # if ==0, then no data present
                self.assertEqual(len(scan.L), n, "scan %s #L line" % scanNum)


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue188,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
