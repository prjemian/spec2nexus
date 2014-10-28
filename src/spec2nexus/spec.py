#!/usr/bin/env python 
# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------
# :author:    Pete R. Jemian
# :email:     prjemian@gmail.com
# :copyright: (c) 2014, Pete R. Jemian
#
# Distributed under the terms of the Creative Commons Attribution 4.0 International Public License.
#
# The full license is in the file LICENSE.txt, distributed with this software.
#-----------------------------------------------------------------------------


"""
Provides a set of classes to read the contents of a SPEC data file.

:author: Pete Jemian
:email: jemian@anl.gov

:meth:`~spec2nexus.spec.SpecDataFile` is the only class users will need to call.
All other :mod:`~spec2nexus.spec` classes are called from this class.
The :meth:`~spec2nexus.spec.SpecDataFile.read` method is called automatically.

The user should create a class instance for each spec data file,
specifying the file reference (by path reference as needed)
and the internal routines will take care of all that is necessary
to read and interpret the information.

..  -----------------------------------------------------------------------------------------
    old documentation
    -----------------------------------------------------------------------------------------
    
    .. index:: SPEC data file structure

    The parser makes the assumption that a SPEC data file is composed from
    a sequence of component blocks.  The component blocks are either header 
    or scan blocks.  Header blocks have the first line starting with ``#F``
    while scan blocks have the first line starting with ``#S``.  Usually,
    there is only one header block in a SPEC data file, followed by many 
    scan blocks.  The header block contains information common to all the 
    scan blocks that follow it.  Content for each block continues until 
    the next block starts or the file ends.  The pattern is:
    
    * #F line starts a header block
    * there could be multiple #F lines in a data file
    * #S lines start a SPEC scan
    * everything between #F and the next #S is header content
    * everything after a #S line is scan content (until EOF, the next #S or the next #F)
    
    .. rubric:: Additional assumptions
    
    * Lines that begin with ``#`` contain metadata of some form.
    * Lines that begin with ``@`` contain MCA data
    * Lines that begin with a number are data points
    * Line that are blank will be ignored
    * Lines that begin with anything else are unexpected and will be ignored
    
    For lines that begin with ``#``, these hold keys to some form of metadata.
    Some of the keys are identified and used by the SPEC standard.mac (and other) 
    macro files.  Other keys are left to the user to define.  There are two 
    general types of key, best described by a regular expression:

    ====================  ============  ============================
    regexp                example       how it appears
    ====================  ============  ============================
    ``^#[a-zA-Z]+\s``     ``#S``        by itself
    ``^#[a-zA-Z]+\d+\s``  ``#P5``       part of a numbered series
    ====================  ============  ============================
    
    Note that keys that appear as part of a numbered series (such as ``#O0 #O1 #O2`` ...),
    usually have numbers starting at 0.  
    -----------------------------------------------------------------------------------------

Note that the SPEC geometry control lines (``#G0 #G1`` ...)
have meanings that are unique to specific diffractometer geometries including
different numbers of values.  Consult the geometry macro file for specifics.



.. rubric:: Examples

Get the first and last scan numbers from the file:

    >>> from spec2nexus import spec
    >>> spec_data = spec.SpecDataFile('path/to/my/spec_data.dat')
    >>> print spec_data.fileName
    path/to/my/spec_data.dat
    >>> print 'first scan: ', spec_data.getMinScanNumber()
    1
    >>> print 'last scan: ', spec_data.getMaxScanNumber()
    22

Get plottable data from scan number 10:

    >>> from spec2nexus import spec
    >>> spec_data = spec.SpecDataFile('path/to/my/spec_data.dat')
    >>> scan10 = spec_data.getScan(10)
    >>> x_label = scan10.L[0]
    >>> y_label = scan10.L[-1]
    >>> x_data = scan10.data[x_label]
    >>> y_data = scan10.data[y_label]


Try to read a file that does not exist:

    >>> spec_data = spec.SpecDataFile('missing_file')
    Traceback (most recent call last):
      ...
    spec.SpecDataFileNotFound: file does not exist: missing_file

.. rubric::  Classes and Methods

"""


import re       #@UnusedImport
import os       #@UnusedImport
import sys      #@UnusedImport
from spec2nexus.utils import get_all_plugins
from lxml import etree


plugin_manager = None   # will initialize when SpecDataFile is first called


class SpecDataFileNotFound(IOError): 
    '''data file was not found'''
    pass

class SpecDataFileCouldNotOpen(IOError): 
    '''data file could not be opened'''
    pass

