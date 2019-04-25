
'''
test punx tests/common module (supports unit testing)
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


class Issue64(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(path, 'data', 'issue64_data.txt')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))

        scanNum = 50
        scan = specData.getScan(scanNum)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))

    def test_extractSpecScans_issue_64(self):
        args = self.testfile + ' -s 50   -c si1t  pind1'
        for _ in args.split():
            sys.argv.append(_)
        sys.argv.append('-G')
        sys.argv.append('-V')
        sys.argv.append('-Q')
        sys.argv.append('-P')

        with tests.common.Capture_stdout() as printed_lines:
            spec2nexus.extractSpecScan.main()
        self.assertEqual(len(printed_lines), 3, 'extractSpecScan')

        for item, text in enumerate('program: read: wrote:'.split()):
            self.assertTrue(printed_lines[item].startswith(text))

        outfile = printed_lines[2][len('wrote: '):]
        self.assertTrue(os.path.exists(outfile))
        os.remove(outfile)
        self.assertFalse(os.path.exists(outfile))

    def test_extractSpecScans_issue_66_verbose_reporting_mismatch_P_O(self):
        args = self.testfile + ' --verbose -s 50   -c si1t  pind1'
        for _ in args.split():
            sys.argv.append(_)
        with tests.common.Capture_stdout() as printed_lines:
            spec2nexus.extractSpecScan.main()
        if len(printed_lines) != 5:
            print(args)
            print("\n".join(printed_lines))
        self.assertEqual(len(printed_lines), 5, 'extractSpecScan')

        outfile = printed_lines[2][len('wrote: '):]
        self.assertTrue(os.path.exists(outfile))
        os.remove(outfile)
        self.assertFalse(os.path.exists(outfile))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue64,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
