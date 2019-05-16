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

import os
import shutil
import sys
import tempfile
import unittest

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

from spec2nexus import nexus

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class TestNexus(unittest.TestCase):

    def setUp(self):
        self._owd = os.getcwd()
        self.data_path = os.path.join(os.path.dirname(nexus.__file__), "data")
        self.sys_argv0 = sys.argv[0]
        self.tempdir = tempfile.mkdtemp()
        os.chdir(self.tempdir)

        self.test_files = {
            "02_03_setup.dat":          "-f --verbose   -s 46",
            "33id_spec.dat":            "-f --verbose   -s 1",
            "spectra_example.dat":      "-f --verbose   -s 1",
            "mca_spectra_example.dat":  "-f --verbose   -s 1",
            "xpcs_plugin_sample.spec":  "-f --verbose   -s 1",
            }

    def tearDown(self):
        sys.argv = [self.sys_argv0,]
        if os.path.exists(self._owd):
            os.chdir(self._owd)
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir, ignore_errors=True)

    def test_trivial(self):
        self.assertTrue(True, "trivial assertion - always True")
        
        for fn, args in self.test_files.items():
            shutil.copy2(os.path.join(self.data_path, fn), self.tempdir)
            cmd = fn + "  " + args
            sys.argv = [self.sys_argv0,] + [cmd for cmd in args.split()]

            # FIXME: nexus.main()
            # pydev debugger: starting (pid: 14288)
            # usage: spec2nexus [-h] [-e HDF5_EXTENSION] [-f] [-v] [-s SCAN_LIST]
            #                   [--quiet | --verbose]
            #                   infile [infile ...]
            # spec2nexus: error: the following arguments are required: infile
            # E
            # ======================================================================
            # ERROR: test_trivial (__main__.TestNexus)
            # ----------------------------------------------------------------------
            # Traceback (most recent call last):
            #   File "C:\Users\Pete\Documents\eclipse\spec2nexus\tests\test_nexus.py", line 65, in test_trivial
            #     nexus.main()
            #   File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\nexus.py", line 159, in main
            #     user_parms = get_user_parameters()
            #   File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\nexus.py", line 112, in get_user_parameters
            #     return parser.parse_args()
            #   File "C:\Users\Pete\Apps\Anaconda\lib\argparse.py", line 1734, in parse_args
            #     args, argv = self.parse_known_args(args, namespace)
            #   File "C:\Users\Pete\Apps\Anaconda\lib\argparse.py", line 1766, in parse_known_args
            #     namespace, args = self._parse_known_args(args, namespace)
            #   File "C:\Users\Pete\Apps\Anaconda\lib\argparse.py", line 2001, in _parse_known_args
            #     ', '.join(required_actions))
            #   File "C:\Users\Pete\Apps\Anaconda\lib\argparse.py", line 2393, in error
            #     self.exit(2, _('%(prog)s: error: %(message)s\n') % args)
            #   File "C:\Users\Pete\Apps\Anaconda\lib\argparse.py", line 2380, in exit
            #     _sys.exit(status)
            # SystemExit: 2
            # 
            # ----------------------------------------------------------------------
            # Ran 1 test in 80.857s
            # 
            # FAILED (errors=1)


def suite(*args, **kw):
    test_list = [
        TestNexus,
        ]

    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
