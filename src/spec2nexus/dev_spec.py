#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""development of the :mod:`spec` module"""

# TODO: fold into the unit test suite


import os
from lxml import etree
from spec2nexus import spec

def prettify(someXML):
    #for more on lxml/XSLT see: http://lxml.de/xpathxslt.html#xslt-result-objects
    xslt_tree = etree.XML("""\
        <!-- XSLT taken from Comment 4 by Michael Kay found here:
        http://www.dpawson.co.uk/xsl/sect2/pretty.html#d8621e19 -->
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
          <xsl:strip-space elements="*"/>
          <xsl:template match="/">
            <xsl:copy-of select="."/>
          </xsl:template>
        </xsl:stylesheet>""")
    transform = etree.XSLT(xslt_tree)
    result = transform(someXML)
    return str(result)

def developer_test(spec_file_name = None):
    """
    test the routines that read from the spec data file
    
    :param str spec_file_name: if set, spec file name is given on command line
    """
    if spec_file_name is None:
        path = os.path.join(os.path.dirname(__file__), 'data')
        spec_dir = os.path.abspath(path)
        #spec_file_name = os.path.join(spec_dir, 'APS_spec_data.dat')
        #spec_file_name = os.path.join(spec_dir, '03_05_UImg.dat')
        #spec_file_name = os.path.join(spec_dir, '33id_spec.dat')
        #spec_file_name = os.path.join(spec_dir, '33bm_spec.dat')
        #spec_file_name = os.path.join(spec_dir, 'CdSe')
        #spec_file_name = os.path.join(spec_dir, 'lmn40.spe')
        #spec_file_name = os.path.join(spec_dir, 'YSZ011_ALDITO_Fe2O3_planar_fired_1.spc')
        #spec_file_name = os.path.join(spec_dir, '130123B_2.spc')
        spec_file_name = os.path.join(spec_dir, 'user6idd.dat')
        os.chdir(spec_dir)
        print ('-'*70)
    # now open the file and read it
    test = spec.SpecDataFile(spec_file_name)
    scan = test.getScan(1)
    scan.interpret()
    #print (scan.UXML_root)
    #print (prettify(scan.UXML_root))

    if False:
        # tell us about the test file
        print ('file %s' % test.fileName)
        print ('headers %d' % len(test.headers))
        print ('scans %d' % len(test.scans))
        #print ('positioners in first scan:'); print (test.scans[0].positioner)
        for scan in test.scans.values():
            # print (scan.scanNum, scan.date, scan.column_first, scan.positioner[scan.column_first], 'eV', 1e3*scan.metadata['DCM_energy'])
            print (scan.scanNum, scan.scanCmd)
        print ('first scan: %s' % test.getMinScanNumber())
        print ('last scan: %s' % test.getMaxScanNumber())
        print ('positioners in last scan:')
        last_scan = test.getScan(-1)
        print (last_scan.positioner)
        pLabel = last_scan.column_first
        dLabel = last_scan.column_last
        if len(pLabel) > 0:
            print (last_scan.data[pLabel])
            print (len(last_scan.data[pLabel]))
            print (pLabel, dLabel)
            for i in range(len(last_scan.data[pLabel])):
                print (last_scan.data[pLabel][i], last_scan.data[dLabel][i])
        print ('labels in scan 1: %s' % test.getScan(1).L)
        if test.getScan(1) is not None:
            print ('command line of scan 5: %s' % test.getScan(5).scanCmd)
        print ('\n'.join(test.getScanCommands([1, 2])))
    pass


if __name__ == "__main__":
    full_name = None
    full_name = 'data/xpcs_plugin_sample.spec'
    developer_test(full_name)
