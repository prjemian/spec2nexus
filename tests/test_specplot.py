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

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)
from spec2nexus import specplot

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class Handler_Log_lin_Plot(specplot.MacroPlotHandler):
    '''
    custom log-lin plot
    '''
    # TODO: too much work - simplify!
    
    def get_y_log(self):
        'override'
        return True


class Issue_66_plotting_problems(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.join(_path, 'spec2nexus')
        self.datapath = os.path.join(self.basepath, 'data')
        self.plotFile = tests.common.create_test_file(suffix='.png')

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
        plotter = specplot.Plotter()

        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        self.assertRaises(
            specplot.ScanAborted, 
            plotter.plot_scan,
            scan,
            self.plotFile)
        self.assertFalse(os.path.exists(self.plotFile))
        
    def test_y_values_all_zero_lin_lin(self):
        specFile = os.path.join('data', 'issue64_data.txt')
        scan_number = 50

        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        plotter = specplot.Plotter()

        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        plotter.plot_scan(scan, self.plotFile)
        self.assertTrue(os.path.exists(self.plotFile))
        
    def test_y_values_all_zero_log_lin(self):
        specFile = os.path.join('data', 'issue64_data.txt')
        scan_number = 50

        sfile = specplot.openSpecFile(specFile)
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        plotter = specplot.Plotter()
        # TODO: configure for log-lin plot
        
        handler = Handler_Log_lin_Plot()
        handler.macro = scan.get_macro_name()
        plotter.registry.db[handler.macro] = handler

        if os.path.exists(self.plotFile):   # always re-create this plot for testing
            os.remove(self.plotFile)
        self.assertRaises(
            ValueError, 
            plotter.plot_scan,
            scan,
            self.plotFile, 
            ylog=True)
        self.assertFalse(os.path.exists(self.plotFile))


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
