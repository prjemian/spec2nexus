'''
unit tests for the plugin module
'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2016, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

import unittest
import plugin
import os


class TestPlugin(unittest.TestCase):

    def setUp(self):
        os.environ['SPEC2NEXUS_PLUGIN_PATH'] = 'C://Users//Pete//Desktop, /tmp'
        self.basepath = os.path.abspath(os.path.dirname(__file__))
        self.datapath = os.path.join(self.basepath, 'data')
        self.manager = plugin.PluginManager()
        self.manager.load_plugins()

#     def tearDown(self):
#         pass

#     def testName(self):
#         pass
    
    def test_handler_keys(self):
        h = plugin.ControlLineHandler()
        self.assertEqual(h.key, None)
        self.assertEqual(str(h.key), h.getKey())
    
    def test_sample_control_line_keys(self):
        spec_data = {
            '#S'           : r'#S 1 ascan eta 43.6355 44.0355 40 1',
            '#D'           : r'#D Thu Jul 17 02:38:24 2003',
            '#T'           : r'#T 1 (seconds)',
            '#G\\d+'       : r'#G0 0 0 0 0 0 1 0 0 0 0 0 0 50 0 0 0 1 0 0 0 0',
            '#V\\d+'       : r'#V110 101.701 56 1 4 1 1 1 1 992.253',
            '#N'           : r'#N 14',
            '#L'           : r'#L eta H K L elastic Kalpha Epoch seconds signal I00 harmonic signal2 I0 I0',
            '#@MCA'        : r'#@MCA 16C',
            '#@CHANN'      : r'#@CHANN 1201 1110 1200 1',
            '#o\d+'        : r'#o0 un0 mx my waxsx ax un5 az un7',
            #r'@A\d*'       : r'@A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\',
            r'@A\d*'       : r'@A1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\',
            #r'@A\d*'       : r'@A2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\\',
            'scan data'    : r' 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'.lstrip(),
            '#H\\d+'       : r'#H4 FB_o2_on FB_o2_r FB_o2_sp',
            None           : r'#Pete wrote this stuff',
            'scan data'    : r'43.6835 0.998671 -0.0100246 11.0078 1 0 66 1 0 863 0 0 1225 1225',
        }
        for k, v in spec_data.items():
            self.assertEqual(k, self.manager.getKey(v))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    #unittest.main()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestPlugin)
    unittest.TextTestRunner(verbosity=2).run(suite)
