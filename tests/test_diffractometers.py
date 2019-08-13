'''
unit tests for the diffractometers module
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

import numpy
import os
import sys
import unittest

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import spec, diffractometers


class Test(unittest.TestCase):
    
    def test_dictionary(self):
        diffractometers.reset_geometry_catalog()
        self.assertIsNone(diffractometers._geometry_catalog)
        with self.assertRaises(RuntimeError):
            diffractometers.DiffractometerGeometryCatalog()
        
        self.assertTrue(os.path.exists(diffractometers.DICT_FILE))

        dgc = diffractometers.get_geometry_catalog()
        self.assertEqual(len(dgc.db), 20)
    
    def test_split_name_variation(self):
        nm, variant = diffractometers.split_name_variation("only")
        self.assertEqual(nm, "only")
        self.assertIsNone(variant)
        nm, variant = diffractometers.split_name_variation("two.parts")
        self.assertEqual(nm, "two")
        self.assertIsNotNone(variant)
        self.assertEqual(variant, "parts")
        nm, variant = diffractometers.split_name_variation("more.than.two.parts")
        self.assertEqual(nm, "more.than.two.parts")
        self.assertIsNone(variant)
    
    def test_class_DiffractometerGeometryCatalog(self):
        dgc1 = diffractometers.get_geometry_catalog()
        self.assertEqual(dgc1, diffractometers._geometry_catalog)
        dgc2 = diffractometers.get_geometry_catalog()
        self.assertEqual(dgc1, dgc2)
        diffractometers.reset_geometry_catalog()
        self.assertNotEqual(dgc1, diffractometers._geometry_catalog)
        self.assertEqual(dgc1, dgc2)
        self.assertIsNone(diffractometers._geometry_catalog)
        
        diffractometers.reset_geometry_catalog()
        dgc = diffractometers.get_geometry_catalog()
        self.assertIsNotNone(dgc)
        self.assertNotEqual(dgc, dgc1)
        self.assertNotEqual(dgc, dgc2)
        
        expected = "DiffractometerGeometryCatalog(number=20)"
        self.assertEqual(str(dgc), expected)
        
        self.assertTrue(hasattr(dgc, "_default_geometry"))
        self.assertIsNotNone(dgc._default_geometry)
        self.assertEqual(dgc.get_default_geometry()["name"], "spec")
        
        # spot tests verify method has_geometry()
        self.assertTrue(dgc.has_geometry("fourc"))
        self.assertTrue(dgc.has_geometry("fourc.kappa"))
        self.assertTrue(dgc.has_geometry("spec"))
        self.assertFalse(dgc.has_geometry("spec.kappa"))
        self.assertTrue(dgc.has_geometry("psic.s2d2+daz"))
        self.assertFalse(dgc.has_geometry("s2d2.psic+daz"))
        
        geos = dgc.geometries()
        expected = [
            'spec', 'fivec', 'fourc', 'oscam', 'pi1go', 'psic', 's1d2', 's2d2', 
            'sevc', 'sixc', 'surf', 'suv', 'trip', 'twoc', 
            'twoc_old', 'w21h', 'w21v', 'zaxis', 'zaxis_old', 'zeta']
        self.assertEqual(len(geos), 20)
        self.assertEqual(geos, expected)

        geos = dgc.geometries(True)
        expected = [        # sorted
            'fivec.default', 'fivec.kappa', 
            'fourc.3axis', 'fourc.default', 'fourc.kappa', 
            'fourc.omega', 'fourc.picker', 'fourc.xtalogic', 
            'oscam.default', 
            'pi1go.default', 
            'psic.+daz', 'psic.default', 'psic.kappa', 'psic.s2d2', 'psic.s2d2+daz', 
            's1d2.default', 
            's2d2.default', 
            'sevc.default', 
            'sixc.default', 
            'spec.default', 
            'surf.default', 
            'suv.default', 
            'trip.default', 
            'twoc.default', 'twoc_old.default', 
            'w21h.default', 
            'w21v.d32', 'w21v.default', 'w21v.gmci', 'w21v.id10b', 
            'zaxis.default', 
            'zaxis_old.beta', 'zaxis_old.default', 
            'zeta.default'
        ]
        self.assertEqual(len(geos), 34)
        self.assertEqual(sorted(geos), expected)
        
        for geo_name in dgc.geometries():
            msg = "name='%s' defined?" % geo_name
            geom = dgc.get(geo_name)
            self.assertTrue("name" in geom, msg)
            self.assertEqual(geom["name"], geo_name, msg)
        
    def process_files(self, dgc, test_files, base_path):
        for triplet in test_files:
            filename, scan_number, geo_name = triplet
            fullname = os.path.join(base_path, filename)
            scan = spec.SpecDataFile(fullname).getScan(scan_number)
            geom = dgc.match(scan)
            self.assertIsNotNone(geom, filename)
            self.assertEqual(geom, geo_name, filename)
            
            gonio = diffractometers.Diffractometer(geom)
            gonio.parse(scan)

            if len(gonio.geometry_parameters) > 0:
                gpar = gonio.geometry_parameters
                for k in "g_aa g_bb g_cc g_al g_be g_ga LAMBDA".split():
                    if k in gpar:
                        self.assertGreater(gpar[k].value, 0, filename)
                        
                if ("ub_matrix" in gpar):
                    ub = gpar["ub_matrix"].value
                    self.assertTrue(isinstance(ub, numpy.ndarray), filename)
                    self.assertTupleEqual(ub.shape, (3, 3), filename)

    def test_tests_data(self):
        """
        identify geometries in tests.data files
        """
        dgc = diffractometers.get_geometry_catalog()
        
        test_files = [
            ['issue109_data.txt', -1, 'fourc.default'],         # 8-ID-I
            ['issue119_data.txt', -1, 'spec.default'],          # USAXS
            ['issue161_spock_spec_file', -1, 'spec.default'],   # SPOCK
            ['JL124_1.spc', -1, 'sixc.default'],
            #['test_3_error.spec', -1, 'spec'],                  # FIXME: #UXML, plugin has error
            ['test_3.spec', -1, 'spec'],                         # predates #o (mnemonics) lines
            ['test_4.spec', -1, 'spec'],                         # predates #o (mnemonics) lines
        ]
        base_path = os.path.join(_test_path, "tests", "data")
        self.process_files(dgc, test_files, base_path)
            
    def test_src_spec2nexus_data(self):
        """
        identify geometries in src.spec2nexus.data files
        """
        dgc = diffractometers.get_geometry_catalog()
        
        test_files = [
            ['02_03_setup.dat', -1, 'spec.default'],
            ['03_06_JanTest.dat', -1, 'spec.default'],
            ['05_02_test.dat', -1, 'spec.default'],
            ['33bm_spec.dat', -1, 'fourc.default'],
            ['33id_spec.dat', -1, 'spec'],  # psic but predates #o (mnemonics) lines
            ['APS_spec_data.dat', -1, 'spec.default'],
            ['CdOsO', -1, 'fourc.default'],
            ['CdSe', -1, 'fourc.default'],
            ['lmn40.spe', -1, 'spec'],
            ['mca_spectra_example.dat', -1, 'spec.default'],
            ['spec_from_spock.spc', -1, 'spec.default'],
            ['startup_1.spec', 1, 'spec'],
            ['usaxs-bluesky-specwritercallback.dat', -1, 'spec.default'],
            ['user6idd.dat', -1, 'spec'],            # predates #o (mnemonics) lines
            ['YSZ011_ALDITO_Fe2O3_planar_fired_1.spc', -1, 'fourc.default'],
        ]
        base_path = os.path.join(_path, "spec2nexus", "data")
        self.process_files(dgc, test_files, base_path)
    
    def test_class_Diffractometer(self):
        gonio = diffractometers.Diffractometer("big.little")
        self.assertEqual(gonio.geometry_name_full, "big.little")
        self.assertEqual(gonio.geometry_name, "big")
        self.assertEqual(gonio.variant, "little")
        self.assertIsNotNone(gonio.geometry_parameters)


def suite(*args, **kw):
    test_list = [
        Test,
        ]
    test_suite = unittest.TestSuite()
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
