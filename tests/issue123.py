
'''
test issue 123
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

from spec2nexus import spec

import tests.common


class Issue123(unittest.TestCase):
   
    def setUp(self):
        self.path = os.path.dirname(spec.__file__)
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_spock_file(self):
        testfile = os.path.join(self.path, 'data', 'spec_from_spock.spc')

        self.assertTrue(os.path.exists(testfile))

        self.assertFalse(spec.is_spec_file_with_header(testfile))
        self.assertTrue(spec.is_spec_file(testfile))

        specData = spec.SpecDataFile(testfile)
        self.assertTrue(isinstance(specData, spec.SpecDataFile))
        
        self.assertEqual(len(specData.headers), 1, "expected number of headers")
        header = specData.headers[0]
        self.assertTrue(isinstance(header, spec.SpecDataFileHeader))
        self.assertEqual(len(header.raw), 0, "no raw content")
        self.assertNotEqual(len(header.date), 0, "default date")
        self.assertEqual(header.epoch, 1505468350, "default epoch")
        self.assertEqual(len(header.comments), 0, "expected number of header comments")
        self.assertEqual(len(header.O), 0, "defined positioner label rows")
        self.assertEqual(len(header.H), 0, "defined metadata label rows")

        scans = specData.getScanNumbers()
        self.assertEqual(len(scans), 171, "expected number of scans")
        scan = specData.getScan(2)
        self.assertTrue(isinstance(scan, spec.SpecDataFileScan))

        self.assertEqual(len(scan.P), 20, "defined positioner value rows")
        self.assertEqual(len(header.O), 20, "defined positioner label rows")
        self.assertEqual(scan.header.O, header.O, "same object")
        self.assertEqual(len(scan.V), 0, "defined metadata value rows")
        self.assertEqual(len(scan.L), 23, "defined data column labels")
        self.assertEqual(len(scan.data), 23, "defined data variables")
        self.assertEqual(scan.L[0], "Pt_No", "first data column label")
        self.assertEqual(scan.L[-1], "dt", "last data column label")
        d1 = scan.data.get("Pt_No")
        self.assertNotEqual(d1, None, "data 'Pt_No' exists")
        self.assertEqual(len(d1), 51, "data 'Pt_No' has expected number of values")
        self.assertEqual(scan.scanCmd, "dscan th -0.5 0.5 50 1.0", "scan command")
        self.assertEqual(scan.scanNum, "2", "scan number as string")
        self.assertNotEqual(scan.scanNum, 2, "scan number as integer")
        self.assertEqual(len(scan.positioner), 155, "defined positioners")
        d1 = scan.positioner.get("abs")
        self.assertNotEqual(d1, None, "positioner 'abs' exists")
        self.assertEqual(d1, 0.0, "positioner 'abs' value is zero")

    def test_33id_file(self):
        testfile = os.path.join(self.path, 'data', '33id_spec.dat')

        self.assertTrue(os.path.exists(testfile))

        self.assertTrue(spec.is_spec_file_with_header(testfile))
        self.assertTrue(spec.is_spec_file(testfile))

        specData = spec.SpecDataFile(testfile)
        self.assertTrue(isinstance(specData, spec.SpecDataFile))

        scans = specData.getScanNumbers()
        self.assertEqual(len(scans), 106, "expected number of scans")
        
        self.assertEqual(len(specData.headers), 1, "expected number of headers")
        header = specData.headers[0]
        self.assertTrue(isinstance(header, spec.SpecDataFileHeader))
        self.assertGreater(len(header.raw), 0, "raw content")
        self.assertGreater(len(header.date), 0, "defined date")
        self.assertEqual(header.epoch, 1058427452, "expected epoch")
        self.assertEqual(len(header.comments), 1, "expected number of header comments")
        self.assertEqual(len(header.O), 4, "defined positioner label rows")
        self.assertEqual(len(header.H), 21, "defined metadata label rows")


def suite(*args, **kw):
    test_list = [
        Issue123,
        ]
    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
