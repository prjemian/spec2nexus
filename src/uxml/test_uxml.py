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


import unittest
import os
from spec2nexus import writer
from spec2nexus.spec import SpecDataFile, SpecDataFileScan
from lxml import etree

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
	uxml_path = os.path.abspath(os.path.dirname(__file__))
	basepath = os.path.join(uxml_path, '..')
	return basepath, uxml_path


class TestPlugin(unittest.TestCase):

	def setUp(self):
		self.basepath, self.uxml_path = get_paths()
		os.environ['SPEC2NEXUS_PLUGIN_PATH'] = self.uxml_path
		if 'PYTHONPATH' not in os.environ:
			os.environ['PYTHONPATH'] = ''
		os.environ['PYTHONPATH'] += ':' + self.uxml_path
		self.pythonpath = os.environ['PYTHONPATH']

	def tearDown(self):
		pass

	def test_01_process(self):
		"""test the :meth:`process` method"""
		self.scan = SpecDataFileScan(None, '')
		self.assertTrue(isinstance(self.scan, SpecDataFileScan))

		# test create instance
		os.environ['PYTHONPATH'] = self.pythonpath
		from uxml_spec2nexus import UXML_metadata
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
		self.assertEquals(self.scan.postprocessors['UXML_metadata'], uxml.postprocess)
		self.assertTrue(isinstance(self.scan.UXML, list))
		self.assertEquals(self.scan.UXML, [txt])
		
		# test that UXML lines are parsed
		# TODO: must test bad UXML as well
		self.scan = SpecDataFileScan(None, '')
		for line in SPEC_DATA_FILE_LINES.strip().splitlines():
			txt = line.strip()
			if len(txt) > 0:
				uxml.process(txt, self.scan)
		self.assertTrue(hasattr(self.scan, 'UXML'))
		#print ('\n'.join([ '%3d: %s' % (i,j) for i,j in enumerate(self.scan.UXML) ]))
		self.assertEquals(9, len(self.scan.UXML))
		self.assertTrue(hasattr(self.scan, 'h5writers'))
		self.assertFalse('UXML_metadata' in self.scan.h5writers)
		self.assertFalse(hasattr(self.scan, 'UXML_root'))
	
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
		self.assertEquals('UXML', root.tag)
		node = root[0]
		self.assertEquals('group', node.tag)
		self.assertEquals('attenuator1', node.get('name'))
		self.assertEquals('NXattenuator', node.get('NX_class'))
		self.assertEquals(7, len(node))
		node = node[0]
		self.assertEquals('dataset', node.tag)
		self.assertEquals('enable', node.get('name'))
		self.assertEquals('find_me', node.get('unique_id'))
	
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


class TestData(unittest.TestCase):

	def setUp(self):
		self.basepath, self.uxml_path = get_paths()
		os.environ['SPEC2NEXUS_PLUGIN_PATH'] = self.uxml_path
		self.fname = os.path.join(self.uxml_path, 'test_4.spec')
		basename = os.path.splitext(self.fname)[0]
		self.hname = basename + '.hdf5'

	def tearDown(self):
		for tname in (self.hname,):
			if os.path.exists(tname):
				os.remove(tname)
				#print ("removed test file: %s" % tname)
				pass

	def testName(self):
		spec_data = SpecDataFile(self.fname)
		self.assertTrue(isinstance(spec_data, SpecDataFile))
		out = writer.Writer(spec_data)
		scan_list = [1, ]
		out.save(self.hname, scan_list)
		# TODO: make tests of other things in the Writer
		dd = out.root_attributes()
		self.assertTrue(isinstance(dd, dict))
		
		#scan = spec_data.scans[1]
		#print (etree.tostring(scan.UXML_root))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.testName']
	unittest.main()
	
# 	for test_classes in (TestPlugin, TestData):
# 		suite = unittest.TestLoader().loadTestsFromTestCase(test_classes)
# 		unittest.TextTestRunner(verbosity=2).run(suite)
