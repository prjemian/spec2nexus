'''
unit tests for the spec module
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

import unittest
import os, sys

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import spec, diffractometers


class Test(unittest.TestCase):
    
    def test_dictionary(self):
        dgc = diffractometers.DiffractometerGeometryCatalog()
        self.assertEqual(len(dgc.db), 20)
    
    def test_class_DiffractometerGeometryCatalog(self):
        dgc = diffractometers.DiffractometerGeometryCatalog()
        
        expected = "DiffractometerGeometryCatalog(number=20)"
        self.assertEqual(str(dgc), expected)
        
        self.assertTrue(hasattr(dgc, "_default_geometry"))
        self.assertIsNotNone(dgc._default_geometry)
        self.assertEqual(dgc.get_default_geometry()["name"], "spec")
        
        nm, variant = dgc._split_name_variation_("only")
        self.assertEqual(nm, "only")
        self.assertIsNone(variant)
        nm, variant = dgc._split_name_variation_("two.parts")
        self.assertEqual(nm, "two")
        self.assertIsNotNone(variant)
        self.assertEqual(variant, "parts")
        nm, variant = dgc._split_name_variation_("more.than.two.parts")
        self.assertEqual(nm, "more.than.two.parts")
        self.assertIsNone(variant)
        
        # spot tests verify method hasGeometry()
        self.assertTrue(dgc.hasGeometry("fourc"))
        self.assertTrue(dgc.hasGeometry("fourc.kappa"))
        self.assertTrue(dgc.hasGeometry("spec"))
        self.assertFalse(dgc.hasGeometry("spec.kappa"))
        self.assertTrue(dgc.hasGeometry("psic.s2d2+daz"))
        self.assertFalse(dgc.hasGeometry("s2d2.psic+daz"))
        
        geos = dgc.geometries()
        expected = [
            'spec', 'fivec', 'fourc', 'oscam', 'pi1go', 'psic', 's1d2', 's2d2', 
            'sevc', 'sixc', 'surf', 'suv', 'trip', 'twoc', 
            'twoc_old', 'w21h', 'w21v', 'zaxis', 'zaxis_old', 'zeta']
        self.assertEqual(len(geos), 20)
        self.assertEqual(geos, expected)

        geos = dgc.geometries(True)
        expected = [
            'fivec.kappa', 'fivec.standard', 'fourc.3axis', 'fourc.kappa', 
            'fourc.omega', 'fourc.picker', 'fourc.standard', 'fourc.xtalogic', 
            'oscam.standard', 'pi1go.standard', 'psic.kappa', 'psic.s2d2', 
            'psic.s2d2+daz', 'psic.standard', 'psic.standard+daz', 
            's1d2.standard', 's2d2.standard', 'sevc.standard', 
            'sixc.standard', 'spec.standard', 'surf.standard', 'suv.standard', 
            'trip.standard', 'twoc.standard', 'twoc_old.standard', 
            'w21h.standard', 'w21v.d32', 'w21v.gmci', 'w21v.id10b', 
            'w21v.standard', 'zaxis.standard', 'zaxis_old.beta', 
            'zaxis_old.standard', 'zeta.standard']
        self.assertEqual(len(geos), 34)
        self.assertEqual(sorted(geos), expected)
        
        for geo_name in dgc.geometries():
            msg = "name='%s' defined?" % geo_name
            geom = dgc.get(geo_name)
            self.assertTrue("name" in geom, msg)
            self.assertEqual(geom["name"], geo_name, msg)
        
    def test_tests_data(self):
        """
        identify geometries in tests.data files
        """
        dgc = diffractometers.DiffractometerGeometryCatalog()
        
        test_files = [
            ['issue109_data.txt', -1, 'fourc.standard'],         # 8-ID-I
            ['issue119_data.txt', -1, 'spec.standard'],          # USAXS
            ['issue161_spock_spec_file', -1, 'spec.standard'],   # SPOCK
            ['JL124_1.spc', -1, 'sixc.standard'],
            #['test_3_error.spec', -1, 'spec'],                  # FIXME: #UXML, plugin has error
            ['test_3.spec', -1, 'spec'],                         # predates #o (mnemonics) lines
            ['test_4.spec', -1, 'spec'],                         # predates #o (mnemonics) lines
        ]
        for triplet in test_files:
            filename, scan_number, geo_name = triplet
            scan = spec.SpecDataFile(os.path.join(
                _test_path, "tests", "data", filename)
            ).getScan(scan_number)
            geom = dgc.match(scan)
            self.assertIsNotNone(geom, filename)
            self.assertEqual(geom, geo_name, filename)
        
    def test_src_spec2nexus_data(self):
        """
        identify geometries in src.spec2nexus.data files
        """
        dgc = diffractometers.DiffractometerGeometryCatalog()
        
        test_files = [
            ['02_03_setup.dat', -1, 'spec.standard'],
            ['03_06_JanTest.dat', -1, 'spec.standard'],
            ['05_02_test.dat', -1, 'spec.standard'],
            ['33bm_spec.dat', -1, 'fourc.standard'],
            ['33id_spec.dat', -1, 'spec'],  # psic but predates #o (mnemonics) lines
            ['APS_spec_data.dat', -1, 'spec.standard'],
            ['CdOsO', -1, 'fourc.standard'],
            ['CdSe', -1, 'fourc.standard'],
            ['lmn40.spe', -1, 'spec'],
            ['mca_spectra_example.dat', -1, 'spec.standard'],
            ['spec_from_spock.spc', -1, 'spec.standard'],
            ['startup_1.spec', 1, 'spec'],
            ['usaxs-bluesky-specwritercallback.dat', -1, 'spec.standard'],
            ['user6idd.dat', -1, 'spec'],            # predates #o (mnemonics) lines
            ['YSZ011_ALDITO_Fe2O3_planar_fired_1.spc', -1, 'fourc.standard'],
        ]
        for triplet in test_files:
            file_name, scan_number, geo_name = triplet
            scan = spec.SpecDataFile(os.path.join(
                _path, "spec2nexus", "data", file_name)
            ).getScan(scan_number)
            geom = dgc.match(scan)
            self.assertIsNotNone(geom, file_name)
            self.assertEqual(geom, geo_name, file_name)


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
