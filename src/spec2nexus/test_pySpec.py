'''
unit tests for the pySpec module
'''
import unittest
import pySpec


class Test(unittest.TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def testName(self):
#         pass
    
    def test_strip_first_word(self):
        self.assertEqual(pySpec.strip_first_word('one two three'), 'two three')
    
    def cannot_find_spec_data_file(self):
        pySpec.SpecDataFile('cannot_find_this_file')
    
    def not_a_spec_data_file(self):
        pySpec.SpecDataFile(__file__)

    def test_file(self):
        self.assertRaises(TypeError, pySpec.SpecDataFile)
        self.assertRaises(pySpec.SpecDataFileNotFound, self.cannot_find_spec_data_file)
        self.assertRaises(pySpec.NotASpecDataFile, self.not_a_spec_data_file)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()