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

from collections import OrderedDict
import h5py
import os
import sys
import unittest

_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if _path not in sys.path:
    sys.path.insert(0, _path)

import spec2nexus
from spec2nexus import spec, writer

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if _test_path not in sys.path:
    sys.path.insert(0, _test_path)
import tests.common


class Test_USAXS_Bluesky_SpecWriterCallback(unittest.TestCase):
    """
    look for the metadata
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_the_data_file(self):
        '''
        look for the metadata
        '''
        prefix = os.path.abspath(os.path.join(
            _path, 
            'spec2nexus', 
            'data', 
            'usaxs-bluesky-specwritercallback'))
        file1 = prefix + '.dat'
        hfile = tests.common.create_test_file()
    
        # writer interface has changed, must use new spec module to proceed
        specfile = spec.SpecDataFile(file1)
        self.assertTrue(isinstance(specfile, spec2nexus.spec.SpecDataFile), file1)
        
        for scan_num, scan in specfile.scans.items():
            msg = "Scan %s MD test" % scan_num
            scan.interpret()    # force lazy-loader to parse this scan
            self.assertTrue(hasattr(scan, "MD"), msg)
            self.assertTrue(isinstance(scan.MD, OrderedDict), msg)
            self.assertGreater(len(scan.MD), 0, msg)
        
        # test the metadata in a NeXus file

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
        for nxentry in subgroup_list(fp, 'NXentry'):
            # nxinstrument_groups = subgroup_list(nxentry, 'NXinstrument')
            # self.assertEqual(len(nxinstrument_groups), 1)
            # nxinstrument = nxinstrument_groups[0]

            nxcollection_groups = subgroup_list(nxentry, 'NXcollection')
            self.assertGreater(len(nxcollection_groups), 0)
            md_group = nxentry.get("bluesky_metadata")
            self.assertIsNotNone(md_group, "bluesky_metadata in NeXus file")

        fp.close()
 
        os.remove(hfile)
        self.assertFalse(os.path.exists(hfile))


def suite(*args, **kw):
    test_list = [
        Test_USAXS_Bluesky_SpecWriterCallback,
        ]
    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
