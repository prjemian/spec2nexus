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
(Legacy) Provides a set of classes to read the contents of a SPEC data file.  Support frozen at version 2014.0623.0.

:author: Pete Jemian
:email: jemian@anl.gov

.. note:  This code provides the interface of version 2014.0623.0 and is 
   being retained to avoid breaking existing code that calls this interface.
   
   For new coding efforts using releases of spec2nexus after version 2014.0623.0, 
   please use *pySpec.py* in this package.

:meth:`~spec2nexus.prjPySpec.SpecDataFile` is the only class users will need to call.
All other :mod:`~spec2nexus.prjPySpec` classes are called from this class.
The :meth:`~spec2nexus.prjPySpec.SpecDataFile.read` method is called automatically.

Includes the UNICAT control lines which write additional metadata
in the scan headers using #H/#V pairs of labels/values.
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

    >>> from spec2nexus import prjPySpec
    >>> spec_data = prjPySpec.SpecDataFile('path/to/my/spec_data.dat')
    >>> print spec_data.fileName
    path/to/my/spec_data.dat
    >>> print 'first scan: ', spec_data.getMinScanNumber()
    1
    >>> print 'last scan: ', spec_data.getMaxScanNumber()
    22

Get plottable data from scan number 10:

    >>> from spec2nexus import prjPySpec
    >>> spec_data = prjPySpec.SpecDataFile('path/to/my/spec_data.dat')
    >>> scan10 = spec_data.getScan(10)
    >>> x_label = scan10.L[0]
    >>> y_label = scan10.L[-1]
    >>> x_data = scan10.data[x_label]
    >>> y_data = scan10.data[y_label]


Try to read a file that does not exist:

    >>> spec_data = prjPySpec.SpecDataFile('missing_file')
    Traceback (most recent call last):
      ...
    prjPySpec.SpecDataFileNotFound: file does not exist: missing_file

.. rubric::  Classes and Methods

