#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014-2016, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------

"""
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

"""


from lxml import etree
import os
import six
import sys

from spec2nexus import eznx
from spec2nexus.plugin import AutoRegister
from spec2nexus.plugin import ControlLineHandler
from spec2nexus.utils import strip_first_word


DEFAULT_XML_ROOT_TAG = 'UXML'
UXML_SUPPLIES_ROOT_TAG = False
_path = os.path.dirname(__file__)
XML_SCHEMA = os.path.join(_path, "uxml.xsd")


class UXML_Error(Exception): ...


link_ids = None

# TODO: does not need to be separate classes here
class Dataset(object):
    
    """HDF5/NeXus dataset specification"""

    def __init__(self, h5parent, xml_node):
        attrs = dict(xml_node.attrib)

        self.name = attrs.get('name')
        if self.name is not None:
            del attrs["name"]

        data_type = attrs.get('type')
        if data_type is None:
            data_type = "str"
        else:
            del attrs["type"]

        # TODO: unique_id attribute?

        self.value = xml_node.text

        eznx.makeDataset(h5parent, self.name, self.value, **attrs)


class Group(object):
    
    """HDF5/NeXus group specification"""

    def __init__(self, h5parent, xml_node):
        global link_ids
        _links = link_ids

        attrs = dict(xml_node.attrib)

        self.name = attrs.get('name')
        if self.name is not None:
            del attrs["name"]

        self.NX_class = attrs.get('NX_class')
        if self.NX_class is not None:
            del attrs["NX_class"]

        self.unique_id = attrs.get('unique_id')
        if self.unique_id is not None:
            # TODO: store unique_id in a dict
            #   make sure that dict is cleared with each new scan
            del attrs["unique_id"]

        self.group = eznx.makeGroup(
            h5parent, 
            self.name, 
            self.NX_class, 
            **attrs)

        if self.unique_id is not None:
            link_ids[self.unique_id] = self.group.name
        
        build_HDF5_tree(self.group, xml_node)


class Hardlink(object):
    
    """HDF5/NeXus hard link specification"""

    def __init__(self, h5parent, xml_node):
        global link_ids

        attrs = dict(xml_node.attrib)

        self.name = attrs.get('name')
        if self.name is not None:
            del attrs["name"]

        if "target_id" in attrs:
            self.target_id = attrs["target_id"]
            del attrs["target_id"]
            # TODO: need to make the links *AFTER* all unique_id have been found
            if self.target_id in link_ids:
                source = link_ids[self.target_id]
                z = 2


def build_HDF5_tree(h5parent, xml_node):
    selector = dict(dataset=Dataset, group=Group, hardlink=Hardlink)
    for item in xml_node:
        obj = selector[item.tag](h5parent, item)
        print(item.tag, item.get('name'), obj, obj.name)


@six.add_metaclass(AutoRegister)
class UXML_metadata(ControlLineHandler):

    """
    **#UXML** -- XML metadata in scan header
    
    IN-MEMORY REPRESENTATION
    
    * (SpecDataFileScan): **UXML** : XML document root
    
    HDF5/NeXus REPRESENTATION
    
    * various items below the *NXentry* parent group,
      as indicated in the UXML

    """

    key = '#UXML'
    
    def process(self, text, scan, *args, **kws):
        if not hasattr(scan, 'UXML'):
            scan.UXML = []

        line = strip_first_word(text)
        scan.UXML.append( line )
        scan.addPostProcessor('UXML_metadata', self.postprocess)
    
    def postprocess(self, scan, *args, **kws):
        """
        convert the list of UXML text into a single text block
        
        :param SpecDataFileScan scan: data from a single SPEC scan
        """
        xml_text = '\n'.join(scan.UXML)
        if UXML_SUPPLIES_ROOT_TAG:
            root = etree.fromstring(xml_text)
            # read root_tag from supplied UXML lines
        else:
            # provide default root tag
            xml_text = '<%s>\n' % DEFAULT_XML_ROOT_TAG + xml_text + '\n</%s>' % DEFAULT_XML_ROOT_TAG
            root = etree.fromstring(xml_text)
    
        scan.UXML_root = root
        # validate against the schema
        xml_schema_tree = etree.parse(XML_SCHEMA)
        xml_schema = etree.XMLSchema(xml_schema_tree)

        if not xml_schema.validate(root):
            # XML file is not valid, let lxml report what is wrong as an exception
            #log = xmlschema.error_log    # access more details
            try:
                xml_schema.assertValid(root)   # basic exception report
            except etree.DocumentInvalid as exc:
                emsg = "UXML error: " + str(exc)
                # logger.warn(emsg)
                raise UXML_Error(emsg)

        scan.addH5writer('UXML_metadata', self.writer)
    
    def writer(self, h5parent, writer, scan, *args, **kws):
        """Describe how to store this data in an HDF5 NeXus file"""
        global link_ids
        link_ids = {}       # clear with each new scan

        # FIXME:
        desc = 'UXML metadata'
        group = eznx.makeGroup(h5parent, 'UXML', 'NXentry', default='data')
        eznx.write_dataset(group, "counting_basis", desc)
        eznx.write_dataset(group, "T", float(scan.T), units='s', description = desc)
        
        # parse the XML and store
        build_HDF5_tree(group, scan.UXML_root)
