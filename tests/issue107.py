
'''
test issue 107 and 133
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
import sys
import unittest

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

import spec2nexus.extractSpecScan
import spec2nexus.spec
from spec2nexus import writer

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _path not in sys.path:
    sys.path.insert(0, _path)
import tests.common


class Issue107(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(path, 'data', 'JL124_1.spc')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))

        scanNum = 4
        scan = specData.getScan(scanNum)
        self.assertTrue(hasattr(scan.header, "H"))
        self.assertTrue(hasattr(scan, "V"))
        scan.interpret()
        self.assertTrue(hasattr(scan, "metadata"))
        self.assertEqual(len(scan.metadata), 140)

        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))


class Issue133(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(path, 'data', 'JL124_1.spc')
        self.sys_argv0 = sys.argv[0]
        self.hfile = tests.common.create_test_file()

    def tearDown(self):
        sys.argv = [self.sys_argv0,]
        os.remove(self.hfile)

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specfile = spec2nexus.spec.SpecDataFile(self.testfile)
        scanNum = 1
        scan = specfile.getScan(scanNum)

        # issue #137 & #140
        try:
            u = scan.__getattribute__("U")
        except AttributeError:
            u = None
        self.assertNotEqual(u, None, "U attribute lazy loaded")
        # not needed: scan.interpret()
        self.assertTrue(hasattr(scan, "U"), "#U in scan #1")
        self.assertEqual(len(scan.U), 1, "only one #U in scan #1")

        self.assertTrue(hasattr(scan.header, "U"), "#U in scan header")
        self.assertEqual(len(scan.header.U), 1, "only one #U in header")
        
        # test for UserReserved in a NeXus file

        specwriter = writer.Writer(specfile)
        specwriter.save(self.hfile, "1 2 3 4 5".split())
        self.assertTrue(os.path.exists(self.hfile))

        fp = h5py.File(self.hfile, 'r')
        entry = fp.get("/S1")
        self.assertIsNot(entry, None, "group /S1")
        u = entry.get("UserReserved")
        self.assertNotEqual(u, None, "group /S1/UserReserved")
        self.assertNotEqual(u.get("header_1"), None, "dataset /S1/UserReserved/header_1")
        self.assertEqual(u.get("header_2"), None, "dataset /S1/UserReserved/header_2")
        self.assertNotEqual(u.get("item_1"), None, "dataset /S1/UserReserved/item_1")
        self.assertEqual(u.get("item_2"), None, "dataset /S1/UserReserved/item_2")

        entry = fp.get("/S2")
        self.assertIsNot(entry, None, "group /S2")
        u = entry.get("UserReserved")
        self.assertNotEqual(u, None, "group /S2/UserReserved")
        self.assertNotEqual(u.get("header_1"), None, "dataset /S1/UserReserved/header_1")
        self.assertEqual(u.get("header_2"), None, "dataset /S1/UserReserved/header_2")
        self.assertEqual(u.get("item_1"), None, "dataset /S1/UserReserved/item_1")
        self.assertEqual(u.get("item_2"), None, "dataset /S1/UserReserved/item_2")
        fp.close()


def suite(*args, **kw):
    test_list = [
        Issue107,
        Issue133,
        ]
    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
