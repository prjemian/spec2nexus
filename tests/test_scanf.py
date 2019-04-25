'''
unittest: scanf module
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

import os, sys
import unittest

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

from spec2nexus.scanf import scanf


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
        
        self.assertEqual((123.456e-1,), scanf('%g', '123.456e-1'))
        self.assertEqual((123.456,), scanf('%f', '123.456e-1'))
        self.assertEqual((20,), scanf('%g', '20'))
        self.assertEqual((0,), scanf('%g', '0.'))
        self.assertEqual((0,), scanf('%g', '.0'))
        self.assertEqual((0,), scanf('%g', '.0e-21'))
        self.assertEqual(None, scanf('%g', '.'))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Test,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
