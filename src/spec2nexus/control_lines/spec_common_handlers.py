#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''
provide SPEC data file header

Also serves as an example of a Control Line plugin file.
Can define handlers for one or more Control Lines.
Each handler is a subclass of spec2nexus.plugin.ControlLineHandler

:see: SPEC manual, *Standard Data File Format*, http://www.certif.com/spec_manual/user_1_4_1.html
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


import re
from spec2nexus.plugin import ControlLineHandler
from spec2nexus.pySpec import SpecDataFileHeader, SpecDataFileScan, DuplicateSpecScanNumber, strip_first_word

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# header block

# TODO: add comment to each class

class CL_File(ControlLineHandler):
    key_regexp = '#F'
    
    def process(self, text, spec_file_obj, *args, **kws):
        spec_file_obj.specFile = strip_first_word(text)


class CL_Epoch(ControlLineHandler):
    key_regexp = '#E'
    
    def process(self, buf, spec_obj, *args, **kws):
        header = SpecDataFileHeader(buf, parent=spec_obj)
        line = buf.splitlines()[0].strip()
        header.epoch = int(strip_first_word(line))
        header.interpret()                  # parse the full header
        spec_obj.headers.append(header)
        


class CL_Date(ControlLineHandler):
    key_regexp = '#D'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.date = strip_first_word(text)


class CL_Comment(ControlLineHandler):
    key_regexp = '#C'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.comments.append( strip_first_word(text) )

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# scan block

class CL_Geometry(ControlLineHandler):
    key_regexp = '#G\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        subkey = text.split()[0].lstrip('#')
        spec_obj.G[subkey] = strip_first_word(text)

class CL_NormalizingFactor(ControlLineHandler):
    key_regexp = 'I'

    def process(self, text, spec_obj, *args, **kws):
        spec_obj.I = int(strip_first_word(text))

class CL_CounterNames(ControlLineHandler):
    key_regexp = '#J\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        pass    # ignore this for now

class CL_CounterMnes(ControlLineHandler):
    key_regexp = '#j\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        pass    # ignore this for now

class CL_Labels(ControlLineHandler):
    key_regexp = '#L'
    
    def process(self, text, spec_obj, *args, **kws):
        # Some folks use more than two spaces!  Use regular expression(re) module
        spec_obj.L = re.split("  +", strip_first_word(text))
        spec_obj.column_first = spec_obj.L[0]
        spec_obj.column_last = spec_obj.L[-1]

class CL_Monitor(ControlLineHandler):
    key_regexp = '#M'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.M, dname = strip_first_word(text).split()
        spec_obj.monitor_name = dname.lstrip('(').rstrip(')')

class CL_NumColumns(ControlLineHandler):
    key_regexp = '#N'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.N = int(strip_first_word(text))

class CL_PositionerNames(ControlLineHandler):
    key_regexp = '#O\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.O.append( strip_first_word(text).split() )

class CL_PositionerMnes(ControlLineHandler):
    key_regexp = '#o\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        pass    # ignore this for now

class CL_Positioners(ControlLineHandler):
    key_regexp = '#P\d+'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.P.append( strip_first_word(text) )
        spec_obj.addPostProcessor('motor_positions', motor_positions_postprocessing)

class CL_HKL(ControlLineHandler):
    key_regexp = '#Q'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.Q = strip_first_word(text)

class CL_Scan(ControlLineHandler):
    key_regexp = '#S'
    
    def process(self, part, spec_obj, *args, **kws):
        scan = SpecDataFileScan(spec_obj.headers[-1], part, parent=spec_obj)
        text = part.splitlines()[0].strip()
        scan.S = strip_first_word(text)
        pos = scan.S.find(' ')
        scan.scanNum = int(scan.S[0:pos])
        scan.scanCmd = strip_first_word(scan.S[pos+1:])
        if scan.scanNum in spec_obj.scans:
            msg = str(scan.scanNum) + ' in ' + spec_obj.fileName
            raise DuplicateSpecScanNumber(msg)
        spec_obj.scans[scan.scanNum] = scan

class CL_Time(ControlLineHandler):
    key_regexp = '#T'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.T = strip_first_word(text).split()[0]

class CL_TemperatureSetPoint(ControlLineHandler):
    key_regexp = '#X'
    
    def process(self, text, spec_obj, *args, **kws):
        try:
            x = float( strip_first_word(text) )
        except ValueError:
            # #X       setpoint       The temperature setpoint. 
            # def Fheader '_cols++;printf("#X %gKohm (%gC)\n",TEMP_SP,DEGC_SP)'
            x = strip_first_word(text)  # might have trailing text: 12.345kZ
        spec_obj.X = x

class CL_DataLine(ControlLineHandler):
    key_regexp = r'[+-]?\d*\.?\d?'
    
    def process(self, text, spec_obj, *args, **kws):
        spec_obj.data_lines.append(text)
        spec_obj.addPostProcessor('data_lines', data_lines_postprocessing)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# MCA: multi-channel analyzer

class CL_MCA(ControlLineHandler):
    key_regexp = '#@MCA'

class CL_MCA_Array(ControlLineHandler):
    key_regexp = '@A'

class CL_MCA_Calibration(ControlLineHandler):
    key_regexp = '#@CALIB'

class CL_MCA_ChannelInformation(ControlLineHandler):
    key_regexp = '#@CHANN'

class CL_MCA_CountTime(ControlLineHandler):
    key_regexp = '#@CTIME'

class CL_MCA_RegionOfInterest(ControlLineHandler):
    key_regexp = '#@ROI'

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def data_lines_postprocessing(scan):
    '''
    interpret the data lines from the body of the scan
    
    :param SpecDataFileScan scan: data from a single SPEC scan
    '''
    # interpret the data lines from the body of the scan
    scan.data = {}
    for col in range(len(scan.L)):
        label = scan._unique_key(scan.L[col], scan.data.keys())
        # need to guard when same column label is used more than once
        if label != scan.L[col]:
            scan.L[col] = label    # rename this column's label
        scan.data[label] = []
    in_array_data = False
    for row, values in enumerate(scan.data_lines):
        if values.startswith('@A'):     # Can there be more than 1 specified?    # TODO: move to plugin
            in_array_data = True
            if '_mca_' not in scan.data:
                scan.data['_mca_'] = []
            mca_spectrum = []       # accumulate this spectrum
            values = values[2:]     # strip the header
        if in_array_data:
            if not values.endswith('\\'):
                in_array_data = False       # last row of this spectrum
            mca_spectrum += map(float, values.rstrip('\\').split())
            if not in_array_data:   # last step, add to data column
                scan.data['_mca_'].append(mca_spectrum)
        else:
            buf = scan._interpret_data_row(values)
            if len(buf) == len(scan.data):      # only keep complete rows
                for label, val in buf.items():
                    scan.data[label].append(val)


def motor_positions_postprocessing(scan):
    '''
    interpret the motor positions from the scan header
    
    :param SpecDataFileScan scan: data from a single SPEC scan
    '''
    scan.positioner = {}
    for row, values in enumerate(scan.P):
        for col, val in enumerate(values.split()):
            if row >= len(scan.header.O):
                pass
            if col >= len(scan.header.O[row]):
                pass
            mne = scan.header.O[row][col]
            scan.positioner[mne] = float(val)
