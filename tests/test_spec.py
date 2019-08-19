'''
unit tests for the spec module
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

from spec2nexus import spec, utils


# interval between file update and mtime reading
# at least a clock tick (1/60 s)
# or at least 1 second if not using float time for os.path.getmtime
SHORT_WAIT = 0.1


class Test(unittest.TestCase):
    
    def abs_data_fname(self, fname):
        return os.path.join(_path, 'spec2nexus', 'data', fname)
    
    def test_strip_first_word(self):
        self.assertEqual(utils.strip_first_word('one two three'), 'two three')
        
    def test_isSpecFileThis(self):
        self.assertFalse(spec.is_spec_file('this_does_not_exist'))
        self.assertFalse(spec.is_spec_file(os.path.join(_path, 'spec2nexus')))
        self.assertFalse(spec.is_spec_file(__file__))
        self.assertTrue( spec.is_spec_file(self.abs_data_fname('APS_spec_data.dat')))
        self.assertFalse(spec.is_spec_file_with_header('file does not exist'))
        self.assertTrue( spec.is_spec_file_with_header(self.abs_data_fname('APS_spec_data.dat')))
        self.assertFalse(spec.is_spec_file_with_header(self.abs_data_fname('spec_from_spock.spc')))
    
    def is_spec_file(self, fname):
        return spec.is_spec_file(self.abs_data_fname(fname))
        
    def test_isSpecFile(self):
        '''test all the known data files to see if they are SPEC'''
        files = {
            "33bm_spec.dat": True,
            "33id_spec.dat": True,
            "APS_spec_data.dat": True,
            "CdSe": True,
            "lmn40.spe": True,
            "YSZ011_ALDITO_Fe2O3_planar_fired_1.spc": True,
            "uxml": False,             # directory
            "README.txt": False,       # text file
            "33bm_spec.hdf5": False,
            "33id_spec.hdf5": False,
            "APS_spec_data.hdf5": False,
            "compression.h5": False,
            "Data_Q.h5": False,
            "lmn40.hdf5": False,
            "writer_1_3.h5": False,
        }
        for item, expected in files.items():
            self.assertEqual(self.is_spec_file(item), expected, item)
    
    def test_custom_exceptions(self):
        with self.assertRaises(IOError):
            raise spec.SpecDataFileNotFound()
        with self.assertRaises(IOError):
            raise spec.SpecDataFileCouldNotOpen()
        with self.assertRaises(Exception):
            raise spec.DuplicateSpecScanNumber()
        with self.assertRaises(Exception):
            raise spec.NotASpecDataFile()
        with self.assertRaises(Exception):
            raise spec.UnknownSpecFilePart()

    def test_file_initial_exceptions(self):
        with self.assertRaises(TypeError):
            spec.SpecDataFile()
        with self.assertRaises(spec.SpecDataFileNotFound):
            spec.SpecDataFile('cannot_find_this_file')
        with self.assertRaises(spec.SpecDataFileNotFound):
            spec.SpecDataFile(self.abs_data_fname('03_05_UImg.dat'))
        with self.assertRaises(spec.NotASpecDataFile):
            spec.SpecDataFile(__file__)

    def test_33bm_spec(self):
        fname = self.abs_data_fname('33bm_spec.dat')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 17)
        self.assertEqual(sfile.getMinScanNumber(), '1')
        self.assertEqual(sfile.getMaxScanNumber(), '17')
        self.assertEqual(len(sfile.getScan(1).L), 27)
        scan = sfile.getScan(1)
        self.assertEqual(scan.scanNum, '1')
        cmd = 'ascan  th 19.022 19.222  60 -20000'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
        x = 'theta'
        y = 'signal'
        self.assertEqual(scan.column_first, x)
        self.assertEqual(scan.column_last, y)
        self.assertEqual(len(scan.data[x]), 61)
        self.assertEqual(scan.data[x][0], 19.022)
        self.assertEqual(scan.data[y][0], 0.0)
        self.assertEqual(scan.data[x][-1], 19.222)
        self.assertEqual(scan.data[y][-1], 0.0)
        scan = sfile.getScan(-1)
        self.assertEqual(len(scan.positioner), 22)
        x = '2-theta'
        y = 'm22'
        keys = list(scan.positioner.keys())
        self.assertEqual(keys[0], x)
        self.assertEqual(keys[-1], y)
        self.assertEqual(scan.positioner[x], 67.78225)
        self.assertEqual(scan.positioner[y], 1230.0415)
        # TODO: apply file-specific tests (see README.txt)
        # test hklscan (#14), hklmesh (#17)

    def test_33id_spec(self):
        fname = self.abs_data_fname('33id_spec.dat')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 106)
        self.assertEqual(sfile.getFirstScanNumber(), '1')
        self.assertEqual(sfile.getMinScanNumber(), '1')
        self.assertEqual(sfile.getMaxScanNumber(), '106')
        self.assertEqual(len(sfile.getScan(1).L), 14)
        scan = sfile.getScan(1)
        self.assertEqual(scan.scanNum, '1')
        cmd = 'ascan  eta 43.6355 44.0355  40 1'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
        self.assertEqual(scan.column_first, 'eta')
        self.assertEqual(scan.column_last, 'I0')
        self.assertEqual(len(scan.positioner), 27)
        self.assertEqual(len(scan.data['eta']), 41)
        self.assertEqual(scan.data['eta'][0], 43.628)
        self.assertEqual(scan.data['I0'][0], 1224.0)
        self.assertEqual(scan.data['eta'][-1], 44.0325)
        self.assertEqual(scan.data['I0'][-1], 1222.0)
        scan = sfile.getScan(-1)
        self.assertEqual(scan.scanNum, str(106))
        self.assertEqual(len(scan.positioner), 27)
        self.assertEqual(scan.column_first, 'Energy')
        self.assertEqual(scan.column_last, 'I0')
        self.assertEqual(scan.positioner["DCM theta"], 12.747328)
        self.assertEqual(scan.positioner["ana.theta"], -0.53981253)
        # TODO: test MCA data (#1 but MCA data is all zero, need better test file) - mca_spectra_example.dat
        # test mesh (#22), Escan (#105)

    def test_APS_spec_data(self):
        '''UNICAT metadata'''
        fname = self.abs_data_fname('APS_spec_data.dat')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 20)
        self.assertEqual(sfile.getMinScanNumber(), '1')
        self.assertEqual(sfile.getMaxScanNumber(), '20')
        self.assertEqual(len(sfile.getScan(1).L), 15)
        scan = sfile.getScan(1)
        self.assertEqual(scan.scanNum, '1')
        cmd = 'ascan  mr 15.6102 15.6052  30 0.3'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
        x = 'mr'
        y = 'I0'
        self.assertEqual(scan.column_first, x)
        self.assertEqual(scan.column_last, y)
        self.assertEqual(len(scan.data[x]), 31)
        self.assertEqual(scan.data[x][0], 15.6102)
        self.assertEqual(scan.data[y][0], 222.0)
        self.assertEqual(scan.data[x][-1], 15.6052)
        self.assertEqual(scan.data[y][-1], 255.0)
        scan = sfile.getScan(-1)
        self.assertEqual(scan.scanNum, str(20))
        self.assertEqual(len(scan.positioner), 47)
        self.assertEqual(scan.column_first, "ar")
        self.assertEqual(scan.column_last, "USAXS_PD")
        self.assertEqual(scan.positioner["sa"], -8.67896)
        self.assertEqual(scan.positioner["sx_fine"], -14.4125)
        # TODO: apply file-specific tests (see README.txt)
        # uascan (#5), UNICAT metadata (#5)

    def test_CdSe(self):
        fname = self.abs_data_fname('CdSe')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 102)
        self.assertEqual(sfile.getMinScanNumber(), '1')
        self.assertEqual(sfile.getMaxScanNumber(), '102')
        self.assertEqual(len(sfile.getScan(1).L), 55)
        scan = sfile.getScan(1)
        self.assertEqual(scan.scanNum, '1')
        cmd = 'ascan  herixE -5 5  40 1'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
        x = 'HerixE'
        y = 'Seconds'
        self.assertEqual(scan.column_first, x)
        self.assertEqual(scan.column_last, y)
        self.assertEqual(len(scan.data[x]), 39)
        self.assertEqual(scan.data[x][0], -5.0137065)
        self.assertEqual(scan.data[y][0], 1.0)
        self.assertEqual(scan.data[x][-1], 4.4971428)
        self.assertEqual(scan.data[y][-1], 1.0)
        scan = sfile.getScan(-1)
        self.assertEqual(scan.scanNum, str(102))
        self.assertEqual(len(scan.positioner), 138)
        self.assertEqual(scan.column_first, "HerixE")
        self.assertEqual(scan.column_last, "Seconds")
        self.assertEqual(scan.positioner["cam-x"], 2.06)
        self.assertEqual(scan.positioner["rbs_xy"], -4.4398827)
        # TODO: apply file-specific tests (see README.txt)
        # 1-D scans (ascan), problem with scan abort on lines 5918-9, in scan 92

    def test_lmn40(self):
        fname = self.abs_data_fname('lmn40.spe')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 2) # TODO: test more here!
        self.assertEqual(len(sfile.scans), 262)
        self.assertEqual(sfile.getMinScanNumber(), '1')
        self.assertEqual(sfile.getMaxScanNumber(), '271')
        self.assertEqual(len(sfile.getScan(1).L), 9)
        scan = sfile.getScan(1)
        self.assertEqual(scan.scanNum, '1')
        cmd = 'ascan  tth -0.7 -0.5  101 1'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
        x = 'Two Theta'
        y = 'winCZT'
        self.assertEqual(scan.column_first, x)
        self.assertEqual(scan.column_last, y)
        self.assertEqual(len(scan.data[x]), 50)
        self.assertEqual(scan.data[x][0], -0.70000003)
        self.assertEqual(scan.data[y][0], 1.0)
        self.assertEqual(scan.data[x][-1], -0.60300003)
        self.assertEqual(scan.data[y][-1], 11.0)
        scan = sfile.getScan(-1)
        self.assertEqual(scan.scanNum, str(271))
        self.assertEqual(len(scan.positioner), 17)
        self.assertEqual(scan.column_first, "phi")
        self.assertEqual(scan.column_last, "NaI")
        self.assertEqual(scan.positioner["chi"], 90.000004)
        self.assertEqual(scan.positioner["Two Theta"], 0.15500001)
        # TODO: apply file-specific tests (see README.txt)
        # two #E lines, has two header sections
        # number of scans != maxScanNumber, something missing?

    def test_YSZ011_ALDITO_Fe2O3_planar_fired_1(self):
        fname = self.abs_data_fname('YSZ011_ALDITO_Fe2O3_planar_fired_1.spc')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 37)
        self.assertEqual(sfile.getMinScanNumber(), '1')
        self.assertEqual(sfile.getMaxScanNumber(), '37')
        self.assertEqual(len(sfile.getScan(1).L), 50)
        scan = sfile.getScan(1)
        self.assertEqual(scan.scanNum, '1')
        cmd = 'ascan  th 26.7108 27.1107  60 0.05'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
        x = 'theta'
        y = 'imroi1'
        self.assertEqual(scan.column_first, x)
        self.assertEqual(scan.column_last, y)
        self.assertEqual(len(scan.data[x]), 60)
        self.assertEqual(scan.data[x][0], 26.714)
        self.assertEqual(scan.data[y][0], 6.0)
        self.assertEqual(scan.data[x][-1], 27.1075)
        self.assertEqual(scan.data[y][-1], 7.0)
        scan = sfile.getScan(-1)
        self.assertEqual(scan.scanCmd, "ascan  phi -180 180  720 0.5")
        self.assertEqual(len(scan.positioner), 26)
        x = '2-theta'
        y = 'chSens'
        keys = list(scan.positioner.keys())
        self.assertEqual(keys[0], x)
        self.assertEqual(keys[-1], y)
        self.assertEqual(scan.positioner[x], 18.8)
        self.assertEqual(scan.positioner[y], 5.0)
        # TODO: apply file-specific tests (see README.txt)
        # 1-D scans, text in #V35.2 metadata (powderMotor="theta" others are float), also has #UIM control lines

    def test_extra_control_line_content__issue109(self):
        specFile = os.path.join(
            os.path.dirname(__file__), 
            'data', 
            'issue109_data.txt')
        sfile = spec.SpecDataFile(specFile)
    
        scan_number = 1
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        self.assertEqual(
            scan.T, 
            "0.5", 
            "received expected count time")

        # check scan 25, #T line said 0 seconds, but data for Seconds says 1
        scan_number = 25
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        self.assertEqual(scan.T, "0", "received expected count time")
        self.assertIn("Seco nds", scan.data, "found counting base")
        self.assertEqual(
            scan.data["Seco nds"][0], 
            1, 
            "received expected count time")
        self.assertNotEqual(
            scan.T, 
            str(scan.data["Seco nds"][0]), 
            "did not report what they were about to do")

        # check scan 11, #M line said 400000 counts
        scan_number = 11
        scan = sfile.getScan(scan_number)
        self.assertTrue(scan is not None)
        self.assertEqual(
            scan.M, 
            "400000", 
            "received expected monitor count")
        self.assertTrue(hasattr(scan, 'MCA'), "MCA found")
        self.assertIn("ROI", scan.MCA, "MCA ROI found")
        roi_dict = scan.MCA["ROI"]
        key = "FeKa(mca1 R1)"
        self.assertIn(key, roi_dict, "MCA ROI config found")
        roi = roi_dict[key]
        self.assertEqual(roi["first_chan"], 377, "MCA ROI first channel")
        self.assertEqual(roi["last_chan"], 413, "MCA ROI last channel")

        self.assertIn(key, scan.data, "MCA ROI data found")
        self.assertEqual(
            len(scan.data[key]), 
            61, 
            "embedded comment not part of data")

    def test_str(self):
        specFile = os.path.join(
            os.path.dirname(__file__), 
            'data', 
            'issue109_data.txt')
        sdf = spec.SpecDataFile(specFile)
        self.assertEqual(str(sdf), sdf.fileName)
        sdf = spec.SpecDataFile(None)
        self.assertEqual(str(sdf), 'None')


class TestFileUpdate(unittest.TestCase):

    def setUp(self):
        self.data_file = tempfile.NamedTemporaryFile(
            suffix='.dat', delete=False)
        self.data_file.close()
        file1 = os.path.join(_test_path, "tests", "data", "refresh1.txt")
        shutil.copy(file1, self.data_file.name)

    def addMoreScans(self):
        file2 = os.path.join(_test_path, "tests", "data", "refresh2.txt")
        with open(file2, "r") as fp:
            text = fp.read()
        with open(self.data_file.name, "a") as fp:
            fp.write(text)

    def tearDown(self):
        os.remove(self.data_file.name)
    
    def test_update_available(self):
        # test the ``update_available`` property
        sdf = spec.SpecDataFile(self.data_file.name)
        self.assertGreater(sdf.mtime, 0)
        self.assertFalse(sdf.update_available)
        self.assertEqual(sdf.filesize, 1837)       # OS dependent?
        self.assertEqual(sdf.last_scan, sdf.getLastScanNumber())
        self.assertEqual(sdf.last_scan, '3')

        # update the file with more data
        self.addMoreScans()
        time.sleep(SHORT_WAIT)

        self.assertTrue(sdf.update_available)
    
    def test_refresh(self):
        sdf = spec.SpecDataFile(self.data_file.name)
        self.assertNotEqual(sdf.last_scan, None)
        self.assertEqual(len(sdf.getScanNumbers()), 3)
        self.assertEqual(sdf.filesize, 1837)       # OS dependent?

        # update the file with more data
        self.addMoreScans()
        time.sleep(SHORT_WAIT)

        scan_number = sdf.refresh()
        self.assertGreater(sdf.filesize, 1837)
        self.assertEqual(len(sdf.getScanNumbers()), 5)
        self.assertNotEqual(scan_number, None)
        self.assertNotEqual(sdf.last_scan, None)
        self.assertNotEqual(scan_number, sdf.last_scan)
        self.assertNotEqual(scan_number, sdf.getLastScanNumber())
        self.assertEqual(sdf.last_scan, sdf.getLastScanNumber())

        time.sleep(SHORT_WAIT)
        scan_number = sdf.refresh()
        self.assertEqual(scan_number, None)
        self.assertEqual(len(sdf.getScanNumbers()), 5)


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Test,
        TestFileUpdate,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