"""


import re       #@UnusedImport
import os       #@UnusedImport
import sys      #@UnusedImport


class SpecDataFileNotFound(IOError): 
    '''data file was not found'''
    pass

class SpecDataFileCouldNotOpen(IOError): 
    '''data file could not be opened'''
    pass

class NotASpecDataFile(Exception): 
    '''content of file is not SPEC data (first line must start with ``#F``)'''
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
    expected_controls = ('#F ', '#E ', '#D ', '#C ')
    lines = open(filename).readlines()[:len(expected_controls)]
    if len(lines) != len(expected_controls):
        return False
    for expected, line in zip(expected_controls, lines):
        if not line.startswith(expected):
            return False
    return True


def strip_first_word(line):
    """return everything after the first space on the line from the spec data file"""
    pos = line.find(" ")
    val = line[pos:]
    return val.strip()


#-------------------------------------------------------------------------------------------


class SpecDataFile(object):
    '''
    contents of a spec data file
    '''

    fileName = ''
    parts = ''
    errMsg = ''
    headers = []
    scans = {}
    readOK = -1

    def __init__(self, filename):
        self.fileName = None
        self.errMsg = ''
        self.headers = []
        self.scans = {}
        self.readOK = -1
        if not os.path.exists(filename):
            raise SpecDataFileNotFound, 'file does not exist: ' + str(filename)
        if not is_spec_file(filename):
            raise NotASpecDataFile, 'not a SPEC data file: ' + str(filename)
        self.fileName = filename
        self.read()

    def read(self):
        """Reads a spec data file"""
        try:
            buf = open(self.fileName, 'r').read()
        except IOError:
            msg = 'Could not open spec file: ' + str(self.fileName)
            raise SpecDataFileCouldNotOpen, msg
        if not is_spec_file(self.fileName):
            msg = 'Not a spec data file: ' + str(self.fileName)
            self.errMsg = '\n' + msg + '\n'
            raise NotASpecDataFile, msg
        #------------------------------------------------------
        headers = []
        for part in buf.split('\n#E '):         # Identify the spec file header sections (usually just 1)
            if len(part) == 0: continue         # just in case
            if part.startswith('#F'): 
                self.specFile = strip_first_word(part).strip()
                continue
            headers.append('#E ' + part)        # remember the new header is starting
        del buf                                 # Dispose of the input buffer memory (necessary?)

        self.parts = []         # break into list of blocks, either #E or #S, in order of appearance
        for part in headers:
            for block in part.split('\n#S '):   # break header sections by scans
                if not block.startswith('#S ') and not block.startswith('#E '):
                    block = '#S ' + block
                self.parts.append(block)        # keep each block (starts with either #E or #S
        del headers, block
        #------------------------------------------------------
        # pull the information from each scan head
        for part in self.parts:
            if part.startswith('#E'):
                self.headers.append(SpecDataFileHeader(part, parent=self))
            elif part.startswith('#S'):
                scan = SpecDataFileScan(self.headers[-1], part)
                if scan.scanNum not in self.scans:      # FIXME: silently ignores repeated use of same scan number
                    self.scans[scan.scanNum] = scan
            else:
                self.errMsg = "unknown SPEC data file part: " + part.splitlines()[0].strip()
        self.readOK = 0     # consider raising exceptions instead
    
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
        return self.scans[scan_number]
    
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
        return ['#S ' + str(key) + self.scans[key].scanCmd for key in scan_list if key in self.scans]


#-------------------------------------------------------------------------------------------


class SpecDataFileHeader(object):
    """contents of a spec data file header (#F) section"""

    def __init__(self, buf, parent = None):
        #----------- initialize the instance variables
        self.parent = parent        # instance of SpecDataFile
        self.comments = []
        self.date = ''
        self.epoch = 0
        self.errMsg = ''
        #self.file = None
        self.H = []
        self.O = []
        self.raw = buf
        self.interpret()

    def interpret(self):
        """ interpret the supplied buffer with the spec data file header"""
        lines = self.raw.splitlines()
        i = 0
        for line in lines:
            i += 1
            if len(line) == 0:
                continue            # ignore blank lines
            key = line[0:line.find(' ')].strip()
            if (line.startswith('#C')):
                self.comments.append(strip_first_word(line))
            elif (line.startswith('#D')):
                self.date = strip_first_word(line)
            elif (line.startswith('#E')):
                self.epoch = int(strip_first_word(line))
            #elif (line.startswith('#F')):
            #    self.file = strip_first_word(line)
            elif (line.startswith('#H')):
                self.H.append(strip_first_word(line).split())
            elif (line.startswith('#O')):
                self.O.append(strip_first_word(line).split())
            else:
                self.errMsg = "line %d: unknown key (%s) detected" % (i, key)


#-------------------------------------------------------------------------------------------


class SpecDataFileScan(object):
    """contents of a spec data file scan (#S) section"""
    
    def __init__(self, header, buf, parent=None):
        self.parent = parent        # instance of SpecDataFile
        self.comments = []
        self.data = {}
        self.data_lines = []
        self.date = ''
        self.errMsg = ''
        self.G = {}
        self.header = header        # index number of relevant #F section previously interpreted
        self.L = []
        self.metadata = {}             # UNICAT-style metadata in the header (non-positioners)
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
        else:
            self.specFile = ''
        self.T = ''
        self.V = []
        self.column_first = ''
        self.column_last = ''
        self.interpret()
    
    def __str__(self):
        return self.S

    def interpret(self):
        """interpret the supplied buffer with the spec scan data"""
        lines = self.raw.splitlines()
        i = 0
        for line in lines:
            i += 1
            if len(line) == 0:
                continue            # ignore blank lines
            if (line.startswith('#')):
                if (line.startswith('#C')):
                    self.comments.append(strip_first_word(line))
                elif (line.startswith('#D')):
                    self.date = strip_first_word(line)
                elif (line.startswith('#G')):      # diffractometer geometry
                    subkey = line.split()[0].lstrip('#')
                    self.G[subkey] = strip_first_word(line)
                elif (line.startswith('#L')):
                    # Some folks use more than two spaces!  Use regular expression(re) module
                    self.L = re.split("  +", strip_first_word(line))
                    self.column_first = self.L[0]
                    self.column_last = self.L[-1]
                elif (line.startswith('M')):
                    self.M, dname = strip_first_word(line).split()
                    self.monitor_name = dname.lstrip('(').rstrip(')')
                elif (line.startswith('#N')):
                    self.N = int(strip_first_word(line))
                elif (line.startswith('#P')):
                    self.P.append(strip_first_word(line))
                elif (line.startswith('#Q')):
                    self.Q = strip_first_word(line)
                elif (line.startswith('#S')):
                    self.S = strip_first_word(line)
                    pos = self.S.find(" ")
                    self.scanNum = int(self.S[0:pos])
                    self.scanCmd = self.S[pos+1:]
                elif (line.startswith('#T')):
                    self.T = strip_first_word(line).split()[0]
                elif (line.startswith('#V')):
                    self.V.append(strip_first_word(line))
                else:
                    self.errMsg = "line %d: unknown key, text: %s" % (i, line)
            elif len(line) < 2:
                self.errMsg = "problem with scan header line " + str(i) + ' text: ' + line
            elif line[0:2] == "#@":
                self.errMsg = "cannot handle #@ data yet."
            else:
                self.data_lines.append(line)
        #print self.scanNum, "\n\t".join( self.comments )
        # interpret the motor positions from the scan header
        self.positioner = {}
        for row, values in enumerate(self.P):
            for col, val in enumerate(values.split()):
                if row >= len(self.header.O):
                    continue    # ignore data from any added positioner rows
                if col >= len(self.header.O[row]):
                    continue    # ignore data from any added positioner columns
                mne = self.header.O[row][col]
                self.positioner[mne] = float(val)
        # interpret the UNICAT metadata (mostly floating point) from the scan header
        self.metadata = {}
        for row, values in enumerate(self.V):
            for col, val in enumerate(values.split()):
                label = self.header.H[row][col]
                try:
                    self.metadata[label] = float(val)
                except ValueError:
                    self.metadata[label] = val
        # interpret the data lines from the body of the scan
        self.data = {}
        for col in range(len(self.L)):
            label = self._unique_key(self.L[col], self.data.keys())
            # need to guard when same column label is used more than once
            if label != self.L[col]:
                self.L[col] = label    # rename this column's label
            self.data[label] = []
        in_array_data = False
        for row, values in enumerate(self.data_lines):
            if values.startswith('@A'):     # Can there be more than 1 specified?
                in_array_data = True
                if '_mca_' not in self.data:
                    self.data['_mca_'] = []
                mca_spectrum = []       # accumulate this spectrum
                values = values[2:]     # strip the header
            if in_array_data:
                if not values.endswith('\\'):
                    in_array_data = False       # last row of this spectrum
                mca_spectrum += map(float, values.rstrip('\\').split())
                if not in_array_data:   # last step, add to data column
                    self.data['_mca_'].append(mca_spectrum)
            else:
                buf = self._interpret_data_row(values)
                if len(buf) == len(self.data):      # only keep complete rows
                    for label, val in buf.items():
                        self.data[label].append(val)
    
    def _interpret_data_row(self, row_text):
        buf = {}
        for col, val in enumerate(row_text.split()):
            label = self.L[col]
            try:
                buf[label] = float(val)
            except ValueError:
                break
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


def developer_test(spec_file_name = None):
    """
    test the routines that read from the spec data file
    
    :param str spec_file_name: if set, spec file name is given on command line
    """
    if spec_file_name is None:
        path = os.path.join(os.path.dirname(__file__), 'data')
        spec_dir = os.path.abspath(path)
        spec_file_name = os.path.join(spec_dir, 'APS_spec_data.dat')
        #spec_file_name = os.path.join(spec_dir, '03_05_UImg.dat')
        os.chdir(spec_dir)
    print '-'*70
    # now open the file and read it
    test = SpecDataFile(spec_file_name)
    # tell us about the test file
    print 'file', test.fileName
    print 'OK?', test.readOK
    print 'headers', len(test.headers)
    print 'scans', len(test.scans)
    #print 'positioners in first scan:'; print test.scans[0].positioner
    for scan in test.scans.values():
        print scan.scanNum, scan.date, scan.column_first, scan.positioner[scan.column_first], 'eV', 1e3*scan.metadata['DCM_energy']
    print 'first scan: ', test.getMinScanNumber()
    print 'last scan: ', test.getMaxScanNumber()
    print 'positioners in last scan:'
    last_scan = test.getScan(-1)
    print last_scan.positioner
    pLabel = last_scan.column_first
    dLabel = last_scan.column_last
    print last_scan.data[pLabel]
    print len(last_scan.data[pLabel])
    print pLabel, dLabel
    for i in range(len(last_scan.data[pLabel])):
        print last_scan.data[pLabel][i], last_scan.data[dLabel][i]
    print test.getScan(1).L
    print test.getScan(5)
    print '\n'.join(test.getScanCommands([5, 10, 15, 29, 40, 75]))


def test_isSpecFile():
    '''for the developer'''
    import glob
    for fname in glob.glob('data/*'):
        t = is_spec_file(fname)
        print fname, t


if __name__ == "__main__":
    developer_test()
