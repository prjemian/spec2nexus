"""Unit test for XPCS plugins."""

# -----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2020, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
# -----------------------------------------------------------------------------

import unittest
import os, sys

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_path = os.path.abspath(os.path.join(_test_path, "src"))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

import spec2nexus.spec


class Test(unittest.TestCase):
    def setUp(self):
        self.basepath = os.path.join(_path, "spec2nexus")
        self.datapath = os.path.join(self.basepath, "data")
        self.xpcsPluginSample = os.path.join(
            self.datapath, "xpcs_plugin_sample.spec"
        )

    def tearDown(self):
        pass

    def testVA(self):
        # print "testVA"
        sd = spec2nexus.spec.SpecDataFile(self.xpcsPluginSample)
        self.assertEqual(len(sd.headers[0].VA), 2)
        VA0 = sd.headers[0].VA["VA0"].split()
        self.assertEqual(len(VA0), 8)
        self.assertEqual(VA0[0], "ta1zu")
        self.assertEqual(VA0[1], "ta1zdo")
        self.assertEqual(VA0[2], "ta1zdi")
        self.assertEqual(VA0[3], "ta1xu")
        self.assertEqual(VA0[4], "ta1xd")
        self.assertEqual(VA0[5], "ta2zu")
        self.assertEqual(VA0[6], "ta2zdo")
        self.assertEqual(VA0[7], "ta2zdi")
        VA1 = sd.headers[0].VA["VA1"].split()
        self.assertEqual(len(VA1), 9)
        self.assertEqual(VA1[0], "ta2xu")
        self.assertEqual(VA1[1], "ta2xd")
        self.assertEqual(VA1[2], "motor")
        self.assertEqual(VA1[3], "23")
        self.assertEqual(VA1[4], "ta2rotact")
        self.assertEqual(VA1[5], "sa1zu")
        self.assertEqual(VA1[6], "sa1xu")
        self.assertEqual(VA1[7], "sa1zd")
        self.assertEqual(VA1[8], "sa1xd")

    def testVD(self):
        # print "testVD"
        sd = spec2nexus.spec.SpecDataFile(self.xpcsPluginSample)
        self.assertEqual(len(sd.headers[0].VD), 1)
        VD0 = sd.headers[0].VD["VD0"].split()
        self.assertEqual(len(VD0), 2)
        self.assertEqual(VD0[0], "gonio1")
        self.assertEqual(VD0[1], "gonio2")

    def testVE(self):
        # print "testVE"
        sd = spec2nexus.spec.SpecDataFile(self.xpcsPluginSample)
        self.assertEqual(len(sd.headers[0].VE), 2)
        VE0 = sd.headers[0].VE["VE0"].split()
        self.assertEqual(len(VE0), 6)
        self.assertEqual(VE0[0], "te2xu")
        self.assertEqual(VE0[1], "te2xd")
        self.assertEqual(VE0[2], "te2y")
        self.assertEqual(VE0[3], "te2zu")
        self.assertEqual(VE0[4], "te2zdi")
        self.assertEqual(VE0[5], "te2zdo")
        VE1 = sd.headers[0].VE["VE1"].split()
        self.assertEqual(len(VE1), 4)
        self.assertEqual(VE1[0], "se2b")
        self.assertEqual(VE1[1], "se2t")
        self.assertEqual(VE1[2], "se2o")
        self.assertEqual(VE1[3], "se2i")

    def testXPCS(self):
        # print 'testXPCS'
        sd = spec2nexus.spec.SpecDataFile(self.xpcsPluginSample)
        self.assertTrue(isinstance(sd, spec2nexus.spec.SpecDataFile))

        scan = sd.getScan(7)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))

        # finally, start testing the XPCS plugin
        self.assertFalse("XPCS" in scan.__dict__)
        scan.interpret()  # force the plug-ins to be processed
        self.assertTrue("XPCS" in scan.__dict__)
        for key in "batch_name preset compression multi_img".split():
            self.assertTrue(key in scan.XPCS)


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Test,
    ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())
