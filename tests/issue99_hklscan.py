
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
import shutil
import sys
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

import spec2nexus.specplot
import spec2nexus.spec

import tests.common


class Issue99(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(spec2nexus.spec.__file__)
        self.testfile = os.path.join(path, 'data', 'lmn40.spe')
        self.sys_argv0 = sys.argv[0]

    def tearDown(self):
        sys.argv = [self.sys_argv0,]

    def test_specplot_lmn40_scan64(self):
        scan_number = 64
        expected_x_title = 'L'

        sfile = spec2nexus.specplot.openSpecFile(self.testfile)
        self.assertTrue(isinstance(sfile, spec2nexus.spec.SpecDataFile))

        scan = sfile.getScan(scan_number)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))

        image_maker = spec2nexus.specplot.Selector().auto(scan)
        self.assertTrue(issubclass(image_maker, spec2nexus.specplot.ImageMaker))

        plotter = image_maker()
        self.assertTrue(isinstance(plotter, spec2nexus.specplot.HKLScanPlotter))

        plotter.scan = scan
        plotter.set_plot_title(plotter.plot_title() or plotter.data_file_name())
        plotter.set_plot_subtitle(
            plotter.plot_subtitle() or 
            '#' + str(plotter.scan.scanNum) + ': ' + plotter.scan.scanCmd)
        plotter.set_timestamp(plotter.timestamp() or plotter.scan.date)

        plotter.retrieve_plot_data()
        plotter.plot_options()

        self.assertTrue(plotter.plottable())
        self.assertEqual(plotter.x_title(), expected_x_title)
        self.assertEqual(plotter.y_title(), plotter.signal)
        self.assertEqual(plotter.x_log(), False)
        self.assertEqual(plotter.y_log(), False)
        self.assertEqual(plotter.z_log(), False)
        self.assertTrue(plotter.plot_subtitle().startswith('#'+str(scan_number)))

    def test_specplot_lmn40_scan244(self):
        'watch out for IndexError: list index out of range'
        scan_number = 244
        expected_x_title = 'data point number (hkl all held constant)'

        sfile = spec2nexus.specplot.openSpecFile(self.testfile)
        self.assertTrue(isinstance(sfile, spec2nexus.spec.SpecDataFile))

        scan = sfile.getScan(scan_number)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))

        image_maker = spec2nexus.specplot.Selector().auto(scan)
        self.assertTrue(issubclass(image_maker, spec2nexus.specplot.ImageMaker))

        plotter = image_maker()
        self.assertTrue(isinstance(plotter, spec2nexus.specplot.HKLScanPlotter))

        plotter.scan = scan
        plotter.set_plot_title(plotter.plot_title() or plotter.data_file_name())
        plotter.set_plot_subtitle(
            plotter.plot_subtitle() or 
            '#' + str(plotter.scan.scanNum) + ': ' + plotter.scan.scanCmd)
        plotter.set_timestamp(plotter.timestamp() or plotter.scan.date)

        plotter.retrieve_plot_data()
        plotter.plot_options()

        self.assertTrue(plotter.plottable())
        self.assertEqual(plotter.x_title(), expected_x_title)
        self.assertEqual(plotter.y_title(), plotter.signal)
        self.assertEqual(plotter.x_log(), False)
        self.assertEqual(plotter.y_log(), False)
        self.assertEqual(plotter.z_log(), False)
        self.assertTrue(plotter.plot_subtitle().startswith('#'+str(scan_number)))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue99,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