class NotASpecDataFile(Exception): 
    '''content of file is not SPEC data (first line must start with ``#F``)'''
    pass

class DuplicateSpecScanNumber(Exception): 
    '''multiple use of scan number in a single SPEC data file'''
    pass

class UnknownSpecFilePart(Exception): 
    '''unknown part in a single SPEC data file'''
    pass


def is_spec_file(filename):
    '''
    test if a given file name is a SPEC data file
    
    :param str filename: path/to/possible/spec/data.file

    *filename* is a SPEC file only if the file starts [#]_ 
    with these control lines in order:

    * #F    - original filename
    * #E    - the UNIX epoch (seconds from 00:00 GMT 1/1/70)
    * #D    - current date and time in UNIX format
    * #C    - comment line (the first one provides the filename again and the user name)

    such as::

        #F LNO_LAO
        #E 1276730676
        #D Wed Jun 16 18:24:36 2010
        #C LNO_LAO  User = epix33bm
    
    .. [#] SPEC manual, *Standard Data File Format*, http://www.certif.com/spec_manual/user_1_4_1.html
    '''
    if not os.path.exists(filename):
        return False
    if not os.path.isfile(filename):
        return False
    expected_controls = ('#F ', '#E ', '#D ', '#C ')
    lines = open(filename).readlines()[:len(expected_controls)]
    if len(lines) != len(expected_controls):
        return False
    for expected, line in zip(expected_controls, lines):
        if not line.startswith(expected):
            return False
    return True


#-------------------------------------------------------------------------------------------


class SpecDataFile(object):
    '''
    contents of a spec data file
    '''

    fileName = ''
    parts = ''
    headers = []
    scans = {}
    readOK = -1

    def __init__(self, filename):
        global plugin_manager
        self.fileName = None
        self.headers = []
        self.scans = {}
        self.readOK = -1
        if not os.path.exists(filename):
            raise SpecDataFileNotFound, 'file does not exist: ' + str(filename)
        if not is_spec_file(filename):
            raise NotASpecDataFile, 'not a SPEC data file: ' + str(filename)
        self.fileName = filename

        if plugin_manager is None:
            plugin_manager = get_all_plugins()
        self.plugin_manager = plugin_manager

        self.read()

    def read(self):
        """Reads and parses a spec data file"""
        buf = self._read_file_(self.fileName)
        
        text = buf.splitlines()[0].strip()
        key = self.plugin_manager.getKey(text)
        if key != '#F':
            raise NotASpecDataFile('First line does not start with #F: ' + self.fileName)
        self.plugin_manager.process(key, text, self)
        buf = buf[len(text):]

        #------------------------------------------------------
        # identify all header blocks: split buf on #E control lines
        headers = []
        for part in buf.split('\n#E '):         # Identify the spec file header sections (usually just 1)
            if len(part) == 0: continue         # just in case
            key = self.plugin_manager.getKey(part.splitlines()[0].strip())
            if key != '#E':
                headers.append('#E ' + part)        # new header is starting
        del buf                                 # Dispose of the input buffer memory (necessary?)
        # headers is a list of the #E header blocks (contains all #S scan blocks)

        #------------------------------------------------------
        # walk through all header blocks: split each header block on #S control lines
        self.parts = []         # break into list of blocks, either #E or #S, in order of appearance
        for part in headers:
            for block in part.split('\n#S '):   # break header sections by scans
                text = block.splitlines()[0].strip()
                if self.plugin_manager.getKey(text) not in ('#E', '#S'):
                    block = '#S ' + block
                self.parts.append(block)        # keep each block (starts with either #E or #S)
        del headers, block
        # self.parts is a list of the #E and #S parts

        #------------------------------------------------------
        # pull the information from each scan head
        for part in self.parts:
            text = part.splitlines()[0].strip()
            key = self.plugin_manager.getKey(text)
            if key in ('#E', '#S'):
                self.plugin_manager.process(key, part, self)
            else:
                raise UnknownSpecFilePart(part.splitlines()[0].strip())

    def _read_file_(self, spec_file_name):
        """Reads a spec data file"""
        try:
            buf = open(spec_file_name, 'r').read()
        except IOError:
            msg = 'Could not open spec file: ' + str(spec_file_name)
            raise SpecDataFileCouldNotOpen, msg
        if not is_spec_file(spec_file_name):
            msg = 'Not a spec data file: ' + str(spec_file_name)
            raise NotASpecDataFile(msg)
        return buf
    
    def getScan(self, scan_number=0):
        '''return the scan number indicated, None if not found'''
        if scan_number < 1:
            # relative list index, convert to actual scan number
            keylist = sorted(self.scans.keys())
            key = len(keylist) + scan_number
            if 0 <= key < len(keylist):
                scan_number = keylist[key]
            else:
                return None
        if scan_number in self.scans:
            return self.scans[scan_number]
        return None
    
    def getScanNumbers(self):
        '''return a list of all scan numbers'''
        return self.scans.keys()
    
    def getMinScanNumber(self):
        '''return the lowest numbered scan'''
        return min(self.getScanNumbers())
    
    def getMaxScanNumber(self):
        '''return the highest numbered scan'''
        return max(self.getScanNumbers())
    
    def getScanCommands(self, scan_list=None):
        '''return all the scan commands as a list, with scan number'''
        if scan_list is None:
            scan_list = sorted(self.getScanNumbers())
        return ['#S ' + str(key) + ' ' + self.scans[key].scanCmd for key in scan_list if key in self.scans]


