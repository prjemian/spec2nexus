#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
UXML header information

Excerpt::

    #UXML   <attenuator number="1" pv_prefix="33idd:filter:Fi1:">
    #UXML     <enable>Enable</enable>
    #UXML     <lock>Lock</lock>
    #UXML     <type>Ti</type>
    #UXML     <thickness type="float" units="um">251.000</thickness>
    #UXML     <attenuator_transmission type="float">1.83034167e-02</attenuator_transmission>
    #UXML     <status>Out</status>
    #UXML   </attenuator>

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

from spec2nexus.plugin import ControlLineHandler, strip_first_word
from lxml import etree


class UXML_metadata(ControlLineHandler):
    '''**#UXML** -- XML metadata in scan header'''

    key = '#UXML'
    
    def process(self, text, spec_obj, *args, **kws):
        if not hasattr(spec_obj, 'UXML'):
            spec_obj.UXML = []
        line = strip_first_word(text)
        spec_obj.UXML.append( line )
        spec_obj.addPostProcessor('UXML_metadata', uxml_metadata_postprocessing)


def uxml_metadata_postprocessing(scan):
    '''
    convert the list of UXML text into a single text block
    
    :param SpecDataFileScan scan: data from a single SPEC scan
    '''
    xml_text = '\n'.join(scan.UXML)
    try:
        root = etree.fromstring(xml_text)
        # TODO: read root_tag from supplied UXML lines
    except etree.XMLSyntaxError:
        # provisional support until UXML lines provide a root tag
        root_tag = 'pySpec_uxml'
        xml_text = '<%s>\n' % root_tag + xml_text + '\n</%s>' % root_tag
        root = etree.fromstring(xml_text)

    pass    # TODO: what to do next?
