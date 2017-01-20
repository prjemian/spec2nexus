'''
unit tests for a specific data file
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2017, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import os
import sys
import unittest

import spec2nexus

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

from spec2nexus import spec, writer, h5toText

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class Test_03_06_JanTest_data_file(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_the_data_file(self):
        '''
        write all as HDF5: 1-D scans, USAXS scans, Fly scans, #O+#o and #J+#j control lines
        '''
        prefix = os.path.abspath(os.path.join(_path, 'spec2nexus', 'data', '03_06_JanTest'))
        file1 = prefix + '.dat'
        hfile = tests.common.create_test_file()
    
        # writer interface has changed, must use new spec module to proceed
        specfile = spec.SpecDataFile(file1)
        self.assertTrue(isinstance(specfile, spec2nexus.spec.SpecDataFile), file1)

        specwriter = writer.Writer(specfile)
        self.assertTrue(isinstance(specwriter, spec2nexus.writer.Writer), file1)
        
        specwriter.save(hfile, sorted(specfile.getScanNumbers()))
        self.assertTrue(os.path.exists(hfile))
        self.assertFalse(h5toText.isHdf5File(hfile), 'name of file is not instance of h5py.File')
        self.assertTrue(h5toText.isNeXusFile_ByNXdataAttrs(hfile))
        self.assertFalse(h5toText.isNeXusFile_ByAxes(hfile))
        self.assertFalse(h5toText.isNeXusFile_ByAxisAttr(hfile))

        os.remove(hfile)
        self.assertFalse(os.path.exists(hfile))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        Test_03_06_JanTest_data_file,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
