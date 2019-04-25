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

import unittest
import os, sys
import shutil
import tempfile

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)
from spec2nexus import specplot

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class Issue_66_plotting_problems(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.join(_path, 'spec2nexus')
        self.datapath = os.path.join(self.basepath, 'data')
        self.plotFile = tests.common.create_test_file(suffix='.png')
        sys.argv = [sys.argv[0],]

    def tearDown(self):
        if os.path.exists(self.plotFile):
            os.remove(self.plotFile)

#     def testName(self):
#         pass
    
    def abs_data_fname(self, fname):
        return os.path.join(self.datapath, fname)
         
    def test_scan_aborted_after_0_points(self):
        specFile = self.abs_data_fname('33bm_spec.dat')
        scan_number = 15
     
        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        plotter = specplot.LinePlotter()
     
        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
             
        self.assertRaises(
            specplot.NoDataToPlot, 
            plotter.plot_scan, 
            scan, 
            self.plotFile
            )
             
        self.assertFalse(os.path.exists(self.plotFile))
             
    def test_y_values_all_zero_lin_lin(self):
        specFile = os.path.join(os.path.dirname(__file__), 'data', 'issue64_data.txt')
        scan_number = 50
     
        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        plotter = specplot.LinePlotter()
     
        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        plotter.plot_scan(scan, self.plotFile)
        self.assertTrue(os.path.exists(self.plotFile))
             
    def test_y_values_all_zero_log_lin(self):
        specFile = os.path.join(os.path.dirname(__file__), 'data', 'issue64_data.txt')
        scan_number = 50
     
        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        plotter = specplot.LinePlotter()
     
        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        plotter.set_y_log(True)
        self.assertRaises(
            ValueError, 
            plotter.plot_scan,
            scan,
            self.plotFile)
        self.assertFalse(os.path.exists(self.plotFile))
         
    def test_command_line(self):
        tempdir = tempfile.mkdtemp()
        specFile = self.abs_data_fname('02_03_setup.dat')
        plotFile = os.path.join(tempdir, 'image.png')
        sys.argv = [sys.argv[0], specFile, '1', plotFile]
        specplot.main()
        self.assertTrue(os.path.exists(plotFile))
        shutil.rmtree(tempdir, ignore_errors=True)
        self.assertFalse(os.path.exists(plotFile))
         
    def test_command_line_33bm_spec_issue72_hklmesh_plot(self):
        # mesh:    data/33id_spec.dat  scan 22
        # hklmesh: data/33bm_spec.dat  scan 17
        tempdir = tempfile.mkdtemp()
     
        specFile = self.abs_data_fname('33bm_spec.dat')
        scan_number = 17        # hklmesh
     
        plotFile = os.path.join(tempdir, 'image.png')
        sys.argv = [sys.argv[0], specFile, str(scan_number), plotFile]
     
        specplot.main()
     
        self.assertTrue(os.path.exists(self.plotFile))
        shutil.rmtree(tempdir)
        self.assertFalse(os.path.exists(plotFile))
         
    def test_command_line_33id_spec_issue72_mesh_plot(self):
        # mesh:    data/33id_spec.dat  scan 22
        # hklmesh: data/33bm_spec.dat  scan 17
        tempdir = tempfile.mkdtemp()
      
        specFile = self.abs_data_fname('33id_spec.dat')
        scan_number = 22        # mesh
      
        plotFile = os.path.join(tempdir, 'image.png')
        sys.argv = [sys.argv[0], specFile, str(scan_number), plotFile]
      
        specplot.main()
      
        self.assertTrue(os.path.exists(self.plotFile))
        shutil.rmtree(tempdir)
        self.assertFalse(os.path.exists(plotFile))
         
    def test_command_line_33bm_spec_issue80_hklscan_plot(self):
        # #80: hklscan, l was scanned, scans 14 & 16
        tempdir = tempfile.mkdtemp()
     
        specFile = self.abs_data_fname('33bm_spec.dat')
        scan_number = 14        # hklmesh
     
        plotFile = os.path.join(tempdir, 'image.png')
        sys.argv = [sys.argv[0], specFile, str(scan_number), plotFile]
     
        specplot.main()
     
        self.assertTrue(os.path.exists(self.plotFile))
        shutil.rmtree(tempdir)
        self.assertFalse(os.path.exists(plotFile))
            
    def test_one_line_mesh_scan_as_1D_plot_issue82(self):
        specFile = os.path.join(os.path.dirname(__file__), 'data', 'issue82_data.txt')
        scan_number = 17
    
        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
    
        image_maker = specplot.Selector().auto(scan)
        self.assertTrue(issubclass(image_maker, specplot.ImageMaker))
    
        plotter = image_maker()
        self.assertTrue(isinstance(plotter, specplot.MeshPlotter))
    
        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        plotter.plot_scan(scan, self.plotFile)
        self.assertTrue(os.path.exists(self.plotFile))
         
    def test_one_line_mesh_scan_type_error_33id_29(self):
        specFile = self.abs_data_fname('33id_spec.dat')
        scan_number = 29
 
        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
 
        image_maker = specplot.Selector().auto(scan)
        self.assertTrue(issubclass(image_maker, specplot.ImageMaker))
 
        plotter = image_maker()
        self.assertTrue(isinstance(plotter, specplot.MeshPlotter))
 
        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        plotter.plot_scan(scan, self.plotFile)
        self.assertTrue(os.path.exists(self.plotFile))
        
    def test_40x35_grid_shown_properly_lmn40_spe(self):
        specFile = self.abs_data_fname('lmn40.spe')
        scan_number = 14

        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)

        image_maker = specplot.Selector().auto(scan)
        self.assertTrue(issubclass(image_maker, specplot.ImageMaker))

        plotter = image_maker()
        self.assertTrue(isinstance(plotter, specplot.MeshPlotter))

        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        plotter.plot_scan(scan, self.plotFile)
        self.assertTrue(os.path.exists(self.plotFile))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue_66_plotting_problems,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
