"""
unit tests for the UXML control lines
"""

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2016, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


from lxml import etree
import unittest
import os
import sys

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

from spec2nexus import writer
from spec2nexus.spec import SpecDataFile, SpecDataFileScan

from spec2nexus.plugins.uxml import UXML_metadata

SPEC_DATA_FILE_LINES = """
#UXML <group name="attenuator1" NX_class="NXattenuator" number="1" pv_prefix="33idd:filter:Fi1:" unique_id="33idd:filter:Fi1:">
#UXML   <dataset name="enable" unique_id="find_me">Enable</dataset>
#UXML   <hardlink name="found_you" target_id="find_me"/>
#UXML   <dataset name="lock">Lock</dataset>
#UXML   <dataset name="type">Ti</dataset>
#UXML   <dataset name="thickness" type="float" units="micron">251.000</dataset>
#UXML   <dataset name="attenuator_transmission" type="float">3.55764458e-02</dataset>
#UXML   <dataset name="status">Out</dataset>
#UXML </group>
	"""

def get_paths():
	import spec2nexus.plugins
	uxml_path = os.path.abspath(os.path.dirname(spec2nexus.plugins.__file__))
	basepath = os.path.join(uxml_path, '..')
	return basepath, uxml_path


class TestPlugin(unittest.TestCase):

	def setUp(self):
		self.basepath, self.uxml_path = get_paths()

	def tearDown(self):
		pass

	def test_process(self):
		"""test the :meth:`process` method"""
		self.scan = SpecDataFileScan(None, '')
		self.assertTrue(isinstance(self.scan, SpecDataFileScan))

		# test create instance
		uxml = UXML_metadata()
		self.assertTrue(isinstance(uxml, UXML_metadata))
		
		# test that specific attributes not yet defined
		txt = 'this is text'
		self.assertFalse(hasattr(self.scan, 'UXML'))
		self.assertFalse('UXML_metadata' in self.scan.postprocessors)
		
		# test that specific attributes now defined
		uxml.process('#UXML ' + txt, self.scan)
		self.assertTrue(hasattr(self.scan, 'UXML'))
		self.assertTrue('UXML_metadata' in self.scan.postprocessors)
		self.assertEqual(self.scan.postprocessors['UXML_metadata'], uxml.postprocess)
		self.assertTrue(isinstance(self.scan.UXML, list))
		self.assertEqual(self.scan.UXML, [txt])
		
	def test_parse(self):
		# test that UXML lines are parsed
		# TODO: must test bad UXML as well

		self.scan = SpecDataFileScan(None, '')
		uxml = UXML_metadata()
		for line in SPEC_DATA_FILE_LINES.strip().splitlines():
			txt = line.strip()
			if len(txt) > 0:
				uxml.process(txt, self.scan)
		self.assertTrue(hasattr(self.scan, 'UXML'))
		#print ('\n'.join([ '%3d: %s' % (i,j) for i,j in enumerate(self.scan.UXML) ]))
		self.assertEqual(9, len(self.scan.UXML))
		self.assertTrue(hasattr(self.scan, 'h5writers'))
		self.assertFalse('UXML_metadata' in self.scan.h5writers)
		self.assertFalse(hasattr(self.scan, 'UXML_root'))
		
	def test_postprocess(self):	
		"""test the :meth:`postprocess` method"""
		self.scan = SpecDataFileScan(None, '')
		uxml = UXML_metadata()
		for line in SPEC_DATA_FILE_LINES.strip().splitlines():
			txt = line.strip()
			if len(txt) > 0:
				uxml.process(txt, self.scan)
	
		uxml.postprocess(self.scan)
		self.assertTrue('UXML_metadata' in self.scan.h5writers)
		self.assertTrue(hasattr(self.scan, 'UXML_root'))
		root = self.scan.UXML_root
		self.assertFalse(isinstance(root, str))
		self.assertTrue(isinstance(root, etree._Element))
		self.assertEqual('UXML', root.tag)
		node = root[0]
		self.assertEqual('group', node.tag)
		self.assertEqual('attenuator1', node.get('name'))
		self.assertEqual('NXattenuator', node.get('NX_class'))
		self.assertEqual(7, len(node))
		node = node[0]
		self.assertEqual('dataset', node.tag)
		self.assertEqual('enable', node.get('name'))
		self.assertEqual('find_me', node.get('unique_id'))
	
	def test_writer(self):	
		"""test the :meth:`writer` method"""
		self.scan = SpecDataFileScan(None, '')
		uxml = UXML_metadata()
		for line in SPEC_DATA_FILE_LINES.strip().splitlines():
			txt = line.strip()
			if len(txt) > 0:
				uxml.process(txt, self.scan)
		uxml.postprocess(self.scan)
	
		self.assertTrue(hasattr(self.scan, 'UXML_root'), 'need to test writer()')
		root = self.scan.UXML_root
		schema_file = os.path.join(self.uxml_path, 'uxml.xsd')
		self.assertTrue(os.path.exists(schema_file))
		schema_doc = etree.parse(schema_file)
		schema = etree.XMLSchema(schema_doc)
		result = schema.validate(root)
		self.assertTrue(result)


# TODO: test_3.spec


class TestData_4(unittest.TestCase):

	def setUp(self):
		self.basepath, self.uxml_path = get_paths()
		self.fname = os.path.join(_test_path, "tests", "data", "test_4.spec")
		basename = os.path.splitext(self.fname)[0]
		self.hname = basename + '.hdf5'

	def tearDown(self):
		for tname in (self.hname,):
			if os.path.exists(tname):
				os.remove(tname)

	def testName(self):
		spec_data = SpecDataFile(self.fname)
		self.assertTrue(isinstance(spec_data, SpecDataFile))
		out = writer.Writer(spec_data)
		scan_list = [1, ]
		out.save(self.hname, scan_list)
		# TODO: make tests of other things in the Writer
		dd = out.root_attributes()
		self.assertTrue(isinstance(dd, dict))
		
		# scan = spec_data.scans[1]
		# scan.interpret()
		# print(etree.tostring(scan.UXML_root))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        TestPlugin,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
