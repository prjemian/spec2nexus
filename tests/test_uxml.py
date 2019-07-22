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


import h5py
from lxml import etree
import numpy
import unittest
import os
import sys

_test_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
_path = os.path.abspath(os.path.join(_test_path, 'src'))

sys.path.insert(0, _path)
sys.path.insert(0, _test_path)

import spec2nexus
from spec2nexus import writer
from spec2nexus.spec import SpecDataFile, SpecDataFileScan


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
	_p = os.path.abspath(os.path.dirname(writer.__file__))
	uxml_path = os.path.join(_p, 'plugins')
	return _p, uxml_path


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
		uxml = spec2nexus.plugins.uxml.UXML_metadata()
		self.assertTrue(isinstance(uxml, spec2nexus.plugins.uxml.UXML_metadata))
		
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
		"""test that UXML lines are parsed"""

		self.scan = SpecDataFileScan(None, '')
		uxml = spec2nexus.plugins.uxml.UXML_metadata()
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
		uxml = spec2nexus.plugins.uxml.UXML_metadata()
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
		uxml = spec2nexus.plugins.uxml.UXML_metadata()
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


class TestData_error(unittest.TestCase):

	def setUp(self):
		self.basepath, self.uxml_path = get_paths()
		self.fname = os.path.join(_test_path, "tests", "data", "test_3_error.spec")
		basename = os.path.splitext(self.fname)[0]
		self.hname = basename + '.hdf5'

	def tearDown(self):
		for tname in (self.hname,):
			if os.path.exists(tname):
				os.remove(tname)

	def testName(self):
		spec_data = SpecDataFile(self.fname)
		self.assertTrue(isinstance(spec_data, SpecDataFile))
		scan = spec_data.getScan(1)

		with self.assertRaises(spec2nexus.plugins.uxml.UXML_Error) as context:
			scan.interpret()
		received = str(context.exception)
		expected = "UXML error: Element 'group': "
		expected += "Character content other than whitespace is not allowed "
		expected += "because the content type is 'element-only'."
		self.assertTrue(received.startswith(expected))


class TestData_3(unittest.TestCase):

	def setUp(self):
		self.basepath, self.uxml_path = get_paths()
		self.fname = os.path.join(_test_path, "tests", "data", "test_3.spec")
		basename = os.path.splitext(self.fname)[0]
		self.hname = basename + '.hdf5'

	def tearDown(self):
		for tname in (self.hname,):
			if os.path.exists(tname):
				os.remove(tname)

	def test_contents(self):
		spec_data = SpecDataFile(self.fname)
		self.assertTrue(isinstance(spec_data, SpecDataFile))
		out = writer.Writer(spec_data)
		scan_list = [1, ]
		out.save(self.hname, scan_list)
		
		# text that UXML group defined as expected
		self.assertTrue(os.path.exists(self.hname))
		with h5py.File(self.hname) as h5_file:
			self.assertTrue("S1" in h5_file)
			nxentry = h5_file["/S1"]
			self.assertTrue("UXML" in nxentry)
			uxml = nxentry["UXML"]
			self.assertTrue("NX_class" in uxml.attrs)
			self.assertEqual(uxml.attrs["NX_class"], "NXnote")
			
			# spot-check a couple items
			# group: attenuator_set
			self.assertTrue("attenuator_set" in uxml)
			group = uxml["attenuator_set"]
			prefix = group.attrs.get("prefix")
			description = group.attrs.get("description")
			unique_id = group.attrs.get("unique_id")
			self.assertEqual(prefix, "33idd:filter:")
			self.assertEqual(description, "33-ID-D Filters")
			self.assertEqual(unique_id, None)
			
			# <dataset name="corrdet_counter">corrdet</dataset>
			self.assertTrue("corrdet_counter" in group)
			ds = group["corrdet_counter"]
			# http://docs.h5py.org/en/stable/whatsnew/2.1.html?highlight=dataset#dataset-value-property-is-now-deprecated
			value = ds[()]		# ds.value deprecated in h5py
			self.assertEqual(value, [b"corrdet"])
			
			# <dataset name="wait_time" type="float" units="s">0.500</dataset>
			self.assertTrue("wait_time" in group)
			ds = group["wait_time"]
			attrs = dict(ds.attrs)
			self.assertEqual(ds.attrs.get("units"), "s")
			value = ds[()]		# ds.value deprecated in h5py
			self.assertEqual(value, numpy.array([.5]))
	
			# <hardlink name="attenuator1" target_id="33idd:filter:Fi1:"/>
			self.assertTrue("attenuator1" in group)
			attenuator1 = group["attenuator1"]
			target = attenuator1.attrs.get("target")
			self.assertNotEqual(target, attenuator1.name)
			self.assertEqual(target, uxml["attenuator1"].name)
	
			addr = "/S1/UXML/ad_file_info/file_format"
			self.assertTrue(addr in h5_file)
			ds = h5_file[addr]
			value = ds[()]		# ds.value deprecated in h5py
			self.assertEqual(value, [b"TIFF"])


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

	def test_contents(self):
		spec_data = SpecDataFile(self.fname)
		self.assertTrue(isinstance(spec_data, SpecDataFile))
		out = writer.Writer(spec_data)
		scan_list = [1, ]
		out.save(self.hname, scan_list)
		
		# the ONLY structural difference between test_3.spec 
		# and test_4.spec is the presence of this hardlink
		self.assertTrue(os.path.exists(self.hname))
		with h5py.File(self.hname) as h5_file:
			source = h5_file["/S1/UXML/ad_detector/beam_center_x"]
			link = h5_file["/S1/UXML/beam_center_x"]
			target = source.attrs.get("target")
	
			self.assertNotEqual(source.name, link.name)
			self.assertNotEqual(target, None)
			self.assertEqual(target, source.name)
			self.assertEqual(target, link.attrs.get("target"))


def suite(*args, **kw):
    test_suite = unittest.TestSuite()
    test_list = [
        TestPlugin,
        TestData_error,
        TestData_3,
        TestData_4,
        ]
    for test_case in test_list:
        test_suite.addTest(unittest.makeSuite(test_case))
    return test_suite


if __name__ == "__main__":
    runner=unittest.TextTestRunner()
    runner.run(suite())
