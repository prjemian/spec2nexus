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

import os
import shutil
import sys
import tempfile
import time
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import specplot

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


class TestFileUpdate(unittest.TestCase):

    def setUp(self):
        self.data_file = tempfile.NamedTemporaryFile(
            suffix='.dat', delete=False)
        self.data_file.close()
        file1 = os.path.join(_test_path, "tests", "data", "refresh1.txt")
        shutil.copy(file1, self.data_file.name)
        
        self.tempdir = tempfile.mkdtemp()

    def addMoreScans(self):
        file2 = os.path.join(_test_path, "tests", "data", "refresh2.txt")
        with open(file2, "r") as fp:
            text = fp.read()
        with open(self.data_file.name, "a") as fp:
            fp.write(text)

    def tearDown(self):
        os.remove(self.data_file.name)
        shutil.rmtree(self.tempdir, ignore_errors=True)
    
    def test_refresh(self):
        plot = os.path.join(self.tempdir, 'plot.svg')
        plot2 = os.path.join(self.tempdir, 'plot2.svg')

        sdf = specplot.openSpecFile(self.data_file.name)
        scan = sdf.getScan(3)
        plotter = specplot.LinePlotter()

        # plot the first data
        plotter.plot_scan(scan, plot)
        self.assertTrue(os.path.exists(plot))
        plotsize = os.path.getsize(plot)
        mtime = os.path.getmtime(plot)
        self.assertGreater(plotsize, 0)
        self.assertGreater(mtime, 0)
        
        for iter in range(2):
            scan_number = sdf.refresh()
            if scan_number is None:
                scan = sdf.getScan(3)
                self.assertTrue(scan.__interpreted__)
                # update the file with more data
                self.addMoreScans()
                time.sleep(0.1)
            else:
                scan = sdf.getScan(3)
                self.assertFalse(scan.__interpreted__)
                plotter.plot_scan(scan, plot2)
                self.assertTrue(os.path.exists(plot2))
                self.assertGreater(os.path.getmtime(plot2), mtime)
                self.assertNotEqual(os.path.getsize(plot2), plotsize)


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue_66_plotting_problems,
        TestFileUpdate,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
