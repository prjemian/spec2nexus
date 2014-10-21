'''
unit tests for the writer module
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


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.datapath = os.path.join(self.basepath, 'data')
        self.fname = os.path.join(self.datapath, '33id_spec.dat')
        basename = os.path.splitext(self.fname)[0]
        self.hname = basename + '.hdf5'

    def tearDown(self):
        for tname in (self.hname,):
            if os.path.exists(tname):
                os.remove(tname)
                #print "removed test file:", tname
                pass

    def testWriter(self):
        '''test the writer.Writer class'''
        spec_data = spec.SpecDataFile(self.fname)
        out = writer.Writer(spec_data)
        scan_list = [1, 5, 7]
        out.save(self.hname, scan_list)
        # TODO: make tests of other things in the Writer
        dd = out.root_attributes()
        self.assertTrue(isinstance(dd, dict))

#     sys.argv.append(os.path.join('data', 'APS_spec_data.dat'))
#     sys.argv.append(os.path.join('data', '33id_spec.dat'))
#     sys.argv.append(os.path.join('data', '33bm_spec.dat'))
#     sys.argv.append(os.path.join('data', 'lmn40.spe'))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestWriter)
    unittest.TextTestRunner(verbosity=2).run(suite)
