'''
unit tests for the specplot module
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

import logging
import os, sys
import shutil
import tempfile
import unittest


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
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        if os.path.exists(self.tempdir):
            logging.shutdown()
            shutil.rmtree(self.tempdir)
            self.tempdir = None
        logging.disable(logging.NOTSET)

#     def testName(self):
#         pass
    
    def abs_data_fname(self, fname):
        return os.path.join(self.datapath, fname)
    
    def test_command_line_NeXus_writer_1_3(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('writer_1_3.h5'))
        specplot_gallery.main()
        # this is HDF5 file, not SPEC, so not much content
        children = os.listdir(self.tempdir)
        self.assertEqual(len(children), 1)
        self.assertEqual(children[0], 'specplot_files_processing.log')
    
    def test_command_line_spec_data_file_33bm_spec(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('33bm_spec.dat'))
        specplot_gallery.main()
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, 'mtime_cache.txt')))
        # TODO: test contents of mtime_cache.txt?

        plotDir = os.path.join(self.tempdir, '2010', '06', '33bm_spec')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '33bm_spec.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: #69: look for handling of scan 15
    
    def test_command_line_spec_data_file_user6idd(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('user6idd.dat'))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, 'mtime_cache.txt')))
 
        # S1 aborted, S2 all X,Y are 0,0
        plotDir = os.path.join(self.tempdir, '2013', '10', 'user6idd')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'user6idd.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: #69: look for handling of scan 1
 
    def test_command_line_spec_data_file_03_06_JanTest(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('03_06_JanTest.dat'))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, 'mtime_cache.txt')))
 
        # S1 aborted, S2 all X,Y are 0,0
        plotDir = os.path.join(self.tempdir, '2014', '03', '03_06_JanTest')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '03_06_JanTest.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 's00001.png')))
        # TODO: #69: look for handling of scan 1
        self.assertFalse(os.path.exists(os.path.join(plotDir, 's1.png')))
        # TODO: look for that scan in index.html?
     
    def test_command_line_spec_data_file_02_03_setup(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('02_03_setup.dat'))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, 'mtime_cache.txt')))
 
        plotDir = os.path.join(self.tempdir, '2016', '02', '02_03_setup')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '02_03_setup.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: #69: look for handling of scan 5
     
    def test_command_line_spec_data_file_list(self):
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        for item in 'user6idd.dat APS_spec_data.dat 02_03_setup.dat'.split():
            sys.argv.append(self.abs_data_fname(item))
        specplot_gallery.main()
 
        self.assertTrue(os.path.exists(os.path.join(self.tempdir, 'mtime_cache.txt')))
 
        plotDir = os.path.join(self.tempdir, '2010', '11', 'APS_spec_data')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'APS_spec_data.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: test the order of plots in the index.html
 
        plotDir = os.path.join(self.tempdir, '2013', '10', 'user6idd')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'user6idd.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
 
        plotDir = os.path.join(self.tempdir, '2016', '02', '02_03_setup')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, '02_03_setup.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
     
    def test_command_line_spec_data_file_list_reversed_chronological_issue_79(self):
        sys.argv.append('-r')
        sys.argv.append('-d')
        self.assertTrue(os.path.exists(self.tempdir))
        sys.argv.append(self.tempdir)
        sys.argv.append(self.abs_data_fname('APS_spec_data.dat'))
        specplot_gallery.main()

        plotDir = os.path.join(self.tempdir, '2010', '11', 'APS_spec_data')
        self.assertTrue(os.path.exists(plotDir))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'APS_spec_data.dat')))
        self.assertTrue(os.path.exists(os.path.join(plotDir, 'index.html')))
        # TODO: test the order of plots in the index.html, reversed

    def test_command_line_specified_directory_not_found_issue_98(self):
        sys.argv.append('-d')
        sys.argv.append("Goofball-directory_does_not_exist")
        sys.argv.append(self.abs_data_fname('APS_spec_data.dat'))
        self.assertRaises(specplot_gallery.DirectoryNotFoundError, specplot_gallery.main)

    def test_command_line_specified_directory_fails_isdir_issue_98(self):
        text_file_name = os.path.join(self.tempdir, 'goofball.txt')
        outp = open(text_file_name, 'w')
        outp.write('goofball text is not a directory')
        outp.close()
        sys.argv.append('-d')
        sys.argv.append(text_file_name)
        sys.argv.append(self.abs_data_fname('APS_spec_data.dat'))
        self.assertRaises(specplot_gallery.PathIsNotDirectoryError, specplot_gallery.main)


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        SpecPlotGallery,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner(verbosity=2)
    runner.run(suite())
