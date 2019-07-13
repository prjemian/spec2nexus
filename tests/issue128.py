
'''
test issue 128
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


class Issue128(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(spec.__file__)
        self.testfile = os.path.join(path, 'data', 'CdOsO')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec.SpecDataFile))

        with self.assertRaises(ValueError):
            # #128 failed due to assumption of int keys
            r = sorted(specData.scans.keys(), key=int)

        # next line assumes #128 is fixed
        scans = specData.getScanNumbers()
        self.assertEqual(len(scans), 74, "expected number of scans")
        self.assertTrue("1" in scans)
        self.assertTrue("1.1" in scans)


def suite(*args, **kw):
    test_list = [
        Issue128,
        ]
    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
