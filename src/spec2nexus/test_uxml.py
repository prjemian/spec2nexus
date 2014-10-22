'''
unit tests for the UXML control lines
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
import os
import spec
import writer
import sys


class Test(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(self.basepath, 'data', 'uxml')
        os.environ['SPEC2NEXUS_PLUGIN_PATH'] = path
        self.fname = os.path.join(path, 'test_4.spec')
        basename = os.path.splitext(self.fname)[0]
        self.hname = basename + '.hdf5'

    def tearDown(self):
        for tname in (self.hname,):
            if os.path.exists(tname):
                #os.remove(tname)
                #print "removed test file:", tname
                pass


    def testName(self):
        spec_data = spec.SpecDataFile(self.fname)
        out = writer.Writer(spec_data)
        scan_list = [1, ]
        out.save(self.hname, scan_list)
        # TODO: make tests of other things in the Writer
        dd = out.root_attributes()
        self.assertTrue(isinstance(dd, dict))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()