#-------------------------------------------------------------------------------------------


class SpecDataFileHeader(object):
    """contents of a spec data file header (#F) section"""

    def __init__(self, buf, parent = None):
        #----------- initialize the instance variables
        self.parent = parent        # instance of SpecDataFile
        self.comments = []
        self.date = ''
        self.epoch = 0
        if parent is None:
            self.file = None
        else:
            self.file = parent.fileName
        self.H = []
        self.O = []
        self.raw = buf

    def interpret(self):
        """ interpret the supplied buffer with the spec data file header"""
        for i, line in enumerate(self.raw.splitlines(), start=1):
            if len(line) == 0:
                continue            # ignore blank lines
            key = self.parent.plugin_manager.getKey(line)
            if key is None:
                raise UnknownSpecFilePart("line %d: unknown header line: %s" % (i, line))
            elif key == '#E':
                pass    # avoid recursion
            else:
                # most of the work is done here
                self.parent.plugin_manager.process(key, line, self)


#-------------------------------------------------------------------------------------------

LAZY_INTERPRET_SCAN_DATA_ATTRIBUTES = [
    'comments', 'data', 'data_lines', 'date', 'G', 'I',
    'L', 'M', 'positioner', 'N', 'P', 'Q', 'T',
    'column_first', 'column_last'
]


class SpecDataFileScan(object):
    """contents of a spec data file scan (#S) section"""

    def __init__(self, header, buf, parent=None):
        self.parent = parent        # instance of SpecDataFile
        self.comments = []
        self.data = {}
        self.data_lines = []
        self.date = ''
        self.G = {}
        self.header = header        # index number of relevant #F section previously interpreted
        self.L = []
        self.M = ''
        self.positioner = {}
        self.N = -1
        self.P = []
        self.Q = ''
        self.raw = buf
        self.S = ''
        self.scanNum = -1
        self.scanCmd = ''
        if parent is not None:
            # avoid changing the interface for clients
            self.specFile = parent.fileName
        elif self.header is not None:
	    if self.header.parent is not None:
                self.specFile = self.header.parent.fileName
        else:
            self.specFile = None
        self.T = ''
        self.V = []
        self.column_first = ''
        self.column_last = ''
        self.postprocessors = {}
        self.h5writers = {}
    
        # the attributes defined in LAZY_INTERPRET_SCAN_DATA_ATTRIBUTES
        # (and perhaps others) are set only after a call to self.interpret()
        # That call is triggered on the first call for any of these attributes.
        self.__lazy_interpret__ = True
        self.__interpreted__ = False
    
    def __str__(self):
        return self.S
    
    def __getattribute__(self, attr):
        if attr in LAZY_INTERPRET_SCAN_DATA_ATTRIBUTES:
            if self.__lazy_interpret__:
                self.interpret()
        return object.__getattribute__(self, attr)
        

    def interpret(self):
        """interpret the supplied buffer with the spec scan data"""
        if self.__interpreted__:    # do not do this twice
            return
        self.__lazy_interpret__ = False     # set now to avoid recursion
        lines = self.raw.splitlines()
        for i, line in enumerate(lines, start=1):
            if len(line) == 0:
                continue            # ignore blank lines
            key = self.parent.plugin_manager.getKey(line.lstrip())
            if key is None:
                __s__ = '<' + line + '>'
                msg = "scan %d, line %d: unknown key, ignored text: %s" % (self.scanNum, i, line)
                #raise UnknownSpecFilePart(msg)
            elif key == '#S':
                pass        # avoid recursion
            else:
                # most of the work is done here
                self.parent.plugin_manager.process(key, line, self)

        # call any post-processing hook functions from the plugins
        for func in self.postprocessors.values():
            func(self)
        
        self.__interpreted__ = True
    
    def addPostProcessor(self, label, func):
        '''
        add a function to be processed after interpreting all lines from a scan
        
        :param str label: unique label by which this postprocessor will be known
        :param obj func: function reference of postprocessor
        
        The postprocessors will be called at the end of scan data interpretation.
        '''
        if label not in self.postprocessors:
            self.postprocessors[label] = func
    
    def addH5writer(self, label, func):
        '''
        add a function to be processed when writing the scan data
        
        :param str label: unique label by which this writer will be known
        :param obj func: function reference of writer
        
        The writers will be called when the HDF5 file is to be written.
        '''
        if label not in self.h5writers:
            self.h5writers[label] = func
    
    def _interpret_data_row(self, row_text):
        buf = {}
        for col, val in enumerate(row_text.split()):
            label = self.L[col]
            buf[label] = float(val)
        return buf

    def _unique_key(self, label, keylist):
        '''ensure that label is not yet existing in keylist'''
        i = 0
        key = label
        while key in keylist:
            i += 1
            key = label + '_' + str(i)
            if i == 1000:
                raise RuntimeError, "cannot make unique key for duplicated column label!"
        return key


