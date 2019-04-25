'''
unit tests for the extractSpecScan module
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
from spec2nexus import extractSpecScan

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class Test(unittest.TestCase):


    def setUp(self):
        os.environ['SPEC2NEXUS_PLUGIN_PATH'] = 'C://Users//Pete//Desktop, /tmp'
        self.basepath = os.path.join(_path, 'spec2nexus')
        self.datapath = os.path.join(self.basepath, 'data')


    def tearDown(self):
        for fname in ('CdSe_92', 'CdSe_93', 'CdSe_95'):
            full_name = os.path.join(self.datapath, fname)
            if os.path.exists(full_name):
                os.remove(full_name)
                #print "removed test file:", full_name

    def test_CdSe_scan_92(self):
        fname = os.path.join(self.datapath, 'CdSe')
        sys.argv = [sys.argv[0], fname, ]
        sys.argv.append('-s')
        sys.argv.append('92')
        sys.argv.append('-c')
        columns = 'HerixE T_sample_LS340 HRMpzt1'.split()
        sys.argv += columns

        with tests.common.Capture_stdout() as printed_lines:
            extractSpecScan.main()  # scan #92 was aborted

        for item, text in enumerate('program: read: wrote:'.split()):
            self.assertTrue(printed_lines[item].startswith(text))

        outfile = printed_lines[2][len('wrote: '):]
        self.assertTrue(os.path.exists(outfile))
        buf = open(outfile, 'r').readlines()
        
        self.assertEqual(len(buf), 22, 'number of lines in data file')
        self.assertEqual('# file: '+fname, buf[0].strip(), 'original SPEC data file name in data file')
        self.assertEqual('# scan: 92', buf[1].strip(), 'scan number in data file')
        self.assertEqual('# '+'\t'.join(columns), buf[2].strip(), 'column labels in data file')

        # test first and last lines of data
        # remaining lines: three columns of numbers, tab delimited
        self.assertEqual([-10.118571, 297.467, 66.0], list(map(float, buf[3].split())))
        self.assertEqual([-5.5910424, 297.483, 66.0], list(map(float, buf[-1].split())))

        os.remove(outfile)
        self.assertFalse(os.path.exists(outfile))
        _breakpoint = True
        
    def test_CdSe_scan_95(self):
        fname = os.path.join(self.datapath, 'CdSe')
        sys.argv = [sys.argv[0], fname, ]
        sys.argv.append('-s')
        sys.argv.append('95')
        sys.argv.append('-c')
        columns = 'HerixE T_sample_LS340 HRMpzt1'.split()
        sys.argv += columns

        with tests.common.Capture_stdout() as printed_lines:
            extractSpecScan.main()
        for item, text in enumerate('program: read: wrote:'.split()):
            self.assertTrue(printed_lines[item].startswith(text))

        outfile = printed_lines[2][len('wrote: '):]
        self.assertTrue(os.path.exists(outfile))
        buf = open(outfile, 'r').readlines()
        
        self.assertEqual(len(buf), 44, 'number of lines in data file')
        self.assertEqual('# file: '+fname, buf[0].strip(), 'original SPEC data file name in data file')
        self.assertEqual('# scan: 95', buf[1].strip(), 'scan number in data file')
        self.assertEqual('# '+'\t'.join(columns), buf[2].strip(), 'column labels in data file')

        # test first and last lines of data
        # remaining lines: three columns of numbers, tab delimited
        self.assertEqual([-12.063282, 297.529, 66.0], list(map(float, buf[3].split())))
        self.assertEqual([-2.0358687, 297.553, 66.0], list(map(float, buf[-1].split())))

        os.remove(outfile)
        self.assertFalse(os.path.exists(outfile))


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
