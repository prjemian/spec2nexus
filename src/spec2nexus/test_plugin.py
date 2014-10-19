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

# TODO: suggestions for testing the plugin architecture
# def simple_test():
#     os.environ[PLUGIN_SEARCH_PATH_ENVIRONMENT_VARIABLE] = 'C://Users//Pete//Desktop, /tmp'
#     manager = ControlLineHandlerManager()
#     manager.load_plugins()
#     pprint.pprint(manager.handler_dict)
# 
#     spec_data = '''
#         #S 1 ascan eta 43.6355 44.0355 40 1
#         #D Thu Jul 17 02:38:24 2003
#         #T 1 (seconds)
#         #G0 0 0 0 0 0 1 0 0 0 0 0 0 50 0 0 0 1 0 0 0 0
#         #V110 101.701 56 1 4 1 1 1 1 992.253
#         #@CHANN 1201 1110 1200 1
#         #N 14
#         #L eta H K L elastic Kalpha Epoch seconds signal I00 harmonic signal2 I0 I0
#         #@MCA 16C
#         #@CHANN 1201 1110 1200 1
#         #o0 un0 mx my waxsx ax un5 az un7
#         @A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0\
#         0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
#         #H4 FB_o2_on FB_o2_r FB_o2_sp
#         #Pete wrote this stuff
#         43.6835 0.998671 -0.0100246 11.0078 1 0 66 1 0 863 0 0 1225 1225
#     '''
#     for spec_line in spec_data.strip().splitlines():
#         txt = spec_line.strip()
#         if len(txt) > 0:
#             key = manager.getKey(txt)
#             print key, manager.get(key)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()