#-------------------------------------------------------------------------------------------

def prettify(someXML):
    #for more on lxml/XSLT see: http://lxml.de/xpathxslt.html#xslt-result-objects
    xslt_tree = etree.XML('''\
        <!-- XSLT taken from Comment 4 by Michael Kay found here:
        http://www.dpawson.co.uk/xsl/sect2/pretty.html#d8621e19 -->
        <xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
        <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
          <xsl:strip-space elements="*"/>
          <xsl:template match="/">
            <xsl:copy-of select="."/>
          </xsl:template>
        </xsl:stylesheet>''')
    transform = etree.XSLT(xslt_tree)
    result = transform(someXML)
    return unicode(result)

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
        spec_file_name = os.path.join(spec_dir, '33id_spec.dat')
        #spec_file_name = os.path.join(spec_dir, '33bm_spec.dat')
        #spec_file_name = os.path.join(spec_dir, 'CdSe')
        #spec_file_name = os.path.join(spec_dir, 'lmn40.spe')
        #spec_file_name = os.path.join(spec_dir, 'YSZ011_ALDITO_Fe2O3_planar_fired_1.spc')
        #spec_file_name = os.path.join(spec_dir, '130123B_2.spc')
        os.chdir(spec_dir)
    print '-'*70
    # now open the file and read it
    test = SpecDataFile(spec_file_name)
    scan = test.scans[1]
    scan.interpret()
    print scan.UXML_root
    
    print prettify(scan.UXML_root)
    if False:
        # tell us about the test file
        print 'file', test.fileName
        print 'headers', len(test.headers)
        print 'scans', len(test.scans)
        #print 'positioners in first scan:'; print test.scans[0].positioner
        for scan in test.scans.values():
            # print scan.scanNum, scan.date, scan.column_first, scan.positioner[scan.column_first], 'eV', 1e3*scan.metadata['DCM_energy']
            print scan.scanNum, scan.scanCmd
        print 'first scan: ', test.getMinScanNumber()
        print 'last scan: ', test.getMaxScanNumber()
        print 'positioners in last scan:'
        last_scan = test.getScan(-1)
        print last_scan.positioner
        pLabel = last_scan.column_first
        dLabel = last_scan.column_last
        if len(pLabel) > 0:
            print last_scan.data[pLabel]
            print len(last_scan.data[pLabel])
            print pLabel, dLabel
            for i in range(len(last_scan.data[pLabel])):
                print last_scan.data[pLabel][i], last_scan.data[dLabel][i]
        print 'labels in scan 1:', test.getScan(1).L
        if test.getScan(5) is not None:
            print 'command line of scan 5:', test.getScan(5).scanCmd
        print '\n'.join(test.getScanCommands([5, 10, 15, 29, 40, 75]))
    pass


if __name__ == "__main__":
    fname = 'test_3.spec'
    spec_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data', 'uxml', ))
    os.environ['SPEC2NEXUS_PLUGIN_PATH'] = spec_dir
    developer_test(os.path.join(spec_dir, fname))
