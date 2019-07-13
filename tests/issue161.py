
'''
test data file with no #E control lines
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

import datetime
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


class Issue161(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(path, 'data', 'issue161_spock_spec_file')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_date_and_epoch(self):
        spec_fmt = '%a %b %d %H:%M:%S %Y'
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))
        self.assertTrue(hasattr(specData, "headers"))
        self.assertEqual(len(specData.headers), 1)
        header = specData.headers[0]
        self.assertTrue(hasattr(header, "date"))
        self.assertTrue(hasattr(header, "epoch"))
        self.assertEqual(
            datetime.datetime.strptime(header.date, spec_fmt), 
            datetime.datetime.fromtimestamp(header.epoch), 
            "date and epoch are identical")

        scanNum = 1
        scan = specData.getScan(scanNum)
        self.assertTrue(hasattr(scan, "date"))
        self.assertTrue(hasattr(scan, "epoch"))
        self.assertEqual(
            datetime.datetime.strptime(scan.date, spec_fmt), 
            datetime.datetime.fromtimestamp(scan.epoch), 
            "date and epoch are identical")
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue161,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
