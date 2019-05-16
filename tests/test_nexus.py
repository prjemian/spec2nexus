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
            "spec_from_spock.spc":      "-f --verbose   -s 116",
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
            _argv = sys.argv = [self.sys_argv0,] + [c for c in cmd.split()]

            print(f"Testing NeXus conversion of SPEC data file: {fn}")
            nexus.main()


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
