
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

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

from spec2nexus import spec

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _path not in sys.path:
    sys.path.insert(0, _path)
import tests.common


class Issue123(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(spec.__file__)
        self.testfile = os.path.join(path, 'data', 'spec_from_spock.spc')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        self.assertFalse(spec.is_spec_file_with_header(self.testfile))
        self.assertTrue(spec.is_spec_file(self.testfile))

        specData = spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec.SpecDataFile))

        scans = specData.getScanNumbers()
        self.assertEqual(len(scans), 172, "expected number of scans")


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
