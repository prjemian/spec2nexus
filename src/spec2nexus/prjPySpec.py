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

Includes the UNICAT extensions which write additional metadata
in the scan headers using #H/#V pairs of labels/values.
The user should create a class instance for each spec data file,
specifying the file reference (by path reference as needed)
and the internal routines will take care of all that is necessary
to read and interpret the information.

:author: Pete Jemian
:email: jemian@anl.gov

**Dependencies**

* os: operating system package
* re: regular expression package
* sys: system package

"""

import re       #@UnusedImport
import os       #@UnusedImport
import sys      #@UnusedImport


__version__ = 'prjPySpec_2014-01-21'


def specScanLine_stripKey(line):
    """return everything after the first space on the line from the spec data file"""
    pos = line.find(" ")
    val = line[pos:]
    return val.strip()


#-------------------------------------------------------------------------------------------


class SpecDataFile(object):
    """contents of a spec data file"""

    fileName = ''
    parts = ''
    errMsg = ''
    headers = []
    scans = {}
    readOK = -1

    def __init__(self, filename):
        self.fileName = filename
        self.errMsg = ''
        self.headers = []
        self.scans = {}
        self.readOK = -1
        self.read()

    def read(self):
        """Reads a spec data file"""
        try:
            buf = open(self.fileName, 'r').read()
        except:
            self.errMsg = "\n Could not open spec file: " + self.fileName +"\n"
            self.readOK = 1
            return
        if (buf.count('#F ') <= 0):
            self.errMsg = '\n' + self.fileName + ' is not a spec data file.\n'
            self.readOK = 2
            return
        #------------------------------------------------------
        self.parts = buf.split('\n\n#')     # Break the spec file into component scans
        del buf                             # Dispose of the input buffer memory (necessary?)
        for index, substr in enumerate(self.parts):
            if (substr[0] != '#'):          # Was "#" stripped by the buf.split() above?
                self.parts[index]= '#' + substr  # Reinstall the "#" character on each part
        #------------------------------------------------------
        # pull the information from each scan head
        for part in self.parts:
            key = part[0:2]
            if (key == "#F"):
                self.headers.append(SpecDataFileHeader(part))
                self.specFile = self.headers[-1].file
            elif (key == "#S"):
                scan = SpecDataFileScan(self.headers[-1], part)
                key = scan.scanNum
                if key in self.scans:
                    pass                # TODO: what if?
                else:
                    self.scans[key] = scan
            else:
                self.errMsg = "unknown key: %s" % key
        self.readOK = 0
        return
    
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
    
    def getMinScanNumber(self):
        return min(self.scans.keys())
    
    def getMaxScanNumber(self):
        return max(self.scans.keys())


#-------------------------------------------------------------------------------------------


class SpecDataFileHeader(object):
    """contents of a spec data file header (#F) section"""

    def __init__(self, buf):
        #----------- initialize the instance variables
        self.comments = []
        self.date = ''
        self.epoch = 0
        self.errMsg = ''
        self.file = ''
        self.H = []
        self.O = []
        self.raw = buf
        self.interpret()
        return

    def interpret(self):
        """ interpret the supplied buffer with the spec data file header"""
        lines = self.raw.splitlines()
        i = 0
        for line in lines:
            i += 1
            key = line[0:2]
            if (key == "#C"):
                self.comments.append(specScanLine_stripKey(line))
            elif (key == "#D"):
                self.date = specScanLine_stripKey(line)
            elif (key == "#E"):
                self.epoch = int(specScanLine_stripKey(line))
            elif (key == "#F"):
                self.file = specScanLine_stripKey(line)
            elif (key == "#H"):
                self.H.append(specScanLine_stripKey(line).split())
            elif (key == "#O"):
                self.O.append(specScanLine_stripKey(line).split())
            else:
                self.errMsg = "line %d: unknown key (%s) detected" % (i, key)
        return


#-------------------------------------------------------------------------------------------


class SpecDataFileScan(object):
    """contents of a spec data file scan (#S) section"""
    
    def __init__(self, header, buf):
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
        self.specFile = ''
        self.T = ''
        self.V = []
        self.column_first = ''
        self.column_last = ''
        self.interpret()
        return
    
    def __str__(self):
        return self.S

    def interpret(self):
        """interpret the supplied buffer with the spec scan data"""
        lines = self.raw.splitlines()
        i = 0
        self.specFile = self.header.file    # this is the short name, does not have the file system path
        for line in lines:
            i += 1
            #print "[%s] %s" % (i, line)
            key = line[0:2]
            #print i, key
            if (key[0] == "#"):
                if (key == "#C"):
                    self.comments.append(specScanLine_stripKey(line))
                elif (key == "#D"):
                    self.date = specScanLine_stripKey(line)
                elif (key == "#G"):     # diffractometer geometry
                    subkey = line.split()[0].lstrip('#')
                    self.G[subkey] = specScanLine_stripKey(line)
                elif (key == "#L"):
                    # Some folks use more than two spaces!  Use regular expression(re) module
                    self.L = re.split("  +", specScanLine_stripKey(line))
                    self.column_first = self.L[0]
                    self.column_last = self.L[-1]
                elif (key == "#M"):
                    self.M, dname = specScanLine_stripKey(line).split()
                    self.monitor_name = dname.lstrip('(').rstrip(')')
                elif (key == "#N"):
                    self.N = int(specScanLine_stripKey(line))
                elif (key == "#P"):
                    self.P.append(specScanLine_stripKey(line))
                elif (key == "#Q"):
                    self.Q = specScanLine_stripKey(line)
                elif (key == "#S"):
                    self.S = specScanLine_stripKey(line)
                    pos = self.S.find(" ")
                    self.scanNum = int(self.S[0:pos])
                    self.scanCmd = self.S[pos+1:]
                elif (key == "#T"):
                    self.T = specScanLine_stripKey(line).split()[0]
                elif (key == "#V"):
                    self.V.append(specScanLine_stripKey(line))
                else:
                    self.errMsg = "line %d: unknown key (%s) detected" % (i, key)
            elif len(line) < 2:
                self.errMsg = "problem with  key " + key + " at scan header line " + str(i)
            elif key[1] == "@":
                self.errMsg = "cannot handle @ data yet."
            else:
                self.data_lines.append(line)
        #print self.scanNum, "\n\t".join( self.comments )
        # interpret the motor positions from the scan header
        self.positioner = {}
        for row, values in enumerate(self.P):
            for col, val in enumerate(values.split()):
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
                for col, val in enumerate(values.split()):
                    label = self.L[col]
                    self.data[label].append(float(val))
        return
    
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


def main(spec_file_name = None):
    """
    test the routines that read from the spec data file
    
    :param str spec_file_name: if set, spec file name is given on command line
    """
    if spec_file_name is None:
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'data')
        spec_dir = os.path.abspath(path)
        spec_file_name = os.path.join(spec_dir, 'APS_spec_data.dat')
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
        print scan.scanNum, scan.date, 'AR', scan.positioner['ar'], 'eV', 1e3*scan.metadata['DCM_energy']
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
    # test = SpecDataFile('07_02_sn281_8950.dat')
    print test.getScan(1).L
    print test.getScan(5)


if __name__ == "__main__":
    main()
