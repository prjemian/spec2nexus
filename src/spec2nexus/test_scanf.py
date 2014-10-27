'''
unittest: scanf module
'''

import unittest
from scanf import scanf


class Test(unittest.TestCase):


    def testName(self):
        fmt = "#X %gKohm (%gC)"
        
        degc_sp = 21.1
        t_sp = 273.15 + degc_sp
        cmd ="#X %gKohm (%gC)" % (degc_sp, t_sp)
        result = scanf(fmt, cmd)
        self.assertIsNot(None, result)
        a, b = result
        self.assertEqual(degc_sp, a)
        self.assertEqual(t_sp, b)
        
        degc_sp = 20
        t_sp = 273.15 + degc_sp
        cmd ="#X %gKohm (%gC)" % (degc_sp, t_sp)
        result = scanf(fmt, cmd)
        self.assertIsNot(None, result, 'could not parse: ' + cmd)
        a, b = scanf(fmt, cmd)
        self.assertEqual(degc_sp, a)
        self.assertEqual(t_sp, b)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(Test)
    unittest.TextTestRunner(verbosity=2).run(suite)
