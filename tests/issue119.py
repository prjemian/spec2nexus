
'''
test issue 119
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

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

import spec2nexus.extractSpecScan
import spec2nexus.spec

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _path not in sys.path:
    sys.path.insert(0, _path)
import tests.common


class Issue119(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(path, 'data', 'issue119_data.txt')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))

        scanNum = 1
        scan = specData.getScan(scanNum)
        self.assertTrue(hasattr(scan.header, "H"))
        scan.interpret()
        self.assertTrue(hasattr(scan, "metadata"))
        self.assertTrue("DCM_energy" in scan.metadata)
        self.assertGreater(len(scan.metadata), 15)
        self.assertTrue("DCM_lambda" in scan.metadata)

        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue119,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
