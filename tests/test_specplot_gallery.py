'''
unit tests for the specplot module
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import unittest
import os, sys
import shutil
import tempfile

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)
from spec2nexus import specplot_gallery, spec

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class SpecPlotGallery(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.join(_path, 'spec2nexus')
        self.datapath = os.path.join(self.basepath, 'data')
        self.tempdir = tempfile.mkdtemp()
        sys.argv = [sys.argv[0],]

    def tearDown(self):
        if os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)
            self.tempdir = None

#     def testName(self):
#         pass
    
    def abs_data_fname(self, fname):
        return os.path.join(self.datapath, fname)
    
    def test_command_line_NeXus_writer_1_3(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('writer_1_3.h5'))
        self.assertRaises(
            spec.NotASpecDataFile,
            specplot_gallery.main)
    
    def test_command_line_spec_data_file_list(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        # lmn40.spe, from 1999, has 271 scans, some hklmesh, takes 2 minutes to process!
        for item in '02_03_setup.dat 03_06_JanTest.dat user6idd.dat 33bm_spec.dat'.split():
            sys.argv.append(self.abs_data_fname(item))
        specplot_gallery.main()

        self.assertTrue(os.path.exists(os.path.join(self.tempdir, 'mtime_cache.txt')))
        # TODO: test contents of mtime_cache.txt?

#         self.assertTrue(os.path.exists(os.path.join(self.tempdir, '1999', '02', 'lmn40', 'lmn40.spe')))
#         self.assertTrue(os.path.exists(os.path.join(self.tempdir, '1999', '02', 'lmn40', 'index.html')))

        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2010', '06', '33bm_spec', '33bm_spec.dat')))
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2010', '06', '33bm_spec', 'index.html')))

        # S1 aborted, S2 all X,Y are 0,0
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2013', '10', 'user6idd', 'user6idd.dat')))
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2013', '10', 'user6idd', 'index.html')))

        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2014', '03', '03_06_JanTest', '03_06_JanTest.dat')))
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2014', '03', '03_06_JanTest', 'index.html')))
        # TODO: image file name _will_ change
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2014', '03', '03_06_JanTest', 's1.png')))

        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2016', '02', '02_03_setup', '02_03_setup.dat')))
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, '2016', '02', '02_03_setup', 'index.html')))

        # TODO: tests?
        _break = True


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        SpecPlotGallery,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
