'''
unit tests for the plugin module
'''
import unittest
import plugin


class Test(unittest.TestCase):

#     def setUp(self):
#         pass

#     def tearDown(self):
#         pass

#     def testName(self):
#         pass
    
    def test_handler_keys(self):
        h = plugin.ControlLineHandler()
        self.assertEqual(h.key, None)
        self.assertEqual(str(h.key), h.getKey())


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()