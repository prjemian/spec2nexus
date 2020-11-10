"""
test spec2nexus code
"""

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2020, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------

import os
import sys
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_path = os.path.abspath(os.path.join(_test_path, "src"))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

import spec2nexus.extractSpecScan
import spec2nexus.spec


class Issue8(unittest.TestCase):
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(path, "data", "n_m.txt")
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [
            self.sys_argv0,
        ]

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertIsInstance(specData, spec2nexus.spec.SpecDataFile)

        scanNum = 6
        scan = specData.getScan(scanNum)
        self.assertIsNotNone(scan)
        self.assertIsInstance(scan, spec2nexus.spec.SpecDataFileScan)
        self.assertTrue(hasattr(scan, "data"))
        self.assertIsInstance(scan.data, dict)
        self.assertIn("mr", scan.data)
        self.assertEqual(len(scan.data["mr"]), 31)
        self.assertFalse(hasattr(scan, "_mca_"))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue8,
    ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
