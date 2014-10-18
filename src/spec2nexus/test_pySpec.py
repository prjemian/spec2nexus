'''
unit tests for the pySpec module
'''

import unittest
import pySpec
import os


class Test(unittest.TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def testName(self):
#         pass
    
    def test_strip_first_word(self):
        self.assertEqual(pySpec.strip_first_word('one two three'), 'two three')
        
    def test_isSpecFileThis(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        self.assertTrue(pySpec.is_spec_file(os.path.join(path, '03_05_UImg.dat')))
    
    def is_spec_file(self, path, fname):
        return pySpec.is_spec_file(os.path.join(path, fname))
        
    def test_isSpecFile(self):
        '''test all the known data files to see if they are SPEC'''
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        self.assertTrue( self.is_spec_file(path, '03_05_UImg.dat'))
        self.assertTrue( self.is_spec_file(path, '130123B_2.spc'))
        self.assertTrue( self.is_spec_file(path, '33bm_spec.dat'))
        self.assertTrue( self.is_spec_file(path, '33id_spec.dat'))
        self.assertTrue( self.is_spec_file(path, 'APS_spec_data.dat'))
        self.assertTrue( self.is_spec_file(path, 'CdSe'))
        self.assertTrue( self.is_spec_file(path, 'lmn40.spe'))
        self.assertTrue( self.is_spec_file(path, 'YSZ011_ALDITO_Fe2O3_planar_fired_1.spc'))
        self.assertFalse(self.is_spec_file(path, '33bm_spec.hdf5'))
        self.assertFalse(self.is_spec_file(path, '33id_spec.hdf5'))
        self.assertFalse(self.is_spec_file(path, 'APS_spec_data.hdf5'))
        self.assertFalse(self.is_spec_file(path, 'compression.h5'))
        self.assertFalse(self.is_spec_file(path, 'Data_Q.h5'))
        self.assertFalse(self.is_spec_file(path, 'lmn40.hdf5'))
        self.assertFalse(self.is_spec_file(path, 'README.txt'))
        self.assertFalse(self.is_spec_file(path, 'uxml'))
        self.assertFalse(self.is_spec_file(path, 'writer_1_3.h5'))
    
    def cannot_find_spec_data_file(self):
        pySpec.SpecDataFile('cannot_find_this_file')
    
    def not_a_spec_data_file(self):
        pySpec.SpecDataFile(__file__)
    
    def spec_data_file(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        fname = os.path.join(path, '03_05_UImg.dat')
        pySpec.SpecDataFile(fname)

    def test_file_initial_exceptions(self):
        self.assertRaises(TypeError, pySpec.SpecDataFile)
        self.assertRaises(pySpec.SpecDataFileNotFound, self.cannot_find_spec_data_file)
        self.assertRaises(pySpec.NotASpecDataFile, self.not_a_spec_data_file)

    def test_file(self):
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data'))
        fname = os.path.join(path, 'APS_spec_data.dat')
        sfile = pySpec.SpecDataFile(fname)
        self.assertEqual(sfile.fileName, fname)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
