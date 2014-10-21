'''
unit tests for the spec module
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import unittest
from spec2nexus import spec, utils
import os


class Test(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.datapath = os.path.join(self.basepath, 'data')

#     def tearDown(self):
#         pass

#     def testName(self):
#         pass

        # TODO: apply principle of one test per one possibility
    
    def abs_data_fname(self, fname):
        return os.path.join(self.datapath, fname)
    
    def test_strip_first_word(self):
        self.assertEqual(utils.strip_first_word('one two three'), 'two three')
        
    def test_isSpecFileThis(self):
        self.assertFalse(spec.is_spec_file('this_does_not_exist'))
        self.assertFalse(spec.is_spec_file(self.basepath))
        self.assertFalse(spec.is_spec_file(__file__))
        self.assertTrue( spec.is_spec_file(self.abs_data_fname('APS_spec_data.dat')))
    
    def is_spec_file(self, fname):
        return spec.is_spec_file(self.abs_data_fname(fname))
        
    def test_isSpecFile(self):
        '''test all the known data files to see if they are SPEC'''
        self.assertTrue( self.is_spec_file('33bm_spec.dat'))
        self.assertTrue( self.is_spec_file('33id_spec.dat'))
        self.assertTrue( self.is_spec_file('APS_spec_data.dat'))
        self.assertTrue( self.is_spec_file('CdSe'))
        self.assertTrue( self.is_spec_file('lmn40.spe'))
        self.assertTrue( self.is_spec_file('YSZ011_ALDITO_Fe2O3_planar_fired_1.spc'))
        self.assertFalse(self.is_spec_file('uxml'))             # directory
        self.assertFalse(self.is_spec_file('README.txt'))       # text file
        self.assertFalse(self.is_spec_file('33bm_spec.hdf5'))
        self.assertFalse(self.is_spec_file('33id_spec.hdf5'))
        self.assertFalse(self.is_spec_file('APS_spec_data.hdf5'))
        self.assertFalse(self.is_spec_file('compression.h5'))
        self.assertFalse(self.is_spec_file('Data_Q.h5'))
        self.assertFalse(self.is_spec_file('lmn40.hdf5'))
        self.assertFalse(self.is_spec_file('writer_1_3.h5'))
    
    def cannot_find_spec_data_file(self):
        spec.SpecDataFile('cannot_find_this_file')
    
    def not_a_spec_data_file(self):
        spec.SpecDataFile(__file__)
    
    def test_custom_exceptions(self):
        self.assertRaises(Exception, spec.SpecDataFileNotFound())
        self.assertRaises(Exception, spec.SpecDataFileCouldNotOpen())
        self.assertRaises(Exception, spec.DuplicateSpecScanNumber())
        self.assertRaises(Exception, spec.NotASpecDataFile())
        self.assertRaises(Exception, spec.UnknownSpecFilePart())

    def spec_data_file(self):
        spec.SpecDataFile(self.abs_data_fname('03_05_UImg.dat'))

    def test_file_initial_exceptions(self):
        self.assertRaises(TypeError, spec.SpecDataFile)
        self.assertRaises(spec.SpecDataFileNotFound, self.cannot_find_spec_data_file)
        self.assertRaises(spec.NotASpecDataFile, self.not_a_spec_data_file)

    def test_33bm_spec(self):
        fname = self.abs_data_fname('33bm_spec.dat')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 17)
        self.assertEqual(sfile.getMinScanNumber(), 1)
        self.assertEqual(sfile.getMaxScanNumber(), 17)
        self.assertEqual(len(sfile.getScan(1).L), 27)
        scan = sfile.scans[1]
        self.assertEqual(scan.scanNum, 1)
        cmd = 'ascan  th 19.022 19.222  60 -20000'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
#         x = 'theta'
#         y = 'signal'
#         self.assertEqual(scan.column_first, x)
#         self.assertEqual(scan.column_last, y)
#         self.assertEqual(len(scan.data[x]), 61)
#         self.assertEqual(scan.data[x][0], 19.022)
#         self.assertEqual(scan.data[y][0], 0.0)
#         self.assertEqual(scan.data[x][-1], 19.222)
#         self.assertEqual(scan.data[y][-1], 0.0)
#         scan = sfile.getScan(-1)
#         self.assertEqual(len(scan.positioner), 22)
#         x = 'yt3'
#         y = 'zt1'
#         self.assertEqual(scan.positioner.keys()[0], x)
#         self.assertEqual(scan.positioner.keys()[-1], y)
#         self.assertEqual(scan.positioner[x], 0.499275)
#         self.assertEqual(scan.positioner[y], -113.52071)
        # TODO: apply file-specific tests (see README.txt)
        # test hklscan (#14), hklmesh (#17)

    def test_33id_spec(self):
        fname = self.abs_data_fname('33id_spec.dat')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 106)
        self.assertEqual(sfile.getMinScanNumber(), 1)
        self.assertEqual(sfile.getMaxScanNumber(), 106)
        self.assertEqual(len(sfile.getScan(1).L), 14)
        scan = sfile.scans[1]
        self.assertEqual(scan.scanNum, 1)
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
        self.assertEqual(len(scan.positioner), 27)
        x = 'a2Theta'
        y = 'slitmb'
        self.assertEqual(scan.positioner.keys()[0], x)
        self.assertEqual(scan.positioner.keys()[-1], y)
        self.assertEqual(scan.positioner[x], 0.0)
        self.assertEqual(scan.positioner[y], 2.4003)
        # TODO: test MCA data (#1 but MCA data is all zero, need better test file)
        # test mesh (#22), Escan (#105)

    def test_APS_spec_data(self):
        '''UNICAT metadata'''
        fname = self.abs_data_fname('APS_spec_data.dat')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 20)
        self.assertEqual(sfile.getMinScanNumber(), 1)
        self.assertEqual(sfile.getMaxScanNumber(), 20)
        self.assertEqual(len(sfile.getScan(1).L), 15)
        scan = sfile.scans[1]
        self.assertEqual(scan.scanNum, 1)
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
        self.assertEqual(len(scan.positioner), 47)
        x = 'a1t'
        y = 'mx'
        self.assertEqual(scan.positioner.keys()[0], x)
        self.assertEqual(scan.positioner.keys()[-1], y)
        self.assertEqual(scan.positioner[x], 3.03)
        self.assertEqual(scan.positioner[y], 24.0)
        # TODO: apply file-specific tests (see README.txt)
        # uascan (#5), UNICAT metadata (#5)

    def test_CdSe(self):
        fname = self.abs_data_fname('CdSe')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 102)
        self.assertEqual(sfile.getMinScanNumber(), 1)
        self.assertEqual(sfile.getMaxScanNumber(), 102)
        self.assertEqual(len(sfile.getScan(1).L), 55)
        scan = sfile.scans[1]
        self.assertEqual(scan.scanNum, 1)
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
        self.assertEqual(len(scan.positioner), 136)
        x = 'focus'
        y = 'bslhc'
        self.assertEqual(scan.positioner.keys()[0], x)
        self.assertEqual(scan.positioner.keys()[-1], y)
        self.assertEqual(scan.positioner[x], -2.83)
        self.assertEqual(scan.positioner[y], 0.6)
        # TODO: apply file-specific tests (see README.txt)
        # 1-D scans (ascan), problem with scan abort on lines 5918-9, in scan 92

    def test_lmn40(self):
        fname = self.abs_data_fname('lmn40.spe')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 2) # TODO: test more here!
        self.assertEqual(len(sfile.scans), 262)
        self.assertEqual(sfile.getMinScanNumber(), 1)
        self.assertEqual(sfile.getMaxScanNumber(), 271)
        self.assertEqual(len(sfile.getScan(1).L), 9)
        scan = sfile.scans[1]
        self.assertEqual(scan.scanNum, 1)
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
        self.assertEqual(len(scan.positioner), 12)
        x = 'Wheel'
        y = 'dslit'
        self.assertEqual(scan.positioner.keys()[0], x)
        self.assertEqual(scan.positioner.keys()[-1], y)
        self.assertEqual(scan.positioner[x], -2.05)
        self.assertEqual(scan.positioner[y], 0.0)
        # TODO: apply file-specific tests (see README.txt)
        # two #E lines, has two header sections
        # number of scans != maxScanNumber, something missing?

    def test_YSZ011_ALDITO_Fe2O3_planar_fired_1(self):
        fname = self.abs_data_fname('YSZ011_ALDITO_Fe2O3_planar_fired_1.spc')
        sfile = spec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)
        self.assertEqual(len(sfile.headers), 1)
        self.assertEqual(len(sfile.scans), 37)
        self.assertEqual(sfile.getMinScanNumber(), 1)
        self.assertEqual(sfile.getMaxScanNumber(), 37)
        self.assertEqual(len(sfile.getScan(1).L), 50)
        scan = sfile.scans[1]
        self.assertEqual(scan.scanNum, 1)
        cmd = 'ascan  th 26.7108 27.1107  60 0.05'
        self.assertEqual(scan.scanCmd, cmd)
        self.assertEqual(sfile.getScanCommands([1,]), ['#S 1 '+cmd,])
#         x = 'theta'
#         y = 'imroi1'
#         self.assertEqual(scan.column_first, x)
#         self.assertEqual(scan.column_last, y)
#         self.assertEqual(len(scan.data[x]), 60)
#         self.assertEqual(scan.data[x][0], 26.714)
#         self.assertEqual(scan.data[y][0], 6.0)
#         self.assertEqual(scan.data[x][-1], 27.1075)
#         self.assertEqual(scan.data[y][-1], 7.0)
#         scan = sfile.getScan(-1)
#         self.assertEqual(len(scan.positioner), 26)
#         x = 'yt2'
#         y = 'wst'
#         self.assertEqual(scan.positioner.keys()[0], x)
#         self.assertEqual(scan.positioner.keys()[-1], y)
#         self.assertEqual(scan.positioner[x], -6.25e-05)
#         self.assertEqual(scan.positioner[y], 2.9999031)
        # TODO: apply file-specific tests (see README.txt)
        # 1-D scans, text in #V35.2 metadata (powderMotor="theta" others are float), also has #UIM control lines


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
