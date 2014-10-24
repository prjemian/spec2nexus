#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
UXML header information

Document the UXML Language

Describe the Validation Process

Excerpt::

    #UXML <group name="attenuator_set" NX_class="NXcollection" prefix="33idd:filter:" description="33-ID-D Filters" unique_id="33idd:filter:">
    #UXML   <dataset name="attenuator_count" type="int">16</dataset>
    #UXML   <dataset name="energy_input">Mono</dataset>
    #UXML   <dataset name="energy_value" type="float" units="keV">16.00002</dataset>
    #UXML   <dataset name="wait_time" type="float" units="s">0.500</dataset>
    #UXML   <dataset name="transmission" type="float">1.00000000e+00</dataset>
    #UXML   <dataset name="binary_mask" type="int">0</dataset>
    #UXML   <dataset name="transmission_counter">trans</dataset>
    #UXML   <dataset name="mask_counter">filters</dataset>
    #UXML   <dataset name="corrdet_counter">corrdet</dataset>
    #UXML   <hardlink name="attenuator1" target_id="33idd:filter:Fi1:"/>
    #UXML   <hardlink name="attenuator2" target_id="33idd:filter:Fi2:"/>
    #UXML   <hardlink name="attenuator3" target_id="33idd:filter:Fi3:"/>
    #UXML   <hardlink name="attenuator4" target_id="33idd:filter:Fi4:"/>
    #UXML   <hardlink name="attenuator5" target_id="33idd:filter:Fi5:"/>
    #UXML   <hardlink name="attenuator6" target_id="33idd:filter:Fi6:"/>
    #UXML   <hardlink name="attenuator7" target_id="33idd:filter:Fi7:"/>
    #UXML   <hardlink name="attenuator8" target_id="33idd:filter:Fi8:"/>
    #UXML   <hardlink name="attenuator9" target_id="33idd:filter:Fi9:"/>
    #UXML   <hardlink name="attenuator10" target_id="33idd:filter:Fi10:"/>
    #UXML   <hardlink name="attenuator11" target_id="33idd:filter:Fi11:"/>
    #UXML   <hardlink name="attenuator12" target_id="33idd:filter:Fi12:"/>
    #UXML   <hardlink name="attenuator13" target_id="33idd:filter:Fi13:"/>
    #UXML   <hardlink name="attenuator14" target_id="33idd:filter:Fi14:"/>
    #UXML   <hardlink name="attenuator15" target_id="33idd:filter:Fi15:"/>
    #UXML   <hardlink name="attenuator16" target_id="33idd:filter:Fi16:"/>
    #UXML </group>
    #UXML <group name="attenuator1" NX_class="NXattenuator" number="1" pv_prefix="33idd:filter:Fi1:" unique_id="33idd:filter:Fi1:">
    #UXML   <dataset name="enable">Enable</dataset>
    #UXML   <dataset name="lock">Lock</dataset>
    #UXML   <dataset name="type">Ti</dataset>
    #UXML   <dataset name="thickness" type="float" units="micron">251.000</dataset>
    #UXML   <dataset name="attenuator_transmission" type="float">3.55764458e-02</dataset>
    #UXML   <dataset name="status">Out</dataset>
    #UXML </group>
    #UXML <group name="attenuator2" NX_class="NXattenuator" number="2" pv_prefix="33idd:filter:Fi2:" unique_id="33idd:filter:Fi2:">
    #UXML   <dataset name="enable">Enable</dataset>
    #UXML   <dataset name="lock">Lock</dataset>
    #UXML   <dataset name="type">Ti</dataset>
    #UXML   <dataset name="thickness" type="float" units="micron">512.000</dataset>
    #UXML   <dataset name="attenuator_transmission" type="float">1.10816011e-03</dataset>
    #UXML   <dataset name="status">Out</dataset>
    #UXML </group>

'''

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

from spec2nexus.plugin import ControlLineHandler
from spec2nexus.utils import strip_first_word
from spec2nexus import eznx, utils
from lxml import etree


DEFAULT_XML_ROOT_TAG = 'spec_uxml'


class UXML_metadata(ControlLineHandler):
    '''**#UXML** -- XML metadata in scan header'''

    key = '#UXML'
    
    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, 'UXML'):
            spec_obj.UXML = []

        line = strip_first_word(text)
        spec_obj.UXML.append( line )
        spec_obj.addPostProcessor('UXML_metadata', self.postprocess)
    
    def postprocess(self, scan, *args, **kws):
        '''
        convert the list of UXML text into a single text block
        
        :param SpecDataFileScan scan: data from a single SPEC scan
        '''
        xml_text = '\n'.join(scan.UXML)
        try:
            root = etree.fromstring(xml_text)   # perhaps root tag was provided
            # read root_tag from supplied UXML lines
        except etree.XMLSyntaxError:
            # provide default root tag
            xml_text = '<%s>\n' % DEFAULT_XML_ROOT_TAG + xml_text + '\n</%s>' % DEFAULT_XML_ROOT_TAG
            root = etree.fromstring(xml_text)
    
        scan.UXML_root = root
        # TODO: validate against the schema
        scan.addH5writer(self.key, self.writer)
    
    def writer(self, h5parent, writer, scan, *args, **kws):
        '''Describe how to store this data in an HDF5 NeXus file'''
        desc = 'UXML metadata'
        #eznx.write_dataset(h5parent, "counting_basis", desc)
        #eznx.write_dataset(h5parent, "T", float(scan.T), units='s', description = desc)
        # TODO: parse the XML and store
