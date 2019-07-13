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

import os, sys
import numpy
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import utils

import tests.common


class TestFunctions(unittest.TestCase):

    # def setUp(self):
    #     self.basepath = os.path.join(_path, 'spec2nexus')
    #     self.datapath = os.path.join(self.basepath, 'data')
    #     self.fname = os.path.join(self.datapath, '33id_spec.dat')
    #     basename = os.path.splitext(self.fname)[0]
    #     self.hname = tests.common.create_test_file()
    # 
    # def tearDown(self):
    #     for tname in (self.hname,):
    #         if os.path.exists(tname):
    #             os.remove(tname)
    #             #print "removed test file:", tname
    #             pass

    def test_clean_name(self):
        candidate = "0 is not a good name"
        result = utils.clean_name(candidate)
        self.assertNotEqual(candidate, result)
        expected = "_0_is_not_a_good_name"
        self.assertEqual(expected, result)

        candidate = "entry_5"
        result = utils.clean_name(candidate)
        self.assertEqual(candidate, result)

    def test_iso8601(self):
        expected = "2010-11-03T13:39:34"
        spec = utils.iso8601("Wed Nov 03 13:39:34 2010")
        self.assertEqual(spec, expected)

        expected = "2017-09-15T04:39:10"
        spock = utils.iso8601("09/15/17 04:39:10")
        self.assertEqual(spock, expected)

    def test_split_columns(self):
        expected = ["two theta", "motor x", "scint counter"]
        spec = utils.split_column_labels("two theta  motor x  scint counter")
        self.assertEqual(spec, expected)

    def test_sanitize_name(self):
        # legacy support only
        expected = "_0_is_not_a_good_name"
        spec = utils.sanitize_name(None, "0 is not a good name")
        self.assertEqual(spec, expected)

    def test_reshape_data(self):
        arr = numpy.array([0, 1, 2, 3, 4, 5])
        expected = [[0, 1], [2, 3], [4, 5]]
        spec = utils.reshape_data(arr, (3, 2))
        self.assertTrue((spec == expected).all())

        expected = [[0, 1, 2], [3, 4, 5]]
        spec = utils.reshape_data(arr, (2, 3))
        self.assertTrue((spec == expected).all())


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        TestFunctions,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
