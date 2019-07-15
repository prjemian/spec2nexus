'''
unit tests for the _requirements module
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

import os, sys
import numpy
import unittest
from builtins import isinstance

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import _requirements

import tests.common


class Test(unittest.TestCase):

    def test_learn_requirements(self):
        reqs = _requirements.learn_requirements()
        self.assertTrue(isinstance(reqs, list))
        self.assertGreater(len(reqs), 0)
        self.assertEqual(len(reqs), 5)
        self.assertTrue("h5py" in reqs)
        self.assertTrue("numpy" in reqs)


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Test,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
