'''
unit tests for the writer module
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

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

from spec2nexus import eznx

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class TestEznx(unittest.TestCase):

    def setUp(self):
        self._owd = os.getcwd()
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

    def tearDown(self):
        if os.path.exists(self._owd):
            os.chdir(self._owd)
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_example_data(self):
        self.assertTrue(True, "trivial assertion - always True")
        
        root = eznx.makeFile('test.h5', creator='eznx', default='entry')
        nxentry = eznx.makeGroup(root, 'entry', 'NXentry')
        ds = eznx.write_dataset(nxentry, 'title', 'simple test data', default='data')
        nxdata = eznx.makeGroup(nxentry, 'data', 'NXdata', signal='counts', axes='tth', tth_indices=0)
        ds = eznx.write_dataset(nxdata, 'tth', [10.0, 10.1, 10.2, 10.3], units='degrees')
        ds = eznx.write_dataset(nxdata, 'counts', [1, 50, 1000, 5], units='counts')
        root.close()


def suite(*args, **kw):
    test_list = [
        TestEznx,
        ]

    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
