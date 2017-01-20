
'''
test punx tests/common module (supports unit testing)
'''

import lxml
import os
import sys
import tempfile
import unittest

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

import spec2nexus.extractSpecScan
import spec2nexus.spec


class Issue64(unittest.TestCase):
   
    def setUp(self):
        path = os.path.dirname(__file__)
        self.testfile = os.path.join(path, 'data', 'issue64_data.txt')

    def tearDown(self):
        pass

    def test_data_file(self):
        self.assertTrue(os.path.exists(self.testfile))

        specData = spec2nexus.spec.SpecDataFile(self.testfile)
        self.assertTrue(isinstance(specData, spec2nexus.spec.SpecDataFile))

        scanNum = 50
        scan = specData.getScan(scanNum)
        self.assertTrue(isinstance(scan, spec2nexus.spec.SpecDataFileScan))

    def test_extractSpecScane(self):
        args = self.testfile + ' -s 50   -c si1t  pind1'
        for _ in args.split():
            sys.argv.append(_)
        sys.argv.append('-G')
        sys.argv.append('-V')
        sys.argv.append('-Q')
        sys.argv.append('-P')
        spec2nexus.extractSpecScan.main()   # TODO: need to grab the stdout and file output
        '''
        pydev debugger: starting (pid: 12052)
        .program: C:\Users\Pete\Documents\eclipse\spec2nexus\tests\issue64.py
        read: C:\Users\Pete\Documents\eclipse\spec2nexus\tests\data\issue64_data.txt
        E
        ======================================================================
        ERROR: test_extractSpecScane (__main__.Issue64)
        ----------------------------------------------------------------------
        Traceback (most recent call last):
          File "C:\Users\Pete\Documents\eclipse\spec2nexus\tests\issue64.py", line 47, in test_extractSpecScane
            spec2nexus.extractSpecScan.main()
          File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\extractSpecScan.py", line 237, in main
            if label in scan.L:
          File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\spec.py", line 455, in __getattribute__
            self.interpret()
          File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\spec.py", line 488, in interpret
            func(self)
          File "C:\Users\Pete\Documents\eclipse\spec2nexus\src\spec2nexus\plugins\spec_common_spec2nexus.py", line 556, in postprocess
            mne = scan.header.O[row][col]
        IndexError: list index out of range
        
        ----------------------------------------------------------------------
        Ran 2 tests in 56.151s
        
        FAILED (errors=1)
        '''

        _break = True


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Issue64,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == '__main__':
    runner=unittest.TextTestRunner()
    runner.run(suite())
