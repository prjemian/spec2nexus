'''
unit tests for the extractSpecScan module
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import unittest
import extractSpecScan
import os
import sys


class Test(unittest.TestCase):


    def setUp(self):
        os.environ['SPEC2NEXUS_PLUGIN_PATH'] = 'C://Users//Pete//Desktop, /tmp'
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.datapath = os.path.join(self.basepath, 'data')


    def tearDown(self):
        for fname in ('CdSe_92', 'CdSe_93', 'CdSe_95'):
            full_name = os.path.join(self.datapath, fname)
            if os.path.exists(full_name):
                os.remove(full_name)
                #print "removed test file:", full_name
                pass

#     def test_usage(self):
#         sys.argv = [sys.argv[0], ]
#         sys.argv.append('-h')
#         self.assertRaises(SystemExit, extractSpecScan.main)

#     def test_version(self):
#         sys.argv = [sys.argv[0], ]
#         sys.argv.append('-v')
#         self.assertRaises(SystemExit, extractSpecScan.main)

    def test_CdSe(self):
        fname = os.path.join(self.datapath, 'CdSe')
        sys.argv = [sys.argv[0], fname, ]
        sys.argv.append('--quiet')
        sys.argv.append('-s')
        sys.argv.append('92')
        sys.argv.append('-c')
        sys.argv.append('HerixE')
        sys.argv.append('T_sample_LS340')
        sys.argv.append('HRMpzt1')
        # aborted scan #92
        # TODO: should not raise this ValueError but instead, handle it fail-safe
        self.assertRaises(ValueError, extractSpecScan.main)
        
        sys.argv = [sys.argv[0], fname, ]
        sys.argv.append('--quiet')
        sys.argv.append('-s')
        sys.argv.append('95')
        sys.argv.append('-c')
        sys.argv.append('HerixE')
        sys.argv.append('T_sample_LS340')
        sys.argv.append('HRMpzt1')
        extractSpecScan.main()
        
        full_name = os.path.join(self.datapath, 'CdSe_95')
        self.assertTrue(os.path.exists(full_name), full_name + ' was not found')
        buf = open(full_name, 'r').readlines()
        self.assertEqual(42, len(buf))
        self.assertEqual('# HerixE\tT_sample_LS340\tHRMpzt1\n', buf[0])
        self.assertEqual([-12.063282, 297.529, 66.0], map(float, buf[1].split()))
        self.assertEqual([-2.0358687, 297.553, 66.0], map(float, buf[-1].split()))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
