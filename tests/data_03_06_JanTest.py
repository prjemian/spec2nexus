'''
unit tests for a specific data file
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

import h5py
import os
import sys
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

import spec2nexus
from spec2nexus import spec, writer

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
        
        def subgroup_list(parent, nxclass):
            children = []
            for item in sorted(parent):
                obj = parent[item]
                if isinstance(obj, h5py.Group):
                    if obj.attrs.get('NX_class', '') == nxclass:
                        children.append(obj)
            return children
        
        fp = h5py.File(hfile, 'r')
        self.assertTrue(isinstance(fp, h5py.File), hfile)
        nxentry_groups = subgroup_list(fp, 'NXentry')
        self.assertGreater(len(nxentry_groups), 0)
        for nxentry in nxentry_groups:
            nxdata_groups = subgroup_list(nxentry, 'NXdata')
            self.assertGreater(len(nxdata_groups), 0)
            for nxdata in nxdata_groups:
                signal = nxdata.attrs.get('signal')
                self.assertTrue(signal in nxdata)

        default = fp.attrs.get('default')
        self.assertTrue(default in fp)
        nxentry = fp[default]

        default = nxentry.attrs.get('default')
        self.assertTrue(default in nxentry)
        nxdata = nxentry[default]

        signal = nxdata.attrs.get('signal')
        self.assertTrue(signal in nxdata)

        fp.close()

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
